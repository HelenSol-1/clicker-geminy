document.addEventListener("DOMContentLoaded", () => {
    console.log("Страница загружена!");

    const dialogText = document.getElementById("dialog-text");

    // Проверяем, есть ли кнопка генерации изображения
    const generateBtn = document.getElementById("generate-image-btn");
    if (generateBtn) {
        generateBtn.addEventListener("click", async () => {
            const userPrompt = prompt("Что ты хочешь увидеть?");
            if (!userPrompt) return;

            dialogText.textContent = "Генерирую изображение...";

            try {
                const response = await fetch("/generate-image", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ prompt: userPrompt })
                });

                const data = await response.json();
                dialogText.textContent = data.description || "Описание недоступно";

                if (data.image_url) {
                    document.getElementById("image-container").innerHTML = `<img src="${data.image_url}" alt="Generated Image">`;
                }
            } catch (error) {
                dialogText.textContent = "Ошибка генерации изображения.";
            }
        });
    }

    // Проверяем, есть ли другие кнопки
    const askBrainBtn = document.getElementById("ask-brain-btn");
    if (askBrainBtn) {
        askBrainBtn.addEventListener("click", () => {
            dialogText.textContent = "Ты задал вопрос, мозг думает...";
        });
    }

    const chooseOptionBtn = document.getElementById("choose-option-btn");
    if (chooseOptionBtn) {
        chooseOptionBtn.addEventListener("click", () => {
            dialogText.textContent = "Ты сделал выбор.";
        });
    }

    const backBtn = document.getElementById("back-btn");
    if (backBtn) {
        backBtn.addEventListener("click", () => {
            const url = "https://clicker-pi-two.vercel.app/";
            window.location.href = url;
        });
    }

    // Кнопка "Играть в ракету" (фиксируем)
    const playRocketBtn = document.getElementById("play-rocket");
    if (playRocketBtn) {
        playRocketBtn.addEventListener("click", () => {
            const rocketUrl = "https://clicker-geminy.vercel.app/rocket-game.html";
            console.log("Открываю игру: " + rocketUrl);
            window.open(rocketUrl, "_blank");
        });
    }
});
