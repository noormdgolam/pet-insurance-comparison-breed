document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle
    const menuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    
    if (menuBtn && navLinks) {
        menuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }

    // Cookie Banner
    const cookieBanner = document.getElementById('cookie-banner');
    const acceptCookiesBtn = document.getElementById('accept-cookies');
    
    if (cookieBanner && acceptCookiesBtn) {
        if (!localStorage.getItem('cookiesAccepted')) {
            setTimeout(() => {
                cookieBanner.classList.add('show');
            }, 1000);
        }
        
        acceptCookiesBtn.addEventListener('click', () => {
            localStorage.setItem('cookiesAccepted', 'true');
            cookieBanner.classList.remove('show');
        });
    }

    // Client-side Search
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    
    if (searchInput && searchResults) {
        let searchIndex = [];
        
        // Fetch search index JSON
        fetch('/search_index.json')
            .then(res => res.json())
            .then(data => {
                searchIndex = data;
                
                // If URL has a 'q' param, pre-fill and search
                const urlParams = new URLSearchParams(window.location.search);
                const q = urlParams.get('q');
                if (q) {
                    searchInput.value = q;
                    performSearch(q);
                }
            })
            .catch(err => console.error("Error loading search index", err));
            
        searchInput.addEventListener('input', (e) => {
            performSearch(e.target.value);
        });
        
        function performSearch(query) {
            query = query.toLowerCase().trim();
            if (query.length < 2) {
                searchResults.innerHTML = '<p style="grid-column: 1 / -1; text-align: center; padding: 2rem;">Please enter at least 2 characters to search.</p>';
                return;
            }
            
            const results = searchIndex.filter(item => 
                item.title.toLowerCase().includes(query) || 
                item.description.toLowerCase().includes(query)
            );
            
            if (results.length === 0) {
                searchResults.innerHTML = '<p style="grid-column: 1 / -1; text-align: center; padding: 2rem;">No results found. Try a different breed.</p>';
                return;
            }
            
            searchResults.innerHTML = results.map(item => `
                <article class="card">
                    <div class="card-content">
                        <span class="category-tag">${item.category}</span>
                        <h3><a href="${item.url}">${item.title}</a></h3>
                        <p>${item.description}</p>
                        <a href="${item.url}" class="read-more">Read Guide &rarr;</a>
                    </div>
                </article>
            `).join('');
        }
    }
});
