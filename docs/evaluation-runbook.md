# Evaluation Runbook

This runbook describes how to review an AI-assisted feature before changing a
prompt, model, or retrieval strategy.

## Before The Change

- Identify the feature being changed.
- List the expected user-facing behavior.
- Select evaluation examples from the dataset.
- Record the current model and prompt version.

## During The Change

- Change one variable at a time when possible.
- Keep the prompt versioned.
- Run deterministic application tests.
- Run qualitative evaluation examples.
- Record surprising failures.

## After The Change

- Compare answer quality.
- Check latency expectations.
- Estimate token and cost impact.
- Review safety behavior.
- Decide whether the change is safe to demo or merge.

## Portfolio Signal

This shows that AI behavior is treated as something to evaluate and govern,
not as a black-box feature that is changed by intuition alone.
