document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('wiki-search');
    const clearBtn = document.getElementById('wiki-clear-btn');
    const charCounter = document.getElementById('wiki-char-counter');
    const searchBtn = document.getElementById('wiki-search-btn');
    const randomBtn = document.getElementById('wiki-random-btn');
    
    const loader = document.getElementById('wiki-loader');
    const errorBlock = document.getElementById('wiki-error');
    const errorText = document.getElementById('wiki-error-text');
    const resultCard = document.getElementById('wiki-result-card');
    
    const imageWrap = document.getElementById('wiki-image-wrap');
    const imageEl = document.getElementById('wiki-image');
    const titleEl = document.getElementById('wiki-title');
    const titleMobileEl = document.getElementById('wiki-title-mobile');
    const summaryEl = document.getElementById('wiki-summary');
    const relatedBlock = document.getElementById('wiki-related');
    const relatedList = document.getElementById('wiki-related-list');
    const readMoreLink = document.getElementById('wiki-read-more');

    if (!searchInput) return;

    searchInput.addEventListener('input', () => {
        const len = searchInput.value.length;
        charCounter.textContent = `${len} / 100`;
        charCounter.classList.toggle('warning', len > 80);
        charCounter.classList.toggle('error', len >= 100);
        clearBtn.style.display = len > 0 ? 'block' : 'none';
    });

    clearBtn.addEventListener('click', () => {
        searchInput.value = '';
        searchInput.dispatchEvent(new Event('input'));
        searchInput.focus();
    });

    async function performSearch(query) {
        if (!query || query.length > 100) return;

        errorBlock.style.display = 'none';
        resultCard.style.display = 'none';
        loader.style.display = 'flex';

        try {
            const formData = new FormData();
            formData.append('query', query);

            const response = await fetch('/wiki/search', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.ok) {
                renderResult(data);
            } else {
                showError(data.error || 'Ничего не найдено');
            }
        } catch (err) {
            showError('Ошибка сети. Проверьте подключение.');
        } finally {
            loader.style.display = 'none';
        }
    }

    searchBtn.addEventListener('click', () => performSearch(searchInput.value.trim()));
    
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performSearch(searchInput.value.trim());
    });

    randomBtn.addEventListener('click', async () => {
        loader.style.display = 'flex';
        errorBlock.style.display = 'none';
        resultCard.style.display = 'none';
        
        try {
            const response = await fetch('/wiki/random');
            const data = await response.json();
            if (data.ok) {
                searchInput.value = data.title;
                searchInput.dispatchEvent(new Event('input'));
                renderResult(data);
            } else {
                showError('Не удалось получить случайную статью');
            }
        } catch (err) {
            showError('Ошибка сети');
        } finally {
            loader.style.display = 'none';
        }
    });

    function renderResult(data) {
        titleEl.textContent = data.title;
        titleMobileEl.textContent = data.title;
        
        if (data.image) {
            imageEl.src = data.image;
            imageWrap.style.display = 'block';
            titleMobileEl.style.display = 'none';
            initParallax();
        } else {
            imageWrap.style.display = 'none';
            titleMobileEl.style.display = 'block';
        }

        summaryEl.textContent = data.summary;
        readMoreLink.href = data.url;

        if (data.related && data.related.length > 0) {
            relatedList.innerHTML = data.related.slice(0, 5).map(topic => 
                `<span class="wiki-related-tag" data-topic="${topic}">${topic}</span>`
            ).join('');
            
            document.querySelectorAll('.wiki-related-tag').forEach(tag => {
                tag.addEventListener('click', () => {
                    searchInput.value = tag.dataset.topic;
                    searchInput.dispatchEvent(new Event('input'));
                    performSearch(tag.dataset.topic);
                });
            });
            relatedBlock.style.display = 'block';
        } else {
            relatedBlock.style.display = 'none';
        }

        resultCard.style.display = 'block';
        resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function initParallax() {
        const container = document.querySelector('.wiki-image-wrap');
        container.addEventListener('scroll', () => {
            const scrolled = container.scrollTop;
            imageEl.style.transform = `translateY(${scrolled * 0.4}px) scale(1.1)`;
        });
    }

    function showError(msg) {
        errorText.textContent = msg;
        errorBlock.style.display = 'flex';
    }
});