document.addEventListener("DOMContentLoaded", () => {
    const dialogText = document.getElementById("dialog-text");

    document.getElementById("generate-image-btn").addEventListener("click", async () => {
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

    document.getElementById("ask-brain-btn").addEventListener("click", () => {
        dialogText.textContent = "Ты задал вопрос, мозг думает...";
    });

    document.getElementById("choose-option-btn").addEventListener("click", () => {
        dialogText.textContent = "Ты сделал выбор.";
    });
    
    document.getElementById("back-btn").addEventListener("click", function() {
        if (window.Telegram && window.Telegram.WebApp) {
            window.Telegram.WebApp.openLink("https://clicker-geminy1.vercel.app/");
        } else {
            window.location.href = "https://clicker-geminy1.vercel.app/";
        }
    });
    
    document.getElementById("explore-btn").addEventListener("click", function() {
        if (window.Telegram && window.Telegram.WebApp) {
            window.Telegram.WebApp.openLink("https://clicker-geminy1.vercel.app/rocket-game.html");
        } else {
            window.location.href = "https://clicker-geminy1.vercel.app/rocket-game.html";
        }
    });

});
