with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Header replacement
header_old = '''<!-- Logo -->
                <a href="#home" onclick="navigate('home')" class="flex items-center gap-3 group focus:outline-none flex-shrink-0">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-cyan-400 flex items-center justify-center shadow-lg shadow-blue-500/25 group-hover:scale-105 transition">
                        <svg class="w-6 h-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
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

header_new = '''<!-- Logo -->
                <a href="#home" onclick="navigate('home')" class="flex items-center gap-3.5 group focus:outline-none flex-shrink-0">
                    <div class="relative w-12 h-12 rounded-full p-0.5 bg-gradient-to-tr from-amber-400 via-yellow-300 to-amber-600 shadow-lg shadow-amber-500/25 group-hover:scale-105 group-hover:shadow-amber-500/40 transition-all duration-300 flex-shrink-0">
                        <img src="/static/nvb-logo.png" alt="Next Vision Brand Logo" class="w-full h-full rounded-full object-cover bg-black" />
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

if header_old in html:
    html = html.replace(header_old, header_new)
    print("Replaced Header Logo!")
else:
    print("Warning: header_old not found")

# 2. Footer replacement
footer_old = '''<div class="flex items-center gap-2">
                    <div class="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-black text-sm">NVB</div>
                    <span class="font-display font-bold text-white text-lg">NEXT VISION BRAND</span>
                </div>'''

footer_new = '''<div class="flex items-center gap-3">
                    <div class="w-12 h-12 rounded-full p-0.5 bg-gradient-to-tr from-amber-400 to-amber-600 shadow-md flex-shrink-0">
                        <img src="/static/nvb-logo.png" alt="Next Vision Brand Logo" class="w-full h-full rounded-full object-cover bg-black" />
                    </div>
                    <div>
                        <span class="font-display font-bold text-white text-lg tracking-wider block">NEXT VISION BRAND</span>
                        <p class="text-[10px] text-amber-400 font-mono font-bold tracking-wider uppercase">Dream • Plan • Achieve</p>
                    </div>
                </div>'''

if footer_old in html:
    html = html.replace(footer_old, footer_new)
    print("Replaced Footer Logo!")
else:
    print("Warning: footer_old not found")

# 3. Invoice replacement
inv_old = '''<div class="flex justify-between items-start pb-6 border-b border-slate-200">
                        <div>
                            <h2 class="text-2xl font-black font-display text-slate-900 tracking-wider">NEXT VISION BRAND</h2>
                            <p class="text-xs text-slate-500 font-mono">GSTIN: 29AAAAA0000A1Z5 \u2014 CIN: U72900KA2026PTC099812</p>
                            <p class="text-xs text-slate-500">Official Tax Invoice / Bill of Supply</p>
                        </div>'''

inv_new = '''<div class="flex justify-between items-start pb-6 border-b border-slate-200">
                        <div class="flex items-center gap-3.5">
                            <img src="/static/nvb-logo.png" alt="Next Vision Brand Logo" class="w-14 h-14 rounded-full object-cover border border-amber-500/50 shadow-md" />
                            <div>
                                <h2 class="text-2xl font-black font-display text-slate-900 tracking-wider">NEXT VISION BRAND</h2>
                                <p class="text-[10px] text-amber-600 font-mono font-bold tracking-wider uppercase">Dream \u2022 Plan \u2022 Achieve</p>
                                <p class="text-xs text-slate-500 font-mono">GSTIN: 29AAAAA0000A1Z5 | CIN: U72900KA2026PTC099812</p>
                                <p class="text-xs text-slate-500">Official Tax Invoice / Bill of Supply</p>
                            </div>
                        </div>'''

# Search more loosely if unicode dash differed
idx_inv = html.find('Official Tax Invoice / Bill of Supply')
if idx_inv != -1:
    idx_start = html.rfind('<div class="flex justify-between items-start', 0, idx_inv)
    idx_end = html.find('</div>', idx_inv) + 6
    html = html[:idx_start] + inv_new + html[idx_end:]
    print("Replaced Invoice Logo!")
else:
    print("Warning: invoice section not found")

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("static/index.html successfully updated with official Next Vision Brand logo!")
