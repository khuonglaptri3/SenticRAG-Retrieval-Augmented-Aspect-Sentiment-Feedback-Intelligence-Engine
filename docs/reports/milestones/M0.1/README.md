# M0.1 — Repository audit and requirements inventory

- **Task status:** COMPLETE — inventory, cross-checks, and evidence recording are complete; product gaps are assigned to the relevant tasks.
- **Execution dates:** started 23 October 2026, completed 24 October 2026 (Asia/Saigon), ahead of the baseline schedule on the morning of 26 October. The audit session is not reported as a measured 0.5 person-day.
- **Audited repository:** `develop` at `256c0b47155f0e6876e3f3d6d050177c44c11b36`.
- **Historical source:** `origin/feature/Data_preparing` at `90831354250a7c79f4d3d5bc54dd7b3b9a55b429`.
- **Performed by:** Codex, at the workspace owner's request. This is an internal technical verification, not business approval by a policy/data owner.
- **Criteria:** [M0.1 in the milestone plan](../../../planning/SenticRAG_Milestone.md), contract IO-15; exclude hard-coded API values from the baseline and trace every requirement to its source and phase.
- **English edition:** 24 October 2026, branch `docs/english-reports`. Translation and publication checks are recorded separately in [translation-verification.json](evidence/translation-verification.json). Audit measurements below retain their original dates and scope.

## 1. Current-state conclusion

The repository contains **an architecture scaffold, sample APIs, and initial schemas**. Some components run sufficiently to inspect request/response shapes, but no RAG chatbot, ABSA inference, evidence retrieval, policy engine, GraphRAG, or end-to-end user story is implemented.

The inventory covers **133 tracked files** and **1 preexisting untracked document**. Of **65 Python files**, 61 contain only placeholders/docstrings, 2 contain application code (`main.py`, `data_contracts/__init__.py`), and 2 contain tests. Capability-named directories do not demonstrate implemented capabilities.

The matrix records **90/90 baseline requirements with IDs, sources, valid tasks, current status, and evidence**. No product requirement was fully accepted during this audit; this is not a measure of “0% code completion.” Four items have partial scaffolding, 11 have mock behavior only, 58 are unimplemented, 9 are unmeasured, and 8 extensions are unimplemented/deferred/conditional. Local datasets described in the untracked document are recorded as references requiring verification, not automatically approved data sources.

## 2. Handoff artifacts

| Artifact | Contents |
| --- | --- |
| [inventory.csv](evidence/inventory.csv) | Each baseline file: type, size, working-tree and Git-blob SHA-256, and code-definition locations. |
| [source-register.csv](evidence/source-register.csv) | 39 sources: 28 current files, 5 verified historical blobs, 5 external references not rechecked, and 1 untracked document at audit time. |
| [requirements.csv](evidence/requirements.csv) | Preserves the 90 IDs from milestone §8, with current status, gaps, and evidence. Descriptions are translated into English; source locations are retained. |
| [local-data-intake.csv](evidence/local-data-intake.csv) | 34 S/D/R items from the data document that was untracked at audit time, mapped to current requirements and tasks; this is not dataset acceptance. |
| [baseline-summary.json](evidence/baseline-summary.json) | Counts, Python environment, tool versions, and verification scope. |
| [checks.txt](evidence/checks.txt) | Commands and output for tests, lint, type checking, and lockfile verification. |
| [api-probes.json](evidence/api-probes.json) | 16 observations using synthetic TestClient inputs, including exposed mocks and missing validation. Original Vietnamese payloads/responses are preserved. |
| [crawler-snapshot.json](evidence/crawler-snapshot.json) | Historical report details, 56 page records, and presence checks for 52 capture sets. |
| [document-links.json](evidence/document-links.json) | Local links with missing targets or dependencies on another machine's paths at audit time. |
| [infrastructure-checks.json](evidence/infrastructure-checks.json) | Compose rendering and Docker Engine check results. |
| [artifact-verification.json](evidence/artifact-verification.json) | Original checks of IDs, sources/tasks, links, and integrity of 134 input files. |
| [run-manifest.json](evidence/run-manifest.json) | SHAs, environment, check statuses, limitations, and current audit-artifact hashes under IO-15, with translation provenance. |
| [translation-verification.json](evidence/translation-verification.json) | Checks of the English edition, retained raw evidence, baseline hashes, and report links; separate from original product checks. |

## 3. Actual capability inventory

