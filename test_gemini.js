import 'dotenv/config';
import axios from 'axios';

async function testGeminiAPI() {
    try {
        const apiKey = process.env.GEMINI_API_KEY;
        if (!apiKey) {
            console.error("❌ API-ключ не найден. Проверь .env!");
            return;
        }

        const url = `https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=${apiKey}`;

        const requestData = {
            contents: [
                {
                    parts: [
                        { text: "Объясни, как работает искусственный интеллект." }
                    ]
                }
            ]
        };

        console.log("🔍 Отправляем тестовый запрос...");
        const response = await axios.post(url, requestData, {
            headers: { "Content-Type": "application/json" }
        });

        console.log("✅ Успешный ответ от Gemini API:", JSON.stringify(response.data, null, 2));
    } catch (error) {
        console.error("❌ Ошибка Gemini API:", error.response ? error.response.data : error.message);
    }
}

testGeminiAPI();
