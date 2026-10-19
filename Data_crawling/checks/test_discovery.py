"""Offline behavioral tests; run from Data_crawling with unittest discovery."""

import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from urllib.error import HTTPError

from url_discovery.core import Config, Inventory, load_config, normalize_url, workspace_path
from url_discovery.providers import (
    PageLinks,
    RobotsPolicy,
    collect_browser,
    collect_map,
    guard_request,
    map_urls,
)


class URLTests(unittest.TestCase):
    def test_normalization_preserves_distinct_pages(self):
        self.assertEqual(
            normalize_url(
                "/Product/?page=2&utm_source=test&variant=Red#reviews",
                "https://CELLPHONES.com.vn:443",
            ),
            "https://cellphones.com.vn/Product/?page=2&variant=Red",
        )
        self.assertNotEqual(
            normalize_url("https://cellphones.com.vn/a"),
            normalize_url("https://cellphones.com.vn/a/"),
        )
        self.assertNotEqual(
            normalize_url("https://cellphones.com.vn/?page=1"),
            normalize_url("https://cellphones.com.vn/?page=2"),
        )
        self.assertEqual(
            normalize_url("https://cellphones.com.vn/?token=a%2Fb&x=1+2"),
            "https://cellphones.com.vn/?token=a%2Fb&x=1+2",
        )

    def test_invalid_or_credentialed_links_are_rejected(self):
        for url in (
            "javascript:alert(1)",
            "mailto:a@example.com",
            "https://u:p@cellphones.com.vn/",
            "https://[broken",
            "https://cellphones.com.vn:bad",
            "https://cellphones.com.vn/a\nb",
        ):
            with self.subTest(url=url):
                self.assertIsNone(normalize_url(url))

    def test_inventory_exact_host_scope_and_merged_sources(self):
        inventory = Inventory(["cellphones.com.vn"])
        inventory.add("https://cellphones.com.vn/a#top", "map")
        inventory.add("https://cellphones.com.vn/a?utm_source=test", "browser")
        inventory.add("https://cellphones.com.vn.evil.test/a", "browser")
        inventory.add("https://shop.cellphones.com.vn/a", "map")
        inventory.add("https://cellphones.com.vn:8443/a", "browser")
        self.assertEqual(inventory.urls, ["https://cellphones.com.vn/a"])
        self.assertEqual(inventory.records()[0]["sources"], ["browser", "map"])

    def test_export_contains_urls_not_document_text(self):
        inventory = Inventory(["cellphones.com.vn"])
        inventory.add("https://cellphones.com.vn/a", "map")
        with tempfile.TemporaryDirectory() as directory:
            inventory.write(Path(directory), {"status": "partial"})
            self.assertEqual(
                (Path(directory) / "urls.txt").read_text(), "https://cellphones.com.vn/a\n"
            )
            self.assertEqual(
                json.loads((Path(directory) / "report.json").read_text())["status"], "partial"
            )


