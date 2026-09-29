with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Google Fonts in <head>
old_fonts = '''    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">'''

new_fonts = '''    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">'''

if old_fonts in html:
    html = html.replace(old_fonts, new_fonts)
    print("Replaced Google Fonts with Cinzel and Playfair Display")
else:
    print("Warning: old_fonts not matched")

# 2. Update Header styling
old_hdr = '<header class="sticky top-0 z-40 bg-nvb-dark/95 backdrop-blur-md border-b border-white/10 shadow-2xl">'
new_hdr = '<header class="sticky top-0 z-40 bg-[#090b10]/95 backdrop-blur-md border-b border-amber-500/20 shadow-xl shadow-black/50">'

if old_hdr in html:
    html = html.replace(old_hdr, new_hdr)
    print("Updated Header background and border")
else:
    print("Warning: old_hdr not matched")

# 3. Update Hero Slides 1 and 2 to Editorial Luxury Campaigns
idx_s1 = html.find('<!-- Hero Slide 1 -->')
idx_controls = html.find('<!-- Carousel Controls -->')

new_slides = '''<!-- Hero Slide 1 -->
                        <div id="hero-slide-1" class="hero-slide absolute inset-0 flex flex-col md:flex-row items-center justify-between p-8 md:p-14 bg-gradient-to-r from-[#07080c] via-[#0e1017]/95 to-[#161a25]/85 transition-opacity duration-700 opacity-100">
                            <div class="max-w-xl z-10 space-y-4">
                                <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-mono tracking-widest uppercase">
                                    <i data-lucide="crown" class="w-3.5 h-3.5 text-amber-400"></i> The Autumn Atelier Collection
                                </div>
                                <h1 class="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-black font-display tracking-wide text-white leading-tight">
                                    ENGINEERED <br>
                                    <span class="gold-gradient-text">PERFECTION</span>
                                </h1>
                                <p class="text-slate-300 text-sm md:text-base font-light leading-relaxed max-w-lg">
                                    "Your Next Vision of Shopping." Discover curated flagship electronics, handcrafted apparel, artisanal kitchenware, and certified luxury essentials.
                                </p>
                                <div class="flex flex-wrap items-center gap-4 pt-2">
                                    <button onclick="navigate('shop')" class="px-8 py-3.5 rounded-xl btn-gold text-sm shadow-xl flex items-center gap-2">
                                        <span>Explore Atelier Catalog</span>
                                        <i data-lucide="arrow-right" class="w-4 h-4"></i>
                                    </button>
                                    <button onclick="navigate('deals')" class="px-7 py-3.5 rounded-xl btn-gold-outline font-semibold text-sm">
                                        Private Vault Exclusives
                                    </button>
                                </div>
                            </div>
                            <div class="relative mt-8 md:mt-0 flex-1 flex justify-center">
                                <div class="relative">
                                    <div class="absolute -inset-6 bg-gradient-to-tr from-amber-500/15 to-transparent rounded-full blur-3xl opacity-70"></div>
                                    <img src="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80" alt="Flagship Tech" class="relative max-h-72 md:max-h-96 object-contain drop-shadow-2xl hover:scale-105 transition duration-500">
                                </div>
                            </div>
                        </div>

                        <!-- Hero Slide 2 -->
                        <div id="hero-slide-2" class="hero-slide absolute inset-0 flex flex-col md:flex-row items-center justify-between p-8 md:p-14 bg-gradient-to-r from-[#07080c] via-[#15121c]/90 to-[#1e172a]/70 transition-opacity duration-700 opacity-0 pointer-events-none">
                            <div class="max-w-xl z-10 space-y-4">
                                <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-mono tracking-widest uppercase">
                                    <i data-lucide="shield-check" class="w-3.5 h-3.5 text-amber-400"></i> Bespoke Verified Luxury
                                </div>
                                <h1 class="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-black font-display tracking-wide text-white leading-tight">
                                    THE PRIVATE <br>
                                    <span class="gold-gradient-text">COLLECTION</span>
                                </h1>
                                <p class="text-slate-300 text-sm md:text-base font-light leading-relaxed max-w-lg">
                                    Direct partnerships with authorized designers and manufacturers. Guaranteed authentic serial verification, 2-year warranty, and express courier handling.
                                </p>
                                <div class="flex flex-wrap items-center gap-4 pt-2">
                                    <button onclick="navigate('shop')" class="px-8 py-3.5 rounded-xl btn-gold text-sm shadow-xl flex items-center gap-2">
                                        <span>Discover Heritage Pieces</span>
                                        <i data-lucide="arrow-right" class="w-4 h-4"></i>
                                    </button>
                                    <button onclick="navigate('deals')" class="px-7 py-3.5 rounded-xl btn-gold-outline font-semibold text-sm">
                                        Vault Access
                                    </button>
                                </div>
                            </div>
                            <div class="relative mt-8 md:mt-0 flex-1 flex justify-center">
                                <div class="relative">
                                    <div class="absolute -inset-6 bg-gradient-to-tr from-amber-500/20 to-transparent rounded-full blur-3xl opacity-70"></div>
                                    <img src="https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80" alt="Bespoke Luxury" class="relative max-h-72 md:max-h-96 object-contain drop-shadow-2xl hover:scale-105 transition duration-500">
                                </div>
                            </div>
                        </div>
                    </div>\n\n                    '''

