import streamlit as st

# Configure the page immediately to support a premium layout and custom window headers
st.set_page_config(
    page_title="Premium afrihost | Managed Web Masterpieces",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize interactive variables in session state to handle live pricing, custom previews, and inquiries
if "extra_pages" not in st.session_state:
    st.session_state.extra_pages = 3
if "selected_tier" not in st.session_state:
    st.session_state.selected_tier = "Signature"
if "billing_cycle" not in st.session_state:
    st.session_state.billing_cycle = "Monthly"
if "seo_premium" not in st.session_state:
    st.session_state.seo_premium = True
if "speed_opt" not in st.session_state:
    st.session_state.speed_opt = True
if "preview_brand_name" not in st.session_state:
    st.session_state.preview_brand_name = "Aura Wellness"
if "preview_theme" not in st.session_state:
    st.session_state.preview_theme = "Luxurious Cream"
if "inquiry_submitted" not in st.session_state:
    st.session_state.inquiry_submitted = False

def inject_master_styles():
    """Injects a master CSS block that handles total layout overrides, spacing reduction, and custom element design."""
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:ital,wght@0,400;0,700;1,400;1,700&display=swap');
            
            :root {
                --theme-gold: #c5a022;
                --theme-gold-hover: #e5bd35;
                --theme-green: #064e3b;
                --theme-cream: #fdfcf0;
                --theme-black: #0a0a0a;
                --theme-white: #ffffff;
                --theme-gray-light: #f5f5f0;
                --theme-border-gold: rgba(197, 160, 34, 0.2);
            }

            /* --- GLOBAL VERTICAL FLOW OVERRIDES --- */
            [data-testid="stAppViewContainer"] {
                background-color: var(--theme-white) !important;
                padding-top: 5.5rem !important; /* Make precise space for fixed header */
            }
            [data-testid="stHeader"] {
                display: none !important; /* Remove native streamlit header to prevent visual overlap */
                background: transparent !important;
            }
            .main > span, .main > span > span {
                padding-top: 0px !important;
                padding-bottom: 0px !important;
            }
            [data-testid="stVerticalBlock"] {
                gap: 0px !important;
                padding: 0px !important;
            }
            [data-testid="stVerticalBlockBorderWrapper"] {
                margin: 0px !important;
                padding: 0px !important;
            }

            /* --- SYMMETRICAL COLUMNS & EQUAL SIZING --- */
            [data-testid="stHorizontalBlock"] {
                align-items: stretch !important;
                gap: 2rem !important;
                padding-top: 2rem !important;
                padding-bottom: 2rem !important;
            }
            [data-testid="stColumn"] {
                display: flex !important;
                flex-direction: column !important;
                height: 100% !important;
            }
            [data-testid="stColumn"] > span {
                flex: 1 !important;
                display: flex !important;
                flex-direction: column !important;
                height: 100% !important;
            }

            /* --- CONTAINER CONTAINMENT (:HAS() PARENT TRIGGERS) --- */
            
            /* Navbar Container - Styled as fixed layout banner */
            [data-testid="stHorizontalBlock"]:has(.navbar-trigger) {
                background-color: rgba(255, 255, 255, 0.95) !important;
                backdrop-filter: blur(20px) !important;
                -webkit-backdrop-filter: blur(20px) !important;
                border-bottom: 1px solid rgba(197, 160, 34, 0.15) !important;
                padding: 1.25rem 5% !important;
                position: fixed !important;
                top: 0 !important;
                left: 0 !important;
                right: 0 !important;
                z-index: 99999 !important;
                margin: 0 auto !important;
                border-radius: 0px !important;
                width: 100vw !important;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.03) !important;
            }

            /* Hero Right Card Container */
            [data-testid="stColumn"]:has(.hero-right-trigger) {
                background-color: var(--theme-white) !important;
                border-radius: 4rem !important;
                padding: 1.25rem !important;
                box-shadow: 0 50px 100px -25px rgba(0, 0, 0, 0.12) !important;
                border: 1px solid var(--theme-gray-light) !important;
                height: 100% !important;
            }

            /* Customizer Panel Containment */
            [data-testid="stHorizontalBlock"]:has(.customizer-trigger) {
                background-color: var(--theme-cream) !important;
                padding: 4rem !important;
                border-radius: 3.5rem !important;
                border: 1px solid var(--theme-border-gold) !important;
                margin-top: 4rem !important;
                margin-bottom: 4rem !important;
            }

            /* Pricing Cards (Bronze & Gold) */
            [data-testid="stColumn"]:has(.pricing-card-1-trigger),
            [data-testid="stColumn"]:has(.pricing-card-3-trigger) {
                background-color: var(--theme-white) !important;
                border-radius: 3.5rem !important;
                padding: 4rem 3rem !important;
                border: 1px solid var(--theme-gray-light) !important;
                box-shadow: 0 30px 60px -15px rgba(0, 0, 0, 0.05) !important;
                transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
            }
            [data-testid="stColumn"]:has(.pricing-card-1-trigger):hover,
            [data-testid="stColumn"]:has(.pricing-card-3-trigger):hover {
                transform: translateY(-8px) !important;
                box-shadow: 0 45px 90px -20px rgba(197, 160, 34, 0.15) !important;
                border-color: var(--theme-gold) !important;
            }

            /* Pricing Card (Featured Silver) */
            [data-testid="stColumn"]:has(.pricing-card-2-trigger) {
                background-color: var(--theme-black) !important;
                border-radius: 3.5rem !important;
                padding: 4.5rem 3.5rem !important;
                border: 2px solid var(--theme-gold) !important;
                box-shadow: 0 45px 90px -20px rgba(6, 78, 59, 0.3) !important;
                transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
                position: relative !important;
            }
            [data-testid="stColumn"]:has(.pricing-card-2-trigger):hover {
                transform: translateY(-8px) !important;
                box-shadow: 0 60px 120px -25px rgba(6, 78, 59, 0.4) !important;
            }

            /* Mockup Sandbox Container */
            [data-testid="stHorizontalBlock"]:has(.mockup-studio-trigger) {
                background-color: rgba(253, 252, 240, 0.4) !important;
                padding: 4rem !important;
                border-radius: 3.5rem !important;
                border: 1px solid var(--theme-gray-light) !important;
                margin-top: 4rem !important;
                margin-bottom: 4rem !important;
            }

            /* Guarantee Block Containment */
            [data-testid="stHorizontalBlock"]:has(.pledge-left-trigger) {
                background-color: var(--theme-green) !important;
                padding: 6rem 5rem !important;
                border-radius: 4.5rem !important;
                margin-top: 4rem !important;
                margin-bottom: 4rem !important;
            }
            [data-testid="stColumn"]:has(.pledge-right-trigger) {
                background-color: var(--theme-white) !important;
                padding: 4rem !important;
                border-radius: 3.5rem !important;
                box-shadow: 0 40px 80px -20px rgba(0, 0, 0, 0.25) !important;
            }

            /* Consultation Portal Container */
            [data-testid="stHorizontalBlock"]:has(.consultation-trigger) {
                background-color: var(--theme-cream) !important;
                padding: 6rem !important;
                border-radius: 4rem !important;
                margin-top: 4rem !important;
                margin-bottom: 4rem !important;
                border: 1px solid var(--theme-border-gold) !important;
            }

            /* Footer Container */
            [data-testid="stHorizontalBlock"]:has(.footer-trigger) {
                background-color: var(--theme-black) !important;
                padding: 6rem 4rem 4rem 4rem !important;
                border-radius: 4rem 4rem 0px 0px !important;
                margin-top: 6rem !important;
            }

            /* --- NEW SECTION: STATS COUNTERS --- */
            .stats-container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 4rem 2rem;
                text-align: center;
            }
            .stat-card {
                background: var(--theme-white);
                padding: 2rem;
                border-radius: 2rem;
                text-align: center;
                border: 1px solid var(--theme-gray-light);
                transition: all 0.3s ease;
            }
            .stat-number {
                font-family: 'Playfair Display', serif;
                font-size: 3.5rem;
                font-weight: 900;
                color: var(--theme-gold);
                display: block;
                line-height: 1;
            }
            .stat-label {
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 0.1em;
                color: #6b7280;
                margin-top: 0.5rem;
                display: block;
            }

            /* --- NEW SECTION: TESTIMONIALS --- */
            .testimonials-container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 4rem 2rem;
            }
            .testimonial-card {
                background: var(--theme-white);
                padding: 2rem;
                border-radius: 2rem;
                border: 1px solid var(--theme-gray-light);
                height: 100%;
                transition: all 0.3s ease;
            }
            .testimonial-quote {
                font-size: 1rem;
                line-height: 1.6;
                color: #4b5563;
                font-style: italic;
                margin-bottom: 1.5rem;
                display: block;
            }
            .testimonial-author {
                display: flex;
                align-items: center;
                gap: 1rem;
            }
            .testimonial-avatar {
                width: 3rem;
                height: 3rem;
                background: linear-gradient(135deg, var(--theme-gold), var(--theme-green));
                border-radius: 1rem;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: 700;
            }
            .testimonial-name {
                font-weight: 800;
                color: var(--theme-black);
                display: block;
            }
            .testimonial-title {
                font-size: 0.8rem;
                color: #9ca3af;
                display: block;
            }

            /* --- NEW SECTION: CASE STUDIES --- */
            .case-card {
                background: var(--theme-white);
                border-radius: 2rem;
                overflow: hidden;
                border: 1px solid var(--theme-gray-light);
                transition: all 0.3s ease;
                height: 100%;
            }
            .case-image {
                height: 180px;
                background: linear-gradient(135deg, var(--theme-green), #0a5c48);
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .case-content {
                padding: 1.5rem;
            }
            .case-title {
                font-weight: 800;
                font-size: 1.2rem;
                margin-bottom: 0.5rem;
                display: block;
            }
            .case-metric {
                color: var(--theme-gold);
                font-weight: 700;
                font-size: 0.9rem;
                margin-top: 0.5rem;
                display: block;
            }

            /* --- NEW SECTION: TECHNOLOGY STACK --- */
            .tech-container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 4rem 2rem;
                text-align: center;
            }
            .tech-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
                gap: 2rem;
                margin-top: 3rem;
            }
            .tech-item {
                background: var(--theme-white);
                padding: 1.5rem;
                border-radius: 1.5rem;
                border: 1px solid var(--theme-gray-light);
                transition: all 0.3s ease;
            }
            .tech-item:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 20px -5px rgba(0,0,0,0.05);
            }

            /* --- NEW SECTION: INTERACTIVE ROADMAP --- */
            .roadmap-container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 4rem 2rem;
            }
            .roadmap-badge {
                display: inline-block;
                padding: 4px 12px;
                background: rgba(197, 160, 34, 0.1);
                border: 1px solid rgba(197, 160, 34, 0.2);
                border-radius: 9999px;
                color: var(--theme-gold);
                font-size: 10px;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.2em;
                margin-bottom: 1.5rem;
            }
            .roadmap-header {
                font-family: 'Playfair Display', serif;
                font-size: 4rem;
                font-weight: 900;
                color: var(--theme-black);
                line-height: 1.1;
                margin-bottom: 1rem;
            }
            .roadmap-subheader {
                font-family: 'Inter', sans-serif;
                color: #6b7280;
                font-size: 1.1rem;
                font-weight: 300;
                max-width: 600px;
                margin-bottom: 3rem;
            }
            .step-card {
                background: white;
                padding: 2.5rem;
                border-radius: 2rem;
                border: 1px solid #f3f4f6;
                transition: all 0.3s ease;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
                height: 100%;
                display: flex;
                flex-direction: column;
                margin-bottom: 0.5rem;
            }
            .step-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 20px 25px -12px rgba(0, 0, 0, 0.1);
            }
            .step-number {
                font-family: 'Playfair Display', serif;
                font-size: 4rem;
                color: var(--theme-gold);
                opacity: 0.15;
                display: block;
                line-height: 1;
                margin-bottom: -1rem;
            }
            .step-title {
                font-family: 'Inter', sans-serif;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.1em;
                font-size: 1.1rem;
                color: var(--theme-black);
                display: block;
                margin-bottom: 0.5rem;
            }
            .step-desc {
                font-family: 'Inter', sans-serif;
                font-size: 0.875rem;
                color: #6b7280;
                line-height: 1.6;
                display: block;
                margin-bottom: 0.5rem;
                flex-grow: 1;
            }
            .roadmap-step .stButton button {
                background-color: var(--theme-gold) !important;
                color: white !important;
                border: none !important;
                border-radius: 12px !important;
                padding: 0.5rem 1rem !important;
                font-weight: 700 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.05em !important;
                font-size: 0.7rem !important;
                transition: transform 0.2s ease, background-color 0.2s ease !important;
                width: 100% !important;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }
            .roadmap-step .stButton button:hover {
                background-color: var(--theme-green) !important;
                transform: translateY(-2px);
            }

            /* --- CUSTOM SPAN STYLING BLOCKS (SPAN-ONLY METHODOLOGY) --- */
            .font-serif {
                font-family: 'Playfair Display', serif !important;
            }
            .font-sans {
                font-family: 'Inter', sans-serif !important;
            }
            
            .badge-span {
                display: inline-block;
                padding: 0.4rem 1.2rem;
                background-color: var(--theme-cream);
                border: 1px solid rgba(197, 160, 34, 0.4);
                color: var(--theme-gold);
                font-size: 10px;
                font-weight: 900;
                letter-spacing: 0.3em;
                text-transform: uppercase;
                border-radius: 9999px;
                margin-bottom: 2rem;
                width: fit-content;
            }
            .badge-span-green {
                background-color: rgba(6, 78, 59, 0.08);
                border: 1px solid rgba(6, 78, 59, 0.2);
                color: var(--theme-green);
            }

            .heading-primary {
                font-size: 4.5rem;
                font-weight: 900;
                line-height: 0.95;
                color: var(--theme-black);
                display: block;
                letter-spacing: -0.03em;
                margin-bottom: 2rem;
            }
            .text-italic-green {
                font-style: italic;
                color: var(--theme-green);
            }
            .text-italic-gold {
                font-style: italic;
                color: var(--theme-gold);
            }
            .desc-large {
                font-size: 1.25rem;
                color: #6b7280;
                font-weight: 300;
                line-height: 1.6;
                display: block;
                max-width: 34rem;
                margin-bottom: 3rem;
            }

            /* Hero Visual Inner Elements */
            .green-card-interior {
                background-color: var(--theme-green);
                border-radius: 3.25rem;
                flex: 1;
                display: flex;
                flex-direction: column;
                justify-content: center;
                padding: 4.5rem;
                position: relative;
                overflow: hidden;
                animation: float-effect 6s ease-in-out infinite;
            }
            @keyframes float-effect {
                0%, 100% { transform: translateY(0px) rotate(-0.5deg); }
                50% { transform: translateY(-12px) rotate(0.5deg); }
            }
            .gold-bar {
                height: 6px;
                width: 5.5rem;
                background-color: var(--theme-gold);
                border-radius: 9999px;
                margin-bottom: 3rem;
                display: block;
            }
            .card-title-hero {
                font-size: 4rem;
                font-style: italic;
                font-weight: 700;
                color: var(--theme-white);
                display: block;
                line-height: 1.05;
                margin-bottom: 1.5rem;
            }
            .card-desc-hero {
                font-size: 1.15rem;
                color: rgba(255, 255, 255, 0.7);
                font-weight: 300;
                display: block;
                max-width: 20rem;
                line-height: 1.5;
            }
            .badge-float-card {
                position: absolute;
                bottom: -1rem;
                left: -1rem;
                background-color: var(--theme-white);
                padding: 1.25rem 2rem;
                border-radius: 2.25rem;
                box-shadow: 0 35px 70px -15px rgba(0,0,0,0.2);
                z-index: 50;
                display: flex;
                align-items: center;
                gap: 1.25rem;
                border: 1px solid var(--theme-gray-light);
            }
            .badge-circle-icon {
                background-color: var(--theme-green);
                width: 3.25rem;
                height: 3.25rem;
                border-radius: 1.2rem;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            /* Pricing Elements styled using custom Spans */
            .tier-sub {
                color: var(--theme-gold);
                font-weight: 900;
                letter-spacing: 0.25em;
                text-transform: uppercase;
                font-size: 11px;
                margin-bottom: 0.75rem;
                display: block;
            }
            .tier-title-light {
                font-size: 2.5rem;
                font-weight: 700;
                color: var(--theme-black);
                display: block;
                margin-bottom: 1.5rem;
            }
            .tier-title-dark {
                font-size: 2.5rem;
                font-weight: 700;
                font-style: italic;
                color: var(--theme-white);
                display: block;
                margin-bottom: 1.5rem;
            }
            .price-wrap {
                margin-bottom: 3rem;
                display: block;
            }
            .price-val-light {
                font-size: 3.75rem;
                font-weight: 700;
                color: var(--theme-black);
                display: inline-block;
            }
            .price-val-dark {
                font-size: 3.75rem;
                font-weight: 700;
                color: var(--theme-white);
                display: inline-block;
            }
            .price-cycle {
                font-style: italic;
                color: #9ca3af;
                font-size: 1.15rem;
                margin-left: 0.35rem;
                display: inline-block;
            }
            .features-list-span {
                display: flex;
                flex-direction: column;
                gap: 1.5rem;
                margin-bottom: 4rem;
            }
            .feat-line {
                display: flex;
                align-items: center;
                gap: 1rem;
            }
            .circle-icon-green {
                width: 1.75rem;
                height: 1.75rem;
                border-radius: 9999px;
                background-color: rgba(6, 78, 59, 0.08);
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .circle-icon-gold {
                width: 1.75rem;
                height: 1.75rem;
                border-radius: 9999px;
                background-color: var(--theme-gold);
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .circle-icon-dark {
                width: 1.75rem;
                height: 1.75rem;
                border-radius: 9999px;
                background-color: rgba(255, 255, 255, 0.1);
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .feat-txt-gray {
                font-size: 1rem;
                color: #4b5563;
                font-weight: 300;
            }
            .feat-txt-white {
                font-size: 1rem;
                color: rgba(255, 255, 255, 0.75);
                font-weight: 300;
            }
            .feat-txt-bold-white {
                font-size: 1rem;
                color: var(--theme-white);
                font-weight: 700;
            }
            .featured-badge-ribbon {
                position: absolute;
                top: 0;
                right: 0;
                background: linear-gradient(135deg, var(--theme-gold) 0%, #9e7f16 100%);
                color: var(--theme-white);
                font-size: 9px;
                font-weight: 900;
                letter-spacing: 0.2em;
                text-transform: uppercase;
                padding: 0.85rem 1.75rem;
                border-bottom-left-radius: 1.5rem;
                display: block;
            }

            /* Pledge Rows styling */
            .pledge-item {
                display: flex;
                gap: 1.5rem;
                align-items: flex-start;
                margin-bottom: 2rem;
            }
            .pledge-icon-wrap {
                width: 3rem;
                height: 3rem;
                background-color: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 0.9rem;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .pledge-headline {
                font-size: 1.25rem;
                font-weight: 700;
                color: var(--theme-white);
                display: block;
                margin-bottom: 0.35rem;
            }
            .pledge-paragraph {
                font-size: 0.95rem;
                font-weight: 300;
                color: rgba(255, 255, 255, 0.55);
                line-height: 1.5;
                display: block;
            }

            /* Live Sitemap visual generator */
            .sitemap-flow {
                background-color: var(--theme-white);
                padding: 2rem;
                border-radius: 2rem;
                border: 1px solid var(--theme-border-gold);
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                gap: 0.75rem;
                margin-top: 1.5rem;
                margin-bottom: 1.5rem;
            }
            .sitemap-node-core {
                background-color: var(--theme-black);
                color: var(--theme-gold);
                padding: 0.5rem 1rem;
                font-size: 10px;
                font-weight: 900;
                text-transform: uppercase;
                border-radius: 0.75rem;
            }
            .sitemap-node-secondary {
                background-color: var(--theme-gray-light);
                color: #4b5563;
                padding: 0.5rem 1rem;
                font-size: 10px;
                font-weight: 700;
                text-transform: uppercase;
                border-radius: 0.75rem;
            }
            .sitemap-node-custom {
                background-color: var(--theme-green);
                color: var(--theme-white);
                padding: 0.5rem 1rem;
                font-size: 10px;
                font-weight: 700;
                text-transform: uppercase;
                border-radius: 0.75rem;
                animation: pulse-green-glow 2s infinite;
            }
            @keyframes pulse-green-glow {
                0%, 100% { box-shadow: 0 0 0 0 rgba(6, 78, 59, 0.4); }
                70% { box-shadow: 0 0 0 8px rgba(6, 78, 59, 0); }
            }

            /* Live Visual Mockup Viewport Container */
            .browser-chrome {
                background-color: var(--theme-black);
                border-radius: 2.5rem;
                padding: 0.75rem;
                border: 1px solid #1f2937;
                display: flex;
                flex-direction: column;
                height: 100%;
                box-shadow: 0 50px 100px -30px rgba(0,0,0,0.4);
            }
            .browser-navbar {
                background-color: #111827;
                padding: 0.75rem 1.5rem;
                border-radius: 1.8rem 1.8rem 0px 0px;
                border-bottom: 1px solid #1f2937;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .browser-dots {
                display: flex;
                gap: 0.4rem;
            }
            .dot-red { width: 10px; height: 10px; border-radius: 9999px; background-color: #f87171; }
            .dot-yellow { width: 10px; height: 10px; border-radius: 9999px; background-color: #fbbf24; }
            .dot-green { width: 10px; height: 10px; border-radius: 9999px; background-color: #34d399; }
            .browser-address {
                background-color: var(--theme-black);
                color: #9ca3af;
                font-size: 11px;
                padding: 0.35rem 3rem;
                border-radius: 9999px;
                border: 1px solid #1f2937;
            }
            
            /* Dynamic Mockup Visual Viewports */
            .mockup-viewport {
                border-radius: 0px 0px 1.8rem 1.8rem;
                flex: 1;
                padding: 3.5rem;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                min-height: 400px;
            }
            .viewport-theme-cream {
                background-color: var(--theme-cream);
                color: var(--theme-black);
            }
            .viewport-theme-green {
                background-color: var(--theme-green);
                color: var(--theme-white);
            }
            .viewport-theme-dark {
                background-color: var(--theme-black);
                color: var(--theme-white);
                border: 1px solid #111827;
            }
            
            /* Footer Elements */
            .footer-headline {
                font-size: 1.75rem;
                font-weight: 700;
                display: block;
                margin-bottom: 1.5rem;
            }
            .footer-paragraph {
                font-size: 0.95rem;
                color: #888888;
                font-weight: 300;
                line-height: 1.6;
                display: block;
                max-width: 18rem;
            }
            .footer-column-header {
                font-size: 0.75rem;
                font-weight: 900;
                text-transform: uppercase;
                letter-spacing: 0.25em;
                color: var(--theme-gold);
                display: block;
                margin-bottom: 2rem;
            }
            .footer-link-element {
                font-size: 0.95rem;
                color: #cccccc;
                font-weight: 300;
                display: block;
                margin-bottom: 1rem;
                cursor: pointer;
                transition: color 0.3s ease;
            }
            .footer-link-element:hover {
                color: var(--theme-gold);
            }
            .footer-con-row {
                display: flex;
                align-items: center;
                gap: 0.75rem;
                margin-bottom: 1.25rem;
            }
            .footer-bottom-divider {
                border-top: 1px solid rgba(255,255,255,0.06);
                padding-top: 2rem;
                margin-top: 5rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            /* --- NATIVE STREAMLIT ELEMENT RE-STYLING --- */
            
            /* Hero CTA & General Core Action Buttons */
            .stButton button {
                background: linear-gradient(135deg, var(--theme-gold) 0%, #9e7f16 100%) !important;
                color: var(--theme-white) !important;
                font-weight: 700 !important;
                font-size: 1.1rem !important;
                padding: 1.25rem 3.5rem !important;
                border-radius: 9999px !important;
                border: none !important;
                box-shadow: 0 20px 40px -12px rgba(197, 160, 34, 0.45) !important;
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
                width: auto !important;
                margin-top: 1.5rem !important;
            }
            .stButton button:hover {
                transform: translateY(-3px) scale(1.02) !important;
                box-shadow: 0 30px 50px -12px rgba(197, 160, 34, 0.6) !important;
                color: var(--theme-white) !important;
            }

            /* Light Tiers Selection Buttons */
            [data-testid="stColumn"]:has(.pricing-card-1-trigger) .stButton button,
            [data-testid="stColumn"]:has(.pricing-card-3-trigger) .stButton button {
                width: 100% !important;
                border: 2px solid var(--theme-black) !important;
                color: var(--theme-black) !important;
                background-color: transparent !important;
                background: transparent !important;
                border-radius: 1.25rem !important;
                font-weight: 800 !important;
                font-size: 11px !important;
                text-transform: uppercase !important;
                letter-spacing: 0.2em !important;
                padding: 1.25rem !important;
                margin-top: auto !important;
                box-shadow: none !important;
            }
            [data-testid="stColumn"]:has(.pricing-card-1-trigger) .stButton button:hover,
            [data-testid="stColumn"]:has(.pricing-card-3-trigger) .stButton button:hover {
                background: var(--theme-black) !important;
                color: var(--theme-white) !important;
                border-color: var(--theme-black) !important;
            }

            /* Dark Tier Selection Button (Featured) */
            [data-testid="stColumn"]:has(.pricing-card-2-trigger) .stButton button {
                width: 100% !important;
                background: linear-gradient(135deg, var(--theme-gold) 0%, #9e7f16 100%) !important;
                border: none !important;
                color: var(--theme-white) !important;
                border-radius: 1.25rem !important;
                font-weight: 800 !important;
                font-size: 11px !important;
                text-transform: uppercase !important;
                letter-spacing: 0.2em !important;
                padding: 1.25rem !important;
                margin-top: auto !important;
                box-shadow: 0 15px 30px -10px rgba(197, 160, 34, 0.4) !important;
            }

            /* Quality Charter Callout Button */
            [data-testid="stColumn"]:has(.pledge-right-trigger) .stButton button {
                background: var(--theme-green) !important;
                color: var(--theme-white) !important;
                border-radius: 1.25rem !important;
                font-weight: 800 !important;
                font-size: 11px !important;
                text-transform: uppercase !important;
                letter-spacing: 0.15em !important;
                border: none !important;
                width: 100% !important;
                margin-top: auto !important;
                box-shadow: none !important;
            }
            [data-testid="stColumn"]:has(.pledge-right-trigger) .stButton button:hover {
                background: var(--theme-black) !important;
            }

            /* Consultation Form Submit Button */
            [data-testid="stHorizontalBlock"]:has(.consultation-trigger) .stButton button {
                background: linear-gradient(135deg, var(--theme-gold) 0%, #9e7f16 100%) !important;
                color: var(--theme-white) !important;
                border-radius: 9999px !important;
                font-weight: 900 !important;
                font-size: 11px !important;
                text-transform: uppercase !important;
                letter-spacing: 0.25em !important;
                width: 100% !important;
                padding: 1.4rem !important;
            }

            /* Widget Input Text & Sliders Custom Styles */
            .stSlider [data-baseweb="slider"] {
                margin-bottom: 1.5rem !important;
            }
            
            /* Native Expander Restyling */
            [data-testid="stExpander"] {
                background-color: var(--theme-white) !important;
                border-radius: 1.8rem !important;
                border: 1px solid var(--theme-gray-light) !important;
                box-shadow: 0 10px 30px -10px rgba(0,0,0,0.03) !important;
                margin-bottom: 1rem !important;
                padding: 0.5rem 1rem !important;
            }
            [data-testid="stExpander"] summary {
                font-weight: 700 !important;
                color: var(--theme-black) !important;
                font-size: 1.1rem !important;
            }

            /* Hide raw markdown text spacing issues */
            .cleanup-indicator {
                display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)

def render_header_navbar():
    """Renders the sticky premium header bar utilizing relational classes and parent container styled triggers."""
    col_left, col_right = st.columns([1, 1])
    with col_left:
        # Crucial fix: navbar trigger placed directly inside structural column
        st.markdown('<span class="navbar-trigger" style="display:none;"></span>', unsafe_allow_html=True)
        st.markdown("""
            <span style="display: flex; align-items: center; gap: 0.85rem;">
                <span style="width: 2.6rem; height: 2.6rem; background-color: #064e3b; border-radius: 0.85rem; display: flex; align-items: center; justify-content: center; transform: rotate(4deg); box-shadow: 0 4px 12px rgba(6,78,59,0.2);">
                    <span class="font-serif" style="color: white; font-weight: 900; font-size: 1.4rem;">A</span>
                </span>
                <span class="font-sans" style="font-size: 1.6rem; font-weight: 800; letter-spacing: -0.03em; color: #0a0a0a; display: inline-block;">
                    afri<span style="color: #c5a022;">host</span>
                </span>
            </span>
        """, unsafe_allow_html=True)
        
    with col_right:
        st.markdown("""
            <span style="display: flex; justify-content: flex-end; align-items: center; height: 100%; gap: 2rem;">
                <span class="font-sans" style="font-size: 11px; font-weight: 900; letter-spacing: 0.15em; text-transform: uppercase; color: #888888; display: inline-block;">Concierge Line</span>
                <span class="font-sans" style="font-size: 14px; font-weight: 800; color: #0a0a0a; display: inline-block;">+27 11 612 7200</span>
            </span>
        """, unsafe_allow_html=True)

def render_hero_section():
    """Renders the symmetrical structurally balanced Hero component utilizing spans and container overrides."""
    st.markdown('<span class="hero-wrapper" style="display:block;">', unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1.1, 0.9])
    
    with col_left:
        # Trigger placed inside target column
        st.markdown('<span class="hero-left-trigger" style="display:none;"></span>', unsafe_allow_html=True)
        st.markdown('<span class="badge-span">Bespoke Managed Curations</span>', unsafe_allow_html=True)
        st.markdown("""
            <span class="heading-primary font-serif">
                The Gold Standard of <span class="text-italic-green">Web Hosting.</span>
            </span>
            <span class="desc-large font-sans">
                Managed hosting, expert maintenance, and world-class digital craft curated for South Africa's most ambitious brands. Experience digital distinction built for legacies.
            </span>
        """, unsafe_allow_html=True)
        
        # Symmetrical native interactive block
        if st.button("Reserve Custom Suite", key="hero_reserve_cta"):
            st.toast("⚡ Opening private consultation configuration gateway...", icon="👑")
            
        st.markdown("""
            <span style="display: flex; align-items: center; margin-top: 4rem; gap: 1.5rem;">
                <span style="height: 3.5rem; width: 1px; background-color: #e5e7eb; display: block;"></span>
                <span style="display: flex; flex-direction: column;">
                    <span class="font-sans" style="font-size: 10px; font-weight: 900; color: #9ca3af; letter-spacing: 0.15em; text-transform: uppercase; display: block;">Status Limit</span>
                    <span class="font-sans" style="font-size: 0.85rem; font-weight: 800; color: #111827; letter-spacing: 0.05em; text-transform: uppercase; display: block;">Only 3 slots remaining in Q2</span>
                </span>
            </span>
        """, unsafe_allow_html=True)
        
    with col_right:
        # Trigger placed inside target column
        st.markdown('<span class="hero-right-trigger" style="display:none;"></span>', unsafe_allow_html=True)
        st.markdown("""
            <span class="green-card-interior">
                <span class="gold-bar"></span>
                <span class="card-title-hero font-serif">48h Delivery.</span>
                <span class="card-desc-hero font-sans">
                    Hand-crafted digital visual architectures deployed securely with surgical execution speed.
                </span>
                <!-- Custom decorative background vectors styled via spans -->
                <span style="position: absolute; top: 2.5rem; right: 2.5rem; opacity: 0.15; transform: scale(1.5); display: block;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.5"><path d="M6 3h12l4 6-10 13L2 9Z"/><path d="M11 3 8 9l3 13 3-13-3-6Z"/><path d="M2 9h20"/></svg>
                </span>
            </span>
            
            <span class="badge-float-card">
                <span class="badge-circle-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#c5a022" stroke-width="3"><path d="M20 6 9 17l-5-5"/></svg>
                </span>
                <span style="display: flex; flex-direction: column;">
                    <span class="font-sans" style="font-size: 9px; font-weight: 900; color: #9ca3af; letter-spacing: 0.15em; text-transform: uppercase; display: block;">Craft Code</span>
                    <span class="font-sans" style="font-size: 0.9rem; font-weight: 800; color: #111827; text-transform: uppercase; display: block;">100% Guaranteed</span>
                </span>
            </span>
        """, unsafe_allow_html=True)
        
    st.markdown('</span>', unsafe_allow_html=True)

def get_calculated_plan_rate(tier, billing_cycle, extra_pages, include_seo, include_speed):
    """Computes pricing in South African Rand (ZAR) incorporating parameters dynamically."""
    tier_base_rates = {
        "Essential": {"Monthly": 4500, "Annual": 3800},
        "Signature": {"Monthly": 9500, "Annual": 8000},
        "Bespoke": {"Monthly": 19500, "Annual": 16500}
    }
    
    base = tier_base_rates[tier][billing_cycle]
    pages_cost = extra_pages * 450
    seo_cost = 850 if include_seo else 0
    speed_cost = 650 if include_speed else 0
    
    subtotal = base + pages_cost + seo_cost + speed_cost
    
    # 5% loyalty privilege discount for annual commitment
    final_total = int(subtotal * 0.95) if billing_cycle == "Annual" else subtotal
    return final_total

def render_interactive_customizer():
    """Renders the live configurator panel with sliders and checkboxes to update quotes in real-time."""
    col_left, col_right = st.columns([1.1, 0.9])
    
    with col_left:
        # Trigger placed directly inside structural column so outer selector stays localized
        st.markdown('<span class="customizer-trigger" style="display:none;"></span>', unsafe_allow_html=True)
        st.markdown("""
            <span class="badge-span badge-span-green">Enterprise Architecture Setup</span>
            <span class="font-serif" style="font-size: 2.5rem; font-weight: 700; color: #0a0a0a; display: block; margin-bottom: 2.5rem;">
                Configure Your Dynamic Blueprint
            </span>
        """, unsafe_allow_html=True)

        # Billing Cycle Switcher using standard Streamlit logic in elegant containers
        billing_select = st.radio(
            "Select Your Subscription Tenure",
            ["Monthly Plan", "Annual Suite (Save 15% + Edge Caching Setup)"],
            horizontal=True,
            help="Annual plans gain advanced optimization setups for higher core vitals scores."
        )
        st.session_state.billing_cycle = "Monthly" if "Monthly" in billing_select else "Annual"
        
        # Package tier mapping selectors
        tier_select = st.selectbox(
            "Select Baseline Hosting Masterpiece Tier",
            ["Essential Plan", "Signature (Recommended Model)", "Bespoke Curation Edition"],
            index=1
        )
        if "Essential" in tier_select:
            st.session_state.selected_tier = "Essential"
        elif "Signature" in tier_select:
            st.session_state.selected_tier = "Signature"
        else:
            st.session_state.selected_tier = "Bespoke"
            
        # Slider to dynamically scale estimated pages
        pages_select = st.slider(
            "Bespoke Interface Layout Count",
            min_value=1,
            max_value=12,
            value=st.session_state.extra_pages,
            help="Sitemap elements required to support your content mapping architecture."
        )
        st.session_state.extra_pages = pages_select
        
        # Interactive Node Maps rendered purely in visual Spans
        st.markdown('<span class="font-sans" style="font-size: 11px; font-weight: 900; color: #888888; text-transform: uppercase; letter-spacing: 0.15em; display: block; margin-bottom: 0.5rem;">Estimated Sitemap Blueprint Nodes</span>', unsafe_allow_html=True)
        
        # Dynamic node rendering logic
        nodes_html = """<span class="sitemap-flow">
            <span class="sitemap-node-core">Home (Index)</span>
            <span style="color: #c5a022;">→</span>
            <span class="sitemap-node-secondary">Secure Contact</span>"""
            
        for i in range(pages_select):
            nodes_html += f"""
            <span style="color: #c5a022;">→</span>
            <span class="sitemap-node-custom">Custom Node {i+1}</span>"""
            
        nodes_html += "</span>"
        st.markdown(nodes_html, unsafe_allow_html=True)
        
        # Boolean modifiers for advanced configurations
        st.markdown('<span style="display: flex; gap: 2rem; margin-top: 1.5rem;">', unsafe_allow_html=True)
        st.session_state.seo_premium = st.checkbox("Include Advanced Search Engine Optimization Audit (ZAR 850)", value=st.session_state.seo_premium)
        st.session_state.speed_opt = st.checkbox("Include Ultra Performance Cloud Delivery Networks (ZAR 650)", value=st.session_state.speed_opt)
        st.markdown('</span>', unsafe_allow_html=True)

    with col_right:
        # Calculate pricing outputs in real-time
        price = get_calculated_plan_rate(
            st.session_state.selected_tier,
            st.session_state.billing_cycle,
            st.session_state.extra_pages,
            st.session_state.seo_premium,
            st.session_state.speed_opt
        )
        
        # Output summary receipt styled inside dark onyx card
        st.html(f"""
            <span style="background-color: #0a0a0a; border-radius: 2.5rem; padding: 3rem; display: flex; flex-direction: column; justify-content: space-between; height: 100%; border: 1px solid rgba(197, 160, 34, 0.2); position: relative;">
                <span style="display: block;">
                    <span class="font-sans" style="font-size: 9px; font-weight: 900; color: #c5a022; letter-spacing: 0.25em; text-transform: uppercase; display: block; margin-bottom: 1.5rem;">Dynamic Estimation Summary</span>
                    <span class="font-serif" style="font-size: 2rem; font-weight: 700; color: white; display: block; border-bottom: 1px solid #1f2937; padding-bottom: 1.5rem; margin-bottom: 1.5rem;">
                        {st.session_state.selected_tier} Edition
                    </span>
                    
                    <span style="display: flex; flex-direction: column; gap: 1rem; margin-bottom: 2rem;">
                        <span style="display: flex; justify-content: space-between; font-size: 13px; color: #9ca3af;">
                            <span>Base Subscription Plan ({st.session_state.billing_cycle})</span>
                            <span style="color: white; font-weight: 600;">R {base_price_display(st.session_state.selected_tier, st.session_state.billing_cycle)}</span>
                        </span>
                        <span style="display: flex; justify-content: space-between; font-size: 13px; color: #9ca3af;">
                            <span>Bespoke Layout Node Count ({st.session_state.extra_pages} Nodes)</span>
                            <span style="color: white; font-weight: 600;">R {st.session_state.extra_pages * 450}</span>
                        </span>
                        <span style="display: flex; justify-content: space-between; font-size: 13px; color: #9ca3af;">
                            <span>Advanced SEO Meta Setup</span>
                            <span style="color: white; font-weight: 600;">{"R 850" if st.session_state.seo_premium else "R 0"}</span>
                        </span>
                        <span style="display: flex; justify-content: space-between; font-size: 13px; color: #9ca3af;">
                            <span>Ultra CDN Delivery Integration</span>
                            <span style="color: white; font-weight: 600;">{"R 650" if st.session_state.speed_opt else "R 0"}</span>
                        </span>
                    </span>
                </span>
                
                <span style="border-top: 1px solid #1f2937; padding-top: 2rem; display: block;">
                    <span style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 2rem;">
                        <span style="display: flex; flex-direction: column;">
                            <span class="font-sans" style="font-size: 10px; font-weight: 900; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.1em;">Total Estimate</span>
                            <span class="font-sans" style="font-size: 9px; color: #4b5563;">VAT Exclusive</span>
                        </span>
                        <span>
                            <span class="font-sans" style="font-size: 1.25rem; font-weight: 800; color: #c5a022;">R</span>
                            <span class="font-sans" style="font-size: 2.75rem; font-weight: 900; color: #c5a022;">{price:,}</span>
                            <span class="font-sans" style="font-size: 0.9rem; color: #9ca3af; font-style: italic;">/{'mo' if st.session_state.billing_cycle == 'Monthly' else 'yr'}</span>
                        </span>
                    </span>
                </span>
            </span>
        """)#, unsafe_allow_html=True)
        
        # Button alignment inside card container
        if st.button("Configure Setup Blueprint", key="checkout_integration"):
            st.toast(f"🔒 Blueprint configured successfully! Plan Total: R {price:,}", icon="✨")

def base_price_display(tier, billing_cycle):
    """Simple mapping converter to show string formats of values inside raw inline text blocks."""
    rates = {
        "Essential": {"Monthly": "4,500", "Annual": "3,800"},
        "Signature": {"Monthly": "9,500", "Annual": "8,000"},
        "Bespoke": {"Monthly": "19,500", "Annual": "16,500"}
    }
    return rates[tier][billing_cycle]

def render_mockup_sandbox():
    """Renders the custom simulated website viewport that updates instantly as users interact with control nodes."""
    col_left, col_right = st.columns([0.8, 1.2])
    
    with col_left:
        # Trigger placed inside structural column
        st.markdown('<span class="mockup-studio-trigger" style="display:none;"></span>', unsafe_allow_html=True)
        st.markdown("""
            <span class="badge-span">Live Simulation Laboratory</span>
            <span class="font-serif" style="font-size: 2.5rem; font-weight: 700; color: #0a0a0a; display: block; margin-bottom: 2.5rem;">
                Interactive AI Layout Preview Studio
            </span>
            <span class="font-sans" style="font-size: 14px; color: #6b7280; font-weight: 300; line-height: 1.5; display: block; margin-bottom: 2rem;">
                Tweak parameters in the controls block below to render your custom website interface mockup directly inside our simulated browser canvas on the right.
            </span>
        """, unsafe_allow_html=True)
        
        # Interactive Text configuration for simulation
        brand_name_input = st.text_input(
            "Corporate Identity (Company Name)",
            value=st.session_state.preview_brand_name
        )
        st.session_state.preview_brand_name = brand_name_input
        
        theme_options = ["Luxurious Cream", "Deep Emerald Forest", "Minimalist Matte Black"]
        theme_select = st.selectbox(
            "Visual Guidelines Theme Preset",
            theme_options,
            index=theme_options.index(st.session_state.preview_theme)
        )
        st.session_state.preview_theme = theme_select
        
        if st.button("Generate Layout Mockup", key="mockup_studio_run"):
            st.toast("🎨 Compiling premium styling parameters...", icon="✨")

    with col_right:
        # Theme configuration mapper to match custom HTML nodes dynamically
        style_preset_mapping = {
            "Luxurious Cream": "viewport-theme-cream",
            "Deep Emerald Forest": "viewport-theme-green",
            "Minimalist Matte Black": "viewport-theme-dark"
        }
        
        active_preset_class = style_preset_mapping[st.session_state.preview_theme]
        
        # Compile dynamically built visual layout preview within Simulated Browser Frame
        st.html(f"""
            <span class="browser-chrome">
                <span class="browser-navbar">
                    <span class="browser-dots">
                        <span class="dot-red"></span>
                        <span class="dot-yellow"></span>
                        <span class="dot-green"></span>
                    </span>
                    <span class="browser-address">https://afrihost.za/mockup-preview</span>
                    <span style="color: #4b5563; font-size: 11px;">🔒</span>
                </span>
                
                <span class="mockup-viewport {active_preset_class}">
                    <span style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="font-sans" style="font-weight: 900; text-transform: uppercase; font-size: 12px; letter-spacing: 0.15em;">
                            {st.session_state.preview_brand_name}
                        </span>
                        <span style="display: flex; gap: 1rem; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.8;">
                            <span>Portfolio</span>
                            <span>Contact</span>
                        </span>
                    </span>
                    
                    <span style="display: block; margin-top: 3rem; margin-bottom: 3rem;">
                        <span class="font-serif" style="font-size: 2.5rem; font-weight: 700; line-height: 1.1; display: block; margin-bottom: 1.5rem;">
                            The Epitome of <span class="text-italic-gold">Digital Grace</span>
                        </span>
                        <span class="font-sans" style="font-size: 12px; font-weight: 300; opacity: 0.75; display: block; max-width: 24rem;">
                            Bespoke interfaces custom designed in Cape Town and Sandton. Powered securely by high performance enterprise managed hosting.
                        </span>
                    </span>
                    
                    <span style="border-top: 1px solid rgba(197, 160, 34, 0.2); padding-top: 1.5rem; display: flex; justify-content: space-between; align-items: center;">
                        <span class="font-sans" style="font-size: 9px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.2em; color: #c5a022;">
                            Selected: {st.session_state.selected_tier} Tier
                        </span>
                        <span class="font-sans" style="font-size: 9px; font-weight: 900; text-transform: uppercase; opacity: 0.6;">
                            Active Nodes: {st.session_state.extra_pages + 2} Elements
                        </span>
                    </span>
                </span>
            </span>
        """)#, unsafe_allow_html=True)

def render_pricing_grid():
    """Renders the visually matching three-column Pricing Configuration grid with custom spans and trigger blocks."""
    st.markdown('<span style="padding-top: 4rem; display: block;"></span>', unsafe_allow_html=True)
    st.markdown('<span class="badge-span">Subscription Models</span>', unsafe_allow_html=True)
    st.markdown('<span class="font-serif" style="font-size: 3.5rem; font-weight: 700; line-height: 1.1; margin-bottom: 4rem; display: block;">Curated Investment Plans</span>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<span class="pricing-card-1-trigger" style="display:none;"></span>', unsafe_allow_html=True)
        st.markdown("""
            <span class="tier-sub">Model I</span>
            <span class="tier-title-light font-display">Essential</span>
            <span class="price-wrap">
                <span class="price-val-light font-display">R 4,500</span><span class="price-cycle">/mo</span>
            </span>
            <span class="features-list-span">
                <span class="feat-line">
                    <span class="circle-icon-green"><svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#064e3b" stroke-width="4"><path d="M20 6 9 17l-5-5"/></svg></span>
                    <span class="feat-txt-gray">3 Custom Designed Layouts</span>
                </span>
                <span class="feat-line">
                    <span class="circle-icon-green"><svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#064e3b" stroke-width="4"><path d="M20 6 9 17l-5-5"/></svg></span>
                    <span class="feat-txt-gray">Enterprise Managed Cloud Host</span>
                </span>
                <span class="feat-line">
                    <span class="circle-icon-green"><svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#064e3b" stroke-width="4"><path d="M20 6 9 17l-5-5"/></svg></span>
                    <span class="feat-txt-gray">Standard Monthly Updates</span>
                </span>
            </span>
        """, unsafe_allow_html=True)
        
        if st.button("Apply for Essential", key="tier_btn_1"):
            st.session_state.selected_tier = "Essential"
            st.toast("🥉 Selected Essential Model. Proceed to customization.", icon="✨")

    with col2:
        st.markdown('<span class="pricing-card-2-trigger" style="display:none;"></span>', unsafe_allow_html=True)
        st.markdown("""
            <span class="featured-badge-ribbon">Most Preferred</span>
            <span class="tier-sub" style="color: #c5a022;">Model II</span>
            <span class="tier-title-dark font-display">Signature</span>
            <span class="price-wrap">
                <span class="price-val-dark font-display">R 9,500</span><span class="price-cycle">/mo</span>
            </span>
            <span class="features-list-span">
                <span class="feat-line">
                    <span class="circle-icon-dark"><svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#c5a022" stroke-width="4"><path d="M20 6 9 17l-5-5"/></svg></span>
                    <span class="feat-txt-white">6 Bespoke Visual Frameworks</span>
                </span>
                <span class="feat-line">
                    <span class="circle-icon-dark"><svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#c5a022" stroke-width="4"><path d="M20 6 9 17l-5-5"/></svg></span>
                    <span class="feat-txt-white">Quarterly Performance Audits</span>
                </span>
                <span class="feat-line">
                    <span class="circle-icon-gold"><svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="4"><path d="M20 6 9 17l-5-5"/></svg></span>
                    <span class="feat-txt-bold-white">Priority VIP Support Queue</span>
                </span>
            </span>
        """, unsafe_allow_html=True)
        
        if st.button("Secure Signature", key="tier_btn_2"):
            st.session_state.selected_tier = "Signature"
            st.toast("🥈 Selected Signature Model. Proceed to customization.", icon="✨")

    with col3:
        st.markdown('<span class="pricing-card-3-trigger" style="display:none;"></span>', unsafe_allow_html=True)
        st.markdown("""
            <span class="tier-sub">Model III</span>
            <span class="tier-title-light font-display">Bespoke</span>
            <span class="price-wrap">
                <span class="price-val-light font-display">R 19,500</span><span class="price-cycle">/mo</span>
            </span>
            <span class="features-list-span">
                <span class="feat-line">
                    <span class="circle-icon-green"><svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#064e3b" stroke-width="4"><path d="M20 6 9 17l-5-5"/></svg></span>
                    <span class="feat-txt-gray">Unlimited Modular Layout Pages</span>
                </span>
                <span class="feat-line">
                    <span class="circle-icon-green"><svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#064e3b" stroke-width="4"><path d="M20 6 9 17l-5-5"/></svg></span>
                    <span class="feat-txt-gray">Interactive Motion Integrations</span>
                </span>
                <span class="feat-line">
                    <span class="circle-icon-green"><svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#064e3b" stroke-width="4"><path d="M20 6 9 17l-5-5"/></svg></span>
                    <span class="feat-txt-gray">Bespoke Custom API Development</span>
                </span>
            </span>
        """, unsafe_allow_html=True)
        
        if st.button("Apply for Bespoke", key="tier_btn_3"):
            st.session_state.selected_tier = "Bespoke"
            st.toast("🥇 Selected Bespoke Model. Proceed to customization.", icon="✨")

def render_pledge_charter():
    """Renders the balanced, high-contrast, emerald and gold Guarantee charter section."""
    col_left, col_right = st.columns([1, 1])

    with col_left:
        # Trigger placed inside structural column
        st.markdown('<span class="pledge-left-trigger" style="display:none;"></span>', unsafe_allow_html=True)
        st.html("""
            <span class="badge-span" style="border: 1px solid rgba(255,255,255,0.2) !important; background-color: rgba(255,255,255,0.05) !important;">
                The afrihost Standard
            </span>
            <span class="font-serif" style="font-size: 3rem; font-weight: 700; color: white; line-height: 1.1; margin-bottom: 3.5rem; display: block;">
                Our Pledge of <br><span class="text-italic-gold">Absolute Quality.</span>
            </span>
            
            <span style="display: flex; flex-direction: column;">
                <span class="pledge-item">
                    <span class="pledge-icon-wrap">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#c5a022" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                    </span>
                    <span style="display: flex; flex-direction: column;">
                        <span class="pledge-headline font-sans">48-Hour Concepts Deployed</span>
                        <span class="pledge-paragraph font-sans">Elite execution workflows. We deliver high-fidelity draft layouts in record time.</span>
                    </span>
                </span>
                
                <span class="pledge-item">
                    <span class="pledge-icon-wrap">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#c5a022" stroke-width="2"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
                    </span>
                    <span style="display: flex; flex-direction: column;">
                        <span class="pledge-headline font-sans">Absolute Design Care</span>
                        <span class="pledge-paragraph font-sans">We continuously refine typography, assets, and structural alignments to perfect your vision.</span>
                    </span>
                </span>
            </span>
        """)#, unsafe_allow_html=True)

    with col_right:
        # Trigger placed inside structural column
        st.markdown('<span class="pledge-right-trigger" style="display:none;"></span>', unsafe_allow_html=True)
        st.markdown("""
            <span style="width: 3rem; height: 3rem; background-color: #c5a022; border-radius: 0.85rem; display: flex; align-items: center; justify-content: center; margin-bottom: 2rem;">
                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M6 3h12l4 6-10 13L2 9Z"/><path d="M11 3 8 9l3 13 3-13-3-6Z"/><path d="M2 9h20"/></svg>
            </span>
            <span class="font-serif" style="font-size: 1.85rem; font-weight: 700; font-style: italic; color: #0a0a0a; display: block; margin-bottom: 1rem;">
                Excellence by Default.
            </span>
            <span class="font-sans" style="font-size: 1rem; color: #6b7280; font-weight: 300; line-height: 1.6; display: block; margin-bottom: 2.5rem;">
                Join South Africa's most prestigious network of organizations. We don't just engineer interfaces; we design and protect digital legacies.
            </span>
        """, unsafe_allow_html=True)
        
        # Native interactive callout trigger
        if st.button("Join Prestige Registry", key="pledge_btn"):
            st.toast("🤝 Welcome to the Elite afrihost Care ecosystem.", icon="💎")

# ==================== NEW SECTIONS ====================

def render_stats():
    """Animated stats counters."""
    st.markdown('<div class="stats-container">', unsafe_allow_html=True)
    cols = st.columns(3)
    stats = [
        {"value": 98, "label": "Client Retention", "suffix": "%"},
        {"value": 247, "label": "Projects Deployed", "suffix": "+"},
        {"value": 15000, "label": "Hours Saved", "suffix": "+"}
    ]
    for i, stat in enumerate(stats):
        with cols[i]:
            st.markdown(f"""
                <div class="stat-card">
                    <span class="stat-number"><span class="stat-number-value" data-final="{stat['value']}">0</span>{stat['suffix']}</span>
                    <span class="stat-label">{stat['label']}</span>
                </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # JavaScript for counter animation (run once)
    if "counter_js_injected" not in st.session_state:
        st.session_state.counter_js_injected = True
        st.markdown("""
            <script>
                function animateCounter(element, start, end, duration) {
                    let startTimestamp = null;
                    const step = (timestamp) => {
                        if (!startTimestamp) startTimestamp = timestamp;
                        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
                        element.innerText = Math.floor(progress * (end - start) + start);
                        if (progress < 1) {
                            window.requestAnimationFrame(step);
                        }
                    };
                    window.requestAnimationFrame(step);
                }
                
                const observerCounters = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const el = entry.target;
                            const final = parseInt(el.getAttribute('data-final'));
                            animateCounter(el, 0, final, 1500);
                            observerCounters.unobserve(el);
                        }
                    });
                }, { threshold: 0.5 });
                
                setTimeout(() => {
                    document.querySelectorAll('.stat-number-value').forEach(el => observerCounters.observe(el));
                }, 500);
            </script>
        """, unsafe_allow_html=True)

def render_testimonials():
    """Testimonials section with client quotes."""
    st.markdown('<div class="testimonials-container">', unsafe_allow_html=True)
    st.markdown('<span class="badge-span" style="margin: 0 auto 2rem auto;">Client Voices</span>', unsafe_allow_html=True)
    st.markdown('<div class="roadmap-header" style="text-align: center;">Trusted by <span style="color:#064e3b">Industry Leaders</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="roadmap-subheader" style="text-align: center; margin: 0 auto 3rem auto;">What our clients say about the afrihost experience.</div>', unsafe_allow_html=True)
    
    testimonials = [
        {"quote": "The 48-hour deployment is not a gimmick. Our site was live, optimized, and converting within two days. Unmatched service.", "name": "Sarah Nkosi", "title": "Founder, Luxe Haven", "initial": "S"},
        {"quote": "Afrihost transformed our digital presence. The concierge support is genuinely responsive, and the quality is world-class.", "name": "James van der Merwe", "title": "CEO, Cape Analytics", "initial": "J"},
        {"quote": "From strategy to launch, every step was seamless. The ongoing care takes all the stress out of running a business website.", "name": "Thabo Molefe", "title": "Creative Director, Studio M", "initial": "T"},
        {"quote": "We've tried several agencies, but none offer the combination of design excellence and managed hosting like afrihost. Pure gold.", "name": "Priya Naidoo", "title": "Marketing Lead, Durban Digital", "initial": "P"}
    ]
    
    cols = st.columns(2)
    for i, test in enumerate(testimonials):
        with cols[i % 2]:
            st.markdown(f"""
                <div class="testimonial-card">
                    <span class="testimonial-quote">"{test['quote']}"</span>
                    <div class="testimonial-author">
                        <div class="testimonial-avatar">{test['initial']}</div>
                        <div><span class="testimonial-name">{test['name']}</span><span class="testimonial-title">{test['title']}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_tech_stack():
    """Technology stack grid."""
    st.markdown('<div class="tech-container">', unsafe_allow_html=True)
    st.markdown('<span class="badge-span" style="margin: 0 auto 2rem auto;">Enterprise-Grade Tech</span>', unsafe_allow_html=True)
    st.markdown('<div class="roadmap-header" style="text-align: center;">Powered by <span style="color:#064e3b">World-Class Infrastructure</span></div>', unsafe_allow_html=True)
    
    techs = ["WordPress", "Shopify", "WooCommerce", "Stripe", "Cloudflare", "Google Analytics"]
    st.markdown('<div class="tech-grid">', unsafe_allow_html=True)
    for tech in techs:
        st.markdown(f'<div class="tech-item"><i data-lucide="check-circle" style="color: #c5a022; width: 2rem; height: 2rem; margin-bottom: 0.5rem;"></i><br><strong>{tech}</strong></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_case_studies():
    """Case studies / portfolio showcase."""
    st.markdown('<div class="testimonials-container">', unsafe_allow_html=True)
    st.markdown('<span class="badge-span" style="margin: 0 auto 2rem auto;">Success Stories</span>', unsafe_allow_html=True)
    st.markdown('<div class="roadmap-header" style="text-align: center;">Real Results, <span style="color:#064e3b">Real Impact</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="roadmap-subheader" style="text-align: center; margin: 0 auto 3rem auto;">See how we’ve helped brands achieve digital excellence.</div>', unsafe_allow_html=True)
    
    cases = [
        {"title": "Luxe Haven", "desc": "E-commerce transformation for luxury boutique.", "metric": "+156% online revenue", "icon": "shopping-bag"},
        {"title": "Cape Analytics", "desc": "B2B lead generation platform rebuild.", "metric": "+89% conversion rate", "icon": "bar-chart-3"},
        {"title": "Studio M", "desc": "Creative portfolio with immersive interactions.", "metric": "Awwwards nominee", "icon": "award"}
    ]
    
    cols = st.columns(3)
    for i, case in enumerate(cases):
        with cols[i]:
            st.markdown(f"""
                <div class="case-card">
                    <div class="case-image"><i data-lucide="{case['icon']}" style="color: white; width: 3rem; height: 3rem;"></i></div>
                    <div class="case-content">
                        <span class="case-title">{case['title']}</span>
                        <span class="step-desc" style="margin-bottom: 0.5rem;">{case['desc']}</span>
                        <span class="case-metric">{case['metric']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_roadmap():
    """Interactive 4-step roadmap."""
    st.markdown('<div class="roadmap-container">', unsafe_allow_html=True)
    st.markdown('<span class="roadmap-badge">Our Workflow</span>', unsafe_allow_html=True)
    st.markdown('<div class="roadmap-header">The Roadmap to <span style="color:#064e3b">Perfection</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="roadmap-subheader">A streamlined experience designed to respect your time while maximizing your digital impact. We architect digital legacies.</div>', unsafe_allow_html=True)

    steps = [
        {"id": "01", "title": "Curation", "desc": "We analyze your brand DNA and curate a bespoke aesthetic strategy tailored to your industry's elite tier.", "action": "View Strategy"},
        {"id": "02", "title": "The Build", "desc": "Elite developers execute the blueprint on Afrihost managed technology, ensuring peak performance.", "action": "See Tech"},
        {"id": "03", "title": "Deployment", "desc": "Your site goes live with seamless domain migration, SSL certification, and edge-server optimization.", "action": "Launch Plan"},
        {"id": "04", "title": "Concierge", "desc": "Ongoing monthly refinements and priority updates ensure your brand stays at the absolute pinnacle.", "action": "Learn More"}
    ]
    cols = st.columns(4)
    for i, step in enumerate(steps):
        with cols[i]:
            st.markdown(f"""
                <div class="step-card">
                    <span class="step-number">{step["id"]}</span>
                    <span class="step-title">{step["title"]}</span>
                    <span class="step-desc">{step["desc"]}</span>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="roadmap-step">', unsafe_allow_html=True)
            if st.button(step["action"], key=f"roadmap_btn_{step['id']}"):
                st.toast(f"Opening details for {step['title']}...")
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== END NEW SECTIONS ====================

def render_consultation_form():
    """Renders the custom styled interactive Blueprint Consultation form utilizing modern spans and form triggers."""
    col_form_left, col_form_right = st.columns(2)
    
    with col_form_left:
        # Trigger placed inside structural columns
        st.markdown('<span class="consultation-trigger" style="display:none;"></span>', unsafe_allow_html=True)
        st.markdown("""
            <span class="badge-span">Secure Executive Slot</span>
            <span class="font-serif" style="font-size: 2.5rem; font-weight: 700; color: #0a0a0a; display: block; margin-bottom: 2.5rem;">
                Initiate Project Blueprint
            </span>
        """, unsafe_allow_html=True)
        
        rep_name = st.text_input("Representative Name *", placeholder="e.g. Liam Daniels")
        rep_email = st.text_input("Corporate Email Address *", placeholder="e.g. liam@brand.co.za")
        
    with col_form_right:
        rep_brand = st.text_input("Organization Name", placeholder="e.g. Daniels & Co.")
        rep_notes = st.text_area("Concept Requirements & Directives", placeholder="Any special branding guidelines or layout notes...")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state.inquiry_submitted:
        st.markdown("""
            <span style="background-color: white; border-radius: 2rem; padding: 3rem; display: block; text-align: center; border: 1px solid rgba(197, 160, 34, 0.2); margin-top: 2rem;">
                <span style="width: 4rem; height: 4rem; background-color: #064e3b; border-radius: 9999px; display: flex; align-items: center; justify-content: center; margin: 0 auto 2rem auto;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#c5a022" stroke-width="3"><path d="M20 6 9 17l-5-5"/></svg>
                </span>
                <span class="font-serif" style="font-size: 1.75rem; font-weight: 700; display: block; margin-bottom: 1rem; color: #0a0a0a;">
                    Application Received Successfully
                </span>
                <span class="font-sans" style="font-size: 13px; color: #6b7280; display: block; max-width: 24rem; margin: 0 auto;">
                    Our lead architect has reserved your configuration slot. We will reach out to you within the next 12 hours.
                </span>
            </span>
        """, unsafe_allow_html=True)
        
        if st.button("Reset Application Form", key="reset_inquiry_form"):
            st.session_state.inquiry_submitted = False
            st.rerun()
            
    else:
        # Native action button aligned at full width utilizing container form definitions
        if st.button("Reserve My Consultation Slot", key="submit_consultation"):
            if rep_name and rep_email:
                st.session_state.inquiry_submitted = True
                st.toast("🔒 Vault space secured. Initiating blueprint creation...", icon="👑")
                st.rerun()
            else:
                st.error("Please fill in the required fields (Name and Email) to proceed.")

def render_faqs():
    """Renders highly styled native Streamlit Expander accordions."""
    st.markdown('<span style="padding-top: 4rem; display: block;"></span>', unsafe_allow_html=True)
    st.markdown('<span class="font-serif" style="font-size: 2.5rem; font-weight: 700; text-align: center; margin-bottom: 3.5rem; color: #0a0a0a; display: block;">Concierge Queries</span>', unsafe_allow_html=True)
    
    with st.expander("Who owns the finalized design assets?"):
        st.write("Ownership of layouts, code architectures, and graphic structures fully belongs to your organization upon project launch. Unlike standard legacy providers, we ensure you maintain total control.")
        
    with st.expander("How are ongoing maintenance layout updates managed?"):
        st.write("Every monthly plan includes dedicated concierge hours to implement standard updates (text, asset replacement, visual modifications). Simply send directives to your support engineer, and changes are applied securely.")
        
    with st.expander("Are custom payment gateway integrations supported?"):
        st.write("Yes. We natively support high-end dynamic e-commerce pipelines, South African payment integrations (PayFast, Peach Payments, Stitch), and currency adapters starting on our Silver configurations.")

def render_footer_block():
    """Renders the rich Black four-column footer at the bottom of the landing page using spans."""
    col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1.5])

    with col1:
        # Trigger placed inside structural columns
        st.markdown('<span class="footer-trigger" style="display:none;"></span>', unsafe_allow_html=True)
        st.markdown("""
            <span class="footer-headline font-sans" style="color: white;">afri<span style="color: #c5a022;">design</span></span>
            <span class="footer-paragraph font-sans">
                Hand-crafting the digital future for South Africa's most prestigious organizations. Bespoke design meets surgical precision.
            </span>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<span class="footer-column-header font-sans">Collection</span>', unsafe_allow_html=True)
        st.markdown('<span class="footer-link-element">The Visual Collection</span>', unsafe_allow_html=True)
        st.markdown('<span class="footer-link-element">Managed Care Framework</span>', unsafe_allow_html=True)
        st.markdown('<span class="footer-link-element">Bespoke Design Philosophy</span>', unsafe_allow_html=True)

    with col3:
        st.markdown('<span class="footer-column-header font-sans">Concierge Contact</span>', unsafe_allow_html=True)
        st.markdown("""
            <span class="footer-con-row">
                <span style="color: #c5a022; font-size: 14px;">📞</span>
                <span class="footer-link-element" style="margin-bottom: 0;">+27 11 612 7200</span>
            </span>
            <span class="footer-con-row">
                <span style="color: #c5a022; font-size: 14px;">✉️</span>
                <span class="footer-link-element" style="margin-bottom: 0;">concierge@afrihost.za</span>
            </span>
            <span class="footer-con-row">
                <span style="color: #c5a022; font-size: 14px;">📍</span>
                <span class="footer-link-element" style="margin-bottom: 0;">Sandton, RSA</span>
            </span>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown('<span class="footer-column-header font-sans">Corporate Registry</span>', unsafe_allow_html=True)
        st.markdown('<span class="footer-paragraph font-sans" style="margin-bottom: 1.5rem;">Join our private registry list for quarterly availability updates.</span>', unsafe_allow_html=True)
        
        news_email = st.text_input("Corporate Registry Email", placeholder="your@organization.co.za", key="newsletter_footer_input", label_visibility="collapsed")
        if st.button("Apply for Membership Registry", key="newsletter_footer_btn"):
            if news_email:
                st.toast("🛡️ Successfully enrolled in our private elite availability database.", icon="✨")
            else:
                st.error("Please enter a valid email address.")

    st.markdown("""
        <span class="footer-bottom-divider">
            <span class="font-sans" style="font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.15em; color: #4b5563;">
                © 2026 Premium afrihost Managed Services. All Rights Reserved.
            </span>
            <span style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="width: 6px; height: 6px; background-color: #22c55e; border-radius: 9999px; box-shadow: 0 0 10px #22c55e;"></span>
                <span class="font-sans" style="font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.15em; color: #22c55e;">
                    AWS Core Instances Active
                </span>
            </span>
        </span>
    """, unsafe_allow_html=True)

def main():
    """Unified coordinator setting up layout elements smoothly."""
    # 1. Inject Stylesheets
    inject_master_styles()
    
    # 2. Render Page Sections Sequentially with Zero vertical space gaps
    render_header_navbar()
    render_hero_section()
    render_interactive_customizer()
    render_mockup_sandbox()
    render_pricing_grid()
    render_pledge_charter()
    
    # New sections added here
    render_stats()
    render_testimonials()
    render_tech_stack()
    render_case_studies()
    render_roadmap()
    
    # Original sections continue
    render_consultation_form()
    render_faqs()
    render_footer_block()
    
    # Clean up indicator to keep Streamlit output clean
    st.markdown('<span class="cleanup-indicator">Layout complete</span>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()