class ConfigTests(unittest.TestCase):
    def test_output_cannot_escape_workspace_or_follow_external_symlink(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory)
            with self.assertRaises(ValueError):
                workspace_path(root, "../outside")
            (root / "escape").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                workspace_path(root, "escape/output")

    def test_config_rejects_out_of_scope_seeds_and_zero_page_budget(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "config.toml"
            for extra in (
                'seed_urls = ["https://other.test/"]',
                'seed_urls = ["https://cellphones.com.vn/"]\n[browser]\nmax_pages = 0',
            ):
                path.write_text('allowed_hosts = ["cellphones.com.vn"]\n' + extra)
                with self.assertRaises(ValueError):
                    load_config(root, "config.toml")


class MapTests(unittest.TestCase):
    def test_map_sends_scope_and_keeps_only_urls(self):
        def respond(request, timeout):
            payload = json.loads(request.data)
            self.assertFalse(payload["includeSubdomains"])
            self.assertFalse(payload["ignoreQueryParameters"])
            self.assertEqual(payload["url"], "https://cellphones.com.vn/")
            self.assertEqual(request.get_header("Authorization"), "Bearer fake-test-key")
            return io.BytesIO(
                json.dumps(
                    {
                        "success": True,
                        "links": [
                            {
                                "url": "https://cellphones.com.vn/a",
                                "title": "Do not export",
                                "description": "Do not export",
                            }
                        ],
                    }
                ).encode()
            )

        with patch("url_discovery.providers.urlopen", side_effect=respond):
            self.assertEqual(
                map_urls("https://cellphones.com.vn/", "fake-test-key", 100, 10),
                ["https://cellphones.com.vn/a"],
            )

    def test_api_failure_does_not_leak_response_body(self):
        error = HTTPError(
            "https://api.firecrawl.dev/v2/map", 401, "Unauthorized", {}, io.BytesIO(b"secret-key")
        )
        with patch("url_discovery.providers.urlopen", side_effect=error):
            with self.assertRaisesRegex(RuntimeError, "401") as caught:
                map_urls("https://cellphones.com.vn/", "secret-key", 100, 10)
        self.assertNotIn("secret-key", str(caught.exception))

    def test_malformed_response_is_not_reported_as_empty_success(self):
        for payload in ({"success": False}, {"success": True}, {"success": True, "links": [123]}):
            with patch(
                "url_discovery.providers.urlopen",
                return_value=io.BytesIO(json.dumps(payload).encode()),
            ):
                with self.assertRaises(RuntimeError):
                    map_urls("https://cellphones.com.vn/", "fake", 100, 10)

    def test_partial_map_preserves_first_seed_and_records_limit(self):
        config = Config(
            allowed_hosts=["cellphones.com.vn"],
            seed_urls=["https://cellphones.com.vn/", "https://cellphones.com.vn/help"],
            map_limit=1,
        )
        inventory = Inventory(config.allowed_hosts)
        with patch(
            "url_discovery.providers.map_urls",
            side_effect=[["https://cellphones.com.vn/a"], RuntimeError("HTTP 429")],
        ):
            report = collect_map(config, inventory, "fake")
        self.assertIn("https://cellphones.com.vn/a", inventory.urls)
        self.assertEqual(len(report["errors"]), 1)
        self.assertTrue(report["limit_reached"])


class BrowserTests(unittest.TestCase):
    def config(self, **kwargs):
        return Config(
            allowed_hosts=["cellphones.com.vn"],
            seed_urls=["https://cellphones.com.vn/"],
            browser_delay=0,
            **kwargs,
        )

    def test_traversal_handles_cycles_and_keeps_document_urls(self):
        pages = {
            "https://cellphones.com.vn/": ["/a", "/manual.pdf", "https://other.test/", "/blocked"],
            "https://cellphones.com.vn/a": ["/", "/b?variant=2"],
            "https://cellphones.com.vn/b?variant=2": [],
        }
        visited = []

        def fetch(url):
            visited.append(url)
            return PageLinks(url, pages[url])

        inventory = Inventory(["cellphones.com.vn"])
        report = collect_browser(
            self.config(browser_max_pages=10),
            inventory,
            fetch,
            lambda url: not url.endswith("/blocked"),
        )
        self.assertEqual(
            visited,
            [
                "https://cellphones.com.vn/",
                "https://cellphones.com.vn/a",
                "https://cellphones.com.vn/b?variant=2",
            ],
        )
        self.assertIn("https://cellphones.com.vn/manual.pdf", inventory.urls)
        self.assertIn("https://cellphones.com.vn/blocked", inventory.urls)
        self.assertEqual(report["skipped_robots"], 1)
        self.assertFalse(report["limit_reached"])

    def test_page_limit_is_reported_without_losing_discovered_links(self):
        inventory = Inventory(["cellphones.com.vn"])
        report = collect_browser(
            self.config(browser_max_pages=1),
            inventory,
            lambda url: PageLinks(url, ["/a", "/b"]),
            lambda url: True,
        )
        self.assertEqual(len(inventory.urls), 3)
        self.assertEqual(report["visited"], 1)
        self.assertTrue(report["limit_reached"])

    def test_failed_page_and_external_redirect_are_recorded(self):
        inventory = Inventory(["cellphones.com.vn"])
        report = collect_browser(
            self.config(),
            inventory,
            lambda url: PageLinks("https://outside.test/", ["https://cellphones.com.vn/untrusted"]),
            lambda url: True,
        )
        self.assertNotIn("https://cellphones.com.vn/untrusted", inventory.urls)
        self.assertEqual(len(report["errors"]), 1)


class NavigationTests(unittest.TestCase):
    def test_redirect_is_queued_without_following_it_automatically(self):
        calls = []

        class Response:
            status = 302
            headers = {"location": "/new-page"}

            def dispose(self):
                pass

        class Route:
            request = SimpleNamespace(
                method="GET",
                url="https://cellphones.com.vn/old",
                resource_type="document",
                is_navigation_request=lambda: True,
            )

            def fetch(self, **kwargs):
                calls.append(kwargs)
                return Response()

            def fulfill(self, **kwargs):
                self.result = kwargs

            def abort(self):
                self.result = "blocked"

        route = Route()
        redirects = []
        guard_request(
            route,
            Inventory(["cellphones.com.vn"]),
            SimpleNamespace(allowed=lambda url: url.endswith("/old")),
            redirects,
            1000,
        )
        self.assertEqual(calls, [{"max_redirects": 0, "timeout": 1000}])
        self.assertEqual(redirects, ["https://cellphones.com.vn/new-page"])
        self.assertEqual(route.result["status"], 200)

        # The redirected URL is still a discovery, even when robots forbids a visit.
        inventory = Inventory(["cellphones.com.vn"])
        report = collect_browser(
            Config(
                allowed_hosts=["cellphones.com.vn"],
                seed_urls=["https://cellphones.com.vn/old"],
                browser_delay=0,
            ),
            inventory,
            lambda url: PageLinks(url, redirects),
            lambda url: url.endswith("/old"),
        )
        self.assertIn("https://cellphones.com.vn/new-page", inventory.urls)
        self.assertEqual(report["visited"], 1)
        self.assertEqual(report["skipped_robots"], 1)

    def test_external_navigation_is_aborted_before_fetch(self):
        class Route:
            request = SimpleNamespace(
                method="GET",
                url="https://outside.test/",
                resource_type="document",
                is_navigation_request=lambda: True,
            )

            def fetch(self, **kwargs):
                raise AssertionError("Out-of-scope page must not be fetched")

            def abort(self):
                self.blocked = True

        route = Route()
        guard_request(
            route,
            Inventory(["cellphones.com.vn"]),
            SimpleNamespace(allowed=lambda url: True),
            [],
            1000,
        )
        self.assertTrue(route.blocked)


class RobotsTests(unittest.TestCase):
    def test_wildcards_allow_exceptions_and_crawl_delay(self):
        body = b"User-agent: *\nDisallow: /*?*\nAllow: /public?*\nCrawl-delay: 2\n"
        with patch("url_discovery.providers.urlopen", return_value=io.BytesIO(body)):
            policy = RobotsPolicy()
            self.assertFalse(policy.allowed("https://cellphones.com.vn/private?x=1"))
            self.assertTrue(policy.allowed("https://cellphones.com.vn/public?x=1"))
            self.assertEqual(policy.delay_for("https://cellphones.com.vn/"), 2)

    def test_missing_robots_allows_but_service_failure_does_not(self):
        for status, expected in ((404, True), (503, False), (403, False)):
            with patch(
                "url_discovery.providers.urlopen",
                side_effect=HTTPError("https://cellphones.com.vn/robots.txt", status, "", {}, None),
            ):
                policy = RobotsPolicy()
                self.assertEqual(policy.allowed("https://cellphones.com.vn/"), expected)
                self.assertEqual(bool(policy.errors), not expected)


if __name__ == "__main__":
    unittest.main()
