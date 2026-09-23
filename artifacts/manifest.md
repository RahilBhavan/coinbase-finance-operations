# Artifact manifest

Prepared 2026-09-20 and revalidated 2026-09-22. The synthetic build exists in `generated/`.

| Artifact | Status | Note |
|---|---|---|
| `operations-memo.pdf` | Verified | two-page recommendation; rendered and visually reviewed |
| `state-model.md` | Verified | independent payment, fulfillment, refund, and exception states |
| `incidents-v1.jsonl` and `incidents-v1.oracle.json` | Verified | 65 events; 16 cases; separate expected-state oracle |
| `reconciliation.xlsx` | Verified | four-sheet workbook; formulas recalculated, scanned, and rendered |
| `generated/policy-results.csv` | Verified | identical-workload four-policy comparison |
| `generated/scenario-sweep-summary.json` | Verified | 3,600 seeded sensitivity scenarios with declared assumptions |
| `operator-runbook.md` | Verified | ownership, evidence, allowed/forbidden actions, closure tests |
| `validation-report.md` | Verified | automated suite plus cross-artifact consistency gate |
| `usability-review.md` | Verified self-review | no external usability claim |
| `demo.mp4` | Verified | 180-second narrated 1280x720 demo; frames inspected |
| `source-register.csv` | Verified | dated primary sources and limitations |
| `generated/exception-desk.sqlite` | Verified | append-only normalized event store |
| `generated/operator-report.html` | Verified | accessible 16-case local desk with safe static fallback |
| `operator-task-protocol.md` | Ready | external three-reviewer protocol; not yet executed |
| `package-manifest.json` | Verified | SHA-256 and byte length for PDF, workbook, and video |

`../outputs/coinbase-finance-operations-package.zip.sha256` authenticates the refreshed deterministic ZIP as a whole.

The analytical package is complete and locally reproducible. External usability validation and live protocol interoperability remain explicitly out of scope; neither is required to inspect the decision. Planned criteria are defined in [`../04-deliverables/artifact-plan.md`](../04-deliverables/artifact-plan.md).
