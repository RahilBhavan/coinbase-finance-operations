# Three designs compared

Scores are planning judgments (1 weak–5 strong), not measured outcomes.

| Design | Decision value | Control depth | Buildability | Reviewer clarity | Total /20 |
|---|---:|---:|---:|---:|---:|
| A. Append-only ledger + deterministic reducer + exception queue | 5 | 5 | 4 | 5 | **19** |
| B. Mutable order table + status dashboard | 3 | 2 | 5 | 4 | 14 |
| C. Event-sourced services + live Base Sepolia adapter | 4 | 5 | 1 | 3 | 13 |

## Selection: A

It makes late evidence, replay, restart, and auditability first-class without turning a prototype into distributed-systems theater. Payment and fulfillment evolve independently; a derived case view can be rebuilt from events. The queue policy is testable against the same immutable workload.

## Rejected tradeoffs

Design B is fastest, but a single mutable `status` invites impossible states and erases how a timeout became a late success. It can still be a UI projection, not the source of truth.

Design C best resembles a production integration but requires wallets, facilitator behavior, dependency/version decisions, and operational assumptions that add little to the core finance-operations decision. Defer it until the local controls pass; even then, use only Base Sepolia and treat it as interoperability evidence, not production validation.

