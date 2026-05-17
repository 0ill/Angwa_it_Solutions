import streamlit as st

st.set_page_config(
    page_title="Premium afridesign | Managed Web Excellence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def inject_master_styles():
    """Injects a master CSS block that overrides standard Streamlit layouts with a premium theme."""
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
            
            :root {
                --theme-gold: #c5a022;
                --theme-green: #064e3b;
                --theme-cream: #fdfcf0;
                --theme-black: #0a0a0a;
                --theme-white: #ffffff;
                --theme-gray-light: #f3f4f6;
            }

            /* Main Page Overrides for Zero-Gap Vertical Flow */
            .stApp {
                background-color: var(--theme-cream) !important;
            }
            [data-testid="stHeader"] {
                background: transparent !important;
            }
            .main > div {
                padding-top: 0px !important;
                padding-bottom: 0px !important;
            }
            [data-testid="stVerticalBlock"] {
                gap: 0px !important;
            }

            /* Typography */
            html, body, [class*="css"] {
                font-family: 'Inter', sans-serif;
            }
            .font-serif {
                font-family: 'Playfair Display', serif;
            }

            /* Symmetrical Equal Height Columns Magic */
            [data-testid="stHorizontalBlock"] {
                align-items: stretch !important;
                gap: 2rem !important;
            }
            [data-testid="stColumn"] {
                display: flex !important;
                flex-direction: column !important;
                height: 100% !important;
            }
            [data-testid="stColumn"] > div {
                flex: 1 !important;
                display: flex !important;
                flex-direction: column !important;
                height: 100% !important;
            }

            /* --- COLUMN-LEVEL CONTAINER CONTAINMENT (:has) --- */
            
            /* Navbar Header Row */
            [data-testid="stHorizontalBlock"]:has(.navbar-trigger) {
                background-color: rgba(255, 255, 255, 0.85) !important;
                backdrop-filter: blur(20px) !important;
                border-bottom: 1px solid rgba(197, 160, 34, 0.1) !important;
                padding: 1.5rem 3rem !important;
                position: sticky !important;
                top: 0 !important;
                z-index: 1000 !important;
                border-radius: 0 0 2rem 2rem !important;
            }

            /* Hero Right Column Card Container */
            [data-testid="stColumn"]:has(.hero-right-trigger) {
                background-color: var(--theme-white) !important;
                border-radius: 4rem !important;
                padding: 1.2rem !important;
                box-shadow: 0 60px 120px -30px rgba(0, 0, 0, 0.15) !important;
                border: 1px solid var(--theme-gray-light) !important;
                height: 100% !important;
                position: relative !important;
            }

            /* Pricing Card 1 & 3 Containment */
            [data-testid="stColumn"]:has(.pricing-card-1-trigger),
            [data-testid="stColumn"]:has(.pricing-card-3-trigger) {
                background-color: var(--theme-white) !important;
                border-radius: 3.5rem !important;
                padding: 3.5rem 2.5rem !important;
                border: 1px solid var(--theme-gray-light) !important;
                box-shadow: 0 40px 100px -20px rgba(6, 78, 59, 0.08) !important;
                transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
                position: relative !important;
            }
            [data-testid="stColumn"]:has(.pricing-card-1-trigger):hover,
            [data-testid="stColumn"]:has(.pricing-card-3-trigger):hover {
                transform: translateY(-10px) !important;
                box-shadow: 0 60px 120px -30px rgba(6, 78, 59, 0.12) !important;
            }

            /* Pricing Card 2 (Dark/Featured Card Containment) */
            [data-testid="stColumn"]:has(.pricing-card-2-trigger) {
                background-color: var(--theme-black) !important;
                border-radius: 3.5rem !important;
                padding: 3.5rem 2.5rem !important;
                border: 1px solid rgba(197, 160, 34, 0.2) !important;
                box-shadow: 0 40px 100px -20px rgba(0, 0, 0, 0.4) !important;
                transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
                position: relative !important;
            }
            [data-testid="stColumn"]:has(.pricing-card-2-trigger):hover {
                transform: translateY(-10px) !important;
                box-shadow: 0 60px 120px -30px rgba(0, 0, 0, 0.5) !important;
            }

            /* Pledge Panel Block */
            [data-testid="stHorizontalBlock"]:has(.pledge-left-trigger) {
                background-color: var(--theme-green) !important;
                padding: 6rem 4rem !important;
                color: white !important;
                border-radius: 4rem !important;
                overflow: visible !important;
                margin-top: 4rem !important;
                margin-bottom: 4rem !important;
            }
            
            /* Pledge Right Column Card Containment */
            [data-testid="stColumn"]:has(.pledge-right-trigger) {
                background-color: var(--theme-white) !important;
                padding: 3rem !important;
                border-radius: 3rem !important;
                box-shadow: 0 40px 80px -20px rgba(0,0,0,0.3) !important;
                position: relative !important;
            }

            /* Force internal elements to fill height and align perfectly */
            [data-testid="stColumn"]:has(.pricing-card-1-trigger) div[data-testid="stVerticalBlock"],
            [data-testid="stColumn"]:has(.pricing-card-2-trigger) div[data-testid="stVerticalBlock"],
            [data-testid="stColumn"]:has(.pricing-card-3-trigger) div[data-testid="stVerticalBlock"],
            [data-testid="stColumn"]:has(.hero-right-trigger) div[data-testid="stVerticalBlock"],
            [data-testid="stColumn"]:has(.pledge-right-trigger) div[data-testid="stVerticalBlock"] {
                height: 100% !important;
                display: flex !important;
                flex-direction: column !important;
                justify-content: space-between !important;
                gap: 1rem !important;
            }

            /* FAQs Accordions */
            [data-testid="stExpander"] {
                background-color: var(--theme-white) !important;
                border-radius: 2rem !important;
                border: 1px solid var(--theme-gray-light) !important;
                box-shadow: 0 4px 12px rgba(0,0,0,0.02) !important;
                margin-bottom: 1rem !important;
                padding: 0.5rem 1rem !important;
            }
            [data-testid="stExpander"] summary {
                font-weight: 700 !important;
                color: var(--theme-black) !important;
                font-size: 1.1rem !important;
            }

            /* Footer Containment */
            [data-testid="stHorizontalBlock"]:has(.footer-trigger) {
                background-color: var(--theme-black) !important;
                color: var(--theme-white) !important;
                padding: 6rem 3rem 4rem 3rem !important;
                border-radius: 4rem 4rem 0 0 !important;
                overflow: visible !important;
                margin-top: 6rem !important;
            }

            /* --- COMPONENT LEVEL STYLE INJECTIONS ON SPAN ELEMENTS --- */

            /* Section Badging */
            .badge-span {
                display: inline-block;
                padding: 0.4rem 1.2rem;
                background-color: var(--theme-cream);
                border: 1px solid rgba(197, 160, 34, 0.3);
                color: var(--theme-gold);
                font-size: 11px;
                font-weight: 900;
                letter-spacing: 0.3em;
                text-transform: uppercase;
                border-radius: 9999px;
                margin-bottom: 2rem;
                box-shadow: 0 1px 2px rgba(0,0,0,0.03);
                width: fit-content;
            }
            .heading-main {
                font-size: 4.5rem;
                font-weight: 700;
                line-height: 0.95;
                color: var(--theme-black);
                display: block;
                margin-bottom: 2rem;
            }
            .heading-italic-green {
                font-style: italic;
                color: var(--theme-green);
            }
            .desc-text {
                font-size: 1.25rem;
                color: #6b7280;
                font-weight: 300;
                line-height: 1.6;
                display: block;
                max-width: 32rem;
                margin-bottom: 3rem;
            }

            /* Inner Card Floating Elements */
            .green-card-inner {
                background-color: var(--theme-green);
                border-radius: 3.5rem;
                overflow: hidden;
                flex: 1;
                display: flex;
                flex-direction: column;
                justify-content: center;
                padding: 4rem;
                position: relative;
                animation: float-animation 8s ease-in-out infinite;
            }
            @keyframes float-animation {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-16px); }
            }
            .gold-accent-line {
                height: 6px;
                width: 5rem;
                background-color: var(--theme-gold);
                border-radius: 9999px;
                margin-bottom: 2.5rem;
                display: block;
            }
            .card-heading {
                font-size: 3.5rem;
                font-style: italic;
                font-weight: 700;
                color: var(--theme-white);
                display: block;
                margin-bottom: 1.5rem;
                line-height: 1.1;
            }
            .card-description {
                font-size: 1.2rem;
                color: rgba(255,255,255,0.7);
                font-weight: 300;
                display: block;
                max-width: 18rem;
                line-height: 1.5;
            }
            .gem-icon {
                position: absolute;
                top: 3rem;
                right: 3rem;
                color: rgba(197, 160, 34, 0.4);
                display: block;
            }
            .floating-badge {
                position: absolute;
                bottom: -1.5rem;
                left: -1.5rem;
                background-color: var(--theme-white);
                padding: 1.2rem 2rem;
                border-radius: 2.5rem;
                box-shadow: 0 30px 60px -15px rgba(0,0,0,0.25);
                z-index: 30;
                display: flex;
                align-items: center;
                gap: 1.2rem;
                border: 1px solid #f9fafb;
                transform: rotate(-3deg);
            }
            .badge-circle {
                background-color: var(--theme-green);
                width: 3.5rem;
                height: 3.5rem;
                border-radius: 1.2rem;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            /* Pricing Cards specific markup */
            .tier-label {
                color: var(--theme-gold);
                font-weight: 900;
                letter-spacing: 0.2em;
                text-transform: uppercase;
                font-size: 11px;
                margin-bottom: 0.5rem;
                display: block;
            }
            .pricing-card-title {
                font-size: 2.2rem;
                font-weight: 700;
                margin-bottom: 1.5rem;
                display: block;
                color: var(--theme-black);
            }
            .pricing-card-title-white {
                color: var(--theme-white);
                font-style: italic;
                font-size: 2.2rem;
                font-weight: 700;
                margin-bottom: 1.5rem;
                display: block;
            }
            .price-container {
                margin-bottom: 2.5rem;
                display: block;
            }
            .price-number {
                font-size: 3.5rem;
                font-weight: 700;
                color: var(--theme-black);
                display: inline-block;
            }
            .price-number-dark {
                color: var(--theme-white);
                font-size: 3.5rem;
                font-weight: 700;
                display: inline-block;
            }
            .price-period {
                font-style: italic;
                color: #9ca3af;
                font-size: 1.1rem;
                margin-left: 0.25rem;
                display: inline-block;
            }
            .feature-box {
                display: flex;
                flex-direction: column;
                gap: 1.25rem;
                flex-grow: 1;
            }
            .feature-item {
                display: flex;
                align-items: center;
                gap: 1rem;
            }
            .icon-circle {
                width: 1.8rem;
                height: 1.8rem;
                border-radius: 50%;
                background-color: rgba(6, 78, 59, 0.05);
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
            }
            .icon-circle-dark {
                background-color: rgba(255,255,255,0.1);
                width: 1.8rem;
                height: 1.8rem;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
            }
            .icon-circle-gold {
                background-color: var(--theme-gold);
                width: 1.8rem;
                height: 1.8rem;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
            }
            .feature-text {
                font-size: 1rem;
                color: #4b5563;
                font-weight: 300;
            }
            .feature-text-white {
                color: rgba(255,255,255,0.7);
                font-size: 1rem;
                font-weight: 300;
            }
            .feature-text-bold {
                font-weight: 700;
                color: var(--theme-white);
                font-size: 1rem;
            }
            .recommended-badge {
                position: absolute;
                top: 0;
                right: 0;
                background: linear-gradient(135deg, #c5a022 0%, #a6841a 100%);
                color: var(--theme-white);
                font-size: 9px;
                font-weight: 900;
                letter-spacing: 0.2em;
                text-transform: uppercase;
                padding: 0.75rem 1.5rem;
                border-bottom-left-radius: 1.5rem;
                z-index: 5;
                display: block;
            }

            /* Section Pledge (Guarantees) details */
            .italic-gold {
                font-style: italic;
                color: var(--theme-gold);
            }
            .pledge-row {
                display: flex;
                gap: 1.25rem;
                align-items: flex-start;
                margin-bottom: 1.5rem;
            }
            .pledge-icon-box {
                width: 2.8rem;
                height: 2.8rem;
                background-color: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 0.8rem;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
            }
            .pledge-row-title {
                font-size: 1.1rem;
                font-weight: 700;
                color: var(--theme-white);
                display: block;
                margin-bottom: 0.25rem;
            }
            .pledge-row-desc {
                font-size: 0.9rem;
                font-weight: 300;
                color: rgba(255,255,255,0.55);
                line-height: 1.4;
                display: block;
            }
            .gold-pulse-box {
                width: 3rem;
                height: 3rem;
                background-color: var(--theme-gold);
                border-radius: 0.8rem;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 2rem;
                animation: pulse-gold-effect 3s infinite;
                display: block;
            }
            @keyframes pulse-gold-effect {
                0% { box-shadow: 0 0 0 0 rgba(197, 160, 34, 0.4); }
                70% { box-shadow: 0 0 0 15px rgba(197, 160, 34, 0); }
                100% { box-shadow: 0 0 0 0 rgba(197, 160, 34, 0); }
            }

            /* Footer Inner elements */
            .footer-logo-text {
                font-size: 1.6rem;
                font-weight: 700;
                letter-spacing: -0.02em;
                display: block;
                margin-bottom: 1.5rem;
            }
            .footer-bio {
                font-size: 0.9rem;
                color: #888888;
                font-weight: 300;
                line-height: 1.6;
                display: block;
                max-width: 18rem;
            }
            .footer-heading {
                font-size: 0.7rem;
                font-weight: 900;
                text-transform: uppercase;
                letter-spacing: 0.25em;
                color: var(--theme-gold);
                display: block;
                margin-bottom: 2rem;
            }
            .footer-link-span {
                font-size: 0.9rem;
                color: #cccccc;
                font-weight: 300;
                display: block;
                margin-bottom: 1rem;
                cursor: pointer;
                transition: color 0.3s ease;
            }
            .footer-link-span:hover {
                color: var(--theme-gold);
            }
            .footer-contact-row {
                display: flex;
                align-items: center;
                gap: 0.75rem;
                margin-bottom: 1.25rem;
            }
            .footer-bottom-bar {
                border-top: 1px solid rgba(255,255,255,0.05);
                padding-top: 2rem;
                margin-top: 5rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .copyright-text {
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.15em;
                color: #555555;
                display: block;
            }
            .status-pill {
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            .status-dot {
                width: 6px;
                height: 6px;
                background-color: #22c55e;
                border-radius: 50%;
                box-shadow: 0 0 10px #22c55e;
                animation: pulse-dot-effect 2s infinite;
                display: block;
            }
            @keyframes pulse-dot-effect {
                0%, 100% { opacity: 0.4; }
                50% { opacity: 1; }
            }

            /* --- NATIVE STREAMLIT COMPONENT OVERRIDES --- */
            
            /* Primary CTA Button */
            [data-testid="stColumn"] .stButton button {
                background: linear-gradient(135deg, var(--theme-gold) 0%, #a6841a 100%) !important;
                color: var(--theme-white) !important;
                font-weight: 700 !important;
                font-size: 1.1rem !important;
                padding: 1.2rem 3rem !important;
                border-radius: 9999px !important;
                border: none !important;
                box-shadow: 0 20px 40px -12px rgba(197, 160, 34, 0.45) !important;
                transition: all 0.3s ease !important;
                text-transform: none !important;
                width: auto !important;
                margin-top: 1.5rem !important;
            }
            [data-testid="stColumn"] .stButton button:hover {
                transform: translateY(-3px) scale(1.02) !important;
                box-shadow: 0 30px 50px -12px rgba(197, 160, 34, 0.6) !important;
            }

            /* Light Pricing Card Buttons (Tiers 1 & 3) */
            [data-testid="stColumn"]:has(.pricing-card-1-trigger) .stButton button,
            [data-testid="stColumn"]:has(.pricing-card-3-trigger) .stButton button {
                width: 100% !important;
                border: 2px solid var(--theme-black) !important;
                color: var(--theme-black) !important;
                background-color: transparent !important;
                border-radius: 1.25rem !important;
                font-weight: 700 !important;
                font-size: 11px !important;
                text-transform: uppercase !important;
                letter-spacing: 0.15em !important;
                padding: 1.25rem !important;
                margin-top: auto !important;
                box-shadow: none !important;
                transition: all 0.3s ease !important;
            }
            [data-testid="stColumn"]:has(.pricing-card-1-trigger) .stButton button:hover,
            [data-testid="stColumn"]:has(.pricing-card-3-trigger) .stButton button:hover {
                background-color: var(--theme-black) !important;
                color: var(--theme-white) !important;
                transform: none !important;
            }

            /* Dark Pricing Card Button (Tier 2) */
            [data-testid="stColumn"]:has(.pricing-card-2-trigger) .stButton button {
                width: 100% !important;
                background: linear-gradient(135deg, var(--theme-gold) 0%, #a6841a 100%) !important;
                border: none !important;
                color: var(--theme-white) !important;
                border-radius: 1.25rem !important;
                font-weight: 700 !important;
                font-size: 11px !important;
                text-transform: uppercase !important;
                letter-spacing: 0.15em !important;
                padding: 1.25rem !important;
                margin-top: auto !important;
                box-shadow: 0 15px 30px -10px rgba(197, 160, 34, 0.4) !important;
                transition: all 0.3s ease !important;
            }
            [data-testid="stColumn"]:has(.pricing-card-2-trigger) .stButton button:hover {
                opacity: 0.95 !important;
                transform: scale(0.98) !important;
            }

            /* Quality Charter Standard Button */
            [data-testid="stColumn"]:has(.pledge-right-trigger) .stButton button {
                background-color: var(--theme-green) !important;
                color: var(--theme-white) !important;
                padding: 0.8rem 1.5rem !important;
                border-radius: 1.25rem !important;
                font-weight: 700 !important;
                font-size: 11px !important;
                text-transform: uppercase !important;
                letter-spacing: 0.15em !important;
                border: none !important;
                width: 100% !important;
                margin-top: auto !important;
                box-shadow: none !important;
                transition: all 0.3s ease !important;
            }
            [data-testid="stColumn"]:has(.pledge-right-trigger) .stButton button:hover {
                background-color: var(--theme-black) !important;
                transform: none !important;
            }

            /* Footer Subscription Input & Button styling */
            .footer-newsletter-btn .stButton button {
                background-color: var(--theme-gold) !important;
                color: var(--theme-black) !important;
                border-radius: 0.75rem !important;
                font-weight: 700 !important;
                font-size: 11px !important;
                text-transform: uppercase !important;
                letter-spacing: 0.1em !important;
                border: none !important;
                padding: 0.5rem 1.5rem !important;
                box-shadow: none !important;
                transition: all 0.3s ease !important;
                margin-top: 0 !important;
            }
            .footer-newsletter-btn .stButton button:hover {
                background-color: var(--theme-white) !important;
                color: var(--theme-black) !important;
                transform: none !important;
            }
            .footer-newsletter-input input {
                background-color: rgba(255,255,255,0.03) !important;
                border: 1px solid rgba(255,255,255,0.1) !important;
                color: var(--theme-white) !important;
                border-radius: 0.75rem !important;
                padding: 0.75rem !important;
            }
        </style>
    """, unsafe_allow_html=True)

def inject_lucide_renderer():
    """Injects Lucide script with MutationObserver to re-render custom vector icons cleanly."""
    st.markdown("""
        <script src="https://unpkg.com/lucide@latest"></script>
        <script>
            function renderIcons() {
                if (typeof lucide !== 'undefined') lucide.createIcons();
            }
            window.addEventListener('load', renderIcons);
            const observer = new MutationObserver(renderIcons);
            observer.observe(document.body, { childList: true, subtree: true });
        </script>
    """, unsafe_allow_html=True)

def render_header():
    """Renders the sticky premium header bar using span elements."""
    st.markdown('<span class="navbar-trigger" style="display:none;"></span>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
            <span style="display: flex; align-items: center; gap: 0.75rem;">
                <span style="width: 2.5rem; height: 2.5rem; background-color: #064e3b; border-radius: 0.75rem; display: flex; align-items: center; justify-content: center; transform: rotate(3deg); box-shadow: 0 4px 10px rgba(6,78,59,0.15);">
                    <span style="color: white; font-weight: 900; font-size: 1.3rem; font-family: 'Playfair Display', serif;">A</span>
                </span>
                <span class="font-sans" style="font-size: 1.5rem; font-weight: 700; letter-spacing: -0.02em; color: #0a0a0a; display: inline-block;">afri<span style="color: #c5a022;">design</span></span>
            </span>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <span style="display: flex; justify-content: flex-end; align-items: center; height: 100%; gap: 1.5rem;">
                <span style="font-size: 11px; font-weight: 900; letter-spacing: 0.15em; text-transform: uppercase; color: #888888; display: inline-block;">Concierge Support</span>
                <span style="font-size: 14px; font-weight: 700; color: #0a0a0a; display: inline-block;">011 612 7200</span>
            </span>
        """, unsafe_allow_html=True)

def render_hero():
    """Renders the symmetrical structurally balanced Hero component using span elements."""
    st.markdown('<span class="hero-wrapper" style="display:block;">', unsafe_allow_html=True)
    left_col, right_col = st.columns([1.1, 0.9])
    
    with left_col:
        st.markdown('<span class="hero-left-trigger" style="display:none;"></span>', unsafe_allow_html=True)
        st.markdown('<span class="badge-span">Bespoke Managed Services</span>', unsafe_allow_html=True)
        st.markdown("""
            <span class="heading-main font-serif">
                The Gold Standard of <span class="heading-italic-green">Web Design.</span>
            </span>
            <span class="desc-text">
                Managed hosting, complete maintenance, and world-class craft curated for South Africa's most ambitious brands. Experience digital distinction built for legacy.
            </span>
        """, unsafe_allow_html=True)
        
        # Streamlit CTA block
        if st.button("View The Collection", key="hero_cta_btn"):
            st.toast("✨ Accessing premium collections vault...", icon="💎")

        st.markdown("""
            <span style="display: flex; align-items: center; margin-top: 3.5rem; gap: 1.5rem;">
                <span style="height: 3.5rem; width: 1px; background-color: #e5e7eb; display: block;"></span>
                <span style="display: flex; flex-direction: column;">
                    <span style="font-size: 10px; font-weight: 900; color: #9ca3af; letter-spacing: 0.15em; text-transform: uppercase; display: block;">Limited</span>
                    <span style="font-size: 0.85rem; font-weight: 700; color: #111827; letter-spacing: 0.05em; text-transform: uppercase; display: block;">Quarterly Openings</span>
                </span>
            </span>
        """, unsafe_allow_html=True)
        
    with right_col:
        st.markdown('<span class="hero-right-trigger" style="display:none;"></span>', unsafe_allow_html=True)
        st.markdown("""
            <span class="green-card-inner" style="display: flex;">
                <span class="gold-accent-line"></span>
                <span class="card-heading font-serif">48h Delivery.</span>
                <span class="card-description">
                    Hand-crafted digital experiences delivered with surgical precision and absolute managed care.
                </span>
                <span class="gem-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-gem"><path d="M6 3h12l4 6-10 13L2 9Z"/><path d="M11 3 8 9l3 13 3-13-3-6Z"/><path d="M2 9h20"/></svg>
                </span>
            </span>
            <span class="floating-badge">
                <span class="badge-circle">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#c5a022" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
                </span>
                <span style="display: flex; flex-direction: column;">
                    <span style="font-size: 10px; font-weight: 900; color: #9ca3af; letter-spacing: 0.1em; text-transform: uppercase; display: block;">Quality</span>
                    <span style="font-size: 0.9rem; font-weight: 700; color: #111827; text-transform: uppercase; display: block;">Guaranteed</span>
                </span>
            </span>
            <span style="position: absolute; top: -50px; left: -50px; width: 200px; height: 200px; background: rgba(197, 160, 34, 0.08); filter: blur(80px); border-radius: 50%; z-index: 0; display: block;"></span>
            <span style="position: absolute; bottom: -50px; right: -50px; width: 300px; height: 300px; background: rgba(6, 78, 59, 0.05); filter: blur(100px); border-radius: 50%; z-index: 0; display: block;"></span>
        """, unsafe_allow_html=True)
        
    st.markdown('</span>', unsafe_allow_html=True)

def render_pricing():
    """Renders the beautifully balanced 3-column Pricing Grid using span elements."""
    st.markdown('<span style="max-width: 1400px; margin: 0 auto; padding: 6rem 2rem 0 2rem; display: block;">', unsafe_allow_html=True)
    st.markdown('<span class="section-badge" style="display: inline-block; padding: 0.4rem 1.2rem; background-color: rgba(6,78,59,0.05); color: var(--theme-green); font-size: 11px; font-weight: 900; letter-spacing: 0.3em; text-transform: uppercase; border-radius: 9999px; margin-bottom: 2rem;">Investment Tiers</span>', unsafe_allow_html=True)
    st.markdown('<span class="font-serif" style="font-size: 3.5rem; font-weight: 700; line-height: 1.1; margin-bottom: 4rem; display: block;">Curated Packages for <br><span class="heading-italic-green">Digital Distinction.</span></span>', unsafe_allow_html=True)
    st.markdown('</span>', unsafe_allow_html=True)

    grid_container = st.container()
    with grid_container:
        col1, col2, col3 = st.columns(3, gap="large")

        # ---------- TIER 01: BRONZE ----------
        with col1:
            st.markdown('<span class="pricing-card-1-trigger" style="display:none;"></span>', unsafe_allow_html=True)
            st.markdown("""
                <span class="tier-label">Tier 01</span>
                <span class="pricing-card-title font-serif">Bronze</span>
                <span class="price-container">
                    <span class="price-number">R309</span><span class="price-period">/mo</span>
                </span>
                <span class="feature-box">
                    <span class="feature-item">
                        <span class="icon-circle"><i data-lucide="check" style="color: #064e3b; width: 1rem; height: 1rem;"></i></span>
                        <span class="feature-text">Bespoke 3-Page Build</span>
                    </span>
                    <span class="feature-item">
                        <span class="icon-circle"><i data-lucide="shield-check" style="color: #064e3b; width: 1rem; height: 1rem;"></i></span>
                        <span class="feature-text">Premium Managed Hosting</span>
                    </span>
                    <span class="feature-item">
                        <span class="icon-circle"><i data-lucide="clock" style="color: #064e3b; width: 1rem; height: 1rem;"></i></span>
                        <span class="feature-text">Monthly Concierge Hour</span>
                    </span>
                </span>
            """, unsafe_allow_html=True)
            
            if st.button("Apply for Bronze", key="btn_bronze"):
                st.toast("🥉 Bronze tier onboarding initiated.", icon="✨")

        # ---------- TIER 02: SILVER (Featured) ----------
        with col2:
            st.markdown('<span class="pricing-card-2-trigger" style="display:none;"></span>', unsafe_allow_html=True)
            st.markdown("""
                <span class="recommended-badge">Recommended</span>
                <span class="tier-label">Tier 02</span>
                <span class="pricing-card-title-white font-serif">Silver</span>
                <span class="price-container">
                    <span class="price-number-dark">R449</span><span class="price-period">/mo</span>
                </span>
                <span class="feature-box">
                    <span class="feature-item">
                        <span class="icon-circle-dark"><i data-lucide="check" style="color: #c5a022; width: 1rem; height: 1rem;"></i></span>
                        <span class="feature-text feature-text-white">Expansive 6-Page Build</span>
                    </span>
                    <span class="feature-item">
                        <span class="icon-circle-dark"><i data-lucide="zap" style="color: #c5a022; width: 1rem; height: 1rem;"></i></span>
                        <span class="feature-text feature-text-white">Executive Priority Build</span>
                    </span>
                    <span class="icon-circle-gold" style="display:none;"></span> <!-- alignment proxy -->
                    <span class="feature-item">
                        <span class="icon-circle-gold"><i data-lucide="star" style="color: white; width: 1rem; height: 1rem;"></i></span>
                        <span class="feature-text-bold">VIP Support Line</span>
                    </span>
                </span>
            """, unsafe_allow_html=True)
            
            if st.button("Secure Silver", key="btn_silver"):
                st.toast("🥈 Silver tier priority access granted.", icon="✨")

        # ---------- TIER 03: GOLD ----------
        with col3:
            st.markdown('<span class="pricing-card-3-trigger" style="display:none;"></span>', unsafe_allow_html=True)
            st.markdown("""
                <span class="tier-label">Tier 03</span>
                <span class="pricing-card-title font-serif">Gold</span>
                <span class="price-container">
                    <span class="price-number">R599</span><span class="price-period">/mo</span>
                </span>
                <span class="feature-box">
                    <span class="feature-item">
                        <span class="icon-circle"><i data-lucide="check" style="color: #064e3b; width: 1rem; height: 1rem;"></i></span>
                        <span class="feature-text">Unlimited 12-Page Build</span>
                    </span>
                    <span class="feature-item">
                        <span class="icon-circle"><i data-lucide="shopping-bag" style="color: #064e3b; width: 1rem; height: 1rem;"></i></span>
                        <span class="feature-text">Commerce Integration</span>
                    </span>
                    <span class="feature-item">
                        <span class="icon-circle"><i data-lucide="award" style="color: #064e3b; width: 1rem; height: 1rem;"></i></span>
                        <span class="feature-text">Strategic Quarterly Review</span>
                    </span>
                </span>
            """, unsafe_allow_html=True)
            
            if st.button("Apply for Gold", key="btn_gold"):
                st.toast("🥇 Gold tier executive suite initiated.", icon="✨")

def render_pledge():
    """Renders the balanced, high-contrast, emerald and gold Pledge layout using span elements."""
    with st.container():
        col_left, col_right = st.columns([1, 1], gap="large")

        with col_left:
            st.markdown('<span class="pledge-left-trigger" style="display:none;"></span>', unsafe_allow_html=True)
            st.markdown('<span class="section-badge font-sans" style="border: 1px solid rgba(255,255,255,0.15) !important; display: inline-block; padding: 0.4rem 1.2rem; background-color: rgba(6,78,59,0.05); color: var(--theme-gold); font-size: 11px; font-weight: 900; letter-spacing: 0.3em; text-transform: uppercase; border-radius: 9999px; margin-bottom: 2rem;">The afridesign Standard</span>', unsafe_allow_html=True)
            st.markdown('<span class="font-serif" style="font-size: 2.8rem; font-weight: 700; line-height: 1.1; margin-bottom: 2rem; display: block;">Our Pledge of<br><span class="italic-gold">Absolute Quality.</span></span>', unsafe_allow_html=True)

            st.markdown("""
                <span style="display: flex; flex-direction: column; gap: 1.5rem; flex-grow: 1;">
                    <span class="pledge-row">
                        <span class="pledge-icon-box"><i data-lucide="clock-3" style="color: #c5a022; width: 1.1rem; height: 1.1rem;"></i></span>
                        <span style="display: flex; flex-direction: column;">
                            <span class="pledge-row-title font-sans">48-Hour Deployment</span>
                            <span class="pledge-row-desc font-sans">Elite execution. Your project goes live in days, or your first month is on us.</span>
                        </span>
                    </span>
                    <span class="pledge-row">
                        <span class="pledge-icon-box"><i data-lucide="heart" style="color: #c5a022; width: 1.1rem; height: 1.1rem;"></i></span>
                        <span style="display: flex; flex-direction: column;">
                            <span class="pledge-row-title font-sans">The "Love It" Clause</span>
                            <span class="pledge-row-desc font-sans">If the initial aesthetic doesn't captivate you, we redesign until it does. No questions.</span>
                        </span>
                    </span>
                    <span class="pledge-row">
                        <span class="pledge-icon-box"><i data-lucide="zap" style="color: #c5a022; width: 1.1rem; height: 1.1rem;"></i></span>
                        <span style="display: flex; flex-direction: column;">
                            <span class="pledge-row-title font-sans">Performance Benchmark</span>
                            <span class="pledge-row-desc font-sans">Every build is optimized. We guarantee a Google PageSpeed score of 80+.</span>
                        </span>
                    </span>
                </span>
            """, unsafe_allow_html=True)

        with col_right:
            st.markdown('<span class="pledge-right-trigger" style="display:none;"></span>', unsafe_allow_html=True)
            st.markdown("""
                <span class="gold-pulse-box">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-gem"><path d="M6 3h12l4 6-10 13L2 9Z"/><path d="M11 3 8 9l3 13 3-13-3-6Z"/><path d="M2 9h20"/></svg>
                </span>
                <span class="font-serif" style="font-size: 1.8rem; font-weight: 700; font-style: italic; display: block; margin-bottom: 1rem; color: #0a0a0a;">Excellence by Default.</span>
                <span class="font-sans" style="font-size: 0.95rem; color: #6b7280; font-weight: 300; line-height: 1.5; margin-bottom: 2rem; display: block; flex-grow: 1;">Join South Africa's most prestigious network of businesses powered by Afrihost managed technology. We don't just build sites; we manage digital legacies.</span>
            """, unsafe_allow_html=True)
            
            if st.button("Start Your Journey", key="btn_pledge_charter"):
                st.toast("🛡️ Quality standard registered. Welcome onboard.", icon="💎")

def render_faqs():
    """Renders highly styled native Streamlit Expander accordions."""
    st.markdown('<span style="max-width: 800px; margin: 0 auto; padding: 6rem 2rem 6rem 2rem; display: block;">', unsafe_allow_html=True)
    st.markdown('<span class="font-serif" style="font-size: 3rem; font-weight: 700; text-align: center; margin-bottom: 3rem; color: #0a0a0a; display: block;">Concierge Queries</span>', unsafe_allow_html=True)
    st.markdown('</span>', unsafe_allow_html=True)
    
    with st.expander("Who owns the finalized design?"):
        st.write("Ownership remains with Afrihost as part of the managed service ecosystem. However, a buyout option is available after 24 months of active subscription should you wish to take the assets elsewhere.")
        
    with st.expander("What happens if I need content updates?"):
        st.write("Every month, your membership includes dedicated concierge designer hours depending on your chosen tier. Just send your text, images, or layout edits to your support manager and we'll apply them securely.")
        
    with st.expander("Is dynamic checkout e-commerce supported?"):
        st.write("E-commerce integration is fully optimized and supported natively starting with our Gold Tier plan. We implement dynamic checkout flows, secure payment gateways, and South African shipping calculators.")

def render_footer():
    """Renders the rich Black 4-column footer at the bottom of the landing page using span elements."""
    st.markdown('<span class="footer-trigger" style="display:none;"></span>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1.5])

    with col1:
        st.markdown("""
            <span class="footer-logo-text font-sans" style="color: white; display: block;">afri<span style="color: #c5a022;">design</span></span>
            <span class="footer-bio font-sans" style="display: block;">Hand-crafting the digital future for South Africa's most ambitious brands. Bespoke design meets surgical precision.</span>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<span class="footer-heading font-sans">Collection</span>', unsafe_allow_html=True)
        st.markdown('<span class="footer-link-span">The Collection</span>', unsafe_allow_html=True)
        st.markdown('<span class="footer-link-span">Managed Care</span>', unsafe_allow_html=True)
        st.markdown('<span class="footer-link-span">Design Ethos</span>', unsafe_allow_html=True)

    with col3:
        st.markdown('<span class="footer-heading font-sans">Concierge</span>', unsafe_allow_html=True)
        st.markdown("""
            <span class="footer-contact-row" style="display: flex;">
                <i data-lucide="phone" style="color: #c5a022; width: 0.9rem; height: 0.9rem;"></i>
                <span class="footer-link-span" style="margin-bottom: 0;">+27 11 612 7200</span>
            </span>
            <span class="footer-contact-row" style="display: flex;">
                <i data-lucide="mail" style="color: #c5a022; width: 0.9rem; height: 0.9rem;"></i>
                <span class="footer-link-span" style="margin-bottom: 0;">concierge@afridesign.za</span>
            </span>
            <span class="footer-contact-row" style="display: flex;">
                <i data-lucide="map-pin" style="color: #c5a022; width: 0.9rem; height: 0.9rem;"></i>
                <span class="footer-link-span" style="margin-bottom: 0;">Sandton, RSA</span>
            </span>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown('<span class="footer-heading font-sans">Membership</span>', unsafe_allow_html=True)
        st.markdown('<span class="footer-bio font-sans" style="margin-bottom: 1.5rem; display: block;">Join our private list for quarterly availability updates.</span>', unsafe_allow_html=True)
        
        # Streamlit inputs wrapper inside target span
        st.markdown('<span class="footer-newsletter-input" style="display:block;">', unsafe_allow_html=True)
        email = st.text_input("Email Address", placeholder="Enter your email...", label_visibility="collapsed")
        st.markdown('</span>', unsafe_allow_html=True)
        
        st.markdown('<span class="footer-newsletter-btn" style="margin-top: 0.75rem; display:block;">', unsafe_allow_html=True)
        if st.button("Join List", key="newsletter_submit_btn"):
            if email:
                st.toast("🛡️ Successfully added to our private elite database.", icon="✨")
            else:
                st.toast("⚠️ Please enter a valid email address.", icon="🔍")
        st.markdown('</span>', unsafe_allow_html=True)

    # Bottom footer copyrights
    st.markdown("""
        <span class="footer-bottom-bar" style="display: flex;">
            <span class="copyright-text font-sans">© 2026 afridesign Managed Services. Pure Digital Joy.</span>
            <span class="status-pill" style="display: flex;">
                <span class="status-dot"></span>
                <span class="copyright-text font-sans" style="color: #888888; font-size: 10px;">Accepting 2 Private Projects</span>
            </span>
        </span>
    """, unsafe_allow_html=True)

def main():
    """Central runner executing all modular design layouts."""
    # 1. Inject Styles
    inject_master_styles()
    inject_lucide_renderer()
    
    # 2. Render Page Blocks sequentially
    render_header()
    render_hero()
    render_pricing()
    render_pledge()
    render_faqs()
    render_footer()

if __name__ == "__main__":
    main()