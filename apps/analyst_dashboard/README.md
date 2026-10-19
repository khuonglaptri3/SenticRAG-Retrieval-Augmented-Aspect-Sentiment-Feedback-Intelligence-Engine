# SenticRAG Analyst & PM Dashboard (`apps/analyst_dashboard`)

Interactive intelligence dashboard serving **Product / CX Analysts** and **Chief Product Officers (CPO) / Product Managers (PM)** as defined in [`US-ANALYST-01`](file:///home/intern-tdkhuong/Desktop/Intership%20/SenticRAG%20%E2%80%94%20Retrieval-Augmented%20Aspect%20Sentiment%20&%20Feedback%20Intelligence%20Engine/docs/product/user-stories.md#3-us-analyst-01--analyst-detects-trend-drills-down-and-confirms-root-cause) and [`US-PM-01`](file:///home/intern-tdkhuong/Desktop/Intership%20/SenticRAG%20%E2%80%94%20Retrieval-Augmented%20Aspect%20Sentiment%20&%20Feedback%20Intelligence%20Engine/docs/product/user-stories.md#4-us-pm-01--product-manager--cpo-monitors-defect-severity-and-resolution-efficacy).

## Key Features
1. **Macro Corpus View (Quantitative ABSA)**: Real-time tracking of negative aspect sentiment ratios across 100% of review data, segmented by SKU, firmware, and sales channel.
2. **Qualitative Drill-Down**: Hybrid Retrieval magnifying glass that isolates the Top-K representative review cohort explaining any observed metric anomaly.
3. **GraphRAG Root-Cause Explorer**: Traversal graph visualizer mapping defects across `Version → Symptom → Root Cause → Resolution`.
4. **Knowledge Contribution & Verification**: Tools enabling analysts to formulate new defect hypotheses, tag emerging issues, and push updates to the Knowledge Graph.
