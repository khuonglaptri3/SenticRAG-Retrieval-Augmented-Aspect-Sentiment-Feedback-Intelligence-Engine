"""Real Firefox smoke check with synthetic pages; no external network calls.

Run: .venv/bin/python -m checks.browser_smoke
"""

import os
from pathlib import Path

from playwright.sync_api import sync_playwright

from url_discovery.core import Config
from url_discovery.providers import extract_rendered_links


def main():
    workspace = Path(__file__).resolve().parents[1]
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(workspace / ".browsers")
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=True)
        try:
            page = browser.new_page()
            page.route("**/*", lambda route: route.abort())
            page.set_content("""
                <base href="https://cellphones.com.vn/">
                <a href="/static">Static navigation</a>
                <div style="height: 3000px"></div>
                <script>
                    const dynamic = document.createElement('a');
                    dynamic.href = '/dynamic?page=2';
                    document.body.append(dynamic);
                    window.addEventListener('scroll', () => {
                        const lazy = document.createElement('a');
                        lazy.href = '/after-scroll';
                        document.body.append(lazy);
                    }, {once: true});
                </script>
            """)
            config = Config(
                allowed_hosts=["cellphones.com.vn"],
                seed_urls=[],
                scroll_steps=2,
                render_wait_ms=100,
            )
            links = extract_rendered_links(page, config)
            assert links == [
                "https://cellphones.com.vn/after-scroll",
                "https://cellphones.com.vn/dynamic?page=2",
                "https://cellphones.com.vn/static",
            ], links
            print(
                "PASS: Firefox extracted static, JavaScript-generated, and scroll-triggered URLs."
            )
        finally:
            browser.close()


if __name__ == "__main__":
    main()
