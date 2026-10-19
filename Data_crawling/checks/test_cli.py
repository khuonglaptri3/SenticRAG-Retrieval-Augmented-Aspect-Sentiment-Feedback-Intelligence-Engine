import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from url_discovery.cli import main


class CLITests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        (self.workspace / "configs").mkdir()
        (self.workspace / "configs/cellphones.toml").write_text(
            'allowed_hosts = ["cellphones.com.vn"]\nseed_urls = ["https://cellphones.com.vn/"]\n'
        )
        self.stdout = io.StringIO()
        self.stderr = io.StringIO()

    def run_cli(self, *arguments):
        with contextlib.redirect_stdout(self.stdout), contextlib.redirect_stderr(self.stderr):
            return main(list(arguments), workspace=self.workspace)

    def test_dry_run_needs_no_key_and_creates_no_output(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(self.run_cli("--mode", "combined", "--dry-run"), 0)
        self.assertFalse((self.workspace / "outputs").exists())
        self.assertIn("cellphones.com.vn", self.stdout.getvalue())

    def test_missing_key_fails_without_creating_output(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(self.run_cli("--mode", "map"), 2)
        self.assertFalse((self.workspace / "outputs").exists())
        self.assertIn("FIRECRAWL_API_KEY", self.stderr.getvalue())

    def test_combined_failure_preserves_map_urls_and_reports_partial(self):
        def mapped(config, inventory, key):
            inventory.add("https://cellphones.com.vn/a", "map")
            return {"provider": "firecrawl", "errors": [], "limit_reached": False}

        with (
            patch.dict(os.environ, {"FIRECRAWL_API_KEY": "fake"}),
            patch("url_discovery.cli.collect_map", side_effect=mapped),
            patch("url_discovery.cli.run_browser", side_effect=RuntimeError("Browser unavailable")),
        ):
            self.assertEqual(self.run_cli("--mode", "combined"), 1)
        report_file = next((self.workspace / "outputs").glob("*/report.json"))
        report = json.loads(report_file.read_text())
        self.assertEqual(report["status"], "partial")
        self.assertFalse(report["coverage_complete"])
        self.assertEqual(
            (report_file.parent / "urls.txt").read_text(), "https://cellphones.com.vn/a\n"
        )

    def test_interruption_saves_discovered_urls(self):
        def interrupted(config, inventory, workspace):
            inventory.add("https://cellphones.com.vn/found", "browser")
            raise KeyboardInterrupt

        with patch("url_discovery.cli.run_browser", side_effect=interrupted):
            self.assertEqual(self.run_cli("--mode", "browser"), 130)
        report_file = next((self.workspace / "outputs").glob("*/report.json"))
        self.assertEqual(json.loads(report_file.read_text())["status"], "interrupted")
        self.assertIn(
            "https://cellphones.com.vn/found", (report_file.parent / "urls.txt").read_text()
        )

    def test_repeated_runs_do_not_overwrite_previous_run(self):
        with (
            patch.dict(os.environ, {"FIRECRAWL_API_KEY": "fake"}),
            patch(
                "url_discovery.cli.collect_map",
                return_value={"provider": "firecrawl", "errors": [], "limit_reached": False},
            ),
        ):
            self.assertEqual(self.run_cli(), 0)
            self.assertEqual(self.run_cli(), 0)
        self.assertEqual(len(list((self.workspace / "outputs").glob("*/report.json"))), 2)

    def test_stage_errors_survive_later_browser_failure(self):
        failure = {
            "provider": "firecrawl",
            "errors": [{"error": "Map rate limit"}],
            "limit_reached": False,
        }
        with (
            patch.dict(os.environ, {"FIRECRAWL_API_KEY": "fake"}),
            patch("url_discovery.cli.collect_map", return_value=failure),
            patch("url_discovery.cli.run_browser", side_effect=RuntimeError("Browser unavailable")),
        ):
            self.assertEqual(self.run_cli("--mode", "combined"), 1)
        report_file = next((self.workspace / "outputs").glob("*/report.json"))
        errors = json.loads(report_file.read_text())["errors"]
        self.assertEqual(
            {entry["error"] for entry in errors}, {"Map rate limit", "Browser unavailable"}
        )

    def test_export_failure_is_not_printed_as_completed(self):
        with (
            patch.dict(os.environ, {"FIRECRAWL_API_KEY": "fake"}),
            patch(
                "url_discovery.cli.collect_map", return_value={"errors": [], "limit_reached": False}
            ),
            patch("url_discovery.cli.Inventory.write", side_effect=OSError("disk full")),
        ):
            self.assertEqual(self.run_cli(), 1)
        self.assertIn("not fully saved", self.stdout.getvalue())

    def test_explicit_tls_settings_are_preserved_for_browser_run(self):
        observed = []

        def browser(config, inventory, workspace):
            observed.append(
                (os.environ.get("SSL_CERT_FILE"), os.environ.get("NODE_EXTRA_CA_CERTS"))
            )
            return {"errors": [], "limit_reached": False}

        with (
            patch.dict(
                os.environ,
                {
                    "SSL_CERT_FILE": "/custom/python-ca.pem",
                    "NODE_EXTRA_CA_CERTS": "/custom/node-ca.pem",
                },
            ),
            patch("url_discovery.cli.run_browser", side_effect=browser),
        ):
            self.assertEqual(self.run_cli("--mode", "browser"), 0)
        self.assertEqual(observed, [("/custom/python-ca.pem", "/custom/node-ca.pem")])

    @unittest.skipUnless(
        Path("/etc/ssl/certs/ca-certificates.crt").is_file(), "Ubuntu/Debian system CA bundle"
    )
    def test_browser_defaults_to_system_ca_when_environment_is_unset(self):
        observed = []

        def browser(config, inventory, workspace):
            observed.append(
                (os.environ.get("SSL_CERT_FILE"), os.environ.get("NODE_EXTRA_CA_CERTS"))
            )
            return {"errors": [], "limit_reached": False}

        with (
            patch.dict(os.environ, {}, clear=True),
            patch("url_discovery.cli.run_browser", side_effect=browser),
        ):
            self.assertEqual(self.run_cli("--mode", "browser"), 0)
        self.assertEqual(
            observed, [("/etc/ssl/certs/ca-certificates.crt", "/etc/ssl/certs/ca-certificates.crt")]
        )


if __name__ == "__main__":
    unittest.main()
