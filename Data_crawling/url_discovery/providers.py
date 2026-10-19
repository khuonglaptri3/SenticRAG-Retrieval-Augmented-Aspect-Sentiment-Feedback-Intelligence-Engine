"""Firecrawl Map and bounded Playwright URL discovery."""

import json
import os
import time
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

from .core import Config, Inventory

USER_AGENT = "SenticRAG-URL-Discovery/0.1"
DOCUMENT_SUFFIXES = {
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".zip",
    ".gz",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".svg",
    ".webp",
    ".mp4",
    ".mp3",
    ".css",
    ".js",
    ".xml",
}


def map_urls(seed: str, api_key: str, limit: int, timeout: float) -> list[str]:
    request = Request(
        "https://api.firecrawl.dev/v2/map",
        data=json.dumps(
            {
                "url": seed,
                "sitemap": "include",
                "includeSubdomains": False,
                "ignoreQueryParameters": False,
                "limit": limit,
                "timeout": int(timeout * 1000),
            }
        ).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout + 10) as response:
            payload = json.load(response)
    except HTTPError as error:
        raise RuntimeError(
            f"Firecrawl returned HTTP {error.code}; check API access, credit balance, or rate limits."
        ) from None
    except (URLError, TimeoutError, OSError) as error:
        raise RuntimeError(
            f"Firecrawl request failed ({type(error).__name__}); check connectivity."
        ) from None
    except (ValueError, UnicodeError):
        raise RuntimeError("Firecrawl returned an invalid JSON response.") from None
    if (
        not isinstance(payload, dict)
        or payload.get("success") is not True
        or not isinstance(payload.get("links"), list)
    ):
        raise RuntimeError("Firecrawl response did not contain a successful links list.")
    if any(
        not isinstance(link, dict) or not isinstance(link.get("url"), str)
        for link in payload["links"]
    ):
        raise RuntimeError("Firecrawl returned a malformed URL entry.")
    return [link["url"] for link in payload["links"]]


def collect_map(config: Config, inventory: Inventory, api_key: str) -> dict:
    report = {
        "provider": "firecrawl",
        "errors": [],
        "limit_reached": False,
        "seeds_processed": 0,
        "urls_returned": 0,
    }
    for seed in config.seed_urls:
        try:
            urls = map_urls(seed, api_key, config.map_limit, config.map_timeout)
            report["seeds_processed"] += 1
            report["urls_returned"] += len(urls)
            report["limit_reached"] |= len(urls) >= config.map_limit
            for url in urls:
                inventory.add(url, "map", seed)
        except RuntimeError as error:
            report["errors"].append({"url": seed, "error": str(error)})
    return report


@dataclass
class PageLinks:
    final_url: str
    links: list[str]
    warnings: list[str] = field(default_factory=list)


def collect_browser(config: Config, inventory: Inventory, fetch, allowed, delay_for=None) -> dict:
    """Breadth-first discovery; the fetch boundary can be tested offline."""
    queue = deque()
    scheduled = set()
    report = {
        "provider": "playwright",
        "visited": 0,
        "skipped_robots": 0,
        "skipped_documents": 0,
        "errors": [],
        "warnings": [],
        "limit_reached": False,
    }

    def enqueue(raw, parent=""):
        url = inventory.add(raw, "browser", parent)
        if url and url not in scheduled:
            scheduled.add(url)
            if Path(urlsplit(url).path).suffix.lower() in DOCUMENT_SUFFIXES:
                report["skipped_documents"] += 1
            else:
                queue.append(url)

    for seed in config.browser_seed_urls or config.seed_urls:
        enqueue(seed)
    while queue and report["visited"] < config.browser_max_pages:
        url = queue.popleft()
        try:
            if not allowed(url):
                report["skipped_robots"] += 1
                continue
            delay = max(config.browser_delay, delay_for(url) if delay_for else 0)
            if delay:
                time.sleep(delay)
            report["visited"] += 1
            result = fetch(url)
            if not inventory.accepts(result.final_url):
                raise RuntimeError("Navigation redirected outside allowed hosts.")
            if not allowed(result.final_url):
                raise RuntimeError("Navigation redirected to a robots-disallowed URL.")
            inventory.add(result.final_url, "browser", url)
            report["warnings"].extend(
                {"url": url, "warning": warning} for warning in result.warnings
            )
            for link in result.links:
                enqueue(link, result.final_url)
        except Exception as error:
            # Do not persist browser traces or response bodies; they can contain page text.
            message = str(error) if isinstance(error, RuntimeError) else type(error).__name__
            report["errors"].append({"url": url, "error": message})
    report["limit_reached"] = bool(queue)
    report["pending_pages"] = len(queue)
    return report


