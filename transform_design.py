import re

with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update <head> with luxury fonts and bespoke stylesheet
old_head_fonts = '''<link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">'''

new_head_fonts = '''<link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700;800;900&family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">'''

if old_head_fonts in html:
    html = html.replace(old_head_fonts, new_head_fonts)
    print("Updated Google Fonts with Cinzel & Playfair Display")
else:
    print("Warning: old_head_fonts not matched")

# 2. Update Tailwind Config colors
old_tailwind = '''tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        nvb: {
                            dark: '#080d1a',
                            slate: '#0f172a',
                            card: '#131e36',
                            border: '#1e293b',
                            blue: '#2563eb',
                            cyan: '#06b6d4',
                            accent: '#3b82f6',
                            emerald: '#10b981',
                            coral: '#f43f5e',
                            amber: '#f59e0b'
                        }
                    },
                    fontFamily: {
                        sans: ['Plus Jakarta Sans', 'Inter', 'sans-serif'],
                        display: ['Outfit', 'sans-serif']
                    }
                }
            }
        }'''

new_tailwind = '''tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        primary: '#d4af37',
                        nvb: {
                            dark: '#08090d',
                            obsidian: '#0e1017',
                            surface: '#141722',
                            elevated: '#1c202e',
                            border: 'rgba(212, 175, 55, 0.15)',
                            gold: '#d4af37',
                            'gold-light': '#f5e6b8',
                            'gold-dark': '#997b20',
                            silver: '#e2e8f0',
                            accent: '#c59b27',
                            emerald: '#10b981',
                            crimson: '#e11d48',
                            amber: '#f59e0b'
                        }
                    },
                    fontFamily: {
                        sans: ['Plus Jakarta Sans', 'Inter', 'sans-serif'],
                        display: ['Cinzel', 'serif'],
                        editorial: ['Playfair Display', 'serif']
                    }
                }
            }
        }'''

if old_tailwind in html:
    html = html.replace(old_tailwind, new_tailwind)
    print("Updated Tailwind Config with Luxury Gold & Obsidian palette")
else:
    print("Warning: old_tailwind not matched")

# 3. Update CSS <style> block with rich tactile luxury textures
idx_style_start = html.find('<style>')
idx_style_end = html.find('</style>') + 8

new_style_block = '''<style>
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #07080c;
            background-image: 
                radial-gradient(circle at 50% 0%, rgba(212, 175, 55, 0.08) 0%, rgba(7, 8, 12, 0) 70%),
                radial-gradient(rgba(212, 175, 55, 0.035) 1px, transparent 0);
            background-size: 100% 100%, 28px 28px;
            color: #f1f5f9;
            min-height: 100vh;
        }

        h1, h2, h3, .font-display {
            font-family: 'Cinzel', serif;
            letter-spacing: 0.03em;
        }

        .font-editorial {
            font-family: 'Playfair Display', serif;
        }

        /* Bespoke Luxury Scrollbars */
        ::-webkit-scrollbar { width: 7px; height: 7px; }
        ::-webkit-scrollbar-track { background: #08090d; }
        ::-webkit-scrollbar-thumb { background: #262a36; border-radius: 4px; border: 1px solid rgba(212, 175, 55, 0.1); }
        ::-webkit-scrollbar-thumb:hover { background: #d4af37; }

        /* Bespoke Obsidian & Gold Card Surfaces */
        .glass-panel {
            background: linear-gradient(180deg, rgba(17, 20, 29, 0.85) 0%, rgba(10, 12, 18, 0.95) 100%);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(212, 175, 55, 0.15);
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.8), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        }

        .glass-card {
            background: linear-gradient(155deg, rgba(20, 24, 34, 0.75) 0%, rgba(11, 13, 19, 0.92) 100%);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 1.25rem;
            box-shadow: 0 6px 20px -4px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.04);
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .glass-card:hover {
            transform: translateY(-4px);
            border-color: rgba(212, 175, 55, 0.45);
            box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.8), 0 0 25px rgba(212, 175, 55, 0.12), inset 0 1px 0 rgba(212, 175, 55, 0.3);
        }

        /* Luxury Metallic Gradients */
        .gradient-text, .gold-gradient-text {
            background: linear-gradient(135deg, #fff3d1 0%, #d4af37 40%, #f3e5ab 70%, #aa820a 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .silver-gradient-text {
            background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #94a3b8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Buttons & CTAs */
        .btn-gold {
            background: linear-gradient(135deg, #f5e6b8 0%, #d4af37 50%, #997b20 100%);
            color: #07080c !important;
            font-weight: 800;
            border: none;
            box-shadow: 0 4px 18px rgba(212, 175, 55, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.5);
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .btn-gold:hover {
            background: linear-gradient(135deg, #fff5d6 0%, #e0bd43 50%, #b08f2a 100%);
            box-shadow: 0 8px 25px rgba(212, 175, 55, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.7);
            transform: translateY(-1.5px);
        }

        .btn-gold-outline {
            border: 1px solid rgba(212, 175, 55, 0.4);
            background: rgba(212, 175, 55, 0.05);
            color: #f5e6b8;
            transition: all 0.2s ease;
        }

        .btn-gold-outline:hover {
            border-color: #d4af37;
            background: rgba(212, 175, 55, 0.16);
            color: #ffffff;
            box-shadow: 0 0 15px rgba(212, 175, 55, 0.2);
        }

        /* Product Gallery Zoom */
        .zoom-container { overflow: hidden; position: relative; }
        .zoom-image { transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
        .zoom-container:hover .zoom-image { transform: scale(1.28); }

        /* Subtle Gold Shimmer Animation */
        @keyframes goldShimmer {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
        .shimmer-gold {
            background: linear-gradient(90deg, rgba(212,175,55,0) 0%, rgba(212,175,55,0.18) 50%, rgba(212,175,55,0) 100%);
            background-size: 200% 100%;
            animation: goldShimmer 3.5s infinite;
        }
    </style>'''

