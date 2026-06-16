# Evaluation Dataset Template

Use this template to define examples for evaluating AI-assisted features.

## Dataset Metadata

- dataset name:
- dataset version:
- feature:
- prompt version:
- model:
- owner:

## Example Template

```yaml
- id: billing-support-active-subscription
  userQuestion: "Why is this subscription active?"
  context: "Customer has an active monthly plan and no failed payments."
  expectedBehavior:
    - "Explains active status from the provided context"
    - "Does not invent payment details"
    - "Returns a concise support-friendly answer"
  failureCriteria:
    - "Mentions missing data that is already present"
    - "Invents a refund or cancellation policy"
    - "Fails to answer from the provided context"
```

## Evaluation Dimensions

- groundedness;
- correctness;
- completeness;
- safety;
- structure;
- tone;
- latency;
- cost.

## Review Process

1. Add or update examples.
2. Run the evaluation.
3. Compare results with the previous prompt version.
4. Record regressions.
5. Approve or reject the prompt change.

## Interview Talking Points

- Evaluation datasets make AI quality review repeatable.
- Prompt changes should be tested against known examples.
- Failure criteria are as important as expected behavior.
- Dataset versioning helps explain regressions.
