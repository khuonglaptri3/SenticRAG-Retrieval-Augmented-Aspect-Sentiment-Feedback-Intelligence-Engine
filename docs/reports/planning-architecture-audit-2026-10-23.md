# SenticRAG plan review against the architecture specification — 23 October 2026

**Conclusion:** after correcting gaps in implementation order, reliability, and acceptance criteria, the plan is a suitable baseline for an integrated 14-week demo. It does not establish full architecture compliance or sufficient effort: ATE, quality, latency, IAM, and production requirements need their own evidence. Coverage in a plan does not demonstrate implementation.

The main source is [ARCHITECTURE.md](../architecture/ARCHITECTURE.md), cross-checked against the [detailed specification](../architecture/Final_project_rewritten.md), [user stories](../product/user-stories.md), [acceptance criteria](../product/acceptance-criteria.md), [capability map](../product/capability-map.md), [ontology](../ontology/ontology-schema.md), and [research report](deep-research-report.md). Changes were synchronized into the [milestone Markdown](../planning/SenticRAG_Milestone.md), [Excel workbook](../planning/SenticRAG_Milestone.xlsx), and [HTML](../planning/SenticRAG_Milestone.html).

The audit covered design/planning. It did not run benchmarks, accept the crawler, or approve the 52 files awaiting user review. The Data Plan, all M1 tasks, and the baseline schedule/effort were retained. Technical web sources informed implementation checks rather than replacing product requirements.

English edition: 24 October 2026. The findings and verification results below describe the original 23 October audit; translating this document does not constitute a fresh application test, benchmark, legal review, or external-source verification.

## 1. Areas already aligned

| Original requirement | Plan coverage | Assessment |
| --- | --- | --- |
| §1, §5.2: full-corpus ABSA separate from Top-K retrieval | M4.5, M5.1, MOD-07/09; Q-10 | Aligned. Accepted/processed/pending/failed accounting must be separate from the successful-inference rate. |
| §5.3–5.4: seven layers, four memory types | M1/M2 gateway; M3 orchestration/tools/context; M4 triage; M6 graph; M2/M7/M8 telemetry | Mapped. Implement each control before enabling the capability that uses it. |
| §6.3: dense + BM25 + RRF + BGE | M2.1–M2.3, M5.3 | Benchmarks and adapters are planned. Disabling BGE for quality/latency reasons is a deviation to record, not full topology equivalence. |
| §6.4: operational graph connecting version/symptom/cause/policy/resolution/service center | M6.1–M6.8 | Aligned; the ontology includes Issue/Evidence/Team from the detailed specification. |
| §6.5: policy-grounded drafts, tools, and guardrails | M3.2–M3.5; IO-06..09 | Correct direction; the policy engine determines eligibility and the LLM phrases the result. Add MCP protocol and individual guardrail criteria. |
| §8: four product APIs | IO-03/08/12/13 and corresponding tasks | Retain canonical `/api/v1` APIs; separate chat is a compatible extension, without requiring a product for policy Q&A. |
| §3–4: five user stories, feedback, and stewardship | M2/M3/M4/M5/M6/M7/M8 | One UI application preserves the roles; Analyst and PM may share an area with different permissions. |
| §7, §9: IAM, AI metrics, business outcomes | M8; Q-01..18; DEC-03..05/11 | Planned. Rendered IaC, a passing demo, or synthetic KPIs do not prove production readiness. |

ARCHITECTURE.md does not mandate LangGraph; it requires lifecycle FSM, planning, reflection, and tools. Keeping LangGraph conditional at M0 is reasonable. PostgreSQL driver/migration choices and a unified UI are implementation details consistent with the architecture boundaries.

## 2. Findings and corrections

