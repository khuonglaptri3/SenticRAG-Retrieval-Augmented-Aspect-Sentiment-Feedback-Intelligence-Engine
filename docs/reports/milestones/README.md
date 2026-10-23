# Milestone task reports

Each task has a directory named with its exact milestone ID. Open the task's `README.md` to review results; supporting tables, logs, JSON, images, and evidence are stored in `evidence/`. All report prose and authored supporting descriptions must be in English; preserve original source data and raw logs when required for evidence integrity.

| Task | Description | Status | Report |
| --- | --- | --- | --- |
| M0.1 | Repository audit and requirements inventory | COMPLETE | [Read results](M0.1/README.md) |

Apply the same layout to subsequent tasks, for example `M1.1`:

```text
milestones/
├── README.md
└── M1.1/
    ├── README.md       # Results, verification, open issues, and next steps
    └── evidence/       # CSV, JSON, logs, images, and supporting documentation
```

- Keep each results report inside its task directory.
- Link supporting files from `README.md` using relative paths into `evidence/`.
- Add one row to the table when completing a new task so reviewers can find it quickly.
- Record task and gate status separately; a COMPLETE task does not automatically make its gate PASS.
