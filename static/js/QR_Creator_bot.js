document.addEventListener('DOMContentLoaded', () => {
    const tg = window.Telegram.WebApp;
    tg.ready();
    tg.expand();

    const themeToggle = document.getElementById('theme-toggle');
    const urlInput = document.getElementById('urlInput');
    const generateBtn = document.getElementById('generateBtn');
    const errorMessage = document.getElementById('errorMessage');
    const resultContainer = document.getElementById('resultContainer');
    const qrcodeContainer = document.getElementById('qrcode');
    const downloadBtn = document.getElementById('downloadBtn');

    let currentUrl = '';

    const applyTheme = (isDark) => {
        if (isDark) {
            document.documentElement.classList.add('dark-mode');
        } else {
            document.documentElement.classList.remove('dark-mode');
        }
    };

    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const tgTheme = tg.colorScheme === 'dark';
    applyTheme(tgTheme || prefersDark);

    themeToggle.addEventListener('click', () => {
        document.documentElement.classList.toggle('dark-mode');
        if (tg.HapticFeedback) tg.HapticFeedback.impactOccurred('light');
    });

    const isValidUrl = (string) => {
        try {
            const urlToTest = string.startsWith('http') ? string : `https://${string}`;
            new URL(urlToTest);
            return true;
        } catch (_) {
            return false;
        }
    };

    generateBtn.addEventListener('click', () => {
        let text = urlInput.value.trim();

        errorMessage.style.display = 'none';
        resultContainer.style.display = 'none';
        qrcodeContainer.innerHTML = '';

        if (!text) {
            showError('⚠️ Введите ссылку или текст.');
            return;
        }

        if (!text.startsWith('http://') && !text.startsWith('https://')) {
            text = 'https://' + text;
            urlInput.value = text;
        }

        if (isValidUrl(text)) {
            currentUrl = text;
            
            if (tg.HapticFeedback) tg.HapticFeedback.impactOccurred('medium');

            new QRCode(qrcodeContainer, {
                text: text,
                width: 200,
                height: 200,
                colorDark: "#000000",
                colorLight: "#ffffff",
                correctLevel: QRCode.CorrectLevel.H
            });

            resultContainer.style.display = 'flex';
            setTimeout(() => {
                resultContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 100);

        } else {
            showError('❌ Это не ссылка.');
            if (tg.HapticFeedback) tg.HapticFeedback.notificationOccurred('error');
        }
    });

    function showError(msg) {
        errorMessage.textContent = msg;
        errorMessage.style.display = 'block';
    }

    downloadBtn.addEventListener('click', async () => {
        if (!currentUrl) {
            if (tg.HapticFeedback) tg.HapticFeedback.notificationOccurred('error');
            alert("Сначала сгенерируйте QR-код");
            return;
        }

        downloadBtn.disabled = true;
        downloadBtn.textContent = 'Подготовка...';

        try {
            const response = await fetch('/api/generate_qr', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: currentUrl })
            });

            const data = await response.json();

            if (!data.success || !data.download_url) {
                throw new Error('Ошибка генерации QR');
            }

            const fileResponse = await fetch(data.download_url);
            const blob = await fileResponse.blob();

            const file = new File([blob], 'qrcode.png', { type: 'image/png' });

            if (navigator.share && navigator.canShare && navigator.canShare({ files: [file] })) {
                await navigator.share({
                    files: [file],
                });

                if (tg.HapticFeedback) {
                    tg.HapticFeedback.notificationOccurred('success');
                }
            } else {
                throw new Error('Web Share API не поддерживается');
            }

        } catch (error) {
            console.error('Ошибка:', error);
            
            try {
                const link = document.createElement('a');
                link.href = data.download_url;
                link.download = 'qrcode.png';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                
                if (tg.HapticFeedback) {
                    tg.HapticFeedback.notificationOccurred('success');
                }
            } catch (fallbackError) {
                if (tg.HapticFeedback) {
                    tg.HapticFeedback.notificationOccurred('error');
                }
                alert('Не удалось поделиться файлом. Попробуйте сделать скриншот.');
            }
        } finally {
            downloadBtn.disabled = false;
            downloadBtn.textContent = 'Поделиться';
        }
    });

    urlInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            generateBtn.click();
            urlInput.blur();
        }
    });
});