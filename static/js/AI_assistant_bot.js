document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById("chat-form");
    const input = document.getElementById("message-input");
    const history = document.getElementById("chat-messages");
    const sendBtn = document.getElementById("send-btn");
    const resetForm = document.querySelector(".chat-clear-form");
    const chatHistoryContainer = document.getElementById("chat-history");

    if (!form || !input || !history || !sendBtn || !chatHistoryContainer) return;

    function scrollBottom() {
        setTimeout(() => {
            chatHistoryContainer.scrollTop = chatHistoryContainer.scrollHeight;
        }, 50);
    }

    function autoResize() {
        input.style.height = "auto";
        input.style.height = Math.min(input.scrollHeight, 120) + "px";
        scrollBottom();
    }

    input.addEventListener("input", autoResize);
    
    input.addEventListener("focus", () => {
        setTimeout(() => {
            input.scrollIntoView({ behavior: "smooth", block: "end" });
        }, 300);
    });

    scrollBottom();

    function addBubble(role, text) {
        const row = document.createElement("div");
        row.className = "chat-row " + role;

        const bubble = document.createElement("div");
        bubble.className = "chat-bubble";
        bubble.innerHTML = text.replace(/\n/g, '<br>');

        row.appendChild(bubble);
        history.appendChild(row);
        scrollBottom();
        return bubble;
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const text = input.value.trim();
        if (!text) return;

        input.value = "";
        input.style.height = "auto";
        input.disabled = true;
        sendBtn.disabled = true;

        addBubble("user", text);
        const typingBubble = addBubble("bot", "Печатает...");

        try {
            const fd = new FormData();
            fd.append("message", text);

            const resp = await fetch("/AI_assistant_bot/send", {
                method: "POST",
                body: fd
            });

            const data = await resp.json();

            if (!data.ok) {
                typingBubble.textContent = "Ошибка отправки";
            } else {
                typingBubble.innerHTML = data.bot.replace(/\n/g, '<br>');
            }
        } catch (err) {
            typingBubble.textContent = "Ошибка сети";
        } finally {
            input.disabled = false;
            sendBtn.disabled = false;
            input.focus();
            setTimeout(() => {
                input.scrollIntoView({ behavior: "smooth", block: "end" });
            }, 100);
        }
    });

    if (resetForm) {
        resetForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            try {
                await fetch(resetForm.action, { method: "POST" });
                window.location.reload();
            } catch (err) {
                window.location.reload();
            }
        });
    }

    // Закрытие клавиатуры при клике вне поля ввода
    document.addEventListener('click', function(event) {
        if (document.activeElement === input) {
            if (!form.contains(event.target)) {
                input.blur();
            }
        }
    });

    // Прокрутка при изменении размера окна
    window.addEventListener('resize', () => {
        if (document.activeElement === input) {
            setTimeout(() => {
                form.scrollIntoView({ behavior: 'auto', block: 'end' });
            }, 100);
        }
    });
});