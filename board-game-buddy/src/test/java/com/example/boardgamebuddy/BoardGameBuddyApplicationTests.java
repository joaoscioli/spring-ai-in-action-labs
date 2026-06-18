package com.example.boardgamebuddy;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest(properties = {
        "spring.ai.azure.openai.chat.enabled=false",
        "spring.ai.ollama.chat.enabled=false"
})
class BoardGameBuddyApplicationTests {

    @Test
    void contextLoads() {
    }

}
