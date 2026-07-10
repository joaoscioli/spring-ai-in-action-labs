package com.example.boardgamebuddy;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.stereotype.Service;

@Service
public class SpringAiBoardGameService implements BoardGameService {

    static final String SYSTEM_PROMPT_VERSION = "board-game-buddy-v1";

    static final String SYSTEM_PROMPT = """
            Prompt version: board-game-buddy-v1.
            You are a board game assistant.
            Answer only board game questions.
            If the user asks about another topic, explain that you can only help with board games.
            Prefer concise answers with rules references when the question is about gameplay.
            """;

    private final ChatClient chatClient;

    public SpringAiBoardGameService(ChatClient.Builder chatClientBuilder) {
        this.chatClient = chatClientBuilder.build();
    }

    @Override
    public Anwser askQuestion(Question question) {
        var answerText = chatClient.prompt()
                .system(SYSTEM_PROMPT)
                .user(question.question())
                .call()
                .content();
        return new Anwser(answerText);
    }
}
