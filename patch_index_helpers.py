with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Additional helper functions
helper_js = '''
        // ==========================================
        // UI & SEARCH HELPERS
        // ==========================================
        function toggleMobileNav() {
            const nav = document.getElementById('mobile-nav-drawer');
            if (nav) nav.classList.toggle('hidden');
        }

        function handleSearchSubmit(e) {
            if (e) e.preventDefault();
            const inp = document.getElementById('global-search-input');
            const q = inp ? inp.value.trim() : '';
            appState.searchQuery = q;
            closeSearchDropdown();
            navigate('shop');
            fetchProducts();
        }

        function executeSearch() {
            handleSearchSubmit();
        }

        function handleSearchAutocomplete(val) {
            const q = (val || '').trim().toLowerCase();
            const box = document.getElementById('search-suggestions');
            const list = document.getElementById('search-suggestions-list');
            if (!box || !list) return;
            if (q.length < 2) {
                box.classList.add('hidden');
                return;
            }
            const matches = (appState.products || []).filter(p =>
                p.title.toLowerCase().includes(q) ||
                (p.brand && p.brand.toLowerCase().includes(q)) ||
                (p.category && p.category.toLowerCase().includes(q))
            ).slice(0, 6);
            if (matches.length > 0) {
                list.innerHTML = matches.map(m => `
                    <a href="#product/${m.id}" onclick="closeSearchDropdown()" class="flex items-center gap-3 p-2 hover:bg-slate-800/60 rounded-xl transition-all">
                        <img src="${m.images ? m.images[0] : (m.image_url || '')}" class="w-9 h-9 object-cover rounded-lg border border-slate-700 flex-shrink-0" />
                        <div class="min-w-0 flex-1">
                            <div class="font-bold text-xs text-slate-200 truncate">${escapeHtml(m.title)}</div>
                            <div class="text-[10px] text-cyan-400 font-mono font-bold">₹${m.price.toLocaleString('en-IN')}</div>
                        </div>
                    </a>
                `).join('');
                box.classList.remove('hidden');
            } else {
                box.classList.add('hidden');
            }
        }

        function showSearchDropdown() {
            const inp = document.getElementById('global-search-input');
            if (inp && inp.value.trim().length >= 2) {
                handleSearchAutocomplete(inp.value.trim());
            }
        }

        function closeSearchDropdown() {
            const box = document.getElementById('search-suggestions');
            if (box) box.classList.add('hidden');
        }

        function filterAdminProducts(val) {
            const q = (val || '').trim().toLowerCase();
            const rows = document.querySelectorAll('#admin-products-table-body tr');
            rows.forEach(r => {
                const text = r.textContent.toLowerCase();
                r.style.display = text.includes(q) ? '' : 'none';
            });
        }

        function handleImagePreview(event) {
            const file = event.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = function(e) {
                const previewContainer = document.getElementById('image-preview-container');
                if (previewContainer) {
                    previewContainer.innerHTML = `<img src="${e.target.result}" class="w-full h-full object-contain rounded-xl" />`;
                }
                const imgUrlInput = document.getElementById('add-prod-img-url');
                if (imgUrlInput && !imgUrlInput.value) {
                    imgUrlInput.value = e.target.result;
                }
            };
            reader.readAsDataURL(file);
        }

        function toggle360Modal(show, imgUrl) {
            const modal = document.getElementById('modal-360');
            if (!modal) return;
            const isCurrentlyHidden = modal.classList.contains('hidden');
            const shouldShow = (typeof show === 'boolean') ? show : isCurrentlyHidden;
            if (shouldShow) {
                const currentProd = appState.currentDetailProduct;
                const targetImg = imgUrl || (currentProd ? (currentProd.images ? currentProd.images[0] : currentProd.image_url) : '');
                open360Modal(targetImg);
            } else {
                close360Modal();
            }
        }

        function saveRecentlyViewed(product) {
            try {
                let recent = JSON.parse(localStorage.getItem('nvb_recent_products') || '[]');
                recent = recent.filter(item => item.id !== product.id);
                recent.unshift({
                    id: product.id,
                    title: product.title,
                    price: product.price,
                    images: product.images || [product.image_url],
                    rating: product.rating
                });
                if (recent.length > 8) recent = recent.slice(0, 8);
                localStorage.setItem('nvb_recent_products', JSON.stringify(recent));
            } catch (e) {
                console.error('Error saving recently viewed:', e);
            }
        }

        function getRecentlyViewed() {
            try {
                return JSON.parse(localStorage.getItem('nvb_recent_products') || '[]');
            } catch (e) {
                return [];
            }
        }
'''

# Update navigate function
old_nav = '''function navigate(viewName, updateHash = true) {
            appState.currentView = viewName;
            if (updateHash) {
                window.location.hash = viewName;
            }
            document.querySelectorAll('.view-section').forEach(sec => sec.classList.add('hidden'));
            const targetSec = document.getElementById(`view-${viewName}`);
            if (targetSec) {
                targetSec.classList.remove('hidden');
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
            if (viewName === 'shop') renderShop();
            if (viewName === 'cart') renderCartPage();
            if (viewName === 'orders') renderOrdersPage();
            if (viewName === 'wishlist') renderWishlistPage();
            if (viewName === 'deals') renderDealsPage();
            if (viewName === 'compare') renderComparePage();
            if (viewName === 'admin') initAdminDashboard();
            initLucide();
        }'''

new_nav = '''function navigate(viewName, updateHash = true) {
            viewName = (viewName || 'home').replace(/^#+/, '');
            if (viewName.startsWith('product/') || viewName.startsWith('product-')) {
                const pid = viewName.includes('/') ? viewName.split('/')[1] : viewName.replace('product-', '');
                openProductDetail(pid);
                return;
            }
            appState.currentView = viewName;
            if (updateHash) {
                window.location.hash = viewName;
            }
            document.querySelectorAll('.view-section').forEach(sec => sec.classList.add('hidden'));
            const targetSec = document.getElementById(`view-${viewName}`);
            if (targetSec) {
                targetSec.classList.remove('hidden');
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
            if (viewName === 'shop') renderShop();
            if (viewName === 'cart') renderCartPage();
            if (viewName === 'orders') renderOrdersPage();
            if (viewName === 'wishlist') renderWishlistPage();
            if (viewName === 'deals') renderDealsPage();
            if (viewName === 'compare') renderComparePage();
            if (viewName === 'admin') initAdminDashboard();
            initLucide();
        }'''

if old_nav in html:
    html = html.replace(old_nav, new_nav)
    print("Replaced navigate")
else:
    print("Warning: old_nav not found")

# Insert helper_js right before closing </script>
idx_close = html.rfind('</script>')
if idx_close != -1:
    html = html[:idx_close] + helper_js + html[idx_close:]
    print("Inserted helper_js")

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("static/index.html updated successfully!")
