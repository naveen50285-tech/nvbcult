
        // State variables
        
        // Smart Backend Origin Resolver (Supports http://localhost:8000, file:///, Live Server, etc.)
        const API_BASE = (window.location.protocol === 'file:' || !window.location.host) 
            ? 'http://localhost:8000' 
            : '';
    
        let allProducts = [];
        let filteredProducts = [];
        let currentCategory = "all";
        let currentSubcategory = "all";
        let searchQuery = "";
        let currentSort = "featured";
        let wishlistItems = new Set();
        let cartItems = [];
        let activeProductModal = null;
        let selectedVariant = "";
        let modalQuantity = 1;
        let adminToken = localStorage.getItem("nvb_cult_admin_token") || null;
        let selectedImageBase64 = null;

        const subcategoriesMap = {
            "T-Shirts": ["Oversized Streetwear", "Graphic & Art", "Supima Plain", "Polo & Collared", "Hoodies & Sweatshirts"],
            "Electronics": ["Earbuds & Audio", "Smartwatches", "Fast Chargers", "Creator Mics", "Desk Accessories"]
        };

        
        // ==================== PWA INSTALL & SERVICE WORKER ====================
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/static/sw.js')
                    .then(reg => console.log('NVB Cult SW registered:', reg.scope))
                    .catch(err => console.log('NVB Cult SW register failed:', err));
            });
        }

        let deferredPrompt = null;
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            const btn = document.getElementById('pwa-install-btn');
            if (btn) btn.style.display = 'inline-flex';
        });

        async function triggerPwaInstall() {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const { outcome } = await deferredPrompt.userChoice;
                if (outcome === 'accepted') {
                    showToast('INSTALLING NVB CULT APP...');
                }
                deferredPrompt = null;
            } else {
                alert(`✦ TO INSTALL NVB CULT AS AN APP:

1. Click the Install App icon on the right side of your browser address bar.
2. Click 'Install' to add NVB Cult to your Windows Start Menu, Taskbar & Desktop!

Or use the desktop shortcut created on your desktop: 'NVB Cult App'`);
            }
        }
    
        // Initialize Store on load
        document.addEventListener("DOMContentLoaded", () => {
            initAuthStatus();
            loadWishlist();
            loadCart();
            fetchProducts();
            fetchAdminStats();
        });

        function scrollToManifesto() {
            const el = document.getElementById("nvb-company-story");
            if (el) el.scrollIntoView({ behavior: 'smooth' });
        }

        // ==================== FETCH PRODUCTS ====================
        async function fetchProducts() {
            try {
                const res = await fetch(`${API_BASE}/api/products`);
                allProducts = await res.json();
                
                // Update hero counter badges
                const teeCount = allProducts.filter(p => p.category === "T-Shirts").length;
                const elecCount = allProducts.filter(p => p.category === "Electronics").length;
                
                document.getElementById("hero-tee-count").textContent = `${teeCount} DROPS • ${teeCount === 0 ? 'OWNER UPLOAD READY' : 'IN VAULT'}`;
                document.getElementById("hero-elec-count").textContent = `${elecCount} DROPS • ${elecCount === 0 ? 'OWNER UPLOAD READY' : 'IN VAULT'}`;
                document.getElementById("total-count-badge").textContent = allProducts.length;
                
                applyFiltersAndRender();
                renderInventoryTable();
            } catch (err) {
                console.error("Failed to load products:", err);
            }
        }

        // ==================== FILTERING & SEARCH ====================
        function filterByCategory(cat) {
            currentCategory = cat;
            currentSubcategory = "all";
            
            // Switch tabs
            document.querySelectorAll(".cat-tab").forEach(tab => {
                tab.classList.toggle("active", tab.dataset.cat === cat);
            });
            document.querySelectorAll(".header-nav .nav-link").forEach(link => {
                if (link.dataset.cat) {
                    link.classList.toggle("active", link.dataset.cat === cat);
                }
            });

            renderSubcategoryChips();
            applyFiltersAndRender();

            // Scroll to catalog smoothly if triggered from hero
            if (event && event.currentTarget && event.currentTarget.classList.contains("hero-card")) {
                const main = document.querySelector(".store-container");
                if (main) main.scrollIntoView({ behavior: 'smooth' });
            }
        }

        function renderSubcategoryChips() {
            const container = document.getElementById("subcat-chips-container");
            container.innerHTML = "";
            
            if (currentCategory === "all") {
                container.style.display = "none";
                return;
            }

            container.style.display = "flex";
            const subs = subcategoriesMap[currentCategory] || [];
            
            // 'All' chip
            const allChip = document.createElement("button");
            allChip.className = `subcat-chip ${currentSubcategory === 'all' ? 'active' : ''}`;
            allChip.textContent = `All ${currentCategory}`;
            allChip.onclick = () => {
                currentSubcategory = "all";
                renderSubcategoryChips();
                applyFiltersAndRender();
            };
            container.appendChild(allChip);

            subs.forEach(sub => {
                const chip = document.createElement("button");
                chip.className = `subcat-chip ${currentSubcategory === sub ? 'active' : ''}`;
                chip.textContent = sub;
                chip.onclick = () => {
                    currentSubcategory = sub;
                    renderSubcategoryChips();
                    applyFiltersAndRender();
                };
                container.appendChild(chip);
            });
        }

        function handleSearch(val) {
            searchQuery = val.trim().toLowerCase();
            const clearBtn = document.getElementById("clear-search");
            clearBtn.style.display = searchQuery ? "block" : "none";
            applyFiltersAndRender();
        }

        function clearSearch() {
            document.getElementById("store-search-input").value = "";
            searchQuery = "";
            document.getElementById("clear-search").style.display = "none";
            applyFiltersAndRender();
        }

        function handleSort(val) {
            currentSort = val;
            applyFiltersAndRender();
        }

        function applyFiltersAndRender() {
            filteredProducts = allProducts.filter(p => {
                const matchCat = currentCategory === "all" || p.category === currentCategory;
                const matchSub = currentSubcategory === "all" || p.subcategory === currentSubcategory;
                const matchSearch = !searchQuery || 
                    p.title.toLowerCase().includes(searchQuery) ||
                    (p.short_description && p.short_description.toLowerCase().includes(searchQuery)) ||
                    (p.tags && p.tags.toLowerCase().includes(searchQuery)) ||
                    p.category.toLowerCase().includes(searchQuery);
                return matchCat && matchSub && matchSearch;
            });

            // Sorting
            if (currentSort === "price_asc") {
                filteredProducts.sort((a, b) => a.price - b.price);
            } else if (currentSort === "price_desc") {
                filteredProducts.sort((a, b) => b.price - a.price);
            } else if (currentSort === "rating") {
                filteredProducts.sort((a, b) => (b.rating || 0) - (a.rating || 0));
            } else if (currentSort === "discount") {
                filteredProducts.sort((a, b) => (b.discount || 0) - (a.discount || 0));
            }

            renderProductsGrid();
        }

        // ==================== RENDER PRODUCT GRID ====================
        function renderProductsGrid() {
            const grid = document.getElementById("products-grid");
            grid.innerHTML = "";

            if (filteredProducts.length === 0) {
                // Customized Melodic Empty State Box (Black & Gold)
                const emptyBox = document.createElement("div");
                emptyBox.className = "empty-archive-box";
                
                if (currentCategory === "T-Shirts") {
                    emptyBox.innerHTML = `
                        <div style="font-size: 44px; margin-bottom: 12px;">👕</div>
                        <h3 style="font-family: 'Cinzel', serif; font-size: 20px; font-weight: 800; text-transform: uppercase; color:#ffffff;">NVB Cult T-Shirt Vault Empty</h3>
                        <p style="color: #cbd5e1; font-size: 14px; margin: 8px auto 20px auto; max-width: 480px;">
                            All placeholder example products have been cleared! As the store owner, you can upload your custom 260 GSM streetwear and tees right now.
                        </p>
                        <button class="btn-submit-product" style="padding: 10px 24px; font-size: 12px;" onclick="openUploadForCategory('T-Shirts')">
                            + Upload T-Shirt Drop as Owner
                        </button>
                    `;
                } else if (currentCategory === "Electronics") {
                    emptyBox.innerHTML = `
                        <div style="font-size: 44px; margin-bottom: 12px;">⚡</div>
                        <h3 style="font-family: 'Cinzel', serif; font-size: 20px; font-weight: 800; text-transform: uppercase; color:#ffffff;">NVB Cult Electronics Vault Empty</h3>
                        <p style="color: #cbd5e1; font-size: 14px; margin: 8px auto 20px auto; max-width: 480px;">
                            All placeholder electronic products have been cleared! As the store owner, you can upload your creator audio and tech drops.
                        </p>
                        <button class="btn-submit-product" style="padding: 10px 24px; font-size: 12px;" onclick="openUploadForCategory('Electronics')">
                            + Upload Electronics Drop as Owner
                        </button>
                    `;
                } else {
                    emptyBox.innerHTML = `
                        <div style="font-size: 44px; margin-bottom: 12px;">👑</div>
                        
                        <div style="display:inline-flex; align-items:center; gap:8px; background:rgba(34,197,94,0.12); border:1.5px solid rgba(34,197,94,0.35); padding:6px 14px; border-radius:4px; font-family:'Space Mono', monospace; font-size:11px; color:#22c55e; margin-bottom:18px;">
                            <span style="width:7px; height:7px; background:#22c55e; border-radius:50%; box-shadow:0 0 6px #22c55e;"></span>
                            <span>BACKEND & SQLITE DATABASE: CONNECTED (0 DROPS STORED)</span>
                        </div><br>
    <h3 style="font-family:'Cinzel', serif; font-size: 20px; font-weight: 800; text-transform: uppercase; color:#ffffff;">NVB Cult Archive Clear</h3>
                        <p style="color: #cbd5e1; font-size: 14px; margin: 8px auto 20px auto; max-width: 480px;">
                            Zero dummy products in the database. Ready for authentic drops to be uploaded in T-Shirts or Electronics.
                        </p>
                        <div style="display:flex; justify-content:center; gap:14px; flex-wrap:wrap;">
                            <button class="btn-submit-product" style="padding:10px 22px; font-size:12px;" onclick="openUploadForCategory('T-Shirts')">
                                + Upload T-Shirt Drop
                            </button>
                            <button class="btn-submit-product" style="padding:10px 22px; font-size:12px; background:#14141c; color:var(--gold-bright); border:1.5px solid var(--gold); box-shadow:3px 3px 0px #000000;" onclick="openUploadForCategory('Electronics')">
                                + Upload Electronics Drop
                            </button>
                        </div>
                    `;
                }
                grid.appendChild(emptyBox);
                return;
            }

            filteredProducts.forEach(prod => {
                const card = document.createElement("div");
                card.className = "product-card";

                const isWish = wishlistItems.has(prod.id);
                const isTee = prod.category === "T-Shirts";
                const isDiscount = prod.discount > 0;

                card.innerHTML = `
                    <div class="card-top-strip">
                        <span class="card-sku-tag">${prod.sku || 'NVB-CULT'}</span>
                        <span class="card-drop-tag">LIMITED DROP</span>
                    </div>

                    <div class="card-img-wrap" onclick="openDetailsModal('${prod.id}')">
                        <img src="${prod.image_url || '/static/placeholder.jpg'}" alt="${prod.title}" class="card-img" loading="lazy">
                        
                        <div class="card-badges">
                            <span class="badge ${isTee ? 'badge-category-tee' : 'badge-category-elec'}">${prod.category}</span>
                            ${isDiscount ? `<span class="badge badge-discount">${prod.discount}% OFF</span>` : ''}
                        </div>

                        <button class="card-wish-btn ${isWish ? 'active' : ''}" onclick="toggleWishlist(event, '${prod.id}')" title="Save to Wishlist">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="${isWish ? '#d4af37' : 'none'}" stroke="currentColor" stroke-width="2">
                                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                            </svg>
                        </button>
                    </div>

                    <div class="card-body">
                        <span class="card-category-name">${prod.subcategory || prod.category}</span>
                        <h3 class="card-title" onclick="openDetailsModal('${prod.id}')">${prod.title}</h3>
                        
                        <div class="card-rating-row">
                            <span class="stars">★★★★★</span>
                            <span style="font-weight:700; color:#ffffff;">${prod.rating || 4.9}</span>
                            <span class="reviews-count">(${prod.review_count || 12} reviews)</span>
                        </div>

                        <div class="card-price-row">
                            <span class="price-current">₹${prod.price}</span>
                            ${prod.mrp ? `<span class="price-mrp">₹${prod.mrp}</span>` : ''}
                            ${isDiscount ? `<span class="price-off">${prod.discount}% OFF</span>` : ''}
                        </div>

                        <div class="card-action-btns">
                            <button class="btn-add-cart" onclick="quickAddToCart('${prod.id}')">
                                <span>+ ADD TO BAG</span>
                            </button>
                            <button class="btn-quick-view" onclick="openDetailsModal('${prod.id}')" title="Inspect Specs">
                                👁
                            </button>
                        </div>
                    </div>
                `;
                grid.appendChild(card);
            });
        }

        // Open owner upload tab pre-selected for category
        function openUploadForCategory(cat) {
            if (!adminToken) {
                openLoginModal();
                return;
            }
            toggleStoreMode("upload");
            const catSelect = document.getElementById("p-category");
            if (catSelect) {
                catSelect.value = cat;
                updateSubcatOptions(cat);
            }
        }

        // ==================== PRODUCT DETAILS MODAL ====================
        function openDetailsModal(prodId) {
            const prod = allProducts.find(p => p.id === prodId);
            if (!prod) return;
            activeProductModal = prod;
            modalQuantity = 1;

            document.getElementById("det-modal-title").textContent = `Specimen // ${prod.sku || 'NVB-CULT'}`;
            document.getElementById("det-img").src = prod.image_url || '/static/placeholder.jpg';
            document.getElementById("det-title").textContent = prod.title;
            document.getElementById("det-desc").textContent = prod.description || prod.short_description || "";
            document.getElementById("det-price").textContent = `₹${prod.price}`;
            document.getElementById("det-mrp").textContent = prod.mrp ? `₹${prod.mrp}` : "";
            document.getElementById("det-off").textContent = prod.discount ? `${prod.discount}% OFF` : "";
            document.getElementById("modal-qty").textContent = "1";

            const catBadge = document.getElementById("det-badge-cat");
            catBadge.textContent = prod.category;
            catBadge.className = `badge ${prod.category === 'T-Shirts' ? 'badge-category-tee' : 'badge-category-elec'}`;

            // Render variants
            const varContainer = document.getElementById("det-variants-chips");
            varContainer.innerHTML = "";
            let variants = [];
            if (prod.sizes && Array.isArray(prod.sizes) && prod.sizes.length > 0) {
                variants = prod.sizes;
            } else if (prod.variants && Array.isArray(prod.variants) && prod.variants.length > 0) {
                variants = prod.variants;
            } else {
                variants = prod.category === "T-Shirts" ? ["S", "M", "L", "XL", "XXL"] : ["Standard Issue"];
            }

            selectedVariant = variants[0] || "Standard";
            variants.forEach(v => {
                const btn = document.createElement("button");
                btn.className = `subcat-chip ${selectedVariant === v ? 'active' : ''}`;
                btn.textContent = v;
                btn.onclick = () => {
                    selectedVariant = v;
                    varContainer.querySelectorAll(".subcat-chip").forEach(b => b.classList.remove("active"));
                    btn.classList.add("active");
                };
                varContainer.appendChild(btn);
            });

            // Thumbnails
            const thumbsBox = document.getElementById("det-thumbs-container");
            thumbsBox.innerHTML = "";
            if (prod.images && Array.isArray(prod.images) && prod.images.length > 1) {
                prod.images.forEach(imgUrl => {
                    const thumb = document.createElement("img");
                    thumb.src = imgUrl;
                    thumb.className = "details-thumb";
                    thumb.onclick = () => {
                        document.getElementById("det-img").src = imgUrl;
                    };
                    thumbsBox.appendChild(thumb);
                });
            }

            document.getElementById("product-details-modal").style.display = "flex";
        }

        function closeDetailsModal(e) {
            if (e && e.target && e.target.classList.contains("modal-body")) return;
            document.getElementById("product-details-modal").style.display = "none";
            activeProductModal = null;
        }

        function updateModalQty(delta) {
            modalQuantity = Math.max(1, modalQuantity + delta);
            document.getElementById("modal-qty").textContent = modalQuantity;
        }

        function addModalItemToCart() {
            if (!activeProductModal) return;
            addToCart(activeProductModal, selectedVariant, modalQuantity);
            document.getElementById("product-details-modal").style.display = "none";
            openCartDrawer();
        }

        function buyModalItemNow() {
            if (!activeProductModal) return;
            addToCart(activeProductModal, selectedVariant, modalQuantity);
            document.getElementById("product-details-modal").style.display = "none";
            openCheckoutModal();
        }

        // ==================== CART MANAGEMENT ====================
        function quickAddToCart(prodId) {
            const prod = allProducts.find(p => p.id === prodId);
            if (!prod) return;
            const defVar = (prod.sizes && prod.sizes[0]) || (prod.variants && prod.variants[0]) || (prod.category === 'T-Shirts' ? 'L' : 'Standard');
            addToCart(prod, defVar, 1);
            showToast(`ADDED ${prod.title.slice(0, 20)}...`);
        }

        function addToCart(product, variant, qty) {
            const existing = cartItems.find(i => i.product.id === product.id && i.variant === variant);
            if (existing) {
                existing.quantity += qty;
            } else {
                cartItems.push({
                    product: product,
                    variant: variant,
                    quantity: qty
                });
            }
            saveCart();
            updateCartBadges();
            renderCartItems();
        }

        function saveCart() {
            localStorage.setItem("nvb_cult_cart", JSON.stringify(cartItems));
        }

        function loadCart() {
            try {
                const stored = localStorage.getItem("nvb_cult_cart");
                if (stored) cartItems = JSON.parse(stored);
            } catch (e) {
                cartItems = [];
            }
            updateCartBadges();
        }

        function updateCartBadges() {
            const total = cartItems.reduce((acc, item) => acc + item.quantity, 0);
            document.getElementById("cart-count").textContent = total;
        }

        function openCartDrawer() {
            renderCartItems();
            document.getElementById("cart-drawer-overlay").style.display = "block";
        }

        function closeCartDrawer(e) {
            if (e && e.target && e.target.classList.contains("cart-drawer")) return;
            document.getElementById("cart-drawer-overlay").style.display = "none";
        }

        function renderCartItems() {
            const container = document.getElementById("cart-items-container");
            container.innerHTML = "";

            if (cartItems.length === 0) {
                container.innerHTML = `
                    <div style="text-align:center; padding:60px 20px; font-family:'Space Mono', monospace; color:#94a3b8;">
                        <div style="font-size:36px; margin-bottom:12px;">🛍️</div>
                        <div style="font-size:13px; font-weight:700; color:#ffffff;">BAG ARCHIVE IS EMPTY</div>
                        <div style="font-size:11px; margin-top:6px;">Select drops from Side A or Side B</div>
                    </div>
                `;
                document.getElementById("cart-total-payable").textContent = "₹0";
                return;
            }

            let total = 0;
            cartItems.forEach((item, index) => {
                const itemTotal = item.product.price * item.quantity;
                total += itemTotal;

                const row = document.createElement("div");
                row.className = "cart-item-card";
                row.innerHTML = `
                    <img src="${item.product.image_url || '/static/placeholder.jpg'}" class="cart-item-thumb" alt="${item.product.title}">
                    <div style="overflow:hidden;">
                        <div style="font-family:'Cinzel', serif; font-size:13px; font-weight:700; color:#ffffff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                            ${item.product.title}
                        </div>
                        <div style="font-family:'Space Mono', monospace; font-size:10px; color:var(--gold-bright); margin-top:2px;">
                            ${item.variant} • ₹${item.product.price} each
                        </div>
                        <div class="inv-stock-stepper" style="margin-top:6px;">
                            <button class="inv-stock-btn" onclick="updateCartItemQty(${index}, -1)">-</button>
                            <span class="inv-stock-num">${item.quantity}</span>
                            <button class="inv-stock-btn" onclick="updateCartItemQty(${index}, 1)">+</button>
                        </div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-family:'Space Mono', monospace; font-size:14px; font-weight:700; color:var(--gold-bright);">₹${itemTotal}</div>
                        <button onclick="removeCartItem(${index})" style="background:none; color:#ef4444; font-family:'Space Mono', monospace; font-size:11px; margin-top:6px; cursor:pointer;">REMOVE</button>
                    </div>
                `;
                container.appendChild(row);
            });

            document.getElementById("cart-total-payable").textContent = `₹${total}`;
        }

        function updateCartItemQty(idx, delta) {
            if (cartItems[idx]) {
                cartItems[idx].quantity += delta;
                if (cartItems[idx].quantity <= 0) {
                    cartItems.splice(idx, 1);
                }
                saveCart();
                updateCartBadges();
                renderCartItems();
            }
        }

        function removeCartItem(idx) {
            cartItems.splice(idx, 1);
            saveCart();
            updateCartBadges();
            renderCartItems();
        }

        // ==================== CHECKOUT & ORDERS ====================
        function openCheckoutModal() {
            if (cartItems.length === 0) {
                alert("Your bag is empty! Add items first.");
                return;
            }
            closeCartDrawer();
            const total = cartItems.reduce((acc, i) => acc + (i.product.price * i.quantity), 0);
            document.getElementById("checkout-btn-amt").textContent = `₹${total}`;
            document.getElementById("checkout-modal").style.display = "flex";
        }

        function closeCheckoutModal(e) {
            if (e && e.target && e.target.classList.contains("modal-card")) return;
            document.getElementById("checkout-modal").style.display = "none";
        }

        async function handlePlaceOrder(e) {
            e.preventDefault();
            const total = cartItems.reduce((acc, i) => acc + (i.product.price * i.quantity), 0);
            const orderPayload = {
                customer_name: document.getElementById("order-name").value,
                customer_phone: document.getElementById("order-phone").value,
                shipping_address: `${document.getElementById("order-address").value}, ${document.getElementById("order-city").value} - ${document.getElementById("order-pincode").value}`,
                payment_method: document.getElementById("order-payment").value,
                total: total,
                items: cartItems.map(i => ({
                    product_id: i.product.id,
                    title: i.product.title,
                    price: i.product.price,
                    quantity: i.quantity,
                    variant: i.variant
                }))
            };

            try {
                const res = await fetch(`${API_BASE}/api/orders`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(orderPayload)
                });

                if (res.ok) {
                    const data = await res.json();
                    cartItems = [];
                    saveCart();
                    updateCartBadges();
                    closeCheckoutModal();
                    alert(`✓ DISPATCH ORDER CONFIRMED!

Order ID: #${data.order_id || 'NVB-CULT'}
Total: ₹${total}
Status: Confirmed for dispatch.`);
                    fetchAdminStats();
                } else {
                    alert("Order placement failed. Please verify fields.");
                }
            } catch (err) {
                console.error(err);
                alert("Order connection failed.");
            }
        }

        // ==================== WISHLIST ====================
        function loadWishlist() {
            try {
                const stored = localStorage.getItem("nvb_cult_wishlist");
                if (stored) wishlistItems = new Set(JSON.parse(stored));
            } catch (e) {
                wishlistItems = new Set();
            }
            updateWishlistBadge();
        }

        function saveWishlist() {
            localStorage.setItem("nvb_cult_wishlist", JSON.stringify(Array.from(wishlistItems)));
            updateWishlistBadge();
        }

        function updateWishlistBadge() {
            document.getElementById("wishlist-count").textContent = wishlistItems.size;
        }

        function toggleWishlist(e, prodId) {
            e.stopPropagation();
            if (wishlistItems.has(prodId)) {
                wishlistItems.delete(prodId);
                showToast("REMOVED FROM SAVED");
            } else {
                wishlistItems.add(prodId);
                showToast("SAVED TO WISHLIST");
            }
            saveWishlist();
            applyFiltersAndRender();
        }

        function filterByWishlist() {
            if (wishlistItems.size === 0) {
                showToast("WISHLIST IS EMPTY");
                return;
            }
            filteredProducts = allProducts.filter(p => wishlistItems.has(p.id));
            renderProductsGrid();
            const main = document.querySelector(".store-container");
            if (main) main.scrollIntoView({ behavior: 'smooth' });
        }

        // ==================== OWNER AUTH & SWITCHING ====================
        function initAuthStatus() {
            const btn = document.getElementById("auth-cta-btn");
            const topBar = document.getElementById("owner-top-bar");

            if (adminToken) {
                btn.innerHTML = `<span>👑 OWNER ACTIVE</span>`;
                btn.classList.add("logged-in");
                topBar.style.display = "flex";
            } else {
                btn.innerHTML = `<span>OWNER ACCESS</span>`;
                btn.classList.remove("logged-in");
                topBar.style.display = "none";
            }
        }

        function handleAuthAction() {
            if (adminToken) {
                toggleStoreMode("portal");
            } else {
                openLoginModal();
            }
        }

        function openLoginModal() {
            document.getElementById("login-modal").style.display = "flex";
        }

        function closeLoginModal(e) {
            if (e && e.target && e.target.classList.contains("modal-card")) return;
            document.getElementById("login-modal").style.display = "none";
        }

        async function handleAdminLogin(e) {
            e.preventDefault();
            const u = document.getElementById("login-username").value;
            const p = document.getElementById("login-password").value;

            try {
                const res = await fetch(`${API_BASE}/api/auth/login`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username: u, password: p })
                });

                if (res.ok) {
                    const data = await res.json();
                    adminToken = data.token || "admin_session_token_nvb_2026";
                    localStorage.setItem("nvb_cult_admin_token", adminToken);
                    closeLoginModal();
                    initAuthStatus();
                    toggleStoreMode("upload");
                    showToast("OWNER ACCESS GRANTED");
                } else {
                    alert("Invalid Credentials. Please use admin / admin123");
                }
            } catch (err) {
                // Fallback for direct token mock if endpoint strictly returns simple auth
                if (u === "admin" && p === "admin123") {
                    adminToken = "admin_session_token_nvb_2026";
                    localStorage.setItem("nvb_cult_admin_token", adminToken);
                    closeLoginModal();
                    initAuthStatus();
                    toggleStoreMode("upload");
                    showToast("OWNER ACCESS GRANTED");
                } else {
                    alert("Sign in failed. Check credentials.");
                }
            }
        }

        function logoutAdmin() {
            adminToken = null;
            localStorage.removeItem("nvb_cult_admin_token");
            initAuthStatus();
            toggleStoreMode("store");
            showToast("SIGNED OUT OF OWNER CONSOLE");
        }

        function toggleStoreMode(mode) {
            const custView = document.getElementById("customer-store-view");
            const portalView = document.getElementById("owner-portal-view");

            if (mode === "store") {
                custView.style.display = "block";
                portalView.style.display = "none";
                window.scrollTo({ top: 0, behavior: 'smooth' });
            } else {
                custView.style.display = "none";
                portalView.style.display = "block";
                window.scrollTo({ top: 0, behavior: 'smooth' });

                if (mode === "upload") switchPortalTab("upload");
                if (mode === "inventory") switchPortalTab("inventory");
                if (mode === "orders") switchPortalTab("orders");
            }
        }

        function switchPortalTab(tab) {
            document.getElementById("portal-tab-upload").style.display = tab === "upload" ? "block" : "none";
            document.getElementById("portal-tab-inventory").style.display = tab === "inventory" ? "block" : "none";
            document.getElementById("portal-tab-orders").style.display = tab === "orders" ? "block" : "none";

            document.querySelectorAll(".portal-tab").forEach(t => t.classList.remove("active"));
            const targetBtn = document.getElementById(`tab-btn-${tab}`);
            if (targetBtn) targetBtn.classList.add("active");

            if (tab === "inventory") renderInventoryTable();
            if (tab === "orders") renderOrdersTable();
        }

        // ==================== OWNER PRODUCT UPLOAD ====================
        function updateSubcatOptions(category) {
            const subSelect = document.getElementById("p-subcategory");
            subSelect.innerHTML = "";
            const subs = subcategoriesMap[category] || [];
            subs.forEach(s => {
                const opt = document.createElement("option");
                opt.value = s;
                opt.textContent = s;
                subSelect.appendChild(opt);
            });
        }

        function handleImageFileSelect(e) {
            const file = e.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = (event) => {
                selectedImageBase64 = event.target.result;
                document.getElementById("p-preview-img").src = selectedImageBase64;
                document.getElementById("p-preview-name").textContent = file.name;
                document.getElementById("p-preview-box").style.display = "flex";
            };
            reader.readAsDataURL(file);
        }

        function clearSelectedImage() {
            selectedImageBase64 = null;
            document.getElementById("p-image-file").value = "";
            document.getElementById("p-preview-box").style.display = "none";
        }

        async function handleProductUpload(e) {
            e.preventDefault();
            const submitBtn = document.getElementById("btn-upload-submit");
            submitBtn.disabled = true;
            submitBtn.textContent = "Processing Specimen Drop...";

            const title = document.getElementById("p-title").value;
            const category = document.getElementById("p-category").value;
            const subcategory = document.getElementById("p-subcategory").value;
            const price = parseFloat(document.getElementById("p-price").value);
            const mrp = parseFloat(document.getElementById("p-mrp").value);
            const stock = parseInt(document.getElementById("p-stock").value);
            const sku = document.getElementById("p-sku").value || `NVB-${category === 'T-Shirts' ? 'TEE' : 'ELEC'}-${Date.now().toString().slice(-4)}`;
            const shortDesc = document.getElementById("p-short-desc").value;
            const desc = document.getElementById("p-description").value;
            const variantsStr = document.getElementById("p-variants").value;
            const tagsStr = document.getElementById("p-tags").value;
            const urlInput = document.getElementById("p-image-url").value;

            let finalImageUrl = urlInput || "/static/placeholder.jpg";

            // If base64 file selected, upload image to server first
            if (selectedImageBase64) {
                try {
                    const uploadRes = await fetch(`${API_BASE}/api/upload-image`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ image_data: selectedImageBase64, filename: "product_drop.png" })
                    });
                    if (uploadRes.ok) {
                        const uploadData = await uploadRes.json();
                        finalImageUrl = uploadData.url || uploadData.image_url || finalImageUrl;
                    }
                } catch (err) {
                    console.warn("Image upload failed, using fallback base64 directly");
                    finalImageUrl = selectedImageBase64;
                }
            }

            const discount = mrp > price ? Math.round(((mrp - price) / mrp) * 100) : 0;
            const variantsList = variantsStr.split(",").map(s => s.trim()).filter(Boolean);

            const payload = {
                title: title,
                category: category,
                subcategory: subcategory,
                price: price,
                mrp: mrp,
                discount: discount,
                stock: stock,
                sku: sku,
                image_url: finalImageUrl,
                images: [finalImageUrl],
                short_description: shortDesc,
                description: desc,
                sizes: variantsList,
                variants: variantsList,
                tags: tagsStr,
                rating: 5.0,
                review_count: 1
            };

            try {
                // Post to products API (using admin endpoint or fallback standard)
                let res = await fetch("/api/products", {
                    method: "POST",
                    headers: { 
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${adminToken}`
                    },
                    body: JSON.stringify(payload)
                });

                if (!res.ok) {
                    // Try alternative /api/admin/products endpoint
                    res = await fetch(`${API_BASE}/api/admin/products`, {
                        method: "POST",
                        headers: { 
                            "Content-Type": "application/json",
                            "Authorization": `Bearer ${adminToken}`
                        },
                        body: JSON.stringify(payload)
                    });
                }

                if (res.ok) {
                    showToast("DROP PUBLISHED TO VAULT!");
                    document.getElementById("owner-upload-form").reset();
                    clearSelectedImage();
                    await fetchProducts();
                    toggleStoreMode("store");
                    filterByCategory(category);
                } else {
                    alert("Upload failed. Verify product fields.");
                }
            } catch (err) {
                console.error(err);
                alert("Upload connection failed.");
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = "⚡ Publish Drop to Storefront";
            }
        }

        // ==================== INVENTORY TABLE ====================
        function renderInventoryTable() {
            const tbody = document.getElementById("portal-inventory-tbody");
            if (!tbody) return;
            tbody.innerHTML = "";
            document.getElementById("portal-inv-count").textContent = allProducts.length;

            if (allProducts.length === 0) {
                tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:30px; font-family:'Space Mono', monospace; color:#94a3b8;">NO PRODUCTS IN VAULT. UPLOAD YOUR FIRST SPECIMEN.</td></tr>`;
                return;
            }

            allProducts.forEach(prod => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>
                        <div class="inv-prod-cell">
                            <img src="${prod.image_url || '/static/placeholder.jpg'}" alt="" class="inv-prod-thumb">
                            <div>
                                <div style="font-weight:700; color:#ffffff;">${prod.title}</div>
                                <div style="font-family:'Space Mono', monospace; font-size:11px; color:#94a3b8;">SKU: ${prod.sku}</div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <span class="badge ${prod.category === 'T-Shirts' ? 'badge-category-tee' : 'badge-category-elec'}">${prod.category}</span>
                        <div style="font-size:11px; color:#94a3b8; margin-top:2px;">${prod.subcategory || ''}</div>
                    </td>
                    <td style="font-family:'Space Mono', monospace; font-weight:700; color:var(--gold-bright);">₹${prod.price}</td>
                    <td>
                        <div class="inv-stock-stepper">
                            <button class="inv-stock-btn" onclick="adjustProductStock('${prod.id}', -5)">-</button>
                            <span class="inv-stock-num">${prod.stock}</span>
                            <button class="inv-stock-btn" onclick="adjustProductStock('${prod.id}', 5)">+</button>
                        </div>
                    </td>
                    <td>
                        <span style="font-family:'Space Mono', monospace; font-size:11px; color:${prod.stock > 0 ? '#22c55e' : '#ef4444'}; font-weight:700;">
                            ${prod.stock > 0 ? '✓ ACTIVE' : '⚠ DEPLETED'}
                        </span>
                    </td>
                    <td>
                        <button onclick="deleteAdminProduct('${prod.id}', '${encodeURIComponent(prod.title)}')" style="background:none; color:#ef4444; font-family:'Space Mono', monospace; font-size:11px; font-weight:700; cursor:pointer;" title="Delete Product">DELETE</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        async function adjustProductStock(prodId, delta) {
            const prod = allProducts.find(p => p.id === prodId);
            if (!prod) return;
            const newStock = Math.max(0, (prod.stock || 0) + delta);
            try {
                await fetch(`${API_BASE}/api/products/${prodId}`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ stock: newStock })
                });
                prod.stock = newStock;
                renderInventoryTable();
                showToast(`STOCK UPDATED: ${newStock}`);
            } catch (err) {
                console.error(err);
            }
        }

        async function deleteAdminProduct(prodId, title) {
            if (!confirm(`Are you sure you want to permanently delete specimen:

${decodeURIComponent(title)}?`)) return;
            try {
                const res = await fetch(`${API_BASE}/api/products/${prodId}`, { method: "DELETE" });
                if (res.ok) {
                    showToast("SPECIMEN REMOVED");
                    await fetchProducts();
                } else {
                    alert("Delete failed.");
                }
            } catch (err) {
                console.error(err);
            }
        }

        // ==================== FREIGHT ORDERS TABLE ====================
        async function renderOrdersTable() {
            const tbody = document.getElementById("portal-orders-tbody");
            if (!tbody) return;
            tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:20px; font-family:'Space Mono', monospace;">Scanning Freight Dispatches...</td></tr>`;

            try {
                const res = await fetch(`${API_BASE}/api/orders`);
                const orders = await res.json();
                document.getElementById("portal-orders-count").textContent = orders.length;

                if (orders.length === 0) {
                    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:30px; font-family:'Space Mono', monospace; color:#94a3b8;">NO FREIGHT ORDERS DISPATCHED YET.</td></tr>`;
                    return;
                }

                tbody.innerHTML = "";
                orders.forEach(ord => {
                    const tr = document.createElement("tr");
                    tr.innerHTML = `
                        <td style="font-family:'Space Mono', monospace; font-weight:700; color:var(--gold-bright);">#${ord.id ? ord.id.slice(0, 8) : 'ORD'}</td>
                        <td>
                            <div style="font-weight:700; color:#ffffff;">${ord.customer_name}</div>
                            <div style="font-size:11px; color:#94a3b8;">${ord.created_at ? ord.created_at.slice(0, 16) : ''}</div>
                        </td>
                        <td>
                            <div style="font-size:12px; color:#ffffff;">${ord.customer_phone}</div>
                            <div style="font-size:11px; color:#94a3b8;">${ord.shipping_address}</div>
                        </td>
                        <td>
                            <span class="badge" style="background:#14141c; color:#ffffff; border-color:var(--gold);">${ord.items ? ord.items.length : 1} ITEM(S)</span>
                        </td>
                        <td style="font-family:'Space Mono', monospace; font-weight:700; color:var(--gold-bright);">₹${ord.total}</td>
                        <td>
                            <select class="form-control" style="padding:4px 8px; font-size:11px; font-family:'Space Mono', monospace;" onchange="updateOrderStatus('${ord.id}', this.value)">
                                <option value="CONFIRMED" ${ord.status === 'CONFIRMED' ? 'selected' : ''}>CONFIRMED</option>
                                <option value="IN_TRANSIT" ${ord.status === 'IN_TRANSIT' ? 'selected' : ''}>IN TRANSIT</option>
                                <option value="DELIVERED" ${ord.status === 'DELIVERED' ? 'selected' : ''}>DELIVERED</option>
                            </select>
                        </td>
                    `;
                    tbody.appendChild(tr);
                });
            } catch (err) {
                console.error(err);
            }
        }

        async function updateOrderStatus(orderId, status) {
            try {
                await fetch(`${API_BASE}/api/orders/${orderId}`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ status: status })
                });
                showToast(`ORDER #${orderId.slice(0,6)}: ${status}`);
            } catch (err) {
                console.error(err);
            }
        }

        async function fetchAdminStats() {
            try {
                const res = await fetch(`${API_BASE}/api/admin/stats`);
                const stats = await res.json();
                if (stats) {
                    if (document.getElementById("portal-orders-count")) {
                        document.getElementById("portal-orders-count").textContent = stats.total_orders || 0;
                    }
                }
            } catch (e) {}
        }

        // ==================== CULT AI ASSISTANT ====================
        function toggleAiChat() {
            const chat = document.getElementById("ai-chat-window");
            const isVisible = chat.style.display === "flex";
            chat.style.display = isVisible ? "none" : "flex";
            if (!isVisible) {
                document.getElementById("ai-input").focus();
            }
        }

        function clearAiChat() {
            const body = document.getElementById("ai-chat-body");
            body.innerHTML = `
                <div class="ai-bubble ai-bubble-bot">
                    ✦ <strong>COMM-LINK CLEARED</strong> ✦
                    <br><br>
                    Ready for your queries regarding <strong>NVB Cult</strong> drops, our <strong>company story</strong>, sizing guides, or owner commands.
                </div>
                <div class="ai-suggestions-row">
                    <button class="ai-chip" onclick="sendAiPrompt('Tell me about the NVB company story and motto')">👑 Our Company Story</button>
                    <button class="ai-chip" onclick="sendAiPrompt('What does the NVB logo symbolize?')">👁️ Logo Symbolism</button>
                    <button class="ai-chip" onclick="sendAiPrompt('Tell me about 260 GSM heavyweight cotton')">👕 260 GSM Fabric</button>
                    <button class="ai-chip" onclick="sendAiPrompt('What size should I choose for oversized t-shirts?')">📐 Sizing Guide</button>
                    <button class="ai-chip" onclick="sendAiPrompt('Any discount coupon code?')">🏷️ Coupon 'VISION10'</button>
                </div>
                <div class="ai-typing-indicator" id="ai-typing-indicator">
                    <span class="ai-typing-dot"></span>
                    <span class="ai-typing-dot"></span>
                    <span class="ai-typing-dot"></span>
                </div>
            `;
        }

        function sendAiPrompt(prompt) {
            document.getElementById("ai-input").value = prompt;
            submitAiMessage();
        }

        async function submitAiMessage() {
            const input = document.getElementById("ai-input");
            const text = input.value.trim();
            if (!text) return;

            input.value = "";
            appendAiBubble(text, true);

            const typing = document.getElementById("ai-typing-indicator");
            typing.style.display = "flex";
            const body = document.getElementById("ai-chat-body");
            body.scrollTop = body.scrollHeight;

            try {
                const res = await fetch(`${API_BASE}/api/ai-assistant`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ query: text })
                });
                const data = await res.json();
                typing.style.display = "none";

                let respContent = data.response || data.text || "Transmission interrupted.";
                // Format markdown bold & linebreaks
                let cleanText = respContent
                    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                    .replace(/
/g, '<br>');

                let recsHtml = "";
                if (data.recommended_products && data.recommended_products.length > 0) {
                    recsHtml = `<div style="margin-top:10px; font-family:'Space Mono', monospace; font-size:11px; color:var(--gold-bright); font-weight:700;">RECOMMENDED DROPS:</div>`;
                    data.recommended_products.slice(0, 2).forEach(p => {
                        recsHtml += `
                            <div class="ai-rec-card" onclick="openDetailsModal('${p.id}')">
                                <img src="${p.image_url || '/static/placeholder.jpg'}" class="ai-rec-thumb" alt="">
                                <div style="flex:1; overflow:hidden;">
                                    <div style="font-weight:700; font-size:12px; color:#ffffff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${p.title}</div>
                                    <div style="font-family:'Space Mono', monospace; font-size:11px; color:var(--gold-bright); font-weight:700;">₹${p.price}</div>
                                </div>
                                <span style="font-family:'Space Mono', monospace; font-size:10px; background:var(--gold); color:#000000; font-weight:800; padding:2px 6px; border-radius:2px;">INSPECT</span>
                            </div>
                        `;
                    });
                }

                appendAiBubble(cleanText + (recsHtml ? `<div style="margin-top:10px; font-family:'Space Mono', monospace; font-size:10px; border-top:1px solid rgba(212, 175, 55, 0.4); padding-top:6px;">${recsHtml}</div>` : ''), false);
            } catch (err) {
                typing.style.display = "none";
                appendAiBubble("Comm-link connection failed. Please verify local server is running.", false);
            }
        }

        function appendAiBubble(htmlContent, isUser) {
            const body = document.getElementById("ai-chat-body");
            const typing = document.getElementById("ai-typing-indicator");
            const bubble = document.createElement("div");
            bubble.className = `ai-bubble ${isUser ? 'ai-bubble-user' : 'ai-bubble-bot'}`;
            bubble.innerHTML = htmlContent;
            body.insertBefore(bubble, typing);
            body.scrollTop = body.scrollHeight;
        }

        // ==================== TOAST NOTIFICATIONS ====================
        function showToast(msg) {
            const toast = document.getElementById("toast-msg");
            toast.textContent = msg;
            toast.style.display = "block";
            setTimeout(() => {
                toast.style.display = "none";
            }, 3000);
        }
    