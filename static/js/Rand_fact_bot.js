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
        loader.style.display = 'flex';
        nextBtn.disabled = true;

        try {
            const response = await fetch('/api/random_fact');
            const data = await response.json();

            if (data.ok) {
                currentText = data.text;

                setTimeout(() => {
                    textEl.textContent = data.text;
                    loader.style.display = 'none';
                    card.classList.remove('fade-out');
                    card.classList.add('fade-in');
                    nextBtn.disabled = false;
                }, 300);
            } else {
                throw new Error(data.error || 'Ошибка');
            }
        } catch (err) {
            loader.style.display = 'none';
            textEl.textContent = '❌ Ошибка загрузки. Попробуй ещё раз!';
            card.classList.remove('fade-out');
            card.classList.add('fade-in');
            nextBtn.disabled = false;
        }
    }

    nextBtn.addEventListener('click', loadFact);

    shareBtn.addEventListener('click', async () => {
        if (!currentText) return;

        const shareText = `💡 Интересный факт:\n\n${currentText}`;

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