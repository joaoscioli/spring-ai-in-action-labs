# Technical Debt Register

This register makes project trade-offs visible instead of hiding unfinished work.

## Current Debt

| Area | Debt | Impact | Next Action |
| --- | --- | --- | --- |
| Evaluation | Evaluation templates exist before a larger dataset. | AI behavior quality is harder to compare over time. | Add curated examples with expected outcomes. |
| Provider Strategy | Model selection is documented before multi-provider code. | Fallback design is not fully executable. | Add provider abstraction and mocked fallback tests. |
| Cost Controls | Cost and latency strategy is documented before enforcement. | Runtime limits are not yet demonstrable. | Add request budgets and metrics examples. |

## Review Rule

Debt is acceptable when it is explicit, bounded, and connected to a follow-up
decision. Hidden debt is what damages engineering trust.
