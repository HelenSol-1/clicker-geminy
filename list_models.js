import 'dotenv/config';
import axios from 'axios';

async function listGeminiModels() {
    try {
        const apiKey = process.env.GEMINI_API_KEY;
        if (!apiKey) {
            console.error("❌ API-ключ не найден. Проверь .env!");
            return;
        }

        const url = `https://generativelanguage.googleapis.com/v1/models?key=${apiKey}`;

        console.log("🔍 Запрашиваем список доступных моделей...");
        const response = await axios.get(url);

        console.log("✅ Доступные модели:");
        console.log(JSON.stringify(response.data, null, 2));
    } catch (error) {
        console.error("❌ Ошибка запроса:", error.response ? error.response.data : error.message);
    }
}

listGeminiModels();
