// main.js — students will add JavaScript here as features are built

document.addEventListener('DOMContentLoaded', function () {
    var themeToggle = document.getElementById('theme-toggle');

    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            var root = document.documentElement;
            var systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            var current = root.getAttribute('data-theme') || (systemPrefersDark ? 'dark' : 'light');
            var next = current === 'dark' ? 'light' : 'dark';

            root.setAttribute('data-theme', next);
            localStorage.setItem('expensio-theme', next);
        });
    }

    var openBtn = document.getElementById('see-how-it-works-btn');
    var modal = document.getElementById('video-modal');
    var closeBtn = document.getElementById('modal-close-btn');
    var iframe = document.getElementById('modal-video-iframe');

    if (!openBtn || !modal || !closeBtn || !iframe) return;

    var videoSrc = iframe.getAttribute('data-src');

    function openModal(event) {
        event.preventDefault();
        iframe.src = videoSrc + (videoSrc.indexOf('?') > -1 ? '&' : '?') + 'autoplay=1';
        modal.hidden = false;
    }

    function closeModal() {
        modal.hidden = true;
        iframe.src = '';
    }

    openBtn.addEventListener('click', openModal);
    closeBtn.addEventListener('click', closeModal);

    modal.addEventListener('click', function (event) {
        if (event.target === modal) {
            closeModal();
        }
    });

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && !modal.hidden) {
            closeModal();
        }
    });
});
