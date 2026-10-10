package com.example.boardgamebuddy;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.retry.NonTransientAiException;
import org.springframework.ai.retry.TransientAiException;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Service
public class SpringAiBoardGameService implements BoardGameService {
    private static final Logger LOGGER = LoggerFactory.getLogger(SpringAiBoardGameService.class);

    static final String SYSTEM_PROMPT_VERSION = "board-game-buddy-v1";
    static final String EMPTY_RESPONSE_FALLBACK =
            "I couldn't generate an answer. Please try your board game question again.";
    static final String PROVIDER_ERROR_FALLBACK =
            "The board game assistant is unavailable right now. Please try again later.";

    static final String SYSTEM_PROMPT = """
            Prompt version: board-game-buddy-v1.
            You are a board game assistant.
            Answer only board game questions.
            If the user asks about another topic, explain that you can only help with board games.
            Prefer concise answers with rules references when the question is about gameplay.
            """;

    private final ChatClient chatClient;
    private final Counter successfulAnswers;
    private final Counter emptyResponses;
    private final Counter providerErrors;

    public SpringAiBoardGameService(ChatClient.Builder chatClientBuilder, MeterRegistry meterRegistry) {
        this.chatClient = chatClientBuilder.build();
        this.successfulAnswers = outcomeCounter(meterRegistry, "success");
        this.emptyResponses = outcomeCounter(meterRegistry, "empty_response");
        this.providerErrors = outcomeCounter(meterRegistry, "provider_error");
    }

    private static Counter outcomeCounter(MeterRegistry registry, String outcome) {
        return Counter.builder("boardgame.answers")
                .description("Completed board game answers by service outcome, after provider retries")
                .tag("prompt_version", SYSTEM_PROMPT_VERSION)
                .tag("outcome", outcome)
                .register(registry);
    }

    @Override
    public Anwser askQuestion(Question question) {
        final String answerText;
        try {
            answerText = chatClient.prompt()
                    .system(SYSTEM_PROMPT)
                    .user(question.question())
                    .call()
                    .content();
        } catch (NonTransientAiException | TransientAiException exception) {
            providerErrors.increment();
            LOGGER.warn("AI fallback promptVersion={} reason=provider_error exceptionType={}",
                    SYSTEM_PROMPT_VERSION, exception.getClass().getSimpleName());
            return new Anwser(PROVIDER_ERROR_FALLBACK);
        }
        if (answerText == null || answerText.isBlank()) {
            emptyResponses.increment();
            LOGGER.warn("AI fallback promptVersion={} reason=empty_response", SYSTEM_PROMPT_VERSION);
            return new Anwser(EMPTY_RESPONSE_FALLBACK);
        }
        successfulAnswers.increment();
        return new Anwser(answerText);
    }
}
