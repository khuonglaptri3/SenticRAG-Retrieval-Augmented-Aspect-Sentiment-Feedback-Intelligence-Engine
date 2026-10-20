# Standalone company URL discovery and scraping

This folder contains an independent URL-discovery tool for CellphoneS. It uses
**Firecrawl Map** for an initial inventory and **Playwright Firefox** for additional
rendered links. The exported data contains URLs and discovery metadata, not page
text, product information, or policy contents.

A separate `scrape.py` command now captures page contents from the saved URL
inventory. Discovery and content scraping are separate steps.

## Scrape the saved policy URLs

Use the same local Python environment and Firefox installation described below.
The scraper processes `Evident/policy_urls.txt` **sequentially, in file order**.
It preserves query parameters such as `?part=refund-policy`, removes duplicate
URLs while keeping their first position, and continues after individual failures.
It does not follow discovered links to expand the inventory.

```bash
# Test the first URL only (deterministic).
.venv/bin/python scrape.py --limit 1

# Run the complete saved inventory sequentially.
.venv/bin/python scrape.py

# Optional input and timing settings; paths remain inside this workspace.
.venv/bin/python scrape.py --input Evident/policy_urls.txt --delay-seconds 2 --timeout-seconds 45
```

Each invocation creates a fresh folder under `Evident/raw/`:

```text
Evident/raw/<UTC timestamp>-<run id>/
  report.json          # source, counts, status, ordered page records
  0001/
    response.html      # original HTTP response body bytes, before JavaScript
    rendered.html      # DOM serialized after JavaScript and bounded scrolling
    text.txt           # full visible body text, including navigation and footer
    page.json          # requested/final URL, title, HTTP status, times, text, errors
  0002/                # next URL, and so on
```

These are raw captures: no summarization, content cleaning, or RAG chunking.
Vietnamese text and JSON are saved as UTF-8. Response bytes are saved in their
original encoding. HTTP error pages retain captured data but count as failures.
Navigation failures have a `page.json` error record. The report is saved after
each page; Ctrl+C preserves completed pages and marks the run interrupted.
Exit codes are `0` for success, `1` for scraping errors, `2` for invalid input,
and `130` for interruption. Generated captures are ignored by Git.

The scraper reuses the discovery robots policy and request guard. Redirects are
checked one hop at a time against robots and the exact hosts and ports in the input inventory.
It blocks non-GET/HEAD requests, embedded-frame navigation, service workers,
images, media, and fonts. Pages that rely on blocked requests may be incomplete.
Rendering waits are bounded; increase `--render-wait-ms` for slower pages.

Everything needed to run it lives here. You can copy this folder outside the
SenticRAG repository and use the same commands.

## Isolation

- Separate `pyproject.toml`, optional dependencies, virtual environment, config,
  browser binaries, tests, and output directory.
- No imports from the parent `apps/`, `packages/`, or `pipelines/` directories.
- No changes to the parent Poetry files, CI, application settings, or databases.
- Configuration and output paths are restricted to this folder, including when
  a symlink would otherwise point outside it.
- No automatic `.env` loading. Only an explicitly supplied process environment
  variable is used for the Firecrawl credential.
- Outputs, credentials, caches, browsers, and the virtual environment are ignored
  by this folder's `.gitignore`.

## Setup

Use Python 3.11 or newer. Start in this directory:

```bash
cd Data_crawling
python3 -m venv .venv
PIP_CACHE_DIR="$PWD/.cache/pip" .venv/bin/python -m pip install -e '.[browser,dev]'
PLAYWRIGHT_BROWSERS_PATH="$PWD/.browsers" .venv/bin/python -m playwright install firefox
```

For **Map only**, install with `pip install -e .` and skip the browser download.
If Firefox reports missing operating-system libraries, arrange those separately;
this project does not install system packages or change your existing environment.

Keep the browser-install environment variable shown above: runtime also uses
`Data_crawling/.browsers`, not your machine's shared Playwright browser cache.

