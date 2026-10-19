# Standalone URL Discovery Implementation Plan

> **For agentic workers:** Implement in this session with the executing-plans
> workflow. Keep every artifact inside `Data_crawling`; do not commit or modify
> unrelated user work.

**Goal:** A separately runnable Firecrawl Map / Playwright URL discovery tool.

**Architecture:** Local TOML config feeds a shared URL inventory. Providers add
URLs and provenance; the CLI persists a separate run directory even after
partial discovery failures.

**Tech Stack:** Python 3.11+, standard-library HTTP/JSON/TOML, Protego,
optional Playwright, unittest, Ruff.

**Spec:** [design.md](design.md)

## Global constraints

- Every new file is inside `Data_crawling`.
- No parent dependencies, configuration, source code, or databases are changed.
- Export URLs and discovery metadata only, never page text or API credentials.
- Default to exact `cellphones.com.vn` host scope and bounded browser navigation.

## Review focus

- Lookalike domains and redirects escaping the configured host list.
- Query normalization incorrectly merging different pages.
- Robots failures and browser/service limits appearing as complete success.
- Interruptions losing previously discovered URLs.
- Configuration or output paths escaping the standalone workspace.

## Tasks

- [x] Write failing offline tests for URL inventory, local path validation,
  configuration, provider failure handling, and bounded traversal.
- [x] Implement `url_discovery/core.py`: `Config`, `Inventory`, `normalize_url`,
  and isolated configuration/output helpers. Run the core checks.
- [x] Implement `url_discovery/providers.py`: Firecrawl API adapter, robots policy,
  and browser traversal; Playwright imports stay lazy. Run provider checks.
- [x] Implement `discover.py` and `url_discovery/cli.py`: dry-run, map, browser,
  combined modes, partial reports, and unique run directories. Run CLI checks.
- [x] Add local packaging, example config, environment template, ignore rules,
  setup/use instructions, and local browser installation instructions.
- [x] Run the complete local test suite, lint, CLI dry-run, browser smoke check
  if installed, and parent-workspace hash verification. Record actual results.

## Completion record — 2026-10-19

- User clarified Ubuntu/Firefox; switched the browser engine and local browser
  installation instructions to Playwright Firefox.
- All 26 offline tests pass, including regression cases observed failing before
  their fixes. The standalone folder passes Ruff lint and formatting checks.
- Real Firefox synthetic-page smoke passed; one-page live CellphoneS smoke
  discovered 152 URLs, with no errors and the intentional page-limit status.
- A read-only reviewer identified lost robots-disallowed redirect discoveries;
  the fix records those URLs while still skipping their navigation. Its expanded
  regression test failed before the fix and passes afterward.
- Live testing found stale Anaconda CA trust. The runner now defaults to Ubuntu's
  system CA bundle within its process, preserving explicit TLS environment values.
  No certificate verification was disabled and no system trust files were changed.
- All 130 baseline files outside this folder remain byte-for-byte unchanged.
- Firecrawl live verification remains credential-dependent; its API adapter was
  checked offline against documented request/response shapes.
- No commits, branch changes, parent dependency changes, or application integration.

See [verification.md](verification.md) for commands and existing lint limitations.
