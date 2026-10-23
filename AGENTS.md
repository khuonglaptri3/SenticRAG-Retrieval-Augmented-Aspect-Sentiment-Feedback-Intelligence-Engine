# Reporting conventions for milestone tasks

When working on a milestone task, organize its report using these conventions so reviewers can find the results immediately upon opening the task directory. All reports must be written in English, prioritizing conclusions, evidence, and outstanding work. This language requirement includes report titles, headings, narrative, table labels, review indexes, and authored supporting documentation. Preserve original source data, quotations, commands, and raw logs when needed for evidence integrity.

## 1. Required structure

Each task has its own directory at `docs/reports/milestones/<TASK-ID>/`, using the exact ID from the plan, such as `M0.1`, `M1.1`, or `M0.G`.

```text
docs/reports/milestones/
├── README.md                 # Task index and quick review links
├── M0.1/
│   ├── README.md             # M0.1 results report
│   └── evidence/             # All supporting material for M0.1
└── M1.1/
    ├── README.md             # M1.1 results report
    └── evidence/             # All supporting material for M1.1
```

The task directory must contain only these two entries at its top level:

1. **`README.md`:** the main report for user review.
2. **`evidence/`:** supporting files such as CSV, JSON, logs, images, check results, manifests, detailed tables, or supplementary documentation.

Reports must reside inside their task directory. Do not place standalone reports outside it, such as `milestones/m0.1-audit.md`, or put CSV/JSON/log files alongside the task's `README.md`. Store archived report versions in `evidence/`; `README.md` must always present the current results.

Create a task directory only when work begins or results need to be reported. The `M1.1` entry in the example above illustrates the convention; it does not imply that the task has been performed.

## 2. Main report content

The first few lines of `README.md` must communicate the outcome before presenting details. Include:

- **Task information:** ID, name, actual status, execution date, and requirement source. Include the branch/commit when results are tied to a repository version.
- **Conclusion:** achievements, remaining gaps, and important limitations; distinguish verified results from assumptions.
- **Work performed:** meaningful changes or findings, without reproducing the entire action history.
- **Outputs:** a table of filenames, purposes, and relative links to files in `evidence/`.
- **Verification:** commands or methods, actual results, scope, and supporting evidence.
- **Open issues:** impact, required follow-up, and the receiving task if identified.
- **Acceptance and next steps:** assessment against task criteria, final task status, and inputs handed over to the next step.

Place long tables, full terminal output, and detailed data in `evidence/`. Keep only what is necessary to assess the outcome in the main report. Use "None" or "Not applicable" with a reason for irrelevant sections; do not invent content to fill the template.

## 3. Task README.md template

````markdown
# <TASK-ID> — <Task name>

- Status: <NOT_STARTED / IN_PROGRESS / BLOCKED / COMPLETE>
- Execution date: <actual date; timezone if needed>
- Requirement source: <link to the task in the milestone plan>
- Repository version: <branch / commit, if applicable>

## Conclusion

<Summarize the main results, criteria met, and important limitations.>

## Work performed

- <Work completed and the corresponding outcome.>

## Outputs

| File | Purpose |
| --- | --- |
| [Filename](evidence/<filename>) | <What this file demonstrates or provides> |

## Verification

| Check | Result | Scope / evidence |
| --- | --- | --- |
| <Command or verification method> | <PASS / FAIL / BLOCKED / NOT_RUN> | <Scope and evidence link> |

## Open issues

| Issue | Impact | Follow-up / responsible task |
| --- | --- | --- |
| <Finding> | <Actual impact> | <Resolution or next action> |

## Acceptance and handoff

| Task criterion | Result | Evidence |
| --- | --- | --- |
| <Criterion> | <Met / Not met / Not verified> | <Link or check result> |

<State the final task status, related gate status, and inputs for the next step.>
````

## 4. Status and evidence

- Mark a task `COMPLETE` only when its own outputs and acceptance criteria have been satisfied. For audit tasks, documenting product defects is part of the outcome; fixing every defect outside the audit scope is not required to close the task.
- Record `FAIL`, `BLOCKED`, or `NOT_RUN` according to actual verification results. Do not present mock data, hard-coded values, or historical results as fresh measurements.
- Distinguish task status from milestone/gate status. A `COMPLETE` task does not automatically complete the milestone or make its gate `PASS`.
- Use relative links in reports, such as `evidence/checks.txt`; avoid paths that work only on the author's machine.
- When renaming or moving files, update affected links and manifest paths. If hashes are recorded, update hashes for files whose contents actually changed and recheck the remaining files.

## 5. Quick review index

[docs/reports/milestones/README.md](docs/reports/milestones/README.md) is the shared entry point. When adding or updating a report, update its corresponding table row:

| Task | Description | Status | Report |
| --- | --- | --- | --- |
| M0.1 | Repository audit and requirements inventory | COMPLETE | `M0.1/README.md` |

The index status must match the task report. Each task must have exactly one current row for quick discovery and review.

Existing example: [M0.1 report](docs/reports/milestones/M0.1/README.md).

## 6. Pre-handoff checks

- All report prose, headings, table labels, review index entries, and authored supporting documentation are in English.
- The correct `<TASK-ID>/` directory contains only `README.md` and `evidence/` at its top level.
- The conclusion and task status are clear at the start of the report.
- Supporting files are stored in `evidence/` and linked where cross-checking is needed.
- Local links resolve; manifest paths and hashes remain valid where applicable.
- Verification results, unresolved issues, and acceptance scope are reported accurately.
- The quick review index has been updated.
- When reporting results in the conversation, summarize the key points and link to the task's `README.md`.
