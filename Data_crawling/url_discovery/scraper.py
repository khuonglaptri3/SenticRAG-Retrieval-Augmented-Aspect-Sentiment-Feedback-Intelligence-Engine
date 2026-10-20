"""Sequential Playwright content capture from an existing URL inventory."""

import argparse
import json
import math
import os
import sys
import time
import uuid
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlsplit

from .core import normalize_url, workspace_path
from .providers import USER_AGENT, RobotsPolicy, guard_request


def timestamp():
    return datetime.now(UTC).isoformat()


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_urls(path: Path) -> list[str]:
    """Deduplicate in first-seen order, preserving meaningful query parameters."""
    urls: dict[str, None] = {}
    for index, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        url = normalize_url(line.strip())
        if url is None:
            raise ValueError(f"Invalid HTTP(S) URL on line {index} of {path.name}.")
        urls[url] = None
    if not urls:
        raise ValueError("The input file contains no URLs.")
    return list(urls)


class InputScope:
    """Exact input hosts and ports; also supports local fixture servers."""

    def __init__(self, urls):
        self.authorities = {urlsplit(normalize_url(url)).netloc for url in urls}

    def accepts(self, url):
        normalized = normalize_url(url)
        return normalized is not None and urlsplit(normalized).netloc in self.authorities


def run_pipeline(urls, directory: Path, fetch, delay_seconds=1.0):
    """Fetch and persist each URL before starting the next; continue on page errors."""
    directory.mkdir(parents=True, exist_ok=False)
    report = {
        "started_at": timestamp(),
        "status": "running",
        "total": len(urls),
        "attempted": 0,
        "succeeded": 0,
        "failed": 0,
        "pages": [],
    }
    write_json(directory / "report.json", report)
    try:
        for index, url in enumerate(urls, 1):
            if index > 1 and delay_seconds:
                time.sleep(delay_seconds)
            folder = directory / f"{index:04d}"
            folder.mkdir()
            record = {"index": index, "requested_url": url, "started_at": timestamp()}
            print(f"[{index}/{len(urls)}] {url}", flush=True)
            try:
                result = dict(fetch(url))
                response_body = result.pop("response_body")
                rendered_html = result.pop("rendered_html")
                (folder / "response.html").write_bytes(response_body)
                (folder / "rendered.html").write_text(rendered_html, encoding="utf-8")
                (folder / "text.txt").write_text(result["text"], encoding="utf-8")
                record.update(result)
                record["files"] = ["response.html", "rendered.html", "text.txt", "page.json"]
                if result["http_status"] >= 400:
                    raise RuntimeError(f"HTTP {result['http_status']}")
                if not result["text"].strip():
                    raise RuntimeError("Rendered page has no visible text.")
                record["status"] = "succeeded"
            except Exception as error:
                record.update(status="failed", error=str(error))
            record["finished_at"] = timestamp()
            write_json(folder / "page.json", record)
            report["pages"].append(
                {
                    "index": index,
                    "requested_url": url,
                    "status": record["status"],
                    "record": f"{index:04d}/page.json",
                }
            )
            report["attempted"] += 1
            report["succeeded" if record["status"] == "succeeded" else "failed"] += 1
            write_json(directory / "report.json", report)
        report["status"] = (
            "completed" if not report["failed"] else "partial" if report["succeeded"] else "failed"
        )
    except KeyboardInterrupt:
        report["status"] = "interrupted"
    finally:
        report["finished_at"] = timestamp()
        write_json(directory / "report.json", report)
    return report