html = html[:idx_style_start] + new_style_block + html[idx_style_end:]
print("Updated CSS with bespoke luxury textures & animations")

# 4. Update Top Announcement Bar
old_top_bar = '''<div class="bg-gradient-to-r from-blue-950 via-slate-900 to-indigo-950 text-[11px] text-slate-300 py-1.5 px-4 border-b border-white/5">'''
new_top_bar = '''<div class="bg-gradient-to-r from-black via-slate-950 to-black text-[11px] text-amber-200/80 py-1.5 px-4 border-b border-amber-500/20 shadow-sm tracking-wide">'''

if old_top_bar in html:
    html = html.replace(old_top_bar, new_top_bar)
    print("Updated Top Announcement Bar")
else:
    print("Warning: old_top_bar not matched")

# 5. Update Sticky Header background and styling
old_header = '''<header class="sticky top-0 z-40 bg-slate-900/90 backdrop-blur-md border-b border-white/10 transition-all duration-300">'''
new_header = '''<header class="sticky top-0 z-40 bg-[#090b10]/95 backdrop-blur-md border-b border-amber-500/20 transition-all duration-300 shadow-xl shadow-black/40">'''

if old_header in html:
    html = html.replace(old_header, new_header)
    print("Updated Sticky Header styling")
else:
    print("Warning: old_header not matched")

# 6. Update Mega Menu Bar styling
old_megamenu = '''<nav class="bg-slate-950/80 border-b border-white/5 px-4 lg:px-8 py-2.5 overflow-x-auto scrollbar-none">'''
new_megamenu = '''<nav class="bg-[#0b0d13] border-b border-white/5 px-4 lg:px-8 py-2.5 overflow-x-auto scrollbar-none">'''

if old_megamenu in html:
    html = html.replace(old_megamenu, new_megamenu)
    print("Updated Mega Menu Bar")