if idx_s1 != -1 and idx_controls != -1:
    html = html[:idx_s1] + new_slides + html[idx_controls:]
    print("Replaced Hero Slides with Luxury Campaigns")
else:
    print("Warning: hero slides bounds not found")

# 4. Replace renderProductCard with Luxury Showroom Card
idx_rpc = html.find('function renderProductCard')
idx_home = html.find('function renderHome()', idx_rpc)

new_render_product_card = '''function renderProductCard(p, isFlash = false) {
            const isWished = appState.wishlist.some(w => w.product_id === p.id);
            const isCompared = appState.compareList.includes(p.id);
            const discPill = p.discount > 0 ? `<span class="bg-amber-500/15 text-amber-300 border border-amber-500/40 text-[9px] font-mono font-bold px-2 py-0.5 rounded tracking-wider uppercase">${p.discount}% PRIVILEGE</span>` : '';
            const flashProgress = isFlash ? `
                <div class="mt-2 space-y-1">
                    <div class="flex justify-between text-[10px] text-slate-400 font-medium">
                        <span>Vault Reserved: ${p.flash_sold || 35}</span>
                        <span class="text-amber-400 font-semibold font-mono">Only ${Math.max(1, p.flash_stock_limit - (p.flash_sold || 0))} Available!</span>
                    </div>
                    <div class="w-full bg-slate-900 rounded-full h-1.5 overflow-hidden border border-white/5">
                        <div class="bg-gradient-to-r from-amber-500 to-yellow-300 h-1.5 rounded-full" style="width: ${Math.min(100, Math.round(((p.flash_sold || 35) / p.flash_stock_limit) * 100))}%"></div>
                    </div>
                </div>
            ` : '';

            const imgUrl = (p.images && p.images.length > 0) ? p.images[0] : (p.image_url || 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800');

            return `
            <div class="glass-card p-4 flex flex-col justify-between group relative">
                <div class="relative">
                    <div class="aspect-square rounded-xl overflow-hidden bg-[#0c0e14] border border-white/5 flex items-center justify-center p-3 relative cursor-pointer group-hover:border-amber-500/25 transition duration-300" onclick="openProductDetail('${p.id}')">
                        <img src="${imgUrl}" alt="${p.title}" class="max-h-full max-w-full object-contain group-hover:scale-105 transition duration-500">
                    </div>
                    <div class="absolute top-2 left-2 flex flex-col gap-1.5">
                        ${discPill}
                        ${p.is_flash_sale ? '<span class="bg-[#090b10]/90 text-amber-300 border border-amber-500/40 font-mono font-bold text-[9px] px-2 py-0.5 rounded uppercase tracking-wider">VAULT EXCLUSIVE</span>' : ''}
                    </div>
                    <button onclick="event.stopPropagation(); toggleWishlist('${p.id}')" class="absolute top-2 right-2 p-2 rounded-xl bg-black/60 backdrop-blur-md border border-white/10 hover:border-amber-400/40 text-slate-300 hover:text-rose-400 transition ${isWished ? 'text-rose-500 border-rose-500/30' : ''}">
                        <i data-lucide="heart" class="w-4 h-4 ${isWished ? 'fill-current text-rose-500' : ''}"></i>
                    </button>
                </div>

                <div class="mt-4 flex-1 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between text-xs text-slate-400 mb-1">
                            <span class="font-mono text-[10px] text-amber-400 uppercase tracking-widest font-semibold">${p.brand || 'NEXT VISION'}</span>
                            <span class="flex items-center gap-1 text-amber-400 font-semibold font-mono text-xs"><i data-lucide="star" class="w-3.5 h-3.5 fill-current text-amber-400"></i> ${p.rating}</span>
                        </div>
                        <h3 class="font-bold text-white text-sm line-clamp-2 hover:text-amber-300 cursor-pointer transition mb-2" onclick="openProductDetail('${p.id}')">${p.title}</h3>
                    </div>

                    ${flashProgress}

                    <div class="mt-3 pt-3 border-t border-white/5 flex items-center justify-between">
                        <div>
                            <div class="flex items-baseline gap-2">
                                <span class="text-lg font-black text-amber-300 font-mono">₹${p.price.toLocaleString('en-IN')}</span>
                                ${p.mrp > p.price ? `<span class="text-xs text-slate-500 line-through font-mono">₹${p.mrp.toLocaleString('en-IN')}</span>` : ''}
                            </div>
                        </div>
                        <div class="flex items-center gap-1.5">
                            <button onclick="event.stopPropagation(); toggleCompare('${p.id}')" class="p-2 rounded-xl border border-white/10 hover:border-amber-400/50 text-slate-400 hover:text-white transition ${isCompared ? 'bg-amber-500 text-slate-950 font-bold border-amber-400' : 'bg-slate-900'}" title="Compare">
                                <i data-lucide="repeat" class="w-4 h-4"></i>
                            </button>
                            <button onclick="event.stopPropagation(); addToCart('${p.id}')" class="p-2 rounded-xl btn-gold text-slate-950 transition" title="Add to Bag">
                                <i data-lucide="shopping-bag" class="w-4 h-4"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            `;
        }\n\n        '''

if idx_rpc != -1 and idx_home != -1:
    html = html[:idx_rpc] + new_render_product_card + html[idx_home:]
    print("Replaced renderProductCard with Luxury Showroom Card")
else:
    print("Warning: renderProductCard range not found")

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("apply_luxury_gui.py finished successfully!")
