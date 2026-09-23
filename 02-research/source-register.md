# Source register

Reviewed 2026-09-20. Technical pages are mutable; freeze a commit/release before implementation.

| ID | Primary source | Evidence used | Date/evidence status | Design consequence |
|---|---|---|---|---|
| S1 | [x402 v2 specification](https://github.com/coinbase/x402/blob/main/specs/x402-specification-v2.md) | Defines payment requirements/payloads; separate verify and settle responses; `exact` EVM uses EIP-3009; amount is atomic-unit string; nonce prevents authorization replay | Opened 2026-09-20; branch is mutable | Model authorization, verification, settlement, and business delivery as separate facts. Pin a commit before build. |
| S2 | [Base transaction finality](https://docs.base.org/specifications/transactions/transaction-finality) | Distinguishes Flashblock, L2 inclusion, L1 batch inclusion, and L1 batch finality; ordinary L2 transactions are not the seven-day withdrawal path | Opened 2026-09-20 | Store stage, evidence time, and observation time; never convert a success flag into strongest finality. Timings are not service guarantees. |
| S3 | [Coinbase CDP SDK x402 examples](https://github.com/coinbase/cdp-sdk/tree/main/examples/typescript/x402) | First-party runnable examples exist for x402 client and resource-server flows; testnet USDC/account setup is required for live examples | Search-verified 2026-09-20 | Confirms later interoperability is feasible but unnecessary for the synthetic first build. No account or dependency required now. |
| S4 | [x402 repository](https://github.com/x402-foundation/x402) | Official schemas, examples, packages, and tests are public | Reviewed through specification 2026-09-20 | Candidate protocol-shape source; not an operational incident dataset. |
| S5 | Prior project package | Earlier lifecycle, fixtures, metrics, and delivery standard | Copied 2026-09-20 | Reused selectively; originals preserved. |

## Access limitations

The current Coinbase careers navigation was previously blocked by browser administrator-policy verification. This plan does not bypass or proxy that restriction. Therefore role availability and eligibility remain provisional. Some earlier Base payment/refund guide URLs have moved or were not directly accessible in the research tool; no current claim depends solely on those inaccessible pages.

## Assumption register

| ID | Assumption | How challenged |
|---|---|---|
| A1 | One asset, one entity, Base Sepolia label, x402 v2 `exact` | reject mixed network/asset evidence; keep totals separate |
| A2 | Eight operator-hours/day and deterministic handling durations | half/double handling times |
| A3 | Deadline-first then value tie-breaker is the candidate policy | compare with FIFO on identical seeded events |
| A4 | L2 inclusion is sufficient for simulated delivery release | rerun at stronger evidence-stage requirement |
| A5 | Refund reservation begins at approval | concurrent approval fixture must not over-reserve |

