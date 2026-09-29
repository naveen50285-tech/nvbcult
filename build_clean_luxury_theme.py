import re

with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update <head> Google Fonts
old_fonts = '''<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">'''
if old_fonts in html:
    html = html.replace(old_fonts, '''<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">''')
    print("Updated Google Fonts")

# 2. Update CSS <style> block to clean luxury retail styling
idx_style_start = html.find('<style>')
idx_style_end = html.find('</style>') + 8

new_style_block = '''<style>
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #f8fafc;
            color: #0f172a;
            min-height: 100vh;
        }

        h1, h2, h3, .font-display {
            font-family: 'Cinzel', serif;
            letter-spacing: 0.02em;
        }

        .font-editorial {
            font-family: 'Playfair Display', serif;
        }

        /* Clean Luxury Scrollbars */
        ::-webkit-scrollbar { width: 7px; height: 7px; }
        ::-webkit-scrollbar-track { background: #f1f5f9; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

        /* Real Human-Designed Luxury Card Surfaces (Not Generic AI Dark Glass) */
        .glass-panel {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 1.25rem;
            box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05);
        }

        .glass-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 1rem;
            box-shadow: 0 2px 8px -2px rgba(0, 0, 0, 0.04), 0 1px 3px rgba(0, 0, 0, 0.02);
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .glass-card:hover {
            transform: translateY(-3px);
            border-color: rgba(212, 175, 55, 0.5);
            box-shadow: 0 14px 30px -4px rgba(0, 0, 0, 0.08), 0 0 1px rgba(212, 175, 55, 0.3);
        }

        /* Luxury Metallic Gradients */
        .gradient-text, .gold-gradient-text {
            background: linear-gradient(135deg, #1e293b 0%, #b48c26 50%, #d4af37 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Primary CTAs */
        .btn-gold {
            background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%);
            color: #ffffff !important;
            font-weight: 700;
            border: none;
            box-shadow: 0 4px 14px rgba(184, 134, 11, 0.25);
            transition: all 0.2s ease;
        }

        .btn-gold:hover {
            background: linear-gradient(135deg, #e5c07b 0%, #c59b27 100%);
            box-shadow: 0 6px 20px rgba(184, 134, 11, 0.35);
            transform: translateY(-1px);
        }

        .btn-black {
            background: #0f172a;
            color: #ffffff;
            font-weight: 700;
            transition: all 0.2s ease;
        }

        .btn-black:hover {
            background: #000000;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
            transform: translateY(-1px);
        }

        /* Product Gallery Zoom */
        .zoom-container { overflow: hidden; position: relative; }
        .zoom-image { transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
        .zoom-container:hover .zoom-image { transform: scale(1.25); }
    </style>'''

if idx_style_start != -1 and idx_style_end != -1:
    html = html[:idx_style_start] + new_style_block + html[idx_style_end:]
    print("Replaced CSS style block with Clean Luxury Retail styles")

# 3. Update renderProductCard JS to output pristine showroom cards
idx_rpc = html.find('function renderProductCard')
idx_home = html.find('function renderHome()', idx_rpc)