| Area | Present | Missing / limitations | Receiving tasks |
| --- | --- | --- | --- |
| API | FastAPI; 10 application routes: 3 health, 4 product, 3 legacy; OpenAPI; required-field Pydantic validation. | Product/legacy handlers return samples; no DB, queue, model, LLM, or retrieval calls. | M0.3–M0.4; M2.5; M3.4; M4.5 |
| Contracts | 12 shared models; 6 models in the API file. | No chat/session, policy registry/decision, outcome, or versioned prediction contracts; missing enums/bounds/ownership and citation URL/version/effective date. | M0.3 |
| Chat/UI | Agent Workspace and Analyst Dashboard READMEs. | No `apps/web`, frontend build, chat messages API, history, session, or Steward UI. | M0.2–M0.4; M2.5–M2.6 |
| ABSA / retrieval / graph / LLM / policy | Package structure, dependencies, and specifications. | Packages are placeholders; no model weights, index, approved policy, or executable pipeline in the checkout. | M1–M7 according to the matrix |
| Worker / pipelines | 10 pipeline directories and a worker skeleton. | No consumer/job, durable ingestion, outbox, retries, PII masking, or full-corpus inference. | M1.2–M1.3; M4.5 |
| Crawler | Code, documentation, and snapshots in separate-branch commit `9083135`. | `Data_crawling` is absent from the `develop` checkout; no application ingestion/approval adapter. | M1.1–M1.4 |
| Storage / operations | Compose declares PostgreSQL, Redis, Qdrant, Neo4j, and the API; two Dockerfiles use non-root users. | No application migrations or SQLAlchemy/psycopg/Alembic in the dependency manifest; Helm/Terraform/observability contain only `.gitkeep`. | M0.3–M0.4; M2.7; M8 |
| Tests / CI | 5 API tests, 2 contract tests; Ruff/mypy/pytest configuration; 4 workflow YAML files. | No integration/evaluation/E2E/smoke/load cases. CI ignores mypy/pytest failures; the security scan is also non-blocking. | M0.4; M8.1; M8.5 |

**Values excluded from the baseline:** 100,000 reviews; a 65,000/15,000/20,000 distribution; a negative rate of 0.42 over 1,280 reviews; confidence values of 0.89/0.94/0.95; evidence count 35. These are literals in the [API](../../../../apps/api/app/main.py), not corpus/model measurements. F1, Recall, latency, cost, business impact, freshness, and production readiness are **NOT_MEASURED / NOT_VALIDATED**.

## 4. Verification performed

The original audit used a temporary Python **3.11.16** virtual environment; API/test/lint/type-check dependencies were constrained to versions from `poetry.lock`. Poetry **2.2.1** ran in a separate tool environment. The full ML stack was not installed; a full project installation/build and Python 3.12 compatibility matrix remain unverified.

| Check | Result | Meaning and limitations |
| --- | --- | --- |
| `python -m pytest tests -q -p no:cacheprovider` | **PASS: 7 tests**, 1 Starlette/httpx deprecation warning. | Covers 5 API scaffold cases and 2 basic contract cases; no datasets or external services. |
| `python -m ruff check . --output-format concise` | **FAIL: 34 findings**. | 8 in the API, 21 in contracts, 4 in contract tests, 1 in unit tests; imports/type style/unused imports/whitespace. These predate the audit. |
| `python -m mypy packages apps pipelines --ignore-missing-imports` | **PASS: 56 source files**. | Static typing only; many files are placeholders. |
| `poetry check --lock --strict` with Poetry 2.2.1 | **PASS**. | Metadata/lock validity; does not prove heavy dependencies are installed or models run. |
| `docker compose -f infra/compose/docker-compose.yml config --quiet` | **PASS**. | Compose configuration renders. |
| `docker version --format ...` | **BLOCKED: Docker Engine unavailable**. | Could not connect to `dockerDesktopLinuxEngine`; image build, stack startup, and DB smoke checks were not run. |
| 16 synthetic API/schema probes | **Actual observations recorded**. | Observations identify mocks/gaps; they are not 16 passing acceptance tests. |
| AST inventory, source/task IDs, and hashes | **PASS**. | 90 unique IDs with no missing source/task; original file hashes checked. |

These are the original audit results, not fresh measurements from the translation work. See [translation verification](evidence/translation-verification.json) for checks performed on this edition.

## 5. Findings and required follow-up

“High” indicates priority before using the affected capability in a real demo; it does not imply that the system has production users.

