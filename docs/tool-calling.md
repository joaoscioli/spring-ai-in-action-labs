# Tool Calling

Tool calling lets an AI model request that the application execute a specific
backend capability.

The key idea is not that the model has direct access to the system. The key idea
is that the application exposes narrow, validated tools and stays responsible
for authorization, execution, and auditing.

## Business Scenario

Imagine a billing support assistant.

A support agent asks:

```text
Why is customer Ada's subscription marked as canceled?
```

The model should not invent account data. Instead, it can request a backend tool
that looks up subscription status from the application.

The application controls:

- which tool exists;
- which parameters are accepted;
- whether the current user is authorized;
- what data is returned to the model;
- what actions are audited.

## Safe Tool Boundary

A good tool boundary is narrow.

Example read-only tool:

```text
getSubscriptionStatus(organizationSlug, subscriptionId)
```

Good properties:

- read-only;
- domain-specific;
- validates identifiers;
- returns only necessary fields;
- does not expose database internals;
- can be tested without a model.

Risky tool:

```text
runSql(query)
```

Why risky:

- too broad;
- hard to authorize safely;
- can expose sensitive data;
- easy to misuse through prompt injection.

## Example Tool Shape

```java
public class SubscriptionTools {
    private final SubscriptionService subscriptionService;

    public SubscriptionTools(SubscriptionService subscriptionService) {
        this.subscriptionService = subscriptionService;
    }

    @Tool(description = "Find the current status of a subscription")
    public SubscriptionStatusResult getSubscriptionStatus(
            String organizationSlug,
            String subscriptionId
    ) {
        return subscriptionService.findStatus(organizationSlug, subscriptionId);
    }
}
```

The model can request the tool, but the application still executes normal Java
code through a service boundary.

## Authorization Rules

Tool calling must follow the same authorization rules as normal API calls.

Before executing a tool, the application should know:

- who is asking;
- which organization they belong to;
- which role they have;
- whether the tool is read-only or write-capable;
- whether the requested resource belongs to the allowed scope.

Write-capable tools require extra care.

For the first portfolio examples, prefer read-only tools.

## Validation Rules

Validate every tool input.

Examples:

- `organizationSlug` must match the expected slug format;
- `subscriptionId` must be a UUID;
- date ranges must have a maximum size;
- free-text search should have length limits;
- optional filters should have safe defaults.

Do not assume model-generated tool arguments are safe.

## Auditing

Important tool calls should produce audit logs.

Useful audit fields:

- authenticated user id;
- organization id or slug;
- tool name;
- resource id;
- timestamp;
- success or failure;
- correlation id.

Avoid logging:

- model secrets;
- access tokens;
- full prompt text with sensitive customer data;
- payment details.

## Failure Modes

Tool calling can fail when:

- the model requests a tool with invalid arguments;
- the requested resource does not exist;
- the user is not authorized;
- the backend dependency fails;
- the model overuses tools unnecessarily.

The application should return a safe failure response instead of exposing raw
exceptions.

## Stakeholder Explanation

```text
The assistant can ask the backend for approved information, such as subscription
status, but it cannot directly change customer accounts. Every tool is
validated, authorized, and auditable.
```

## Interview Talking Points

- Tool calling connects AI behavior to real backend capabilities.
- The model requests actions; the application decides whether and how to execute them.
- Tools should be narrow, validated, authorized, and auditable.
- Read-only tools are safer first portfolio examples.
- Prompt injection risk increases when tools can perform sensitive actions.