new_render_card = '''function renderProductCard(p, isFlash = false) {
            const isWished = appState.wishlist.some(w => w.product_id === p.id);
            const isCompared = appState.compareList.includes(p.id);
            const discPill = p.discount > 0 ? `<span class="bg-rose-50 text-rose-700 border border-rose-200 font-mono font-bold text-[10px] px-2 py-0.5 rounded-full tracking-wider uppercase">${p.discount}% OFF</span>` : '';
            const flashProgress = isFlash ? `
                <div class="mt-2.5 space-y-1">
                    <div class="flex justify-between text-[11px] text-slate-500 font-medium">
                        <span>Sold: ${p.flash_sold || 35}</span>
                        <span class="text-amber-700 font-bold font-mono">Only ${Math.max(1, p.flash_stock_limit - (p.flash_sold || 0))} Left!</span>
                    </div>
                    <div class="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden border border-slate-200">
                        <div class="bg-gradient-to-r from-amber-500 to-amber-600 h-1.5 rounded-full" style="width: ${Math.min(100, Math.round(((p.flash_sold || 35) / p.flash_stock_limit) * 100))}%"></div>
                    </div>
                </div>
            ` : '';

            const imgUrl = (p.images && p.images.length > 0) ? p.images[0] : (p.image_url || 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800');

            return `
            <div class="glass-card p-4 flex flex-col justify-between group relative bg-white">
                <div class="relative">
                    <div class="aspect-square rounded-xl overflow-hidden bg-slate-50 border border-slate-100 flex items-center justify-center p-3 relative cursor-pointer group-hover:bg-amber-50/20 transition duration-300" onclick="openProductDetail('${p.id}')">
                        <img src="${imgUrl}" alt="${p.title}" class="max-h-full max-w-full object-contain group-hover:scale-105 transition duration-500">
                    </div>
                    <div class="absolute top-2 left-2 flex flex-col gap-1.5">
                        ${discPill}
                        ${p.is_flash_sale ? '<span class="bg-amber-100 text-amber-900 border border-amber-300 font-mono font-bold text-[9px] px-2 py-0.5 rounded-full uppercase tracking-wider">VAULT DEAL</span>' : ''}
                    </div>
                    <button onclick="event.stopPropagation(); toggleWishlist('${p.id}')" class="absolute top-2 right-2 p-2 rounded-xl bg-white/90 backdrop-blur-md border border-slate-200 text-slate-400 hover:text-rose-500 shadow-sm transition ${isWished ? 'text-rose-500 border-rose-300' : ''}">
                        <i data-lucide="heart" class="w-4 h-4 ${isWished ? 'fill-current text-rose-500' : ''}"></i>
                    </button>
                </div>

                <div class="mt-4 flex-1 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between text-xs text-slate-500 mb-1">
                            <span class="font-mono text-[10px] text-amber-700 uppercase tracking-widest font-bold">${p.brand || 'NEXT VISION'}</span>
                            <span class="flex items-center gap-1 text-amber-600 font-bold font-mono text-xs"><i data-lucide="star" class="w-3.5 h-3.5 fill-current text-amber-400"></i> ${p.rating}</span>
                        </div>
                        <h3 class="font-bold text-slate-900 text-sm line-clamp-2 hover:text-amber-700 cursor-pointer transition mb-2" onclick="openProductDetail('${p.id}')">${p.title}</h3>
                    </div>

                    ${flashProgress}

                    <div class="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between">
                        <div>
                            <div class="flex items-baseline gap-2">
                                <span class="text-lg font-black text-slate-950 font-mono">₹${p.price.toLocaleString('en-IN')}</span>
                                ${p.mrp > p.price ? `<span class="text-xs text-slate-400 line-through font-mono">₹${p.mrp.toLocaleString('en-IN')}</span>` : ''}
                            </div>
                        </div>
                        <div class="flex items-center gap-1.5">
                            <button onclick="event.stopPropagation(); toggleCompare('${p.id}')" class="p-2 rounded-xl border border-slate-200 hover:border-slate-400 text-slate-500 hover:text-slate-900 bg-slate-50 transition ${isCompared ? 'bg-amber-100 text-amber-900 font-bold border-amber-300' : ''}" title="Compare">
                                <i data-lucide="repeat" class="w-4 h-4"></i>
                            </button>
                            <button onclick="event.stopPropagation(); addToCart('${p.id}')" class="p-2.5 rounded-xl btn-black text-white transition shadow-sm" title="Add to Bag">
                                <i data-lucide="shopping-bag" class="w-4 h-4"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            `;
        }\n\n        '''

if idx_rpc != -1 and idx_home != -1:
    html = html[:idx_rpc] + new_render_card + html[idx_home:]
    print("Replaced renderProductCard with Clean Showroom Cards")

