def get_design_html():
    return """
<!-- ==================== PAGE: DESIGN ==================== -->
<div id="page-design" class="page-view hidden">

<!-- Design Hero Section -->
<section class="relative bg-brand-lightBg text-brand-black overflow-hidden py-20 border-b border-black/5">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
        <div class="inline-flex items-center gap-2 bg-brand-gold/10 border border-brand-gold/20 px-4 py-2 rounded-full text-brand-goldDark text-xs font-medium tracking-widest uppercase mb-6">Premium Web Design</div>
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight">Bespoke Digital <span class="text-brand-goldDark">Experiences</span></h1>
        <p class="mt-4 text-gray-500 max-w-2xl mx-auto">Hand-coded, performance-optimized websites tailored to your brand. Choose from luxury dark themes, neon tech designs, or clean minimal layouts. Each package includes SEO, responsive fluid grids, and rapid delivery.</p>
        <div class="flex flex-wrap justify-center gap-4 mt-8"><a href="#design-products" class="glossy-gold text-brand-black px-7 py-3 rounded-full font-bold text-xs uppercase tracking-wider shadow-md">Explore Products</a><a href="#why-angwa" class="glossy-black text-white px-7 py-3 rounded-full font-bold text-xs uppercase tracking-wider shadow-md">Learn More</a></div>
    </div>
</section>

<!-- ==================== NEW: OUR PRODUCT RANGE FOR DESIGN ==================== -->
<section id="design-products" class="py-20 bg-brand-lightBg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-3xl mx-auto mb-16 space-y-4">
            <span class="text-brand-goldDark uppercase font-black tracking-widest text-xs px-3.5 py-1 bg-brand-gold/10 rounded-full">Our Product Range</span>
            <h2 class="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-brand-black">Web Design & Development Solutions</h2>
            <p class="text-gray-500 text-sm">Choose from custom-coded designs, eCommerce platforms, or our drag-and-drop site builder. All include responsive layouts, SEO optimization, and fast delivery.</p>
        </div>
        <!-- Design Category Tabs -->
        <div class="flex flex-col items-center gap-6 mb-12">
            <div class="bg-brand-darkGray/5 p-1 rounded-2xl shadow-inner border border-black/5 flex flex-wrap justify-center gap-1 w-full max-w-2xl">
                <button onclick="setDesignCategory('all')" id="design-tab-all" class="design-cat-tab flex-1 px-5 py-2.5 rounded-xl font-bold text-xs tracking-wider uppercase transition-all text-brand-goldDark bg-white shadow-sm">All Products</button>
                <button onclick="setDesignCategory('design')" id="design-tab-design" class="design-cat-tab flex-1 px-5 py-2.5 rounded-xl font-bold text-xs tracking-wider uppercase transition-all text-gray-500 hover:bg-white/50">Design</button>
                <button onclick="setDesignCategory('ecom')" id="design-tab-ecom" class="design-cat-tab flex-1 px-5 py-2.5 rounded-xl font-bold text-xs tracking-wider uppercase transition-all text-gray-500 hover:bg-white/50">Design eCom</button>
                <button onclick="setDesignCategory('sitebuilder')" id="design-tab-sitebuilder" class="design-cat-tab flex-1 px-5 py-2.5 rounded-xl font-bold text-xs tracking-wider uppercase transition-all text-gray-500 hover:bg-white/50">SiteBuilder</button>
            </div>
        </div>
        <!-- Design Products Container -->
        <div id="design-products-container" class="grid sm:grid-cols-2 lg:grid-cols-3 gap-8"></div>
        <div class="mt-16 bg-white border border-black/5 rounded-3xl p-8 shadow-md flex flex-col md:flex-row items-center justify-between gap-6 relative overflow-hidden sheen-effect">
            <div class="flex items-center gap-5 z-10"><div class="h-14 w-14 bg-brand-gold/10 rounded-2xl flex items-center justify-center text-brand-goldDark text-2xl"><i class="fa-solid fa-pen-ruler"></i></div><div><h4 class="text-lg font-bold text-brand-black">Need a custom design?</h4><p class="text-xs text-gray-500">Contact our design team for a fully bespoke website tailored to your exact requirements.</p></div></div>
            <a href="#coverage" class="glossy-gold text-brand-black px-6 py-3 rounded-full font-bold text-xs tracking-wider uppercase shadow-md z-10">Request a Quote</a>
        </div>
    </div>
</section>

<!-- Custom Design Sandbox Suite Section (kept for live preview) -->
<section id="design-suite" class="py-20 bg-brand-slateBlack text-white overflow-hidden relative border-t border-b border-white/10">
    <div class="absolute inset-0 opacity-10 pointer-events-none"><div class="absolute top-0 right-0 w-96 h-96 bg-brand-gold rounded-full filter blur-[120px]"></div><div class="absolute bottom-0 left-10 w-96 h-96 bg-brand-green rounded-full filter blur-[120px]"></div></div>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div class="text-center max-w-3xl mx-auto mb-16 space-y-4">
            <span class="text-brand-gold uppercase font-black tracking-widest text-xs px-3.5 py-1 bg-brand-gold/10 rounded-full">Live Preview Sandbox</span>
            <h2 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight">Interactive Design Mockup</h2>
            <p class="text-gray-400 text-sm">Select any design product below to see a live preview. Customize colors, typography, and layout in real-time.</p>
        </div>
        <div class="grid lg:grid-cols-12 gap-12 items-center">
            <div class="lg:col-span-5 space-y-4">
                <h3 class="text-xl font-bold text-white mb-2">Select Design Tier</h3>
                <p class="text-xs text-gray-400 leading-relaxed mb-6">Every plan is completely hand-coded, SEO optimized, integrated with ultra-fast light hosting, and customizable to your exact requirements.</p>
                <div id="design-selector-cards">
                    <!-- Dynamic design selector cards will be populated by JS -->
                </div>
            </div>
            <div class="lg:col-span-7">
                <div class="bg-brand-darkGray p-3 rounded-3xl border border-white/10 shadow-2xl relative">
                    <div class="flex items-center justify-between px-4 py-2 border-b border-white/5 text-xs text-gray-500"><div class="flex items-center gap-1.5"><span class="h-2.5 w-2.5 rounded-full bg-red-500/80 block"></span><span class="h-2.5 w-2.5 rounded-full bg-yellow-500/80 block"></span><span class="h-2.5 w-2.5 rounded-full bg-green-500/80 block"></span></div><div class="bg-black/40 px-6 py-1 rounded-full text-[10px] tracking-wide text-gray-400 flex items-center gap-1.5 font-mono select-none"><i class="fa-solid fa-lock text-[9px] text-brand-green"></i> https://preview.angwa.design</div><div class="flex items-center gap-3"><button onclick="simulateReload()" class="hover:text-white transition-colors"><i class="fa-solid fa-rotate-right"></i></button><span class="text-[9px] font-bold text-brand-green">Live Sandbox</span></div></div>
                    <div id="live-web-viewport" class="bg-black text-white p-6 sm:p-10 rounded-2xl min-h-[420px] flex flex-col justify-between transition-all duration-500 relative overflow-hidden">
                        <div class="absolute inset-0 pointer-events-none sheen-effect opacity-10"></div>
                        <div class="flex justify-between items-center relative z-10"><span id="mockup-logo" class="text-xs font-black tracking-tight flex items-center gap-1.5 text-brand-gold"><span class="h-5 w-5 bg-gradient-to-r from-brand-gold to-brand-goldDark rounded-md flex items-center justify-center text-brand-black text-[10px]">L</span> <span>OBSIDIAN.</span></span><div class="flex gap-3 text-[9px] font-bold uppercase tracking-wider text-gray-400"><span>Products</span><span>Pricing</span><span>SLA</span></div></div>
                        <div class="my-auto space-y-4 py-8 relative z-10 text-center sm:text-left"><div id="mockup-badge" class="inline-block text-[8px] tracking-widest font-bold uppercase px-2.5 py-1 bg-brand-gold/10 text-brand-gold border border-brand-gold/20 rounded-full">Cinematic Luxury Layout</div><h4 id="mockup-title" class="text-2xl sm:text-3xl font-extrabold text-white leading-tight">Slick. Cinematic.<br><span class="text-brand-gold">Gold Obsidian Accent.</span></h4><p id="mockup-desc" class="text-[11px] text-gray-400 max-w-sm leading-relaxed mx-auto sm:mx-0">Designed with luxury aesthetics. Highly interactive bento architecture mapped for corporate powerbrands and creatives.</p></div>
                        <div class="flex flex-col sm:flex-row items-center justify-between gap-4 border-t border-white/10 pt-5 relative z-10"><div class="text-center sm:text-left"><span class="text-[8px] uppercase tracking-wider text-gray-500 block font-bold">Standard Project Timeline</span><span id="mockup-time" class="text-xs font-bold text-white">4-6 Business Days Delivery</span></div><button id="mockup-btn" class="glossy-gold text-brand-black text-[10px] font-black tracking-wider uppercase px-5 py-2.5 rounded-full shadow-md flex items-center gap-1.5"><span>Explore Blueprint</span> <i class="fa-solid fa-chevron-right text-[8px]"></i></button></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Design Process Section -->
<section class="py-20 bg-brand-lightBg border-t border-black/5">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="text-center max-w-2xl mx-auto mb-12"><span class="text-brand-gold uppercase font-black tracking-widest text-xs bg-brand-gold/10 px-3 py-1 rounded-full">Our Workflow</span><h2 class="text-2xl font-bold mt-2">From Concept to Launch in Days</h2></div><div class="grid md:grid-cols-3 gap-8 text-center"><div><i class="fa-solid fa-pen-ruler text-3xl text-brand-gold mb-3"></i><h3 class="font-bold">Wireframe & Design</h3><p class="text-xs text-gray-500">Collaborative mockups & style tiles.</p></div><div><i class="fa-solid fa-code text-3xl text-brand-gold mb-3"></i><h3 class="font-bold">Hand-Coded Development</h3><p class="text-xs text-gray-500">Pixel-perfect, SEO-optimized frontend.</p></div><div><i class="fa-solid fa-rocket text-3xl text-brand-gold mb-3"></i><h3 class="font-bold">Launch & Support</h3><p class="text-xs text-gray-500">Deployed on high-speed servers plus training.</p></div></div></div>
</section>

</div><!-- END page-design -->
"""
