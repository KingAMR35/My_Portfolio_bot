document.addEventListener('DOMContentLoaded', () => {
    const tg = window.Telegram.WebApp;
    tg.ready();
    tg.expand();

    const urlInput = document.getElementById('urlInput');
    const generateBtn = document.getElementById('generateBtn');
    const errorMessage = document.getElementById('errorMessage');
    const resultContainer = document.getElementById('resultContainer');
    const qrcodeContainer = document.getElementById('qrcode');
    const downloadBtn = document.getElementById('downloadBtn');

    let currentUrl = '';
    let qrCodeObj = null;

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

            qrCodeObj = new QRCode(qrcodeContainer, {
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
        if (!currentUrl || !qrCodeObj) {
            if (tg.HapticFeedback) tg.HapticFeedback.notificationOccurred('error');
            alert("Сначала сгенерируйте QR-код");
            return;
        }

        downloadBtn.disabled = true;
        downloadBtn.textContent = 'Подготовка...';

        try {
            const canvas = qrcodeContainer.querySelector('canvas');
            if (!canvas) throw new Error('Canvas не найден');

            const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));
            const file = new File([blob], 'qrcode.png', { type: 'image/png' });

            if (navigator.share && navigator.canShare && navigator.canShare({ files: [file] })) {
                await navigator.share({ files: [file] });
                if (tg.HapticFeedback) tg.HapticFeedback.notificationOccurred('success');
            } else {
                const url = URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.download = 'qrcode.png';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(url);
                if (tg.HapticFeedback) tg.HapticFeedback.notificationOccurred('success');
            }

        } catch (error) {
            console.error('Ошибка:', error);
            
            if (error.name === 'AbortError') {
                console.log('Пользователь отменил');
            } else {
                if (tg.HapticFeedback) tg.HapticFeedback.notificationOccurred('error');
                alert('Не удалось поделиться. Удерживайте QR-код для сохранения.');
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

    document.addEventListener('click', function(event) {
        if (document.activeElement === urlInput) {
            if (!document.querySelector('.input-group').contains(event.target)) {
                urlInput.blur();
            }
        }
    });
});