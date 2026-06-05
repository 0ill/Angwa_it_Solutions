import streamlit as st
import random
import time
import math
import json

# ==============================================================================
# 1. PAGE CONFIGURATION & SESSION STATE INITIALIZATION
# ==============================================================================
st.set_page_config(
    page_title="Premium AfriSuite | Managed Web Excellence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def init_session_state():
    """Ensure all core interactive states are initialized cleanly."""
    defaults = {
        "active_tab": "all",
        "selected_tier": "Signature",
        "billing_cycle": "Monthly",
        "extra_pages": 3,
        "seo_premium": True,
        "speed_opt": True,
        "brand_name": "Aura Wellness",
        "preview_theme": "cream",
        "is_deploying": False,
        "deployment_step": 0,
        "deployment_logs": [],
        "is_live": False,
        "include_logos": True,
        "include_booking_widget": False,
        "include_contact_form": True,
        "benchmarking_state": "idle",
        "client_site_url": "https://mysite.com",
        "client_platform": "WordPress",
        "client_est_speed": 3.8,
        "audit_progress": 0,
        "audit_logs": [],
        "custom_page_weight": 4.2,
        "selected_map_node": "cdn",
        "is_cdn_purging": False,
        "firewall_status": "Strict Guard Enabled",
        "db_backup_time": "11:00 AM Today",
        "active_heartbeat_node": "af-south-1",
        "rolling_latency": [12.0, 14.2, 11.5, 15.1, 13.0, 12.4, 14.1, 15.0, 12.2, 13.5, 11.1, 12.0, 13.4, 14.2, 12.0],
        "terminal_history": [
            {"type": "system", "text": "--- afriHost Managed Core SSH v4.0.2 ---"},
            {"type": "system", "text": "Type 'help' to list secure high-frequency infrastructure controls."}
        ],
        "terminal_input_value": "",
        "ai_prompt": "High-end organic spa retreat in Cape Town",
        "ai_response": None,
        "is_ai_loading": False,
        "active_ai_theme_custom": None,
        "hub_api_key": "afri_live_58c264a93f7e1d4b899a2c3d",
        "webhook_url": "https://api.yourdomain.com/webhooks",
        "selected_language": "javascript",
        "consultation_submitted": False,
        "sys_ping": 12,
        "active_conns": 482
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ==============================================================================
# 2. MASTER STYLING BLOCK (Strictly utilizing SPAN tags for layout styling)
# ==============================================================================
def inject_master_styles():
    """Overrides default Streamlit styles with elegant luxury assets and themes."""
    st.markdown("""
        <span style="display:none;">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,400;0,700;1,400;1,700&family=JetBrains+Mono:wght@400;700&display=swap');
                
                /* Layout Customizations */
                .stApp {
                    background-color: #faf9f2 !important;
                    font-family: 'Inter', sans-serif !important;
                }
                [data-testid="stHeader"] {
                    background: transparent !important;
                }
                .block-container {
                    padding-top: 1rem !important;
                    padding-bottom: 5rem !important;
                }
                
                /* Custom Premium Typography */
                h1, h2, h3, h4, h5, h6 {
                    font-family: 'Playfair Display', serif !important;
                    color: #064e3b !important;
                }
                
                /* Premium buttons override */
                div.stButton > button {
                    background-color: #064e3b !important;
                    color: #fdfcf0 !important;
                    font-weight: 700 !important;
                    border: 1px solid #127c62 !important;
                    border-radius: 12px !important;
                    text-transform: uppercase !important;
                    font-size: 11px !important;
                    letter-spacing: 0.12em !important;
                    padding: 0.75rem 1.5rem !important;
                    transition: all 0.3s ease !important;
                    box-shadow: 0 4px 10px rgba(6, 78, 59, 0.1) !important;
                }
                div.stButton > button:hover {
                    background-color: #043427 !important;
                    color: #ffffff !important;
                    transform: translateY(-2px) !important;
                    box-shadow: 0 6px 15px rgba(6, 78, 59, 0.2) !important;
                }
                
                /* Secondary or Custom Buttons */
                .ai-gen-btn div.stButton > button {
                    background-color: #c5a022 !important;
                    color: #0a0a0a !important;
                    border: 1px solid #ebd69c !important;
                }
                .ai-gen-btn div.stButton > button:hover {
                    background-color: #ebd69c !important;
                    color: #0a0a0a !important;
                }

                /* Override Form input backgrounds */
                input, select, textarea {
                    background-color: #ffffff !important;
                    border: 1px solid #ebd69c !important;
                    border-radius: 10px !important;
                    color: #1a1608 !important;
                }
                
                /* Live System Ticker Container styled with spans */
                .ticker-wrapper {
                    display: block;
                    background-color: #0a0a0a;
                    padding: 0.6rem 1.5rem;
                    border-bottom: 1px solid #1f1f1f;
                    margin-bottom: 1.5rem;
                }
            </style>
        </span>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. INTERACTIVE SYSTEM SIMULATORS (BACKGROUND THREADS)
# ==============================================================================
def update_telemetry_metrics():
    """Randomly shift system parameters dynamically to simulate an active cloud core."""
    st.session_state.sys_ping = max(8, min(18, st.session_state.sys_ping + random.choice([-1, 0, 1])))
    st.session_state.active_conns = max(450, min(520, st.session_state.active_conns + random.choice([-2, 0, 2])))
    
    # Update rolling latency
    node = st.session_state.active_heartbeat_node
    base_latency = 12.0
    if node == "eu-west-1":
        base_latency = 48.0
    elif node == "us-east-1":
        base_latency = 75.0
    elif node == "ap-southeast-1":
        base_latency = 112.0
        
    next_latency = list(st.session_state.rolling_latency[1:])
    variation = random.choice([-1.5, -0.5, 0.5, 1.5])
    new_val = max(base_latency - 5, min(base_latency + 8, st.session_state.rolling_latency[-1] + variation))
    next_latency.append(round(new_val, 1))
    st.session_state.rolling_latency = next_latency

update_telemetry_metrics()

# ==============================================================================
# 4. STRUCTURAL PRESET SCHEMAS & UTILITIES
# ==============================================================================
THEMES = {
    "cream": {
        "bg": "#fdfcf0",
        "text": "#1a1608",
        "border": "#ebd69c",
        "accent": "#c5a022",
        "cardBg": "#faf9eb",
        "previewHeader": "#f5f3df",
        "btnBg": "#064e3b",
        "btnText": "#fdfcf0"
    },
    "emerald": {
        "bg": "#064e3b",
        "text": "#fdfcf0",
        "border": "#127c62",
        "accent": "#d4af37",
        "cardBg": "#033427",
        "previewHeader": "#032e23",
        "btnBg": "#d4af37",
        "btnText": "#0f172a"
    },
    "obsidian": {
        "bg": "#0a0a0a",
        "text": "#f1f5f9",
        "border": "#27272a",
        "accent": "#e2b53c",
        "cardBg": "#121212",
        "previewHeader": "#1f1f1f",
        "btnBg": "#ffffff",
        "btnText": "#000000"
    },
    "amethyst": {
        "bg": "#1a0e2e",
        "text": "#fbf9fe",
        "border": "#512c96",
        "accent": "#d6a3fb",
        "cardBg": "#24133f",
        "previewHeader": "#1e0f35",
        "btnBg": "#d6a3fb",
        "btnText": "#1e0f35"
    },
    "aiCustom": {
        "bg": "#0f172a",
        "text": "#f8fafc",
        "border": "#38bdf8",
        "accent": "#38bdf8",
        "cardBg": "#1e293b",
        "previewHeader": "#1e293b",
        "btnBg": "#38bdf8",
        "btnText": "#0f172a"
    }
}

# Apply AI customized theme override dynamically
if st.session_state.active_ai_theme_custom:
    ai_theme = st.session_state.active_ai_theme_custom
    THEMES["aiCustom"] = {
        "bg": ai_theme.get("primaryBg", "#0f172a"),
        "text": ai_theme.get("textColor", "#f8fafc"),
        "border": ai_theme.get("accentColor", "#38bdf8"),
        "accent": ai_theme.get("accentColor", "#38bdf8"),
        "cardBg": ai_theme.get("secondaryBg", "#1e293b"),
        "previewHeader": ai_theme.get("secondaryBg", "#1e293b"),
        "btnBg": ai_theme.get("accentColor", "#38bdf8"),
        "btnText": ai_theme.get("primaryBg", "#0f172a")
    }

def calculate_pricing_details():
    base_price = 1200 if st.session_state.selected_tier == "Bespoke Single" else (2800 if st.session_state.selected_tier == "Signature" else 6500)
    hosting_price = 45 if st.session_state.selected_tier == "Bespoke Single" else (85 if st.session_state.selected_tier == "Signature" else 195)
    
    overage = st.session_state.extra_pages * 50
    seo_cost = 35 if st.session_state.seo_premium else 0
    speed_cost = 25 if st.session_state.speed_opt else 0
    
    actual_monthly = hosting_price + seo_cost + speed_cost
    if st.session_state.billing_cycle == "Annual":
        actual_monthly *= 0.8 # 20% Discount
        
    return {
        "setup_fee": base_price + overage,
        "monthly": actual_monthly,
        "annual_total": (base_price + overage) + (actual_monthly * 12)
    }

# ==============================================================================
# 5. MODULAR RENDERING MODULES (Complying with span tag rule)
# ==============================================================================
def render_live_ticker():
    """Renders the top black premium ticker with system telemetry."""
    ping = st.session_state.sys_ping
    conns = st.session_state.active_conns
    st.markdown(f"""
        <span class="ticker-wrapper">
            <span style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; font-family: 'JetBrains Mono', monospace; color: #a3a3a3; font-size: 11px;">
                <span style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="width: 8px; height: 8px; background-color: #10b981; border-radius: 50%; display: inline-block; box-shadow: 0 0 8px #10b981;"></span>
                    <span style="color: #ffffff; font-weight: 700; letter-spacing: 0.1em; font-size: 10px;">ALL SYSTEMS SECURE:</span>
                    <span>AWS Edge Nodes fully propagated globally</span>
                </span>
                <span style="display: flex; gap: 1.5rem; align-items: center; flex-wrap: wrap;">
                    <span>AWS Network Latency: <strong style="color: #c5a022;">{ping}ms</strong></span>
                    <span>Active Compute Cores: <strong style="color: #c5a022;">{conns}</strong></span>
                    <span style="border-left: 1px solid #3f3f46; height: 12px; display: inline-block;"></span>
                    <span style="color: #c5a022; font-weight: 700; letter-spacing: 0.05em;">ACCEPTING 2 COMMISSION WINDOWS</span>
                </span>
            </span>
        </span>
    """, unsafe_allow_html=True)

def render_navigation_header():
    """Main Header navigation with custom tabs using spans for branding."""
    st.markdown("""
        <span style="display: block; border-bottom: 1px solid #e5e5e0; padding: 1.25rem 2rem; margin-bottom: 2rem; background-color: rgba(250, 249, 242, 0.95);">
            <span style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                <span style="display: flex; align-items: center; gap: 0.75rem;">
                    <span style="width: 40px; height: 40px; background-color: #064e3b; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-family: serif; font-size: 20px; font-weight: bold; color: #fdfcf0; box-shadow: 0 4px 6px rgba(6,78,59,0.15);">💎</span>
                    <span style="display: block;">
                        <span style="font-family: 'Playfair Display', serif; font-size: 1.5rem; font-weight: 700; color: #064e3b; line-height: 1.1; display: block;">AFRISUITE</span>
                        <span style="font-size: 9px; font-weight: 800; letter-spacing: 0.25em; color: #c5a022; display: block; text-transform: uppercase;">Managed Digital Masterpieces</span>
                    </span>
                </span>
                <span style="display: flex; gap: 0.5rem; background-color: #e5e5db; padding: 4px; border-radius: 50px;">
                    <span style="display: inline-block;">
                        <!-- Custom Streamlit tab inputs are handled below -->
                    </span>
                </span>
            </span>
        </span>
    """, unsafe_allow_html=True)
    
    # Render Streamlit-styled navigation pill selectors
    tabs = ["Unified Suite", "afriDesign (Creative)", "afriHost (AWS Cloud)"]
    sel_idx = 0 if st.session_state.active_tab == "all" else (1 if st.session_state.active_tab == "design" else 2)
    selected_tab = st.segmented_control(
        "Navigation Focus",
        options=tabs,
        default=tabs[sel_idx],
        key="segmented_navigation_tabs",
        label_visibility="collapsed"
    )
    if selected_tab == "Unified Suite":
        st.session_state.active_tab = "all"
    elif selected_tab == "afriDesign (Creative)":
        st.session_state.active_tab = "design"
    else:
        st.session_state.active_tab = "host"

def render_hero_section():
    """Presents a dynamic luxury hero section custom-targeted to the tab state."""
    active = st.session_state.active_tab
    
    # Hero container using spans
    st.markdown("""
        <span style="display: block; padding: 3rem 0; text-align: center; max-width: 850px; margin: 0 auto; margin-bottom: 2rem;">
            <span style="display: inline-flex; align-items: center; gap: 0.5rem; background-color: rgba(197, 160, 34, 0.12); border: 1px solid rgba(197, 160, 34, 0.3); padding: 0.35rem 1rem; border-radius: 50px; color: #9c7d15; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 1.5rem;">
                ✦ The Absolute Pinnacle of Luxury Web Engineering
            </span>
        </span>
    """, unsafe_allow_html=True)
    
    if active == "all":
        st.markdown("""
            <span style="display:block; text-align:center;">
                <h1 style="font-size: clamp(2rem, 5vw, 3.5rem); margin: 0; line-height: 1.15; font-weight: 800;">
                    Forging elite digital monuments. <br>
                    <span style="font-family: serif; font-style: italic; color: #c5a022;">Managed. Automated. Flawless.</span>
                </h1>
                <p style="font-size: 1.1rem; color: #57534e; font-weight: 300; max-width: 700px; margin: 1.5rem auto; line-height: 1.6;">
                    Welcome to the combined synergy of <strong>afriDesign</strong> and <strong>afriHost</strong>. We sculpt gorgeous high-end website architectures, publish hand-tailored assets, and deploy them on bespoke isolated AWS infrastructure in-house. Pure Digital Joy.
                </p>
            </span>
        """, unsafe_allow_html=True)
    elif active == "design":
        st.markdown("""
            <span style="display:block; text-align:center;">
                <h1 style="font-size: clamp(2rem, 5vw, 3.5rem); margin: 0; line-height: 1.15; font-weight: 800;">
                    Creative excellence <br>
                    <span style="font-family: serif; font-style: italic; color: #c5a022;">without the compromises.</span>
                </h1>
                <p style="font-size: 1.1rem; color: #57534e; font-weight: 300; max-width: 700px; margin: 1.5rem auto; line-height: 1.6;">
                    Under <strong>afriDesign</strong>, we completely abandon bloated templates, Wordpress builders, and slow plugins. Your bespoke platform is constructed line-by-line, optimized to load instantly, convert, and represent absolute corporate prestige.
                </p>
            </span>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <span style="display:block; text-align:center;">
                <h1 style="font-size: clamp(2rem, 5vw, 3.5rem); margin: 0; line-height: 1.15; font-weight: 800;">
                    Hyper-performance <br>
                    <span style="font-family: serif; font-style: italic; color: #c5a022;">AWS hosting for digital pioneers.</span>
                </h1>
                <p style="font-size: 1.1rem; color: #57534e; font-weight: 300; max-width: 700px; margin: 1.5rem auto; line-height: 1.6;">
                    Welcome to <strong>afriHost</strong>. We isolate every premium layout inside dedicated hardware nodes, run daily automated backups, provision 22 edge caches globally, and guarantee optimal Core Web Vitals with flatline latency.
                </p>
            </span>
        """, unsafe_allow_html=True)

def render_performance_audit():
    """Lighthouse speed comparative simulator."""
    st.markdown("""
        <span style="display: block; margin-top: 4rem; margin-bottom: 2rem;">
            <span style="text-align: center; display: block; max-width: 700px; margin: 0 auto; margin-bottom: 3rem;">
                <span style="display: inline-flex; align-items: center; gap: 0.5rem; background-color: rgba(197,160,34,0.12); border: 1px solid rgba(197,160,34,0.3); padding: 0.35rem 1rem; border-radius: 50px; color: #9c7d15; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 1rem;">
                    ⚡ Interactive Optimization Engine
                </span>
                <h2 style="font-size: 2.25rem; font-weight: 700; margin: 0;">Benchmark your current site speed</h2>
                <p style="color: #6b7280; font-weight: 300; font-size: 14px; margin-top: 0.75rem;">
                    Traditional site builders introduce bloat that slows down your load times. Run our live comparative simulator to inspect what high-fidelity hand-coded Next.js can achieve for your conversion metrics.
                </p>
            </span>
        </span>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 7])
    
    with col1:
        st.markdown("""
            <span style="display: block; background-color: #ffffff; border: 1px solid #ebd69c; border-radius: 20px; padding: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
                <span style="font-family: serif; font-size: 1.2rem; font-weight: 700; color: #064e3b; display: block; border-bottom: 1px solid #f3f4f6; padding-bottom: 0.75rem; margin-bottom: 1.25rem;">
                    Configure Site Diagnostics
                </span>
            </span>
        """, unsafe_allow_html=True)
        
        url_input = st.text_input(
            "Current Domain URL", 
            value=st.session_state.client_site_url, 
            key="audit_domain_url_input"
        )
        st.session_state.client_site_url = url_input
        
        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            platform_select = st.selectbox(
                "Current Platform",
                ["WordPress", "Shopify", "Wix / Squarespace", "Custom React/NextJS"],
                index=["WordPress", "Shopify", "Wix / Squarespace", "Custom React/NextJS"].index(st.session_state.client_platform),
                key="audit_platform_select"
            )
            st.session_state.client_platform = platform_select
        with sub_col2:
            speed_input = st.number_input(
                "Estimated Load Speed (s)",
                min_value=0.5, max_value=15.0, value=st.session_state.client_est_speed, step=0.1,
                key="audit_speed_number_input"
            )
            st.session_state.client_est_speed = speed_input
            
        st.markdown('<span style="display:block; margin-top: 1.5rem;"></span>', unsafe_allow_html=True)
        
        trigger_audit = st.button("Run Diagnostics", key="trigger_speed_audit_btn")
        if trigger_audit:
            st.session_state.benchmarking_state = "running"
            st.session_state.audit_progress = 10
            st.session_state.audit_logs = [
                "Contacting client URL index endpoints...",
                "Evaluating framework asset payload overhead..."
            ]
            st.rerun()
            
    with col2:
        st.markdown("""
            <span style="display: block; background-color: #0c0c0c; border: 1px solid #27272a; border-radius: 20px; padding: 2rem; color: #ffffff; height: 100%;">
                <span style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1f1f1f; padding-bottom: 0.75rem; margin-bottom: 1.5rem;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; letter-spacing: 0.15em; color: #c5a022; font-weight: bold;">
                        Performance Diagnostic Core Output
                    </span>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #52525b;">Lighthouse-Engine 10.0</span>
                </span>
        """, unsafe_allow_html=True)
        
        # State: IDLE
        if st.session_state.benchmarking_state == "idle":
            st.markdown("""
                <span style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 3rem 0; gap: 1rem;">
                    <span style="font-size: 40px; display: block;">📊</span>
                    <span style="display: block;">
                        <span style="font-family: serif; font-size: 15px; font-weight: bold; color: #e4e4e7; display: block;">Diagnostics Awaiting Execution</span>
                        <span style="font-size: 11px; color: #a1a1aa; max-width: 380px; display: block; margin-top: 0.25rem; line-height: 1.5;">
                            Initiate the diagnostics engine on the left. The compiler will map loading times, SEO structure, Core Web Vitals, and projected user retention.
                        </span>
                    </span>
                </span>
            """, unsafe_allow_html=True)
            
        # State: RUNNING (Simulation)
        elif st.session_state.benchmarking_state == "running":
            progress = st.session_state.audit_progress
            st.markdown(f"""
                <span style="display: block; margin-bottom: 1rem;">
                    <span style="display: flex; justify-content: space-between; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #c5a022; margin-bottom: 0.5rem;">
                        <span>Scanning Client Endpoints...</span>
                        <span>{progress}%</span>
                    </span>
                </span>
            """, unsafe_allow_html=True)
            st.progress(progress / 100.0)
            
            log_block = "".join([f"<span style='display:block; margin-bottom:4px;'>&gt; {log}</span>" for log in st.session_state.audit_logs])
            st.markdown(f"""
                <span style="display: block; background-color: rgba(0,0,0,0.4); border: 1px solid #1f1f1f; padding: 1rem; border-radius: 12px; font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #10b981; height: 110px; overflow-y: auto; margin-top: 1rem;">
                    {log_block}
                </span>
            """, unsafe_allow_html=True)
            
            # Simulated increments
            time.sleep(0.5)
            if progress < 100:
                if progress == 10:
                    st.session_state.audit_progress = 30
                    st.session_state.audit_logs.append("Mapping Google Lighthouse performance matrices...")
                elif progress == 30:
                    st.session_state.audit_progress = 55
                    st.session_state.audit_logs.append("Estimating Server-Side Rendering (SSR) latency mismatch...")
                elif progress == 55:
                    st.session_state.audit_progress = 80
                    st.session_state.audit_logs.append("Identifying bloated media formats and unused script tags...")
                elif progress == 80:
                    st.session_state.audit_progress = 100
                    st.session_state.audit_logs.append("Audit fully completed. Analyzing afriSuite optimization ratios...")
                st.rerun()
            else:
                st.session_state.benchmarking_state = "completed"
                st.rerun()
                
        # State: COMPLETED
        elif st.session_state.benchmarking_state == "completed":
            client_score = max(10, min(95, int(100 - (st.session_state.client_est_speed * 15))))
            conv_boost = round(st.session_state.client_est_speed * 8.2, 1)
            
            # Triple visual gauges utilizing inline spans and SVG configurations
            g1_dash = int(213 - (213 * client_score / 100))
            g2_dash = int(213 - (213 * 99 / 100))
            
            st.markdown(f"""
                <span style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
                    <!-- Gauge 1 -->
                    <span style="background-color: rgba(255,255,255,0.03); border: 1px solid #1f1f1f; border-radius: 12px; padding: 1rem; text-align: center; display: block;">
                        <span style="font-size: 9px; font-weight: 700; text-transform: uppercase; color: #a1a1aa; display: block; margin-bottom: 0.5rem; font-family: 'JetBrains Mono', monospace;">Your Site ({st.session_state.client_platform})</span>
                        <span style="position: relative; width: 80px; height: 80px; display: inline-flex; align-items: center; justify-content: center;">
                            <svg width="80" height="80" viewBox="0 0 80 80" style="transform: rotate(-90deg);">
                                <circle cx="40" cy="40" r="34" stroke="#1f1f1f" stroke-width="4" fill="transparent" />
                                <circle cx="40" cy="40" r="34" stroke="#f43f5e" stroke-width="4" fill="transparent" stroke-dasharray="213" stroke-dashoffset="{g1_dash}" />
                            </svg>
                            <span style="position: absolute; font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: 700; color: #f43f5e;">{client_score}%</span>
                        </span>
                        <span style="font-size: 11px; font-weight: 700; color: #f43f5e; display: block; margin-top: 0.5rem; font-family: 'JetBrains Mono', monospace;">{st.session_state.client_est_speed}s load time</span>
                    </span>
                    
                    <!-- Gauge 2 -->
                    <span style="background-color: rgba(255,255,255,0.03); border: 1px solid rgba(197,160,34,0.3); border-radius: 12px; padding: 1rem; text-align: center; display: block;">
                        <span style="font-size: 9px; font-weight: 700; text-transform: uppercase; color: #c5a022; display: block; margin-bottom: 0.5rem; font-family: 'JetBrains Mono', monospace;">afriSuite Standard</span>
                        <span style="position: relative; width: 80px; height: 80px; display: inline-flex; align-items: center; justify-content: center;">
                            <svg width="80" height="80" viewBox="0 0 80 80" style="transform: rotate(-90deg);">
                                <circle cx="40" cy="40" r="34" stroke="#1f1f1f" stroke-width="4" fill="transparent" />
                                <circle cx="40" cy="40" r="34" stroke="#10b981" stroke-width="4" fill="transparent" stroke-dasharray="213" stroke-dashoffset="{g2_dash}" />
                            </svg>
                            <span style="position: absolute; font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: 700; color: #10b981;">99%</span>
                        </span>
                        <span style="font-size: 11px; font-weight: 700; color: #10b981; display: block; margin-top: 0.5rem; font-family: 'JetBrains Mono', monospace;">0.18s load time</span>
                    </span>
                    
                    <!-- Gauge 3 -->
                    <span style="background-color: rgba(255,255,255,0.03); border: 1px solid #1f1f1f; border-radius: 12px; padding: 1rem; text-align: center; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                        <span style="font-size: 9px; font-weight: 700; text-transform: uppercase; color: #a1a1aa; display: block; margin-bottom: 0.25rem; font-family: 'JetBrains Mono', monospace;">Est. Conversions</span>
                        <span style="font-family: serif; font-size: 24px; font-weight: bold; color: #c5a022; display: block;">+{conv_boost}%</span>
                        <span style="font-size: 9px; color: #71717a; display: block; margin-top: 0.25rem; line-height: 1.2;">Direct prediction based on bounce reductions</span>
                    </span>
                </span>
                
                <span style="display: block; background-color: #040404; padding: 0.75rem 1rem; border-radius: 10px; border: 1px solid #1f1f1f; font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #71717a; line-height: 1.5; margin-bottom: 1rem;">
                    <span style="color: #10b981; font-weight: bold; font-size: 12px; display: inline-block; margin-right: 0.5rem;">CO₂</span>
                    <span>ECO METRIC: Deploying onto isolated zero-carbon AWS Cape Town clusters reduces footprint from <strong style="color:#f43f5e;">1.84g</strong> down to <strong style="color:#10b981;">0.12g</strong> per view. Complete carbon offset included.</span>
                </span>
            """, unsafe_allow_html=True)
            
        st.markdown(f"""
                <span style="display: flex; justify-content: space-between; align-items: center; background-color: rgba(0,0,0,0.3); padding: 0.5rem 1rem; border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: 9px; color: #52525b;">
                    <span>TARGET: {st.session_state.client_site_url}</span>
                </span>
            """, unsafe_allow_html=True)
            
        st.markdown('<span style="display:block; margin-top: 0.5rem;"></span>', unsafe_allow_html=True)
        reset_audit = st.button("Reset Simulator", key="reset_speed_audit_btn")
        if reset_audit:
            st.session_state.benchmarking_state = "idle"
            st.rerun()
            
    st.markdown("""</span>""", unsafe_allow_html=True)

def render_payload_simulator():
    """Renders the custom page weight slider & bandwidth latency comparison."""
    st.markdown("""
        <span style="display: block; margin-top: 4rem; margin-bottom: 2rem;">
            <span style="text-align: center; display: block; max-width: 700px; margin: 0 auto; margin-bottom: 3rem;">
                <span style="display: inline-flex; align-items: center; gap: 0.5rem; background-color: rgba(6,78,59,0.08); border: 1px solid rgba(6,78,59,0.2); padding: 0.35rem 1rem; border-radius: 50px; color: #064e3b; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 1rem;">
                    🛰️ Bandwidth Delivery Optimization
                </span>
                <h2 style="font-size: 2.25rem; font-weight: 700; margin: 0;">Inspect Asset weight transfer metrics</h2>
                <p style="color: #6b7280; font-weight: 300; font-size: 14px; margin-top: 0.75rem;">
                    As assets scale, unoptimized video players and raw image resolutions completely saturate mobile web pathways. AfriSuite dynamic compilation automatically minifies assets. Drag the slider to observe transfer latencies.
                </p>
            </span>
        </span>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <span style="display: block; background-color: #ffffff; border: 1px solid #ebd69c; border-radius: 20px; padding: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.02); height: 100%;">
                <span style="font-family: serif; font-size: 1.2rem; font-weight: 700; color: #064e3b; display: block; border-bottom: 1px solid #f3f4f6; padding-bottom: 0.75rem; margin-bottom: 1.5rem;">
                    Configure Asset Footprint Weight
                </span>
        """, unsafe_allow_html=True)
        
        weight = st.slider(
            "Simulated Layout Weight (MB)",
            min_value=0.2, max_value=12.0, value=st.session_state.custom_page_weight, step=0.1,
            key="payload_weight_slider"
        )
        st.session_state.custom_page_weight = weight
        
        st.markdown(f"""
                <span style="display: flex; justify-content: space-between; font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #71717a; margin-top: 0.5rem;">
                    <span>0.2 MB (AfriSuite standard)</span>
                    <span>6.0 MB (Heavier Templates)</span>
                    <span>12.0 MB (Raw Unoptimized)</span>
                </span>
                <span style="display: block; background-color: #faf9f2; border: 1px solid #ebd69c; border-radius: 12px; padding: 1rem; margin-top: 2rem; font-size: 11px; color: #44403c; line-height: 1.5;">
                    <strong style="color: #064e3b;">💡 Optimization Metric:</strong> By removing heavy redundant Javascript libraries and serving WebP formats on-the-fly, afriSuite targets an initial payload build weight of exactly <strong>0.24 MB</strong>. Timeless performance.
                </span>
            </span>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <span style="display: block; background-color: #ffffff; border: 1px solid #ebd69c; border-radius: 20px; padding: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.02); height: 100%;">
                <span style="font-family: serif; font-size: 1.2rem; font-weight: 700; color: #064e3b; display: block; border-bottom: 1px solid #f3f4f6; padding-bottom: 0.75rem; margin-bottom: 1.5rem;">
                    Calculated Network Delivery Speed
                </span>
        """, unsafe_allow_html=True)
        
        # Speeds in Mbps: Fiber (100), 5G (40), 4G (10), 3G (1.2)
        speeds = [
            ("Ultra Fiber (100 Mbps)", 100, "#10b981"),
            ("Standard 5G (40 Mbps)", 40, "#14b8a6"),
            ("Standard 4G LTE (10 Mbps)", 10, "#f59e0b"),
            ("Slow 3G Network (1.2 Mbps)", 1.2, "#f43f5e")
        ]
        
        for name, speed_val, color_hex in speeds:
            sec_val = round((weight * 8) / speed_val, 2)
            st.markdown(f"""
                <span style="display: flex; justify-content: space-between; align-items: center; background-color: #faf9f2; border: 1px solid #ebd69c; padding: 0.75rem 1.25rem; border-radius: 12px; margin-bottom: 0.75rem; font-family: 'JetBrains Mono', monospace; font-size: 11px;">
                    <span style="display: flex; align-items: center; gap: 0.5rem; color: #1c1917;">
                        <span style="width: 8px; height: 8px; background-color: {color_hex}; border-radius: 50%; display: inline-block;"></span>
                        <strong>{name}</strong>
                    </span>
                    <span style="color: {color_hex}; font-weight: bold;">{sec_val}s load speed</span>
                </span>
            """, unsafe_allow_html=True)
            
        st.markdown("</span>", unsafe_allow_html=True)

def render_visual_sandbox():
    """Core interactive Visual customizer linked instantly with the mockup canvas."""
    st.markdown("""
        <span style="display: block; margin-top: 4rem; margin-bottom: 2rem;">
            <span style="text-align: center; display: block; max-width: 700px; margin: 0 auto; margin-bottom: 3rem;">
                <span style="display: inline-flex; align-items: center; gap: 0.5rem; background-color: rgba(6,78,59,0.08); border: 1px solid rgba(6,78,59,0.2); padding: 0.35rem 1rem; border-radius: 50px; color: #064e3b; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 1rem;">
                    🎨 Real-time Creative Proving Ground
                </span>
                <h2 style="font-size: 2.25rem; font-weight: 700; margin: 0;">See your brand in luxury design</h2>
                <p style="color: #6b7280; font-weight: 300; font-size: 14px; margin-top: 0.75rem;">
                    Modify interactive parameters, apply dynamic custom color presets generated by our Gemini strategic module, and preview compiled UI outputs before deploying to AWS edge systems.
                </p>
            </span>
        </span>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 7])
    
    with col1:
        st.markdown("""
            <span style="display: block; background-color: #ffffff; border: 1px solid #ebd69c; border-radius: 20px; padding: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.02); height: 100%;">
                <span style="font-family: serif; font-size: 1.2rem; font-weight: 700; color: #064e3b; display: block; border-bottom: 1px solid #f3f4f6; padding-bottom: 0.75rem; margin-bottom: 1.25rem;">
                    Configure Layout Variables
                </span>
        """, unsafe_allow_html=True)
        
        brand_name_input = st.text_input(
            "Your Brand Name", 
            value=st.session_state.brand_name, 
            key="sandbox_brand_name_input"
        )
        st.session_state.brand_name = brand_name_input
        
        # Palette Options
        palette_options = ["Lux Cream", "Royal Emerald", "Obsidian Dark", "Amethyst"]
        if st.session_state.active_ai_theme_custom:
            palette_options.append("AI Custom Palette")
            
        palette_choice = st.radio(
            "Select Luxury Preset Style",
            palette_options,
            index=palette_options.index("AI Custom Palette" if st.session_state.preview_theme == "aiCustom" else (
                "Lux Cream" if st.session_state.preview_theme == "cream" else (
                    "Royal Emerald" if st.session_state.preview_theme == "emerald" else (
                        "Obsidian Dark" if st.session_state.preview_theme == "obsidian" else "Amethyst"
                    )
                )
            )),
            key="sandbox_preset_theme_radio"
        )
        if palette_choice == "Lux Cream":
            st.session_state.preview_theme = "cream"
        elif palette_choice == "Royal Emerald":
            st.session_state.preview_theme = "emerald"
        elif palette_choice == "Obsidian Dark":
            st.session_state.preview_theme = "obsidian"
        elif palette_choice == "Amethyst":
            st.session_state.preview_theme = "amethyst"
        else:
            st.session_state.preview_theme = "aiCustom"
            
        # Component Assembler checkboxes
        st.markdown("""
            <span style="display:block; margin-top: 1.5rem; border-top: 1px solid #f3f4f6; padding-top: 1rem;">
                <span style="font-size: 10px; font-weight: 700; text-transform: uppercase; color: #71717a; letter-spacing: 0.1em; display:block; margin-bottom: 0.75rem;">
                    Modular Component Assembler
                </span>
            </span>
        """, unsafe_allow_html=True)
        
        st.session_state.include_logos = st.checkbox(
            "Bespoke Partner Scroller Overlay", 
            value=st.session_state.include_logos, 
            key="sandbox_include_logos_chk"
        )
        st.session_state.include_booking_widget = st.checkbox(
            "Interactive VIP Booking Card", 
            value=st.session_state.include_booking_widget, 
            key="sandbox_include_booking_chk"
        )
        st.session_state.include_contact_form = st.checkbox(
            "High-Net-Worth Capture Form", 
            value=st.session_state.include_contact_form, 
            key="sandbox_include_contact_chk"
        )
        
        # Trigger simulated deployment sequence
        st.markdown("""<span style="display:block; margin-top: 1.5rem; border-top: 1px solid #f3f4f6; padding-top: 1.5rem;"></span>""", unsafe_allow_html=True)
        
        deploy_active = st.session_state.is_deploying
        deploy_btn = st.button(
            "Provision Virtual Machine Cluster" if not deploy_active else "Deploying Instance...",
            disabled=deploy_active,
            key="sandbox_deploy_sequence_btn"
        )
        if deploy_btn:
            st.session_state.is_deploying = True
            st.session_state.is_live = False
            st.session_state.deployment_step = 1
            st.session_state.deployment_logs = ["Initializing secure connection to AWS Cape Town (af-south-1)..."]
            st.rerun()
            
        live_color = "#10b981" if st.session_state.is_live else "#e5e7eb"
        live_shadow = "0 0 10px #10b981" if st.session_state.is_live else "none"
        live_label = "● ONLINE (CDN PROPAGATED)" if st.session_state.is_live else "○ OFFLINE / CONFIGURING"
        
        st.markdown(f"""
                <span style="display: flex; justify-content: space-between; align-items: center; background-color: #faf9f2; border: 1px solid #ebd69c; padding: 0.75rem; border-radius: 12px; margin-top: 1rem; font-family: 'JetBrains Mono', monospace; font-size: 10px;">
                    <span style="color: #71717a;">CLOUD STATUS:</span>
                    <span style="color: {live_color}; font-weight: bold; text-shadow: {live_shadow};">{live_label}</span>
                </span>
            </span>
        """, unsafe_allow_html=True)
        
    with col2:
        # Style resolution dictionary
        theme = THEMES[st.session_state.preview_theme]
        
        # Visual Canvas Box using spans (full inline style mapping)
        st.markdown(f"""
            <span style="display: block; border: 2px solid {theme['border']}; background-color: {theme['bg']}; border-radius: 24px; padding: 2.5rem; color: {theme['text']}; min-height: 480px; position: relative; box-shadow: 0 10px 30px rgba(0,0,0,0.03);">
                <!-- Header Component -->
                <span style="display: flex; justify-content: space-between; align-items: center; background-color: {theme['previewHeader']}; border: 1px solid rgba(0,0,0,0.05); padding: 0.5rem 1rem; border-radius: 12px; font-size: 11px;">
                    <strong style="font-family: serif; font-size: 14px;">{st.session_state.brand_name}</strong>
                    <span style="display: flex; gap: 1rem; font-family: 'JetBrains Mono', monospace; opacity: 0.75; font-size: 9px;">
                        <span>EXCELLENCE</span>
                        <span>COMMISSIONS</span>
                    </span>
                    <span style="background-color: {theme['btnBg']}; color: {theme['btnText']}; padding: 0.25rem 0.75rem; border-radius: 50px; font-weight: bold; font-size: 9px; text-transform: uppercase;">Intake</span>
                </span>
                
                <!-- Main Body -->
                <span style="display: block; margin: 3rem 0; max-width: 480px;">
                    <span style="display: block; font-family: 'JetBrains Mono', monospace; font-size: 9px; text-transform: uppercase; color: {theme['accent']}; font-weight: bold; letter-spacing: 0.2em; margin-bottom: 0.75rem;">
                        🛡️ Tailored Performance Architecture
                    </span>
                    <h3 style="font-size: 2.25rem; color: {theme['text']} !important; margin: 0; line-height: 1.15; font-weight: 800; font-family: 'Playfair Display', serif;">
                        Bespoke web assets for <span style="text-decoration: underline; text-underline-offset: 6px;">{st.session_state.brand_name}</span>.
                    </h3>
                    <p style="font-size: 12px; font-weight: 300; opacity: 0.8; margin-top: 1rem; line-height: 1.6;">
                        Indulge in a premium high-speed layout custom-sculpted in our Cape Town engineering facility. Hosted purely on secure, dedicated AWS virtual machine hardware.
                    </p>
                </span>
        """, unsafe_allow_html=True)
        
        # Assembler components inside the preview canvas
        if st.session_state.include_logos:
            st.markdown(f"""
                <span style="display: flex; justify-content: space-between; align-items: center; background-color: rgba(255,255,255,0.08); border: 1px solid rgba(0,0,0,0.05); padding: 0.75rem 1rem; border-radius: 12px; margin-bottom: 1rem; font-size: 9px;">
                    <span style="font-family: 'JetBrains Mono', monospace; opacity: 0.6;">TRUSTED SECURE SYSTEMS:</span>
                    <span style="display: flex; gap: 1rem; font-weight: 800;">
                        <span>✦ CAPE CAPITAL</span>
                        <span>✦ STELLENBOSCH</span>
                    </span>
                </span>
            """, unsafe_allow_html=True)
            
        if st.session_state.include_booking_widget:
            st.markdown(f"""
                <span style="display: grid; grid-template-columns: 2fr 1fr; align-items: center; background-color: #ffffff; border: 1px solid rgba(0,0,0,0.08); padding: 1rem; border-radius: 12px; margin-bottom: 1rem; color: #1a1505; gap: 1rem;">
                    <span>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 8px; font-weight: 700; color: #c5a022; display: block; text-transform: uppercase;">SECURE ALLOCATIONS PANEL</span>
                        <span style="font-family: serif; font-size: 11px; font-weight: bold; display: block; margin-top: 2px;">Reserve Commission Slot</span>
                        <span style="font-size: 9px; opacity: 0.6; display: block; line-height: 1.2;">Exactly 2 configuration allocations remain for Q2.</span>
                    </span>
                    <span style="text-align: right;">
                        <span style="background-color: #064e3b; color: #ffffff; padding: 0.4rem 0.8rem; border-radius: 8px; font-size: 9px; font-weight: bold; text-transform: uppercase; display: inline-block;">Reserve</span>
                    </span>
                </span>
            """, unsafe_allow_html=True)
            
        if st.session_state.include_contact_form:
            st.markdown(f"""
                <span style="display: flex; justify-content: space-between; align-items: center; background-color: #121212; border: 1px solid rgba(255,255,255,0.1); padding: 0.75rem 1.25rem; border-radius: 12px; margin-bottom: 1rem; color: #ffffff;">
                    <span>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 8px; font-weight: 700; color: #c5a022; display: block; text-transform: uppercase;">CORRESPONDENCE</span>
                        <span style="font-size: 10px; font-weight: bold; display: block;">Private Intake Access</span>
                    </span>
                    <span style="display: flex; gap: 0.5rem; align-items: center;">
                        <span style="background-color: #1c1c1c; border: 1px solid #2d2d2d; padding: 4px 10px; border-radius: 6px; font-family: 'JetBrains Mono', monospace; font-size: 9px; color: #8a8a8a;">VIP@AFRISUITE.IO</span>
                    </span>
                </span>
            """, unsafe_allow_html=True)
            
        # Preview Footer
        st.markdown(f"""
                <span style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(0,0,0,0.08); padding-top: 1.25rem; margin-top: 2rem; font-size: 10px;">
                    <span style="font-family: 'JetBrains Mono', monospace; opacity: 0.6;">ESTABLISHED 2026</span>
                    <span style="background-color: {theme['accent']}20; border: 1px solid {theme['accent']}40; color: {theme['accent']}; padding: 0.25rem 0.75rem; border-radius: 50px; font-weight: bold; font-family: 'JetBrains Mono', monospace; font-size: 9px;">🚀 Latency: 0.18s</span>
                </span>
            </span>
        """, unsafe_allow_html=True)
        
        # Deploy logs display
        if st.session_state.deployment_step > 0:
            st.markdown("""
                <span style="display: block; margin-top: 1.5rem; background-color: #0c0c0c; border: 1px solid #27272a; border-radius: 16px; padding: 1.5rem; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #10b981; box-shadow: 0 4px 15px rgba(0,0,0,0.15);">
                    <span style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1f1f1f; padding-bottom: 0.5rem; margin-bottom: 1rem; color: #a1a1aa;">
                        <span>💻 AWS PROVISIONING TERMINAL</span>
                        <span>Server: af-south-1.aws</span>
                    </span>
            """, unsafe_allow_html=True)
            
            # Loop compile logging
            log_output = "".join([f"<span style='display:block; margin-bottom:4px;'>[{idx+1}] {log}</span>" for idx, log in enumerate(st.session_state.deployment_logs)])
            st.markdown(f"""
                <span style="display: block; max-height: 120px; overflow-y: auto;">
                    {log_output}
                </span>
            """, unsafe_allow_html=True)
            
            # Interactive Simulation Engine loop triggers
            if st.session_state.is_deploying:
                curr_step = st.session_state.deployment_step
                time.sleep(0.4)
                
                steps = [
                    "Spinning up virtual isolated AWS Compute Instances...",
                    "Syncing premium Next.js asset distribution pipelines...",
                    "Compiling Tailwind responsive styling tokens...",
                    "Injecting custom premium shield firewall systems...",
                    "Securing free automated wildcard SSL Certs...",
                    "Deploying edge nodes across 22 major server regions...",
                    "Deploy complete. Site fully propagated at edge endpoints!"
                ]
                if curr_step <= len(steps):
                    st.session_state.deployment_logs.append(steps[curr_step - 1])
                    st.session_state.deployment_step = curr_step + 1
                    if curr_step == len(steps):
                        st.session_state.is_deploying = False
                        st.session_state.is_live = True
                    st.rerun()
                    
            if st.session_state.is_live:
                st.markdown("""
                    <span style="display: block; text-align: center; border-top: 1px solid #1f1f1f; padding-top: 0.75rem; margin-top: 0.75rem; color: #c5a022; font-weight: bold; animation: pulse 2s infinite;">
                        ✔ AWS Core instances live. DNS Connected. Pure digital joy.
                    </span>
                """, unsafe_allow_html=True)
                
            st.markdown("</span>", unsafe_allow_html=True)

def render_aws_telemetry():
    """Renders the custom cluster map diagram with live svg latency monitor."""
    st.markdown("""
        <span style="display: block; margin-top: 4rem; margin-bottom: 2rem;">
            <span style="text-align: center; display: block; max-width: 700px; margin: 0 auto; margin-bottom: 3rem;">
                <span style="display: inline-flex; align-items: center; gap: 0.5rem; background-color: rgba(197,160,34,0.12); border: 1px solid rgba(197,160,34,0.3); padding: 0.35rem 1rem; border-radius: 50px; color: #9c7d15; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 1rem;">
                    🌐 Infrastructure Cloud Telemetry
                </span>
                <h2 style="font-size: 2.25rem; font-weight: 700; margin: 0; color: #064e3b;">AWS Dedicated Cluster Telemetry</h2>
                <p style="color: #6b7280; font-weight: 300; font-size: 14px; margin-top: 0.75rem;">
                    We bypass standard shared network nodes. Select cluster nodes below to analyze network states, configure DDoS firewalls, force DB backups, and monitor live SVG latency paths.
                </p>
            </span>
        </span>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([7, 5])
    
    with col1:
        st.markdown("""
            <span style="display: block; background-color: #0c0c0c; border: 1px solid #27272a; border-radius: 20px; padding: 2rem; color: #ffffff;">
                <span style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1f1f1f; padding-bottom: 0.75rem; margin-bottom: 1.5rem;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; color: #71717a; font-weight: bold;">
                        Interactive Topology Node Map
                    </span>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #10b981;">● 4 Virtual Clusters Operating</span>
                </span>
        """, unsafe_allow_html=True)
        
        # Clicking simulated buttons acts as nodes
        node_col1, node_col2, node_col3, node_col4 = st.columns(4)
        with node_col1:
            if st.button("🌐 1. CDN Edge", key="topol_cdn_btn"):
                st.session_state.selected_map_node = "cdn"
        with node_col2:
            if st.button("🛡️ 2. Secure WAF", key="topol_waf_btn"):
                st.session_state.selected_map_node = "waf"
        with node_col3:
            if st.button("💻 3. Isolated VM", key="topol_vm_btn"):
                st.session_state.selected_map_node = "vm"
        with node_col4:
            if st.button("🗄️ 4. Secure DB", key="topol_db_btn"):
                st.session_state.selected_map_node = "db"
                
        # SVG network connection diagram
        st.markdown("""
            <span style="display: block; margin: 1.5rem 0; text-align: center;">
                <svg width="100%" height="80" style="max-width: 500px; display: inline-block;">
                    <line x1="10%" y1="40" x2="35%" y2="40" stroke="#c5a022" stroke-width="2" stroke-dasharray="5,5" />
                    <line x1="37%" y1="40" x2="62%" y2="40" stroke="#c5a022" stroke-width="2" stroke-dasharray="5,5" />
                    <line x1="64%" y1="40" x2="90%" y2="40" stroke="#c5a022" stroke-width="2" stroke-dasharray="5,5" />
                    <circle cx="10%" cy="40" r="6" fill="#10b981" />
                    <circle cx="37%" cy="40" r="6" fill="#10b981" />
                    <circle cx="64%" cy="40" r="6" fill="#10b981" />
                    <circle cx="90%" cy="40" r="6" fill="#10b981" />
                </svg>
            </span>
        """, unsafe_allow_html=True)
        
        # Real-time SVG rolling latency heartbeat
        node_hb_col1, node_hb_col2 = st.columns([4, 6])
        with node_hb_col1:
            st.markdown("""
                <span style="display: block; margin-top: 0.5rem;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #a1a1aa; display:block; margin-bottom: 0.5rem; font-weight: bold; text-transform: uppercase;">
                        Telemetry Target Region:
                    </span>
                </span>
            """, unsafe_allow_html=True)
            region_choice = st.radio(
                "Telemetry Node Target Region",
                ["af-south-1 (Cape Town)", "eu-west-1 (Dublin)", "us-east-1 (Virginia)", "ap-southeast-1 (Singapore)"],
                index=["af-south-1", "eu-west-1", "us-east-1", "ap-southeast-1"].index(st.session_state.active_heartbeat_node),
                key="telemetry_region_target_radio",
                label_visibility="collapsed"
            )
            st.session_state.active_heartbeat_node = region_choice.split(" ")[0]
            
        with node_hb_col2:
            st.markdown("""
                <span style="display: block; margin-top: 0.5rem;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #a1a1aa; display:block; margin-bottom: 0.5rem; font-weight: bold; text-transform: uppercase;">
                        Dynamic Latency Waveform:
                    </span>
                </span>
            """, unsafe_allow_html=True)
            
            lat_points = st.session_state.rolling_latency
            svg_points = " ".join([f"{(idx * 20)},{int(60 - ((val / 150) * 50))}" for idx, val in enumerate(lat_points)])
            
            st.markdown(f"""
                <span style="display: block; background-color: #050505; border: 1px solid #1f1f1f; border-radius: 12px; padding: 0.5rem; position: relative; height: 75px; overflow: hidden;">
                    <svg width="100%" height="100%" style="position: absolute; inset:0;">
                        <polyline fill="none" stroke="#c5a022" stroke-width="2" points="{svg_points}" />
                        <line x1="0" y1="30" x2="350" y2="30" stroke="#1f1f1f" stroke-width="1" stroke-dasharray="3,3" />
                    </svg>
                    <span style="position: absolute; bottom: 4px; right: 8px; font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #ffffff;">
                        {lat_points[-1]} ms
                    </span>
                </span>
            """, unsafe_allow_html=True)
            
        st.markdown("</span>", unsafe_allow_html=True)
        
    with col2:
        node = st.session_state.selected_map_node
        st.markdown("""
            <span style="display: block; background-color: #0c0c0c; border: 1px solid #27272a; border-radius: 20px; padding: 2rem; color: #ffffff; height: 100%;">
        """, unsafe_allow_html=True)
        
        if node == "cdn":
            st.markdown("""
                <span style="display: block; margin-bottom: 1rem;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 9px; color: #c5a022; font-weight: bold; display: block; text-transform: uppercase;">Node: CloudFront Edge CDN</span>
                    <span style="font-family: serif; font-size: 1.25rem; font-weight: bold; display: block; margin-top: 2px;">Global Edge Caching System</span>
                </span>
                <p style="font-size: 12px; font-weight: 300; color: #a1a1aa; line-height: 1.5; margin-bottom: 1.5rem;">
                    Edge node caching routes layouts globally to minimize server trip latency metrics down to 12ms.
                </p>
                <span style="display: block; background-color: #121212; padding: 1rem; border-radius: 12px; border: 1px solid #1f1f1f; font-family: 'JetBrains Mono', monospace; font-size: 11px; margin-bottom: 1.5rem;">
                    <span style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                        <span style="color: #71717a;">Active Edge Hubs:</span>
                        <span>22 Online</span>
                    </span>
                    <span style="display: flex; justify-content: space-between;">
                        <span style="color: #71717a;">Edge Hit Efficiency:</span>
                        <span style="color: #10b981;">98.4% Hit Ratio</span>
                    </span>
                </span>
            """, unsafe_allow_html=True)
            
            purge_active = st.session_state.is_cdn_purging
            purge_btn = st.button("Purge Edge Caches", key="cdn_purge_action_btn")
            if purge_btn:
                st.session_state.is_cdn_purging = True
                st.rerun()
                
            if purge_active:
                time.sleep(0.8)
                st.session_state.is_cdn_purging = False
                st.toast("⚡ Caches successfully purged across global edge nodes.", icon="✔")
                st.rerun()
                
        elif node == "waf":
            st.markdown(f"""
                <span style="display: block; margin-bottom: 1rem;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 9px; color: #c5a022; font-weight: bold; display: block; text-transform: uppercase;">Node: AWS Web Application Shield</span>
                    <span style="font-family: serif; font-size: 1.25rem; font-weight: bold; display: block; margin-top: 2px;">Web Application Shielding</span>
                </span>
                <p style="font-size: 12px; font-weight: 300; color: #a1a1aa; line-height: 1.5; margin-bottom: 1.5rem;">
                    Deflects Layer-7 security attacks, SQL exploits, and DDoS vectors natively at edge levels without bloating backend computation.
                </p>
                <span style="display: block; background-color: #121212; padding: 1rem; border-radius: 12px; border: 1px solid #1f1f1f; font-family: 'JetBrains Mono', monospace; font-size: 11px; margin-bottom: 1.5rem;">
                    <span style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                        <span style="color: #71717a;">Shield Status:</span>
                        <span style="color: #10b981;">{st.session_state.firewall_status}</span>
                    </span>
                    <span style="display: flex; justify-content: space-between;">
                        <span style="color: #71717a;">Firewall Protocol:</span>
                        <span>SHA-256 HSTS</span>
                    </span>
                </span>
            """, unsafe_allow_html=True)
            
            st.markdown("<span style='font-family: \"JetBrains Mono\", monospace; font-size: 10px; color:#71717a; display:block; margin-bottom:4px;'>Select Shield Level:</span>", unsafe_allow_html=True)
            waf_sel = st.segmented_control(
                "Shield Level Selector",
                ["Strict Shield Active", "Hyper DDoS Mitigation"],
                default=st.session_state.firewall_status,
                key="telemetry_waf_selector_btn"
            )
            if waf_sel:
                st.session_state.firewall_status = waf_sel
                st.toast(f"🔒 Shield rules updated to: {waf_sel}", icon="🛡️")
                
        elif node == "vm":
            st.markdown("""
                <span style="display: block; margin-bottom: 1rem;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 9px; color: #c5a022; font-weight: bold; display: block; text-transform: uppercase;">Node: AWS EC2 Core</span>
                    <span style="font-family: serif; font-size: 1.25rem; font-weight: bold; display: block; margin-top: 2px;">Isolated Layout Environments</span>
                </span>
                <p style="font-size: 12px; font-weight: 300; color: #a1a1aa; line-height: 1.5; margin-bottom: 1.5rem;">
                    Client platforms operate entirely inside dedicated, secured micro-VM slices to prevent database leaks or script interference.
                </p>
                <span style="display: block; background-color: #121212; padding: 1rem; border-radius: 12px; border: 1px solid #1f1f1f; font-family: 'JetBrains Mono', monospace; font-size: 11px; margin-bottom: 1.5rem;">
                    <span style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                        <span style="color: #71717a;">Hardware Core:</span>
                        <span>v4 Dedicated VM CPU</span>
                    </span>
                    <span style="display: flex; justify-content: space-between;">
                        <span style="color: #71717a;">Build Version:</span>
                        <span>NextJS v15 ISR Engine</span>
                    </span>
                </span>
            """, unsafe_allow_html=True)
            st.markdown("""
                <span style="display: block; text-align: center; border: 1px dashed #3f3f46; padding: 1rem; border-radius: 10px; font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #71717a;">
                    Use secure SSH Administrative Console below to manage VM.
                </span>
            """, unsafe_allow_html=True)
            
        elif node == "db":
            st.markdown(f"""
                <span style="display: block; margin-bottom: 1rem;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 9px; color: #c5a022; font-weight: bold; display: block; text-transform: uppercase;">Node: PostgreSQL database</span>
                    <span style="font-family: serif; font-size: 1.25rem; font-weight: bold; display: block; margin-top: 2px;">Secured Transactional Logs</span>
                </span>
                <p style="font-size: 12px; font-weight: 300; color: #a1a1aa; line-height: 1.5; margin-bottom: 1.5rem;">
                    Store contact form inputs, private transactional endpoints, and catalog parameters safely using premium database configurations.
                </p>
                <span style="display: block; background-color: #121212; padding: 1rem; border-radius: 12px; border: 1px solid #1f1f1f; font-family: 'JetBrains Mono', monospace; font-size: 11px; margin-bottom: 1.5rem;">
                    <span style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                        <span style="color: #71717a;">Last Database Backup:</span>
                        <span>{st.session_state.db_backup_time}</span>
                    </span>
                    <span style="display: flex; justify-content: space-between;">
                        <span style="color: #71717a;">Encryption Protocol:</span>
                        <span style="color: #10b981;">AES-256 Enabled</span>
                    </span>
                </span>
            """, unsafe_allow_html=True)
            
            force_backup = st.button("Force Database Backup", key="db_force_backup_btn")
            if force_backup:
                st.session_state.db_backup_time = time.strftime("%I:%M:%S %p Today")
                st.toast("💾 Database snapshot saved successfully.", icon="💾")
                st.rerun()
                
        st.markdown("""
                <span style="display: flex; justify-content: space-between; align-items: center; background-color: rgba(0,0,0,0.3); padding: 0.5rem 1rem; border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: 9px; color: #52525b;">
                    <span>AWS DIAGNOSTICS:</span>
                    <span style="color: #10b981; font-weight: bold;">100% HEALTHY</span>
                </span>
            </span>
        """, unsafe_allow_html=True)

def render_terminal_console():
    """Renders the administrative secure SSH console."""
    st.markdown("""
        <span style="display: block; margin-top: 4rem; margin-bottom: 2rem;">
            <span style="text-align: center; display: block; max-width: 700px; margin: 0 auto; margin-bottom: 2rem;">
                <span style="display: inline-flex; align-items: center; gap: 0.5rem; background-color: rgba(6,78,59,0.08); border: 1px solid rgba(6,78,59,0.2); padding: 0.35rem 1rem; border-radius: 50px; color: #064e3b; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 1rem;">
                    🔒 Administrator Command Interface
                </span>
                <h2 style="font-size: 2.25rem; font-weight: 700; margin: 0; color: #064e3b;">The AWS Core SSH Console</h2>
                <p style="color: #6b7280; font-weight: 300; font-size: 14px; margin-top: 0.75rem;">
                    Execute hardware-level diagnostic scripts directly from your client window. Type <strong style="color:#064e3b;">help</strong> inside the input terminal command line below.
                </p>
            </span>
        </span>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <span style="display: block; max-width: 800px; margin: 0 auto; background-color: #000000; border: 1px solid #27272a; border-radius: 16px; padding: 1.5rem; font-family: 'JetBrains Mono', monospace; font-size: 11px; box-shadow: 0 10px 30px rgba(0,0,0,0.15);">
            <span style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1f1f1f; padding-bottom: 0.5rem; margin-bottom: 1rem; color: #71717a; font-size: 10px;">
                <span>🔒 afriHost.secure-core.ssh</span>
                <span>Client Endpoint: af-south-1</span>
            </span>
            
            <span style="display: block; height: 180px; overflow-y: auto; color: #d4d4d8; margin-bottom: 1rem; scroll-behavior: smooth;">
    """, unsafe_allow_html=True)
    
    # Loop display of shell logs
    for log_item in st.session_state.terminal_history:
        color = "#c5a022" if log_item["type"] == "input" else ("#71717a" if log_item["type"] == "system" else "#e4e4e7")
        st.markdown(f'<span style="display:block; margin-bottom:4px; color:{color};">{log_item["text"]}</span>', unsafe_allow_html=True)
        
    st.markdown("""
            </span>
            <span style="display: block; border-top: 1px solid #1f1f1f; padding-top: 0.75rem;">
                <!-- Commands are handled natively in Streamlit -->
            </span>
        </span>
    """, unsafe_allow_html=True)
    
    # Form input layout for Terminal
    with st.form("ssh_console_form", clear_on_submit=True):
        st_cmd = st.text_input("Enter command:", value="", placeholder="Type 'help' and press Submit...", key="terminal_text_field_input")
        sub_btn = st.form_submit_button("Submit Command")
        
        if sub_btn and st_cmd.strip():
            user_cmd = st_cmd.strip().lower()
            st.session_state.terminal_history.append({"type": "input", "text": f"$ {st_cmd}"})
            
            if user_cmd == "help":
                st.session_state.terminal_history.append({"type": "output", "text": "Secure AWS Core commands:"})
                st.session_state.terminal_history.append({"type": "output", "text": "  - status       : Queries CPU, network states & uptime matrices"})
                st.session_state.terminal_history.append({"type": "output", "text": "  - ping         : Performs diagnostic round-trip latency checks"})
                st.session_state.terminal_history.append({"type": "output", "text": "  - flush-cdn    : Evaporates active caches globally"})
                st.session_state.terminal_history.append({"type": "output", "text": "  - harden       : Forces cryptographic SSL configuration cycles"})
                st.session_state.terminal_history.append({"type": "output", "text": "  - logs         : Displays historical isolated VM logs"})
                st.session_state.terminal_history.append({"type": "output", "text": "  - clear        : Wipes secure terminal display logs"})
            elif user_cmd == "status":
                st.session_state.terminal_history.append({"type": "output", "text": "NODE: af-south-1.aws-instance-01.local"})
                st.session_state.terminal_history.append({"type": "output", "text": f"UPTIME: 99.998% | LATENCY: {st.session_state.sys_ping}ms"})
                st.session_state.terminal_history.append({"type": "output", "text": "SSL STATUS: Valid, Auto-Renewing Wildcard [SHA-256]"})
                st.session_state.terminal_history.append({"type": "output", "text": "FIREWALL: Active (99.8% DDoS shield protection)"})
            elif user_cmd == "ping":
                st.session_state.terminal_history.append({"type": "output", "text": f"64 bytes from af-south-1: icmp_seq=1 ttl=64 time={st.session_state.sys_ping}ms"})
                st.session_state.terminal_history.append({"type": "output", "text": f"64 bytes from af-south-1: icmp_seq=2 ttl=64 time={st.session_state.sys_ping - 1}ms"})
                st.session_state.terminal_history.append({"type": "output", "text": "Diagnostic ping benchmark complete."})
            elif user_cmd == "flush-cdn":
                st.session_state.terminal_history.append({"type": "output", "text": "Flushing global CloudFront Edge Cache Nodes [22 Cities]..."})
                st.session_state.terminal_history.append({"type": "output", "text": "Flushed 3.42 GB cached objects. Rebuilding assets index..."})
                st.session_state.terminal_history.append({"type": "output", "text": "Edge Nodes fully propagated with fresh code layouts."})
            elif user_cmd == "harden":
                st.session_state.terminal_history.append({"type": "output", "text": "Enforcing strict HTTP-Strict-Transport-Security [HSTS]..."})
                st.session_state.terminal_history.append({"type": "output", "text": "Regenerating secure ephemeral elliptic curves..."})
                st.session_state.terminal_history.append({"type": "output", "text": "Security hardening successfully finalized."})
            elif user_cmd == "logs":
                st.session_state.terminal_history.append({"type": "output", "text": "VM Boot initialized at 2026-05-18 08:00:22 UTC"})
                st.session_state.terminal_history.append({"type": "output", "text": "NextJS Static ISR compiled in 1.48s"})
                st.session_state.terminal_history.append({"type": "output", "text": "System status - 0 errors, 0 security warnings"})
            elif user_cmd == "clear":
                st.session_state.terminal_history = []
            else:
                st.session_state.terminal_history.append({"type": "output", "text": f"Command not recognized: '{user_cmd}'. Type 'help' for options."})
            st.rerun()

def render_api_simulator():
    """Renders custom webhook endpoints and copyable boilerplate outputs."""
    st.markdown("""
        <span style="display: block; margin-top: 4rem; margin-bottom: 2rem;">
            <span style="text-align: center; display: block; max-width: 700px; margin: 0 auto; margin-bottom: 3rem;">
                <span style="display: inline-flex; align-items: center; gap: 0.5rem; background-color: rgba(6,78,59,0.08); border: 1px solid rgba(6,78,59,0.2); padding: 0.35rem 1rem; border-radius: 50px; color: #064e3b; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 1rem;">
                    🔌 Cloud API Gateway
                </span>
                <h2 style="font-size: 2.25rem; font-weight: 700; margin: 0; color: #064e3b;">Interactive Webhook Simulator</h2>
                <p style="color: #6b7280; font-weight: 300; font-size: 14px; margin-top: 0.75rem;">
                    Seamlessly incorporate afriSuite assets natively into existing build pipelines. Generate custom integration configurations below.
                </p>
            </span>
        </span>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 7])
    
    with col1:
        st.markdown("""
            <span style="display: block; background-color: #ffffff; border: 1px solid #ebd69c; border-radius: 20px; padding: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.02); height: 100%;">
                <span style="font-family: serif; font-size: 1.2rem; font-weight: 700; color: #064e3b; display: block; border-bottom: 1px solid #f3f4f6; padding-bottom: 0.75rem; margin-bottom: 1.25rem;">
                    Credentials Configuration
                </span>
        """, unsafe_allow_html=True)
        
        # Display simulated key
        st.text_input("Live Access Token", value=st.session_state.hub_api_key, disabled=True, key="api_token_read_only")
        
        # Input custom webhook URL
        st.session_state.webhook_url = st.text_input(
            "Webhook Payload Destination",
            value=st.session_state.webhook_url,
            key="api_webhook_url_input_field"
        )
        
        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            regen_btn = st.button("Regen Token", key="api_regen_token_btn")
            if regen_btn:
                st.session_state.hub_api_key = f"afri_live_{random.randint(10000000, 99999999)}c{random.randint(100000, 999999)}a"
                st.rerun()
        with sub_col2:
            save_btn = st.button("Save Webhooks", key="api_save_webhooks_btn")
            if save_btn:
                st.toast("✔ Configuration successfully synced to active secure cluster variables.", icon="✔")
                
        st.markdown("</span>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <span style="display: block; background-color: #0c0c0c; border: 1px solid #27272a; border-radius: 20px; padding: 2rem; color: #ffffff; height: 100%;">
                <span style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1f1f1f; padding-bottom: 0.75rem; margin-bottom: 1.5rem;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; color: #c5a022; font-weight: bold;">
                        Instantiated SDK Boilerplate
                    </span>
                </span>
        """, unsafe_allow_html=True)
        
        lang = st.segmented_control(
            "SDK Programming Language",
            ["NodeJS", "Python"],
            default="NodeJS",
            key="api_sdk_lang_selector_pill"
        )
        st.session_state.selected_language = "javascript" if lang == "NodeJS" else "python"
        
        # Code compilation based on state parameters
        if st.session_state.selected_language == "javascript":
            sdk_code = f"""// Instantiate afriSuite Client Router
const afriSuite = require('@afrisuite/sdk')('{st.session_state.hub_api_key}');

async function routeSecureCommission() {{
  const transaction = await afriSuite.deployments.create({{
    brand: "{st.session_state.brand_name}",
    niche: "{st.session_state.ai_prompt}",
    options: {{
      seoBoost: {str(st.session_state.seo_premium).lower()},
      extremeSpeed: {str(st.session_state.speed_opt).lower()},
      baseTier: "{st.session_state.selected_tier}"
    }}
  }});

  console.log(`[AWS-Core] Secure Node Propagated at: ${{transaction.cdnUrl}}`);
}}

routeSecureCommission();"""
        else:
            sdk_code = f"""# Instantiate afriSuite Python SDK Client
import afrisuite

client = afrisuite.Client(api_key="{st.session_state.hub_api_key}")

response = client.deployments.create(
    brand="{st.session_state.brand_name}",
    niche="{st.session_state.ai_prompt}",
    options={{
        "seo_boost": {st.session_state.seo_premium},
        "extreme_speed": {st.session_state.speed_opt},
        "base_tier": "{st.session_state.selected_tier}"
    }}
)

print(f"[AWS-Core] Node Active: {{response.cdn_url}}")"""
            
        st.code(sdk_code, language="javascript" if st.session_state.selected_language == "javascript" else "python")
        
        st.markdown("""
                <span style="display: flex; justify-content: space-between; align-items: center; background-color: rgba(0,0,0,0.3); padding: 0.5rem 1rem; border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: 9px; color: #52525b;">
                    <span>STATUS: SDK CONFIGURED</span>
                    <span style="color:#10b981;">READY FOR BUILD COMPILATION</span>
                </span>
            </span>
        """, unsafe_allow_html=True)

def render_ai_brand_strategist():
    """Dynamic brand palette styling engine powered by AI."""
    st.markdown("""
        <span style="display: block; margin-top: 4rem; margin-bottom: 2rem;">
            <span style="text-align: center; display: block; max-width: 700px; margin: 0 auto; margin-bottom: 3rem;">
                <span style="display: inline-flex; align-items: center; gap: 0.5rem; background-color: rgba(197,160,34,0.12); border: 1px solid rgba(197,160,34,0.3); padding: 0.35rem 1rem; border-radius: 50px; color: #9c7d15; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 1rem;">
                    ✨ Gemini 2.5 Flash Engine Active
                </span>
                <h2 style="font-size: 2.25rem; font-weight: 700; margin: 0; color: #064e3b;">AI Brand Stylist & Digital Strategy Copilot</h2>
                <p style="color: #6b7280; font-weight: 300; font-size: 14px; margin-top: 0.75rem;">
                    Describe your target business niche below. We will custom craft an elegant tagline, landing copy matrices, and a bespoke luxury HEX palette which can be dynamically applied to the Visual Sandbox with one click.
                </p>
            </span>
        </span>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 7])
    
    with col1:
        st.markdown("""
            <span style="display: block; background-color: #0c0c0c; border: 1px solid #27272a; border-radius: 20px; padding: 2rem; color: #ffffff; height: 100%;">
                <span style="font-family: serif; font-size: 1.2rem; font-weight: 700; color: #c5a022; display: block; border-bottom: 1px solid #1f1f1f; padding-bottom: 0.75rem; margin-bottom: 1.25rem;">
                    Input Brand Parameter
                </span>
        """, unsafe_allow_html=True)
        
        st.session_state.ai_prompt = st.text_area(
            "Define Business Niche & Esthetic Vibe",
            value=st.session_state.ai_prompt,
            key="ai_copilot_prompt_text_area",
            height=120
        )
        
        st.markdown('<span style="display:block; margin-top: 1rem;"></span>', unsafe_allow_html=True)
        
        st.markdown('<span class="ai-gen-btn">', unsafe_allow_html=True)
        trigger_ai = st.button("Synthesize Strategy", key="ai_copilot_run_btn")
        st.markdown('</span>', unsafe_allow_html=True)
        
        if trigger_ai:
            st.session_state.is_ai_loading = True
            st.rerun()
            
        if st.session_state.is_ai_loading:
            time.sleep(1.2) # Simulated computation
            
            # Simulated schema output
            st.session_state.ai_response = {
                "brandSlogan": f"Timeless Botanical Harmony by {st.session_state.brand_name}",
                "heroHeadline": "Forging Exquisite Mineral Structures",
                "luxuryColorDescription": "An elite botanical palette pairing mineral obsidian depths with crushed golden sand and eucalyptus accents, optimized strictly for high-end monitors.",
                "hexPalette": {
                    "primaryBg": "#1e1b4b",
                    "textColor": "#e0e7ff",
                    "accentColor": "#fcd34d",
                    "secondaryBg": "#312e81"
                },
                "sectionsCopy": [
                    {"title": "I. Architectural Purity", "body": "Custom compiled layout engines run with surgical precision, eliminating third-party dependencies."},
                    {"title": "II. Absolute Compute Isolation", "body": "Your assets operate within restricted, hardware-secured virtual cloud containers."},
                    {"title": "III. Timeless Elegance", "body": "Meticulously designed elements constructed dynamically to capture modern corporate authority."}
                ]
            }
            st.session_state.active_ai_theme_custom = st.session_state.ai_response["hexPalette"]
            st.session_state.is_ai_loading = False
            st.toast("🎨 Strategy blocks compiled. Dynamic theme ready to inject.", icon="✨")
            st.rerun()
            
        st.markdown("</span>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <span style="display: block; background-color: #0c0c0c; border: 1px solid #27272a; border-radius: 20px; padding: 2rem; color: #ffffff; height: 100%;">
                <span style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1f1f1f; padding-bottom: 0.75rem; margin-bottom: 1.5rem;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; color: #c5a022; font-weight: bold;">
                        Interactive Copilot Output
                    </span>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #52525b;">GEMINI-COPILOT v2.5</span>
                </span>
        """, unsafe_allow_html=True)
        
        if not st.session_state.ai_response:
            st.markdown("""
                <span style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 4rem 0; gap: 1rem;">
                    <span style="font-size: 40px; display: block;">✨</span>
                    <span style="display: block;">
                        <span style="font-family: serif; font-size: 15px; font-weight: bold; color: #e4e4e7; display: block;">Awaiting Custom parameters</span>
                        <span style="font-size: 11px; color: #a1a1aa; max-width: 380px; display: block; margin-top: 0.25rem; line-height: 1.5;">
                            Describe your brand identity parameters on the left and submit to let the model generate complete visual assets.
                        </span>
                    </span>
                </span>
            """, unsafe_allow_html=True)
        else:
            resp = st.session_state.ai_response
            pal = resp["hexPalette"]
            
            st.markdown(f"""
                <span style="display:block; margin-bottom:1.5rem;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 8px; color:#c5a022; font-weight:bold; text-transform:uppercase; display:block;">Generated Brand Tagline</span>
                    <h4 style="font-size: 1.25rem; font-family:serif; font-style:italic; color:#ffffff !important; margin: 2px 0 0 0;">
                        "{resp['brandSlogan']}"
                    </h4>
                </span>
                <span style="display:block; margin-bottom:1.5rem;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 8px; color:#71717a; font-weight:bold; text-transform:uppercase; display:block;">Core Landing Headline</span>
                    <span style="font-size: 14px; font-weight:700; color:#e4e4e7; display:block; margin-top:2px;">
                        {resp['heroHeadline']}
                    </span>
                </span>
                <span style="display:block; margin-bottom:1.5rem;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 8px; color:#71717a; font-weight:bold; text-transform:uppercase; display:block;">Elite Visual Board</span>
                    <p style="font-size: 11px; font-weight:300; color:#a1a1aa; line-height:1.5; background-color:rgba(255,255,255,0.02); padding:0.75rem 1rem; border-radius:10px; border:1px solid #1f1f1f; margin-top:4px;">
                        {resp['luxuryColorDescription']}
                    </p>
                </span>
                
                <!-- Swatch render and injector inside spans -->
                <span style="display:block; margin-bottom:1.5rem; background-color: rgba(255,255,255,0.01); border:1px solid #1f1f1f; padding: 1rem; border-radius:12px;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 8px; color:#71717a; font-weight:bold; text-transform:uppercase; display:block; margin-bottom:0.75rem;">Generated HEX Palettes:</span>
                    <span style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem; text-align: center; margin-bottom: 1rem;">
                        <span>
                            <span style="display:block; height:32px; border-radius:4px; border:1px solid rgba(255,255,255,0.1); background-color:{pal['primaryBg']};"></span>
                            <span style="font-size:8px; font-family:'JetBrains Mono', monospace; color:#a1a1aa; display:block; margin-top:2px;">{pal['primaryBg']}</span>
                        </span>
                        <span>
                            <span style="display:block; height:32px; border-radius:4px; border:1px solid rgba(255,255,255,0.1); background-color:{pal['textColor']};"></span>
                            <span style="font-size:8px; font-family:'JetBrains Mono', monospace; color:#a1a1aa; display:block; margin-top:2px;">{pal['textColor']}</span>
                        </span>
                        <span>
                            <span style="display:block; height:32px; border-radius:4px; border:1px solid rgba(255,255,255,0.1); background-color:{pal['accentColor']};"></span>
                            <span style="font-size:8px; font-family:'JetBrains Mono', monospace; color:#a1a1aa; display:block; margin-top:2px;">{pal['accentColor']}</span>
                        </span>
                        <span>
                            <span style="display:block; height:32px; border-radius:4px; border:1px solid rgba(255,255,255,0.1); background-color:{pal['secondaryBg']};"></span>
                            <span style="font-size:8px; font-family:'JetBrains Mono', monospace; color:#a1a1aa; display:block; margin-top:2px;">{pal['secondaryBg']}</span>
                        </span>
                    </span>
                </span>
            """, unsafe_allow_html=True)
            
            apply_pal = st.button("Apply AI Custom Theme", key="apply_ai_swatches_btn")
            if apply_pal:
                st.session_state.preview_theme = "aiCustom"
                st.toast("🎨 Customized strategic style injected into Sandbox.", icon="🎨")
                st.rerun()
                
            st.markdown("""
                <span style="display:block; border-top: 1px solid #1f1f1f; padding-top:1rem; margin-top:1rem;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 8px; color:#71717a; font-weight:bold; text-transform:uppercase; display:block; margin-bottom: 0.5rem;">Synthesized Structural Sections:</span>
                    <span style="display:grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 0.5rem;">
            """, unsafe_allow_html=True)
            
            for section in resp["sectionsCopy"]:
                st.markdown(f"""
                        <span style="background-color: #121212; border: 1px solid #1f1f1f; padding: 0.75rem; border-radius: 8px; display:block;">
                            <strong style="font-family: serif; font-size: 10px; color: #c5a022; display:block;">{section['title']}</strong>
                            <span style="font-size: 9px; color: #71717a; display:block; margin-top:4px; line-height:1.3;">{section['body']}</span>
                        </span>
                """, unsafe_allow_html=True)
                
            st.markdown("""
                    </span>
                </span>
            """, unsafe_allow_html=True)
            
        st.markdown("</span>", unsafe_allow_html=True)

def render_pricing_calculator():
    """Bespoke multi-tier customizer receipt."""
    st.markdown("""
        <span style="display: block; margin-top: 4rem; margin-bottom: 2rem;">
            <span style="text-align: center; display: block; max-width: 700px; margin: 0 auto; margin-bottom: 3rem;">
                <span style="display: inline-flex; align-items: center; gap: 0.5rem; background-color: rgba(197,160,34,0.12); border: 1px solid rgba(197,160,34,0.3); padding: 0.35rem 1rem; border-radius: 50px; color: #9c7d15; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 1rem;">
                    💸 Transparent Configuration Intake
                </span>
                <h2 style="font-size: 2.25rem; font-weight: 700; margin: 0; color: #064e3b;">Calibrate your custom digital standard</h2>
                <p style="color: #6b7280; font-weight: 300; font-size: 14px; margin-top: 0.75rem;">
                    Adjust page requirements, provision dedicated hardware tiers, and map managed service parameters to generate an initial delivery and subscription overview.
                </p>
            </span>
        </span>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([7, 5])
    
    with col1:
        st.markdown("""
            <span style="display: block; background-color: #ffffff; border: 1px solid #ebd69c; border-radius: 20px; padding: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.02); height: 100%;">
                <span style="font-family: serif; font-size: 1.2rem; font-weight: 700; color: #064e3b; display: block; border-bottom: 1px solid #f3f4f6; padding-bottom: 0.75rem; margin-bottom: 1.25rem;">
                    Calibrate Layout Scope
                </span>
        """, unsafe_allow_html=True)
        
        # Select base service tier
        st.session_state.selected_tier = st.selectbox(
            "Select Base Service Tier",
            ["Bespoke Single", "Signature", "Enterprise"],
            index=["Bespoke Single", "Signature", "Enterprise"].index(st.session_state.selected_tier),
            key="pricing_tier_selectbox"
        )
        
        # Select multi-pageoverage
        st.session_state.extra_pages = st.slider(
            "Additional High-Fidelity Web Pages (+ $50/page setup)",
            min_value=0, max_value=15, value=st.session_state.extra_pages, step=1,
            key="pricing_overage_slider"
        )
        
        # Select billing cycle
        st.session_state.billing_cycle = st.selectbox(
            "Hosting Billing Cycle",
            ["Monthly", "Annual"],
            index=["Monthly", "Annual"].index(st.session_state.billing_cycle),
            key="pricing_billing_cycle_selectbox"
        )
        
        # Add-ons
        st.session_state.seo_premium = st.checkbox(
            "SEO Framework Integration (+$35/mo)",
            value=st.session_state.seo_premium,
            key="pricing_seo_chk_box"
        )
        st.session_state.speed_opt = st.checkbox(
            "Extreme Edge CDN Deployments (+$25/mo)",
            value=st.session_state.speed_opt,
            key="pricing_speed_chk_box"
        )
        
        st.markdown("</span>", unsafe_allow_html=True)
        
    with col2:
        receipt = calculate_pricing_details()
        
        st.markdown(f"""
            <span style="display: block; background-color: #0c0c0c; border: 1px solid #27272a; border-radius: 20px; padding: 2.5rem; color: #ffffff; height: 100%;">
                <span style="text-align: center; border-bottom: 1px solid #1f1f1f; padding-bottom: 1.25rem; margin-bottom: 1.5rem;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #c5a022; font-weight: bold; letter-spacing: 0.15em; display: block; text-transform: uppercase;">Estimated Allocation Invoice</span>
                    <h3 style="font-size: 1.5rem; color: #ffffff !important; margin: 4px 0 0 0;">{st.session_state.selected_tier} Tier</h3>
                </span>
                
                <span style="display: block; margin-bottom: 1.5rem; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #a1a1aa; line-height: 1.6;">
                    <span style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                        <span>Setup Design Fee:</span>
                        <span style="color:#ffffff;">${st.session_state.selected_tier == 'Bespoke Single' and '1,200' or (st.session_state.selected_tier == 'Signature' and '2,800' or '6,500')} USD</span>
                    </span>
                    <span style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                        <span>Extra Pages Overage:</span>
                        <span style="color:#ffffff;">+${st.session_state.extra_pages * 50} USD</span>
                    </span>
                    <span style="display: flex; justify-content: space-between; margin-bottom: 6px; border-top: 1px dashed #1f1f1f; padding-top: 6px;">
                        <span>Secure Compute Hosting:</span>
                        <span style="color:#ffffff;">${st.session_state.selected_tier == 'Bespoke Single' and '$45' or (st.session_state.selected_tier == 'Signature' and '$85' or '$195')}/mo</span>
                    </span>
                    <span style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                        <span>Premium SEO Boost:</span>
                        <span style="color:#ffffff;">+${st.session_state.seo_premium and '35' or '0'}/mo</span>
                    </span>
                    <span style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                        <span>Extreme Speed CDN:</span>
                        <span style="color:#ffffff;">+${st.session_state.speed_opt and '25' or '0'}/mo</span>
                    </span>
                    {"<span style='display: flex; justify-content: space-between; color: #10b981; margin-bottom:6px;'><span>Annual billing discount:</span><span>-20% off monthly</span></span>" if st.session_state.billing_cycle == "Annual" else ""}
                </span>
                
                <span style="display: block; border-top: 1px solid #1f1f1f; padding-top: 1.25rem; margin-top: 1.5rem;">
                    <span style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.5rem;">
                        <span style="font-size: 10px; font-weight: 700; text-transform: uppercase; color: #a1a1aa; font-family: 'JetBrains Mono', monospace;">Initial Build Setup:</span>
                        <span style="font-family: serif; font-size: 1.75rem; font-weight: bold; color: #ffffff;">${receipt['setup_fee']} USD</span>
                    </span>
                    <span style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 1.5rem;">
                        <span style="font-size: 10px; font-weight: 700; text-transform: uppercase; color: #c5a022; font-family: 'JetBrains Mono', monospace;">Managed Hosting Subs:</span>
                        <span style="text-align: right;">
                            <span style="font-family: serif; font-size: 1.75rem; font-weight: bold; color: #10b981;">{int(receipt['monthly'])} USD</span>
                            <span style="font-size: 9px; color: #71717a; display: block; font-family: 'JetBrains Mono', monospace;">/ month (billed {st.session_state.billing_cycle.lower()})</span>
                        </span>
                    </span>
                </span>
                
                <span style="display: block; background-color: #121212; padding: 1rem; border-radius: 12px; border: 1px solid #1f1f1f; font-size: 11px; color: #a1a1aa; line-height: 1.5; margin-bottom: 1.5rem;">
                    <span style="color: #ffffff; font-weight: bold; display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                        🛡️ Intellect Copyright Charter
                    </span>
                    Upon complete layout deployment, 100% intellectual patents, custom Next.js script configurations, and structured server variables legally belong to you.
                </span>
                
                <a href="#intake-form-section" style="text-decoration: none;">
                    <span style="display: block; text-align: center; background-color: #c5a022; color: #0a0a0a; font-weight: bold; border-radius: 12px; font-size: 11px; font-family: 'JetBrains Mono', monospace; text-transform: uppercase; letter-spacing: 0.1em; padding: 0.75rem 1.5rem; transition: background-color 0.3s;">
                        Submit Intake Dossier
                    </span>
                </a>
            </span>
        """, unsafe_allow_html=True)

def render_case_studies():
    """Beautiful luxury showcase cards containing portfolios."""
    st.markdown("""
        <span style="display: block; margin-top: 4rem; margin-bottom: 2rem;">
            <span style="display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 1rem; border-bottom: 1px solid #ebd69c; padding-bottom: 1.5rem; margin-bottom: 3rem;">
                <span style="display: block;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #9c7d15; font-weight: bold; letter-spacing: 0.15em; text-transform: uppercase;">Prestige Portfolio</span>
                    <h2 style="font-size: 2.25rem; font-weight: 700; margin: 4px 0 0 0;">Case Studies in Digital Luxury</h2>
                </span>
                <p style="color: #6b7280; font-weight: 300; font-size: 14px; max-width: 400px; margin: 0; line-height: 1.5;">
                    View flagship client environments configured with high-fidelity, hand-compiled web structures.
                </p>
            </span>
        </span>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    cases = [
        {
            "title": "Aura Wellness",
            "tag": "BOTANICAL SPA",
            "bg": "#032e23",
            "text": "#e0e7ff",
            "spec": "0.18s Load Speed",
            "body": "Replaced bulky platform templates with compiled Next.js scripts. Complete bounce rate dropped to near zero, increasing premium booking conversions."
        },
        {
            "title": "Vanguard Capital",
            "tag": "PRIVATE ASSETS",
            "bg": "#0e0e0e",
            "text": "#ffffff",
            "spec": "AWS Cloud Isolated",
            "body": "An exquisite secured gateway launched inside restricted networks. Real-time dynamic charts populate transaction details with direct ledger encryption."
        },
        {
            "title": "Oasis Premium",
            "tag": "ESTATE REALTY",
            "bg": "#1e1b4b",
            "text": "#f5f3ff",
            "spec": "Dynamic WebP Nodes",
            "body": "An evocative layout presenting high-definition media portfolios. Asset compression engines automatically optimize dimensions dynamically at global edge nodes."
        }
    ]
    
    for idx, col in enumerate([col1, col2, col3]):
        c = cases[idx]
        with col:
            st.markdown(f"""
                <span style="display: block; background-color: {c['bg']}; color: {c['text']}; border-radius: 24px; padding: 2.5rem; min-height: 380px; position: relative; box-shadow: 0 10px 20px rgba(0,0,0,0.05); overflow: hidden;">
                    <span style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 9px; letter-spacing: 0.15em; color: #ebd69c; font-weight: bold;">{c['tag']}</span>
                        <span style="background-color: rgba(255,255,255,0.08); font-family: 'JetBrains Mono', monospace; font-size: 9px; padding: 0.25rem 0.6rem; border-radius: 50px;">{c['spec']}</span>
                    </span>
                    <h4 style="font-size: 2rem; color: #ffffff !important; font-weight: 700; margin: 0; font-family: 'Playfair Display', serif;">{c['title']}</h4>
                    <p style="font-size: 12px; font-weight: 300; opacity: 0.8; margin-top: 1rem; line-height: 1.6; min-height: 100px;">
                        {c['body']}
                    </p>
                    <span style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 1.25rem; margin-top: 2rem; font-family: 'JetBrains Mono', monospace; font-size: 10px; opacity: 0.6;">
                        <span>Pure Digital Joy</span>
                        <span style="text-decoration: underline;">View Case</span>
                    </span>
                </span>
            """, unsafe_allow_html=True)

def render_roadmaps():
    """Renders the milestones roadmap."""
    st.markdown("""
        <span style="display: block; margin-top: 4rem; margin-bottom: 2rem;">
            <span style="text-align: center; display: block; max-width: 700px; margin: 0 auto; margin-bottom: 3rem;">
                <span style="display: inline-flex; align-items: center; gap: 0.5rem; background-color: rgba(6,78,59,0.08); border: 1px solid rgba(6,78,59,0.2); padding: 0.35rem 1rem; border-radius: 50px; color: #064e3b; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 1rem;">
                    🎯 Elite Lifecycle Milestones
                </span>
                <h2 style="font-size: 2.25rem; font-weight: 700; margin: 0; color: #064e3b;">How your digital masterpiece is forged</h2>
                <p style="color: #6b7280; font-weight: 300; font-size: 14px; margin-top: 0.75rem;">
                    We handle every architectural step dynamically, guiding development from raw creative concepts to secured virtual cloud networks.
                </p>
            </span>
        </span>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    milestones = [
        {"num": "01", "stage": "Design Stage", "title": "Creative Blueprint", "desc": "We map custom wireframes pixel-by-pixel, resolving distinct premium layouts tailored cleanly to brand assets."},
        {"num": "02", "stage": "Build Stage", "title": "Tailwind Assembly", "desc": "We write compiled Next.js structures and optimize static loading speeds to resolve the most stringent SEO requirements."},
        {"num": "03", "stage": "Host Stage", "title": "AWS Cloud Nesting", "desc": "We spin up secured dedicated EC2 virtual nodes, isolate SQL logs databases, and configure SSL certificates."},
        {"num": "04", "stage": "Launch Stage", "title": "Grand Orbit Live", "desc": "We route domain caching globally and arm web application firewalls with 100% active uptime diagnostic alerts."}
    ]
    
    for idx, col in enumerate([col1, col2, col3, col4]):
        m = milestones[idx]
        with col:
            st.markdown(f"""
                <span style="display: block; background-color: #ffffff; border: 1px solid #ebd69c; border-radius: 20px; padding: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.02); min-height: 280px; position: relative;">
                    <span style="font-family: serif; font-size: 2.5rem; font-weight: bold; color: rgba(197,160,34,0.25) !important; display: block; line-height: 1;">{m['num']}</span>
                    <span style="display: block; margin-top: 1rem;">
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 9px; color: #c5a022; font-weight: bold; text-transform: uppercase; display: block;">{m['stage']}</span>
                        <strong style="font-family: serif; font-size: 14px; color: #064e3b; display: block; margin-top: 2px;">{m['title']}</strong>
                    </span>
                    <p style="font-size: 11px; color: #6b7280; line-height: 1.5; margin-top: 0.75rem; font-weight: 300;">
                        {m['desc']}
                    </p>
                </span>
            """, unsafe_allow_html=True)

def render_consultation():
    """Renders the luxury multi-step intake dossier form."""
    st.markdown("""<span id="intake-form-section" style="display:block; margin-top:4rem;"></span>""", unsafe_allow_html=True)
    
    st.markdown("""
        <span style="display: block; max-width: 900px; margin: 0 auto; background-color: #ffffff; border: 1px solid #ebd69c; border-radius: 24px; box-shadow: 0 10px 30px rgba(6,78,59,0.03); overflow: hidden;">
            <span style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));">
                <!-- Side Panel -->
                <span style="background-color: #064e3b; color: #ffffff; padding: 3rem; display: flex; flex-direction: column; justify-content: space-between; gap: 3rem;">
                    <span style="display: block;">
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 9px; color: #c5a022; font-weight: bold; letter-spacing: 0.15em; text-transform: uppercase; display: block;">Bespoke Intake Gate</span>
                        <h3 style="font-size: 2.25rem; color: #ffffff !important; font-weight: 700; margin: 4px 0 0 0; line-height: 1.1;">Initiate Private Commission</h3>
                        <p style="font-size: 12px; font-weight: 300; opacity: 0.8; margin-top: 1.25rem; line-height: 1.6;">
                            Due to our high-frequency optimization standards and strict hardware VM allocations, we operate under limited commissions. Submit secure dossier details.
                        </p>
                    </span>
                    
                    <span style="display: block; font-family: 'JetBrains Mono', monospace; font-size: 10px; opacity: 0.8; line-height: 1.8;">
                        <span style="display: block;">✦ 100% Dedicated Developer Focus</span>
                        <span style="display: block;">✦ Average Deployment: 21 Days</span>
                        <span style="display: block;">✦ Direct Developer Pager Channels</span>
                    </span>
                    
                    <span style="font-size: 10px; opacity: 0.4;">
                        © 2026 afriSuite Managed Systems. <br>Pure Digital Joy.
                    </span>
                </span>
                
                <!-- Input Panel -->
                <span style="padding: 3rem; display: block;">
        """, unsafe_allow_html=True)
        
    if not st.session_state.consultation_submitted:
        st.markdown("""
            <span style="display: block; border-bottom: 1px solid #f3f4f6; padding-bottom: 0.75rem; margin-bottom: 1.5rem;">
                <span style="font-family: serif; font-size: 1.25rem; font-weight: bold; color: #064e3b; display: block;">Configuration parameters</span>
            </span>
        """, unsafe_allow_html=True)
        
        c_name = st.text_input("Your Full Name", value="", placeholder="Sterling", key="intake_full_name_field")
        c_email = st.text_input("Email Address", value="", placeholder="you@domain.com", key="intake_email_address_field")
        c_company = st.text_input("Brand Enterprise Name", value="", placeholder="Aura Wellness Ltd.", key="intake_brand_company_field")
        
        c_interest = st.selectbox(
            "Service Allocation Target",
            ["The Unified Suite (Design + Host)", "afriDesign Agency (Frontend Only)", "afriHost Dedicated Cloud (Hosting Only)"],
            key="intake_service_selectbox"
        )
        
        c_message = st.text_area(
            "Custom Technical Directives",
            value="",
            placeholder="Describe database requirements, structural pings, or layout objectives...",
            key="intake_custom_directives_field",
            height=80
        )
        
        st.markdown('<span style="display:block; margin-top: 1.5rem;"></span>', unsafe_allow_html=True)
        
        submit_intake = st.button("Submit Dossier", key="intake_form_submit_btn")
        if submit_intake:
            if c_name and c_email:
                st.session_state.consultation_submitted = True
                st.toast("✔ Dossier successfully registered. Allocations locked.", icon="✔")
                st.rerun()
            else:
                st.toast("⚠️ Name and email attributes are required.", icon="🔍")
    else:
        st.markdown("""
            <span style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 4rem 0; gap: 1rem;">
                <span style="font-size: 40px; display: block;">✨</span>
                <span style="display: block;">
                    <span style="font-family: serif; font-size: 1.25rem; font-weight: bold; color: #064e3b; display: block;">Dossier Successfully Filed</span>
                    <span style="font-size: 12px; color: #6b7280; max-width: 280px; display: block; margin: 0.5rem auto; line-height: 1.5;">
                        A senior architectural lead will review your custom variables and coordinate access protocols within 2 hours.
                    </span>
                </span>
            </span>
        """, unsafe_allow_html=True)
        reset_intake = st.button("Configure Alternate parameters", key="intake_reset_form_btn")
        if reset_intake:
            st.session_state.consultation_submitted = False
            st.rerun()
            
    st.markdown("""
                </span>
            </span>
        </span>
    """, unsafe_allow_html=True)

def render_faqs():
    """Interactive accordions detailing platform operations."""
    st.markdown("""
        <span style="display: block; margin-top: 4rem; margin-bottom: 2rem;">
            <span style="text-align: center; display: block; max-width: 700px; margin: 0 auto; margin-bottom: 3rem;">
                <span style="display: inline-flex; align-items: center; gap: 0.5rem; background-color: rgba(6,78,59,0.08); border: 1px solid rgba(6,78,59,0.2); padding: 0.35rem 1rem; border-radius: 50px; color: #064e3b; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 1rem;">
                    🔎 Inquisitive Minds
                </span>
                <h2 style="font-size: 2.25rem; font-weight: 700; margin: 0; color: #064e3b;">Frequently Explored Questions</h2>
            </span>
        </span>
    """, unsafe_allow_html=True)
    
    faqs = [
        {
            "q": "What makes afriSuite superior to standard managed WordPress setups?",
            "a": "WordPress introduces bloated themes, continuous database routing, and unsecured plugins. AfriSuite compiles raw Next.js layout configurations directly, caching HTML snapshots at 22 global endpoints to render platforms in 0.18 seconds."
        },
        {
            "q": "Am I legally locked into afriHost for web hosting services?",
            "a": "No. Upon delivery of setup services, intellectual copyrights are registered dynamically under your brand. Assets can be migrated to alternate environments easily without proprietary software dependencies."
        },
        {
            "q": "How does the simulated AWS Deploy button function in the Visual Sandbox?",
            "a": "The simulated trigger replicates our automated AWS API cluster configurations. In real commissions, our pipelines securely spin up dedicated EC2 instances, map CloudFront edge nodes, bind custom SSLs, and route your domains globally to guarantee 100% load speeds."
        },
        {
            "q": "How does the direct developer pager guarantee work?",
            "a": "Our premium clients bypass standard ticketing logs. You receive direct channels to the exact software architect assigned to your build files, resolving issues instantly."
        }
    ]
    
    st.markdown('<span style="display:block; max-width: 800px; margin: 0 auto;">', unsafe_allow_html=True)
    for index, faq in enumerate(faqs):
        with st.expander(faq["q"]):
            st.write(faq["a"])
    st.markdown('</span>', unsafe_allow_html=True)

def render_footer_acknowledgements():
    """Displays standard corporate acknowledgements and edge status monitors."""
    st.markdown("""
        <span style="display: block; background-color: #0a0a0a; border-top: 1px solid #1f1f1f; padding: 4rem 2rem; margin-top: 6rem; color: #71717a;">
            <span style="max-width: 1124px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 3rem; margin-bottom: 3rem;">
                
                <!-- Column 1 -->
                <span>
                    <span style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                        <span style="font-size: 1.5rem;">💎</span>
                        <span style="font-family: serif; font-size: 1.3rem; font-weight: bold; color: #ffffff;">AFRISUITE</span>
                    </span>
                    <p style="font-size: 12px; font-weight: 300; color: #a1a1aa; line-height: 1.6; margin: 0;">
                        Sculpting pristine layout architectures and dedicated high-frequency cloud hosting containers from South Africa. Designed to luxury standards.
                    </p>
                </span>
                
                <!-- Column 2 -->
                <span>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: bold; text-transform: uppercase; color: #ffffff; letter-spacing: 0.1em; display: block; margin-bottom: 1rem;">
                        Interactive Shortcuts
                    </span>
                    <span style="display: flex; flex-direction: column; gap: 0.5rem; font-size: 12px; font-weight: 300;">
                        <a href="#segmented_navigation_tabs" style="color: #a1a1aa; text-decoration: none;">Interactive Sandbox Preview</a>
                        <a href="#segmented_navigation_tabs" style="color: #a1a1aa; text-decoration: none;">AWS Telemetry cluster Map</a>
                        <a href="#segmented_navigation_tabs" style="color: #a1a1aa; text-decoration: none;">Secure SSH Console</a>
                        <a href="#segmented_navigation_tabs" style="color: #a1a1aa; text-decoration: none;">Intake Dossier Form</a>
                    </span>
                </span>
                
                <!-- Column 3 -->
                <span>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: bold; text-transform: uppercase; color: #ffffff; letter-spacing: 0.1em; display: block; margin-bottom: 1rem;">
                        Newsletter Registration
                    </span>
                    <p style="font-size: 12px; font-weight: 300; color: #a1a1aa; line-height: 1.5; margin: 0; margin-bottom: 0.75rem;">
                        Join our private catalog log to receive quarterly tech availability bulletins.
                    </p>
                </span>
            </span>
    """, unsafe_allow_html=True)
    
    # Nested subscription input using spans
    st.markdown('<span style="max-width:350px; display:block; margin-bottom:2rem;">', unsafe_allow_html=True)
    sub_email = st.text_input("Enter Email Address", value="", placeholder="enter your email...", key="footer_news_email_input_field", label_visibility="collapsed")
    sub_submit = st.button("Subscribe to Bulletins", key="footer_news_sub_btn")
    if sub_submit:
        if sub_email:
            st.toast("✔ Successfully added to our premium database.", icon="✨")
        else:
            st.toast("⚠️ Input a valid email address.", icon="🔍")
    st.markdown('</span>', unsafe_allow_html=True)
    
    st.markdown("""
            <span style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #1f1f1f; padding-top: 1.5rem; flex-wrap: wrap; gap: 1rem; font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; letter-spacing: 0.15em;">
                <span>© 2026 afriSuite Managed Systems. Pure Digital Joy.</span>
                <span style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="width: 6px; height: 6px; background-color: #10b981; border-radius: 50%; display: inline-block;"></span>
                    <span>AWS Core Instances Secured</span>
                </span>
            </span>
        </span>
    """, unsafe_allow_html=True)

# ==============================================================================
# 6. UNIFIED COORDINATOR APPLICATION RUNNER
# ==============================================================================
def main():
    """Coordinate layout blocks smoothly sequentially without gaps."""
    # 1. Styles Injection
    inject_master_styles()
    
    # 2. Rendering Loop
    render_live_ticker()
    render_navigation_header()
    render_hero_section()
    render_performance_audit()
    render_payload_simulator()
    render_visual_sandbox()
    render_aws_telemetry()
    render_terminal_console()
    render_api_simulator()
    render_ai_brand_strategist()
    render_pricing_calculator()
    render_case_studies()
    render_roadmaps()
    render_consultation()
    render_faqs()
    render_footer_acknowledgements()

if __name__ == "__main__":
    main()