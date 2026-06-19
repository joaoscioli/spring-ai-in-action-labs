# Local Development

This document describes how to run the Spring AI lab locally without exposing
real credentials.

## Java Version

The `board-game-buddy` application is configured with a Java 17 Gradle
toolchain.

On Windows PowerShell, a local test run can use:

```powershell
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-17.0.9.9-hotspot"
$env:Path = "$env:JAVA_HOME\bin;$env:Path"
.\gradlew.bat test
```

## Model Provider

The runnable example currently uses the OpenAI Spring AI starter. Other
providers can be documented as future variants, but the executable sample should
keep one default provider to avoid ambiguous auto-configuration.

## Test Strategy

Tests use WireMock and a canned OpenAI-compatible response so the suite can
validate application behavior without calling a real model provider.

## Credential Rule

Do not commit real provider API keys. Local examples can use fake values for
tests and documentation, but real credentials should come from environment
variables or a local secret manager.
