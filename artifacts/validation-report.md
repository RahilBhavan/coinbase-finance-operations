# Validation report

Executed 2026-09-20 on the local synthetic build. All files and results refer to simulated data.

| Check | Method | Result | Evidence |
|---|---|---|---|
| Full automated suite | 51 unit and integration tests | Pass | reducer, fixtures, policies, experiments, report, store, consistency |
| Oracle conformance | all 16 projected cases compared with pre-authored oracle | Pass | `generated/oracle-conformance.json` |
| Timeout and late success | reducer integration test | Pass | one attempt; timeout retained; late evidence observed |
| Replay and restart | store/reducer tests | Pass | duplicate replay idempotent; canonical ordering stable |
| Cross-order claim | reducer test | Pass | second claim opens conflict |
| Refund cap | reducer test | Pass | reservations plus settled cannot exceed capture |
| Payment/delivery separation | reducer and report tests | Pass | independent projections and cards |
| Policy fairness | four-policy tests and fingerprint | Pass | identical input fingerprint |
| Sensitivity analysis | 3,600 seeded scenarios | Pass | staffing, duration, evidence-delay, and finality-delay dimensions |
| No future leakage | actionability test | Pass | unavailable cases excluded from current decision |
| Operator desk safety | escaping, accessibility, and refusal tests | Pass | all 16 cases; unsafe recharge never executes |
| Cross-artifact consistency | independent audit gate | Pass | source hashes, run ID, counts, labels, and policy metrics agree |
| Documentation links | local link checker | Pass | zero broken relative links |

## Policy decision

The initial nine-case actionable workload produced six overdue cases under both FIFO and deadline-first. Deadline-first reduced value-weighted overdue minutes, but the declared gate required at least 15% fewer overdue cases. **Retain FIFO for that fixture scenario.** The added four-policy, 3,600-scenario sweep exposes sensitivity and tradeoffs; it does not turn synthetic handling-time assumptions into a production recommendation.

## Limits

No live protocol interoperability, wallet, transaction, external practitioner review, accessibility study with users, performance load test, or production security assessment was performed. The test suite proves behavior only for the implemented rules and synthetic corpus. The external-review protocol is ready but has not been executed.
