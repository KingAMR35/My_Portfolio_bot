document.addEventListener('DOMContentLoaded', () => {
    const textarea = document.getElementById('tts-text');
    const charCount = document.getElementById('char-count');
    const generateBtn = document.getElementById('tts-generate');
    const resultBlock = document.getElementById('tts-result');
    const audioEl = document.getElementById('tts-audio');
    const resultLang = document.getElementById('result-lang');
    const shareBtn = document.getElementById('download-btn');
    const copyBtn = document.getElementById('tts-copy');
    const errorBlock = document.getElementById('tts-error');
    const langBtns = document.querySelectorAll('.lang-btn');

    if (!textarea || !generateBtn) return;

    let currentLang = 'ru';
    let currentText = '';
    let currentAudioUrl = '';

    const LANG_NAMES = {
        'ru': '🇷🇺 Русский',
        'en': '🇺🇸 Английский',
        'uk': '🇺🇦 Украинский',
        'de': '🇩🇪 Немецкий',
        'fr': '🇫🇷 Французский',
        'es': '🇪🇸 Испанский',
        'it': '🇮🇹 Итальянский',
        'ja': '🇯🇵 Японский',
        'ko': '🇰🇷 Корейский',
        'zh-CN': '🇨🇳 Китайский',
        'ar': '🇸🇦 Арабский',
        'hi': '🇮🇳 Индийский'
    };

    textarea.addEventListener('input', () => {
        charCount.textContent = textarea.value.length;
    });

    langBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            langBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentLang = btn.dataset.lang;
        });
    });

    generateBtn.addEventListener('click', async () => {
        const text = textarea.value.trim();
        if (!text) {
            showError('Введите текст для озвучки');
            return;
        }

        generateBtn.disabled = true;
        generateBtn.querySelector('.btn-text').style.display = 'none';
        generateBtn.querySelector('.btn-loader').style.display = 'inline';
        errorBlock.style.display = 'none';
        resultBlock.style.display = 'none';

        const formData = new FormData();
        formData.append('text', text);
        formData.append('lang', currentLang);

        try {
            const response = await fetch('/tts/generate', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.ok) {
                currentText = data.text;
                currentAudioUrl = data.audio_url;
                audioEl.src = data.audio_url;
                resultLang.textContent = LANG_NAMES[data.lang] || data.lang;
                resultBlock.style.display = 'block';
                audioEl.play();
            } else {
                showError(data.error || 'Ошибка генерации');
            }
        } catch (err) {
            showError('Ошибка сети: ' + err.message);
        } finally {
            generateBtn.disabled = false;
            generateBtn.querySelector('.btn-text').style.display = 'inline';
            generateBtn.querySelector('.btn-loader').style.display = 'none';
        }
    });

    copyBtn.addEventListener('click', () => {
        if (!currentText) return;
        navigator.clipboard.writeText(currentText).then(() => {
            copyBtn.textContent = '✅ Скопировано!';
            setTimeout(() => {
                copyBtn.textContent = '📋 Копировать текст';
            }, 1500);
        }).catch(() => {
            showError('Не удалось скопировать');
        });
    });

    shareBtn.addEventListener('click', async () => {
        if (!currentAudioUrl || !currentText) {
            showError('Сначала сгенерируйте речь');
            return;
        }

        try {
            shareBtn.disabled = true;
            shareBtn.textContent = '⏳ Подготовка...';

            const response = await fetch(currentAudioUrl);
            const blob = await response.blob();
            
            const file = new File([blob], 'speech.mp3', { type: 'audio/mpeg' });
            
            const shareText = `🎙️ Озвученный текст:\n\n"${currentText}"\n\n🌐 Язык: ${LANG_NAMES[currentLang] || currentLang}\n\n@KingAMR_bot`;

            if (navigator.canShare && navigator.canShare({ files: [file] })) {
                await navigator.share({
                    title: 'Text to Speech',
                    text: shareText,
                    files: [file]
                });
                shareBtn.textContent = '✅ Отправлено!';
            } else if (navigator.share) {
                await navigator.share({
                    title: 'Text to Speech',
                    text: shareText
                });
                shareBtn.textContent = '✅ Отправлено!';
            } else {
                await navigator.clipboard.writeText(shareText);
                shareBtn.textContent = '📋 Скопировано в буфер!';
            }

            setTimeout(() => {
                shareBtn.textContent = 'Поделиться';
                shareBtn.disabled = false;
            }, 2000);

        } catch (err) {
            if (err.name !== 'AbortError') {
                showError('Ошибка шаринга: ' + err.message);
            }
            shareBtn.textContent = 'Поделиться';
            shareBtn.disabled = false;
        }
    });

    function showError(msg) {
        errorBlock.textContent = '❌ ' + msg;
        errorBlock.style.display = 'block';
    }
});