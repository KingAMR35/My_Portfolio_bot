(function () {
    function applySavedTheme() {
        const savedTheme = localStorage.getItem("theme");
        if (savedTheme === "dark") {
            document.documentElement.classList.add("dark-mode");
        }
    }

    function initThemeToggle() {
        const toggle = document.getElementById("theme-toggle");
        if (!toggle) return;

        toggle.addEventListener("click", () => {
            const isDark = document.documentElement.classList.toggle("dark-mode");
            localStorage.setItem("theme", isDark ? "dark" : "light");
        });
    }

    function initTelegramBackButton() {
        if (!window.Telegram || !window.Telegram.WebApp) return;

        const tg = window.Telegram.WebApp;
        tg.ready();

        if (window.location.pathname === "/" || window.location.pathname === "") {
            tg.BackButton.hide();
            return;
        }

        tg.BackButton.show();
        tg.BackButton.onClick(() => {
            window.location.href = "/";
        });
    }

    applySavedTheme();

    document.addEventListener("DOMContentLoaded", () => {
        initThemeToggle();
        initTelegramBackButton();
    });
})();