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

            /* === FIXED HEADER STYLES (Direct class) === */
            .premium-navbar {
                background-color: rgba(255, 255, 255, 0.85) !important;
                backdrop-filter: blur(20px) !important;
                border-bottom: 1px solid rgba(197, 160, 34, 0.1) !important;
                padding: 1.5rem 3rem !important;
                position: sticky !important;
                top: 0 !important;
                z-index: 1000 !important;
                border-radius: 0 0 2rem 2rem !important;
                margin-bottom: 2rem;
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

            /* --- NEW SECTION: CONTACT FORM --- */
            .contact-container {
                max-width: 1000px;
                margin: 0 auto;
                padding: 4rem 2rem;
            }
            .contact-card {
                background: var(--theme-white);
                border-radius: 2rem;
                padding: 3rem;
                border: 1px solid var(--theme-gray-light);
                box-shadow: 0 20px 40px -12px rgba(0,0,0,0.05);
            }
            .contact-form-field {
                margin-bottom: 1.5rem;
            }
            .contact-form-field label {
                font-weight: 600;
                color: var(--theme-black);
                display: block;
                margin-bottom: 0.5rem;
            }
            .contact-form-field input, .contact-form-field select, .contact-form-field textarea {
                width: 100%;
                padding: 0.75rem;
                border: 1px solid #e5e7eb;
                border-radius: 0.75rem;
                font-family: 'Inter', sans-serif;
            }
            .contact-submit-btn .stButton button {
                background: linear-gradient(135deg, var(--theme-gold) 0%, #a6841a 100%) !important;
                width: 100% !important;
                padding: 0.75rem !important;
            }

            /* --- ROADMAP SECTION (FIXED with overlapping buttons) --- */
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
            .roadmap-step {
                margin-top: -1rem;
                position: relative;
                z-index: 2;
                width: 100%;
                padding: 0 0.25rem;
            }
            .roadmap-step .stButton {
                width: 100%;
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
            [data-testid="column"]:has(.step-card) {
                display: flex !important;
                height: 100% !important;
            }
            .roadmap-quote {
                margin-top: 4rem;
                padding-top: 2rem;
                border-top: 1px solid #e5e7eb;
            }
            .quote-text {
                font-family: 'Playfair Display', serif;
                font-style: italic;
                font-size: 1.5rem;
                color: #064e3b;
            }
            .quote-attribution {
                color: #6b7280;
                font-size: 0.8rem;
                margin-top: 0.5rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.1em;
            }

            /* --- COMPONENT LEVEL STYLE INJECTIONS ON SPAN ELEMENTS --- */
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
            }
            [data-testid="stColumn"]:has(.pricing-card-1-trigger) .stButton button:hover,
            [data-testid="stColumn"]:has(.pricing-card-3-trigger) .stButton button:hover {
                background-color: var(--theme-black) !important;
                color: var(--theme-white) !important;
            }
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
            }
            [data-testid="stColumn"]:has(.pricing-card-2-trigger) .stButton button:hover {
                opacity: 0.95 !important;
                transform: scale(0.98) !important;
            }
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
            }
            [data-testid="stColumn"]:has(.pledge-right-trigger) .stButton button:hover {
                background-color: var(--theme-black) !important;
            }
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
                margin-top: 0 !important;
            }
            .footer-newsletter-btn .stButton button:hover {
                background-color: var(--theme-white) !important;
                color: var(--theme-black) !important;
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
            
            // Counter animation
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
            
            document.querySelectorAll('.stat-number-value').forEach(el => observerCounters.observe(el));
        </script>
    """, unsafe_allow_html=True)

def render_header():
    st.markdown("""
        <div class="premium-navbar">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <div style="width: 2.5rem; height: 2.5rem; background-color: #064e3b; border-radius: 0.75rem; display: flex; align-items: center; justify-content: center; transform: rotate(3deg); box-shadow: 0 4px 10px rgba(6,78,59,0.15);">
                        <span style="color: white; font-weight: 900; font-size: 1.3rem; font-family: 'Playfair Display', serif;">A</span>
                    </div>
                    <span style="font-size: 1.5rem; font-weight: 700; letter-spacing: -0.02em; color: #0a0a0a;">afri<span style="color: #c5a022;">design</span></span>
                </div>
                <div style="display: flex; align-items: center; gap: 1.5rem;">
                    <span style="font-size: 11px; font-weight: 900; letter-spacing: 0.15em; text-transform: uppercase; color: #888888;">Concierge Support</span>
                    <span style="font-size: 14px; font-weight: 700; color: #0a0a0a;">011 612 7200</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_hero():
    left_col, right_col = st.columns([1.1, 0.9])
    with left_col:
        st.markdown('<span class="badge-span">Bespoke Managed Services</span>', unsafe_allow_html=True)
        st.markdown("""
            <span class="heading-main font-serif">
                The Gold Standard of <span class="heading-italic-green">Web Design.</span>
            </span>
            <span class="desc-text">
                Managed hosting, complete maintenance, and world-class craft curated for South Africa's most ambitious brands. Experience digital distinction built for legacy.
            </span>
        """, unsafe_allow_html=True)
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

def render_pricing():
    st.markdown('<span style="max-width: 1400px; margin: 0 auto; padding: 6rem 2rem 0 2rem; display: block;">', unsafe_allow_html=True)
    st.markdown('<span class="badge-span" style="background-color: rgba(6,78,59,0.05); color: var(--theme-green);">Investment Tiers</span>', unsafe_allow_html=True)
    st.markdown('<span class="font-serif" style="font-size: 3.5rem; font-weight: 700; line-height: 1.1; margin-bottom: 4rem; display: block;">Curated Packages for <br><span class="heading-italic-green">Digital Distinction.</span></span>', unsafe_allow_html=True)
    st.markdown('</span>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        st.markdown('<span class="pricing-card-1-trigger" style="display:none;"></span>', unsafe_allow_html=True)
        st.markdown("""
            <span class="tier-label">Tier 01</span>
            <span class="pricing-card-title font-serif">Bronze</span>
            <span class="price-container"><span class="price-number">R309</span><span class="price-period">/mo</span></span>
            <span class="feature-box">
                <span class="feature-item"><span class="icon-circle"><i data-lucide="check" style="color: #064e3b;"></i></span><span class="feature-text">Bespoke 3-Page Build</span></span>
                <span class="feature-item"><span class="icon-circle"><i data-lucide="shield-check" style="color: #064e3b;"></i></span><span class="feature-text">Premium Managed Hosting</span></span>
                <span class="feature-item"><span class="icon-circle"><i data-lucide="clock" style="color: #064e3b;"></i></span><span class="feature-text">Monthly Concierge Hour</span></span>
            </span>
        """, unsafe_allow_html=True)
        if st.button("Apply for Bronze", key="btn_bronze"):
            st.toast("🥉 Bronze tier onboarding initiated.", icon="✨")
    with col2:
        st.markdown('<span class="pricing-card-2-trigger" style="display:none;"></span>', unsafe_allow_html=True)
        st.markdown("""
            <span class="recommended-badge">Recommended</span>
            <span class="tier-label">Tier 02</span>
            <span class="pricing-card-title-white font-serif">Silver</span>
            <span class="price-container"><span class="price-number-dark">R449</span><span class="price-period">/mo</span></span>
            <span class="feature-box">
                <span class="feature-item"><span class="icon-circle-dark"><i data-lucide="check" style="color: #c5a022;"></i></span><span class="feature-text feature-text-white">Expansive 6-Page Build</span></span>
                <span class="feature-item"><span class="icon-circle-dark"><i data-lucide="zap" style="color: #c5a022;"></i></span><span class="feature-text feature-text-white">Executive Priority Build</span></span>
                <span class="feature-item"><span class="icon-circle-gold"><i data-lucide="star" style="color: white;"></i></span><span class="feature-text-bold">VIP Support Line</span></span>
            </span>
        """, unsafe_allow_html=True)
        if st.button("Secure Silver", key="btn_silver"):
            st.toast("🥈 Silver tier priority access granted.", icon="✨")
    with col3:
        st.markdown('<span class="pricing-card-3-trigger" style="display:none;"></span>', unsafe_allow_html=True)
        st.markdown("""
            <span class="tier-label">Tier 03</span>
            <span class="pricing-card-title font-serif">Gold</span>
            <span class="price-container"><span class="price-number">R599</span><span class="price-period">/mo</span></span>
            <span class="feature-box">
                <span class="feature-item"><span class="icon-circle"><i data-lucide="check" style="color: #064e3b;"></i></span><span class="feature-text">Unlimited 12-Page Build</span></span>
                <span class="feature-item"><span class="icon-circle"><i data-lucide="shopping-bag" style="color: #064e3b;"></i></span><span class="feature-text">Commerce Integration</span></span>
                <span class="feature-item"><span class="icon-circle"><i data-lucide="award" style="color: #064e3b;"></i></span><span class="feature-text">Strategic Quarterly Review</span></span>
            </span>
        """, unsafe_allow_html=True)
        if st.button("Apply for Gold", key="btn_gold"):
            st.toast("🥇 Gold tier executive suite initiated.", icon="✨")

def render_pledge():
    col_left, col_right = st.columns([1, 1], gap="large")
    with col_left:
        st.markdown('<span class="pledge-left-trigger" style="display:none;"></span>', unsafe_allow_html=True)
        st.markdown('<span class="badge-span" style="border: 1px solid rgba(255,255,255,0.15) !important; background-color: rgba(6,78,59,0.05); color: var(--theme-gold);">The afridesign Standard</span>', unsafe_allow_html=True)
        st.markdown('<span class="font-serif" style="font-size: 2.8rem; font-weight: 700; line-height: 1.1; margin-bottom: 2rem; display: block;">Our Pledge of<br><span class="italic-gold">Absolute Quality.</span></span>', unsafe_allow_html=True)
        st.markdown("""
            <span style="display: flex; flex-direction: column; gap: 1.5rem;">
                <span class="pledge-row"><span class="pledge-icon-box"><i data-lucide="clock-3" style="color: #c5a022;"></i></span><span><span class="pledge-row-title">48-Hour Deployment</span><span class="pledge-row-desc">Elite execution. Your project goes live in days, or your first month is on us.</span></span></span>
                <span class="pledge-row"><span class="pledge-icon-box"><i data-lucide="heart" style="color: #c5a022;"></i></span><span><span class="pledge-row-title">The "Love It" Clause</span><span class="pledge-row-desc">If the initial aesthetic doesn't captivate you, we redesign until it does. No questions.</span></span></span>
                <span class="pledge-row"><span class="pledge-icon-box"><i data-lucide="zap" style="color: #c5a022;"></i></span><span><span class="pledge-row-title">Performance Benchmark</span><span class="pledge-row-desc">Every build is optimized. We guarantee a Google PageSpeed score of 80+.</span></span></span>
            </span>
        """, unsafe_allow_html=True)
    with col_right:
        st.markdown('<span class="pledge-right-trigger" style="display:none;"></span>', unsafe_allow_html=True)
        st.markdown("""
            <span class="gold-pulse-box"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-gem"><path d="M6 3h12l4 6-10 13L2 9Z"/><path d="M11 3 8 9l3 13 3-13-3-6Z"/><path d="M2 9h20"/></svg></span>
            <span class="font-serif" style="font-size: 1.8rem; font-weight: 700; font-style: italic; display: block; margin-bottom: 1rem; color: #0a0a0a;">Excellence by Default.</span>
            <span class="font-sans" style="font-size: 0.95rem; color: #6b7280; font-weight: 300; line-height: 1.5; margin-bottom: 2rem; display: block;">Join South Africa's most prestigious network of businesses powered by Afrihost managed technology. We don't just build sites; we manage digital legacies.</span>
        """, unsafe_allow_html=True)
        if st.button("Start Your Journey", key="btn_pledge_charter"):
            st.toast("🛡️ Quality standard registered. Welcome onboard.", icon="💎")

def render_stats():
    """Stats counters section."""
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

def render_testimonials():
    """Testimonials section."""
    st.markdown('<div class="testimonials-container">', unsafe_allow_html=True)
    st.markdown('<span class="badge-span" style="margin: 0 auto 2rem auto;">Client Voices</span>', unsafe_allow_html=True)
    st.markdown('<div class="roadmap-header" style="text-align: center;">Trusted by <span style="color:#064e3b">Industry Leaders</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="roadmap-subheader" style="text-align: center; margin: 0 auto 3rem auto;">What our clients say about the afridesign experience.</div>', unsafe_allow_html=True)
    
    testimonials = [
        {"quote": "The 48-hour deployment is not a gimmick. Our site was live, optimized, and converting within two days. Unmatched service.", "name": "Sarah Nkosi", "title": "Founder, Luxe Haven", "initial": "S"},
        {"quote": "Afridesign transformed our digital presence. The concierge support is genuinely responsive, and the quality is world-class.", "name": "James van der Merwe", "title": "CEO, Cape Analytics", "initial": "J"},
        {"quote": "From strategy to launch, every step was seamless. The ongoing care takes all the stress out of running a business website.", "name": "Thabo Molefe", "title": "Creative Director, Studio M", "initial": "T"},
        {"quote": "We've tried several agencies, but none offer the combination of design excellence and managed hosting like afridesign. Pure gold.", "name": "Priya Naidoo", "title": "Marketing Lead, Durban Digital", "initial": "P"}
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

def render_case_studies():
    """Case studies / portfolio section."""
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

def render_tech_stack():
    """Technology stack logos grid."""
    st.markdown('<div class="tech-container">', unsafe_allow_html=True)
    st.markdown('<span class="badge-span" style="margin: 0 auto 2rem auto;">Enterprise-Grade Tech</span>', unsafe_allow_html=True)
    st.markdown('<div class="roadmap-header" style="text-align: center;">Powered by <span style="color:#064e3b">World-Class Infrastructure</span></div>', unsafe_allow_html=True)
    
    techs = ["WordPress", "Shopify", "WooCommerce", "Stripe", "Cloudflare", "Google Analytics"]
    st.markdown('<div class="tech-grid">', unsafe_allow_html=True)
    for tech in techs:
        st.markdown(f'<div class="tech-item"><i data-lucide="check-circle" style="color: #c5a022; width: 2rem; height: 2rem; margin-bottom: 0.5rem;"></i><br><strong>{tech}</strong></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_contact_form():
    """Simple lead generation form."""
    st.markdown('<div class="contact-container">', unsafe_allow_html=True)
    st.markdown('<div class="contact-card">', unsafe_allow_html=True)
    st.markdown('<span class="badge-span" style="margin-bottom: 1rem;">Start a Conversation</span>', unsafe_allow_html=True)
    st.markdown('<div class="roadmap-header" style="font-size: 2.5rem;">Ready to Elevate<br><span style="color:#064e3b">Your Digital Presence?</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="roadmap-subheader" style="margin-bottom: 2rem;">Tell us about your vision, and we’ll respond within 24 hours.</div>', unsafe_allow_html=True)
    
    with st.form(key="contact_form"):
        name = st.text_input("Full Name", placeholder="Enter your name")
        email = st.text_input("Email Address", placeholder="you@company.com")
        project_type = st.selectbox("Project Type", ["Select one", "New Website", "Redesign", "E-commerce", "Managed Care"])
        budget = st.selectbox("Budget Range", ["Select one", "R5k - R10k", "R10k - R25k", "R25k - R50k", "R50k+"])
        submitted = st.form_submit_button("Send Inquiry")
        if submitted:
            if name and email and project_type != "Select one":
                st.toast(f"✨ Thank you {name}! A concierge will contact you shortly.", icon="💎")
            else:
                st.toast("⚠️ Please fill in all required fields.", icon="🔍")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_roadmap():
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
    st.markdown("""
        <div class="roadmap-quote">
            <div class="quote-text">"Excellence is not an act, but a habit."</div>
            <div class="quote-attribution">Powered by Afrihost Infrastructure</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_faqs():
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
    st.markdown('<span class="footer-trigger" style="display:none;"></span>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1.5])
    with col1:
        st.markdown("""
            <span class="footer-logo-text" style="color: white;">afri<span style="color: #c5a022;">design</span></span>
            <span class="footer-bio">Hand-crafting the digital future for South Africa's most ambitious brands. Bespoke design meets surgical precision.</span>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown('<span class="footer-heading">Collection</span>', unsafe_allow_html=True)
        st.markdown('<span class="footer-link-span">The Collection</span>', unsafe_allow_html=True)
        st.markdown('<span class="footer-link-span">Managed Care</span>', unsafe_allow_html=True)
        st.markdown('<span class="footer-link-span">Design Ethos</span>', unsafe_allow_html=True)
    with col3:
        st.markdown('<span class="footer-heading">Concierge</span>', unsafe_allow_html=True)
        st.markdown("""
            <span class="footer-contact-row"><i data-lucide="phone" style="color: #c5a022;"></i><span class="footer-link-span" style="margin-bottom: 0;">+27 11 612 7200</span></span>
            <span class="footer-contact-row"><i data-lucide="mail" style="color: #c5a022;"></i><span class="footer-link-span" style="margin-bottom: 0;">concierge@afridesign.za</span></span>
            <span class="footer-contact-row"><i data-lucide="map-pin" style="color: #c5a022;"></i><span class="footer-link-span" style="margin-bottom: 0;">Sandton, RSA</span></span>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown('<span class="footer-heading">Membership</span>', unsafe_allow_html=True)
        st.markdown('<span class="footer-bio" style="margin-bottom: 1.5rem;">Join our private list for quarterly availability updates.</span>', unsafe_allow_html=True)
        st.html('<span class="footer-newsletter-input" style="display:block;">')
        email = st.text_input("Email Address", placeholder="Enter your email...", label_visibility="collapsed")
        st.markdown('</span>', unsafe_allow_html=True)
        st.markdown('<span class="footer-newsletter-btn" style="margin-top: 0.75rem; display:block;">', unsafe_allow_html=True)
        if st.button("Join List", key="newsletter_submit_btn"):
            if email:
                st.toast("🛡️ Successfully added to our private elite database.", icon="✨")
            else:
                st.toast("⚠️ Please enter a valid email address.", icon="🔍")
        st.html('</span>')
    st.markdown("""
        <span class="footer-bottom-bar">
            <span class="copyright-text">© 2026 afridesign Managed Services. Pure Digital Joy.</span>
            <span class="status-pill"><span class="status-dot"></span><span class="copyright-text" style="color: #888888; font-size: 10px;">Accepting 2 Private Projects</span></span>
        </span>
    """, unsafe_allow_html=True)

def main():
    inject_master_styles()
    inject_lucide_renderer()
    render_header()
    render_hero()
    render_pricing()
    render_pledge()
    render_stats()
    render_testimonials()
    render_case_studies()
    render_tech_stack()
    render_contact_form()
    render_roadmap()
    render_faqs()
    render_footer()

if __name__ == "__main__":
    main()