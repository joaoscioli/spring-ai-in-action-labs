# Prompt and Response Patterns

AI-assisted backend features need clear contracts around prompts and responses.

The model may generate text, but the application still needs predictable
boundaries, validation, fallback behavior, and tests around deterministic logic.

## Business Scenario

Imagine a SaaS billing application with an assistant that explains subscription
status to support agents.

The assistant should:

- answer using the provided subscription context;
- avoid inventing billing data;
- return a short explanation;
- include a confidence level;
- suggest the next operational action.

This is a better portfolio example than a generic chatbot because it connects AI
behavior to a backend domain.

## Prompt Template Shape

A useful prompt separates role, task, context, and output rules.

```text
You are a support assistant for a SaaS billing platform.

Task:
Explain the customer's subscription status to an internal support agent.

Rules:
- Use only the provided subscription context.
- Do not invent payment, plan, or customer data.
- If the context is insufficient, say what is missing.
- Keep the answer concise.
- Return the response using the requested structure.

Subscription context:
{subscriptionContext}

User question:
{question}
```

## Structured Response Shape

Backend systems should prefer structured responses when the model output drives
application behavior.

Example Java record:

```java
public record SubscriptionExplanation(
        String summary,
        String recommendedAction,
        String confidence,
        List<String> missingInformation
) {
}
```

Why this helps:

- the API can validate fields;
- frontend clients receive predictable data;
- tests can assert the application mapping;
- downstream workflows do not parse free-form prose.

## Prompt Boundary Rules

Prompt boundaries define what the model is allowed to do.

Good boundary rules:

- answer only from supplied context;
- do not expose secrets or internal configuration;
- do not perform account changes directly;
- ask for missing information when required;
- return a structured response when the caller expects one.

Weak boundary rules:

- "be helpful";
- "answer the user";
- "act like an expert";
- "do the best you can".

Weak instructions sound nice, but they do not protect the application.

## Failure Modes

AI features should document expected failure modes.

Common examples:

- model timeout;
- provider unavailable;
- empty response;
- response does not match expected structure;
- answer is unsupported by the provided context;
- prompt injection attempt inside user input;
- sensitive data accidentally included in context.

For each failure mode, define application behavior.

Example fallback:

```text
If the model response cannot be parsed, return a safe support workflow message
and log the parsing failure without logging the full prompt.
```

## Testing Strategy

Not every AI behavior can be made fully deterministic, but application logic
around AI calls should still be tested.

Test without calling a real model:

- prompt template rendering;
- input validation;
- response mapping;
- fallback behavior;
- controller behavior;
- service boundaries.

Test with controlled doubles:

- successful model response;
- malformed model response;
- timeout or provider error;
- missing required fields.

Evaluate separately:

- answer quality;
- hallucination rate;
- prompt regression;
- cost and latency.

## Example Service Boundary

```java
public class SubscriptionAssistantService {
    private final ChatClient chatClient;

    public SubscriptionAssistantService(ChatClient chatClient) {
        this.chatClient = chatClient;
    }

    public SubscriptionExplanation explain(String context, String question) {
        return chatClient.prompt()
                .system("You are a support assistant for a SaaS billing platform.")
                .user(user -> user.text("""
                        Subscription context:
                        {context}

                        User question:
                        {question}
                        """)
                        .param("context", context)
                        .param("question", question))
                .call()
                .entity(SubscriptionExplanation.class);
    }
}
```

The important design point is not the exact syntax. The important point is that
AI interaction is isolated behind a service boundary.

## Stakeholder Explanation

A stakeholder-friendly explanation:

```text
This feature helps support agents understand billing state faster. It does not
change account data automatically. It uses only the context provided by the
backend and returns a structured recommendation that the application can display
and validate.
```

## Interview Talking Points

- Prompt design is part of backend contract design.
- Structured output reduces fragile text parsing.
- AI service boundaries make the feature easier to test and replace.
- Fallback behavior should be designed before production use.
- Evaluation checks answer quality; unit tests check deterministic application logic.
