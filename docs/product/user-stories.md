# SenticRAG Product User Stories

This document formalizes the four foundational User Stories driving the **SenticRAG Platform**, extracted from the core architecture specification at [`docs/architecture/ARCHITECTURE.md`](file:///home/intern-tdkhuong/Desktop/Intership%20/SenticRAG%20%E2%80%94%20Retrieval-Augmented%20Aspect%20Sentiment%20&%20Feedback%20Intelligence%20Engine/docs/architecture/ARCHITECTURE.md).

---

## 1. US-BUY-01 — Buyer reports defect and receives policy-compliant resolution
- **Actor:** Buyer / Customer.
- **Job-To-Be-Done:** When my purchased product malfunctions, I want to receive an accurate, policy-compliant resolution without having to repeat my order and defect details across multiple departments.
- **Scenario:** Customer submits a complaint that their device fails to charge and overheats after a recent system update.
- **Happy Path:**
  1. Buyer submits review or support ticket through e-commerce or customer portal.
  2. Gateway anonymizes PII and parses product/order references.
  3. ABSA flags high negative polarity on aspect `battery_charging`.
  4. Hybrid retrieval retrieves similar verified cases; GraphRAG correlates symptom with known issue `ISSUE-FIRMWARE-1.2` and warranty policy `POL-WARRANTY-2026#Clause4.2`.
  5. System generates an empathetic, actionable response explaining the known update issue with firmware rollback instructions and the nearest authorized service center location.
- **Outcome:** First Response Time (FRT) < 30 seconds; zero repetitive questions; verified policy correctness.

---

## 2. US-AGENT-01 — Support Agent receives pre-triaged ticket with grounded draft
- **Actor:** Customer Support Agent.
- **Job-To-Be-Done:** When I open an incoming ticket, I want the system to have already classified aspect/sentiment, verified warranty eligibility, and drafted an evidence-backed response with policy citations so I can resolve it rapidly with confidence.
- **Required Context Card:**
  - Structured defect tags: `Aspect: battery`, `Sentiment: negative`, `Urgency: HIGH`.
  - Customer order info & warranty expiration status.
  - Linked root-cause candidate with confidence score.
  - Draft response accompanied by clickable policy clause citations (`[POL-WARRANTY-2026-v2.1#4.2]`).
- **Outcome:** Average Handling Time (AHT) reduced by 40%; elimination of unauthorized compensation promises; 1-click feedback contribution for knowledge correction.

---

## 3. US-ANALYST-01 — Analyst detects trend, drills down, and confirms root cause
- **Actor:** Product / Customer Experience (CX) Analyst.
- **Job-To-Be-Done:** When a negative sentiment KPI spikes on the dashboard, I want to drill down from macro quantitative metrics into representative qualitative reviews, confirm the underlying root cause, and contribute this finding back into the Knowledge Graph.
- **Analysis Workflow:**
  1. Anomaly alert triggers: "Negative sentiment on aspect `battery` surged to 42% over the last 7 days".
  2. Analyst filters by product model and firmware version (`v1.2`).
  3. Hybrid retrieval fetches Top-10 representative reviews highlighting: *"charging slows down, phone gets hot"*.
  4. Analyst traces graph relationships connecting `Firmware v1.2` to `Battery Charging Loop`.
  5. Analyst marks the defect as an active emerging bug and submits a new relation to the Knowledge Graph for steward approval.
- **Outcome:** Emergent software defects identified within 24-48 hours rather than weeks; proactive resolution enablement for support teams.

---

## 4. US-PM-01 — Product Manager / CPO monitors defect severity and resolution efficacy
- **Actor:** Chief Product Officer (CPO) / Product Manager (PM).
- **Job-To-Be-Done:** I want a high-level view of defect trends across hardware revisions and software versions in real time, alongside resolution metrics, to make informed product recall, hotfix, or warranty policy decisions.
- **Executive Dashboard Requirements:**
  - Real-time aspect sentiment distribution by SKU and release version.
  - Root cause lifecycle tracking: *Emerging → Investigating → Confirmed → Mitigated*.
  - Business impact metrics: First Contact Resolution (FCR), Customer Satisfaction (CSAT), Mean Time To Resolution (MTTR), and Cost Per Ticket.
- **Outcome:** Objective data to halt defective firmware rollouts or negotiate component supplier warranties.
