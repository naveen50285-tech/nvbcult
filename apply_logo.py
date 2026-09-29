with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add favicon and apple-touch-icon in <head>
if '<link rel="icon"' not in html:
    html = html.replace('<title>', '<link rel="icon" type="image/png" href="/static/favicon.png" />\n    <link rel="apple-touch-icon" href="/static/favicon.png" />\n    <title>')
    print("Added favicon link")

# 2. Update Header Logo
old_header_logo = '''<a href="#home" class="flex items-center gap-3 flex-shrink-0 group">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-cyan-400 flex items-center justify-center text-white shadow-lg shadow-blue-500/20 group-hover:scale-105 transition duration-300">
                        <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
                            <polyline points="2 17 12 22 22 17"></polyline>
                            <polyline points="2 12 12 17 22 12"></polyline>
                        </svg>
                    </div>
                    <div>
                        <span class="font-display font-black text-xl tracking-wider text-white flex items-center gap-1">
                            NEXT VISION <span class="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">NVB</span>
                        </span>
                        <p class="text-[10px] text-slate-400 tracking-widest uppercase font-semibold">Your Next Vision of Shopping</p>
                    </div>
                </a>'''

new_header_logo = '''<a href="#home" class="flex items-center gap-3.5 flex-shrink-0 group">
                    <div class="relative w-12 h-12 rounded-full p-0.5 bg-gradient-to-tr from-amber-400 via-yellow-300 to-amber-600 shadow-lg shadow-amber-500/25 group-hover:scale-105 group-hover:shadow-amber-500/40 transition-all duration-300 flex-shrink-0">
                        <img src="/static/nvb-logo.png" alt="Next Vision Brand" class="w-full h-full rounded-full object-cover bg-black" />
                    </div>
                    <div>
                        <span class="font-display font-black text-xl tracking-wider text-white flex items-center gap-1.5 leading-none">
                            NEXT VISION <span class="bg-gradient-to-r from-amber-400 via-yellow-300 to-amber-200 bg-clip-text text-transparent">BRAND</span>
                        </span>
                        <div class="flex items-center gap-2 mt-1">
                            <p class="text-[9px] text-amber-300/90 font-mono tracking-widest uppercase font-bold">Dream • Plan • Achieve</p>
                            <span class="text-[9px] text-slate-500 hidden sm:inline">|</span>
                            <p class="text-[9px] text-slate-400 tracking-wider font-semibold hidden sm:inline">Your Next Vision of Shopping</p>
                        </div>
                    </div>
                </a>'''

if old_header_logo in html:
    html = html.replace(old_header_logo, new_header_logo)
    print("Replaced Header Logo")
else:
    print("Warning: old_header_logo not matched exactly")

# 3. Update Mobile Drawer Header
old_mobile_logo = '''                <div class="flex items-center justify-between pb-4 border-b border-white/10">
                    <div class="flex items-center gap-2">
                        <div class="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold text-sm">NVB</div>
                        <span class="font-display font-bold text-white text-lg">Menu</span>
                    </div>
                    <button onclick="toggleMobileNav()" class="text-slate-400 hover:text-white"><i data-lucide="x" class="w-6 h-6"></i></button>
                </div>'''

new_mobile_logo = '''                <div class="flex items-center justify-between pb-4 border-b border-white/10">
                    <div class="flex items-center gap-3">
                        <img src="/static/nvb-logo.png" alt="Next Vision Brand" class="w-10 h-10 rounded-full object-cover ring-2 ring-amber-400/50 shadow-md" />
                        <div>
                            <span class="font-display font-bold text-white text-base tracking-wider block">NEXT VISION BRAND</span>
                            <span class="text-[9px] text-amber-300 font-mono uppercase font-bold">Dream • Plan • Achieve</span>
                        </div>
                    </div>
                    <button onclick="toggleMobileNav()" class="text-slate-400 hover:text-white"><i data-lucide="x" class="w-6 h-6"></i></button>
                </div>'''

if old_mobile_logo in html:
    html = html.replace(old_mobile_logo, new_mobile_logo)
    print("Replaced Mobile Drawer Logo")
else:
    print("Warning: old_mobile_logo not matched exactly")

# 4. Update Footer Logo
old_footer_logo = '''                <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-black text-sm">NVB</div>
                    <span class="font-display font-bold text-white text-lg">NEXT VISION BRAND</span>
                </div>'''

new_footer_logo = '''                <div class="flex items-center gap-3">
                    <div class="w-12 h-12 rounded-full p-0.5 bg-gradient-to-tr from-amber-400 to-amber-600 shadow-md flex-shrink-0">
                        <img src="/static/nvb-logo.png" alt="Next Vision Brand" class="w-full h-full rounded-full object-cover bg-black" />
                    </div>
                    <div>
                        <span class="font-display font-bold text-white text-lg tracking-wider block">NEXT VISION BRAND</span>
                        <p class="text-[10px] text-amber-400 font-mono font-bold tracking-wider uppercase">Dream • Plan • Achieve</p>
                    </div>
                </div>'''

if old_footer_logo in html:
    html = html.replace(old_footer_logo, new_footer_logo)
    print("Replaced Footer Logo")
else:
    print("Warning: old_footer_logo not matched exactly")

# 5. Update AI Assistant Modal Avatar
old_ai_avatar = '''            <div class="flex items-center gap-2.5">
                <div class="w-8 h-8 rounded-xl bg-purple-500/30 text-purple-300 flex items-center justify-center border border-purple-500/40">
                    <i data-lucide="bot" class="w-4 h-4"></i>
                </div>
                <div>
                    <h4 class="font-bold text-white text-xs">NVB AI Shopping Assistant</h4>'''

new_ai_avatar = '''            <div class="flex items-center gap-2.5">
                <img src="/static/nvb-logo.png" alt="Next Vision Brand" class="w-8 h-8 rounded-full object-cover ring-1 ring-amber-400/40 shadow-sm flex-shrink-0" />
                <div>
                    <h4 class="font-bold text-white text-xs">Next Vision Brand AI</h4>'''

if old_ai_avatar in html:
    html = html.replace(old_ai_avatar, new_ai_avatar)
    print("Replaced AI Assistant Header Avatar")
else:
    print("Warning: old_ai_avatar not matched exactly")

# 6. Update viewInvoice to render the real logo
old_inv_logo = '''                    <div class="flex justify-between items-start pb-6 border-b border-slate-200">
                        <div>
                            <h2 class="text-2xl font-black font-display text-slate-900">NEXT VISION BRAND</h2>
                            <p class="text-xs text-slate-500">Tax Invoice / Bill of Supply</p>'''

new_inv_logo = '''                    <div class="flex justify-between items-start pb-6 border-b border-slate-200">
                        <div class="flex items-center gap-3">
                            <img src="/static/nvb-logo.png" alt="Next Vision Brand" class="w-12 h-12 rounded-full object-cover border border-amber-500/40 shadow-sm" />
                            <div>
                                <h2 class="text-2xl font-black font-display text-slate-900">NEXT VISION BRAND</h2>
                                <p class="text-[10px] text-amber-600 font-mono font-bold tracking-wider uppercase">Dream • Plan • Achieve</p>
                                <p class="text-xs text-slate-500">Official Tax Invoice / Bill of Supply</p>
                            </div>
                        </div>'''

if old_inv_logo in html:
    html = html.replace(old_inv_logo, new_inv_logo)
    print("Replaced Invoice Logo")
else:
    print("Warning: old_inv_logo not matched exactly")

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("static/index.html updated with official Next Vision Brand logo!")