# 4. Update the Mega Menu styling to clean high-end retail navigation
html = html.replace('bg-slate-950/80 border-b border-white/5', 'bg-white border-b border-slate-200 text-slate-800 shadow-sm')
html = html.replace('bg-[#0b0d13] border-b border-white/5', 'bg-white border-b border-slate-200 text-slate-800 shadow-sm')

# 5. Update Header background to Deep Obsidian with Gold Hairline
html = re.sub(r'<header class="sticky top-0 z-40 bg-[^"]+">', '<header class="sticky top-0 z-40 bg-[#0a0b10] border-b border-[#d4af37]/30 shadow-xl">', html)

# 6. Update Top Announcement Bar
html = re.sub(r'<div class="bg-gradient-to-r from-[^"]+ py-1.5 px-4[^"]*">', '<div class="bg-[#050608] text-amber-200/90 py-1.5 px-4 border-b border-[#d4af37]/20 text-[11px] font-medium tracking-wide">', html)

# 7. Update Home Section wrapper from dark background to clean luxury canvas
html = html.replace('bg-gradient-to-b from-slate-950 to-nvb-dark border-b border-white/5', 'bg-slate-950 border-b border-slate-900')
html = html.replace('bg-slate-900/80 min-h-[380px]', 'bg-[#0c0e14] min-h-[380px]')

# 8. Update Hero Slide 1 to high-fashion editorial campaign
old_slide1_marker = '<div id="hero-slide-1"'
idx_s1 = html.find(old_slide1_marker)
if idx_s1 != -1:
    idx_s1_end = html.find('<div id="hero-slide-2"', idx_s1)
    new_s1_html = '''<div id="hero-slide-1" class="hero-slide absolute inset-0 flex flex-col md:flex-row items-center justify-between p-8 md:p-14 bg-gradient-to-r from-[#07080c] via-[#0d0f17]/95 to-[#161a25]/90 transition-opacity duration-700 opacity-100">
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
                                    <button onclick="navigate('deals')" class="px-7 py-3.5 rounded-xl border border-white/20 hover:border-amber-400 text-white font-semibold text-sm transition">
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
                        </div>\n\n                        '''
    html = html[:idx_s1] + new_s1_html + html[idx_s1_end:]
    print("Replaced Hero Slide 1 with Editorial Campaign")

# 9. Update Slide 2
idx_s2 = html.find('<div id="hero-slide-2"')
if idx_s2 != -1:
    idx_s2_end = html.find('</div>\n                    </div>\n\n                    <!-- Carousel Controls -->', idx_s2)
    if idx_s2_end == -1:
        idx_s2_end = html.find('<!-- Carousel Controls -->', idx_s2)
    if idx_s2_end != -1:
        new_s2_html = '''<div id="hero-slide-2" class="hero-slide absolute inset-0 flex flex-col md:flex-row items-center justify-between p-8 md:p-14 bg-gradient-to-r from-[#07080c] via-[#12141c]/95 to-[#1a1728]/80 transition-opacity duration-700 opacity-0 pointer-events-none">
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
                                    <button onclick="navigate('deals')" class="px-7 py-3.5 rounded-xl border border-white/20 hover:border-amber-400 text-white font-semibold text-sm transition">
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
                        </div>\n                    </div>\n\n                    '''
        # find matching end div
        idx_controls = html.find('<!-- Carousel Controls -->', idx_s2)
        html = html[:idx_s2] + new_s2_html + html[idx_controls:]
        print("Replaced Hero Slide 2 with Editorial Campaign")

# 10. Update Section Titles and Badges
html = html.replace('text-cyan-400', 'text-amber-700')
html = html.replace('border-cyan-500/30', 'border-amber-500/30')
html = html.replace('border-cyan-500', 'border-amber-500')

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("build_clean_luxury_theme.py finished successfully!")