On Ubuntu this uses Playwright's patched Firefox build, separately from your
normal Firefox installation. It does not open or modify your personal Firefox
profile. Playwright does not support automating the regular branded Firefox
binary; see the [Firefox browser documentation](https://playwright.dev/python/docs/browsers#firefox).

On Ubuntu/Debian, the runner defaults to the system CA bundle for Python HTTPS
and the Playwright driver. This avoids stale certificate bundles inherited from
Anaconda. Explicit `SSL_CERT_FILE` and `NODE_EXTRA_CA_CERTS` settings take
precedence. Certificate verification remains enabled; no system files are changed.

## Validate without network access

```bash
.venv/bin/python discover.py --mode combined --dry-run
```

This checks configuration, displays the scope and limits, and creates no outputs.
The launcher resolves paths relative to this folder even if invoked elsewhere.

## Discover URLs

For Map, set your Firecrawl API key in the current terminal. In Bash, this avoids
putting the key in command history or echoing it:

```bash
read -r -s -p 'Firecrawl API key: ' FIRECRAWL_API_KEY
export FIRECRAWL_API_KEY
```

Then choose one mode:

```bash
# Initial inventory from Firecrawl Map (default mode).
.venv/bin/python discover.py --mode map

# Browser traversal only; no Firecrawl key needed.
.venv/bin/python discover.py --mode browser

# Map followed by browser traversal; merge both inventories.
.venv/bin/python discover.py --mode combined
```

Map sends the configured seed URLs to the Firecrawl API and may consume your
account credits. The tool does not automatically retry billable Map requests.

## Scope and browser navigation

Edit [configs/cellphones.toml](configs/cellphones.toml):

- `allowed_hosts`: exact hostnames. Add each verified company subdomain explicitly.
  External links are not assumed to belong to the company.
- `seed_urls`: starting URLs for Map and the default browser seeds.
- `firecrawl.limit`: maximum returned links **per seed**, up to 100,000. Reaching
  that limit is reported; a lower count does not establish complete coverage.
- `browser.seed_urls`: navigation pages to explore. Combined mode deliberately
  does not open every mapped URL in Firefox.
- `browser.max_pages`: maximum browser navigation attempts per run; starts at 100.
- `browser.delay_seconds`: pause between page visits; robots crawl-delay can
  increase this pause.
- `browser.scroll_steps`, `render_wait_ms`: bounded scrolling and JavaScript waits.
- `browser.hover_selectors`: optional CSS menu selectors to hover for additional
  links. These start empty because CellphoneS-specific selectors have not been
  validated. This version does not click arbitrary buttons or load-more controls.

The browser follows discovered anchors, including pagination links, breadth-first.
It honors robots wildcard/allow rules, blocks out-of-scope navigations and redirects,
and records failed visits. Missing robots files (404/410) permit navigation; other
robots-fetch failures conservatively skip that origin and appear in the report.
In-scope redirect destinations are recorded and queued as separate visits so
their robots rules and page budget are checked before fetching them.
Document/download links are recorded without navigating their contents. Images,
fonts, media, service workers, and non-GET/HEAD browser requests are disabled; sites
that depend on these may reveal fewer links.

The browser still fetches HTML and executes JavaScript to discover links. Page
bodies and descriptions are not saved. Firecrawl's remote discovery is governed by
its own service behavior; the local browser rules do not control that service.

## Output

Each invocation creates a new directory, so previous runs are preserved:

```text
outputs/cellphones/<UTC timestamp>-<run id>/
  urls.txt        # one normalized URL per line
  urls.jsonl      # URL, discovery source(s), first discovery time, referring URL
  report.json     # scope, counts, limits, skipped visits, errors, completion state
```

Tracking parameters and document fragments are removed. Meaningful query
parameters, query ordering, path case, and trailing slashes are preserved.
No status in the report means "every company URL has been found":

| Status | Meaning |
| --- | --- |
| `completed` | Configured stages finished without recorded errors or reached limits |
| `limited` | At least one configured URL/page limit was reached |
| `partial` / `failed` | A provider or page failed; inspect errors and saved URLs |
| `interrupted` | Ctrl+C stopped the run; in-memory discoveries were saved |

Exit codes: `0` completed/limited, `1` provider or export errors, `2` invalid
configuration/missing credential, `130` interrupted. Map results are saved before
the browser phase, and Ctrl+C saves partial results. Hard process termination or
power loss during browser traversal can lose discoveries since the last export.

## Checks

```bash
.venv/bin/python -m unittest discover -s checks -v
.venv/bin/python -m ruff check .
```

Offline tests do not call Firecrawl or CellphoneS. Real browser smoke checks can
be run separately after installing the browser:

```bash
.venv/bin/python -m checks.browser_smoke
.venv/bin/python -m checks.scraper_browser_smoke
```

This launches real Firefox against synthetic HTML and verifies static,
JavaScript-generated, and scroll-triggered links without calling any website.
The scraper smoke check uses a local HTTP server to verify original versus
rendered HTML, redirect order, robots and scope restrictions, and continuation
after failures. Neither smoke check calls an external website.

## References

- [Firecrawl Map API](https://docs.firecrawl.dev/api-reference/endpoint/map)
- [Firecrawl Map discovery and coverage limits](https://docs.firecrawl.dev/features/map)
- [Playwright Python](https://playwright.dev/python/docs/library)
- [CellphoneS robots and sitemap declaration](https://cellphones.com.vn/robots.txt)
- [Design](docs/design.md) and [implementation plan](docs/implementation-plan.md)
- [Recorded verification and live smoke results](docs/verification.md)
