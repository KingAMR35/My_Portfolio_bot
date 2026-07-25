(function () {
    const tg = window.Telegram && window.Telegram.WebApp ? window.Telegram.WebApp : null;
    const STACK_KEY = "miniapp_nav_stack";
    let backHandler = null;
    let closeHandler = null;
    let bound = false;

    function currentPath() {
        return window.location.pathname.replace(/\/+$/, "") || "/";
    }

    function isHomePage() {
        const path = currentPath();
        return path === "/" || path.endsWith("/index.html");
    }

    function getStack() {
        try {
            return JSON.parse(sessionStorage.getItem(STACK_KEY) || "[]");
        } catch (e) {
            return [];
        }
    }

    function setStack(stack) {
        sessionStorage.setItem(STACK_KEY, JSON.stringify(stack));
    }

    function initStack() {
        const stack = getStack();
        const path = currentPath();
        
        if (!stack.length) {
            setStack([path]);
            return;
        }
        if (stack[stack.length - 1] !== path) {
            stack.push(path);
            setStack(stack);
        }
    }

    function goPrev() {
        const stack = getStack();
        if (stack.length <= 1) {
            if (tg) {
                try { tg.close(); } catch (e) {}
            } else {
                window.location.href = "/";
            }
            return;
        }
        stack.pop();
        const prev = stack[stack.length - 1] || "/";
        setStack(stack);
        window.location.replace(prev);
    }

    window.goBack = goPrev;

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

    function removeCloseHandler() {
        if (!tg || !closeHandler) return;
        try {
            tg.CloseButton.offClick(closeHandler);
        } catch (e) {}
        closeHandler = null;
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
            goPrev();
        };

        try {
            tg.BackButton.onClick(backHandler);
            tg.BackButton.show();
        } catch (e) {}
    }

    function hideClose() {
        if (!tg) return;
        removeCloseHandler();
        try {
            tg.CloseButton.hide();
        } catch (e) {}
    }

    function showClose() {
        if (!tg) return;

        removeCloseHandler();
        closeHandler = () => {
            tg.close();
        };

        try {
            tg.CloseButton.onClick(closeHandler);
            tg.CloseButton.show();
        } catch (e) {}
    }

    function syncTelegramButtons() {
        if (!tg) return;

        try {
            tg.ready();
        } catch (e) {}

        if (isHomePage()) {
            hideBack();
            showClose();
        } else {
            showBack();
            hideClose();
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
                    await fetch(resetForm.action, {
                        method: "POST"
                    });
                    window.location.reload();
                } catch (err) {
                    window.location.reload();
                }
            });
        }
    }

    function bindNavigationLinks() {
        if (bound) return;
        bound = true;

        document.querySelectorAll("a[href]").forEach((link) => {
            const href = link.getAttribute("href");
            if (!href || href === "#" || href.startsWith("http") || href.startsWith("javascript:")) return;

            link.addEventListener("click", () => {
                initStack();
            });
        });
    }

    function initAll() {
        applySavedTheme();
        initThemeToggle();
        initStack();
        initImageModal();
        initChatAjax();
        bindNavigationLinks();
        syncTelegramButtons();
        
        if (tg) {
            try {
                tg.expand();
            } catch (e) {}
        }
    }

    document.addEventListener("DOMContentLoaded", initAll);
    window.addEventListener("pageshow", syncTelegramButtons);
    window.addEventListener("focus", syncTelegramButtons);
    document.addEventListener("visibilitychange", () => {
        if (!document.hidden) syncTelegramButtons();
    });
})();