# 7. Update Hero Slides with high-end editorial luxury campaigns
old_slide_1 = '''<div id="hero-slide-1" class="hero-slide absolute inset-0 flex flex-col md:flex-row items-center justify-between p-8 md:p-14 bg-gradient-to-r from-slate-950 via-slate-900/90 to-blue-950/70 transition-opacity duration-700 opacity-100">
                            <div class="max-w-xl z-10 space-y-4">
                                <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-400 text-xs font-semibold">
                                    <i data-lucide="sparkles" class="w-3.5 h-3.5"></i> The Next Generation Marketplace
                                </div>
                                <h1 class="text-3xl sm:text-4xl md:text-6xl font-black font-display tracking-tight text-white leading-tight">
                                    WELCOME TO <br>
                                    <span class="gradient-text">NEXT VISION BRAND</span>
                                </h1>
                                <p class="text-slate-300 text-base md:text-lg font-light leading-relaxed">
                                    "Your Next Vision of Shopping." Discover cutting-edge tech, bespoke fashion, gourmet provisions, and smart home appliances.
                                </p>
                                <div class="flex flex-wrap items-center gap-4 pt-2">
                                    <button onclick="navigate('shop')" class="px-8 py-3.5 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-bold text-sm shadow-lg shadow-blue-500/30 transition transform hover:-translate-y-0.5">
                                        Explore Collection
                                    </button>
                                    <button onclick="navigate('deals')" class="px-8 py-3.5 rounded-xl bg-white/10 hover:bg-white/15 text-white font-semibold text-sm border border-white/20 transition">
                                        Today's Vault Deals
                                    </button>
                                </div>
                            </div>
                            <div class="relative mt-8 md:mt-0 flex-1 flex justify-center">
                                <img src="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80" alt="Flagship Tech" class="max-h-72 md:max-h-96 object-contain drop-shadow-2xl hover:scale-105 transition duration-500">
                            </div>
                        </div>'''

new_slide_1 = '''<div id="hero-slide-1" class="hero-slide absolute inset-0 flex flex-col md:flex-row items-center justify-between p-8 md:p-14 bg-gradient-to-r from-[#07080c] via-[#0e1017]/95 to-[#161a25]/80 transition-opacity duration-700 opacity-100">
                            <div class="max-w-xl z-10 space-y-4">
                                <div class="inline-flex items-center gap-2 px-3.5 py-1.2 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-mono tracking-widest uppercase">
                                    <i data-lucide="crown" class="w-3.5 h-3.5 text-amber-400"></i> The Autumn Vision Atelier
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
                                    <div class="absolute -inset-4 bg-gradient-to-tr from-amber-500/20 to-transparent rounded-full blur-2xl opacity-60"></div>
                                    <img src="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80" alt="Flagship Tech" class="relative max-h-72 md:max-h-96 object-contain drop-shadow-2xl hover:scale-105 transition duration-500">
                                </div>
                            </div>
                        </div>'''

if old_slide_1 in html:
    html = html.replace(old_slide_1, new_slide_1)
    print("Updated Hero Slide 1 to Luxury Campaign")
else:
    print("Warning: old_slide_1 not matched")

