(function () {
    const tg = window.Telegram && window.Telegram.WebApp ? window.Telegram.WebApp : null;
    let backHandler = null;

    function currentPath() {
        return window.location.pathname.replace(/\/+$/, "") || "/";
    }

    function isHomePage() {
        const path = currentPath();
        return path === "/" || path.endsWith("/index.html");
    }

    function applySavedTheme() {
        const savedTheme = localStorage.getItem("theme");
        document.documentElement.classList.toggle("dark-mode", savedTheme === "dark");
    }

    function initThemeToggle() {
        const toggle = document.getElementById("theme-toggle");
        if (!toggle) return;

        toggle.addEventListener("click", () => {
            const isDark = document.documentElement.classList.toggle("dark-mode");
            localStorage.setItem("theme", isDark ? "dark" : "light");
        });
    }

    function removeBackHandler() {
        if (!tg || !backHandler) return;
        try {
            tg.BackButton.offClick(backHandler);
        } catch (e) {}
        backHandler = null;
    }

    function hideBack() {
        if (!tg) return;
        removeBackHandler();
        try {
            tg.BackButton.hide();
        } catch (e) {}
    }

    function showBack() {
        if (!tg) return;
        removeBackHandler();

        backHandler = () => {
            window.history.back();
        };

        try {
            tg.BackButton.onClick(backHandler);
        } catch (e) {}

        try {
            tg.BackButton.show();
        } catch (e) {}
    }

    function syncTelegramButtons() {
        if (!tg) return;

        try {
            tg.ready();
        } catch (e) {}

        if (isHomePage()) {
            hideBack();
        } else {
            showBack();
        }

        try {
            tg.MainButton && tg.MainButton.hide();
        } catch (e) {}
    }

    function initImageModal() {
        const modal = document.getElementById("image-modal");
        const modalImg = document.getElementById("image-modal-img");
        const modalCaption = document.getElementById("image-modal-caption");
        const closeBtn = document.getElementById("image-modal-close");

        if (!modal || !modalImg || !modalCaption || !closeBtn) return;

        function openModal(img) {
            modalImg.src = img.src;
            modalImg.alt = img.alt || "";
            const caption = img.parentElement?.querySelector(".MurArt-caption");
            modalCaption.textContent = caption ? caption.textContent : "";
            modal.classList.add("show");
            modal.setAttribute("aria-hidden", "false");
            document.body.style.overflow = "hidden";
        }

        function closeModal() {
            modal.classList.remove("show");
            modal.setAttribute("aria-hidden", "true");
            modalImg.src = "";
            modalCaption.textContent = "";
            document.body.style.overflow = "";
        }

        document.querySelectorAll(".MurArt-figure .MurArt-img").forEach((img) => {
            img.addEventListener("click", () => openModal(img));
        });

        closeBtn.addEventListener("click", closeModal);

        modal.addEventListener("click", (event) => {
            if (event.target === modal) closeModal();
        });

        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape" && modal.classList.contains("show")) {
                closeModal();
            }
        });
    }

    function initChatAjax() {
        const form = document.getElementById("chat-form");
        const input = document.getElementById("message-input");
        const history = document.getElementById("chat-messages");
        const sendBtn = document.getElementById("send-btn");
        const resetForm = document.querySelector(".chat-clear-form");

        if (!form || !input || !history || !sendBtn) return;

        function scrollBottom() {
            const container = document.getElementById("chat-history");
            if (container) container.scrollTop = container.scrollHeight;
        }

        function addBubble(role, text) {
            const row = document.createElement("div");
            row.className = "chat-row " + role;

            const bubble = document.createElement("div");
            bubble.className = "chat-bubble";
            bubble.textContent = text;

            row.appendChild(bubble);
            history.appendChild(row);
            scrollBottom();
            return bubble;
        }

        scrollBottom();

        form.addEventListener("submit", async (e) => {
            e.preventDefault();

            const text = input.value.trim();
            if (!text) return;

            input.value = "";
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
                    typingBubble.textContent = data.bot;
                }
            } catch (err) {
                typingBubble.textContent = "Ошибка сети";
            } finally {
                input.disabled = false;
                sendBtn.disabled = false;
                input.focus();
                scrollBottom();
            }
        });

        if (resetForm) {
            resetForm.addEventListener("submit", async (e) => {
                e.preventDefault();

                try {
                    await fetch("/AI_assistant_bot/reset", { method: "POST" });
                    history.replaceChildren();
                    scrollBottom();
                } catch (err) {}
            });
        }
    }

    function initAll() {
        applySavedTheme();
        initThemeToggle();
        initImageModal();
        initChatAjax();
        syncTelegramButtons();
    }

    document.addEventListener("DOMContentLoaded", initAll);
    window.addEventListener("pageshow", syncTelegramButtons);
    window.addEventListener("popstate", syncTelegramButtons);
    window.addEventListener("focus", syncTelegramButtons);
    document.addEventListener("visibilitychange", () => {
        if (!document.hidden) syncTelegramButtons();
    });
})();