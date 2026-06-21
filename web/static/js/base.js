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

/* ============================================================
   REPLACE the existing "── Search Suggestions ──" block inside
   base.js (the one that does searchInput.addEventListener(...))
   with everything below. It now:
     1. Calls the real autocomplete endpoint as the user types
     2. Renders live product suggestions (name + price)
     3. Clicking a suggestion goes straight to that product
     4. Pressing Enter / clicking the search icon submits the
        real search form (GET ?q=...) to search_view
   ============================================================ */

const searchInput = document.querySelector('.search-bar input');
const searchForm = document.getElementById('site-search-form');
const searchSuggestions = document.querySelector('.search-suggestions');
const suggestionsResults = document.getElementById('suggestions-results');
const suggestionsResultsList = document.getElementById('suggestions-results-list');
const suggestionsEmpty = document.getElementById('suggestions-empty');

if (searchInput && searchSuggestions) {

    let debounceTimer = null;
    let activeIndex = -1;

    function openSuggestions() {
        searchSuggestions.classList.add('active');
        searchInput.setAttribute('aria-expanded', 'true');
    }

    function closeSuggestions() {
        searchSuggestions.classList.remove('active');
        searchInput.setAttribute('aria-expanded', 'false');
        activeIndex = -1;
    }

    function renderSuggestions(items) {
        suggestionsResultsList.innerHTML = '';

        if (!items.length) {
            suggestionsResults.style.display = 'none';
            suggestionsEmpty.style.display = 'block';
            suggestionsEmpty.querySelector('h3').textContent = 'No matches';
            suggestionsEmpty.querySelector('span').textContent = 'Try a different search term';
            return;
        }

        suggestionsEmpty.style.display = 'none';
        suggestionsResults.style.display = 'block';

        items.forEach(function (item) {
            const row = document.createElement('a');
            row.href = '/products/' + item.id + '/';   // adjust to your product detail URL pattern
            row.className = 'suggestion-item';
            row.setAttribute('role', 'option');
            row.setAttribute('tabindex', '0');
            row.style.textDecoration = 'none';
            row.style.justifyContent = 'space-between';
            row.innerHTML =
                '<span style="display:flex;align-items:center;gap:10px;">' +
                    '<i class="fas fa-magnifying-glass" aria-hidden="true"></i>' +
                    '<span>' + item.name + '</span>' +
                '</span>' +
                '<span style="color:var(--primary-dark);font-weight:700;">$' + item.price + '</span>';
            suggestionsResultsList.appendChild(row);
        });
    }

    function fetchSuggestions(query) {
        fetch('/search/autocomplete/?q=' + encodeURIComponent(query))
            .then(function (res) { return res.json(); })
            .then(function (data) { renderSuggestions(data.suggestions || []); })
            .catch(function () { renderSuggestions([]); });
    }

    searchInput.addEventListener('focus', openSuggestions);

    searchInput.addEventListener('input', function () {
        const query = this.value.trim();
        openSuggestions();

        clearTimeout(debounceTimer);

        if (query.length < 2) {
            suggestionsResults.style.display = 'none';
            suggestionsEmpty.style.display = 'block';
            suggestionsEmpty.querySelector('h3').textContent = 'Start typing';
            suggestionsEmpty.querySelector('span').textContent = 'Search for products, brands or categories';
            return;
        }

        debounceTimer = setTimeout(function () {
            fetchSuggestions(query);
        }, 220);
    });

    document.addEventListener('click', function (e) {
        if (!searchInput.contains(e.target) && !searchSuggestions.contains(e.target)) {
            closeSuggestions();
        }
    });

    // Keyboard navigation in suggestions
    searchInput.addEventListener('keydown', function (e) {
        const items = searchSuggestions.querySelectorAll('.suggestion-item[role="option"]');

        if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
            e.preventDefault();
            if (!items.length) return;
            if (activeIndex >= 0 && items[activeIndex]) {
                items[activeIndex].style.background = '';
            }
            activeIndex = e.key === 'ArrowDown'
                ? (activeIndex + 1) % items.length
                : (activeIndex - 1 + items.length) % items.length;
            items[activeIndex].style.background = '#FFF8EC';
            items[activeIndex].focus();
        }

        if (e.key === 'Enter') {
            // If a suggestion is highlighted, go to it; otherwise submit real search
            if (activeIndex >= 0 && items[activeIndex]) {
                e.preventDefault();
                window.location.href = items[activeIndex].href;
            } else if (searchForm) {
                // let the form submit naturally to search_view (GET ?q=...)
                closeSuggestions();
            }
        }

        if (e.key === 'Escape') closeSuggestions();
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

    // ── Header scroll shadow + auto-hide on scroll ────────────
const header = document.querySelector('header');
if (header) {
    let lastScrollY = window.scrollY;
    let headerTicking = false;
    const hideThreshold = 80; // header sirf itna scroll hone ke baad hide hoga

    function handleHeaderScroll() {
        const currentScrollY = window.scrollY;

        // Shadow intensity based on scroll position
        header.style.boxShadow = currentScrollY > 10
            ? '0 4px 30px rgba(0,0,0,0.35)'
            : '0 2px 20px rgba(0,0,0,0.25)';

        if (currentScrollY > lastScrollY && currentScrollY > hideThreshold) {
            // Scrolling down -> hide header
            header.classList.add('header-hidden');
        } else if (currentScrollY < lastScrollY) {
            // Scrolling up -> show header
            header.classList.remove('header-hidden');
        }

        lastScrollY = currentScrollY;
        headerTicking = false;
    }

    window.addEventListener('scroll', function () {
        if (!headerTicking) {
            requestAnimationFrame(handleHeaderScroll);
            headerTicking = true;
        }
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