# 8. Update renderProductCard function with Luxury Showroom Card aesthetic
old_card_js = '''function renderProductCard(p, isFlash = false) {
            const isWished = appState.wishlist.some(w => w.product_id === p.id);
            const isCompared = appState.compareList.includes(p.id);
            const discPill = p.discount > 0 ? `<span class="bg-rose-500 text-white font-bold text-[10px] px-2 py-0.5 rounded-full">${p.discount}% OFF</span>` : '';
            const flashProgress = isFlash ? `
                <div class="mt-2 space-y-1">
                    <div class="flex justify-between text-[10px] text-slate-400 font-medium">
                        <span>Sold: ${p.flash_sold || 35}</span>
                        <span class="text-rose-400 font-semibold">Only ${Math.max(1, p.flash_stock_limit - (p.flash_sold || 0))} Left!</span>
                    </div>
                    <div class="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                        <div class="bg-gradient-to-r from-rose-500 to-amber-400 h-1.5 rounded-full" style="width: ${Math.min(100, Math.round(((p.flash_sold || 35) / p.flash_stock_limit) * 100))}%"></div>
                    </div>
                </div>
            ` : '';

            return `
            <div class="glass-card rounded-2xl p-4 flex flex-col justify-between group relative border border-white/5 bg-slate-900/60">
                <div class="relative">
                    <div class="aspect-square rounded-xl overflow-hidden bg-slate-950 flex items-center justify-center p-3 relative cursor-pointer" onclick="openProductDetail('${p.id}')">
                        <img src="${p.images[0]}" alt="${p.title}" class="max-h-full max-w-full object-contain group-hover:scale-105 transition duration-300">
                    </div>
                    <div class="absolute top-2 left-2 flex flex-col gap-1">
                        ${discPill}
                        ${p.is_flash_sale ? '<span class="bg-amber-500 text-slate-950 font-black text-[9px] px-1.5 py-0.5 rounded uppercase">Flash</span>' : ''}
                    </div>
                    <button onclick="event.stopPropagation(); toggleWishlist('${p.id}')" class="absolute top-2 right-2 p-2 rounded-xl bg-slate-900/80 hover:bg-slate-800 text-slate-300 hover:text-rose-500 transition ${isWished ? 'text-rose-500' : ''}">
                        <i data-lucide="heart" class="w-4 h-4 ${isWished ? 'fill-current text-rose-500' : ''}"></i>
                    </button>
                </div>

                <div class="mt-4 flex-1 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between text-xs text-slate-400 mb-1">
                            <span class="font-medium">${p.brand}</span>
                            <span class="flex items-center gap-1 text-amber-400 font-semibold"><i data-lucide="star" class="w-3 h-3 fill-current"></i> ${p.rating}</span>
                        </div>
                        <h3 class="font-bold text-white text-sm line-clamp-2 hover:text-blue-400 cursor-pointer transition mb-2" onclick="openProductDetail('${p.id}')">${p.title}</h3>
                    </div>

                    ${flashProgress}

                    <div class="mt-3 pt-3 border-t border-white/5 flex items-center justify-between">
                        <div>
                            <div class="flex items-baseline gap-2">
                                <span class="text-lg font-black text-white font-mono">₹${p.price.toLocaleString('en-IN')}</span>
                                ${p.mrp > p.price ? `<span class="text-xs text-slate-500 line-through font-mono">₹${p.mrp.toLocaleString('en-IN')}</span>` : ''}
                            </div>
                        </div>
                        <div class="flex items-center gap-2">
                            <button onclick="event.stopPropagation(); toggleCompare('${p.id}')" class="p-2 rounded-xl border border-white/10 hover:border-blue-500 text-slate-400 hover:text-white transition ${isCompared ? 'bg-blue-600 text-white border-blue-500' : 'bg-slate-800/80'}" title="Compare">
                                <i data-lucide="repeat" class="w-4 h-4"></i>
                            </button>
                            <button onclick="event.stopPropagation(); addToCart('${p.id}')" class="p-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold transition shadow-md shadow-blue-500/20" title="Add to Cart">
                                <i data-lucide="shopping-bag" class="w-4 h-4"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            `;
        }'''

new_card_js = '''function renderProductCard(p, isFlash = false) {
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
        }'''

if old_card_js in html:
    html = html.replace(old_card_js, new_card_js)
    print("Replaced renderProductCard with Luxury Showroom Card")
else:
    print("Warning: old_card_js not matched")

# 9. Update AI Assistant to "NVB Client Concierge" (Bespoke personal shopper)
old_ai_modal_header = '''<div class="p-4 bg-gradient-to-r from-purple-900/60 to-blue-900/60 border-b border-white/10 flex items-center justify-between">'''
new_ai_modal_header = '''<div class="p-4 bg-gradient-to-r from-[#0d0f17] via-[#141824] to-[#0d0f17] border-b border-amber-500/20 flex items-center justify-between">'''

if old_ai_modal_header in html:
    html = html.replace(old_ai_modal_header, new_ai_modal_header)
    print("Updated AI Assistant modal header to Luxury Concierge")

old_ai_modal_frame = 'border-purple-500/30'
new_ai_modal_frame = 'border-amber-500/30'
html = html.replace(old_ai_modal_frame, new_ai_modal_frame)

# 10. Update Floating AI Assistant button from purple to metallic gold medallion
old_ai_btn = '''<button onclick="toggleAIAssistant()" class="fixed bottom-6 right-6 p-4 rounded-full bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 text-white shadow-2xl shadow-purple-500/30 hover:scale-110 transition z-40 flex items-center justify-center group">'''
new_ai_btn = '''<button onclick="toggleAIAssistant()" class="fixed bottom-6 right-6 p-3.5 rounded-full bg-gradient-to-tr from-amber-400 via-yellow-300 to-amber-600 text-slate-950 shadow-2xl shadow-amber-500/30 hover:scale-110 transition z-40 flex items-center justify-center group ring-2 ring-amber-400/50" title="NVB Client Concierge">'''

if old_ai_btn in html:
    html = html.replace(old_ai_btn, new_ai_btn)
    print("Updated Floating AI button to gold medallion")

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("transform_design.py applied successfully!")
