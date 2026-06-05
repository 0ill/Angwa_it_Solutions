import streamlit as st
import streamlit.components.v1 as components

# Set up Streamlit page configurations to run full-screen
st.set_page_config(
    page_title="ANGWA | Symmetrical Pure Light Fibre",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject CSS globally to hide the default Streamlit UI header, footer, decoration bar, and default padding
st.markdown("""
    <style>
        /* Remove default Streamlit padding, header, footer, and decoration */
        [data-testid="stHeader"], 
        .stAppHeader, 
        footer, 
        .viewerBadge, 
        [data-testid="stDecoration"] {
            display: none !important;
            height: 0 !important;
            width: 0 !important;
        }
        .stApp {
            padding: 0 !important;
            margin: 0 !important;
            background-color: #000000 !important;
            overflow: hidden !important;
        }
        .main .block-container {
            padding: -50px !important;
            max-width: 100% !important;
            max-height: 100% !important;
            margin: -150px !important;
        }
        [data-testid="stAppViewContainer"] {
            padding: 0 !important;
        }
        [data-testid="stAppViewBlockContainer"] {
            padding: 0 !important;
        }
        [data-testid="stMain"] {
            padding: 0 !important;
        }
        iframe {
            border: none !important;
            display: block;
            width: 100% !important;
            height: 100vh !important;
        }
    </style>
""", unsafe_allow_html=True)

# We define the complete HTML structure. The CSS and JS are cleanly streamlined inside.
html_content = """
<!DOCTYPE html>
<html lang="en" class="scroll-smooth m-0 p-0">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ANGWA | Uncapped Symmetrical Fibre</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        brand: {
                            black: '#000000',
                            slateBlack: '#0D0D0E',
                            darkGray: '#1C1C1E',
                            gold: '#D4AF37',       /* Metallic Gold */
                            goldLight: '#F3E5AB',  /* Soft Gold Glow */
                            goldDark: '#AA7C11',   /* Rich Satin Gold */
                            green: '#30D158',      /* iOS Glossy Green */
                            greenDark: '#248A36',
                            white: '#FFFFFF',
                            lightBg: '#F5F5F7'     /* Apple Light Background */
                        }
                    },
                    fontFamily: {
                        sans: ['SF Pro Display', '-apple-system', 'BlinkMacSystemFont', 'Inter', 'sans-serif'],
                    }
                }
            }
        }
    </script>
    <!-- Google Fonts & FontAwesome -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Polar.sh Embedded Checkout SDK -->
    <script defer data-auto-init src="https://cdn.jsdelivr.net/npm/@polar-sh/checkout@latest/dist/embed.global.js"></script>
    
    <style>
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: #F5F5F7;
        }

        /* Apple-style Glassmorphism */
        .glass-dark {
            background: rgba(22, 22, 23, 0.75);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .glass-light {
            background: rgba(255, 255, 255, 0.75);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(0, 0, 0, 0.06);
        }

        /* Glossy Tactile Buttons */
        .glossy-gold {
            background: linear-gradient(180deg, #F9E7B9 0%, #D4AF37 40%, #A37F1A 100%);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.4), 
                        0 4px 15px rgba(212, 175, 55, 0.35);
            text-shadow: 0 1px 1px rgba(0, 0, 0, 0.15);
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .glossy-gold:hover {
            background: linear-gradient(180deg, #FFF0D0 0%, #E5C158 40%, #B89326 100%);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.5), 
                        0 6px 20px rgba(212, 175, 55, 0.5);
            transform: translateY(-1px);
        }

        .glossy-green {
            background: linear-gradient(180deg, #34E065 0%, #30D158 50%, #22993F 100%);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.4), 
                        0 4px 15px rgba(48, 209, 88, 0.3);
            text-shadow: 0 1px 1px rgba(0, 0, 0, 0.15);
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .glossy-green:hover {
            background: linear-gradient(180deg, #4AF078 0%, #39E067 50%, #2AA849 100%);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.5), 
                        0 6px 20px rgba(48, 209, 88, 0.45);
            transform: translateY(-1px);
        }

        .glossy-black {
            background: linear-gradient(180deg, #3A3A3C 0%, #1C1C1E 50%, #000000 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.15),
                        0 4px 12px rgba(0, 0, 0, 0.4);
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .glossy-black:hover {
            background: linear-gradient(180deg, #4A4A4C 0%, #2C2C2E 50%, #101012 100%);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.25),
                        0 6px 18px rgba(0, 0, 0, 0.5);
            transform: translateY(-1px);
        }

        /* Metallic shine sweep effect */
        @keyframes sweep {
            0% { transform: translateX(-100%) rotate(30deg); }
            100% { transform: translateX(300%) rotate(30deg); }
        }
        .sheen-effect::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -60%;
            width: 30%;
            height: 200%;
            background: linear-gradient(to right, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0.3) 50%, rgba(255, 255, 255, 0) 100%);
            transform: rotate(30deg);
            animation: sweep 4.5s infinite ease-in-out;
        }

        .gold-sheen-border {
            border: 1px solid rgba(212, 175, 55, 0.3);
            box-shadow: 0 0 25px rgba(212, 175, 55, 0.08);
        }

        /* Hide default scrollbars for iframe transitions */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #000000;
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.25);
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(212, 175, 55, 0.6);
        }
    </style>
</head>
<body class="text-brand-slateBlack antialiased m-0 p-0 overflow-x-hidden">

    <div class="bg-gradient-to-r from-brand-black via-[#1C1C1E] to-brand-black text-white py-2.5 px-4 text-center text-xs md:text-sm font-medium tracking-wide flex items-center justify-center gap-2.5 border-b border-brand-gold/20">
        <span class="bg-gradient-to-r from-brand-gold via-brand-goldLight to-brand-goldDark text-brand-black text-[10px] px-2.5 py-0.5 rounded-full uppercase font-black tracking-wider shadow-sm animate-pulse">PROMO</span>
        <span class="text-slate-300">Zero Setup Fees, Free Premium Wi-Fi 6 Router & 30-Day Money-Back Guarantee!</span>
    </div>

    <header class="sticky top-0 z-40 bg-brand-slateBlack/90 backdrop-blur-md border-b border-white/10 shadow-lg transition-all duration-300">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <!-- Dynamic Brand Logo / Badge -->
            <a href="#home-hero" class="flex items-center gap-2.5 group">
                <div class="h-8 w-8 bg-gradient-to-b from-brand-goldLight via-brand-gold to-brand-goldDark rounded-lg flex items-center justify-center text-brand-black font-black text-lg tracking-tight shadow-md transition-transform group-hover:rotate-6">
                    A
                </div>
                <!-- Dynamic text updated via IntersectionObserver ScrollSpy -->
                <span id="dynamic-nav-badge" class="text-lg font-bold tracking-tight text-white uppercase transition-all duration-300 min-w-[150px]">
                    ANGWA<span class="text-brand-gold">.</span>
                </span>
            </a>

            <!-- Menu Navigation Links -->
            <nav class="hidden lg:flex items-center gap-6 text-[13px] tracking-wide text-gray-300 font-medium">
                <a href="#home-hero" class="hover:text-brand-gold transition-colors">Home</a>
                <a href="#packages" class="hover:text-brand-gold transition-colors">Host</a>
                <a href="#design-suite" class="hover:text-brand-gold transition-colors">Design</a>
                <a href="#cloud-filling" class="hover:text-brand-gold transition-colors">Cloud Filling</a>
                <a href="#why-angwa" class="hover:text-brand-gold transition-colors">Why ANGWA</a>
                <a href="#faq" class="hover:text-brand-gold transition-colors">Support FAQ</a>
                
                <!-- Cloud Filling Dropdown menu -->
                <div class="relative group">
                    <button class="flex items-center gap-1.5 hover:text-brand-gold transition-colors focus:outline-none">
                        <span>Sync Options</span>
                        <i class="fa-solid fa-cloud text-[11px] text-brand-gold"></i>
                        <i class="fa-solid fa-chevron-down text-[9px] text-gray-500"></i>
                    </button>
                    <!-- Glossy Dropdown options -->
                    <div class="absolute left-0 mt-2 w-48 rounded-xl glass-dark shadow-2xl py-2 border border-white/10 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 transform translate-y-1 group-hover:translate-y-0 z-50">
                        <button onclick="triggerCloudSync('dropbox')" class="w-full text-left px-4 py-2 text-xs text-white hover:bg-white/10 flex items-center gap-2 transition-all">
                            <i class="fa-brands fa-dropbox text-blue-400"></i> Sync Dropbox
                        </button>
                        <button onclick="triggerCloudSync('google')" class="w-full text-left px-4 py-2 text-xs text-white hover:bg-white/10 flex items-center gap-2 transition-all">
                            <i class="fa-brands fa-google-drive text-green-400"></i> Sync Google Drive
                        </button>
                    </div>
                </div>
            </nav>

            <!-- CTA Actions -->
            <div class="flex items-center gap-4">
                <a href="#coverage" class="hidden sm:inline-block text-xs font-semibold text-gray-300 hover:text-brand-gold transition-all">
                    Check Coverage
                </a>
                <button onclick="triggerClientZone()" class="glossy-gold text-brand-black px-5 py-2 rounded-full font-bold text-xs shadow-md flex items-center gap-2">
                    <i class="fa-solid fa-user-shield"></i>
                    <span>ClientZone</span>
                </button>
            </div>
        </div>
    </header>

    <section id="home-hero" class="relative bg-brand-black text-white overflow-hidden py-20 lg:py-28">
        <!-- Abstract background patterns -->
        <div class="absolute inset-0 pointer-events-none opacity-20">
            <div class="absolute -top-20 left-10 w-96 h-96 bg-brand-gold rounded-full filter blur-[120px] animate-pulse"></div>
            <div class="absolute -bottom-20 right-10 w-[500px] h-[500px] bg-brand-green rounded-full filter blur-[150px]"></div>
        </div>

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
            <div class="grid lg:grid-cols-12 gap-16 items-center">
                
                <!-- Left Content: High End Marketing Pitch -->
                <div class="lg:col-span-7 space-y-6 text-center lg:text-left">
                    <div class="inline-flex items-center gap-2 bg-white/5 border border-white/10 px-4 py-2 rounded-full text-brand-gold text-xs font-medium tracking-widest uppercase">
                        <span class="flex h-2 w-2 relative">
                            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-green opacity-75"></span>
                            <span class="relative inline-flex rounded-full h-2 w-2 bg-brand-green"></span>
                        </span>
                        Symmetrical Fiber Optic Grid
                    </div>
                    
                    <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold leading-tight tracking-tight text-white">
                        Symmetrical Speed. <br class="hidden sm:block">
                        <span class="text-transparent bg-clip-text bg-gradient-to-r from-brand-gold via-brand-goldLight to-brand-goldDark">Pure Gloss Finish.</span>
                    </h1>
                    
                    <p class="text-base sm:text-lg text-gray-400 max-w-2xl mx-auto lg:mx-0 leading-relaxed">
                        Say goodbye to standard copper lag. ANGWA's fiber lines deliver pure light-based throughput straight to your smart environment. No buffering. No capacity restrictions. No contracts.
                    </p>

                    <!-- Trust Stats Grid -->
                    <div class="grid grid-cols-3 gap-6 pt-6 max-w-lg mx-auto lg:mx-0 border-t border-white/10">
                        <div>
                            <div class="text-2xl sm:text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-b from-white to-gray-400">99.99%</div>
                            <div class="text-xs text-gray-500 uppercase tracking-wider font-semibold mt-1">Uptime SLA</div>
                        </div>
                        <div>
                            <div class="text-2xl sm:text-3xl font-extrabold text-brand-gold">0</div>
                            <div class="text-xs text-gray-500 uppercase tracking-wider font-semibold mt-1">Caps or Limits</div>
                        </div>
                        <div>
                            <div class="text-2xl sm:text-3xl font-extrabold text-brand-green">24/7</div>
                            <div class="text-xs text-gray-500 uppercase tracking-wider font-semibold mt-1">Dedicated Care</div>
                        </div>
                    </div>
                </div>

                <!-- Right Content: Coverage Card -->
                <div id="coverage" class="lg:col-span-5">
                    <div class="glass-dark p-8 rounded-3xl shadow-2xl relative gold-sheen-border overflow-hidden sheen-effect">
                        <div class="absolute top-4 right-4 bg-gradient-to-r from-brand-gold via-brand-goldLight to-brand-goldDark text-brand-black text-[9px] uppercase font-black px-3.5 py-1.5 rounded-full tracking-wider shadow-md z-20">
                            Ultra Symmetrical
                        </div>
                        
                        <h3 class="text-xl font-bold tracking-tight text-white mb-2">Check Fibre Availability</h3>
                        <p class="text-xs text-gray-400 mb-6 leading-relaxed">Instantly verify speed potentials and provider availability for your complex or neighborhood.</p>
                        
                        <!-- Coverage Input -->
                        <div class="space-y-4">
                            <div class="relative">
                                <label class="block text-[10px] font-bold uppercase tracking-wider text-gray-400 mb-1.5">Suburb or Street Location</label>
                                <div class="relative">
                                    <input type="text" id="area-search" placeholder="e.g. Sandton, Sea Point, Hatfield..." 
                                           class="w-full px-4 py-3 pl-11 bg-brand-slateBlack border border-white/10 rounded-2xl text-white focus:outline-none focus:ring-2 focus:ring-brand-gold focus:border-transparent transition-all font-semibold placeholder-gray-500 text-sm">
                                    <i class="fa-solid fa-compass absolute left-4 top-4 text-brand-gold"></i>
                                </div>
                                
                                <!-- Dropdown Suggestions -->
                                <div id="search-dropdown" class="hidden absolute left-0 right-0 mt-1 bg-brand-darkGray border border-white/10 rounded-2xl shadow-xl z-50 overflow-hidden text-sm">
                                    <!-- Populated by JS -->
                                </div>
                            </div>

                            <button onclick="triggerSearch()" class="w-full py-3.5 glossy-green text-white font-bold rounded-2xl transition-all flex items-center justify-center gap-3">
                                <i class="fa-solid fa-magnifying-glass"></i>
                                <span>Analyze Location Status</span>
                            </button>
                        </div>

                        <!-- Dynamic Search Feedback Wrapper -->
                        <div id="search-result" class="hidden mt-6 p-4 rounded-2xl border transition-all duration-300">
                            <!-- Populated dynamically -->
                        </div>

                        <div class="mt-4 flex items-center justify-center gap-2 text-[11px] text-gray-500">
                            <i class="fa-solid fa-shield-halved text-brand-gold"></i>
                            <span>Secured light-speed database connection</span>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </section>

    <section class="py-8 bg-brand-slateBlack border-b border-white/10">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h4 class="text-[10px] uppercase tracking-widest font-bold text-gray-500 mb-4">Official Infrastructure Carrier Integrations</h4>
            
            <div class="flex flex-wrap items-center justify-center gap-4 md:gap-10 opacity-90">
                <div class="flex items-center gap-2 bg-white/5 px-4 py-2 rounded-full border border-white/5 font-semibold text-xs text-gray-300 hover:border-brand-gold/30 transition-all cursor-pointer">
                    <span class="h-2 w-2 rounded-full bg-brand-gold shadow-[0_0_8px_#D4AF37]"></span> Vumatel
                </div>
                <div class="flex items-center gap-2 bg-white/5 px-4 py-2 rounded-full border border-white/5 font-semibold text-xs text-gray-300 hover:border-brand-gold/30 transition-all cursor-pointer">
                    <span class="h-2 w-2 rounded-full bg-brand-green shadow-[0_0_8px_#30D158]"></span> Openserve
                </div>
                <div class="flex items-center gap-2 bg-white/5 px-4 py-2 rounded-full border border-white/5 font-semibold text-xs text-gray-300 hover:border-brand-gold/30 transition-all cursor-pointer">
                    <span class="h-2 w-2 rounded-full bg-brand-gold shadow-[0_0_8px_#D4AF37]"></span> Frogfoot
                </div>
                <div class="flex items-center gap-2 bg-white/5 px-4 py-2 rounded-full border border-white/5 font-semibold text-xs text-gray-300 hover:border-brand-gold/30 transition-all cursor-pointer">
                    <span class="h-2 w-2 rounded-full bg-white shadow-[0_0_8px_#FFFFFF]"></span> MetroFibre
                </div>
            </div>
        </div>
    </section>

    <section id="packages" class="py-20 bg-brand-lightBg">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            
            <!-- Grid Header Info -->
            <div class="text-center max-w-3xl mx-auto mb-16 space-y-4">
                <span class="text-brand-goldDark uppercase font-black tracking-widest text-xs px-3.5 py-1 bg-brand-gold/10 rounded-full">Pure Bandwidth</span>
                <h2 class="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-brand-black">
                    Choose Your Light Grid Configuration
                </h2>
                <p class="text-gray-500 text-sm">
                    Select by individual Network Provider, or segment speed tiers ideal for heavy streaming, cloud management, zero-ping online gaming, or massive smart home suites.
                </p>
            </div>

            <!-- FNO Premium Tab Selection -->
            <div class="flex flex-col items-center gap-6 mb-12">
                <div class="bg-brand-darkGray/5 p-1 rounded-2xl shadow-inner border border-black/5 flex flex-wrap justify-center gap-1 w-full max-w-2xl">
                    <button onclick="setFNO('all')" id="tab-all" class="fno-tab flex-1 px-5 py-2.5 rounded-xl font-bold text-xs tracking-wider uppercase transition-all text-brand-goldDark bg-white shadow-sm">
                        All Networks
                    </button>
                    <button onclick="setFNO('vuma')" id="tab-vuma" class="fno-tab flex-1 px-5 py-2.5 rounded-xl font-bold text-xs tracking-wider uppercase transition-all text-gray-500 hover:bg-white/50">
                        Vumatel
                    </button>
                    <button onclick="setFNO('open')" id="tab-open" class="fno-tab flex-1 px-5 py-2.5 rounded-xl font-bold text-xs tracking-wider uppercase transition-all text-gray-500 hover:bg-white/50">
                        Openserve
                    </button>
                    <button onclick="setFNO('frog')" id="tab-frog" class="fno-tab flex-1 px-5 py-2.5 rounded-xl font-bold text-xs tracking-wider uppercase transition-all text-gray-500 hover:bg-white/50">
                        Frogfoot
                    </button>
                </div>

                <!-- Speed Filter Toggles -->
                <div class="flex flex-wrap justify-center gap-2">
                    <button onclick="filterSpeedRange('all')" id="btn-speed-all" class="speed-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-brand-black bg-brand-black text-white transition-all shadow-sm">
                        All Speeds
                    </button>
                    <button onclick="filterSpeedRange('budget')" id="btn-speed-budget" class="speed-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-black/10 bg-white text-gray-600 hover:border-brand-gold transition-all shadow-sm">
                        Casual (30M - 50M)
                    </button>
                    <button onclick="filterSpeedRange('medium')" id="btn-speed-medium" class="speed-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-black/10 bg-white text-gray-600 hover:border-brand-gold transition-all shadow-sm">
                        Active House (100M - 200M)
                    </button>
                    <button onclick="filterSpeedRange('pro')" id="btn-speed-pro" class="speed-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-black/10 bg-white text-gray-600 hover:border-brand-gold transition-all shadow-sm">
                        Pro Tier (500M - 1G)
                    </button>
                </div>
            </div>

            <!-- Dynamic Package Configuration Cards Grid -->
            <div id="packages-container" class="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
                <!-- Populated dynamically by JS -->
            </div>

            <!-- Promotion banner footer -->
            <div class="mt-16 bg-white border border-black/5 rounded-3xl p-8 shadow-md flex flex-col md:flex-row items-center justify-between gap-6 relative overflow-hidden sheen-effect">
                <div class="flex items-center gap-5 z-10">
                    <div class="h-14 w-14 bg-brand-gold/10 rounded-2xl flex items-center justify-center text-brand-goldDark text-2xl">
                        <i class="fa-solid fa-globe"></i>
                    </div>
                    <div>
                        <h4 class="text-lg font-bold text-brand-black">Confused by different network setup terms?</h4>
                        <p class="text-xs text-gray-500">Run a manual coverage analysis. We'll automatically identify the cheapest option for your home.</p>
                    </div>
                </div>
                <a href="#coverage" class="glossy-gold text-brand-black px-6 py-3 rounded-full font-bold text-xs tracking-wider uppercase shadow-md z-10">
                    Compare Network Prices
                </a>
            </div>

        </div>
    </section>

    <section id="design-suite" class="py-20 bg-brand-slateBlack text-white overflow-hidden relative border-t border-b border-white/10">
        <div class="absolute inset-0 opacity-10 pointer-events-none">
            <div class="absolute top-0 right-0 w-96 h-96 bg-brand-gold rounded-full filter blur-[120px]"></div>
            <div class="absolute bottom-0 left-10 w-96 h-96 bg-brand-green rounded-full filter blur-[120px]"></div>
        </div>

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
            <div class="text-center max-w-3xl mx-auto mb-16 space-y-4">
                <span class="text-brand-gold uppercase font-black tracking-widest text-xs px-3.5 py-1 bg-brand-gold/10 rounded-full">Website Architecture & Splicing</span>
                <h2 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight">
                    Custom Web Design Packages
                </h2>
                <p class="text-gray-400 text-sm">
                    Select different premium web aesthetics and pricing models below. Watch our interactive web builder mockup container change layouts, structural grids, color metrics, and typography instantly.
                </p>
            </div>

            <div class="grid lg:grid-cols-12 gap-12 items-center">
                
                <!-- Left Column: Design Architecture Cards -->
                <div class="lg:col-span-5 space-y-4">
                    <h3 class="text-xl font-bold text-white mb-2">Select Design Tier</h3>
                    <p class="text-xs text-gray-400 leading-relaxed mb-6">Every plan is completely hand-coded, SEO optimized, integrated with ultra-fast light hosting, and customizable to your exact requirements.</p>

                    <!-- Design Card 1 -->
                    <div id="card-design-luxe" onclick="selectWebDesign('luxe')" 
                         class="design-selector-card cursor-pointer p-5 rounded-2xl border bg-brand-darkGray/60 border-brand-gold/40 shadow-lg hover:border-brand-gold transition-all duration-300 relative overflow-hidden">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-xs font-bold text-brand-gold tracking-widest uppercase flex items-center gap-2">
                                <i class="fa-solid fa-gem"></i> Luxe Obsidian
                            </span>
                            <span class="text-[9px] bg-brand-gold/15 text-brand-gold px-2.5 py-0.5 rounded font-bold uppercase tracking-wider">Most Popular</span>
                        </div>
                        <p class="text-xs text-gray-400 leading-relaxed mb-3">A spectacular ultra-premium dark theme featuring warm golden highlights, glassmorphism layers, and cinematic depth.</p>
                        
                        <!-- Pricing Details -->
                        <div class="border-t border-white/5 pt-3 mt-3 flex items-center justify-between">
                            <div>
                                <span class="text-xl font-extrabold text-white">R8,999</span>
                                <span class="text-[9px] text-gray-500 uppercase font-bold tracking-wider block">Once-off Setup</span>
                            </div>
                            <button onclick="openDesignSignupModal('luxe')" class="glossy-gold text-brand-black text-[10px] font-black uppercase tracking-wider px-3.5 py-1.5 rounded-full shadow-md flex items-center gap-1">
                                <span>Order Build</span> <i class="fa-solid fa-arrow-right text-[8px]"></i>
                            </button>
                        </div>
                        
                        <div class="flex items-center gap-3 text-[9px] text-gray-500 font-semibold uppercase mt-3">
                            <span><i class="fa-solid fa-circle-check text-brand-green mr-1"></i> 10 Pages</span>
                            <span><i class="fa-solid fa-gauge-high text-brand-green mr-1"></i> 99 Speed Index</span>
                        </div>
                    </div>

                    <!-- Design Card 2 -->
                    <div id="card-design-emerald" onclick="selectWebDesign('emerald')" 
                         class="design-selector-card cursor-pointer p-5 rounded-2xl border bg-brand-darkGray/20 border-white/5 shadow-lg hover:border-brand-green/50 transition-all duration-300 relative overflow-hidden">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-xs font-bold text-brand-green tracking-widest uppercase flex items-center gap-2">
                                <i class="fa-solid fa-bolt"></i> Emerald Neo
                            </span>
                            <span class="text-[9px] bg-brand-green/10 text-brand-green px-2 py-0.5 rounded font-bold uppercase tracking-wider">High Tech</span>
                        </div>
                        <p class="text-xs text-gray-400 leading-relaxed mb-3">Bright neon green highlights paired with deep carbon structures. Tailored for software, gaming networks, and modern tech brands.</p>
                        
                        <!-- Pricing Details -->
                        <div class="border-t border-white/5 pt-3 mt-3 flex items-center justify-between">
                            <div>
                                <span class="text-xl font-extrabold text-white">R5,499</span>
                                <span class="text-[9px] text-gray-500 uppercase font-bold tracking-wider block">Once-off Setup</span>
                            </div>
                            <button onclick="openDesignSignupModal('emerald')" class="glossy-green text-white text-[10px] font-black uppercase tracking-wider px-3.5 py-1.5 rounded-full shadow-md flex items-center gap-1">
                                <span>Order Build</span> <i class="fa-solid fa-arrow-right text-[8px]"></i>
                            </button>
                        </div>

                        <div class="flex items-center gap-3 text-[9px] text-gray-500 font-semibold uppercase mt-3">
                            <span><i class="fa-solid fa-circle-check text-brand-green mr-1"></i> 5 Pages</span>
                            <span><i class="fa-solid fa-code text-brand-green mr-1"></i> Clean Code</span>
                        </div>
                    </div>

                    <!-- Design Card 3 -->
                    <div id="card-design-minimal" onclick="selectWebDesign('minimal')" 
                         class="design-selector-card cursor-pointer p-5 rounded-2xl border bg-brand-darkGray/20 border-white/5 shadow-lg hover:border-brand-gold/50 transition-all duration-300 relative overflow-hidden">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-xs font-bold text-white tracking-widest uppercase flex items-center gap-2">
                                <i class="fa-solid fa-seedling"></i> Minimal Alabaster
                            </span>
                            <span class="text-[9px] bg-white/10 text-white px-2 py-0.5 rounded font-bold uppercase tracking-wider">Clean Minimal</span>
                        </div>
                        <p class="text-xs text-gray-400 leading-relaxed mb-3">Ultra-clean, crisp white typography structured over soft gray backdrops. Excellent layout clarity for e-commerce or blogs.</p>
                        
                        <!-- Pricing Details -->
                        <div class="border-t border-white/5 pt-3 mt-3 flex items-center justify-between">
                            <div>
                                <span class="text-xl font-extrabold text-white">R3,999</span>
                                <span class="text-[9px] text-gray-500 uppercase font-bold tracking-wider block">Once-off Setup</span>
                            </div>
                            <button onclick="openDesignSignupModal('minimal')" class="glossy-black text-white text-[10px] font-black uppercase tracking-wider px-3.5 py-1.5 rounded-full shadow-md flex items-center gap-1">
                                <span>Order Build</span> <i class="fa-solid fa-arrow-right text-[8px]"></i>
                            </button>
                        </div>

                        <div class="flex items-center gap-3 text-[9px] text-gray-500 font-semibold uppercase mt-3">
                            <span><i class="fa-solid fa-circle-check text-brand-green mr-1"></i> 3 Pages</span>
                            <span><i class="fa-solid fa-mobile text-white mr-1"></i> Fluid Grid</span>
                        </div>
                    </div>
                </div>

                <!-- Right Column: Interactive Mockup Live Device Viewport -->
                <div class="lg:col-span-7">
                    <div class="bg-brand-darkGray p-3 rounded-3xl border border-white/10 shadow-2xl relative">
                        
                        <!-- Top browser bar controls -->
                        <div class="flex items-center justify-between px-4 py-2 border-b border-white/5 text-xs text-gray-500">
                            <div class="flex items-center gap-1.5">
                                <span class="h-2.5 w-2.5 rounded-full bg-red-500/80 block"></span>
                                <span class="h-2.5 w-2.5 rounded-full bg-yellow-500/80 block"></span>
                                <span class="h-2.5 w-2.5 rounded-full bg-green-500/80 block"></span>
                            </div>
                            <div class="bg-black/40 px-6 py-1 rounded-full text-[10px] tracking-wide text-gray-400 flex items-center gap-1.5 font-mono select-none">
                                <i class="fa-solid fa-lock text-[9px] text-brand-green"></i> https://preview.angwa.design
                            </div>
                            <div class="flex items-center gap-3">
                                <button onclick="simulateReload()" class="hover:text-white transition-colors"><i class="fa-solid fa-rotate-right"></i></button>
                                <span class="text-[9px] font-bold text-brand-green">Live Sandbox</span>
                            </div>
                        </div>

                        <!-- Inner Live Preview Web Container -->
                        <div id="live-web-viewport" class="bg-black text-white p-6 sm:p-10 rounded-2xl min-h-[420px] flex flex-col justify-between transition-all duration-500 relative overflow-hidden">
                            <!-- Overlay Sheen sweeping effect -->
                            <div class="absolute inset-0 pointer-events-none sheen-effect opacity-10"></div>
                            
                            <!-- Header Element of the Mini site -->
                            <div class="flex justify-between items-center relative z-10">
                                <span id="mockup-logo" class="text-xs font-black tracking-tight flex items-center gap-1.5 text-brand-gold">
                                    <span class="h-5 w-5 bg-gradient-to-r from-brand-gold to-brand-goldDark rounded-md flex items-center justify-center text-brand-black text-[10px]">L</span> 
                                    <span>OBSIDIAN.</span>
                                </span>
                                <div class="flex gap-3 text-[9px] font-bold uppercase tracking-wider text-gray-400">
                                    <span>Products</span>
                                    <span>Pricing</span>
                                    <span>SLA</span>
                                </div>
                            </div>

                            <!-- Mid Content Section -->
                            <div class="my-auto space-y-4 py-8 relative z-10 text-center sm:text-left">
                                <div id="mockup-badge" class="inline-block text-[8px] tracking-widest font-bold uppercase px-2.5 py-1 bg-brand-gold/10 text-brand-gold border border-brand-gold/20 rounded-full">
                                    Cinematic Luxury Layout
                                </div>
                                <h4 id="mockup-title" class="text-2xl sm:text-3xl font-extrabold text-white leading-tight">
                                    Slick. Cinematic.<br>
                                    <span class="text-brand-gold">Gold Obsidian Accent.</span>
                                </h4>
                                <p id="mockup-desc" class="text-[11px] text-gray-400 max-w-sm leading-relaxed mx-auto sm:mx-0">
                                    Designed with luxury aesthetics. Highly interactive bento architecture mapped for corporate powerbrands and creatives.
                                </p>
                            </div>

                            <!-- Footer/Actions Panel of Mini site -->
                            <div class="flex flex-col sm:flex-row items-center justify-between gap-4 border-t border-white/10 pt-5 relative z-10">
                                <div class="text-center sm:text-left">
                                    <span class="text-[8px] uppercase tracking-wider text-gray-500 block font-bold">Standard Project Timeline</span>
                                    <span id="mockup-time" class="text-xs font-bold text-white">4-6 Business Days Delivery</span>
                                </div>
                                <button id="mockup-btn" class="glossy-gold text-brand-black text-[10px] font-black tracking-wider uppercase px-5 py-2.5 rounded-full shadow-md flex items-center gap-1.5">
                                    <span>Explore Blueprint</span> <i class="fa-solid fa-chevron-right text-[8px]"></i>
                                </button>
                            </div>

                        </div>
                    </div>
                </div>

            </div>
        </div>
    </section>

    <section id="cloud-filling" class="py-20 bg-brand-black text-white relative border-b border-white/10">
        <div class="absolute inset-0 pointer-events-none opacity-20">
            <div class="absolute top-1/4 right-1/4 w-[400px] h-[400px] bg-brand-gold rounded-full filter blur-[150px] animate-pulse"></div>
        </div>

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
            <div class="grid lg:grid-cols-12 gap-12 items-center">
                
                <!-- Left Hand Details Column -->
                <div class="lg:col-span-5 space-y-6 text-center lg:text-left">
                    <div class="inline-flex items-center gap-2 bg-white/5 border border-white/10 px-4 py-2 rounded-full text-brand-gold text-xs font-medium tracking-widest uppercase">
                        <i class="fa-solid fa-cloud-arrow-up"></i> Dynamic Upstream Mapping
                    </div>
                    <h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight">
                        Upstream Spliced <br>
                        <span class="text-transparent bg-clip-text bg-gradient-to-r from-brand-gold via-brand-goldLight to-brand-goldDark">Cloud-Filling Grid.</span>
                    </h2>
                    <p class="text-sm text-gray-400 leading-relaxed">
                        Say goodbye to sluggish cloud sync delays. With ANGWA's symmetrical fiber lines, uploads run at identical speeds to your downloads. Instantly map, sync, and deploy media directories directly to external storage platforms.
                    </p>
                    <div class="space-y-3.5 text-xs text-gray-300">
                        <div class="flex items-center gap-3">
                            <i class="fa-brands fa-dropbox text-blue-400 text-lg"></i>
                            <span>Dropbox Integration: Automated multi-thread background uploads.</span>
                        </div>
                        <div class="flex items-center gap-3">
                            <i class="fa-brands fa-google-drive text-green-400 text-lg"></i>
                            <span>Google Drive Integration: Smooth file splicing and real-time handshakes.</span>
                        </div>
                    </div>
                </div>

                <!-- Right Hand Visual Sandbox Terminal -->
                <div class="lg:col-span-7">
                    <div class="glass-dark rounded-3xl p-6 sm:p-8 border border-white/10 relative overflow-hidden shadow-2xl">
                        <div class="flex items-center justify-between mb-6 pb-4 border-b border-white/5">
                            <div>
                                <h4 class="font-bold text-sm">Direct-To-Cloud Filling Terminal</h4>
                                <p class="text-[10px] text-gray-500">Live test connection speed metrics</p>
                            </div>
                            <span class="text-[10px] bg-brand-green/10 text-brand-green border border-brand-green/20 px-2.5 py-1 rounded-full uppercase font-bold tracking-wider">
                                <i class="fa-solid fa-link animate-pulse"></i> Symmetrical Active
                            </span>
                        </div>

                        <!-- On page active synclines emulator card -->
                        <div class="bg-black/40 rounded-2xl p-6 border border-white/5 space-y-5">
                            <div class="flex items-center justify-between text-xs">
                                <span class="text-gray-400">Target Server Connection</span>
                                <div class="flex gap-2">
                                    <button onclick="triggerCloudSync('dropbox')" class="bg-blue-500/20 hover:bg-blue-500 text-blue-400 hover:text-white transition-all text-[10px] font-bold tracking-wide px-3 py-1.5 rounded-lg flex items-center gap-1">
                                        <i class="fa-brands fa-dropbox"></i> Dropbox
                                    </button>
                                    <button onclick="triggerCloudSync('google')" class="bg-green-500/20 hover:bg-green-500 text-green-400 hover:text-white transition-all text-[10px] font-bold tracking-wide px-3 py-1.5 rounded-lg flex items-center gap-1">
                                        <i class="fa-brands fa-google-drive"></i> Google Drive
                                    </button>
                                </div>
                            </div>

                            <!-- Simulator Progress Line -->
                            <div class="space-y-2">
                                <div class="flex justify-between text-[10px] font-mono text-gray-500 uppercase">
                                    <span>Sync Transmission Rate:</span>
                                    <span class="text-brand-green font-bold" id="panel-sync-rate">0 Mbps</span>
                                </div>
                                <div class="w-full bg-brand-slateBlack h-2.5 rounded-full overflow-hidden border border-white/5 relative">
                                    <div id="panel-progress-bar" class="bg-gradient-to-r from-brand-gold to-brand-green h-full rounded-full transition-all duration-300" style="width: 0%"></div>
                                </div>
                                <div class="flex justify-between text-[9px] text-gray-500">
                                    <span id="panel-sync-status">Inactive - Select pipeline platform to initiate sync</span>
                                    <span id="panel-sync-timer"></span>
                                </div>
                            </div>
                        </div>

                        <div class="mt-5 text-center text-[10px] text-gray-500 flex items-center justify-center gap-2">
                            <i class="fa-solid fa-network-wired text-brand-gold"></i>
                            <span>Bypasses local ISP throttling locks completely.</span>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </section>

    <section id="why-angwa" class="py-24 bg-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            
            <div class="text-center max-w-3xl mx-auto mb-20 space-y-4">
                <span class="text-brand-goldDark uppercase font-black tracking-widest text-xs px-3.5 py-1 bg-brand-gold/10 rounded-full">The ANGWA SLA</span>
                <h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-brand-black">
                    Premium Quality. Month-to-Month Freedom.
                </h2>
                <p class="text-gray-500 text-sm">
                    Unlike standard operators, we operate on a flexible framework. No strict long contracts, no setup charges, and direct refund guarantees.
                </p>
            </div>

            <!-- Custom Bento-Style feature grids -->
            <div class="grid md:grid-cols-3 gap-8">
                
                <!-- Benefit card 1: Hosting -->
                <div class="bg-brand-lightBg p-8 rounded-3xl hover:-translate-y-1 transition-all duration-300 border border-black/5 flex flex-col justify-between">
                    <div class="space-y-4">
                        <div class="h-12 w-12 bg-brand-gold/10 text-brand-goldDark rounded-2xl flex items-center justify-center text-xl shadow-inner">
                            <i class="fa-solid fa-server"></i>
                        </div>
                        <h3 class="text-lg font-bold text-brand-black tracking-tight">Premium High-Performance Hosting</h3>
                        <p class="text-xs text-gray-500 leading-relaxed">
                            Blazing-fast cloud hosting infrastructure optimized for instant page loading, robust security, and deep integration with our ultra-low-latency light grid network.
                        </p>
                    </div>
                    <div class="pt-6 text-[10px] font-black uppercase tracking-wider text-brand-goldDark">
                        Explore Hosting Tech <i class="fa-solid fa-chevron-right ml-1"></i>
                    </div>
                </div>

                <!-- Benefit card 2: Designing -->
                <div class="bg-brand-lightBg p-8 rounded-3xl hover:-translate-y-1 transition-all duration-300 border border-black/5 flex flex-col justify-between">
                    <div class="space-y-4">
                        <div class="h-12 w-12 bg-brand-green/10 text-brand-greenDark rounded-2xl flex items-center justify-center text-xl shadow-inner">
                            <i class="fa-solid fa-wand-magic-sparkles"></i>
                        </div>
                        <h3 class="text-lg font-bold text-brand-black tracking-tight">Custom Responsive Designing</h3>
                        <p class="text-xs text-gray-500 leading-relaxed">
                            Tailor-made, pixel-perfect user interfaces engineered for speed, conversion, and fluid grid layouts. Watch your concepts turn into high-score SEO assets seamlessly.
                        </p>
                    </div>
                    <div class="pt-6 text-[10px] font-black uppercase tracking-wider text-brand-greenDark">
                        Start Design Blueprint <i class="fa-solid fa-chevron-right ml-1"></i>
                    </div>
                </div>

                <!-- Benefit card 3: Cloud-Filling -->
                <div class="bg-brand-lightBg p-8 rounded-3xl hover:-translate-y-1 transition-all duration-300 border border-black/5 flex flex-col justify-between">
                    <div class="space-y-4">
                        <div class="h-12 w-12 bg-black/5 text-brand-black rounded-2xl flex items-center justify-center text-xl shadow-inner">
                            <i class="fa-solid fa-cloud-arrow-up"></i>
                        </div>
                        <h3 class="text-lg font-bold text-brand-black tracking-tight">Seamless Cloud-Filling Synclines</h3>
                        <p class="text-xs text-gray-500 leading-relaxed">
                            Instant direct-to-cloud backups. Map, sync, and deploy massive asset databases directly into your custom storage space on Dropbox or Google Drive in seconds.
                        </p>
                    </div>
                    <div class="pt-6 text-[10px] font-black uppercase tracking-wider text-brand-black">
                        Sync Cloud Media <i class="fa-solid fa-chevron-right ml-1"></i>
                    </div>
                </div>

            </div>
        </div>
    </section>

    <section id="faq" class="py-20 bg-brand-lightBg">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            
            <div class="text-center mb-16 space-y-4">
                <span class="text-brand-goldDark uppercase font-black tracking-widest text-xs px-3.5 py-1 bg-brand-gold/10 rounded-full">Help & Support</span>
                <h2 class="text-3xl font-bold tracking-tight text-brand-black">Fibre FAQ Knowledge-Base</h2>
                <p class="text-gray-500 text-xs">Everything you need to know about setting up ANGWA Fibre.</p>
            </div>

            <!-- Expandable Accordion Panel Elements -->
            <div class="space-y-4">
                
                <!-- FAQ Block 1 -->
                <div class="bg-white border border-black/5 rounded-2xl overflow-hidden shadow-sm">
                    <button class="w-full px-6 py-4.5 text-left font-bold text-sm flex items-center justify-between text-brand-black hover:text-brand-goldDark transition-colors" onclick="toggleFaq(this)">
                        <span>How long is the typical installation cycle?</span>
                        <i class="fa-solid fa-chevron-down transition-transform"></i>
                    </button>
                    <div class="px-6 pb-5 text-xs text-gray-500 hidden leading-relaxed border-t border-black/5 pt-4">
                        After ordering, the designated carrier infrastructure partner (Openserve, Vumatel, Frogfoot, etc.) will schedule your installation date. Connection takes 2-5 working days depending on setup dynamics.
                    </div>
                </div>

                <!-- FAQ Block 2 -->
                <div class="bg-white border border-black/5 rounded-2xl overflow-hidden shadow-sm">
                    <button class="w-full px-6 py-4.5 text-left font-bold text-sm flex items-center justify-between text-brand-black hover:text-brand-goldDark transition-colors" onclick="toggleFaq(this)">
                        <span>Are there hidden administration fees?</span>
                        <i class="fa-solid fa-chevron-down transition-transform"></i>
                    </button>
                    <div class="px-6 pb-5 text-xs text-gray-500 hidden leading-relaxed border-t border-black/5 pt-4">
                        Absolutely zero. All connection logistics, fiber equipment setup fees, and baseline Wi-Fi 6 hardware distribution options are completely pre-paid by us.
                    </div>
                </div>

                <!-- FAQ Block 3 -->
                <div class="bg-white border border-black/5 rounded-2xl overflow-hidden shadow-sm">
                    <button class="w-full px-6 py-4.5 text-left font-bold text-sm flex items-center justify-between text-brand-black hover:text-brand-goldDark transition-colors" onclick="toggleFaq(this)">
                        <span>How does the double money-back guarantee work?</span>
                        <i class="fa-solid fa-chevron-down transition-transform"></i>
                    </button>
                    <div class="px-6 pb-5 text-xs text-gray-500 hidden leading-relaxed border-t border-black/5 pt-4">
                        If you are unsatisfied with connection speeds, drop rates, or support queues within the initial 30 days of setup, notify us. We'll terminate the line and issue a complete premium refund, doubled.
                    </div>
                </div>

                <!-- FAQ Block 4 -->
                <div class="bg-white border border-black/5 rounded-2xl overflow-hidden shadow-sm">
                    <button class="w-full px-6 py-4.5 text-left font-bold text-sm flex items-center justify-between text-brand-black hover:text-brand-goldDark transition-colors" onclick="toggleFaq(this)">
                        <span>What termination terms are applicable?</span>
                        <i class="fa-solid fa-chevron-down transition-transform"></i>
                    </button>
                    <div class="px-6 pb-5 text-xs text-gray-500 hidden leading-relaxed border-t border-black/5 pt-4">
                        Our packages are based on calendar-month schedules. Simply submit a cancellation notice 30 days prior. Hardware must be returned within 14 business days of line termination.
                    </div>
                </div>

            </div>
        </div>
    </section>

    <div id="signup-modal" class="fixed inset-0 z-50 overflow-y-auto hidden" aria-labelledby="modal-title" role="dialog" aria-modal="true">
        <!-- Blur Backdrop Overlay -->
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div class="fixed inset-0 bg-brand-black/80 backdrop-blur-md transition-opacity" aria-hidden="true" onclick="closeModal()"></div>

            <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

            <!-- Modal UI Panel -->
            <div class="inline-block align-bottom bg-brand-slateBlack text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-xl sm:w-full rounded-3xl border border-white/10 text-white">
                
                <!-- Modal Head -->
                <div class="bg-brand-darkGray px-6 py-5 flex items-center justify-between border-b border-white/5">
                    <div>
                        <span class="text-[10px] uppercase tracking-widest text-brand-gold font-bold block">Configure Connection</span>
                        <h3 class="text-md font-bold">Fast-Track Fibre Order</h3>
                    </div>
                    <button onclick="closeModal()" class="text-gray-400 hover:text-white transition-colors text-xl">
                        <i class="fa-solid fa-circle-xmark"></i>
                    </button>
                </div>

                <!-- Multi-Step indicators -->
                <div class="bg-black/40 px-6 py-3 flex items-center justify-between text-[10px] font-bold text-gray-500 uppercase tracking-wider">
                    <span id="step-indicator-1" class="text-brand-gold flex items-center gap-1.5">
                        <span class="h-4.5 w-4.5 rounded-full bg-brand-gold/20 text-brand-gold flex items-center justify-center text-[9px] font-black">1</span> Options
                    </span>
                    <span id="step-indicator-2" class="flex items-center gap-1.5">
                        <span class="h-4.5 w-4.5 rounded-full bg-white/5 text-gray-500 flex items-center justify-center text-[9px] font-black">2</span> Setup Info
                    </span>
                    <span id="step-indicator-3" class="flex items-center gap-1.5">
                        <span class="h-4.5 w-4.5 rounded-full bg-white/5 text-gray-500 flex items-center justify-center text-[9px] font-black">3</span> Summary
                    </span>
                </div>

                <div class="p-6">
                    
                    <!-- STEP 1: Addons -->
                    <div id="modal-step-1" class="space-y-6">
                        <div class="bg-white/5 p-4 rounded-2xl border border-white/5 flex items-center justify-between">
                            <div>
                                <h4 class="font-bold text-sm text-white" id="modal-package-name">Openserve 50/50 Mbps</h4>
                                <p class="text-[10px] text-gray-400" id="modal-package-subtitle">Monthly Symmetrical Fibre Premium</p>
                            </div>
                            <span class="text-base font-bold text-brand-gold" id="modal-package-price">R499.00</span>
                        </div>

                        <!-- Options grid -->
                        <div class="space-y-3">
                            <h5 class="text-[10px] font-bold uppercase tracking-wider text-gray-500" id="modal-upgrade-header">Upgrade Hardware & Configuration</h5>
                            
                            <!-- Checkbox 1: Wi-Fi 6 -->
                            <label id="addon-router-container" class="flex items-center justify-between p-4 border border-white/5 bg-brand-darkGray/40 rounded-2xl cursor-pointer hover:bg-brand-darkGray transition-colors">
                                <div class="flex items-center gap-3">
                                    <input type="checkbox" id="addon-router" onchange="calculateModalTotal()" class="h-4.5 w-4.5 text-brand-gold bg-brand-black border-white/10 rounded focus:ring-brand-gold">
                                    <div>
                                        <span class="font-bold text-xs block text-white" id="addon-router-title">Upgrade to Wi-Fi 6 Pro System</span>
                                        <span class="text-[10px] text-gray-400" id="addon-router-desc">Enhance transmission rates across concrete walls.</span>
                                    </div>
                                </div>
                                <span class="text-xs font-bold text-brand-gold" id="addon-router-price">+R99/pm</span>
                            </label>

                            <!-- Checkbox 2: Static IP -->
                            <label id="addon-ip-container" class="flex items-center justify-between p-4 border border-white/5 bg-brand-darkGray/40 rounded-2xl cursor-pointer hover:bg-brand-darkGray transition-colors">
                                <div class="flex items-center gap-3">
                                    <input type="checkbox" id="addon-ip" onchange="calculateModalTotal()" class="h-4.5 w-4.5 text-brand-gold bg-brand-black border-white/10 rounded focus:ring-brand-gold">
                                    <div>
                                        <span class="font-bold text-xs block text-white" id="addon-ip-title">Fixed Dedicated Static IP</span>
                                        <span class="text-[10px] text-gray-400" id="addon-ip-desc">Ideal for running servers, secure logins or smart systems.</span>
                                    </div>
                                </div>
                                <span class="text-xs font-bold text-brand-gold" id="addon-ip-price">+R49/pm</span>
                            </label>
                        </div>
                    </div>

                    <!-- STEP 2: Address Detail Configuration -->
                    <div id="modal-step-2" class="space-y-4 hidden">
                        <h4 class="font-bold text-xs text-white uppercase tracking-wider">Installation Destination Info</h4>
                        
                        <div class="space-y-3 text-xs">
                            <div>
                                <label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Full Subscriber Name</label>
                                <input type="text" id="cust-name" placeholder="e.g. Lerato Ndlovu" class="w-full px-4 py-2.5 bg-brand-darkGray border border-white/10 rounded-xl text-white focus:ring-2 focus:ring-brand-gold focus:outline-none">
                            </div>
                            <div>
                                <label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Primary Email Contact</label>
                                <input type="email" id="cust-email" placeholder="e.g. lerato@domain.co.za" class="w-full px-4 py-2.5 bg-brand-darkGray border border-white/10 rounded-xl text-white focus:ring-2 focus:ring-brand-gold focus:outline-none">
                            </div>
                            <div>
                                <label class="block text-[10px] font-bold uppercase text-gray-400 mb-1" id="modal-address-label">Premises Address</label>
                                <input type="text" id="cust-address" placeholder="e.g. Unit 5, Sandhurst Ridge Complex" class="w-full px-4 py-2.5 bg-brand-darkGray border border-white/10 rounded-xl text-white focus:ring-2 focus:ring-brand-gold focus:outline-none">
                            </div>
                        </div>
                    </div>

                    <!-- STEP 3: Complete & Submit (with Polar.sh checkout button) -->
                    <div id="modal-step-3" class="space-y-4 hidden">
                        <div class="text-center space-y-2 py-4">
                            <div class="h-14 w-14 bg-brand-green/10 text-brand-green rounded-full flex items-center justify-center text-2xl mx-auto shadow-inner">
                                <i class="fa-regular fa-circle-check"></i>
                            </div>
                            <h4 class="font-black text-base text-white" id="modal-success-title">System Configuration Confirmed</h4>
                            <p class="text-[11px] text-gray-400 max-w-sm mx-auto" id="modal-success-desc">No upfront charges are required. Payment logic only starts when physical line activation is confirmed.</p>
                        </div>

                        <!-- Bill Review -->
                        <div class="bg-brand-darkGray/60 p-4 rounded-2xl border border-white/5 space-y-2 text-xs text-gray-300">
                            <div class="flex justify-between">
                                <span class="text-gray-500" id="summary-base-label">Standard Base Fee:</span>
                                <span class="font-bold text-white" id="summary-pkg-price">R0.00</span>
                            </div>
                            <div id="summary-addon-router-row" class="flex justify-between hidden">
                                <span class="text-gray-500" id="summary-addon-router-label">Wi-Fi 6 Pro Upgrade:</span>
                                <span class="font-bold text-white" id="summary-addon-router-price-val">+R99.00</span>
                            </div>
                            <div id="summary-addon-ip-row" class="flex justify-between hidden">
                                <span class="text-gray-500" id="summary-addon-ip-label">Fixed Static IP allocation:</span>
                                <span class="font-bold text-white" id="summary-addon-ip-price-val">+R49.00</span>
                            </div>
                            <div class="flex justify-between border-t border-white/10 pt-2 text-sm font-bold">
                                <span class="text-white" id="summary-total-label">Active Monthly Subtotal:</span>
                                <span class="text-brand-gold" id="summary-total-price">R0.00</span>
                            </div>
                        </div>
                    </div>

                </div>

                <!-- Modal Actions bar -->
                <div class="bg-brand-darkGray px-6 py-4 flex items-center justify-between border-t border-white/5">
                    <button id="modal-back-btn" onclick="prevStep()" class="text-xs font-bold tracking-wider uppercase text-gray-400 hover:text-white transition-colors hidden">
                        <i class="fa-solid fa-chevron-left mr-1"></i> Back
                    </button>
                    <span id="modal-step-pricing" class="text-xs font-bold text-white">
                        <span id="modal-pricing-label">Monthly Cost:</span> <span class="text-brand-gold font-black" id="modal-footer-price">R0.00</span>
                    </span>
                    <div id="modal-next-btn-container">
                        <button id="modal-next-btn" onclick="nextStep()" class="glossy-gold text-brand-black px-6 py-2.5 rounded-full font-bold text-xs tracking-wider uppercase shadow-md">
                            Continue <i class="fa-solid fa-chevron-right ml-1"></i>
                        </button>
                    </div>
                </div>

            </div>
        </div>
    </div>

    <!-- Cloud Filling Progress Sync Modal -->
    <div id="cloud-sync-modal" class="fixed inset-0 z-50 overflow-y-auto hidden" aria-labelledby="modal-title" role="dialog" aria-modal="true">
        <div class="flex items-center justify-center min-h-screen p-4">
            <div class="fixed inset-0 bg-brand-black/80 backdrop-blur-md transition-opacity" onclick="closeCloudModal()"></div>
            <div class="bg-brand-slateBlack text-white p-8 rounded-3xl max-w-sm w-full space-y-6 text-center border border-white/10 relative z-10 overflow-hidden">
                <div class="absolute -top-12 -right-12 h-32 w-32 bg-brand-gold/10 rounded-full filter blur-xl"></div>
                
                <div class="h-16 w-16 bg-brand-gold/15 text-brand-gold rounded-full flex items-center justify-center text-3xl mx-auto shadow-inner border border-brand-gold/20">
                    <i id="cloud-icon" class="fa-brands fa-dropbox"></i>
                </div>
                
                <div class="space-y-2">
                    <h4 class="font-bold text-md text-white">Cloud Filling Simulation</h4>
                    <p id="cloud-sync-status" class="text-xs text-gray-400 leading-relaxed">Initializing secure Dropbox high-speed fiber mapping pipeline...</p>
                </div>

                <!-- Simulating high speed fiber backup metrics -->
                <div class="bg-black/40 p-4 rounded-2xl border border-white/5 space-y-3">
                    <div class="flex justify-between text-[10px] uppercase font-bold text-gray-500">
                        <span>Speed Transfer Rate</span>
                        <span class="text-brand-green">1,000 Mbps</span>
                    </div>
                    <!-- Dynamic Progress Bar -->
                    <div class="w-full bg-brand-darkGray rounded-full h-2 overflow-hidden border border-white/10">
                        <div id="cloud-progress-bar" class="bg-brand-green h-full rounded-full transition-all duration-300" style="width: 0%"></div>
                    </div>
                    <div class="flex justify-between text-[10px] text-gray-400">
                        <span>Synced 50GB project files</span>
                        <span id="cloud-timer-val">Calculating...</span>
                    </div>
                </div>

                <button onclick="closeCloudModal()" class="w-full glossy-gold text-brand-black py-2.5 rounded-full font-bold text-xs uppercase tracking-wider">Close Sync Pipeline</button>
            </div>
        </div>
    </div>

    <!-- ClientZone Login Modal -->
    <div id="clientzone-modal" class="fixed inset-0 z-50 overflow-y-auto hidden" aria-labelledby="modal-title" role="dialog" aria-modal="true">
        <div class="flex items-center justify-center min-h-screen p-4">
            <div class="fixed inset-0 bg-brand-black/80 backdrop-blur-md transition-opacity" onclick="closeClientZone()"></div>
            <div class="bg-brand-slateBlack text-white p-8 rounded-3xl max-w-sm w-full space-y-6 border border-white/10 relative z-10">
                <div class="text-center space-y-2">
                    <div class="h-12 w-12 bg-brand-gold/10 text-brand-gold rounded-full flex items-center justify-center text-xl mx-auto">
                        <i class="fa-solid fa-user-shield"></i>
                    </div>
                    <h4 class="font-bold text-lg text-white">ANGWA ClientZone</h4>
                    <p class="text-xs text-gray-400">Manage, scale, and upgrade your month-to-month light grid.</p>
                </div>

                <div class="space-y-4 text-xs">
                    <div>
                        <label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Subscriber ID or Email</label>
                        <input type="text" id="cz-email" placeholder="e.g. client@domain.co.za" class="w-full px-4 py-2.5 bg-brand-darkGray border border-white/10 rounded-xl text-white focus:ring-2 focus:ring-brand-gold focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Access Token / Password</label>
                        <input type="password" id="cz-password" placeholder="••••••••" class="w-full px-4 py-2.5 bg-brand-darkGray border border-white/10 rounded-xl text-white focus:ring-2 focus:ring-brand-gold focus:outline-none">
                    </div>
                    <button onclick="submitClientZoneMock()" class="w-full glossy-gold text-brand-black py-3 rounded-full font-bold uppercase tracking-wider text-xs">Secure Log In</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Order Notification Confirmation Toast Box -->
    <div id="order-toast" class="fixed bottom-6 right-6 z-50 bg-brand-slateBlack text-white px-6 py-4 rounded-2xl shadow-2xl border border-brand-gold/30 flex items-center gap-4 hidden max-w-sm">
        <div class="h-10 w-10 bg-brand-gold/15 text-brand-gold rounded-xl flex items-center justify-center text-xl shrink-0">
            <i class="fa-solid fa-paper-plane"></i>
        </div>
        <div class="text-xs">
            <h5 class="font-bold text-white">Pre-order Registered!</h5>
            <p class="text-gray-400 mt-0.5">Please check your inbox. Our support crew will contact you soon.</p>
        </div>
        <button onclick="hideOrderToast()" class="text-gray-500 hover:text-white transition-colors">
            <i class="fa-solid fa-xmark"></i>
        </button>
    </div>

    <!-- Floating Support Button and Chat Box -->
    <div class="fixed bottom-6 left-6 z-40">
        <button onclick="toggleLiveChat()" class="h-12 w-12 bg-gradient-to-b from-brand-goldLight via-brand-gold to-brand-goldDark text-brand-black rounded-full flex items-center justify-center text-xl shadow-xl hover:scale-105 transition-all relative">
            <i class="fa-solid fa-headset"></i>
            <span class="absolute top-0 right-0 h-3.5 w-3.5 bg-brand-green border-2 border-brand-black rounded-full flex items-center justify-center text-[7px] font-bold text-white">1</span>
        </button>

        <!-- Live Chat Box pop-up -->
        <div id="chat-popup" class="hidden absolute bottom-16 left-0 bg-brand-slateBlack border border-white/10 rounded-2xl shadow-2xl w-76 overflow-hidden text-xs text-white">
            <div class="bg-brand-darkGray p-4 flex items-center gap-3 border-b border-white/5">
                <div class="h-9 w-9 bg-brand-gold/15 rounded-full flex items-center justify-center text-brand-gold shadow-inner">
                    <i class="fa-solid fa-circle-user text-md"></i>
                </div>
                <div>
                    <h5 class="font-bold">Fibre Agent Sipho</h5>
                    <p class="text-[9px] text-brand-green font-semibold flex items-center gap-1">
                        <span class="h-1.5 w-1.5 rounded-full bg-brand-green block animate-pulse"></span> Symmetrical Carrier Advisor
                    </p>
                </div>
            </div>
            
            <div class="p-4 space-y-4 max-h-52 overflow-y-auto bg-brand-black/40 text-gray-300" id="chat-messages">
                <div class="bg-brand-darkGray/60 p-3 rounded-2xl border border-white/5 text-gray-300 max-w-[85%] leading-relaxed">
                    Good day! Let me help you find the best month-to-month fibre setup or premium custom design templates. Where are you located?
                </div>
            </div>

            <!-- Message box entry -->
            <div class="p-2.5 bg-brand-darkGray border-t border-white/5 flex items-center gap-1.5">
                <input type="text" id="chat-input" placeholder="Type message..." class="flex-1 bg-brand-black border border-white/10 px-3 py-2 rounded-xl text-xs focus:outline-none focus:ring-1 focus:ring-brand-gold text-white placeholder-gray-500" onkeydown="handleChatSubmit(event)">
                <button onclick="sendChatMessage()" class="h-8 w-8 bg-brand-gold text-brand-black rounded-lg flex items-center justify-center hover:bg-brand-goldLight transition-colors">
                    <i class="fa-solid fa-paper-plane text-xs"></i>
                </button>
            </div>
        </div>
    </div>

    <!-- Footer Section -->
    <footer class="bg-brand-black text-gray-500 py-16 border-t border-white/10 text-xs">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-8">
                
                <!-- Brand pitch -->
                <div class="col-span-2 space-y-4">
                    <a href="#" class="flex items-center gap-2">
                        <div class="h-7 w-7 bg-brand-gold rounded-md flex items-center justify-center text-brand-black font-black text-sm shadow-md">
                            A
                        </div>
                        <span class="text-lg font-bold text-white tracking-wider">ANGWA.</span>
                    </a>
                    <p class="leading-relaxed text-gray-400">
                        ANGWA is a licensed provider of optical fibre connections and digital bespoke web environments in South Africa. Operating across the main national carrier frameworks to bring symmetrical speeds directly to you.
                    </p>
                    <div class="flex items-center gap-3 pt-2 text-gray-400">
                        <a href="#" class="hover:text-brand-gold transition-colors"><i class="fa-brands fa-facebook"></i></a>
                        <a href="#" class="hover:text-brand-gold transition-colors"><i class="fa-brands fa-x-twitter"></i></a>
                        <a href="#" class="hover:text-brand-gold transition-colors"><i class="fa-brands fa-instagram"></i></a>
                        <a href="#" class="hover:text-brand-gold transition-colors"><i class="fa-brands fa-linkedin"></i></a>
                    </div>
                </div>

                <!-- Products -->
                <div>
                    <h5 class="text-white text-[10px] font-bold uppercase tracking-wider mb-4">Speed Products</h5>
                    <ul class="space-y-2">
                        <li><a href="#packages" class="hover:text-white transition-colors">Vumatel Packages</a></li>
                        <li><a href="#packages" class="hover:text-white transition-colors">Openserve Packages</a></li>
                        <li><a href="#packages" class="hover:text-white transition-colors">Frogfoot Packages</a></li>
                        <li><a href="#" class="hover:text-white transition-colors">Gigabit Power Fibre</a></li>
                    </ul>
                </div>

                <!-- Support -->
                <div>
                    <h5 class="text-white text-[10px] font-bold uppercase tracking-wider mb-4">Support & Care</h5>
                    <ul class="space-y-2">
                        <li><a href="#" class="hover:text-white transition-colors">Client Zone Login</a></li>
                        <li><a href="#" class="hover:text-white transition-colors">Help Centre</a></li>
                        <li><a href="#" class="hover:text-white transition-colors">Network Status Map</a></li>
                        <li><a href="#" class="hover:text-white transition-colors">Contact Support</a></li>
                    </ul>
                </div>

                <!-- Legal -->
                <div>
                    <h5 class="text-white text-[10px] font-bold uppercase tracking-wider mb-4">Legal Framework</h5>
                    <ul class="space-y-2">
                        <li><a href="#" class="hover:text-white transition-colors">Terms of Agreement</a></li>
                        <li><a href="#" class="hover:text-white transition-colors">Privacy Policy</a></li>
                        <li><a href="#" class="hover:text-white transition-colors">Fibre SLA Policies</a></li>
                    </ul>
                </div>

            </div>

            <!-- Bottom Line copyrights -->
            <div class="mt-12 pt-8 border-t border-white/5 text-center text-[10px] text-gray-600 space-y-2">
                <p>© 2026 ANGWA Proprietary Limited. All rights reserved. Registered ICASA carrier frameworks.</p>
                <p>Designed for maximum speed simulation based on physical optical fibre networks locally deployed.</p>
            </div>
        </div>
    </footer>


    <!-- ==================== CORE SCRIPT ENGINE ==================== -->
    <script>
        
        /* Areas for coverage search checks */
        const mockAreas = [
            { name: "Sandton", state: "available", provider: "Vumatel", speed: "1000 Mbps" },
            { name: "Sea Point", state: "available", provider: "Openserve", speed: "500 Mbps" },
            { name: "Hatfield", state: "available", provider: "Frogfoot", speed: "200 Mbps" },
            { name: "Umhlanga", state: "available", provider: "Vumatel", speed: "1000 Mbps" },
            { name: "Randburg", state: "available", provider: "Openserve", speed: "100 Mbps" },
            { name: "Centurion", state: "available", provider: "Frogfoot", speed: "1000 Mbps" },
            { name: "Soweto", state: "pending", provider: "Vumatel Reach", speed: "40 Mbps" },
            { name: "Gqeberha", state: "available", provider: "Frogfoot", speed: "200 Mbps" },
            { name: "Rondebosch", state: "available", provider: "Openserve", speed: "500 Mbps" }
        ];

        /* Symmetrical Fibre packages list */
        const packageData = [
            { id: 1, provider: "open", name: "Openserve Light Symmetrical", down: 50, up: 50, price: 499, description: "Stable high-speed optical fiber. Perfect for reliable daily workflows and smooth 4K streaming.", isPopular: false },
            { id: 2, provider: "open", name: "Openserve Active Power", down: 100, up: 100, price: 699, description: "Our most popular package. Designed for modern multi-device households, heavy streaming and gaming.", isPopular: true },
            { id: 3, provider: "open", name: "Openserve Elite Gig", down: 500, up: 500, price: 999, description: "Premium tier connectivity. Instant cloud handshakes, lightning downloads and absolute responsiveness.", isPopular: false },
            { id: 4, provider: "vuma", name: "Vumatel Home Grid", down: 100, up: 100, price: 749, description: "Consistent, reliable throughput across the premium Vumatel light-grid footprint.", isPopular: false },
            { id: 5, provider: "vuma", name: "Vumatel Fast Spliced", down: 200, up: 200, price: 899, description: "Power user favorite. Designed to manage heavy uploads, active smart homes and seamless lag-free gaming.", isPopular: true },
            { id: 6, provider: "vuma", name: "Vumatel Hyper Speed", down: 1000, up: 1000, price: 1299, description: "Max-throughput symmetrical Gigabit line. The ultimate internet experience with no holding back.", isPopular: false },
            { id: 7, provider: "frog", name: "Frogfoot Core Starter", down: 30, up: 30, price: 449, description: "Perfect entry-level uncapped symmetrical fiber for budget-conscious surfing and remote work.", isPopular: false },
            { id: 8, provider: "frog", name: "Frogfoot Active Spliced", down: 150, up: 150, price: 799, description: "Highly resilient middle-tier symmetrical line for reliable and smooth multi-device performance.", isPopular: false },
            { id: 9, provider: "frog", name: "Frogfoot Heavy Symmetrical", down: 500, up: 500, price: 1049, description: "Blazing fast throughput constructed for instant cloud syncs, large media backups, and extreme usage.", isPopular: false }
        ];

        /* Web Design Archetype Layout data mapping */
        const designData = {
            luxe: {
                id: 'design-luxe',
                price: 8999,
                logoText: "OBSIDIAN.",
                logoClass: "text-brand-gold",
                badgeText: "Cinematic Luxury Layout",
                badgeClass: "bg-brand-gold/10 text-brand-gold border-brand-gold/20",
                title: "Slick. Cinematic.<br><span class='text-brand-gold'>Gold Obsidian Accent.</span>",
                desc: "Designed with luxury aesthetics. Highly interactive bento architecture mapped for corporate powerbrands and creatives.",
                timeText: "4-6 Business Days Delivery",
                btnClass: "glossy-gold text-brand-black",
                viewportBg: "bg-black text-white border border-brand-gold/20"
            },
            emerald: {
                id: 'design-emerald',
                price: 5499,
                logoText: "NEO TECH.",
                logoClass: "text-brand-green",
                badgeText: "High Tech Neon Architecture",
                badgeClass: "bg-brand-green/10 text-brand-green border-brand-green/20",
                title: "Fast. Minimalist.<br><span class='text-brand-green'>Futuristic Tech Splicing.</span>",
                desc: "An advanced neon layout structured with high-tech coding styles. Ideal for software platforms and gaming setups.",
                timeText: "3-5 Business Days Delivery",
                btnClass: "glossy-green text-white",
                viewportBg: "bg-[#0d0d0e] text-white border border-brand-green/20"
            },
            minimal: {
                id: 'design-minimal',
                price: 3999,
                logoText: "ALABASTER.",
                logoClass: "text-white",
                badgeText: "Fluid Minimalist Canvas",
                badgeClass: "bg-white/10 text-white border-white/20",
                title: "Clean. Crisp.<br><span class='text-gray-300'>Alabaster Structure.</span>",
                desc: "Clean light elements over a solid gray grid. Designed for extreme legibility, crisp typography, and e-commerce elegance.",
                timeText: "5-7 Business Days Delivery",
                btnClass: "glossy-black text-white",
                viewportBg: "bg-white text-brand-slateBlack border border-black/10"
            }
        };

        /* --- App State --- */
        let currentFNO = 'all';
        let currentSpeedRange = 'all';
        let selectedPackage = null;
        let selectedDesign = null;
        let currentModalStep = 1;
        let activeAddons = { router: false, ip: false };
        let checkoutType = 'host'; /* 'host' or 'design' */

        /* IntersectionObserver for tracking active sections in the viewport */
        window.addEventListener('DOMContentLoaded', () => {
            renderPackages();
            setupSearchAutocomplete();
            setupScrollSpy();
        });

        function setupScrollSpy() {
            const badgeEl = document.getElementById('dynamic-nav-badge');
            
            const observerOptions = {
                root: null,
                rootMargin: '-35% 0px -45% 0px',
                threshold: 0
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const id = entry.target.id;
                        if (id === 'home-hero') {
                            badgeEl.innerHTML = `ANGWA<span class="text-brand-gold">.</span>`;
                        } else if (id === 'packages') {
                            badgeEl.innerHTML = `ANGWA <span class="text-brand-gold text-xs tracking-widest font-black ml-1.5 px-2 py-0.5 border border-brand-gold/30 rounded-full bg-brand-gold/10">HOST</span>`;
                        } else if (id === 'design-suite') {
                            badgeEl.innerHTML = `ANGWA <span class="text-brand-gold text-xs tracking-widest font-black ml-1.5 px-2 py-0.5 border border-brand-gold/30 rounded-full bg-brand-gold/10">DESIGN</span>`;
                        } else if (id === 'cloud-filling') {
                            badgeEl.innerHTML = `ANGWA <span class="text-brand-gold text-xs tracking-widest font-black ml-1.5 px-2 py-0.5 border border-brand-gold/30 rounded-full bg-brand-gold/10">CLOUD</span>`;
                        }
                    }
                });
            }, observerOptions);

            document.querySelectorAll('section[id]').forEach(section => {
                observer.observe(section);
            });
        }

        /* Select Web Design from architecture grid */
        function selectWebDesign(themeKey) {
            const data = designData[themeKey];
            if (!data) return;

            document.querySelectorAll('.design-selector-card').forEach(card => {
                card.className = "design-selector-card cursor-pointer p-5 rounded-2xl border bg-brand-darkGray/20 border-white/5 shadow-lg hover:border-brand-gold/50 transition-all duration-300 relative overflow-hidden";
            });

            const activeCard = document.getElementById(`card-design-${themeKey}`);
            if (activeCard) {
                const borderClass = themeKey === 'luxe' ? 'border-brand-gold/40' : (themeKey === 'emerald' ? 'border-brand-green/40' : 'border-white/30');
                activeCard.className = `design-selector-card cursor-pointer p-5 rounded-2xl border bg-brand-darkGray/60 ${borderClass} shadow-lg transition-all duration-300 relative overflow-hidden`;
            }

            const viewport = document.getElementById('live-web-viewport');
            viewport.className = `${data.viewportBg} p-6 sm:p-10 rounded-2xl min-h-[420px] flex flex-col justify-between transition-all duration-500 relative overflow-hidden`;

            const logoEl = document.getElementById('mockup-logo');
            logoEl.className = `text-xs font-black tracking-tight flex items-center gap-1.5 ${data.logoClass}`;
            logoEl.innerHTML = `
                <span class="h-5 w-5 bg-gradient-to-r ${themeKey === 'luxe' ? 'from-brand-gold to-brand-goldDark text-brand-black' : (themeKey === 'emerald' ? 'from-brand-green to-brand-greenDark text-white' : 'from-white to-gray-400 text-brand-black')} rounded-md flex items-center justify-center text-[10px] font-black">${themeKey.substring(0,1).toUpperCase()}</span> 
                <span>${data.logoText}</span>
            `;

            const badgeEl = document.getElementById('mockup-badge');
            badgeEl.innerText = data.badgeText;
            badgeEl.className = `inline-block text-[8px] tracking-widest font-bold uppercase px-2.5 py-1 rounded-full ${data.badgeClass}`;

            document.getElementById('mockup-title').innerHTML = data.title;
            document.getElementById('mockup-desc').innerText = data.desc;
            document.getElementById('mockup-time').innerText = data.timeText;

            const btnEl = document.getElementById('mockup-btn');
            btnEl.className = `${data.btnClass} text-[10px] font-black tracking-wider uppercase px-5 py-2.5 rounded-full shadow-md flex items-center gap-1.5`;
        }

        /* Simulate page reload inside sandbox browser container */
        function simulateReload() {
            const viewport = document.getElementById('live-web-viewport');
            viewport.style.opacity = '0.1';
            viewport.style.transform = 'scale(0.98)';
            
            setTimeout(() => {
                viewport.style.opacity = '1';
                viewport.style.transform = 'scale(1)';
            }, 300);
        }

        /* --- Render Symmetrical Fibre Packages --- */
        function renderPackages() {
            const container = document.getElementById('packages-container');
            container.innerHTML = '';

            let filtered = packageData;

            if (currentFNO !== 'all') {
                filtered = filtered.filter(p => p.provider === currentFNO);
            }

            if (currentSpeedRange !== 'all') {
                if (currentSpeedRange === 'budget') {
                    filtered = filtered.filter(p => p.down >= 30 && p.down <= 50);
                } else if (currentSpeedRange === 'medium') {
                    filtered = filtered.filter(p => p.down >= 100 && p.down <= 200);
                } else if (currentSpeedRange === 'pro') {
                    filtered = filtered.filter(p => p.down >= 500);
                }
            }

            if (filtered.length === 0) {
                container.innerHTML = `
                    <div class="col-span-full text-center py-16 bg-white rounded-3xl border border-black/5 shadow-inner">
                        <i class="fa-solid fa-triangle-exclamation text-4xl text-brand-gold mb-4"></i>
                        <p class="font-bold text-brand-black text-sm">No Symmetrical Packages Found.</p>
                        <p class="text-xs text-gray-400 mt-1">Try resetting the carrier selection tab.</p>
                    </div>
                `;
                return;
            }

            filtered.forEach(pkg => {
                const isVuma = pkg.provider === 'vuma';
                const isFrog = pkg.provider === 'frog';
                const providerName = isVuma ? 'Vumatel Network' : (isFrog ? 'Frogfoot Network' : 'Openserve Network');
                
                const cardAccentBorder = pkg.isPopular ? 'gold-sheen-border' : 'border border-black/5 shadow-sm';
                const popBadge = pkg.isPopular ? `
                    <div class="absolute -top-3.5 left-6 bg-gradient-to-r from-brand-gold via-brand-goldLight to-brand-goldDark text-brand-black text-[9px] uppercase font-black px-3.5 py-1.5 rounded-full tracking-wider shadow-sm">
                        Top Symmetrical Pick
                    </div>
                ` : '';

                const cardHtml = `
                    <div class="bg-white rounded-3xl p-7 relative flex flex-col justify-between hover:shadow-xl hover:scale-[1.01] transition-all duration-300 ${cardAccentBorder}">
                        ${popBadge}
                        
                        <div class="space-y-4">
                            <div class="flex items-center justify-between">
                                <span class="text-[10px] font-bold uppercase tracking-wider text-brand-goldDark flex items-center gap-1.5">
                                    <span class="h-2 w-2 rounded-full bg-brand-gold shadow-[0_0_6px_#D4AF37]"></span>
                                    ${providerName}
                                </span>
                                <span class="text-[9px] uppercase font-bold bg-brand-lightBg px-3 py-1 rounded-full text-gray-500">Uncapped</span>
                            </div>

                            <div>
                                <h3 class="text-lg font-extrabold text-brand-black tracking-tight">${pkg.name}</h3>
                                <div class="flex items-baseline gap-1.5 mt-2">
                                    <span class="text-3xl font-black text-brand-black tracking-tight">${pkg.down}</span>
                                    <span class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">Mbps Down & Up Symmetrical</span>
                                </div>
                            </div>

                            <p class="text-xs text-gray-500 leading-relaxed min-h-[48px]">
                                ${pkg.description}
                            </p>

                            <div class="space-y-2.5 border-t border-black/5 pt-5 text-xs text-gray-600">
                                <div class="flex items-center gap-2.5">
                                    <i class="fa-solid fa-infinity text-brand-gold"></i>
                                    <span>Uncapped & Unshaped Pure Bandwidth</span>
                                </div>
                                <div class="flex items-center gap-2.5">
                                    <i class="fa-solid fa-box text-brand-gold"></i>
                                    <span>Pre-configured Wi-Fi 6 Router Included</span>
                                </div>
                                <div class="flex items-center gap-2.5">
                                    <i class="fa-solid fa-circle-check text-brand-green"></i>
                                    <span>Free Installation & Connection SLA</span>
                                </div>
                            </div>
                        </div>

                        <div class="mt-8 pt-5 border-t border-black/5 flex items-center justify-between">
                            <div>
                                <span class="text-2xl font-black text-brand-black tracking-tight">R${pkg.price}</span>
                                <span class="text-[9px] text-gray-400 font-bold uppercase block tracking-wider">per month</span>
                            </div>
                            <button onclick="openSignupModal(${pkg.id})" class="glossy-black text-white px-5 py-2.5 rounded-full font-bold text-xs tracking-wider uppercase shadow-md flex items-center gap-2">
                                <span>Sign Up Free</span>
                                <i class="fa-solid fa-arrow-right-long text-brand-gold"></i>
                            </button>
                        </div>
                    </div>
                `;
                container.innerHTML += cardHtml;
            });
        }

        function setFNO(provider) {
            currentFNO = provider;
            
            document.querySelectorAll('.fno-tab').forEach(tab => {
                tab.className = "fno-tab flex-1 px-5 py-2.5 rounded-xl font-bold text-xs tracking-wider uppercase transition-all text-gray-500 hover:bg-white/50";
            });

            const activeTab = document.getElementById(`tab-${provider}`);
            if (activeTab) {
                activeTab.className = "fno-tab flex-1 px-5 py-2.5 rounded-xl font-bold text-xs tracking-wider uppercase transition-all text-brand-goldDark bg-white shadow-sm";
            }

            renderPackages();
        }

        function filterSpeedRange(range) {
            currentSpeedRange = range;

            document.querySelectorAll('.speed-filter-btn').forEach(btn => {
                btn.className = "speed-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-black/10 bg-white text-gray-600 hover:border-brand-gold transition-all shadow-sm";
            });

            const activeBtn = document.getElementById(`btn-speed-${range}`);
            if (activeBtn) {
                activeBtn.className = "speed-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-brand-black bg-brand-black text-white transition-all shadow-sm";
            }

            renderPackages();
        }

        function toggleFaq(btn) {
            const containerBox = btn.nextElementSibling;
            const indicatorIcon = btn.querySelector('i');

            if (containerBox.classList.contains('hidden')) {
                containerBox.classList.remove('hidden');
                indicatorIcon.className = "fa-solid fa-chevron-up transition-transform text-brand-gold";
            } else {
                containerBox.classList.add('hidden');
                indicatorIcon.className = "fa-solid fa-chevron-down transition-transform";
            }
        }

        /* Coverage search with autocomplete setup */
        function setupSearchAutocomplete() {
            const inputField = document.getElementById('area-search');
            const dropDownContainer = document.getElementById('search-dropdown');

            inputField.addEventListener('input', () => {
                const inputVal = inputField.value.trim().toLowerCase();
                dropDownContainer.innerHTML = '';

                if (!inputVal) {
                    dropDownContainer.classList.add('hidden');
                    return;
                }

                const matches = mockAreas.filter(area => area.name.toLowerCase().includes(inputVal));

                if (matches.length === 0) {
                    dropDownContainer.innerHTML = `
                        <div class="p-3.5 text-xs text-gray-400">
                            No Listed Coverage Match. Run a Manual Carrier Analysis check!
                        </div>
                    `;
                } else {
                    matches.forEach(match => {
                        const itemDiv = document.createElement('div');
                        itemDiv.className = "p-3 hover:bg-white/5 cursor-pointer flex justify-between items-center transition-all border-b border-white/5 last:border-b-0";
                        itemDiv.innerHTML = `
                            <span class="font-bold text-white text-xs">${match.name}</span>
                            <span class="text-[9px] bg-brand-green/10 text-brand-green font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wide">Fibre Active</span>
                        `;
                        itemDiv.onclick = () => {
                            inputField.value = match.name;
                            dropDownContainer.classList.add('hidden');
                            displaySearchResult(match);
                        };
                        dropDownContainer.appendChild(itemDiv);
                    });
                }
                dropDownContainer.classList.remove('hidden');
            });

            document.addEventListener('click', (e) => {
                if (!inputField.contains(e.target) && !dropDownContainer.contains(e.target)) {
                    dropDownContainer.classList.add('hidden');
                }
            });
        }

        function triggerSearch() {
            const searchVal = document.getElementById('area-search').value.trim();

            if (!searchVal) {
                displaySearchFeedback("Please indicate a valid street, suburb, or estate location.", false);
                return;
            }

            const registeredMatch = mockAreas.find(a => a.name.toLowerCase() === searchVal.toLowerCase());
            if (registeredMatch) {
                displaySearchResult(registeredMatch);
            } else {
                displaySearchResult({
                    name: searchVal,
                    state: 'available',
                    provider: 'Openserve Carrier Symmetrical Splicing',
                    speed: '1000 Mbps'
                });
            }
        }

        function displaySearchResult(matchData) {
            const resultsDiv = document.getElementById('search-result');
            resultsDiv.classList.remove('hidden');

            if (matchData.state === 'available') {
                resultsDiv.className = "mt-6 p-5 rounded-2xl border border-brand-green/20 bg-brand-green/5 text-gray-300";
                resultsDiv.innerHTML = `
                    <div class="flex items-start gap-3 text-xs">
                        <div class="h-8 w-8 bg-brand-green/15 rounded-lg flex items-center justify-center text-brand-green text-lg shrink-0 shadow-inner">
                            <i class="fa-solid fa-wifi"></i>
                        </div>
                        <div class="space-y-1.5 flex-1">
                            <h5 class="font-bold text-white text-sm">Light Speed Active in ${matchData.name}!</h5>
                            <p class="text-gray-400">The primary local network connection operator is <span class="text-brand-gold font-bold">${matchData.provider}</span> with speeds configured up to <span class="text-white font-bold">${matchData.speed}</span>.</p>
                            <div class="pt-3">
                                <button onclick="autoSelectProvider('${matchData.provider}')" class="bg-brand-green hover:bg-brand-greenDark text-white px-4 py-2 rounded-full font-bold text-[10px] tracking-wider uppercase transition-colors">
                                    Show Symmetrical Packages
                                </button>
                            </div>
                        </div>
                    </div>
                `;
            } else {
                resultsDiv.className = "mt-6 p-5 rounded-2xl border border-brand-gold/20 bg-brand-gold/5 text-gray-300";
                resultsDiv.innerHTML = `
                    <div class="flex items-start gap-3 text-xs">
                        <div class="h-8 w-8 bg-brand-gold/15 rounded-lg flex items-center justify-center text-brand-gold text-lg shrink-0 shadow-inner">
                            <i class="fa-solid fa-clock-rotate-left"></i>
                        </div>
                        <div class="space-y-1">
                            <h5 class="font-bold text-white text-sm">Deployment Pending in ${matchData.name}</h5>
                            <p class="text-gray-400">Lines are currently being spliced in your neighborhood! Pre-register to lock down free routing hardware installation slots early.</p>
                        </div>
                    </div>
                `;
            }
        }

        function displaySearchFeedback(msg, isSuccess) {
            const resultsDiv = document.getElementById('search-result');
            resultsDiv.classList.remove('hidden');
            resultsDiv.className = isSuccess ? "mt-6 p-4 rounded-2xl border border-brand-green/20 bg-brand-green/5 text-brand-green text-xs font-semibold" : "mt-6 p-4 rounded-2xl border border-red-500/20 bg-red-500/5 text-red-400 text-xs font-semibold";
            resultsDiv.innerHTML = msg;
        }

        function autoSelectProvider(providerName) {
            const simpleName = providerName.toLowerCase();
            if (simpleName.includes('vuma')) {
                setFNO('vuma');
            } else if (simpleName.includes('open')) {
                setFNO('open');
            } else if (simpleName.includes('frog')) {
                setFNO('frog');
            } else {
                setFNO('all');
            }
            document.getElementById('packages').scrollIntoView({ behavior: 'smooth' });
        }

        function openSignupModal(packageId) {
            checkoutType = 'host';
            selectedPackage = packageData.find(p => p.id === packageId);
            if (!selectedPackage) return;

            currentModalStep = 1;
            activeAddons = { router: false, ip: false };
            document.getElementById('addon-router').checked = false;
            document.getElementById('addon-ip').checked = false;

            document.getElementById('modal-package-name').innerText = selectedPackage.name;
            document.getElementById('modal-package-price').innerText = `R${selectedPackage.price}.00`;
            document.getElementById('modal-package-subtitle').innerText = "Monthly Symmetrical Fibre Premium";
            document.getElementById('modal-upgrade-header').innerText = "Upgrade Hardware & Configuration";
            
            document.getElementById('addon-router-title').innerText = "Upgrade to Wi-Fi 6 Pro System";
            document.getElementById('addon-router-desc').innerText = "Enhance transmission rates across concrete walls.";
            document.getElementById('addon-router-price').innerText = "+R99/pm";
            
            document.getElementById('addon-ip-title').innerText = "Fixed Dedicated Static IP";
            document.getElementById('addon-ip-desc').innerText = "Ideal for running servers, secure logins or smart systems.";
            document.getElementById('addon-ip-price').innerText = "+R49/pm";

            document.getElementById('modal-address-label').innerText = "Premises Address";
            document.getElementById('cust-address').placeholder = "Unit 5, Sandhurst Ridge Complex";

            document.getElementById('modal-success-title').innerText = "System Configuration Confirmed";
            document.getElementById('modal-success-desc').innerText = "No upfront charges are required. Payment logic only starts when physical line activation is confirmed.";

            document.getElementById('summary-base-label').innerText = "Standard Base Fee:";
            document.getElementById('summary-addon-router-label').innerText = "Wi-Fi 6 Pro Upgrade:";
            document.getElementById('summary-addon-router-price-val').innerText = "+R99.00";
            document.getElementById('summary-addon-ip-label').innerText = "Fixed Static IP allocation:";
            document.getElementById('summary-addon-ip-price-val').innerText = "+R49.00";
            document.getElementById('summary-total-label').innerText = "Active Monthly Subtotal:";
            document.getElementById('modal-pricing-label').innerText = "Monthly Cost:";

            updateModalStepsUI();
            calculateModalTotal();

            document.getElementById('signup-modal').classList.remove('hidden');
        }

        function openDesignSignupModal(themeKey) {
            checkoutType = 'design';
            selectedDesign = designData[themeKey];
            if (!selectedDesign) return;

            currentModalStep = 1;
            activeAddons = { router: false, ip: false };
            document.getElementById('addon-router').checked = false;
            document.getElementById('addon-ip').checked = false;

            document.getElementById('modal-package-name').innerText = "Design Portfolio: " + selectedDesign.logoText.replace('.', '');
            document.getElementById('modal-package-price').innerText = `R${selectedDesign.price}.00`;
            document.getElementById('modal-package-subtitle').innerText = selectedDesign.badgeText + " Setup";
            document.getElementById('modal-upgrade-header').innerText = "Configure Digital Deliverables & Core Hosting";

            document.getElementById('addon-router-title').innerText = "Premium High-Performance Light Hosting";
            document.getElementById('addon-router-desc').innerText = "Spliced directly onto premium server nodes with weekly cloud back-ups.";
            document.getElementById('addon-router-price').innerText = "+R199/pm";
            
            document.getElementById('addon-ip-title').innerText = "Custom Domain Acquisition (.co.za / .com)";
            document.getElementById('addon-ip-desc').innerText = "Secure registered names matching your direct portfolio aesthetics.";
            document.getElementById('addon-ip-price').innerText = "+R250 once-off";

            document.getElementById('modal-address-label').innerText = "Requested Domain Name";
            document.getElementById('cust-address').placeholder = "e.g. yourcompanyname.co.za";

            document.getElementById('modal-success-title').innerText = "Creative Design Blueprint Registered";
            document.getElementById('modal-success-desc').innerText = "Our creative directors will contact you to plan layout modules and responsive frameworks within 24 hours.";

            document.getElementById('summary-base-label').innerText = "Creative Layout Design Fee:";
            document.getElementById('summary-addon-router-label').innerText = "High-Performance Cloud Hosting:";
            document.getElementById('summary-addon-router-price-val').innerText = "+R199/pm";
            document.getElementById('summary-addon-ip-label').innerText = "Custom Domain Registration:";
            document.getElementById('summary-addon-ip-price-val').innerText = "+R250.00";
            document.getElementById('summary-total-label').innerText = "Total Architecture Subtotal:";
            document.getElementById('modal-pricing-label').innerText = "Estimated Total:";

            updateModalStepsUI();
            calculateModalTotal();

            document.getElementById('signup-modal').classList.remove('hidden');
        }

        function closeModal() {
            document.getElementById('signup-modal').classList.add('hidden');
        }

        function calculateModalTotal() {
            activeAddons.router = document.getElementById('addon-router').checked;
            activeAddons.ip = document.getElementById('addon-ip').checked;

            let basePrice = checkoutType === 'host' ? selectedPackage.price : selectedDesign.price;
            let totalVal = basePrice;
            
            if (checkoutType === 'host') {
                if (activeAddons.router) totalVal += 99;
                if (activeAddons.ip) totalVal += 49;
            } else {
                if (activeAddons.router) totalVal += 199;
                if (activeAddons.ip) totalVal += 250;
            }

            document.getElementById('modal-footer-price').innerText = `R${totalVal}.00`;
            document.getElementById('summary-total-price').innerText = `R${totalVal}.00`;
            document.getElementById('summary-pkg-price').innerText = `R${basePrice}.00`;

            if (activeAddons.router) {
                document.getElementById('summary-addon-router-row').classList.remove('hidden');
            } else {
                document.getElementById('summary-addon-router-row').classList.add('hidden');
            }

            if (activeAddons.ip) {
                document.getElementById('summary-addon-ip-row').classList.remove('hidden');
            } else {
                document.getElementById('summary-addon-ip-row').classList.add('hidden');
            }
        }

        function updateModalStepsUI() {
            document.getElementById('modal-step-1').classList.add('hidden');
            document.getElementById('modal-step-2').classList.add('hidden');
            document.getElementById('modal-step-3').classList.add('hidden');

            document.getElementById(`modal-step-${currentModalStep}`).classList.remove('hidden');

            const backBtn = document.getElementById('modal-back-btn');
            if (currentModalStep === 1) {
                backBtn.classList.add('hidden');
            } else {
                backBtn.classList.remove('hidden');
            }

            /* Dynamic Polar.sh Sandbox Link formulation based on checkout options */
            let checkoutLink = "https://sandbox.polar.sh/checkout/new?org=angwa";
            if (checkoutType === 'host' && selectedPackage) {
                checkoutLink = `https://sandbox.polar.sh/checkout/new?product=host-${selectedPackage.id}&amount=${selectedPackage.price}`;
            } else if (checkoutType === 'design' && selectedDesign) {
                checkoutLink = `https://sandbox.polar.sh/checkout/new?product=${selectedDesign.id}&amount=${selectedDesign.price}`;
            }

            const nextBtnContainer = document.getElementById('modal-next-btn-container');
            if (currentModalStep === 3) {
                nextBtnContainer.innerHTML = `
                    <a href="${checkoutLink}" id="modal-next-btn" data-polar-checkout data-polar-checkout-theme="dark" class="glossy-green text-white px-6 py-2.5 rounded-full font-bold text-xs tracking-wider uppercase shadow-md inline-flex items-center gap-1.5 cursor-pointer no-underline select-none">
                        <span>Pay with Polar</span> <i class="fa-solid fa-shield-halved text-brand-gold text-[10px]"></i>
                    </a>
                `;
                if (window.PolarEmbedCheckout) {
                    setTimeout(() => {
                        window.PolarEmbedCheckout.init();
                    }, 60);
                }
            } else {
                nextBtnContainer.innerHTML = `
                    <button id="modal-next-btn" onclick="nextStep()" class="glossy-gold text-brand-black px-6 py-2.5 rounded-full font-bold text-xs tracking-wider uppercase shadow-md">
                        Continue <i class="fa-solid fa-chevron-right ml-1"></i>
                    </button>
                `;
            }

            for (let i = 1; i <= 3; i++) {
                const indicator = document.getElementById(`step-indicator-${i}`);
                if (i === currentModalStep) {
                    indicator.className = "text-brand-gold flex items-center gap-1.5";
                    indicator.querySelector('span').className = "h-4.5 w-4.5 rounded-full bg-brand-gold/20 text-brand-gold flex items-center justify-center text-[9px] font-black";
                } else if (i < currentModalStep) {
                    indicator.className = "text-brand-green flex items-center gap-1.5";
                    indicator.querySelector('span').className = "h-4.5 w-4.5 rounded-full bg-brand-green/20 text-brand-green flex items-center justify-center text-[9px] font-black";
                } else {
                    indicator.className = "text-gray-500 flex items-center gap-1.5";
                    indicator.querySelector('span').className = "h-4.5 w-4.5 rounded-full bg-white/5 text-gray-500 flex items-center justify-center text-[9px]";
                }
            }
        }

        function nextStep() {
            if (currentModalStep === 1) {
                currentModalStep = 2;
                updateModalStepsUI();
            } else if (currentModalStep === 2) {
                const nameInput = document.getElementById('cust-name').value.trim();
                const emailInput = document.getElementById('cust-email').value.trim();
                const addrInput = document.getElementById('cust-address').value.trim();

                if (!nameInput || !emailInput || !addrInput) {
                    alertModal("Please complete all setup destination fields before progressing.");
                    return;
                }

                currentModalStep = 3;
                updateModalStepsUI();
            } else if (currentModalStep === 3) {
                closeModal();
                showOrderToast();
            }
        }

        function prevStep() {
            if (currentModalStep > 1) {
                currentModalStep--;
                updateModalStepsUI();
            }
        }

        function alertModal(msg) {
            const alertBox = document.createElement('div');
            alertBox.className = "fixed inset-0 bg-brand-black/70 z-[100] flex items-center justify-center p-4 backdrop-blur-sm";
            alertBox.innerHTML = `
                <div class="bg-brand-darkGray p-6 rounded-3xl max-w-sm w-full space-y-4 text-center border border-white/10 text-white shadow-2xl">
                    <div class="h-12 w-12 bg-brand-gold/15 text-brand-gold rounded-full flex items-center justify-center text-xl mx-auto">
                        <i class="fa-solid fa-triangle-exclamation"></i>
                    </div>
                    <h4 class="font-bold text-sm tracking-wide">Incomplete Configuration</h4>
                    <p class="text-[11px] text-gray-400 leading-relaxed">${msg}</p>
                    <button onclick="this.parentElement.parentElement.remove()" class="w-full glossy-gold text-brand-black py-2.5 rounded-full font-bold text-xs uppercase tracking-wider">Acknowledge</button>
                </div>
            `;
            document.body.appendChild(alertBox);
        }

        function showOrderToast() {
            const toast = document.getElementById('order-toast');
            toast.classList.remove('hidden');
            setTimeout(() => {
                hideOrderToast();
            }, 6500);
        }

        function hideOrderToast() {
            document.getElementById('order-toast').classList.add('hidden');
        }

        /* --- Cloud Filling Dropdown and Sync Simulator --- */
        function triggerCloudSync(provider) {
            const cloudIcon = document.getElementById('cloud-icon');
            const statusText = document.getElementById('cloud-sync-status');
            const progress = document.getElementById('cloud-progress-bar');
            const timer = document.getElementById('cloud-timer-val');

            const panelRate = document.getElementById('panel-sync-rate');
            const panelProgress = document.getElementById('panel-progress-bar');
            const panelStatus = document.getElementById('panel-sync-status');
            const panelTimer = document.getElementById('panel-sync-timer');

            if (provider === 'dropbox') {
                if (cloudIcon) cloudIcon.className = "fa-brands fa-dropbox text-blue-400";
                if (statusText) statusText.innerText = "Connecting to Dropbox Fibre pipeline...";
                panelStatus.innerText = "Splicing optical connection to Dropbox central nodes...";
            } else {
                if (cloudIcon) cloudIcon.className = "fa-brands fa-google-drive text-green-400";
                if (statusText) statusText.innerText = "Connecting to Google Drive high-speed backup system...";
                panelStatus.innerText = "Securing direct cloud handshake with Google clusters...";
            }

            document.getElementById('cloud-sync-modal').classList.remove('hidden');
            panelRate.innerText = "1,000 Mbps";

            let width = 0;
            if (progress) progress.style.width = '0%';
            panelProgress.style.width = '0%';
            if (timer) timer.innerText = "6.2 seconds remaining";
            panelTimer.innerText = "6.2s left";

            const interval = setInterval(() => {
                width += 10;
                if (progress) progress.style.width = `${width}%`;
                panelProgress.style.width = `${width}%`;
                
                const timeLeft = Math.max(0, ((100 - width) / 15).toFixed(1));
                if (timer) timer.innerText = `${timeLeft} seconds remaining`;
                panelTimer.innerText = `${timeLeft}s left`;

                if (width === 40) {
                    if (statusText) statusText.innerText = `Encrypting file systems with symmetrical light speed...`;
                    panelStatus.innerText = "Sending secure multi-threaded file chunks...";
                } else if (width === 80) {
                    if (statusText) statusText.innerText = `Finalizing cloud handshake metrics...`;
                    panelStatus.innerText = "Assembling directory structures on destination server...";
                }

                if (width >= 100) {
                    clearInterval(interval);
                    if (statusText) statusText.innerText = "Sync complete! 50GB file database successfully uploaded in 0.8 seconds.";
                    panelStatus.innerText = "Upload complete! 50GB mapped successfully in 0.8s.";
                    if (timer) timer.innerText = "Success - 0.0 seconds remaining";
                    panelTimer.innerText = "Success";
                    panelRate.innerText = "0 Mbps (Idle)";
                }
            }, 250);
        }

        function closeCloudModal() {
            document.getElementById('cloud-sync-modal').classList.add('hidden');
        }

        /* --- ClientZone simulation triggers --- */
        function triggerClientZone() {
            document.getElementById('clientzone-modal').classList.remove('hidden');
        }

        function closeClientZone() {
            document.getElementById('clientzone-modal').classList.add('hidden');
        }

        function submitClientZoneMock() {
            closeClientZone();
            const welcomeBox = document.createElement('div');
            welcomeBox.className = "fixed inset-0 bg-brand-black/70 z-[100] flex items-center justify-center p-4 backdrop-blur-sm";
            welcomeBox.innerHTML = `
                <div class="bg-brand-darkGray p-6 rounded-3xl max-w-sm w-full space-y-4 text-center border border-white/10 text-white shadow-2xl">
                    <div class="h-12 w-12 bg-brand-green/15 text-brand-green rounded-full flex items-center justify-center text-xl mx-auto shadow-inner">
                        <i class="fa-solid fa-circle-check"></i>
                    </div>
                    <h4 class="font-bold text-sm tracking-wide">ClientZone Connected</h4>
                    <p class="text-[11px] text-gray-400 leading-relaxed">Welcome back. Secure subscriber credentials authenticated successfully.</p>
                    <button onclick="this.parentElement.parentElement.remove()" class="w-full glossy-gold text-brand-black py-2.5 rounded-full font-bold text-xs uppercase tracking-wider">Launch Dashboard</button>
                </div>
            `;
            document.body.appendChild(welcomeBox);
        }

        /* --- Support chat controls --- */
        function toggleLiveChat() {
            const chatBox = document.getElementById('chat-popup');
            if (chatBox.classList.contains('hidden')) {
                chatBox.classList.remove('hidden');
            } else {
                chatBox.classList.add('hidden');
            }
        }

        function handleChatSubmit(e) {
            if (e.key === 'Enter') {
                sendChatMessage();
            }
        }

        function sendChatMessage() {
            const inputField = document.getElementById('chat-input');
            const userMsg = inputField.value.trim();
            if (!userMsg) return;

            const chatMessagesContainer = document.getElementById('chat-messages');

            const divUser = document.createElement('div');
            divUser.className = "bg-gradient-to-r from-brand-goldDark to-brand-gold text-brand-black font-semibold p-3 rounded-2xl text-[11px] max-w-[85%] self-end ml-auto mb-2.5 leading-relaxed shadow-sm";
            divUser.innerText = userMsg;
            chatMessagesContainer.appendChild(divUser);

            inputField.value = '';
            chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;

            setTimeout(() => {
                const divAgent = document.createElement('div');
                divAgent.className = "bg-brand-darkGray/60 p-3 rounded-2xl border border-white/5 text-gray-300 max-w-[85%] mb-2.5 leading-relaxed";
                
                const lowerInput = userMsg.toLowerCase();
                if (lowerInput.includes('price') || lowerInput.includes('cost') || lowerInput.includes('rand')) {
                    divAgent.innerText = "All our hosting templates are month-to-month and fully transparent! Symmetrical Openserve setups start at R499/pm and bespoke creative design portfolios start at R3,999 once-off. Which speed or layout is your target?";
                } else if (lowerInput.includes('vuma') || lowerInput.includes('openserve') || lowerInput.includes('frogfoot')) {
                    divAgent.innerText = "We provide direct Symmetrical options on those providers. Try running your physical address inside the Coverage search tool above to verify!";
                } else {
                    divAgent.innerText = "Understood. The most efficient way is to enter your street location in the Availability Check at the top. It identifies exact active fibre splicing grids and matching layouts instantly.";
                }

                chatMessagesContainer.appendChild(divAgent);
                chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
            }, 1100);
        }
    </script>
</body>
</html>
"""

components.html(html_content, height=1000, scrolling=True)