class RobotsPolicy:
    def __init__(self, timeout=15):
        try:
            from protego import Protego
        except ImportError:
            raise RuntimeError(
                "Install the standalone dependencies: .venv/bin/python -m pip install -e '.[browser]'"
            ) from None
        self.parser = Protego
        self.timeout = timeout
        self.cache = {}
        self.errors = []

    def _policy(self, url):
        parts = urlsplit(url)
        origin = f"{parts.scheme}://{parts.netloc}"
        if origin not in self.cache:
            try:
                request = Request(origin + "/robots.txt", headers={"User-Agent": USER_AGENT})
                with urlopen(request, timeout=self.timeout) as response:
                    text = response.read(1024 * 1024 + 1)
                    if len(text) > 1024 * 1024:
                        raise RuntimeError("robots.txt exceeded the 1 MiB read limit")
                    self.cache[origin] = self.parser.parse(text.decode("utf-8", errors="replace"))
            except HTTPError as error:
                if error.code in {404, 410}:
                    self.cache[origin] = self.parser.parse("")
                else:
                    self.cache[origin] = None
                    self.errors.append(
                        {
                            "url": origin + "/robots.txt",
                            "error": f"HTTP {error.code}; navigation skipped",
                        }
                    )
            except Exception as error:
                self.cache[origin] = None
                self.errors.append(
                    {
                        "url": origin + "/robots.txt",
                        "error": f"{type(error).__name__}; navigation skipped",
                    }
                )
        return self.cache[origin]

    def allowed(self, url):
        policy = self._policy(url)
        return policy is not None and policy.can_fetch(url, USER_AGENT)

    def delay_for(self, url):
        policy = self._policy(url)
        return float(policy.crawl_delay(USER_AGENT) or 0) if policy is not None else 0


def extract_rendered_links(page, config: Config) -> list[str]:
    """Read rendered anchors; do not save page bodies or link descriptions."""
    links = set(
        page.locator("a[href], area[href]").evaluate_all(
            "elements => elements.map(element => element.href)"
        )
    )
    for _ in range(config.scroll_steps):
        page.evaluate("window.scrollBy(0, Math.max(window.innerHeight, 800))")
        page.wait_for_timeout(config.render_wait_ms)
        links.update(
            page.locator("a[href], area[href]").evaluate_all(
                "elements => elements.map(element => element.href)"
            )
        )
    return sorted(links)


def guard_request(route, inventory: Inventory, robots, redirects: list[str], timeout: float):
    """Validate navigation before fetch, including every HTTP redirect target."""
    request = route.request
    if request.method not in {"GET", "HEAD"}:
        route.abort()
    elif request.is_navigation_request():
        if not inventory.accepts(request.url) or not robots.allowed(request.url):
            route.abort()
            return
        # Playwright's route handler does not intercept subsequent redirects.
        # Fetch one hop, then queue allowed destinations as independent visits.
        response = route.fetch(max_redirects=0, timeout=timeout)
        try:
            if response.status in {301, 302, 303, 307, 308}:
                destination = urljoin(request.url, response.headers.get("location", ""))
                if response.headers.get("location") and inventory.accepts(destination):
                    redirects.append(destination)
                    route.fulfill(status=200, content_type="text/html", body="<html></html>")
                else:
                    route.abort()
            else:
                route.fulfill(response=response)
        finally:
            response.dispose()
    elif request.resource_type in {"image", "media", "font"}:
        route.abort()
    else:
        route.continue_()


def run_browser(config: Config, inventory: Inventory, workspace: Path) -> dict:
    try:
        from playwright.sync_api import Error, sync_playwright
    except ImportError:
        raise RuntimeError(
            "Playwright is not installed. Run .venv/bin/python -m pip install -e '.[browser]' inside Data_crawling."
        ) from None
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(workspace / ".browsers")
    robots = RobotsPolicy()
    with sync_playwright() as playwright:
        try:
            browser = playwright.firefox.launch(headless=True)
        except Error:
            raise RuntimeError(
                "Firefox could not start. Install the local Playwright Firefox using the README command and check browser system dependencies."
            ) from None
        try:
            context = browser.new_context(
                user_agent=USER_AGENT, accept_downloads=False, service_workers="block"
            )
            redirects = []

            def guard(route):
                try:
                    guard_request(
                        route, inventory, robots, redirects, config.browser_timeout * 1000
                    )
                except Error:
                    route.abort()

            context.route("**/*", guard)
            page = context.new_page()
            page.set_default_timeout(config.browser_timeout * 1000)

            def fetch(url):
                redirects.clear()
                response = page.goto(
                    url, wait_until="domcontentloaded", timeout=config.browser_timeout * 1000
                )
                if response is None or response.status >= 400:
                    raise RuntimeError(
                        f"Page navigation failed (HTTP {response.status if response else 'unknown'})."
                    )
                if "html" not in response.headers.get("content-type", "").lower():
                    return PageLinks(page.url, [])
                page.wait_for_timeout(config.render_wait_ms)
                warnings = []
                links = set(extract_rendered_links(page, config))
                for selector in config.hover_selectors:
                    try:
                        page.locator(selector).first.hover(
                            timeout=min(config.browser_timeout * 1000, 3000)
                        )
                        page.wait_for_timeout(config.render_wait_ms)
                        links.update(extract_rendered_links(page, config))
                    except Error:
                        warnings.append(f"Could not hover configured selector: {selector}")
                links.update(redirects)
                return PageLinks(page.url, sorted(links), warnings)

            report = collect_browser(config, inventory, fetch, robots.allowed, robots.delay_for)
            report["errors"].extend(robots.errors)
            return report
        finally:
            browser.close()
