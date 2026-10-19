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
