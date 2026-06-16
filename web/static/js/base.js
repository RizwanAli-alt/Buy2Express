document.addEventListener('DOMContentLoaded', function () {

    // ── Sidebar Toggle ────────────────────────────────────────
    const categoryToggle = document.querySelector('.category-toggle');
    const categoriesSidebar = document.querySelector('.categories-sidebar');
    const overlay = document.querySelector('.overlay');
    const closeButton = document.querySelector('.close-categories');

    function openSidebar() {
        categoriesSidebar.classList.add('active');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
        // Stagger category items in
        document.querySelectorAll('.category-item').forEach((item, i) => {
            item.style.opacity = '0';
            item.style.transform = 'translateX(-16px)';
            setTimeout(() => {
                item.style.transition = 'opacity 0.25s ease, transform 0.25s ease';
                item.style.opacity = '1';
                item.style.transform = '';
            }, 60 + i * 40);
        });
    }

    function closeSidebar() {
        categoriesSidebar.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (categoryToggle)  categoryToggle.addEventListener('click', openSidebar);
    if (closeButton)     closeButton.addEventListener('click', closeSidebar);
    if (overlay)         overlay.addEventListener('click', closeSidebar);

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && categoriesSidebar?.classList.contains('active')) {
            closeSidebar();
        }
    });

    // ── Search Suggestions ────────────────────────────────────
    const searchInput = document.querySelector('.search-bar input');
    const searchSuggestions = document.querySelector('.search-suggestions');

    if (searchInput && searchSuggestions) {
        searchInput.addEventListener('focus', () => searchSuggestions.classList.add('active'));
        searchInput.addEventListener('input', function () {
            searchSuggestions.classList.toggle('active', this.value.length >= 0);
        });
        document.addEventListener('click', function (e) {
            if (!searchInput.contains(e.target) && !searchSuggestions.contains(e.target)) {
                searchSuggestions.classList.remove('active');
            }
        });
        // Keyboard navigation in suggestions
        searchInput.addEventListener('keydown', function (e) {
            const items = searchSuggestions.querySelectorAll('.suggestion-item');
            const current = searchSuggestions.querySelector('.suggestion-item.focused');
            if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
                e.preventDefault();
                const idx = Array.from(items).indexOf(current);
                if (current) current.classList.remove('focused');
                const next = e.key === 'ArrowDown'
                    ? items[idx + 1] || items[0]
                    : items[idx - 1] || items[items.length - 1];
                if (next) {
                    next.classList.add('focused');
                    next.style.background = '#FFF8EC';
                }
            }
            if (e.key === 'Escape') searchSuggestions.classList.remove('active');
        });
    }

    // ── Smooth Scroll ─────────────────────────────────────────
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // ── Scroll-to-top Button ──────────────────────────────────
    const scrollTopBtn = document.createElement('button');
    scrollTopBtn.className = 'scroll-top';
    scrollTopBtn.setAttribute('aria-label', 'Scroll to top');
    scrollTopBtn.innerHTML = '&#8679;';
    document.body.appendChild(scrollTopBtn);

    let scrollTicking = false;
    window.addEventListener('scroll', function () {
        if (!scrollTicking) {
            requestAnimationFrame(() => {
                scrollTopBtn.classList.toggle('visible', window.scrollY > 400);
                scrollTicking = false;
            });
            scrollTicking = true;
        }
    }, { passive: true });

    scrollTopBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // ── Toast Notifications ───────────────────────────────────
    const toastContainer = document.createElement('div');
    toastContainer.className = 'toast-container';
    document.body.appendChild(toastContainer);

    window.showToast = function (message, duration = 3000) {
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;
        toastContainer.appendChild(toast);
        setTimeout(() => {
            toast.classList.add('removing');
            toast.addEventListener('animationend', () => toast.remove());
        }, duration);
    };

    // ── Cart Button Micro-interaction ─────────────────────────
    document.querySelectorAll('.btn-cart').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const original = this.innerHTML;
            this.innerHTML = '✓ Added';
            this.style.background = '#2E7D32';
            this.style.color = 'white';
            this.disabled = true;
            setTimeout(() => {
                this.innerHTML = original;
                this.style.background = '';
                this.style.color = '';
                this.disabled = false;
            }, 1800);
            window.showToast?.('Item added to cart 🛒');
        });
    });

    // ── Wishlist Button Micro-interaction ─────────────────────
    document.querySelectorAll('.product-wishlist').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const isActive = this.classList.toggle('active');
            this.innerHTML = isActive ? '❤️' : '🤍';
            this.style.transform = 'scale(1.35)';
            setTimeout(() => { this.style.transform = ''; }, 200);
            window.showToast?.(isActive ? 'Saved to wishlist ♥' : 'Removed from wishlist');
        });
    });

    // ── Scroll-reveal for product cards ───────────────────────
    if ('IntersectionObserver' in window) {
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

        document.querySelectorAll('.product-card').forEach((card, i) => {
            // Skip cards already animated by CSS (first 6)
            if (i >= 6) {
                card.style.opacity = '0';
                card.style.transform = 'translateY(24px)';
                card.style.transition = 'opacity 0.45s ease, transform 0.45s ease';
                revealObserver.observe(card);
            }
        });
    }

    // ── Header scroll shadow ──────────────────────────────────
    const header = document.querySelector('header');
    if (header) {
        window.addEventListener('scroll', function () {
            header.style.boxShadow = window.scrollY > 10
                ? '0 4px 30px rgba(0,0,0,0.35)'
                : '0 2px 20px rgba(0,0,0,0.25)';
        }, { passive: true });
    }

    // ── Nav active link ───────────────────────────────────────
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-menu a').forEach(link => {
        try {
            if (new URL(link.href).pathname === currentPath) {
                link.style.color = 'white';
                link.classList.add('active-nav');
            }
        } catch (_) {}
    });

});