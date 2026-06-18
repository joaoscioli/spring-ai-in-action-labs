package com.example.boardgamebuddy;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.stereotype.Service;

@Service
public class SpringAiBoardGameService implements BoardGameService {

    private final ChatClient chatClient;

    public SpringAiBoardGameService(ChatClient.Builder chatClientBuilder) {
        this.chatClient = chatClientBuilder.build();
    }

    @Override
    public Anwser askQuestion(Question question) {
        var answerText = chatClient.prompt()
                .system("""
                        You are a board game assistant.
                        Answer only board game questions.
                        If the user asks about another topic, explain that you can only help with board games.
                        """)
                .user(question.question())
                .call()
                .content();
        return new Anwser(answerText);
    }
}