| ID | Severity | Specific evidence | Impact / follow-up |
| --- | --- | --- | --- |
| M01-F01 | High | `generate_resolution_draft` always gives the same firmware-fault explanation and free-replacement entitlement, confidence 0.94, and `needs_human_review=false`. A kettle-product probe receives the same content. | No supporting policy/order or guardrails. M2.4, M3.3–M3.4, and M3.7 must handle missing evidence, approval, and applicability before draft acceptance. |
| M01-F02 | High | `ingest_feedback` only counts records and creates a UUID; `contribute_feedback` only creates a UUID. No database/queue calls occur in the handlers. | `queued`/`accepted` does not prove storage or processing. M0.4 establishes persistence; M3.6/M4.5/M7.1 implement storage, outbox, and idempotency. |
| M01-F03 | High | `/predict` returns positive for both negative and positive text; `/ask` returns a fixed sentence with empty citations; drilldown returns the same cohort/evidence. | Do not use these endpoints as ABSA/retrieval/analytics baselines. M2, M4, and M5 must implement pipelines and evaluations using real data. |
| M01-F04 | High | Readiness/startup always return 200 without DB/model checks; the local Docker Engine is unavailable. | Dependency readiness is unverified. M0.4 and M2.7 implement dependency health and failure paths; prepare the Engine before Compose smoke checks. |
| M01-F05 | High | CI contains `mypy ... \|\| true` and `pytest tests/unit ... \|\| true`; security contains `pip-audit ... \|\| true`; CI does not run the contract suite. Ruff has 34 findings. | Non-blocking steps may hide failures; lint may block earlier. M0.4 must clean the baseline, enforce exit codes, and run the required suites. No claim is made about current Actions success/failure because no Actions run was checked. |
| M01-F06 | High | No auth/ownership; all probes run without tokens. Unknown feedback types/self-declared authors are accepted, as are rating 999, top_k 0/-1, out-of-enum sentiment, and confidence 8. | M0.3 locks enums/bounds and derives authors from identity; M0.4/M2.5/M3.2 implement auth/session/ownership for each flow. |
| M01-F07 | High | The crawler commit was fetched from a separate branch; its historical full-run report records 56 attempted, 52 successful, and 4 failed pages. Git contains 56 page JSON files and 52 response/rendered/text sets. | Historical raw captures exist, but no approved policies/clean chunks/index in the app. M1.1 accepts the manifest through a file boundary; M1.2–M1.4 check content, usage rights, effective dates, and evaluation. |
| M01-F08 | Medium | `DATA_REQUIREMENTS.md` was untracked; its dataset path `C:/Users/lanph/Downloads/data` did not exist during this audit. | Its counts/splits/leakage claims were not reverified on this machine. M0.3/M4.1 must identify actual snapshots, licenses, splits, and hashes; do not assume a ready-to-use dataset. |
| M01-F09 | Medium | `apps/web`, a conversation API, migration schemas, evaluation datasets, and 5 persona flows are absent. | This is implementation backlog, not an audit-induced defect. M0.2 uses this baseline for UX/scope and handoff to M0.3–M0.4. |
| M01-F10 | Medium | The `train` workflow only builds an image; default `configs/training/sentiment.yaml` is absent. `release` only builds; outputs reference `steps.meta` without a corresponding step; no Helm chart exists. | Workflow names do not prove complete training/release. M4.3/M7.3 and M8.1–M8.3 implement entrypoints, artifact lineage, and actual pipelines. |
| M01-F11 | Medium | 1 link targets missing `LICENSE`; 4 `file:///home/...` links depend on another machine. Specifications also mention absent legacy documents. | Portable references and source authority need resolution in M0.3/M8.8. Locations are listed below and in the JSON evidence. |
| M01-F12 | Medium | The historical data specification states Qdrant v1.19+; Compose uses v1.9.2; the lockfile has qdrant-client 1.19.1; Neo4j client is 6.4.0 with server target 5.20. | These version differences require compatibility smoke checks; they do not establish a runtime defect. M0.3 pins clients/servers/features; M2.1/M6.2 verify connections and actual APIs. |

These findings remain backlog for the relevant milestones. The audit did not modify product behavior to obscure the starting point.

## 6. Historical sources, missing documents, and conflicts

Object `9083135` was initially absent locally. The audit checked `origin` heads, fetched only `feature/Data_preparing`, and read blobs by full SHA. `develop` and application files were unchanged. SRC-06 and SRC-10..13 have blob/hash evidence but remain **historical sources outside the develop checkout**. The crawler was not run; Firecrawl was not called; websites were not fetched again; the 52 captures were not accepted. The four historical failures still require resolution or justified exclusion in M1.

References without current files at audit time:

