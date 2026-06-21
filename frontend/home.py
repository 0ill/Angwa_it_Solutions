def get_home_html():
    return """
<!-- ==================== PAGE: HOME ==================== -->
<div id="page-home" class="page-view">

<!-- Hero Content -->
<section id="home-hero" class="relative bg-brand-black text-white overflow-hidden py-20 lg:py-28">
    <div class="absolute inset-0 pointer-events-none opacity-20">
        <div class="absolute -top-20 left-10 w-96 h-96 bg-brand-gold rounded-full filter blur-[120px] animate-pulse"></div>
        <div class="absolute -bottom-20 right-10 w-[500px] h-[500px] bg-brand-green rounded-full filter blur-[150px]"></div>
    </div>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div class="grid lg:grid-cols-12 gap-16 items-center">
            <div class="lg:col-span-7 space-y-6 text-center lg:text-left">
                <div class="inline-flex items-center gap-2 bg-white/5 border border-white/10 px-4 py-2 rounded-full text-brand-gold text-xs font-medium tracking-widest uppercase">
                    <span class="flex h-2 w-2 relative"><span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-green opacity-75"></span><span class="relative inline-flex rounded-full h-2 w-2 bg-brand-green"></span></span>Symmetrical Fiber Optic Grid
                </div>
                <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold leading-tight tracking-tight text-white">Symmetrical Speed. <br class="hidden sm:block"><span class="text-transparent bg-clip-text bg-gradient-to-r from-brand-gold via-brand-goldLight to-brand-goldDark">Pure Gloss Finish.</span></h1>
                <p class="text-base sm:text-lg text-gray-400 max-w-2xl mx-auto lg:mx-0 leading-relaxed">Say goodbye to standard copper lag. ANGWA's fiber lines deliver pure light-based throughput straight to your smart environment. No buffering. No capacity restrictions. No contracts.</p>
                <div class="grid grid-cols-3 gap-6 pt-6 max-w-lg mx-auto lg:mx-0 border-t border-white/10">
                    <div><div class="text-2xl sm:text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-b from-white to-gray-400">99.99%</div><div class="text-xs text-gray-500 uppercase tracking-wider font-semibold mt-1">Uptime SLA</div></div>
                    <div><div class="text-2xl sm:text-3xl font-extrabold text-brand-gold">0</div><div class="text-xs text-gray-500 uppercase tracking-wider font-semibold mt-1">Caps or Limits</div></div>
                    <div><div class="text-2xl sm:text-3xl font-extrabold text-brand-green">24/7</div><div class="text-xs text-gray-500 uppercase tracking-wider font-semibold mt-1">Dedicated Care</div></div>
                </div>
            </div>
            <div id="coverage" class="lg:col-span-5">
                <div class="glass-dark p-8 rounded-3xl shadow-2xl relative gold-sheen-border overflow-hidden sheen-effect">
                    <div class="absolute -top-3 -right-3 bg-gradient-to-r from-brand-gold via-brand-goldLight to-brand-goldDark text-brand-black text-[9px] uppercase font-black px-3.5 py-1.5 rounded-full tracking-wider shadow-md">Ultra Symmetrical</div>
                    <h3 class="text-xl font-bold tracking-tight text-white mb-2">Check Fibre Availability</h3>
                    <p class="text-xs text-gray-400 mb-6 leading-relaxed">Instantly verify speed potentials and provider availability for your complex or neighborhood.</p>
                    <div class="space-y-4">
                        <div class="relative">
                            <label class="block text-[10px] font-bold uppercase tracking-wider text-gray-400 mb-1.5">Suburb or Street Location</label>
                            <div class="relative">
                                <input type="text" id="area-search" placeholder="e.g. Sandton, Sea Point, Hatfield..." class="w-full px-4 py-3 pl-11 bg-brand-slateBlack border border-white/10 rounded-2xl text-white focus:outline-none focus:ring-2 focus:ring-brand-gold focus:border-transparent transition-all font-semibold placeholder-gray-500 text-sm">
                                <i class="fa-solid fa-compass absolute left-4 top-4 text-brand-gold"></i>
                            </div>
                            <div id="search-dropdown" class="hidden absolute left-0 right-0 mt-1 bg-brand-darkGray border border-white/10 rounded-2xl shadow-xl z-50 overflow-hidden text-sm"></div>
                        </div>
                        <button onclick="triggerSearch()" class="w-full py-3.5 glossy-green text-white font-bold rounded-2xl transition-all flex items-center justify-center gap-3"><i class="fa-solid fa-magnifying-glass"></i><span>Analyze Location Status</span></button>
                    </div>
                    <div id="search-result" class="hidden mt-6 p-4 rounded-2xl border transition-all duration-300"></div>
                    <div class="mt-4 flex items-center justify-center gap-2 text-[11px] text-gray-500"><i class="fa-solid fa-shield-halved text-brand-gold"></i><span>Secured light-speed database connection</span></div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Partners Logo Marquee -->
<section class="py-8 bg-brand-slateBlack border-b border-white/10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h4 class="text-[10px] uppercase tracking-widest font-bold text-gray-500 mb-4">Official Infrastructure Carrier Integrations</h4>
        <div class="flex flex-wrap items-center justify-center gap-4 md:gap-10 opacity-90">
            <div class="flex items-center gap-2 bg-white/5 px-4 py-2 rounded-full border border-white/5 font-semibold text-xs text-gray-300 hover:border-brand-gold/30 transition-all cursor-pointer"><span class="h-2 w-2 rounded-full bg-brand-gold shadow-[0_0_8px_#D4AF37]"></span> Vumatel</div>
            <div class="flex items-center gap-2 bg-white/5 px-4 py-2 rounded-full border border-white/5 font-semibold text-xs text-gray-300 hover:border-brand-gold/30 transition-all cursor-pointer"><span class="h-2 w-2 rounded-full bg-brand-green shadow-[0_0_8px_#30D158]"></span> Openserve</div>
            <div class="flex items-center gap-2 bg-white/5 px-4 py-2 rounded-full border border-white/5 font-semibold text-xs text-gray-300 hover:border-brand-gold/30 transition-all cursor-pointer"><span class="h-2 w-2 rounded-full bg-brand-gold shadow-[0_0_8px_#D4AF37]"></span> Frogfoot</div>
            <div class="flex items-center gap-2 bg-white/5 px-4 py-2 rounded-full border border-white/5 font-semibold text-xs text-gray-300 hover:border-brand-gold/30 transition-all cursor-pointer"><span class="h-2 w-2 rounded-full bg-white shadow-[0_0_8px_#FFFFFF]"></span> MetroFibre</div>
        </div>
    </div>
</section>

<!-- "Who We Are" Core Promise Section -->
<section id="why-angwa" class="py-24 bg-white border-b border-gray-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-3xl mx-auto mb-20 space-y-4">
            <span class="text-brand-goldDark uppercase font-black tracking-widest text-xs px-3.5 py-1 bg-brand-gold/10 rounded-full">Who We Are</span>
            <h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-brand-black">Premium Quality. Month-to-Month Freedom.</h2>
            <p class="text-gray-500 text-sm">Unlike standard operators, we operate on a flexible framework. No strict long contracts, no setup charges, and direct refund guarantees.</p>
        </div>
        <div class="grid md:grid-cols-3 gap-8">
            <div class="bg-brand-lightBg p-8 rounded-3xl hover:-translate-y-1 transition-all duration-300 border border-black/5 flex flex-col justify-between">
                <div class="space-y-4"><div class="h-12 w-12 bg-brand-gold/10 text-brand-goldDark rounded-2xl flex items-center justify-center text-xl shadow-inner"><i class="fa-solid fa-server"></i></div><h3 class="text-lg font-bold text-brand-black tracking-tight">Premium High-Performance Hosting</h3><p class="text-xs text-gray-500 leading-relaxed">Blazing-fast cloud hosting infrastructure optimized for instant page loading, robust security, and deep integration with our ultra-low-latency light grid network.</p></div>
                <button onclick="showPage('host')" class="pt-6 text-[10px] font-black uppercase tracking-wider text-brand-goldDark text-left">Explore Hosting Tech <i class="fa-solid fa-chevron-right ml-1"></i></button>
            </div>
            <div class="bg-brand-lightBg p-8 rounded-3xl hover:-translate-y-1 transition-all duration-300 border border-black/5 flex flex-col justify-between">
                <div class="space-y-4"><div class="h-12 w-12 bg-brand-green/10 text-brand-greenDark rounded-2xl flex items-center justify-center text-xl shadow-inner"><i class="fa-solid fa-wand-magic-sparkles"></i></div><h3 class="text-lg font-bold text-brand-black tracking-tight">Custom Responsive Designing</h3><p class="text-xs text-gray-500 leading-relaxed">Tailor-made, pixel-perfect user interfaces engineered for speed, conversion, and fluid grid layouts. Watch your concepts turn into high-score SEO assets seamlessly.</p></div>
                <button onclick="showPage('design')" class="pt-6 text-[10px] font-black uppercase tracking-wider text-brand-greenDark text-left">Start Design Blueprint <i class="fa-solid fa-chevron-right ml-1"></i></button>
            </div>
            <div class="bg-brand-lightBg p-8 rounded-3xl hover:-translate-y-1 transition-all duration-300 border border-black/5 flex flex-col justify-between">
                <div class="space-y-4"><div class="h-12 w-12 bg-black/5 text-brand-black rounded-2xl flex items-center justify-center text-xl shadow-inner"><i class="fa-solid fa-cloud-arrow-up"></i></div><h3 class="text-lg font-bold text-brand-black tracking-tight">Secure ANGWA Cloud Storage</h3><p class="text-xs text-gray-500 leading-relaxed">Military-grade encrypted cloud storage powered by our fibre infrastructure. Sync, back up, and access everything at gigabit speeds from SA-based servers.</p></div>
                <button onclick="showPage('cloud')" class="pt-6 text-[10px] font-black uppercase tracking-wider text-brand-black text-left">View Cloud Plans <i class="fa-solid fa-chevron-right ml-1"></i></button>
            </div>
        </div>
    </div>
</section>

<!-- ==================== HOME: SERVICE SUMMARY SECTIONS ==================== -->

<!-- HOST Summary -->
<section class="py-20 bg-white border-t border-black/5">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid lg:grid-cols-2 gap-16 items-center">
            <div class="space-y-6">
                <span class="text-brand-gold uppercase font-black tracking-widest text-xs px-3.5 py-1 bg-brand-gold/10 rounded-full inline-block">Service 01 — Host</span>
                <h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-brand-black">Symmetrical Fibre Packages</h2>
                <p class="text-gray-500 text-sm leading-relaxed">Month-to-month uncapped symmetrical fibre on Vumatel, Openserve, and Frogfoot. No contracts, free Wi-Fi 6 router, and free installation.</p>
                <div class="grid grid-cols-3 gap-4 py-2">
                    <div class="bg-brand-lightBg p-4 rounded-2xl border border-black/5 text-center"><div class="text-xl font-black text-brand-black">R649</div><div class="text-[9px] text-gray-400 uppercase font-bold tracking-wider mt-1">From /pm</div><div class="text-[10px] text-gray-500 mt-1">50 Mbps</div></div>
                    <div class="bg-brand-lightBg p-4 rounded-2xl border gold-sheen-border text-center relative"><div class="absolute -top-2 left-1/2 -translate-x-1/2 bg-brand-gold text-brand-black text-[8px] font-black px-2 py-0.5 rounded-full uppercase tracking-wider whitespace-nowrap">Popular</div><div class="text-xl font-black text-brand-black">R909</div><div class="text-[9px] text-gray-400 uppercase font-bold tracking-wider mt-1">/pm</div><div class="text-[10px] text-gray-500 mt-1">100 Mbps</div></div>
                    <div class="bg-brand-lightBg p-4 rounded-2xl border border-black/5 text-center"><div class="text-xl font-black text-brand-black">R1,689</div><div class="text-[9px] text-gray-400 uppercase font-bold tracking-wider mt-1">/pm</div><div class="text-[10px] text-gray-500 mt-1">1 Gbps</div></div>
                </div>
                <button onclick="showPage('host')" class="glossy-gold text-brand-black px-7 py-3 rounded-full font-bold text-xs tracking-wider uppercase shadow-md inline-flex items-center gap-2">Browse All Packages <i class="fa-solid fa-arrow-right"></i></button>
            </div>
            <div class="bg-brand-slateBlack rounded-3xl p-8 border border-white/10 text-white space-y-5 relative overflow-hidden">
                <div class="absolute top-0 right-0 w-48 h-48 bg-brand-gold/10 rounded-full filter blur-[80px]"></div>
                <h4 class="font-bold text-sm uppercase tracking-widest text-brand-gold">All Packages Include</h4>
                <ul class="space-y-3 text-xs text-gray-300 relative z-10">
                    <li class="flex items-center gap-3"><i class="fa-solid fa-circle-check text-brand-green"></i> Uncapped & unshaped pure symmetrical bandwidth</li>
                    <li class="flex items-center gap-3"><i class="fa-solid fa-circle-check text-brand-green"></i> Free Wi-Fi 6 pre-configured router included</li>
                    <li class="flex items-center gap-3"><i class="fa-solid fa-circle-check text-brand-green"></i> Free professional installation & SLA coverage</li>
                    <li class="flex items-center gap-3"><i class="fa-solid fa-circle-check text-brand-green"></i> 30-day double money-back guarantee</li>
                    <li class="flex items-center gap-3"><i class="fa-solid fa-circle-check text-brand-green"></i> Zero contracts — cancel any month</li>
                    <li class="flex items-center gap-3"><i class="fa-solid fa-circle-check text-brand-green"></i> 99.99% uptime SLA commitment</li>
                </ul>
            </div>
        </div>
    </div>
</section>

<!-- DESIGN Summary -->
<section class="py-20 bg-brand-slateBlack text-white border-t border-white/10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid lg:grid-cols-2 gap-16 items-center">
            <div class="order-2 lg:order-1 grid grid-cols-1 gap-4">
                <div class="bg-brand-darkGray/60 border border-brand-gold/20 p-5 rounded-2xl flex items-start gap-4"><div class="h-10 w-10 bg-brand-gold/15 rounded-xl flex items-center justify-center text-brand-gold shrink-0"><i class="fa-solid fa-gem"></i></div><div><div class="font-bold text-sm text-white">Luxe Obsidian</div><div class="text-xs text-gray-400 mt-1">Ultra-premium dark luxury theme. 10 pages, 99 Speed Index.</div><div class="text-brand-gold font-black text-sm mt-2">R11,699 <span class="text-gray-500 font-normal text-[10px]">once-off</span></div></div></div>
                <div class="bg-brand-darkGray/60 border border-brand-green/20 p-5 rounded-2xl flex items-start gap-4"><div class="h-10 w-10 bg-brand-green/15 rounded-xl flex items-center justify-center text-brand-green shrink-0"><i class="fa-solid fa-bolt"></i></div><div><div class="font-bold text-sm text-white">Emerald Neo</div><div class="text-xs text-gray-400 mt-1">High-tech neon layout. 5 pages, clean coded.</div><div class="text-brand-green font-black text-sm mt-2">R7,149 <span class="text-gray-500 font-normal text-[10px]">once-off</span></div></div></div>
                <div class="bg-brand-darkGray/60 border border-white/10 p-5 rounded-2xl flex items-start gap-4"><div class="h-10 w-10 bg-white/10 rounded-xl flex items-center justify-center text-white shrink-0"><i class="fa-solid fa-seedling"></i></div><div><div class="font-bold text-sm text-white">Minimal Alabaster</div><div class="text-xs text-gray-400 mt-1">Ultra-clean light theme. 3 pages, fluid grid.</div><div class="text-white font-black text-sm mt-2">R5,199 <span class="text-gray-500 font-normal text-[10px]">once-off</span></div></div></div>
            </div>
            <div class="order-1 lg:order-2 space-y-6">
                <span class="text-brand-green uppercase font-black tracking-widest text-xs px-3.5 py-1 bg-brand-green/10 rounded-full inline-block">Service 02 — Design</span>
                <h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight">Custom Web Design Packages</h2>
                <p class="text-gray-400 text-sm leading-relaxed">Hand-coded, pixel-perfect websites with 99/100 performance scores. From luxury dark themes to clean minimal layouts — every design is SEO-optimized and mobile-first.</p>
                <button onclick="showPage('design')" class="glossy-green text-white px-7 py-3 rounded-full font-bold text-xs tracking-wider uppercase shadow-md inline-flex items-center gap-2">Explore Design Suite <i class="fa-solid fa-arrow-right"></i></button>
            </div>
        </div>
    </div>
</section>

<!-- CLOUD Summary -->
<section class="py-20 bg-brand-lightBg border-t border-black/5">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid lg:grid-cols-2 gap-16 items-center">
            <div class="space-y-6">
                <span class="text-brand-goldDark uppercase font-black tracking-widest text-xs px-3.5 py-1 bg-brand-gold/10 rounded-full inline-block">Service 03 — Cloud</span>
                <h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-brand-black">ANGWA Cloud Vault Storage</h2>
                <p class="text-gray-500 text-sm leading-relaxed">Military-grade AES-256 encrypted cloud storage, hosted on South African servers and powered by our symmetrical fibre backbone. Sync at full gigabit speed with zero throttling.</p>
                <div class="grid grid-cols-2 gap-4">
                    <div class="bg-white p-4 rounded-2xl border border-black/5 shadow-sm"><i class="fa-solid fa-cloud-arrow-up text-brand-gold mb-2"></i><div class="font-black text-brand-black text-base">100 GB</div><div class="text-[9px] text-gray-400 uppercase font-bold">Starter — R103/pm</div></div>
                    <div class="bg-white p-4 rounded-2xl gold-sheen-border shadow-sm relative"><div class="absolute -top-2 left-3 bg-brand-gold text-brand-black text-[8px] font-black px-2 py-0.5 rounded-full uppercase tracking-wider">Popular</div><i class="fa-solid fa-cloud-bolt text-brand-gold mb-2"></i><div class="font-black text-brand-black text-base">500 GB</div><div class="text-[9px] text-gray-400 uppercase font-bold">Pro — R259/pm</div></div>
                    <div class="bg-white p-4 rounded-2xl border border-black/5 shadow-sm"><i class="fa-solid fa-database text-brand-gold mb-2"></i><div class="font-black text-brand-black text-base">2 TB</div><div class="text-[9px] text-gray-400 uppercase font-bold">Business — R584/pm</div></div>
                    <div class="bg-brand-slateBlack p-4 rounded-2xl border border-white/10 shadow-sm"><i class="fa-solid fa-server text-brand-gold mb-2"></i><div class="font-black text-white text-base">10 TB</div><div class="text-[9px] text-gray-400 uppercase font-bold">Ultra — R1,299/pm</div></div>
                </div>
                <button onclick="showPage('cloud')" class="glossy-gold text-brand-black px-7 py-3 rounded-full font-bold text-xs tracking-wider uppercase shadow-md inline-flex items-center gap-2">View Cloud Plans <i class="fa-solid fa-arrow-right"></i></button>
            </div>
            <div class="bg-brand-slateBlack rounded-3xl p-8 border border-white/10 text-white space-y-5 relative overflow-hidden">
                <div class="absolute bottom-0 right-0 w-48 h-48 bg-brand-gold/10 rounded-full filter blur-[80px]"></div>
                <h4 class="font-bold text-sm uppercase tracking-widest text-brand-gold">Every Vault Includes</h4>
                <ul class="space-y-3 text-xs text-gray-300 relative z-10">
                    <li class="flex items-center gap-3"><i class="fa-solid fa-shield-halved text-brand-green"></i> AES-256 military-grade encryption</li>
                    <li class="flex items-center gap-3"><i class="fa-solid fa-bolt text-brand-green"></i> Full gigabit upload/download speeds</li>
                    <li class="flex items-center gap-3"><i class="fa-solid fa-rotate text-brand-green"></i> Automatic background backup</li>
                    <li class="flex items-center gap-3"><i class="fa-solid fa-server text-brand-green"></i> SA-based server infrastructure</li>
                    <li class="flex items-center gap-3"><i class="fa-solid fa-mobile-screen text-brand-green"></i> Cross-device sync (desktop, mobile, tablet)</li>
                    <li class="flex items-center gap-3"><i class="fa-solid fa-clock-rotate-left text-brand-green"></i> Version history & file recovery</li>
                </ul>
            </div>
        </div>
    </div>
</section>

</div><!-- END page-home -->
"""
