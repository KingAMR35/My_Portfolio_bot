document.addEventListener('DOMContentLoaded', () => {
    const loader = document.getElementById('fact-loader');
    const card = document.getElementById('fact-card');
    const textEl = document.getElementById('fact-text');
    const nextBtn = document.getElementById('fact-next-btn');
    const shareBtn = document.getElementById('fact-share-btn');

    if (!card) return;

    let currentText = '';

    async function loadFact() {
        card.classList.remove('fade-in');
        card.classList.add('fade-out');
        if (loader) loader.style.display = 'flex';
        nextBtn.disabled = true;

        try {
            const response = await fetch('/api/random_fact');
            
            if (!response.ok) {
                throw new Error(`Сервер вернул ошибку: ${response.status} ${response.statusText}`);
            }

            const data = await response.json();

            if (data.ok) {
                currentText = data.text;
                setTimeout(() => {
                    textEl.textContent = data.text;
                    if (loader) loader.style.display = 'none';
                    card.classList.remove('fade-out');
                    card.classList.add('fade-in');
                    nextBtn.disabled = false;
                }, 300);
            } else {
                throw new Error(data.error || 'Неизвестная ошибка сервера');
            }
        } catch (err) {
            console.error("Ошибка загрузки факта:", err);
            if (loader) loader.style.display = 'none';
            
            textEl.textContent = `❌ Ошибка: ${err.message}`;
            
            card.classList.remove('fade-out');
            card.classList.add('fade-in');
            nextBtn.disabled = false;
        }
    }

    nextBtn.addEventListener('click', loadFact);

    shareBtn.addEventListener('click', async () => {
        if (!currentText) return;
        const shareText = `💡 Интересный факт:\n\n${currentText}\n\n@KingAMR_bot`;
        try {
            if (navigator.share) {
                await navigator.share({ title: 'Интересный факт', text: shareText });
            } else {
                await navigator.clipboard.writeText(shareText);
                const original = shareBtn.innerHTML;
                shareBtn.innerHTML = '<span>✅</span> Скопировано!';
                setTimeout(() => { shareBtn.innerHTML = original; }, 1500);
            }
        } catch (err) {
            if (err.name !== 'AbortError') console.error(err);
        }
    });

    loadFact();
});