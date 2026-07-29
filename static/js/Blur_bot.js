document.addEventListener('DOMContentLoaded', () => {
    if (window.Telegram && window.Telegram.WebApp) {
        window.Telegram.WebApp.ready();
        window.Telegram.WebApp.expand(); 
    }

    const fileInput = document.getElementById('file-input');
    const dropZone = document.getElementById('drop-zone');
    const resultArea = document.getElementById('result-area');
    const resultImage = document.getElementById('result-image');
    const downloadBtn = document.getElementById('download-btn');
    const flashMessages = document.getElementById('flash-messages');

    let currentBlobUrl = '';
    let currentFilename = 'blurred.png';

    // Drag & Drop события
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
        }, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
    });

    dropZone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files.length) {
            fileInput.files = files;
            fileInput.dispatchEvent(new Event('change'));
        }
    });

    dropZone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        // Сбрасываем value, чтобы можно было выбрать тот же файл повторно
        fileInput.value = '';

        if (currentBlobUrl) {
            URL.revokeObjectURL(currentBlobUrl);
        }

        dropZone.querySelector('p').textContent = 'Обработка...';
        dropZone.style.pointerEvents = 'none'; // Блокируем клики
        flashMessages.innerHTML = '';
        resultArea.style.display = 'none';

        const formData = new FormData();
        formData.append('file', file);

        try {
            console.log('Отправка файла на сервер...');
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const data = await response.json().catch(() => ({}));
                throw new Error(data.error || 'Ошибка сервера');
            }

            console.log('Файл получен, создаем Blob...');
            const blob = await response.blob();
            currentBlobUrl = URL.createObjectURL(blob);
            currentFilename = response.headers.get('X-Filename') || 'blurred.png';
            
            resultImage.src = currentBlobUrl;
            resultArea.style.display = 'block';
            dropZone.querySelector('p').textContent = 'Выбрать другое фото';
        } catch (err) {
            console.error('Ошибка:', err);
            flashMessages.innerHTML = `<div class="msg error">${err.message || 'Ошибка сети'}</div>`;
            dropZone.querySelector('p').textContent = 'Нажмите для выбора фото';
        } finally {
            dropZone.style.pointerEvents = 'auto'; // Разблокируем клики
        }
    });

    downloadBtn.addEventListener('click', async () => {
        if (!currentBlobUrl) return;

        try {
            const response = await fetch(currentBlobUrl);
            const blob = await response.blob();
            const file = new File([blob], currentFilename, { type: 'image/png' });

            if (navigator.share && navigator.canShare && navigator.canShare({ files: [file] })) {
                await navigator.share({ files: [file] });
            } else {
                const a = document.createElement('a');
                a.href = currentBlobUrl;
                a.download = currentFilename;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            }
        } catch (err) {
            console.error('Ошибка сохранения:', err);
            if (err.name !== 'AbortError') {
                flashMessages.innerHTML = `<div class="msg error">Не удалось сохранить файл</div>`;
            }
        }
    });
});