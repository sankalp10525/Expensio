// main.js — students will add JavaScript here as features are built

document.addEventListener('DOMContentLoaded', function () {
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