| ID | Severity | Before audit | Plan correction | Source |
| --- | --- | --- | --- | --- |
| F-01 | High | Rate limiting was scheduled for M4.6, although the chatbot calls an LLM from M2 | Move sliding-window limits, token/request quotas, 429 responses, and Redis failure handling into M2.5/G2; M4 only extends route coverage | ARCHITECTURE §6.1; M2.5/M4.6 |
| F-02 | High | M4.5 specified persistence followed by queueing without defining failures between the systems | Commit record + outbox in one SQL transaction; retry dispatch, deduplicate consumers, acknowledge after commit, reclaim pending messages, and add fault tests | ARCHITECTURE §5.2; Final project §7.1/8/15; engineering inference rather than verbatim architecture text |
| F-03 | High | Atomic publication lacked a boundary across PostgreSQL, Qdrant, and Neo4j | Versioned snapshots, integrity checks, an SQL active-release pointer, a manifest pinned per request, reconciliation/rollback, and stale-policy checks before actions | Final project §8.2/15/20; M6.6/M6.7 |
| F-04 | High | Q-09 did not clearly retain the .85 ATE target; demo .80 could be mistaken for original-requirement completion | Separate demo and architecture targets; retain .85 for the architecture target and report ATE separately; missing span labels/tests = NOT VALIDATED | ARCHITECTURE §6.2/9.1; acceptance Agent readiness; research ABSA-AC-05 |
| F-05 | High | “Stage budget <2s” did not clearly cover all of Pipeline B | Q-16/M8.4 measure through guarded output, including every stage used by the route; report TTFT/full response/approval waiting separately | ARCHITECTURE §5.2; user stories <30s; acceptance <60s |
| F-06 | Medium | M3.4 only stated “MCP adapter”; internal function calls could be counted as MCP completion | Add local client/server, pinned transport/version, `tools/list` and `tools/call` for three canonical tools, and error/permission/schema tests | ARCHITECTURE §6.5 |
| F-07 | Medium | Planning engine and episodic/procedural memory were mapped to modules but lacked explicit tasks | Typed plans for sources/tools/missing fields/stop conditions, authorized customer history, versioned playbooks, and ABSA-connected Triaged state in M4 | ARCHITECTURE §5.4/6.5; Final project §7.9 |
| F-08 | Medium | Citation/schema criteria existed but M2 did not distinguish guardrails | Separate claim verification, schema validation, policy compliance, and output PII filtering; valid JSON does not prove evidence entailment | ARCHITECTURE §5.3/6.5; Final project §7.9 |
| F-09 | Medium | M8.2 covered OIDC/per-service identity but not explicit permissions and node-role isolation | Builder only pushes to ECR; separate deployment roles, API/training S3 permissions, IMDS isolation, securityContext, and separate live checks | ARCHITECTURE §7.1–7.3 |
| F-10 | Medium | Source Register referenced absent files and two specification hashes differed from the working tree | Reread SRC-02/05 and update hashes; record SRC-06/10..13 as `git:9083135:<path>` and verify blobs | Source Register; working tree `eb194ff` |
| F-11 | Low | IO-01 declared UUIDs but used `conv-demo-01`; DEC-15..17 were outside the Markdown table | Use a valid UUID; consolidate Decisions into one table; render the complete Markdown to HTML and verify synchronization | IO-01; planning artifacts |
| F-12 | Medium | G0 implied that one person completing the work in 14 weeks was already feasible | Require smoke checks and effort review to establish feasibility; identify tight tasks without automatically adding staff or lowering gates | Task Details; Capacity; DEC-01/02 |

F-02/F-03 are design additions to meet durability/replay/versioning requirements, not claims of observed runtime defects: the repository is at the scaffold stage.

## 3. Intentional differences

- **Roadmap:** ARCHITECTURE §10 describes 12 weeks starting with the quantitative core; the current plan is 14 weeks and chatbot-first at the user's request. Retain that sequence, while limiting M2 acceptance to policy Q&A; the full Buyer story requires M3 context, M4 triage, and M6 graph capabilities.
- **UI:** source paths `apps/analyst_dashboard`/`apps/agent_workspace` represent target interface modules. DEC-16 consolidates them into `apps/web` while preserving functionality and permission checks for five personas; this packaging change is documented.
- **Ontology:** the compact document centers on RootCause; the detailed version adds Issue/Firmware/Evidence/Team. DEC-06 selects the extended ontology and separates issue/cause lifecycles. “Zero cyclic graph errors” means no relationship-invariant violations, not a prohibition on all graph cycles.
- **Hybrid/rerank:** dense-only/BM25-only/hybrid and BGE experiments remain required. Leaving BGE disabled may suit the demo after benchmarking, but full §6.3 topology compliance remains unmet.
- **Cloud:** the Compose demo is mandatory; live EKS, runtime IAM, production review, and real CRM depend on access/resources. Missing evidence means OPEN/BLOCKED/NOT RUN for that part, not PASS based on local smoke tests.
- **LangGraph:** framework presence alone does not establish architecture compliance. The same evidence for state persistence, bounded reflection, approval/resume, and idempotency is required; do not implement two orchestrators.

## 4. Fix acceptance definitions to preserve the original targets

