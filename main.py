from tkinter import W
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Afrihost Premium | Elite Connectivity",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

brand_css = """
<style>
    /* Import Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    :root {
        --brand-green: #064e3b;
        --brand-gold: #d4af37;
        --brand-black: #111827;
        --brand-gray: #f3f4f6;
    }

    /* Hide standard Streamlit header/footer for a cleaner look */
    header {visibility: visible;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .stApp {
        background-color: white;
        font-family: 'Inter', sans-serif;
    }

    /* Custom Nav Bar */
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 5%;
        background: rgba(255, 255, 255, 0.95);
        border-bottom: 2px solid var(--brand-gold);
        position: sticky;
        top: 0;
        z-index: 999;
    }

    .logo-box {
        background: var(--brand-green);
        color: var(--brand-gold);
        padding: 5px 15px;
        border-radius: 8px;
        font-weight: 900;
        font-size: 24px;
        border: 1px solid var(--brand-gold);
    }

    /* Hero Section */
    .hero-block {
        background: linear-gradient(135deg, #064e3b 0%, #022c22 100%);
        padding: 100px 5%;
        color: white;
        border-radius: 0 0 50px 50px;
        text-align: center;
        margin-bottom: 50px;
        border-bottom: 5px solid var(--brand-gold);
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        line-height: 1.1;
    }

    .gold-text {
        color: var(--brand-gold);
    }

    /* Premium Product Cards */
    .product-card {
        background: white;
        padding: 2rem;
        border-radius: 24px;
        border: 1px solid #eee;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        text-align: center;
        height: 100%;
    }

    .product-card:hover {
        transform: translateY(-10px);
        border-color: var(--brand-gold);
        box-shadow: 0 20px 40px rgba(212, 175, 55, 0.15);
    }

    .price-tag {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--brand-green);
    }

    .cta-button {
        display: inline-block;
        background: var(--brand-gold);
        color: var(--brand-green);
        padding: 12px 30px;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 1rem;
        transition: 0.3s;
    }

    .cta-button:hover {
        background: var(--brand-black);
        color: white;
    }

</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""" 
st.markdown(brand_css, unsafe_allow_html=True)

with st.sidebar:
    st.title("Navigation")
    st.write("Navigate to the different sections of the website.")
    with st.expander("World"):
        #st.write("Navigate to the different sections of the website.")
        with st.expander("Africa"):
            #st.write("Navigate to the different sections of the website.")
            with st.expander("South Africa"):
                st.write("Provinces:")
                with st.expander("Gauteng"):
                    st.write("")
                with st.expander("North West"):
                    st.write("Departments:")
                    with st.expander("Arts,Culture, Sports & Recreation"):
                        st.write("Navigate to the different sections of the website.")
                    with st.expander("Cooperative Governance and Traditional Affairs"):
                        st.write("Districts:")
                        with st.expander("Bojanala Platinum District Municipality"):
                            st.write("Departments:")
                        with st.expander("Dr Kenneth Kaunda District Municipality"):
                            st.write("Departments:")
                        with st.expander("Dr Ruth Segomotsi Mompati District Municipality"):
                            st.write("Departments:")      
                        with st.expander("Ngaka Modiri Molema District Municipality "):
                            st.write("Departments:")
                    with st.expander("Public Works & Roads"):
                        st.write("Navigate to the different sections of the website.")

            with st.expander("Botswana"):
                st.write("")
                                
    with st.expander("More"):
        st.write("Navigate to the different sections of the website.")