document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('click', function(event) {
        const messageInput = document.getElementById('message-input');
        const chatForm = document.getElementById('chat-form');

        if (document.activeElement === messageInput) {
            if (!chatForm.contains(event.target)) {
                messageInput.blur(); 
            }
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('message-input');
    const chatForm = document.getElementById('chat-form');
    
    if (!messageInput || !chatForm) return;
    
    const bringInputIntoView = () => {
        setTimeout(() => {
            chatForm.scrollIntoView({ behavior: 'smooth', block: 'end' });
        }, 350);
    };

    messageInput.addEventListener('focus', bringInputIntoView);

    window.addEventListener('resize', () => {
        if (document.activeElement === messageInput) {
            setTimeout(() => {
                chatForm.scrollIntoView({ behavior: 'auto', block: 'end' });
            }, 100);
        }
    });

    document.addEventListener('click', function(event) {
        if (document.activeElement === messageInput) {
            if (!chatForm.contains(event.target)) {
                messageInput.blur(); 
            }
        }
    });
    
    if (window.Telegram && window.Telegram.WebApp) {
        window.Telegram.WebApp.ready();
        window.Telegram.WebApp.expand();
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const tg = window.Telegram && window.Telegram.WebApp ? window.Telegram.WebApp : null;
    if (!tg) return;
    
    tg.ready();
    tg.expand();

    const user = tg.initDataUnsafe?.user;
    const hiddenUserId = document.getElementById('hidden-user-id');
    const hiddenUsername = document.getElementById('hidden-username');
    
    if (user && hiddenUserId && hiddenUsername) {
        hiddenUserId.value = user.id;
        hiddenUsername.value = user.username || 'Anonymous';
    }

    const guessForm = document.getElementById('guess-form');
    const submitBtn = guessForm?.querySelector('.btn-main');
    const resetBtn = document.getElementById('reset-btn');

    if (!guessForm) return;

    function updateUI(data) {
        const triesEl = document.getElementById('tries');
        const statusEl = document.getElementById('status');
        const msgEl = document.getElementById('message');
        const numberEl = document.getElementById('target-number');
        
        if (triesEl) triesEl.textContent = data.tries;
        if (statusEl) statusEl.textContent = data.status;
        
        if (msgEl) {
            msgEl.style.animation = 'none';
            msgEl.offsetHeight;
            msgEl.className = `message ${data.message_class}`;
            msgEl.textContent = data.message;
            msgEl.style.animation = '';
        }

        if (numberEl) {
            if (data.reveal_number) {
                numberEl.textContent = data.the_number;
                createConfetti();
            } else {
                numberEl.textContent = '?';
            }
        }
    }

    if (guessForm && submitBtn) {
        guessForm.addEventListener('submit', (e) => {
            e.preventDefault();
            submitBtn.disabled = true;
            submitBtn.textContent = 'Проверяю...';

            const formData = new FormData(guessForm);

            fetch('/guess', { method: 'POST', body: formData })
            .then(response => response.json())
            .then(data => {
                updateUI(data);
                const guessInput = guessForm.querySelector('input[name="guess"]');
                if (guessInput) {
                    guessInput.value = '';
                    guessInput.focus();
                }
            })
            .catch(err => {
                updateUI({
                    tries: document.getElementById('tries')?.textContent || '0',
                    status: "Ошибка",
                    message: "❌ Ошибка сети.",
                    message_class: "error",
                    reveal_number: false
                });
            })
            .finally(() => {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Проверить';
            });
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            resetBtn.disabled = true;
            resetBtn.textContent = 'Сброс...';

            const formData = new FormData();
            const hiddenUserIdEl = document.getElementById('hidden-user-id');
            const hiddenUsernameEl = document.getElementById('hidden-username');
            
            if (hiddenUserIdEl) formData.append('user_id', hiddenUserIdEl.value);
            if (hiddenUsernameEl) formData.append('username', hiddenUsernameEl.value);

            fetch('/reset', { method: 'POST', body: formData })
            .then(response => response.json())
            .then(data => {
                updateUI(data);
            })
            .finally(() => {
                resetBtn.disabled = false;
                resetBtn.textContent = 'Заново';
            });
        });
    }
});

function createConfetti() {
    const colors = ['#60a5fa', '#f472b6', '#34d399', '#fbbf24', '#a78bfa'];
    for (let i = 0; i < 60; i++) {
        setTimeout(() => {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + '%';
            confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.animationDuration = (Math.random() * 2 + 2) + 's';
            document.body.appendChild(confetti);
            setTimeout(() => confetti.remove(), 4000);
        }, i * 20);
    }
}