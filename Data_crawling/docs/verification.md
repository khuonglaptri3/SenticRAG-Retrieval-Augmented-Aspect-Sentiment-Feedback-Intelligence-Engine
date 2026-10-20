# Verification — 2026-10-19

## Standalone tool

Executed from `Data_crawling`:

| Command/check | Result |
| --- | --- |
| `.venv/bin/python -m unittest discover -s checks -v` | 26 tests passed |
| `.venv/bin/python -m ruff check .` | Passed |
| `.venv/bin/python -m ruff format --check .` | Passed |
| `.venv/bin/python discover.py --mode combined --dry-run` | Validated; no network calls |
| `.venv/bin/python -m checks.browser_smoke` | Real Firefox extracted static, JavaScript-generated, and scroll-triggered links |
| Copy the source folder to `/tmp`, invoke the copied launcher from `/tmp` | Passed; no parent project required |

Installed locally: Python 3.11.14, Playwright 1.64.0, Playwright Firefox build
1555, Protego 0.7.0, Ruff 0.17.1. Browser binaries are under `.browsers`; packages
are under `.venv`. The user's regular Firefox installation/profile is not used.

## Live CellphoneS smoke

A temporary local config at `.cache/smoke.toml` reduced the browser page budget
to one. Running the normal CLI against it produced **152 unique URLs**, visited
one page, and recorded **zero errors**. Its `limited` status is intentional.

Results (locally generated, ignored by Git):

`outputs/smoke-cellphones/20261019T071640Z-162fe7ab/urls.txt`

The first attempt failed certificate verification using Anaconda's bundled CA
store. A verified request using Ubuntu's system CA store succeeded. The final
runner uses that system store by default on Ubuntu/Debian, retaining explicit
user TLS settings. Verification was never disabled.

Firecrawl was **not called live**: no user API credential was supplied. Tests
exercise its request shape, response validation, errors, limits, and URL export
using synthetic HTTP responses.

## Existing repository

- SHA-256 comparison: **130 pre-existing tracked/untracked source files outside
  `Data_crawling` checked; zero changed**. Pre-existing user edits were preserved.
- Existing unit/contract suite: `python3 -m pytest tests/unit tests/contract -q`
  passed **7 tests**, with one existing Starlette/httpx deprecation warning.
- Repository-wide Ruff reports **34 pre-existing issues** in unchanged files:
  `apps/api/app/main.py` (8), `packages/data_contracts/__init__.py` (21),
  `tests/contract/test_data_contracts.py` (4), `tests/unit/test_api.py` (1).
  There are no Ruff findings in `Data_crawling`.

## Review

A read-only independent reviewer found one redirect-inventory issue. It was
fixed and regression-tested: in-scope URLs discovered through redirects remain
in the inventory even if robots rules forbid fetching them. External resource
requests remain browser support traffic, distinct from scoped page navigation.
The single-page live smoke does not establish exhaustive website coverage.

## Sequential content scraping — 2026-10-20

Added `scrape.py`, which processes `Evident/policy_urls.txt` sequentially in
first-seen file order. The default processes the entire inventory; `--limit 1`
tests the first entry. No random URL selection is used.

- `.venv/bin/python -m unittest discover -s checks -q`: **34 tests passed**.
- `.venv/bin/python -m ruff check .`: passed.
- `.venv/bin/python -m ruff format --check .`: **16 files** passed.
- `git diff --check`: passed.
- `.venv/bin/python -m checks.browser_smoke`: passed.
- `.venv/bin/python -m checks.scraper_browser_smoke`: passed against a local
  HTTP server. Verified original response versus JavaScript-rendered contents,
  ordered multi-hop redirects, query preservation, robots restrictions, blocked
  external redirects, and processing the next page after failures.

The local browser check exposed two issues during development: the reused
discovery scope rejected fixture URLs with explicit ports, and redirect metadata
used an unordered set. The scraper now matches exact input host/port pairs and
records redirect history in navigation order; the browser check passed afterward.

Live command: `.venv/bin/python scrape.py --limit 1`.

The first of **56** saved URLs,
`https://cellphones.com.vn/chinh-sach-giao-hang`, returned **HTTP 200**, titled
“Chính sách giao hàng CellphoneS - Nhanh chóng, miễn phí”. One page succeeded,
with no failures or request-guard warnings. Saved files:

`Evident/raw/20261020T072346Z-7a8afddf/0001/`

| File | Size |
| --- | ---: |
| `response.html` | 681,986 bytes |
| `rendered.html` | 680,505 bytes |
| `text.txt` | 17,364 bytes (13,766 characters) |
| `page.json` | 18,576 bytes |

The run's `report.json` identifies the source file, available URL count, limit,
attempts, results, and record paths. Full body text includes navigation/footer
content; the Vietnamese delivery policy was manually confirmed in the capture.
This initial live check tested one saved URL. The subsequent full batch is
recorded below.

## Full sequential crawl — 2026-10-20

The user ran `.venv/bin/python scrape.py --delay-seconds 30` against the entire
56-URL input inventory. The saved report records **56 attempted, 52 succeeded,
4 failed**, with status `partial`. The run started at 08:09:05 UTC and finished
at 08:44:28 UTC.

Results: `Evident/raw/20261020T080902Z-1f9d59ff/`.

All 52 successful records have their response HTML, rendered HTML, text, and JSON
files. The successful records contain a combined **394,582 text characters**.
Each of the four failed entries has a JSON error record. The historical run
records use a generic robots-policy/fetch-failure message. Follow-up checks found:

- `https://cellphones.com.vn/smember` redirects to
  `https://smember.com.vn?company_id=cellphones`.
- Smember's robots file returned HTTP 403; the scraper conservatively skipped
  that redirect and both direct Smember entries.
- The invoice site's robots rules disallow all crawling, so
  `https://hddt.cellphones.com.vn/` was skipped.

These are successful capture counts, not proof of complete text coverage. The
raw snapshots include site navigation and footers, with no content cleaning.
Selected snapshots are committed explicitly; future generated runs remain
ignored by the `Evident/raw/` rule.