def capture_page(context, url, scope, robots, timeout_ms, render_wait_ms):
    """Capture one page; explicitly validate every HTTP redirect before fetching it."""
    from playwright.sync_api import Error

    page = context.new_page()
    page.set_default_timeout(timeout_ms)
    redirects = []
    route_errors = []

    def guard(route):
        request = route.request
        if request.is_navigation_request() and request.frame != page.main_frame:
            route.abort()
            return
        try:
            guard_request(route, scope, robots, redirects, timeout_ms)
        except (Error, RuntimeError) as error:
            route_errors.append(str(error))
            route.abort()

    page.route("**/*", guard)
    try:
        destination = url
        seen = set()
        chain = []
        for _ in range(10):
            if destination in seen:
                raise RuntimeError("Redirect loop detected.")
            seen.add(destination)
            chain.append(destination)
            if not scope.accepts(destination):
                raise RuntimeError("Redirect destination is outside the input inventory's hosts.")
            if not robots.allowed(destination):
                raise RuntimeError("Navigation skipped by robots policy or robots fetch failure.")
            delay = robots.delay_for(destination)
            if delay:
                time.sleep(delay)
            redirects.clear()
            response = page.goto(destination, wait_until="domcontentloaded", timeout=timeout_ms)
            if redirects:
                destination = redirects[-1]
                continue
            break
        else:
            raise RuntimeError("Exceeded the limit of 10 redirect hops.")
        if response is None:
            raise RuntimeError("Navigation returned no HTTP response.")
        content_type = response.headers.get("content-type", "")
        if "html" not in content_type.lower():
            raise RuntimeError(
                f"Expected HTML but received {content_type or 'unknown content type'}."
            )
        response_body = response.body()
        page.locator("body").wait_for(state="attached")
        page.wait_for_timeout(render_wait_ms)
        # Bounded scrolling triggers lazy content without clicking page controls.
        for _ in range(3):
            page.evaluate("window.scrollBy(0, Math.max(window.innerHeight, 800))")
            page.wait_for_timeout(render_wait_ms)
        if not scope.accepts(page.url) or not robots.allowed(page.url):
            raise RuntimeError("Rendered page navigated outside the permitted scope.")
        if page.url != response.url:
            raise RuntimeError("Page navigated during rendering; rerun using the destination URL.")
        return {
            "final_url": page.url,
            "http_status": response.status,
            "title": page.title(),
            "content_type": content_type,
            "captured_at": timestamp(),
            "response_body": response_body,
            "rendered_html": page.content(),
            "text": page.locator("body").inner_text(),
            "text_scope": "body (includes navigation and footer)",
            "redirect_chain": chain,
            "warnings": route_errors,
        }
    finally:
        page.close()


@contextmanager
def browser_fetch(workspace, urls, *, timeout_seconds=30, render_wait_ms=750):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise RuntimeError(
            "Install Playwright: .venv/bin/python -m pip install -e '.[browser]'"
        ) from None

    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(workspace / ".browsers")
    system_ca = Path("/etc/ssl/certs/ca-certificates.crt")
    if system_ca.is_file():
        os.environ.setdefault("SSL_CERT_FILE", str(system_ca))
        os.environ.setdefault("NODE_EXTRA_CA_CERTS", str(system_ca))
    scope = InputScope(urls)
    robots = RobotsPolicy()
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=True)
        try:
            context = browser.new_context(
                user_agent=USER_AGENT,
                accept_downloads=False,
                service_workers="block",
                viewport={"width": 1440, "height": 1000},
            )
            yield lambda url: capture_page(
                context, url, scope, robots, timeout_seconds * 1000, render_wait_ms
            )
        finally:
            browser.close()


def main(argv=None, *, workspace=None):
    workspace = (workspace or Path(__file__).resolve().parents[1]).resolve()
    parser = argparse.ArgumentParser(
        description="Scrape saved URLs sequentially using Playwright Firefox."
    )
    parser.add_argument(
        "--input", default="Evident/policy_urls.txt", help="URL text file in this workspace"
    )
    parser.add_argument(
        "--output-dir", default="Evident/raw", help="Parent directory for new run folders"
    )
    parser.add_argument(
        "--limit", type=int, help="Process only the first N URLs; default: all URLs"
    )
    parser.add_argument(
        "--delay-seconds", type=float, default=1.0, help="Pause between URLs (default: 1)"
    )
    parser.add_argument("--timeout-seconds", type=float, default=30.0)
    parser.add_argument(
        "--render-wait-ms", type=int, default=750, help="Wait after loading and each of 3 scrolls"
    )
    args = parser.parse_args(argv)
    try:
        if args.limit is not None and args.limit < 1:
            raise ValueError("--limit must be at least 1.")
        if not math.isfinite(args.delay_seconds) or args.delay_seconds < 0:
            raise ValueError("--delay-seconds must be finite and nonnegative.")
        if not math.isfinite(args.timeout_seconds) or args.timeout_seconds <= 0:
            raise ValueError("--timeout-seconds must be finite and positive.")
        if args.render_wait_ms < 0:
            raise ValueError("--render-wait-ms must be nonnegative.")
        source = workspace_path(workspace, args.input)
        output = workspace_path(workspace, args.output_dir)
        urls = load_urls(source)
    except (ValueError, OSError) as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        return 2
    selected = urls[: args.limit] if args.limit else urls
    run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    directory = output / run_id
    try:
        with browser_fetch(
            workspace,
            urls,
            timeout_seconds=args.timeout_seconds,
            render_wait_ms=args.render_wait_ms,
        ) as fetch:
            report = run_pipeline(selected, directory, fetch, args.delay_seconds)
        report.update(
            source_file=str(source.relative_to(workspace)),
            available_urls=len(urls),
            limit=args.limit,
        )
        write_json(directory / "report.json", report)
    except Exception as error:
        print(f"Scraping failed: {error}", file=sys.stderr)
        return 1
    print(
        f"{report['status']}: {report['succeeded']} succeeded, {report['failed']} failed. Output: {directory}"
    )
    return 130 if report["status"] == "interrupted" else 1 if report["failed"] else 0
