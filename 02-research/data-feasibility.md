# Data candidate and feasibility

## Selected candidate

Use a **versioned synthetic incident corpus seeded from the public x402 v2 schemas**, not scraped chain activity. The repository/specification supplies protocol-shaped `PaymentRequirements`, `PaymentPayload`, `VerifyResponse`, and `SettlementResponse` examples. Extend those shapes with explicitly project-owned order, fulfillment, chain-observation, exception, and refund events.

Why this is the defensible choice: public chain data can show transfers and inclusion, but cannot establish the fictional seller's order, client receipt, delivery failure, refund approval, operator ownership, or business SLA. Treating transfers as operational incidents would manufacture labels. Synthetic events make expected outcomes and adverse cases explicit and reproducible.

## Feasibility result

**Feasible for the first build.** Public primary sources are sufficient to shape the payment-side fixtures, atomic-unit fields, network identifier, settlement response, and staged finality evidence. They are not sufficient for realistic incident frequencies, handling-time distributions, Coinbase controls, or delivery acknowledgments. Those must remain declared assumptions.

Create `fixtures/incidents-v1.jsonl` later with 16 hand-authored cases: four happy paths and twelve exceptions. Each line needs `fixture_id`, `event_id`, `aggregate_id`, `event_type`, `occurred_at`, `observed_at`, `schema_version`, `evidence_label`, and payload. Expected state and permissible action live in a separate oracle file so implementation output cannot silently redefine the expected result.

Minimum exceptions: authorization reject; preparation failure; timeout then late success; conclusive failure; paid/lost delivery; repeated event across restart; duplicate request; second valid authorization for paid order; amount/asset/recipient/network mismatch; payment evidence reused across orders; pre-finality observation invalidated; concurrent refund approvals with one unknown result.

Fallbacks: if x402 v2 changes before build, freeze a reviewed commit and update fixture shapes; if public examples conflict, follow the frozen spec and document divergence; if a realistic frequency source is unavailable, compare policies across transparent scenario grids rather than claiming representativeness.

