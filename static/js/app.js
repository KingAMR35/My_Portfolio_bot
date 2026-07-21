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

    function initTelegramHeaderButton() {
        if (!window.Telegram || !window.Telegram.WebApp) return;

        const tg = window.Telegram.WebApp;
        tg.ready();

        const isHomePage =
            window.location.pathname === "/" ||
            window.location.pathname.endsWith("index.html");

        tg.BackButton.offClick();
        tg.BackButton.hide();

        if (!isHomePage) {
            tg.BackButton.show();
            tg.BackButton.onClick(() => {
                if (window.history.length > 1) {
                    window.history.back();
                } else {
                    tg.close();
                }
            });
        }
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

    applySavedTheme();

    document.addEventListener("DOMContentLoaded", () => {
        initThemeToggle();
        initTelegramHeaderButton();
        initImageModal();
    });
})();