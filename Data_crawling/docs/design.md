# Standalone URL discovery

The user designated `Data_crawling` as an independent workspace. The agreed
workflow is Firecrawl Map, optional Playwright link discovery, merge, and URL
export. This is a new standalone tool; its first deliverable discovers URLs,
without extracting or storing document bodies.

## Boundaries

- Python 3.11+, a local `.venv`, local browser binaries, and local configuration.
- No imports from SenticRAG, database connections, parent environment-file reads,
  parent dependency changes, or modifications outside this directory.
- Output and config paths must resolve inside this workspace, including through
  symlinks. Each run gets a new directory under `outputs/`.
- Credentials come from `FIRECRAWL_API_KEY` in the process environment. Never put
  credentials in configuration, exported records, or diagnostic response bodies.

## Workflow

1. Validate a TOML configuration and support a network-free `--dry-run`.
2. `map`: request Firecrawl `/v2/map` for configured seed URLs. Keep URL fields
   only. Preserve meaningful query parameters. Report service limits and errors.
3. `browser`: use Playwright Firefox to traverse rendered anchors within exact allowed
   hosts. Honor robots rules using Protego, throttle navigation, and cap page
   visits. Scroll and optionally hover explicitly configured menu selectors.
   Never generically click purchase, login, or other action buttons.
4. `combined`: merge Map discoveries with browser discoveries. Browser seeds are
   deliberately configured navigation pages; avoid opening every mapped product.
5. Export sorted `urls.txt`, URL provenance in `urls.jsonl`, and `report.json`.
   Record discovered URLs even when navigation is skipped. Report failures and
   truncation honestly; never claim complete coverage of a company's websites.

## URL handling

Allow HTTP(S) only, normalize hostname/default port, drop document fragments and
explicit tracking parameters, preserve path case/trailing slash/query ordering,
reject embedded credentials, and match hosts exactly. Subdomains must be listed
explicitly. Deduplicate after normalization. Record documents such as PDF links
but do not navigate them as HTML. Browser redirects must remain within scope.

## Validation

Offline tests cover domain lookalikes, relative URLs, distinct query parameters,
path escape, redirect scope, provider errors, browser limits and cycles, merged
provenance, and partial-result persistence. A real browser smoke check is useful
when Firefox is available. Existing tracked and untracked source-file hashes
are compared before and after to verify isolation.

## Limits

No claim of exhaustive discovery. No automatic company-domain ownership
discovery, content extraction, login, CAPTCHA handling, or production ingestion.
Map requires the user's API credential; Playwright requires a local browser
installation. A full crawl is a separate user-run operation after setup.