st.markdown(f"""
    <div class="nav-container">
        <div style="display: flex; align-items: center;">
            <div class="logo-box">A</div>
            <span style="margin-left: 10px; font-weight: 800; color: var(--brand-green); font-size: 1.5rem;">ANGWA</span>
        </div>
        <div style="display: flex; gap: 25px; align-items: center; font-weight: 600; font-size: 0.9rem;">
            <a href="#" style="color: var(--brand-black); text-decoration: none;">FIBRE</a>
            <a href="#" style="color: var(--brand-black); text-decoration: none;">MOBILE</a>
            <a href="#" style="color: var(--brand-black); text-decoration: none;">HOSTING</a>
            <a href="#" style="color: var(--brand-gold); text-decoration: none; border: 2px solid var(--brand-gold); padding: 5px 20px; border-radius: 20px;">CLIENTZONE</a>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="hero-block">
        <p style="text-transform: uppercase; letter-spacing: 3px; font-weight: 700; color: #d4af37; margin-bottom: 20px;">The Gold Standard of Internet</p>
        <h1 class="hero-title">Elite Connectivity.<br><span class="gold-text">Unrivaled Performance.</span></h1>
        <p style="font-size: 1.2rem; opacity: 0.8; max-width: 700px; margin: 0 auto 40px auto;">
            Experience the internet as it was meant to be. Pure speed, dedicated support, and the premium reliability of South Africa's most decorated ISP.
        </p>
        <div style="display: flex; gap: 15px; justify-content: center;">
            <a href="#" class="cta-button">Check Availability</a>
            <a href="#" class="cta-button" style="background: transparent; color: white; border: 2px solid white;">View Packages</a>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; font-weight: 800; color: #111827; margin-bottom: 40px;'>Select Your Premium Experience</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="product-card">
            <i class="fas fa-bolt" style="font-size: 3rem; color: #d4af37; margin-bottom: 1.5rem;"></i>
            <h3 style="font-weight: 800; margin-bottom: 0.5rem;">PURE FIBRE</h3>
            <p style="color: #666; font-size: 0.9rem; margin-bottom: 1.5rem;">The ultimate home & business link. 100% Uncapped.</p>
            <div class="price-tag">R499<span style="font-size: 1rem; color: #999;">/pm</span></div>
            <ul style="text-align: left; list-style: none; padding: 0; margin: 1.5rem 0; font-size: 0.9rem; color: #444;">
                <li><i class="fas fa-check gold-text"></i> Low Latency Gaming</li>
                <li><i class="fas fa-check gold-text"></i> Wi-Fi 6 Router Included</li>
                <li><i class="fas fa-check gold-text"></i> Free Installation</li>
            </ul>
            <a href="#" class="cta-button" style="width: 100%;">Order Now</a>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="product-card" style="border: 2px solid #d4af37; position: relative;">
            <div style="position: absolute; top: -15px; left: 50%; transform: translateX(-50%); background: #d4af37; color: #064e3b; padding: 2px 15px; border-radius: 10px; font-size: 0.7rem; font-weight: 800;">MOST POPULAR</div>
            <i class="fas fa-tower-cell" style="font-size: 3rem; color: #d4af37; margin-bottom: 1.5rem;"></i>
            <h3 style="font-weight: 800; margin-bottom: 0.5rem;">FIXED LTE</h3>
            <p style="color: #666; font-size: 0.9rem; margin-bottom: 1.5rem;">Instant plug-and-play connectivity anywhere.</p>
            <div class="price-tag">R299<span style="font-size: 1rem; color: #999;">/pm</span></div>
            <ul style="text-align: left; list-style: none; padding: 0; margin: 1.5rem 0; font-size: 0.9rem; color: #444;">
                <li><i class="fas fa-check gold-text"></i> Nationwide 5G Ready</li>
                <li><i class="fas fa-check gold-text"></i> No Contracts</li>
                <li><i class="fas fa-check gold-text"></i> Next-Day Delivery</li>
            </ul>
            <a href="#" class="cta-button" style="width: 100%;">Get Started</a>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="product-card">
            <i class="fas fa-server" style="font-size: 3rem; color: #d4af37; margin-bottom: 1.5rem;"></i>
            <h3 style="font-weight: 800; margin-bottom: 0.5rem;">CLOUD HOSTING</h3>
            <p style="color: #666; font-size: 0.9rem; margin-bottom: 1.5rem;">Enterprise-grade security for your digital assets.</p>
            <div class="price-tag">R149<span style="font-size: 1rem; color: #999;">/pm</span></div>
            <ul style="text-align: left; list-style: none; padding: 0; margin: 1.5rem 0; font-size: 0.9rem; color: #444;">
                <li><i class="fas fa-check gold-text"></i> Free .co.za Domain</li>
                <li><i class="fas fa-check gold-text"></i> Daily Cloud Backups</li>
                <li><i class="fas fa-check gold-text"></i> SSL Certificate</li>
            </ul>
            <a href="#" class="cta-button" style="width: 100%;">Host Now</a>
        </div>
    """, unsafe_allow_html=True)

st.write("---")
st.markdown("<h3 style='color: var(--brand-green); font-weight: 800;'>Premium Network Status</h3>", unsafe_allow_html=True)
col_a, col_b = st.columns([2, 1])

with col_a:
    st.info("💡 **Network Intelligence:** Our global backbone is currently operating at **99.99%** efficiency. No major outages reported in the last 24 hours.")

with col_b:
    search_query = st.text_input("Check your area coverage", placeholder="Enter your suburb...")
    if search_query:
        st.success(f"Excellent! {search_query} is fully compatible with our **Gold Standard Fibre**.")

st.markdown(f"""
    <div style="background: var(--brand-black); color: white; padding: 60px 5% 20px 5%; margin-top: 100px; border-top: 4px solid var(--brand-gold);">
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 40px; margin-bottom: 40px;">
            <div>
                <div style="display: flex; align-items: center; margin-bottom: 20px;">
                    <div class="logo-box" style="font-size: 18px; padding: 2px 10px;">A</div>
                    <span style="margin-left: 10px; font-weight: 800; color: white;">AFRIHOST</span>
                </div>
                <p style="font-size: 0.8rem; color: #888; line-height: 1.6;">
                    South Africa's leading ISP, providing award-winning internet services since 1999.
                </p>
            </div>
            <div>
                <h4 style="color: var(--brand-gold); font-size: 0.9rem; margin-bottom: 20px;">SOLUTIONS</h4>
                <div style="display: flex; flex-direction: column; gap: 10px; font-size: 0.8rem; color: #ccc;">
                    <span>Pure Fibre</span>
                    <span>Fixed LTE</span>
                    <span>Mobile Data</span>
                    <span>AirMobile</span>
                </div>
            </div>
            <div>
                <h4 style="color: var(--brand-gold); font-size: 0.9rem; margin-bottom: 20px;">SUPPORT</h4>
                <div style="display: flex; flex-direction: column; gap: 10px; font-size: 0.8rem; color: #ccc;">
                    <span>Help Centre</span>
                    <span>Network Status</span>
                    <span>ClientZone</span>
                    <span>Contact Us</span>
                </div>
            </div>
            <div>
                <h4 style="color: var(--brand-gold); font-size: 0.9rem; margin-bottom: 20px;">STAY CONNECTED</h4>
                <div style="display: flex; gap: 15px; font-size: 1.2rem; color: var(--brand-gold);">
                    <i class="fab fa-facebook"></i>
                    <i class="fab fa-twitter"></i>
                    <i class="fab fa-instagram"></i>
                    <i class="fab fa-linkedin"></i>
                </div>
            </div>
        </div>
        <div style="border-top: 1px solid #333; pt-20px; text-align: center; font-size: 0.7rem; color: #666; padding-top: 20px;">
            © 2024 AFRIHOST (PTY) LTD. ALL RIGHTS RESERVED. THE GOLD STANDARD OF INTERNET.
        </div>
    </div>
""", unsafe_allow_html=True)