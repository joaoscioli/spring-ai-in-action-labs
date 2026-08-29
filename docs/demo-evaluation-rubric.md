# Demo Evaluation Rubric

Use this rubric to evaluate a technical walkthrough of this project.

| Area | Strong Signal | Weak Signal |
| --- | --- | --- |
| AI boundary | Separates prompt, model call, validation, and fallback. | Treats the feature as only an LLM request. |
| Evaluation | Uses repeatable examples to compare behavior. | Relies only on manual prompt testing. |
| Risk control | Discusses data exposure, cost, latency, and safety. | Ignores operational and privacy concerns. |
| Testability | Tests deterministic behavior around the model. | Depends on live model behavior for every test. |

## Passing Bar

A strong demo shows how to move an AI idea toward a reliable Spring backend
feature that a team can review and operate.
