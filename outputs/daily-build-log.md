# Daily build log

## 2026-09-20

Decision: consolidate every business projection behind one canonical reducer and make the package fail closed when generated artifacts drift.

Evidence: all 16 oracle cases pass through the same reducer used by the application; the independent consistency gate verifies source hashes, run identity, counts, labels, and policy metrics.

Result: PASS — 51 automated tests, 16/16 oracle cases, and the generated consistency audit pass.

Decision: broaden queue analysis beyond a single FIFO/deadline-first comparison.

Evidence: FIFO, deadline-first, value-first, and SLA-window hybrid policies now run against identical fingerprinted workloads over 3,600 seeded scenarios spanning staffing, handling duration, evidence delay, and finality delay.

Result: PASS as an analytical tool; unresolved as a production recommendation because handling times remain synthetic.

Decision: turn the static report into a safe local operator desk.

Evidence: all 16 cases have navigable evidence timelines, independent payment/delivery/refund states, allowed and forbidden actions, traceability, keyboard support, and a recharge control that always refuses.

Result: PASS in automated checks; external practitioner usability review remains unperformed.

Next: run the documented three-reviewer protocol and use their error rate, time, confidence, and corrections to revise the workflow before making any operational claim.
