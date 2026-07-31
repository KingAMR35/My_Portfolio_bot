document.addEventListener('DOMContentLoaded', () => {
    const tg = window.Telegram.WebApp;
    tg.ready();
    tg.expand();

    const textarea = document.getElementById('img-generator-text');
    const charCount = document.getElementById('char-count');
    const generateBtn = document.getElementById('generate-btn');
    const loader = document.getElementById('loader');
    const resultContainer = document.getElementById('result-container');
    const generatedImage = document.getElementById('generated-image');
    const shareBtn = document.getElementById('share-btn');
    const errorMessage = document.getElementById('error-message');
    const generatorPanel = document.querySelector('.img-generator-panel');

    let currentBlob = null;
    let currentBlobUrl = '';

    textarea.addEventListener('input', () => {
        charCount.textContent = textarea.value.length;
    });

    generateBtn.addEventListener('click', async () => {
        const query = textarea.value.trim();
        errorMessage.style.display = 'none';
        resultContainer.style.display = 'none';

        if (currentBlobUrl) {
            URL.revokeObjectURL(currentBlobUrl);
        }
        currentBlob = null;
        currentBlobUrl = '';

        if (!query) {
            errorMessage.textContent = '⚠️ Введите описание для генерации.';
            errorMessage.style.display = 'block';
            return;
        }

        generateBtn.disabled = true;
        generateBtn.innerHTML = '<span>⏳ Генерация...</span>';
        loader.style.display = 'flex';

        if (tg.HapticFeedback) tg.HapticFeedback.impactOccurred('medium');

        try {
            const user = tg.initDataUnsafe?.user || {};
            const userId = user.id || 0;
            const username = user.username || 'unknown';

            const response = await fetch('/api/generate_image', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    query: query,
                    user_id: userId,
                    username: username
                })
            });

            if (!response.ok) {
                const data = await response.json().catch(() => ({}));
                throw new Error(data.error || 'Ошибка сервера');
            }

            const data = await response.json();

            if (data.success && data.image_base64) {
                const base64Data = data.image_base64.split(',')[1];
                const byteCharacters = atob(base64Data);
                const byteNumbers = new Array(byteCharacters.length);
                for (let i = 0; i < byteCharacters.length; i++) {
                    byteNumbers[i] = byteCharacters.charCodeAt(i);
                }
                const byteArray = new Uint8Array(byteNumbers);
                currentBlob = new Blob([byteArray], { type: 'image/png' });

                currentBlobUrl = URL.createObjectURL(currentBlob);
                generatedImage.src = currentBlobUrl;

                loader.style.display = 'none';
                resultContainer.style.display = 'flex';

                if (tg.HapticFeedback) tg.HapticFeedback.notificationOccurred('success');
            } else {
                throw new Error(data.error || 'Не удалось сгенерировать изображение');
            }
        } catch (err) {
            console.error('Ошибка:', err);
            loader.style.display = 'none';
            errorMessage.textContent = `❌ Ошибка: ${err.message}`;
            errorMessage.style.display = 'block';
            if (tg.HapticFeedback) tg.HapticFeedback.notificationOccurred('error');
        } finally {
            generateBtn.disabled = false;
            generateBtn.innerHTML = '<span>✨ Сгенерировать</span>';
        }
    });

    function showError(msg) {
        errorMessage.textContent = msg;
        errorMessage.style.display = 'block';
    }

    shareBtn.addEventListener('click', async () => {
        if (!currentBlob) return;

        try {
            const file = new File([currentBlob], 'generated_image.png', { type: 'image/png' });

            if (navigator.share && navigator.canShare && navigator.canShare({ files: [file] })) {
                await navigator.share({ files: [file] });
            } else {
                const a = document.createElement('a');
                a.href = currentBlobUrl;
                a.download = 'generated_image.png';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            }
        } catch (err) {
            console.error('Ошибка сохранения:', err);
            if (err.name !== 'AbortError') {
                showError('Не удалось сохранить файл');
            }
        }
    });

    document.addEventListener('click', function(event) {
        if (document.activeElement === textarea) {
            if (!generatorPanel.contains(event.target)) {
                textarea.blur();
            }
        }
    });
});