| Area | Demo baseline | Architecture / product target | Status without evidence |
| --- | --- | --- | --- |
| ABSA classification/polarity | .80, critical aspect .75 only after the demo profile is frozen at G0 | Macro-F1 ≥.85; explicit class/aspect averaging | NOT RUN or FAIL according to results |
| ATE | Show spans only when supported by the model/labels | F1 ≥.85 under §9.1; freeze exact/partial span matching and averaging | Missing span tests: NOT VALIDATED; full ABSA architecture compliance unmet |
| Pipeline B | Demo response <60s; <30s stretch under DEC-03 | <2s through guarded output, including every route stage; do not substitute TTFT | Unmeasured: NOT RUN; exceeding the target: FAIL architecture-target |
| Retrieval | Small policy corpus in M2; review/graph coverage added in M5/M6 | Recall@5 ≥.88, MRR ≥.82; report additional research thresholds separately | Do not infer full-corpus quality from one slice |
| Guardrails | Critical suite contains no unsupported policy/refund commitments | Citation completeness ≥95%, generic unsupported-action ≤1%; critical promises remain zero | Added metadata/URLs or schema success do not prove grounding |
| Business | Demonstrate events/formulas/lineage | AHT reduction ≥40%, FCR improvement ≥15%, draft acceptance ≥80% require a pilot and baseline | NOT VALIDATED for synthetic/self-run evidence only |

§9.1 does not fully specify ATE F1 averaging; the plan preserves .85 and requires the measurement to be fixed rather than treating category classification as extraction. The <2s target also needs a fixed request boundary/concurrency/cold–warm definition at G0; reports must retain both the original target and the measurement used.

## 5. Schedule and effort risk

Half-day workbook slot checks found **75 tasks**, with **55.5 core days + 4.5 gate days + 9 buffer days + 1 planned day off = 70 working days**. No slots overlap, end dates match effort, and no finish-to-start dependencies are violated. This is schedule arithmetic only.

Risky timeboxes include M0.4 (1 day: app/DB/contracts foundation), M3.4 (1.5 days: orchestration + persistence + MCP), M4.5 (1.5 days: worker/ingestion/outbox/index), M6.7 (1 day: publication/recovery), and M8.2 (1 day: Helm/Terraform/IAM package). One web app reduces duplicate work, but no time savings have been measured. Clarified criteria expose the work required; they do not reduce effort automatically.

G0 must run minimum smoke checks and identify reusable components. If a timebox is exceeded, record buffer use or rebaseline; do not ignore defects, lower metrics, or mark work Done merely because a deadline arrived. This audit retains the 14-week baseline without guaranteeing sufficient ATE training or live-production time while prerequisites are missing.

## 6. Source validity

- The old plan snapshot is at `9083135`; the planning audit used `develop`, HEAD `eb194ff`, with uncommitted planning changes.
- SRC-02 (`Final_project_rewritten.md`) and SRC-05 (`ARCHITECTURE.md`) differ from the old snapshot; the current versions were read and the Source Register updated.
- SRC-06 (`production-data-specification.md`) and SRC-10..13 (crawler README/design/implementation/verification) were absent from the checkout. All were found using `git show 9083135:<path>`, with hashes matching the previous Source Register. Historical SRC-06 was read to verify requirements; crawler blobs were checked for provenance only, not data quality.
- SRC-06/10..13 references in the plan identify retrievable historical sources, not files present on develop. The audit did not restore or modify crawler/data files.
- The 52 files remain **unapproved by the user**. Approved outputs described in M1 are future handoff conditions, not current status.

## 7. Technical cross-checks using primary sources

- DB/message-broker dual-write handling and consumer idempotency were checked against [AWS transactional outbox](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html). The specific SQL outbox + Redis design is proposed for this repository; AWS services are not required.
- MCP includes discovery/call operations and schemas, so evidence must include protocol interactions; see [MCP Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools). Pin the implemented SDK/protocol version rather than using “latest” as a dependency pin.
- LangGraph requires a checkpointer/thread identity for interrupt/resume and can rerun nodes containing side effects; see [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts). Framework use does not replace permission checks or action idempotency.
- Array filtering must bind aspect/sentiment conditions to the same element; see [Qdrant nested filtering](https://qdrant.tech/documentation/search/filtering/). M5.3 already includes a battery-positive/delivery-negative test, so no separate scope is needed.
- Separate workload identities do not automatically block every path to node credentials; see [AWS EKS Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html). The plan must check IMDS and distinguish manifest rendering from runtime enforcement.
- BGE offers multilingual rerankers, but a model card does not establish gains/latency on this project's corpus; see [BAAI bge-reranker-v2-m3](https://huggingface.co/BAAI/bge-reranker-v2-m3). Retain Vietnamese benchmarks at M2.3 and do not select a model solely from its general description.

## 8. Artifact checks after the original planning corrections

Artifact checks passed for 70 changed fields synchronized across MD/XLSX/HTML, consistent column counts in 10 HTML tables, 21 decisions in one table, and 15 parseable JSON examples (IO-01 uses a valid UUID). All 102 Excel formulas and the schedule/effort/dependencies/owners/status/evidence for 75 tasks were preserved; no overlaps or dependency-order violations were found. The Data Plan, M1 content, and gate/traceability statuses were unchanged. Local/historical source hashes matched; `git diff --check` reported no errors.

Application tests were not run because the original changes were documentation-only. This report does not certify gates G0–G8 or AI benchmark results.
