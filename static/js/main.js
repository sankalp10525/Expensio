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

    var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // --- App-wide "settle" entrance -------------------------------------
    // Fade-and-rise the main sections and key content blocks of each page
    // so views ease into place. querySelectorAll returns document order,
    // so the index gives a natural top-to-bottom stagger. The .settle
    // class is inert under reduced motion (handled in CSS), and absent
    // JS the content simply renders as-is. Runs once the loader lifts.
    function revealPage() {
        var settleTargets = document.querySelectorAll(
            '.hero, .feature-card, .cta-section, ' +
            '.auth-header, .auth-card, .auth-switch, ' +
            '.legal-header, .legal-body'
        );
        Array.prototype.forEach.call(settleTargets, function (el, i) {
            el.style.setProperty('--settle-i', i);
            el.classList.add('settle');
        });

        // Hero mock bars fill from zero once the card has settled, giving
        // the landing visual a satisfying second beat.
        if (!prefersReducedMotion) {
            var mockBars = document.querySelectorAll('.mock-bar');
            Array.prototype.forEach.call(mockBars, function (bar) {
                var target = bar.style.width;
                bar.style.transition = 'none';   // reset to empty without animating
                bar.style.width = '0';
                void bar.offsetWidth;            // flush the reset
                bar.style.transition = '';       // restore the stylesheet's width transition
                setTimeout(function () { bar.style.width = target; }, 500);
            });
        }
    }

    // --- Page loader ----------------------------------------------------
    // The loader covers the page on first paint; once we've shown it for a
    // frame we fade it out and let the content settle in underneath. It is
    // shown again while a same-site navigation is in flight.
    var loader = document.getElementById('page-loader');

    if (loader) {
        window.requestAnimationFrame(function () {
            window.requestAnimationFrame(function () {
                loader.classList.add('is-hidden');
                revealPage();
            });
        });

        var showLoader = function () { loader.classList.remove('is-hidden'); };

        // Spinner while navigating to another page via a normal link click.
        document.addEventListener('click', function (event) {
            if (event.defaultPrevented || event.button !== 0) return;
            if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
            var link = event.target.closest ? event.target.closest('a') : null;
            if (!link) return;
            var href = link.getAttribute('href');
            if (!href || href.charAt(0) === '#') return;
            if (link.target === '_blank' || link.hasAttribute('download')) return;
            if (link.origin && link.origin !== window.location.origin) return;
            showLoader();
        });

        // ...and while a form (login / register) submits.
        Array.prototype.forEach.call(document.querySelectorAll('form'), function (form) {
            form.addEventListener('submit', function () { showLoader(); });
        });

        // Returning via the back/forward cache can restore the page with the
        // spinner still up — make sure it's cleared.
        window.addEventListener('pageshow', function (event) {
            if (event.persisted) loader.classList.add('is-hidden');
        });
    } else {
        revealPage();
    }

    // --- Profile page interactivity (no-ops on pages without these elements) ---

    // Time-of-day greeting personalised to the logged-in user.
    var greeting = document.querySelector('.profile-greeting');
    if (greeting) {
        var name = greeting.getAttribute('data-name') || '';
        var hour = new Date().getHours();
        var salutation = hour < 12 ? 'Good morning'
            : hour < 18 ? 'Good afternoon'
            : 'Good evening';
        greeting.textContent = salutation + (name ? ', ' + name : '');
    }

    // Copy email (or any value) to the clipboard with brief button feedback.
    var copyButtons = document.querySelectorAll('.copy-btn');
    Array.prototype.forEach.call(copyButtons, function (btn) {
        var original = btn.textContent;
        var resetTimer;

        btn.addEventListener('click', function () {
            var value = btn.getAttribute('data-copy') || '';

            function showCopied() {
                btn.textContent = 'Copied!';
                btn.classList.add('is-copied');
                clearTimeout(resetTimer);
                resetTimer = setTimeout(function () {
                    btn.textContent = original;
                    btn.classList.remove('is-copied');
                }, 1500);
            }

            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(value).then(showCopied, function () {});
            }
        });
    });

    // Count the "days as member" badge up from zero on load.
    var badge = document.querySelector('.profile-badge');
    if (badge) {
        var target = parseInt(badge.getAttribute('data-days'), 10) || 0;
        var unit = function (n) { return n + ' day' + (n === 1 ? '' : 's'); };

        if (prefersReducedMotion || target === 0) {
            badge.textContent = unit(target);
        } else {
            var start = null;
            var duration = 800;
            var step = function (timestamp) {
                if (start === null) start = timestamp;
                var progress = Math.min((timestamp - start) / duration, 1);
                badge.textContent = unit(Math.round(progress * target));
                if (progress < 1) window.requestAnimationFrame(step);
            };
            window.requestAnimationFrame(step);
        }
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
