document.addEventListener('DOMContentLoaded', () => {
    const tg = window.tg;
    const guessForm = document.getElementById('guess-form');
    const submitBtn = guessForm?.querySelector('.btn-main');
    const resetBtn = document.getElementById('reset-btn');
    const guessInput = guessForm?.querySelector('input[name="guess"]');

    if (!guessForm) return;

    function updateUI(data) {
        const triesEl = document.getElementById('tries');
        const statusEl = document.getElementById('status');
        const msgEl = document.getElementById('message');
        const numberEl = document.getElementById('target-number');
        
        if (triesEl) triesEl.textContent = data.tries;
        if (statusEl) statusEl.textContent = data.status;
        
        if (msgEl) {
            msgEl.style.animation = 'none';
            msgEl.offsetHeight;
            msgEl.className = `message ${data.message_class}`;
            msgEl.textContent = data.message;
            msgEl.style.animation = '';
        }

        if (numberEl) {
            if (data.reveal_number) {
                numberEl.textContent = data.the_number;
                createConfetti();
            } else {
                numberEl.textContent = '?';
            }
        }
    }

    if (guessForm && submitBtn) {
        guessForm.addEventListener('submit', (e) => {
            e.preventDefault();
            submitBtn.disabled = true;
            submitBtn.textContent = 'Проверяю...';

            const formData = new FormData(guessForm);

            fetch('/guess', { method: 'POST', body: formData })
            .then(response => response.json())
            .then(data => {
                updateUI(data);
                if (guessInput) {
                    guessInput.value = '';
                    guessInput.focus();
                }
            })
            .catch(err => {
                updateUI({
                    tries: document.getElementById('tries')?.textContent || '0',
                    status: "Ошибка",
                    message: "❌ Ошибка сети.",
                    message_class: "error",
                    reveal_number: false
                });
            })
            .finally(() => {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Проверить';
            });
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            resetBtn.disabled = true;
            resetBtn.textContent = 'Сброс...';

            const formData = new FormData();
            const hiddenUserIdEl = document.getElementById('hidden-user-id');
            const hiddenUsernameEl = document.getElementById('hidden-username');
            
            if (hiddenUserIdEl) formData.append('user_id', hiddenUserIdEl.value);
            if (hiddenUsernameEl) formData.append('username', hiddenUsernameEl.value);

            fetch('/reset', { method: 'POST', body: formData })
            .then(response => response.json())
            .then(data => {
                updateUI(data);
            })
            .finally(() => {
                resetBtn.disabled = false;
                resetBtn.textContent = 'Заново';
            });
        });
    }

    document.addEventListener('click', function(event) {
        if (document.activeElement === guessInput) {
            if (!guessForm.contains(event.target)) {
                guessInput.blur();
            }
        }
    });
});

function createConfetti() {
    const colors = ['#60a5fa', '#f472b6', '#34d399', '#fbbf24', '#a78bfa'];
    for (let i = 0; i < 60; i++) {
        setTimeout(() => {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + '%';
            confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.animationDuration = (Math.random() * 2 + 2) + 's';
            document.body.appendChild(confetti);
            setTimeout(() => confetti.remove(), 4000);
        }, i * 20);
    }
}