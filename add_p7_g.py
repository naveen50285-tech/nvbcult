import sys

code_part7g = r'''
        // ==========================================
        // DEALS & FLASH SALE TIMER
        // ==========================================
        let flashSaleSeconds = 14 * 3600 + 42 * 60 + 19; // ~14h 42m

        function startFlashSaleTimer() {
            setInterval(() => {
                if (flashSaleSeconds > 0) flashSaleSeconds--;
                const h = Math.floor(flashSaleSeconds / 3600);
                const m = Math.floor((flashSaleSeconds % 3600) / 60);
                const s = flashSaleSeconds % 60;
                
                const pad = (n) => String(n).padStart(2, '0');
                const th = document.getElementById('timer-hours');
                const tm = document.getElementById('timer-minutes');
                const ts = document.getElementById('timer-seconds');
                if (th) th.textContent = pad(h);
                if (tm) tm.textContent = pad(m);
                if (ts) ts.textContent = pad(s);

                const dt = document.getElementById('deals-page-timer');
                if (dt) dt.textContent = `${pad(h)}h : ${pad(m)}m : ${pad(s)}s`;
            }, 1000);
        }

        async function renderDealsPage() {
            const container = document.getElementById('all-deals-grid');
            if (!container) return;
            container.innerHTML = '<div class="col-span-full py-12 text-center"><i data-lucide="loader-2" class="w-8 h-8 animate-spin mx-auto text-primary"></i></div>';
            initLucide();
            try {
                const res = await fetch('/api/products?limit=24');
                const data = await res.json();
                const deals = (data.products || []).filter(p => p.is_flash_sale || p.deal_of_the_day || p.discount_percent >= 15);
                if (deals.length === 0) {
                    container.innerHTML = '<div class="col-span-full text-center py-12 text-slate-400">No active promotional deals right now. Check back soon!</div>';
                    return;
                }
                container.innerHTML = deals.map(p => renderProductCard(p)).join('');
                initLucide();
            } catch (e) {
                console.error(e);
            }
        }

        // ==========================================
        // HERO CAROUSEL SWITCHER
        // ==========================================
        let currentSlide = 0;
        const totalSlides = 2;

        function switchHeroSlide(idx) {
            currentSlide = idx;
            const slide1 = document.getElementById('hero-slide-1');
            const slide2 = document.getElementById('hero-slide-2');
            const dot0 = document.getElementById('hero-dot-0');
            const dot1 = document.getElementById('hero-dot-1');

            if (slide1 && slide2) {
                if (idx === 0) {
                    slide1.classList.remove('opacity-0', 'pointer-events-none');
                    slide1.classList.add('opacity-100');
                    slide2.classList.remove('opacity-100');
                    slide2.classList.add('opacity-0', 'pointer-events-none');
                } else {
                    slide2.classList.remove('opacity-0', 'pointer-events-none');
                    slide2.classList.add('opacity-100');
                    slide1.classList.remove('opacity-100');
                    slide1.classList.add('opacity-0', 'pointer-events-none');
                }
            }
            if (dot0 && dot1) {
                if (idx === 0) {
                    dot0.className = "w-8 h-2 rounded-full bg-cyan-400 transition-all";
                    dot1.className = "w-2.5 h-2 rounded-full bg-white/30 hover:bg-white/60 transition-all";
                } else {
                    dot0.className = "w-2.5 h-2 rounded-full bg-white/30 hover:bg-white/60 transition-all";
                    dot1.className = "w-8 h-2 rounded-full bg-cyan-400 transition-all";
                }
            }
        }

        setInterval(() => {
            currentSlide = (currentSlide + 1) % totalSlides;
            switchHeroSlide(currentSlide);
        }, 6000);

        // ==========================================
        // PIN CODE & LOCATION MODAL
        // ==========================================
        function openLocationModal() {
            document.getElementById('modal-location').classList.remove('hidden');
        }

        function closeLocationModal() {
            document.getElementById('modal-location').classList.add('hidden');
        }

        async function submitPincodeModal() {
            const input = document.getElementById('modal-pin-input');
            const msgEl = document.getElementById('modal-pin-result');
            const pin = input.value.trim();
            if (!/^\d{6}$/.test(pin)) {
                msgEl.innerHTML = '<span class="text-rose-400 text-xs font-semibold">Please enter a valid 6-digit Indian PIN code.</span>';
                return;
            }
            msgEl.innerHTML = '<span class="text-cyan-400 text-xs font-semibold">Checking delivery availability...</span>';
            try {
                const res = await fetch(`/api/delivery-check?pincode=${pin}`);
                const data = await res.json();
                if (data.available) {
                    appState.userPincode = pin;
                    localStorage.setItem('nvb_pincode', pin);
                    localStorage.setItem('nvb_city', data.city);
                    updateLocationDisplay(pin, data.city);
                    msgEl.innerHTML = `<span class="text-emerald-400 text-xs font-semibold">✓ Delivering to ${data.city} (${data.estimated_days} days). Free shipping available!</span>`;
                    setTimeout(() => {
                        closeLocationModal();
                    }, 1200);
                } else {
                    msgEl.innerHTML = `<span class="text-rose-400 text-xs font-semibold">${data.message || 'Delivery not available to this PIN.'}</span>`;
                }
            } catch (e) {
                msgEl.innerHTML = '<span class="text-rose-400 text-xs font-semibold">Failed to verify PIN code.</span>';
            }
        }

        function updateLocationDisplay(pin, city) {
            const headerDisp = document.getElementById('header-location-display');
            const topDisp = document.getElementById('top-pin-display');
            if (headerDisp) headerDisp.textContent = `${city || 'Deliver to'} ${pin}`;
            if (topDisp) topDisp.textContent = pin;
        }

        // ==========================================
        // 360 INTERACTIVE VIEWER MODAL
        // ==========================================
        let current360Angle = 0;
        let isDragging360 = false;
        let startX360 = 0;

        function open360Modal(imgUrl) {
            const modal = document.getElementById('modal-360');
            const img = document.getElementById('viewer-360-img');
            if (img && imgUrl) {
                img.src = imgUrl;
            }
            current360Angle = 0;
            rotate360(0);
            modal.classList.remove('hidden');
        }

        function close360Modal() {
            document.getElementById('modal-360').classList.add('hidden');
        }

        function rotate360(val) {
            current360Angle = parseInt(val) || 0;
            const img = document.getElementById('viewer-360-img');
            if (img) {
                const normAngle = ((current360Angle % 360) + 360) % 360;
                img.style.transform = `perspective(800px) rotateY(${normAngle}deg) scale(${1 + 0.08 * Math.abs(Math.sin((normAngle * Math.PI) / 180))})`;
            }
        }

        // Mouse drag support for 360 viewer
        const viewerCanvas = document.getElementById('viewer-360-canvas');
        if (viewerCanvas) {
            viewerCanvas.addEventListener('mousedown', (e) => {
                isDragging360 = true;
                startX360 = e.clientX;
            });
            window.addEventListener('mouseup', () => { isDragging360 = false; });
            window.addEventListener('mousemove', (e) => {
                if (!isDragging360) return;
                const delta = e.clientX - startX360;
                startX360 = e.clientX;
                current360Angle = (current360Angle + delta * 1.5) % 360;
                rotate360(current360Angle);
            });
        }

        // ==========================================
        // REVIEWS & RATINGS SUBMISSION
        // ==========================================
        let selectedReviewRating = 5;

        function openWriteReviewModal(productId, productName) {
            document.getElementById('review-product-id').value = productId;
            const titleEl = document.getElementById('modal-review-title');
            if (titleEl) titleEl.textContent = `Review: ${productName || 'Product'}`;
            setReviewRating(5);
            document.getElementById('modal-review').classList.remove('hidden');
        }

        function closeWriteReviewModal() {
            document.getElementById('modal-review').classList.add('hidden');
        }

        function setReviewRating(rating) {
            selectedReviewRating = rating;
            const stars = document.querySelectorAll('#review-stars-selector button');
            stars.forEach((btn, idx) => {
                if (idx < rating) {
                    btn.classList.add('text-amber-400');
                    btn.classList.remove('text-slate-300');
                } else {
                    btn.classList.remove('text-amber-400');
                    btn.classList.add('text-slate-300');
                }
            });
        }

        async function submitReview(event) {
            if (event) event.preventDefault();
            const prodId = document.getElementById('review-product-id').value;
            const title = document.getElementById('review-title').value.trim();
            const comment = document.getElementById('review-comment').value.trim();
            if (!comment) {
                showToast('Please enter your review comments.', 'error');
                return;
            }
            try {
                const res = await fetch(`/api/products/${prodId}/reviews`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        rating: selectedReviewRating,
                        title: title || 'Great product!',
                        comment: comment,
                        author: 'Verified Customer',
                        verified_purchase: true
                    })
                });
                const data = await res.json();
                if (res.ok) {
                    showToast('Review submitted successfully!', 'success');
                    closeWriteReviewModal();
                    document.getElementById('review-title').value = '';
                    document.getElementById('review-comment').value = '';
                    if (location.hash.startsWith('#product-')) {
                        renderProductDetail(prodId);
                    }
                } else {
                    showToast(data.detail || 'Failed to submit review.', 'error');
                }
            } catch (e) {
                showToast('Network error while posting review.', 'error');
            }
        }

        function voteHelpful(reviewId, btn) {
            btn.classList.add('text-primary', 'font-bold');
            const countSpan = btn.querySelector('span');
            if (countSpan) {
                const cur = parseInt(countSpan.textContent) || 0;
                countSpan.textContent = cur + 1;
            }
            btn.disabled = true;
            showToast('Thank you for your feedback!', 'success');
        }

        // ==========================================
        // AI SHOPPING ASSISTANT
        // ==========================================
        function toggleAIAssistant() {
            const modal = document.getElementById('ai-assistant-modal');
            if (modal.classList.contains('hidden')) {
                modal.classList.remove('hidden');
                document.getElementById('ai-chat-input').focus();
            } else {
                modal.classList.add('hidden');
            }
        }

        function openAIAssistant(promptText) {
            const modal = document.getElementById('ai-assistant-modal');
            modal.classList.remove('hidden');
            if (promptText) {
                const inp = document.getElementById('ai-chat-input');
                inp.value = promptText;
                sendAIMessage();
            } else {
                document.getElementById('ai-chat-input').focus();
            }
        }

        async function sendAIMessage() {
            const inp = document.getElementById('ai-chat-input');
            const q = inp.value.trim();
            if (!q) return;
            inp.value = '';

            const container = document.getElementById('ai-chat-messages');

            // User bubble
            const userMsg = document.createElement('div');
            userMsg.className = 'flex justify-end';
            userMsg.innerHTML = `
                <div class="max-w-[85%] bg-primary text-white rounded-2xl rounded-tr-none px-4 py-2.5 text-xs shadow-md shadow-cyan-500/20">
                    ${escapeHtml(q)}
                </div>
            `;
            container.appendChild(userMsg);
            container.scrollTop = container.scrollHeight;

            // Loading bubble
            const loadMsg = document.createElement('div');
            loadMsg.className = 'flex justify-start';
            loadMsg.id = 'ai-loading-indicator';
            loadMsg.innerHTML = `
                <div class="bg-slate-800 text-cyan-400 rounded-2xl rounded-tl-none px-4 py-2.5 text-xs flex items-center gap-2 border border-slate-700">
                    <i data-lucide="sparkles" class="w-3.5 h-3.5 animate-spin"></i> Analyzing NVB marketplace catalog...
                </div>
            `;
            container.appendChild(loadMsg);
            initLucide();
            container.scrollTop = container.scrollHeight;

            try {
                const res = await fetch('/api/ai-assistant', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ query: q })
                });
                const data = await res.json();
                loadMsg.remove();

                const aiBubble = document.createElement('div');
                aiBubble.className = 'flex justify-start';
                
                let prodsHtml = '';
                if (data.recommended_products && data.recommended_products.length > 0) {
                    prodsHtml = `
                        <div class="mt-3 pt-3 border-t border-slate-700/60 space-y-2">
                            <span class="text-[10px] font-bold uppercase tracking-wider text-cyan-400">Recommended Products:</span>
                            <div class="grid grid-cols-1 gap-2">
                                ${data.recommended_products.map(p => `
                                    <div class="flex items-center gap-3 p-2 bg-slate-900/80 rounded-xl border border-white/5 hover:border-cyan-500/30 transition-all">
                                        <img src="${p.image_url}" class="w-12 h-12 object-cover rounded-lg flex-shrink-0" />
                                        <div class="min-w-0 flex-1">
                                            <a href="#product-${p.id}" onclick="toggleAIAssistant()" class="font-bold text-slate-200 hover:text-cyan-400 line-clamp-1 block text-xs">${escapeHtml(p.title)}</a>
                                            <div class="flex items-center gap-2 text-[11px] mt-0.5">
                                                <span class="font-bold text-cyan-400 font-mono">₹${p.price.toLocaleString('en-IN')}</span>
                                                <span class="text-slate-400 line-through text-[10px]">₹${p.mrp.toLocaleString('en-IN')}</span>
                                                <span class="text-[9px] bg-emerald-500/20 text-emerald-400 px-1 rounded font-bold">${p.discount_percent}% OFF</span>
                                            </div>
                                        </div>
                                        <button onclick="addToCart(${p.id}); showToast('Added to cart!', 'success');" class="p-2 rounded-lg bg-primary hover:bg-cyan-400 text-slate-950 font-bold transition-all flex-shrink-0" title="Add to Cart">
                                            <i data-lucide="plus" class="w-3.5 h-3.5"></i>
                                        </button>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    `;
                }

                aiBubble.innerHTML = `
                    <div class="max-w-[90%] bg-slate-800 text-slate-200 rounded-2xl rounded-tl-none p-3.5 text-xs shadow-md border border-slate-700 space-y-1.5 leading-relaxed">
                        <div class="flex items-center gap-1.5 font-bold text-cyan-400 text-[11px] mb-1">
                            <i data-lucide="bot" class="w-3.5 h-3.5"></i> NVB Vision AI
                        </div>
                        <div class="text-slate-300">${escapeHtml(data.response).replace(/\n/g, '<br/>')}</div>
                        ${prodsHtml}
                    </div>
                `;
                container.appendChild(aiBubble);
                initLucide();
                container.scrollTop = container.scrollHeight;

            } catch (e) {
                if (loadMsg) loadMsg.remove();
                showToast('AI Assistant is momentarily unavailable.', 'error');
            }
        }

        // ==========================================
        // VOICE SEARCH SIMULATOR
        // ==========================================
        function triggerVoiceSearch() {
            const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (SpeechRec) {
                const rec = new SpeechRec();
                rec.lang = 'en-IN';
                showToast('Listening... Speak now into your microphone.', 'info');
                rec.onresult = (evt) => {
                    const text = evt.results[0][0].transcript;
                    document.getElementById('global-search-input').value = text;
                    showToast(`Voice recognized: "${text}"`, 'success');
                    executeSearch();
                };
                rec.onerror = () => {
                    simulateVoiceFallback();
                };
                rec.start();
            } else {
                simulateVoiceFallback();
            }
        }

        function simulateVoiceFallback() {
            const samples = [
                'gaming headphones with spatial audio',
                'mechanical keyboard rgb',
                'running shoes under 3000',
                'smart watch with amoled display',
                'wireless ergonomic mouse'
            ];
            const chosen = samples[Math.floor(Math.random() * samples.length)];
            showToast('Simulating Voice: Listening...', 'info');
            setTimeout(() => {
                document.getElementById('global-search-input').value = chosen;
                showToast(`Voice query: "${chosen}"`, 'success');
                executeSearch();
            }, 1000);
        }

        // ==========================================
        // SELLER REGISTRATION MODAL
        // ==========================================
        function openSellerRegisterModal() {
            document.getElementById('modal-seller-register').classList.remove('hidden');
        }

        function closeSellerRegisterModal() {
            document.getElementById('modal-seller-register').classList.add('hidden');
        }

        async function handleSellerRegister(e) {
            if (e) e.preventDefault();
            const name = document.getElementById('seller-reg-name').value.trim();
            const business = document.getElementById('seller-reg-business').value.trim();
            const email = document.getElementById('seller-reg-email').value.trim();
            const phone = document.getElementById('seller-reg-phone').value.trim();
            const gstin = document.getElementById('seller-reg-gstin').value.trim();

            if (!name || !business || !email || !phone) {
                showToast('Please fill in all required seller details.', 'error');
                return;
            }

            try {
                const res = await fetch('/api/seller/register', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        name: name,
                        business_name: business,
                        email: email,
                        phone: phone,
                        gstin: gstin
                    })
                });
                const data = await res.json();
                if (res.ok) {
                    showToast('Seller account registered! Welcome to NVB Partner Network.', 'success');
                    closeSellerRegisterModal();
                    document.getElementById('seller-reg-name').value = '';
                    document.getElementById('seller-reg-business').value = '';
                    document.getElementById('seller-reg-email').value = '';
                    document.getElementById('seller-reg-phone').value = '';
                    document.getElementById('seller-reg-gstin').value = '';
                } else {
                    showToast(data.detail || 'Registration failed.', 'error');
                }
            } catch (err) {
                showToast('Network error during seller registration.', 'error');
            }
        }

        // ==========================================
        // ADMIN DASHBOARD
        // ==========================================
        let adminSalesChartInstance = null;
        let bulkPreviewRows = [];

        async function initAdminDashboard() {
            try {
                const res = await fetch('/api/admin/stats');
                const data = await res.json();
                renderAdminKPIs(data);
                renderAdminChart(data.revenue_chart || []);
                renderAdminCategoriesProgress(data.category_distribution || []);
                loadAdminProductsTable();
                loadAdminOrdersTable();
            } catch (e) {
                console.error('Failed to load admin stats:', e);
            }
        }

        function switchAdminTab(tabKey) {
            const tabs = ['analytics', 'products', 'orders', 'add-product', 'bulk-upload'];
            tabs.forEach(t => {
                const sec = document.getElementById(`admin-sec-${t}`);
                const btn = document.getElementById(`adm-tab-${t}`);
                if (sec) sec.classList.toggle('hidden', t !== tabKey);
                if (btn) {
                    if (t === tabKey) {
                        btn.className = "flex items-center gap-2 px-4 py-2.5 rounded-xl font-bold text-xs bg-primary text-slate-950 shadow-md shadow-cyan-500/20";
                    } else {
                        btn.className = "flex items-center gap-2 px-4 py-2.5 rounded-xl font-semibold text-xs text-slate-400 hover:text-white hover:bg-slate-800 transition-all";
                    }
                }
            });
            if (tabKey === 'analytics' && adminSalesChartInstance) {
                adminSalesChartInstance.resize();
            }
            initLucide();
        }

        function renderAdminKPIs(stats) {
            const grid = document.getElementById('admin-kpi-grid');
            if (!grid) return;
            grid.innerHTML = `
                <div class="p-5 bg-slate-900 border border-slate-800 rounded-2xl relative overflow-hidden group hover:border-cyan-500/40 transition-all">
                    <div class="absolute -right-4 -bottom-4 w-24 h-24 bg-cyan-500/10 rounded-full blur-xl group-hover:bg-cyan-500/20 transition-all"></div>
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Gross Merchandise Value</span>
                        <span class="p-2 rounded-xl bg-cyan-500/10 text-cyan-400"><i data-lucide="badge-dollar-sign" class="w-4 h-4"></i></span>
                    </div>
                    <div class="text-2xl font-black text-white font-mono mt-3">₹${(stats.total_gmv || 0).toLocaleString('en-IN')}</div>
                    <div class="text-[11px] text-emerald-400 flex items-center gap-1 mt-1 font-semibold">
                        <i data-lucide="trending-up" class="w-3.5 h-3.5"></i> +18.4% this month
                    </div>
                </div>

                <div class="p-5 bg-slate-900 border border-slate-800 rounded-2xl relative overflow-hidden group hover:border-cyan-500/40 transition-all">
                    <div class="absolute -right-4 -bottom-4 w-24 h-24 bg-indigo-500/10 rounded-full blur-xl group-hover:bg-indigo-500/20 transition-all"></div>
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Total Orders</span>
                        <span class="p-2 rounded-xl bg-indigo-500/10 text-indigo-400"><i data-lucide="shopping-bag" class="w-4 h-4"></i></span>
                    </div>
                    <div class="text-2xl font-black text-white font-mono mt-3">${stats.total_orders || 0}</div>
                    <div class="text-[11px] text-emerald-400 flex items-center gap-1 mt-1 font-semibold">
                        <i data-lucide="trending-up" class="w-3.5 h-3.5"></i> +9.2% conversion
                    </div>
                </div>

                <div class="p-5 bg-slate-900 border border-slate-800 rounded-2xl relative overflow-hidden group hover:border-cyan-500/40 transition-all">
                    <div class="absolute -right-4 -bottom-4 w-24 h-24 bg-emerald-500/10 rounded-full blur-xl group-hover:bg-emerald-500/20 transition-all"></div>
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Catalog Inventory</span>
                        <span class="p-2 rounded-xl bg-emerald-500/10 text-emerald-400"><i data-lucide="box" class="w-4 h-4"></i></span>
                    </div>
                    <div class="text-2xl font-black text-white font-mono mt-3">${stats.total_products || 0} SKUs</div>
                    <div class="text-[11px] text-slate-400 flex items-center gap-1 mt-1 font-semibold">
                        <span class="text-amber-400">${stats.low_stock_count || 0} low stock</span> items
                    </div>
                </div>

                <div class="p-5 bg-slate-900 border border-slate-800 rounded-2xl relative overflow-hidden group hover:border-cyan-500/40 transition-all">
                    <div class="absolute -right-4 -bottom-4 w-24 h-24 bg-amber-500/10 rounded-full blur-xl group-hover:bg-amber-500/20 transition-all"></div>
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Average Order Value</span>
                        <span class="p-2 rounded-xl bg-amber-500/10 text-amber-400"><i data-lucide="credit-card" class="w-4 h-4"></i></span>
                    </div>
                    <div class="text-2xl font-black text-white font-mono mt-3">₹${(stats.avg_order_value || 0).toLocaleString('en-IN')}</div>
                    <div class="text-[11px] text-cyan-400 flex items-center gap-1 mt-1 font-semibold">
                        <i data-lucide="check-circle-2" class="w-3.5 h-3.5"></i> High-ticket focus
                    </div>
                </div>
            `;
            initLucide();
        }

        function renderAdminChart(chartData) {
            const ctx = document.getElementById('adminSalesChart');
            if (!ctx) return;
            
            const labels = chartData.map(d => d.month || d.label || 'M');
            const dataPoints = chartData.map(d => d.revenue || d.value || 0);

            if (adminSalesChartInstance) {
                adminSalesChartInstance.destroy();
            }

            adminSalesChartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels.length > 0 ? labels : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                    datasets: [{
                        label: 'Gross Revenue (₹)',
                        data: dataPoints.length > 0 ? dataPoints : [42000, 68000, 95000, 142000, 189000, 245000],
                        borderColor: '#06b6d4',
                        backgroundColor: 'rgba(6, 182, 212, 0.1)',
                        fill: true,
                        tension: 0.4,
                        borderWidth: 3,
                        pointBackgroundColor: '#06b6d4',
                        pointBorderColor: '#ffffff',
                        pointHoverRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: (ctx) => ` ₹${ctx.parsed.y.toLocaleString('en-IN')}`
                            }
                        }
                    },
                    scales: {
                        y: {
                            grid: { color: 'rgba(255, 255, 255, 0.05)' },
                            ticks: {
                                color: '#94a3b8',
                                callback: (val) => '₹' + (val >= 1000 ? (val / 1000) + 'k' : val)
                            }
                        },
                        x: {
                            grid: { display: false },
                            ticks: { color: '#94a3b8' }
                        }
                    }
                }
            });
        }

        function renderAdminCategoriesProgress(catDist) {
            const container = document.getElementById('admin-categories-progress');
            if (!container) return;
            if (!catDist || catDist.length === 0) {
                container.innerHTML = '<span class="text-xs text-slate-500">No category data.</span>';
                return;
            }
            const total = catDist.reduce((acc, c) => acc + c.count, 0) || 1;
            container.innerHTML = catDist.slice(0, 5).map(c => {
                const pct = Math.round((c.count / total) * 100);
                return `
                    <div class="space-y-1">
                        <div class="flex justify-between text-xs font-semibold">
                            <span class="text-slate-300">${escapeHtml(c.name)}</span>
                            <span class="text-slate-400 font-mono">${c.count} items (${pct}%)</span>
                        </div>
                        <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                            <div class="bg-primary h-full rounded-full" style="width: ${pct}%"></div>
                        </div>
                    </div>
                `;
            }).join('');
        }

        async function loadAdminProductsTable() {
            const tbody = document.getElementById('admin-products-table-body');
            if (!tbody) return;
            try {
                const res = await fetch('/api/products?limit=50');
                const data = await res.json();
                const prods = data.products || [];
                tbody.innerHTML = prods.map(p => `
                    <tr class="border-b border-slate-800 hover:bg-slate-800/40 text-xs">
                        <td class="py-3 px-4 font-mono text-slate-500">${p.id}</td>
                        <td class="py-3 px-4">
                            <div class="flex items-center gap-3">
                                <img src="${p.image_url}" class="w-10 h-10 object-cover rounded-lg border border-slate-700 flex-shrink-0" />
                                <div>
                                    <span class="font-bold text-white block line-clamp-1">${escapeHtml(p.title)}</span>
                                    <span class="text-[10px] text-slate-400 font-mono">SKU: ${p.sku || 'NVB-PROD'}</span>
                                </div>
                            </div>
                        </td>
                        <td class="py-3 px-4 text-slate-300">${escapeHtml(p.category_name || 'General')}</td>
                        <td class="py-3 px-4 font-mono font-bold text-cyan-400">₹${p.price.toLocaleString('en-IN')}</td>
                        <td class="py-3 px-4 font-mono ${p.stock <= 5 ? 'text-rose-400 font-bold' : 'text-slate-300'}">${p.stock}</td>
                        <td class="py-3 px-4">
                            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold ${p.stock > 0 ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'}">
                                ${p.stock > 0 ? 'Active' : 'Out of Stock'}
                            </span>
                        </td>
                        <td class="py-3 px-4 text-right">
                            <button onclick="deleteAdminProduct(${p.id})" class="p-1.5 rounded-lg text-rose-400 hover:bg-rose-500/10 transition-all" title="Delete Product">
                                <i data-lucide="trash-2" class="w-4 h-4"></i>
                            </button>
                        </td>
                    </tr>
                `).join('');
                initLucide();
            } catch (e) {
                console.error(e);
            }
        }

        async function deleteAdminProduct(id) {
            if (!confirm(`Are you sure you want to delete Product #${id}?`)) return;
            try {
                const res = await fetch(`/api/admin/products/${id}`, { method: 'DELETE' });
                if (res.ok) {
                    showToast(`Product #${id} removed from catalog.`, 'success');
                    loadAdminProductsTable();
                    fetchProducts();
                } else {
                    showToast('Failed to delete product.', 'error');
                }
            } catch (e) {
                showToast('Error connecting to admin API.', 'error');
            }
        }

        async function loadAdminOrdersTable() {
            const tbody = document.getElementById('admin-orders-table-body');
            if (!tbody) return;
            try {
                const res = await fetch('/api/orders');
                const orders = await res.json();
                tbody.innerHTML = orders.map(o => `
                    <tr class="border-b border-slate-800 hover:bg-slate-800/40 text-xs">
                        <td class="py-3 px-4 font-mono font-bold text-cyan-400">${o.order_number}</td>
                        <td class="py-3 px-4 text-slate-300">
                            <div>${escapeHtml(o.shipping_name || 'Customer')}</div>
                            <div class="text-[10px] text-slate-500 font-mono">${o.shipping_phone || ''}</div>
                        </td>
                        <td class="py-3 px-4 font-mono text-slate-400">${(o.created_at || '').substring(0, 10)}</td>
                        <td class="py-3 px-4 font-mono font-bold text-white">₹${o.total.toLocaleString('en-IN')}</td>
                        <td class="py-3 px-4">
                            <select onchange="updateAdminOrderStatus(${o.id}, this.value)" class="bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded-lg px-2.5 py-1 focus:ring-primary focus:border-primary">
                                <option value="Placed" ${o.status === 'Placed' ? 'selected' : ''}>Placed</option>
                                <option value="Processing" ${o.status === 'Processing' ? 'selected' : ''}>Processing</option>
                                <option value="Dispatched" ${o.status === 'Dispatched' ? 'selected' : ''}>Dispatched</option>
                                <option value="Shipped" ${o.status === 'Shipped' ? 'selected' : ''}>Shipped</option>
                                <option value="Delivered" ${o.status === 'Delivered' ? 'selected' : ''}>Delivered</option>
                                <option value="Cancelled" ${o.status === 'Cancelled' ? 'selected' : ''}>Cancelled</option>
                            </select>
                        </td>
                        <td class="py-3 px-4 text-right">
                            <button onclick="viewInvoice(${o.id})" class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold">
                                Invoice
                            </button>
                        </td>
                    </tr>
                `).join('');
                initLucide();
            } catch (e) {
                console.error(e);
            }
        }

        async function updateAdminOrderStatus(orderId, newStatus) {
            try {
                const res = await fetch(`/api/orders/${orderId}/status?status=${encodeURIComponent(newStatus)}`, {
                    method: 'PATCH'
                });
                if (res.ok) {
                    showToast(`Order status updated to "${newStatus}"`, 'success');
                } else {
                    showToast('Failed to update status.', 'error');
                }
            } catch (e) {
                showToast('Network error updating order status.', 'error');
            }
        }

        // ==========================================
        // SECTION 37: 3-COLUMN PRODUCT ADDER
        // ==========================================
        async function handleAdminAddProduct(e) {
            if (e) e.preventDefault();
            const title = document.getElementById('add-prod-title').value.trim();
            const category_id = parseInt(document.getElementById('add-prod-cat').value);
            const subcategory = document.getElementById('add-prod-subcat').value.trim();
            const brand = document.getElementById('add-prod-brand').value.trim();
            const sku = document.getElementById('add-prod-sku').value.trim();
            const price = parseFloat(document.getElementById('add-prod-price').value);
            const mrp = parseFloat(document.getElementById('add-prod-mrp').value);
            const stock = parseInt(document.getElementById('add-prod-stock').value) || 0;
            const short_desc = document.getElementById('add-prod-short-desc').value.trim();
            const description = document.getElementById('add-prod-desc').value.trim();
            const imgUrl = document.getElementById('add-prod-img-url').value.trim();
            const specsRaw = document.getElementById('add-prod-specs').value.trim();
            const is_featured = document.getElementById('add-prod-feat').checked;
            const is_flash = document.getElementById('add-prod-flash').checked;
            const is_deal = document.getElementById('add-prod-deal').checked;

            if (!title || !price || !category_id) {
                showToast('Please fill in required fields: Title, Category, and Price.', 'error');
                return;
            }

            let specsObj = {};
            if (specsRaw) {
                try {
                    specsObj = JSON.parse(specsRaw);
                } catch (err) {
                    showToast('Invalid JSON in Specifications field. Use {"Key": "Value"}.', 'error');
                    return;
                }
            }

            const payload = {
                title: title,
                category_id: category_id,
                subcategory: subcategory,
                brand: brand || 'NVB Vision',
                sku: sku || ('NVB-' + Math.floor(1000 + Math.random() * 9000)),
                price: price,
                mrp: mrp || price * 1.25,
                stock: stock,
                short_description: short_desc,
                description: description,
                image_url: imgUrl || 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80',
                additional_images: [imgUrl || 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80'],
                specifications: specsObj,
                variants: [],
                is_featured: is_featured,
                is_flash_sale: is_flash,
                deal_of_the_day: is_deal,
                rating: 4.8,
                reviews_count: 1
            };

            try {
                const res = await fetch('/api/admin/products', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (res.ok) {
                    showToast(`Product "${title}" added to catalog successfully!`, 'success');
                    document.getElementById('add-prod-title').value = '';
                    document.getElementById('add-prod-price').value = '';
                    document.getElementById('add-prod-mrp').value = '';
                    document.getElementById('add-prod-stock').value = '25';
                    document.getElementById('add-prod-short-desc').value = '';
                    document.getElementById('add-prod-desc').value = '';
                    document.getElementById('add-prod-specs').value = '';
                    loadAdminProductsTable();
                    switchAdminTab('products');
                    fetchProducts();
                } else {
                    showToast(data.detail || 'Failed to add product.', 'error');
                }
            } catch (err) {
                showToast('Network error while creating product.', 'error');
            }
        }

        // ==========================================
        // SECTION 38: BULK CSV IMPORT ENGINE
        // ==========================================
        function downloadCSVTemplate() {
            const csv = 'title,category_id,subcategory,brand,sku,price,mrp,stock,image_url,short_description\n' +
                '"NVB Quantum Soundbar 120W",1,"Audio","NVB Sound","NVB-SB120",8999,14999,35,"https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800","Dolby Atmos home soundbar"\n' +
                '"NVB Vision Neo Smartwatch",1,"Wearables","NVB","NVB-NEO1",3499,5999,50,"https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800","1.96 AMOLED display smartwatch"\n';
            const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.setAttribute('download', 'nvb_products_bulk_template.csv');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        function handleBulkCSVUpload(event) {
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(e) {
                const text = e.target.result;
                parseCSVToPreview(text);
            };
            reader.readAsText(file);
        }

        function parseCSVToPreview(csvText) {
            const lines = csvText.split(/\r?\n/).filter(l => l.trim().length > 0);
            if (lines.length < 2) {
                showToast('CSV must contain a header row and at least 1 product row.', 'error');
                return;
            }

            bulkPreviewRows = [];

            for (let i = 1; i < lines.length; i++) {
                const matches = lines[i].match(/(".*?"|[^",\s]+)(?=\s*,|\s*$)/g) || lines[i].split(',');
                const row = matches.map(c => c.trim().replace(/^"|"$/g, ''));
                if (row.length >= 4) {
                    const title = row[0] || 'Bulk Product ' + i;
                    const catId = parseInt(row[1]) || 1;
                    const subcat = row[2] || 'General';
                    const brand = row[3] || 'NVB';
                    const sku = row[4] || ('NVB-BLK-' + i);
                    const price = parseFloat(row[5]) || 999;
                    const mrp = parseFloat(row[6]) || (price * 1.3);
                    const stock = parseInt(row[7]) || 20;
                    const img = row[8] || 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800';
                    const desc = row[9] || 'Premium product imported via NVB Bulk Import Engine.';

                    bulkPreviewRows.push({
                        title: title,
                        category_id: catId,
                        subcategory: subcat,
                        brand: brand,
                        sku: sku,
                        price: price,
                        mrp: mrp,
                        stock: stock,
                        image_url: img,
                        short_description: desc,
                        description: desc,
                        specifications: {"Import Source": "CSV Bulk Engine"},
                        variants: [],
                        rating: 4.7,
                        reviews_count: 0
                    });
                }
            }

            const wrapper = document.getElementById('bulk-preview-wrapper');
            const tbody = document.getElementById('bulk-preview-tbody');
            const countEl = document.getElementById('bulk-preview-count');

            if (bulkPreviewRows.length > 0) {
                wrapper.classList.remove('hidden');
                countEl.textContent = `${bulkPreviewRows.length} valid rows found`;
                tbody.innerHTML = bulkPreviewRows.map((r, idx) => `
                    <tr class="border-b border-slate-800 text-xs">
                        <td class="py-2 px-3 text-slate-400 font-mono">${idx + 1}</td>
                        <td class="py-2 px-3 font-semibold text-white">${escapeHtml(r.title)}</td>
                        <td class="py-2 px-3 text-slate-400">${r.category_id}</td>
                        <td class="py-2 px-3 font-mono font-bold text-cyan-400">₹${r.price.toLocaleString('en-IN')}</td>
                        <td class="py-2 px-3 font-mono text-slate-300">${r.stock}</td>
                        <td class="py-2 px-3 font-mono text-slate-500">${escapeHtml(r.sku)}</td>
                    </tr>
                `).join('');
            } else {
                showToast('Could not parse valid product rows from CSV.', 'error');
            }
        }

        async function submitBulkImport() {
            if (bulkPreviewRows.length === 0) {
                showToast('No rows to import.', 'error');
                return;
            }

            try {
                const res = await fetch('/api/admin/bulk-import', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ products: bulkPreviewRows })
                });
                const data = await res.json();
                if (res.ok) {
                    showToast(`Successfully imported ${data.imported_count || bulkPreviewRows.length} products into NVB catalog!`, 'success');
                    bulkPreviewRows = [];
                    document.getElementById('bulk-preview-wrapper').classList.add('hidden');
                    document.getElementById('bulk-csv-input').value = '';
                    loadAdminProductsTable();
                    switchAdminTab('products');
                    fetchProducts();
                } else {
                    showToast(data.detail || 'Bulk import failed.', 'error');
                }
            } catch (err) {
                showToast('Network error during bulk import.', 'error');
            }
        }

        // ==========================================
        // TOAST NOTIFICATIONS HELPER
        // ==========================================
        function showToast(message, type = 'info') {
            const container = document.getElementById('toast-container');
            if (!container) return;

            const toast = document.createElement('div');
            let bgClass = 'bg-slate-900 border-cyan-500/40 text-cyan-300';
            let iconName = 'info';

            if (type === 'success') {
                bgClass = 'bg-slate-900 border-emerald-500/40 text-emerald-400';
                iconName = 'check-circle-2';
            } else if (type === 'error') {
                bgClass = 'bg-slate-900 border-rose-500/40 text-rose-400';
                iconName = 'alert-triangle';
            }

            toast.className = `flex items-center gap-2.5 px-4 py-3 rounded-2xl border shadow-xl backdrop-blur-md text-xs font-semibold transition-all transform duration-300 translate-y-4 opacity-0 ${bgClass}`;
            toast.innerHTML = `<i data-lucide="${iconName}" class="w-4 h-4 flex-shrink-0"></i> <span>${escapeHtml(message)}</span>`;
            
            container.appendChild(toast);
            initLucide();

            setTimeout(() => {
                toast.classList.remove('translate-y-4', 'opacity-0');
                toast.classList.add('translate-y-0', 'opacity-100');
            }, 10);

            setTimeout(() => {
                toast.classList.add('opacity-0', 'translate-x-4');
                setTimeout(() => toast.remove(), 300);
            }, 3500);
        }

        function escapeHtml(str) {
            if (!str) return '';
            return String(str)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#039;');
        }

        // ==========================================
        // AUTOCOMPLETE SEARCH SUGGESTIONS
        // ==========================================
        const searchInput = document.getElementById('global-search-input');
        const searchSuggestionsBox = document.getElementById('search-suggestions');
        const searchSuggestionsList = document.getElementById('search-suggestions-list');

        if (searchInput && searchSuggestionsBox && searchSuggestionsList) {
            searchInput.addEventListener('input', (e) => {
                const q = e.target.value.trim().toLowerCase();
                if (q.length < 2) {
                    searchSuggestionsBox.classList.add('hidden');
                    return;
                }
                const matches = (appState.products || []).filter(p => 
                    p.title.toLowerCase().includes(q) || 
                    (p.brand && p.brand.toLowerCase().includes(q)) ||
                    (p.category_name && p.category_name.toLowerCase().includes(q))
                ).slice(0, 5);

                if (matches.length > 0) {
                    searchSuggestionsList.innerHTML = matches.map(m => `
                        <a href="#product-${m.id}" onclick="document.getElementById('search-suggestions').classList.add('hidden')" class="flex items-center gap-3 p-2 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-xl transition-all">
                            <img src="${m.image_url}" class="w-9 h-9 object-cover rounded-lg border border-slate-200 dark:border-slate-700 flex-shrink-0" />
                            <div class="min-w-0 flex-1">
                                <div class="font-bold text-xs text-slate-800 dark:text-slate-200 truncate">${escapeHtml(m.title)}</div>
                                <div class="text-[10px] text-primary font-mono font-bold">₹${m.price.toLocaleString('en-IN')}</div>
                            </div>
                        </a>
                    `).join('');
                    searchSuggestionsBox.classList.remove('hidden');
                } else {
                    searchSuggestionsBox.classList.add('hidden');
                }
            });

            document.addEventListener('click', (e) => {
                if (!searchInput.contains(e.target) && !searchSuggestionsBox.contains(e.target)) {
                    searchSuggestionsBox.classList.add('hidden');
                }
            });
        }

        // ==========================================
        // INITIALIZATION ON DOM READY
        // ==========================================
        window.addEventListener('DOMContentLoaded', async () => {
            initLucide();
            startFlashSaleTimer();

            // Saved pincode
            const savedPin = localStorage.getItem('nvb_pincode') || '560038';
            const savedCity = localStorage.getItem('nvb_city') || 'Bengaluru';
            updateLocationDisplay(savedPin, savedCity);

            // Fetch core datasets
            await fetchCategories();
            await fetchProducts();
            await fetchCart();
            await fetchWishlist();

            // Hash router listener
            window.addEventListener('hashchange', () => {
                navigate(window.location.hash || '#home');
            });

            // Initial route
            navigate(window.location.hash || '#home');
        });
    </script>
</body>
</html>
'''

# Append part 7g to build_ui.py
with open('build_ui.py', 'r', encoding='utf-8') as f:
    orig = f.read()

# Append to parts list in build_ui.py
append_stmt = "\nparts.append(r'''" + code_part7g + "''')\n\nwith open('static/index.html', 'w', encoding='utf-8') as out_f:\n    out_f.write(''.join(parts))\nprint('static/index.html generated successfully! Total size:', len(''.join(parts)))\n"

with open('build_ui.py', 'w', encoding='utf-8') as f:
    f.write(orig + append_stmt)

print("build_ui.py successfully updated with Part 7g and file generator!")
