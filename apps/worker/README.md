# SenticRAG Background Worker (`apps/worker`)

Handles asynchronous backend tasks and scheduled operational jobs across the SenticRAG platform:

- `consumers/`: Ingests customer review and ticket streams from message brokers (Redis Streams / Kafka), triggering real-time PII anonymization and routing to Pipeline A (Batch ABSA) or Pipeline B (Real-time Resolution).
- `jobs/`: Scheduled background workers that execute nightly anomaly detection sweeps, aggregate BI metrics, and trigger active-learning retraining cycles when annotation thresholds are reached.
