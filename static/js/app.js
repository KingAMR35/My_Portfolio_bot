(function () {
    const tg = window.Telegram && window.Telegram.WebApp ? window.Telegram.WebApp : null;
    const STACK_KEY = "miniapp_nav_stack";
    let backHandler = null;
    let closeHandler = null;
    let bound = false;

    window.tg = tg;

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
        try { tg.BackButton.offClick(backHandler); } catch (e) {}
        backHandler = null;
    }

    function removeCloseHandler() {
        if (!tg || !closeHandler) return;
        try { tg.CloseButton.offClick(closeHandler); } catch (e) {}
        closeHandler = null;
    }

    function hideBack() {
        if (!tg) return;
        removeBackHandler();
        try { tg.BackButton.hide(); } catch (e) {}
    }

    function showBack() {
        if (!tg) return;
        removeBackHandler();
        backHandler = () => { goPrev(); };
        try {
            tg.BackButton.onClick(backHandler);
            tg.BackButton.show();
        } catch (e) {}
    }

    function hideClose() {
        if (!tg) return;
        removeCloseHandler();
        try { tg.CloseButton.hide(); } catch (e) {}
    }

    function showClose() {
        if (!tg) return;
        removeCloseHandler();
        closeHandler = () => { tg.close(); };
        try {
            tg.CloseButton.onClick(closeHandler);
            tg.CloseButton.show();
        } catch (e) {}
    }

    function syncTelegramButtons() {
        if (!tg) return;
        try { tg.ready(); } catch (e) {}

        if (isHomePage()) {
            hideBack();
            showClose();
        } else {
            showBack();
            hideClose();
        }

        try { tg.MainButton && tg.MainButton.hide(); } catch (e) {}
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
        bindNavigationLinks();
        syncTelegramButtons();

        if (tg) {
            try { tg.expand(); } catch (e) {}

            const user = tg.initDataUnsafe?.user;
            const hiddenUserId = document.getElementById('hidden-user-id');
            const hiddenUsername = document.getElementById('hidden-username');
            
            if (user && hiddenUserId && hiddenUsername) {
                hiddenUserId.value = user.id;
                hiddenUsername.value = user.username || 'Anonymous';
            }

            if (user) {
                fetch('/register_user', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        user_id: user.id,
                        username: user.username || 'Anonymous'
                    })
                }).catch(err => console.error('Ошибка регистрации:', err));
            }
        }
    }

    document.addEventListener("DOMContentLoaded", initAll);
    window.addEventListener("pageshow", syncTelegramButtons);
    window.addEventListener("focus", syncTelegramButtons);
    document.addEventListener("visibilitychange", () => {
        if (!document.hidden) syncTelegramButtons();
    });
})();