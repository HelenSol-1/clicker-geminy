import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import axios from "axios";
import { GoogleAuth } from "google-auth-library";

// Загружаем переменные окружения из файла .env
dotenv.config();

const app = express();
const port = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());
app.use(express.static("public"));

// Проверяем переменные окружения
if (!process.env.GOOGLE_APPLICATION_CREDENTIALS) {
  console.error("Ошибка: GOOGLE_APPLICATION_CREDENTIALS не задан в .env");
  process.exit(1);
}
if (!process.env.GEMINI_API_KEY) {
  console.error("Ошибка: GEMINI_API_KEY не задан в .env");
  process.exit(1);
}

console.log("GOOGLE_APPLICATION_CREDENTIALS:", process.env.GOOGLE_APPLICATION_CREDENTIALS);
console.log("GEMINI_API_KEY:", process.env.GEMINI_API_KEY);
console.log("Порт:", port);

app.post("/generate-image", async (req, res) => {
  const { prompt } = req.body;
  console.log("Получен запрос на генерацию с prompt:", prompt);

  try {
    // Инициализируем GoogleAuth с JSON-ключом
    console.log("Инициализация GoogleAuth...");
    const auth = new GoogleAuth({
      keyFile: process.env.GOOGLE_APPLICATION_CREDENTIALS,
      scopes: ["https://www.googleapis.com/auth/generativelanguage"],
    });
    const client = await auth.getClient();
    let token = await client.getAccessToken();
    if (typeof token !== "string") {
      token = token.token;
    }
    console.log("Получен access token:", token ? "Token получен" : "Token не получен");

    // Формируем URL запроса для модели gemini-pro
    const url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent";
    console.log("Формирование запроса к URL:", url);

    // Формируем тело запроса
    const requestBody = {
      contents: [{ parts: [{ text: prompt }] }]
    };
    console.log("Отправка POST-запроса к Gemini API...");
    const response = await axios.post(url, requestBody, {
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      }
    });

    console.log("Ответ от Gemini API получен:", response.data);

    let imageUrl = null;
    if (response.data.response_media && response.data.response_media.length > 0) {
      const image = response.data.response_media.find(media => media.media_type === "image");
      if (image) {
        imageUrl = image.uri;
      }
    }

    res.json({
      description: response.data.text || "Описание недоступно",
      image_url: imageUrl
    });

  } catch (error) {
    console.error("Ошибка Gemini API на этапе:", error.response ? JSON.stringify(error.response.data, null, 2) : error.message);
    res.status(500).json({ error: "Ошибка генерации изображения" });
  }
});

app.listen(port, () => {
  console.log(`🚀 Сервер запущен на порту ${port}`);
});
