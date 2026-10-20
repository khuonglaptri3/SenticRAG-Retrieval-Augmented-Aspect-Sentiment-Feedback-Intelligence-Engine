import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from url_discovery import scraper


class ScraperTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        (self.workspace / "Evident").mkdir()
        self.source = self.workspace / "Evident/policy_urls.txt"
        self.source.write_text(
            "https://example.com/first?part=refund-policy\n"
            "https://example.com/second\n"
            "https://example.com/first?part=privacy-policy\n",
            encoding="utf-8",
        )

    def test_urls_preserve_file_order_and_meaningful_queries(self):
        with self.source.open("a") as stream:
            stream.write("\nhttps://example.com/second\n")
        self.assertEqual(
            scraper.load_urls(self.source),
            [
                "https://example.com/first?part=refund-policy",
                "https://example.com/second",
                "https://example.com/first?part=privacy-policy",
            ],
        )

    def test_invalid_input_is_rejected_before_crawling(self):
        self.source.write_text("https://example.com/good\nfile:///etc/passwd\n")
        with self.assertRaisesRegex(ValueError, "line 2"):
            scraper.load_urls(self.source)

    def test_scope_matches_input_hosts_and_ports_exactly(self):
        scope = scraper.InputScope(["https://example.com/a", "http://127.0.0.1:8765/test"])
        self.assertTrue(scope.accepts("https://example.com:443/b"))
        self.assertTrue(scope.accepts("http://127.0.0.1:8765/policy"))
        self.assertFalse(scope.accepts("http://127.0.0.1:8766/policy"))
        self.assertFalse(scope.accepts("https://example.com.evil.test/b"))
        self.assertFalse(scope.accepts("https://example.com:444/b"))

    def test_interruption_preserves_completed_pages_and_reports_interrupted(self):
        def fetch(url):
            if url.endswith("second"):
                raise KeyboardInterrupt
            return self.captured_page(url)

        directory = self.workspace / "Evident/raw/test"
        report = scraper.run_pipeline(scraper.load_urls(self.source), directory, fetch, 0)
        self.assertEqual(report["status"], "interrupted")
        self.assertEqual(report["succeeded"], 1)
        self.assertEqual(report["attempted"], 1)
        self.assertTrue((directory / "0001/text.txt").exists())
        self.assertFalse((directory / "0003").exists())

    @staticmethod
    def captured_page(url):
        return {
            "final_url": url,
            "http_status": 200,
            "title": "Chính sách giao hàng",
            "content_type": "text/html; charset=utf-8",
            "response_body": "<html>Giao hàng</html>".encode(),
            "rendered_html": "<html><body>Giao hàng sau JavaScript</body></html>",
            "text": "Giao hàng sau JavaScript",
        }

    def test_sequential_pipeline_continues_after_failure_and_saves_raw_data(self):
        urls = scraper.load_urls(self.source)
        calls = []

        def fetch(url):
            calls.append(url)
            # First result must already be persisted when the next URL is fetched.
            if len(calls) == 2:
                self.assertTrue((directory / "0001/page.json").exists())
                raise RuntimeError("Page unavailable")
            return self.captured_page(url)

        directory = self.workspace / "Evident/raw/test"
        report = scraper.run_pipeline(urls, directory, fetch, delay_seconds=0)
        self.assertEqual(calls, urls)
        self.assertEqual(report["status"], "partial")
        self.assertEqual((report["succeeded"], report["failed"]), (2, 1))
        self.assertEqual(report["attempted"], 3)
        first = directory / "0001"
        self.assertEqual((first / "response.html").read_bytes(), b"<html>Giao h\xc3\xa0ng</html>")
        self.assertIn("sau JavaScript", (first / "rendered.html").read_text())
        self.assertEqual((first / "text.txt").read_text(), "Giao hàng sau JavaScript")
        record = json.loads((first / "page.json").read_text())
        self.assertEqual(record["requested_url"], urls[0])
        self.assertEqual(record["text"], "Giao hàng sau JavaScript")
        self.assertEqual(record["http_status"], 200)
        self.assertEqual(record["status"], "succeeded")
        failure = json.loads((directory / "0002/page.json").read_text())
        self.assertEqual(failure["error"], "Page unavailable")
        self.assertEqual(json.loads((directory / "report.json").read_text()), report)

    def test_http_error_retains_response_but_is_not_reported_as_success(self):
        def fetch(url):
            return {**self.captured_page(url), "http_status": 404}

        directory = self.workspace / "Evident/raw/test"
        report = scraper.run_pipeline(["https://example.com/missing"], directory, fetch, 0)
        self.assertEqual(report["status"], "failed")
        self.assertEqual(report["failed"], 1)
        self.assertTrue((directory / "0001/response.html").exists())

    def test_limit_one_tests_first_url_and_default_processes_all(self):
        calls = []

        @contextlib.contextmanager
        def browser_fetch(workspace, urls, **kwargs):
            def fetch(url):
                calls.append(url)
                return self.captured_page(url)

            yield fetch

        with (
            patch.object(scraper, "browser_fetch", browser_fetch),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            self.assertEqual(
                scraper.main(["--limit", "1", "--delay-seconds", "0"], workspace=self.workspace),
                0,
            )
            self.assertEqual(calls, [scraper.load_urls(self.source)[0]])
            calls.clear()
            self.assertEqual(scraper.main(["--delay-seconds", "0"], workspace=self.workspace), 0)
            self.assertEqual(calls, scraper.load_urls(self.source))
        self.assertEqual(len(list((self.workspace / "Evident/raw").glob("*/report.json"))), 2)

    def test_output_cannot_escape_workspace(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(
                scraper.main(["--output-dir", "../outside"], workspace=self.workspace), 2
            )
        self.assertFalse((self.workspace / "Evident/raw").exists())


if __name__ == "__main__":
    unittest.main()
