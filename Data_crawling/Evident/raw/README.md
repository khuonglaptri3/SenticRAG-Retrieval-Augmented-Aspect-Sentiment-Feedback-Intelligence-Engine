# Saved Playwright crawl results

These are public-page snapshots captured by `scrape.py`. Each numbered page
folder contains `page.json` and, when capture succeeded, `response.html`,
`rendered.html`, and `text.txt`. Each run's `report.json` records its source
inventory, counts, status, and page record paths. Timestamps are UTC.

The complete sequential run is
[`20261020T080902Z-1f9d59ff`](20261020T080902Z-1f9d59ff/report.json):
56 URLs attempted, 52 successful captures, and 4 robots-related skips recorded
as failures. All 52 successful captures have all four output files.

The other dated folders are one-page test runs. Captures preserve raw contents,
including navigation and footers. A successful capture does not establish that
every possible text section, interaction state, or dynamically loaded item was
captured. The HTML files are source snapshots intended for inspection.

These snapshots are explicitly included in Git. The parent ignore rule keeps
newly generated runs from being committed automatically.
