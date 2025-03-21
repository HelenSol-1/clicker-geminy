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

// Проверка переменных окружения
const GEMINI_API_KEY = process.env.GEMINI_API_KEY || "❌ Не найден";
const GOOGLE_APPLICATION_CREDENTIALS = process.env.GOOGLE_APPLICATION_CREDENTIALS || "Не задан";
const PORT = process.env.PORT || 5000;


// Обработчик генерации изображения
app.post("/generate-image", async (req, res) => {
  const { prompt } = req.body;
  console.log("Получен запрос на генерацию с prompt:", prompt);

  try {
    // Инициализируем GoogleAuth с использованием JSON-ключа
    console.log("Инициализация GoogleAuth...");
    const auth = new GoogleAuth({
      keyFile: process.env.GOOGLE_APPLICATION_CREDENTIALS,
      scopes: ["https://www.googleapis.com/auth/generativelanguage"],
    });
    const client = await auth.getClient();
    let tokenObj = await client.getAccessToken();
    let token = typeof tokenObj === "string" ? tokenObj : tokenObj.token;
    console.log("Access token получен:", token ? "Получен" : "Не получен");

    // Формируем URL запроса для модели gemini-pro
    const url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent";
    console.log("Формирование запроса к URL:", url);

    // Тело запроса
    const requestBody = {
      contents: [
        { parts: [{ text: prompt }] }
      ]
    };

    console.log("Отправка запроса к Gemini API...");
    const response = await axios.post(url, requestBody, {
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      }
    });

    console.log("Ответ от Gemini API:", response.data);

    // Извлекаем URL изображения, если есть
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
    console.error("Ошибка Gemini API:", error.response ? JSON.stringify(error.response.data, null, 2) : error.message);
    res.status(500).json({ error: "Ошибка генерации изображения" });
  }
});

app.listen(port, () => {
  console.log(`🚀 Сервер запущен на порту ${port}`);
});
