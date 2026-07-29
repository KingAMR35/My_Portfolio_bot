document.addEventListener('DOMContentLoaded', () => {
    const loader = document.getElementById('jokes-loader');
    const card = document.getElementById('jokes-card');
    const textEl = document.getElementById('jokes-text');
    const nextBtn = document.getElementById('jokes-next-btn');
    const shareBtn = document.getElementById('jokes-share-btn');

    if (!card) return;

    let currentJoke = '';

    async function loadJoke() {
        card.classList.remove('fade-in');
        card.classList.add('fade-out');
        loader.style.display = 'flex';
        nextBtn.disabled = true;

        try {
            const response = await fetch('/api/get_joke');
            const data = await response.json();

            if (data.ok) {
                currentJoke = data.text;

                setTimeout(() => {
                    textEl.textContent = data.text;
                    loader.style.display = 'none';
                    card.classList.remove('fade-out');
                    card.classList.add('fade-in');
                    nextBtn.disabled = false;
                }, 300);
            } else {
                throw new Error(data.error || 'Ошибка получения шутки');
            }
        } catch (err) {
            console.error('Ошибка загрузки анекдота:', err);
            loader.style.display = 'none';
            textEl.textContent = '❌ Не удалось загрузить анекдот. Попробуйте ещё раз!';
            card.classList.remove('fade-out');
            card.classList.add('fade-in');
            nextBtn.disabled = false;
        }
    }

    nextBtn.addEventListener('click', loadJoke);

    shareBtn.addEventListener('click', async () => {
        if (!currentJoke) return;

        const shareText = `😂 Смешной анекдот:\n\n${currentJoke}\n\n@KingAMR_bot`;

        try {
            if (navigator.share) {
                await navigator.share({
                    title: 'Смешной анекдот',
                    text: shareText
                });
            } else {
                await navigator.clipboard.writeText(shareText);
                const originalHTML = shareBtn.innerHTML;
                shareBtn.innerHTML = '<span>✅</span> Скопировано!';
                
                setTimeout(() => {
                    shareBtn.innerHTML = originalHTML;
                }, 1500);
            }
        } catch (err) {
            if (err.name !== 'AbortError') {
                console.error('Ошибка шаринга:', err);
            }
        }
    });

    loadJoke();
});