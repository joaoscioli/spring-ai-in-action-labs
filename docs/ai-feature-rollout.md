# AI Feature Rollout

AI features should be rolled out carefully because behavior can change with
prompts, models, context, and provider responses.

## Rollout Steps

1. Start with an internal-only demo.
2. Evaluate with a small dataset.
3. Add logging for latency, failures, and fallback usage.
4. Define a safe fallback response.
5. Limit the feature to a narrow use case.
6. Review costs before increasing traffic.
7. Re-evaluate after prompt or model changes.

## Rollback Triggers

- unsafe answers;
- high hallucination rate;
- unacceptable latency;
- unexpected cost increase;
- provider instability;
- tool calls that fail too often.

## Stakeholder Communication

Explain the feature in terms of:

- user value;
- known limitations;
- safety boundaries;
- cost expectations;
- next evaluation milestone.

## Portfolio Signal

Rollout planning shows that AI work is treated as product engineering. The
feature is not considered done just because a model returns an answer locally.
