def get_host_html():
    return """
<!-- ==================== PAGE: HOST ==================== -->
<div id="page-host" class="page-view hidden">

<!-- Host Hero Section -->
<section class="relative bg-gradient-to-br from-brand-slateBlack to-brand-black text-white overflow-hidden py-20 border-b border-white/10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
        <div class="inline-flex items-center gap-2 bg-white/5 border border-white/10 px-4 py-2 rounded-full text-brand-gold text-xs font-medium tracking-widest uppercase mb-6">Premium Web Services</div>
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight">Complete <span class="text-transparent bg-clip-text bg-gradient-to-r from-brand-gold to-brand-goldLight">Hosting & Domain Suite</span></h1>
        <p class="mt-4 text-gray-400 max-w-2xl mx-auto">From powerful hosting plans to domain registration and professional email — all in one place. 24/7 support, 99.99% uptime, and free migration.</p>
        <div class="flex flex-wrap justify-center gap-4 mt-8"><a href="#services" class="glossy-gold text-brand-black px-7 py-3 rounded-full font-bold text-xs uppercase tracking-wider shadow-md">Browse All Products</a><a href="#coverage" class="glossy-black text-white px-7 py-3 rounded-full font-bold text-xs uppercase tracking-wider shadow-md">Check Availability</a></div>
    </div>
</section>

<!-- Products Section -->
<div id="services">
    <section id="packages" class="py-20 bg-brand-lightBg">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center max-w-3xl mx-auto mb-16 space-y-4">
                <span class="text-brand-goldDark uppercase font-black tracking-widest text-xs px-3.5 py-1 bg-brand-gold/10 rounded-full">Our Product Range</span>
                <h2 class="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-brand-black">Everything Your Online Business Needs</h2>
                <p class="text-gray-500 text-sm">Choose from hosting, domains, emails — or bundle and save. All products include our signature support and reliability.</p>
            </div>
            <!-- Main Category Tabs -->
            <div class="flex flex-col items-center gap-6 mb-12">
                <div class="bg-brand-darkGray/5 p-1 rounded-2xl shadow-inner border border-black/5 flex flex-wrap justify-center gap-1 w-full max-w-4xl">
                    <button onclick="setMainCategory('all')" id="tab-all" class="main-cat-tab flex-1 px-5 py-2.5 rounded-xl font-bold text-xs tracking-wider uppercase transition-all text-brand-goldDark bg-white shadow-sm">All Products</button>
                    <button onclick="setMainCategory('hostings')" id="tab-hostings" class="main-cat-tab flex-1 px-5 py-2.5 rounded-xl font-bold text-xs tracking-wider uppercase transition-all text-gray-500 hover:bg-white/50">Hostings</button>
                    <button onclick="setMainCategory('domains')" id="tab-domains" class="main-cat-tab flex-1 px-5 py-2.5 rounded-xl font-bold text-xs tracking-wider uppercase transition-all text-gray-500 hover:bg-white/50">Domains</button>
                    <button onclick="setMainCategory('emails')" id="tab-emails" class="main-cat-tab flex-1 px-5 py-2.5 rounded-xl font-bold text-xs tracking-wider uppercase transition-all text-gray-500 hover:bg-white/50">Emails</button>
                    <button onclick="setMainCategory('internet')" id="tab-internet" class="main-cat-tab flex-1 px-5 py-2.5 rounded-xl font-bold text-xs tracking-wider uppercase transition-all text-gray-500 hover:bg-white/50">Internet</button>
                </div>
                <!-- Sub-category filters (dynamic based on main category) -->
                <div id="subcategory-filters" class="flex flex-wrap justify-center gap-2"></div>
            </div>
            <!-- Products Container -->
            <div id="packages-container" class="grid sm:grid-cols-2 lg:grid-cols-3 gap-8"></div>
            <div class="mt-16 bg-white border border-black/5 rounded-3xl p-8 shadow-md flex flex-col md:flex-row items-center justify-between gap-6 relative overflow-hidden sheen-effect">
                <div class="flex items-center gap-5 z-10"><div class="h-14 w-14 bg-brand-gold/10 rounded-2xl flex items-center justify-center text-brand-goldDark text-2xl"><i class="fa-solid fa-life-ring"></i></div><div><h4 class="text-lg font-bold text-brand-black">Not sure what to choose?</h4><p class="text-xs text-gray-500">Our experts are ready to help you find the perfect solution for your needs.</p></div></div>
                <a href="#coverage" class="glossy-gold text-brand-black px-6 py-3 rounded-full font-bold text-xs tracking-wider uppercase shadow-md z-10">Talk to an Expert</a>
            </div>
        </div>
    </section>
</div>
</div>
"""