- `Bai_Toan_Dat_Ra.md`, `Final_project(3).md`: mentioned in the detailed specification; use current SRC-02/SRC-05 with DEC-21 precedence to trace requirements.
- `GIOI_THIEU_SAN_PHAM_VI.md`: proposed/outlined in the research report; not an existing deliverable.
- `re.txt`: recorded as a historical review input in the milestone; unavailable for checking its original content.
- `LICENSE`, `configs/training/sentiment.yaml`: absent from the audited tracked tree.
- `C:/Users/lanph/Downloads/data`: absent on the audit machine; datasets described in the local document could not be reverified.

| Conflict / difference | Existing plan rule | Decision still required |
| --- | --- | --- |
| A 12-week/ABSA-first roadmap and Phase 1 ABSA data document versus a 14-week/chatbot-first milestone plan. | DEC-01/02/16/21: the current milestone defines execution order; architecture defines capability targets. | M0.2 retains chatbot-first delivery and brings policy data into M1; do not copy the old phase sequence. |
| README/user stories list 4 personas; architecture/milestones add a Steward. | One `apps/web`, 4 areas for 5 personas. | M0.2 includes Steward and API permissions; README scaffolding is not an implemented UI. |
| FRT <30s, <60s, and Pipeline B <2s differ. | DEC-03/18 separate demo from architecture targets and TTFT from full response. | G0 fixes boundaries, percentiles, and concurrency; no measurements establish a passing result. |
| ABSA demo 0.80 versus architecture ATE/polarity 0.85; different Recall@5/@10 thresholds. | DEC-05/18 preserve separate profiles and metric definitions. | M0.3/M4.1 verify ATE labels and data splits; G0 fixes the rubric. |
| The compact ontology centers on RootCause/lifecycle; the blueprint/detailed specification require Issue/Evidence/Team. | DEC-06 proposes a canonical ontology and separates issue/cause states. | M0.3/M6.1 record an ADR and schema; no graph constraints are enforced yet. |
| README/worker mention Celery/Kafka; the plan selects Redis Streams. | DEC-08: one Redis Streams worker for the demo; local BM25 reference. | M0.3 fixes queue/delivery semantics; M4.5 implements outbox/replay. |
| Python metadata specifies >=3.11 while the Poetry lock targets 3.11–3.12. | README explains the intent; Docker defaults to 3.11. | The audit tested only Python 3.11; M0.4 runs the appropriate matrix after fixing the environment. |

The Source Register identifies 5 external URLs as inherited references only (the template and WEB-01..04), not rechecked during this audit. Prices, laws, quotas, and compliance statements are not new audit conclusions. Data/provider/cloud usage rights and 14-week feasibility still require review at M0.3/G0.

## 7. M0.1 acceptance and handoff

| M0.1 criterion | Result | Evidence |
| --- | --- | --- |
| Distinguish mocks from actual functionality | Met | Code inventory, 16 probes, findings F01–F06. |
| Inventory crawler, schemas, CI, and API | Met | Inventory/source register, historical snapshots, checks, and capability table. |
| Provide a baseline inventory and Source Register | Met | CSVs and source SHAs; current/historical/untracked/external sources distinguished. |
| Trace every requirement to a source and phase | Met | 90/90 valid rows; 34 local intake items have separate reference mappings. |
| Record missing documents and conflicts | Met | Findings F08/F11/F12, section 6, and document-links.json. |
| Exclude hard-coded API values from the baseline | Met | Exclusions in section 3; AI/business/runtime metrics remain NOT_MEASURED. |
| Provide an IO-15 manifest/report | Met within the local audit scope | run-manifest.json records sources, environment, command results, and artifact hashes; unavailable deployment/model/index checks remain NOT_RUN. |

**M0.1 is complete for its audit deliverables. M0 and gate G0 remain unaccepted.** M0.2 can start from this baseline: design one apps/web for 5 personas and policy Q&A flows covering citations, follow-up questions, missing evidence, and human handoff. Findings F01–F12 are priority inputs to M0.3–M0.4 and later tasks, not grounds for declaring the entire product Done.

Actual M0.1 progress is recorded in this report/manifest. The **baseline** schedule and statuses in Markdown/HTML/XLSX remain unchanged to separate the original plan from execution results; use this report as evidence when updating WBS progress. The original audit verified that product code, dependency manifests, and the preexisting untracked document were unchanged.

The English edition preserves those historical findings and raw evidence. It publishes the previously untracked [data-requirements source](../../../architecture/DATA_REQUIREMENTS.md) unchanged so its references can be reviewed; its original untracked/unvalidated status describes the audit baseline, not approval of the data. Baseline inventory/source hashes remain historical; current report-artifact hashes and translation checks are recorded separately in the manifest.
