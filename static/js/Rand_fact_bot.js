document.addEventListener('DOMContentLoaded', () => {
    const loader = document.getElementById('fact-loader');
    const card = document.getElementById('fact-card');
    const textEl = document.getElementById('fact-text');
    const nextBtn = document.getElementById('fact-next-btn');
    const shareBtn = document.getElementById('fact-share-btn');

    if (!card || !loader) return;

    let currentText = '';
    let isFirstLoad = true;

    async function loadFact() {
        nextBtn.disabled = true;
        shareBtn.disabled = true;

        if (!isFirstLoad) {
            card.classList.add('hidden');
            setTimeout(() => {
                loader.style.display = 'flex';
            }, 300);
        }

        try {
            const response = await fetch('/api/random_fact');
            
            if (!response.ok) {
                throw new Error(`Сервер вернул ошибку: ${response.status}`);
            }

            const data = await response.json();

            if (data.ok) {
                currentText = data.text;
                textEl.textContent = data.text;
            } else {
                throw new Error(data.error || 'Неизвестная ошибка сервера');
            }
        } catch (err) {
            console.error("Ошибка загрузки факта:", err);
            textEl.textContent = `❌ Ошибка: ${err.message}. Проверьте интернет.`;
        } finally {
            loader.style.display = 'none';
            
            setTimeout(() => {
                card.classList.remove('hidden');
                isFirstLoad = false;
                
                nextBtn.disabled = false;
                shareBtn.disabled = false;
            }, isFirstLoad ? 50 : 350); 
        }
    }

    nextBtn.addEventListener('click', loadFact);

    shareBtn.addEventListener('click', async () => {
        if (!currentText) return;
        
        const shareText = `💡 Интересный факт:\n\n${currentText}\n\n@KingAMR_bot`;
        const originalText = shareBtn.innerHTML;
        
        shareBtn.innerHTML = '<span>⏳</span> Отправка...';
        shareBtn.disabled = true;

        try {
            if (navigator.share) {
                await navigator.share({ title: 'Интересный факт', text: shareText });
                shareBtn.innerHTML = originalText;
            } else {
                await navigator.clipboard.writeText(shareText);
                shareBtn.innerHTML = '<span>✅</span> Скопировано!';
                setTimeout(() => { shareBtn.innerHTML = originalText; }, 1500);
            }
        } catch (err) {
            if (err.name === 'AbortError') {
                shareBtn.innerHTML = originalText;
            } else {
                console.error(err);
                shareBtn.innerHTML = '<span>❌</span> Ошибка';
                setTimeout(() => { shareBtn.innerHTML = originalText; }, 1500);
            }
        } finally {
            shareBtn.disabled = false;
        }
    });

    loadFact();
});