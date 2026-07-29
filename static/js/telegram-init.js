const tg = window.Telegram && window.Telegram.WebApp ? window.Telegram.WebApp : null;

if (tg) {
    tg.ready();
    tg.expand();
}

window.tg = tg;

document.addEventListener('DOMContentLoaded', () => {
    if (!tg) return;

    const user = tg.initDataUnsafe?.user;
    if (!user) return;

    const hiddenUserId = document.getElementById('hidden-user-id');
    const hiddenUsername = document.getElementById('hidden-username');
    if (hiddenUserId) hiddenUserId.value = user.id;
    if (hiddenUsername) hiddenUsername.value = user.username || 'Anonymous';

    fetch('/register_user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user_id: user.id,
            username: user.username || 'Anonymous'
        })
    }).catch(err => console.error('Ошибка регистрации:', err));
});