import streamlit as st
import time
import random
from datetime import datetime

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Afrihost Premium Studio",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS — Using native Streamlit styling + span helpers
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&family=JetBrains+Mono:wght@400;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .gold-text { 
        background: linear-gradient(135deg, #fef08a 0%, #fbbf24 50%, #d97706 100%); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        font-weight: 900; 
    }
    .mono { font-family: 'JetBrains Mono', monospace; }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-family: 'JetBrains Mono', monospace;
    }
    .badge-amber { background: #fbbf24; color: #022c22; }
    .badge-dark { background: #022c22; color: #fbbf24; }
    .badge-green { background: #047857; color: white; }
    .glass {
        background: rgba(255,255,255,0.75);
        backdrop-filter: blur(16px);
        border-radius: 1.5rem;
        padding: 2rem;
        border: 1px solid rgba(255,255,255,0.6);
        box-shadow: 0 8px 32px 0 rgba(2,44,34,0.04);
    }
    .panel-dark {
        background: rgba(1,27,20,0.92);
        backdrop-filter: blur(20px);
        border-radius: 1.5rem;
        padding: 2rem;
        border: 1px solid rgba(255,255,255,0.08);
        color: white;
    }
    .mesh-bg {
        background-color: #011b14;
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(4,120,87,0.45) 0%, transparent 45%),
            radial-gradient(circle at 90% 80%, rgba(245,158,11,0.15) 0%, transparent 45%);
    }
    .chat-bot { background: #f3f4f6; color: #1f2937; border-radius: 1rem; border-top-left-radius: 0; padding: 1rem; }
    .chat-user { background: #022c22; color: white; border-radius: 1rem; border-top-right-radius: 0; padding: 1rem; }
    .chat-system { background: #fef2f2; color: #991b1b; border-radius: 9999px; padding: 0.5rem 1rem; font-size: 0.7rem; font-family: 'JetBrains Mono', monospace; }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #022c22; 
        color: #fbbf24; 
        border-radius: 0.75rem; 
        padding: 0.5rem 1.5rem; 
        font-weight: 700; 
        font-size: 0.75rem; 
        text-transform: uppercase; 
        letter-spacing: 0.05em; 
    }
    .stTabs [aria-selected="true"] { 
        background-color: #fbbf24 !important; 
        color: #022c22 !important; 
    }

    /* Button overrides */
    .stButton>button {
        border-radius: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.7rem;
    }

    /* Metric styling */
    [data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace; font-weight: 900; }
    [data-testid="stMetricLabel"] { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.05em; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE INITIALIZATION — All keys declared upfront
# ============================================================
DEFAULTS = {
    "current_tab": "home",
    "selected_node": None,
    "sidebar_search": "",
    "expanded_nodes": {"1":True, "1.1":True, "1.1.6":True, "1.1.6.4":True, "1.1.6.4.4":True, "1.1.6.4.4.1":True},
    "domain_query": "",
    "domain_tld": ".co.za",
    "domain_result": None,
    "layout_type": "portfolio",
    "accent_color": "gold",
    "cms_integration": True,
    "seo_optimization": True,
    "custom_forms": False,
    "staging_project_name": "My Dream Project",
    "is_annual_billing": False,
    "selected_server_id": "jhb",
    "hosting_test_state": "idle",
    "hosting_results": {"ping":0, "download":0, "upload":0, "ttfb":"--"},
    "hosting_history": [
        {"date":"10 mins ago", "server":"Johannesburg", "ping":"2ms", "download":"943 Mbps", "upload":"491 Mbps"},
        {"date":"1 hour ago", "server":"Cape Town", "ping":"15ms", "download":"812 Mbps", "upload":"382 Mbps"}
    ],
    "client_zone_sub_tab": "projects",
    "support_chat": [{"sender":"bot", "text":"Welcome to the Afrihost Premium Web & Cloud Support Suite. How can I assist you with your staging site or server configuration today?", "time":"Just now"}],
    "message_input": "",
    "is_chat_typing": False,
    "dns_flush_active": False,
    "noc_stats": {"cpu":31, "bandwidth":824, "connections":4182, "status":"SECURE", "failoverActive": False},
    "noc_logs": [
        "Cloud infrastructure monitoring active.",
        "BGP routing protocols balanced on primary WACS circuit.",
        "Dynamic Nginx cache configured for Client Projects."
    ],
    "selected_product": None,
    "checkout_step": 1,
    "form_data": {"name":"", "email":"", "phone":"", "company":""},
    "speed_test_trigger": False,
    "domain_check_trigger": False,
    "dns_flush_trigger": False,
    "send_chat_trigger": False,
    "checkout_next_trigger": False,
    "checkout_back_trigger": False,
    "checkout_finish_trigger": False,
    "close_checkout_trigger": False,
    "purge_cache_trigger": False,
    "failover_trigger": False,
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
# DATA CONSTANTS
# ============================================================
CODE_GLOSSARY = {
    "1": { "name": "DESIGN SYSTEMS", "desc": "Premium Web Design Framework Hub & Mockup Engine" },
    "1.1": { "name": "FRONTEND STACK", "desc": "HTML5, CSS3, & Modern JavaScript Frontend Frameworks" },
    "1.1.1": { "name": "TAILWIND STYLES", "desc": "Tailwind CSS Utility-First Configuration Suite" },
    "1.1.2": { "name": "REACT COMPONENTS", "desc": "React Single Page Application Engine" },
    "1.1.3": { "name": "NEXT.JS STATIC SITES", "desc": "Next.js Static Site Generation (SSG) & SSR Router" },
    "1.1.4": { "name": "FIGMA PROTOTYPES", "desc": "High-Fidelity Wireframes & Figma Dynamic Layouts" },
    "1.1.5": { "name": "SEO INTEGRITY", "desc": "Advanced Search Engine Optimization Pipelines & JSON-LD schema" },
    "1.1.6": { "name": "CLOUD HOST-CORE", "desc": "Global Managed Cloud Hosting Orchestrator" },
    "1.1.6.1": { "name": "NVMe SSD POOL", "desc": "Primary Enterprise NVMe SSD Raid-10 High Speed Arrays" },
    "1.1.6.2": { "name": "CDN EDGE NODES", "desc": "African Regional Content Delivery Edge Cache Nodes" },
    "1.1.6.3": { "name": "SSL CERTIFICATES", "desc": "Auto-Renewing Let's Encrypt Encryption Gateways" },
    "1.1.6.4": { "name": "DATABASE CLUSTERS", "desc": "High-Availability PostgreSQL & Dedicated Redis Instances" },
    "1.1.6.4.1": { "name": "REDIS CACHE", "desc": "Redis In-Memory Key-Value Caching Layer" },
    "1.1.6.4.2": { "name": "S3 BACKUPS", "desc": "Hourly S3 Off-Site Compressed Backup Repositories" },
    "1.1.6.4.3": { "name": "DDOS SHIELD", "desc": "Global DDoS Traffic Scrubbing Cluster & WAF Guard" },
    "1.1.6.4.4": { "name": "NOC SITE SYNC", "desc": "Network Operations & Critical Website Live Sync Engine" },
    "1.1.6.4.4.1": { "name": "RSA CLOUD HUB", "desc": "South African Republic Primary Hosting Cluster" },
    "1.1.6.4.4.1.1": { "name": "RSA-WEB", "desc": "Production Nginx Web Server Core" },
    "1.1.6.4.4.1.2": { "name": "RSA-DB", "desc": "Clustered Primary Database Instance" },
    "1.1.6.4.4.1.3": { "name": "RSA-DNS", "desc": "Ultra-low Latency Anycast DNS Node" },
    "1.1.6.4.4.1.4": { "name": "RSA-NOC", "desc": "Active Site Heartbeat Check Pipeline" },
    "1.1.6.4.4.1.5": { "name": "RSA-CRM", "desc": "Client Portal CRM Integration Core" },
    "1.1.6.4.4.1.6": { "name": "RSA-MAIL", "desc": "Secured Postfix IMAP/POP3 Webmail Handler" },
    "1.1.6.4.4.1.7": { "name": "RSA-STAGING", "desc": "Client Development sandbox environment" },
    "1.1.6.4.4.1.8": { "name": "RSA-BILLING", "desc": "Automated Billing, invoices, & dynamic ledgers" },
    "1.1.6.4.4.1.9": { "name": "RSA-FIREWALL", "desc": "Hardware IPS/IDS Stateful Packet Inspector" },
    "1.1.6.4.5": { "name": "GLOBAL FALLBACK", "desc": "Secondary routing to EU/US cloud mirrors" },
    "1.2": { "name": "STAGING PLAYGROUND", "desc": "Isolated developer workspace for customer testing" },
    "2": { "name": "DOMAIN DNS REGISTRAR", "desc": "Dynamic DNS & instant domain registration system" },
    "3": { "name": "IMAP MAIL EXCHANGE", "desc": "Premium corporate custom email routing servers" },
    "4": { "name": "WORDPRESS ENGINE", "desc": "Optimized Managed WordPress cache layers" },
    "5": { "name": "STAGING ENVIRONMENTS", "desc": "Dynamic isolated site deployment pods" },
    "6": { "name": "API GATEWAY CLUSTER", "desc": "Security endpoint gateway with traffic rate-limiters" },
    "7": { "name": "BGP ROUTING INFRA", "desc": "Dynamic multi-homed transit balancer" },
    "8": { "name": "BILLING & INVOICING", "desc": "Core customer payment processor & sync node" },
    "9": { "name": "HEADLESS CMS API", "desc": "Fast-loading content delivery API cluster" }
}

NAVIGATION_DATA = [
    {
        "id": "1",
        "label": "1. DESIGN SYSTEMS",
        "children": [
            {
                "id": "1.1",
                "label": "1.1. FRONTEND STACK",
                "children": [
                    { "id": "1.1.1", "label": "1.1.1. TAILWIND STYLES" },
                    { "id": "1.1.2", "label": "1.1.2. REACT COMPONENTS" },
                    { "id": "1.1.3", "label": "1.1.3. NEXT.JS STATIC SITES" },
                    { "id": "1.1.4", "label": "1.1.4. FIGMA PROTOTYPES" },
                    { "id": "1.1.5", "label": "1.1.5. SEO INTEGRITY" },
                    {
                        "id": "1.1.6",
                        "label": "1.1.6. CLOUD HOST-CORE",
                        "children": [
                            { "id": "1.1.6.1", "label": "1.1.6.1. NVMe SSD POOL" },
                            { "id": "1.1.6.2", "label": "1.1.6.2. CDN EDGE NODES" },
                            { "id": "1.1.6.3", "label": "1.1.6.3. SSL CERTIFICATES" },
                            {
                                "id": "1.1.6.4",
                                "label": "1.1.6.4. DATABASE CLUSTERS",
                                "children": [
                                    { "id": "1.1.6.4.1", "label": "1.1.6.4.1. REDIS CACHE" },
                                    { "id": "1.1.6.4.2", "label": "1.1.6.4.2. S3 BACKUPS" },
                                    { "id": "1.1.6.4.3", "label": "1.1.6.4.3. DDOS SHIELD" },
                                    {
                                        "id": "1.1.6.4.4",
                                        "label": "1.1.6.4.4. NOC SITE SYNC",
                                        "children": [
                                            {
                                                "id": "1.1.6.4.4.1",
                                                "label": "1.1.6.4.4.1. RSA CLOUD HUB",
                                                "children": [
                                                    { "id": "1.1.6.4.4.1.1", "label": "1.1.6.4.4.1.1. RSA-WEB" },
                                                    { "id": "1.1.6.4.4.1.2", "label": "1.1.6.4.4.1.2. RSA-DB" },
                                                    { "id": "1.1.6.4.4.1.3", "label": "1.1.6.4.4.1.3. RSA-DNS" },
                                                    { "id": "1.1.6.4.4.1.4", "label": "1.1.6.4.4.1.4. RSA-NOC" },
                                                    { "id": "1.1.6.4.4.1.5", "label": "1.1.6.4.4.1.5. RSA-CRM" },
                                                    { "id": "1.1.6.4.4.1.6", "label": "1.1.6.4.4.1.6. RSA-MAIL" },
                                                    { "id": "1.1.6.4.4.1.7", "label": "1.1.6.4.4.1.7. RSA-STAGING" },
                                                    { "id": "1.1.6.4.4.1.8", "label": "1.1.6.4.4.1.8. RSA-BILLING" },
                                                    { "id": "1.1.6.4.4.1.9", "label": "1.1.6.4.4.1.9. RSA-FIREWALL" },
                                                ]
                                            }
                                        ]
                                    },
                                    { "id": "1.1.6.4.5", "label": "1.1.6.4.5. GLOBAL FALLBACK" }
                                ]
                            }
                        ]
                    },
                    { "id": "1.2", "label": "1.2. STAGING PLAYGROUND" }
                ]
            }
        ]
    },
    { "id": "2", "label": "2. DOMAIN DNS REGISTRAR" },
    { "id": "3", "label": "3. IMAP MAIL EXCHANGE" },
    { "id": "4", "label": "4. WORDPRESS ENGINE" },
    { "id": "5", "label": "5. STAGING ENVIRONMENTS" },
    { "id": "6", "label": "6. API GATEWAY CLUSTER" },
    { "id": "7", "label": "7. BGP ROUTING INFRA" },
    { "id": "8", "label": "8. BILLING & INVOICING" },
    { "id": "9", "label": "9. HEADLESS CMS API" }
]

HOSTING_SERVERS = [
    { "id": "jhb", "name": "Johannesburg Teraco Datacenter", "code": "JHB-Core-1", "ping": 2, "ttfb": "12ms" },
    { "id": "cpt", "name": "Cape Town ClockTower Hub", "code": "CPT-Edge-2", "ping": 14, "ttfb": "24ms" },
    { "id": "lon", "name": "London Equinix LD5", "code": "LON-Uplink-4", "ping": 142, "ttfb": "155ms" },
    { "id": "nyc", "name": "New York Telehouse North", "code": "NYC-Transit-8", "ping": 210, "ttfb": "228ms" }
]

# ============================================================
# HELPERS
# ============================================================
def calculate_design_price():
    base = 2500
    if st.session_state.layout_type == "corporate":
        base = 4800
    if st.session_state.layout_type == "ecommerce":
        base = 8500
    add_ons = 0
    if st.session_state.cms_integration:
        add_ons += 1200
    if st.session_state.seo_optimization:
        add_ons += 750
    if st.session_state.custom_forms:
        add_ons += 450
    return base + add_ons

def calculate_hosting_monthly_price():
    base = 99
    if st.session_state.layout_type == "corporate":
        base = 199
    if st.session_state.layout_type == "ecommerce":
        base = 499
    return base

def get_hosting_price(base_monthly):
    if st.session_state.is_annual_billing:
        discounted = base_monthly * 0.85
        return {"unit": "pm", "value": round(discounted), "period_label": "billed annually"}
    return {"unit": "pm", "value": base_monthly, "period_label": "billed monthly"}

def flatten_tree(nodes, depth=0):
    result = []
    for node in nodes:
        result.append((node, depth))
        if node.get("children") and st.session_state.expanded_nodes.get(node["id"], False):
            result.extend(flatten_tree(node["children"], depth + 1))
    return result

def handle_domain_check():
    if not st.session_state.domain_query.strip():
        return
    st.session_state.domain_result = "checking"
    time.sleep(1.2)
    h = len(st.session_state.domain_query) % 3
    st.session_state.domain_result = "taken" if h == 0 else "available"

def run_speed_test():
    st.session_state.hosting_test_state = "pinging"
    st.session_state.hosting_results = {"ping": 0, "download": 0, "upload": 0, "ttfb": "--"}
    time.sleep(1.2)

    target = next(s for s in HOSTING_SERVERS if s["id"] == st.session_state.selected_server_id)
    st.session_state.hosting_results["ping"] = target["ping"]
    st.session_state.hosting_results["ttfb"] = target["ttfb"]

    st.session_state.hosting_test_state = "download"
    target_max = 620 if st.session_state.selected_server_id in ["lon", "nyc"] else 940
    for i in range(10):
        st.session_state.hosting_results["download"] = min(target_max, (i + 1) * (target_max / 10) + random.randint(-20, 20))
        time.sleep(0.1)
    st.session_state.hosting_results["download"] = target_max + random.uniform(0, 8)

    st.session_state.hosting_test_state = "upload"
    target_up = target_max / 2
    for i in range(10):
        st.session_state.hosting_results["upload"] = min(target_up, (i + 1) * (target_up / 10) + random.randint(-10, 10))
        time.sleep(0.1)
    st.session_state.hosting_results["upload"] = target_up + random.uniform(0, 5)

    st.session_state.hosting_test_state = "complete"
    st.session_state.hosting_history.insert(0, {
        "date": "Just now",
        "server": target["name"].split(" ")[0],
        "ping": f"{target['ping']}ms",
        "download": f"{st.session_state.hosting_results['download']:.0f} Mbps",
        "upload": f"{st.session_state.hosting_results['upload']:.0f} Mbps"
    })
    if len(st.session_state.hosting_history) > 5:
        st.session_state.hosting_history = st.session_state.hosting_history[:5]

def send_chat_message():
    text = st.session_state.message_input.strip()
    if not text:
        return
    st.session_state.support_chat.append({"sender": "user", "text": text, "time": "Just now"})
    st.session_state.message_input = ""
    st.session_state.is_chat_typing = True
    time.sleep(1.5)

    lower = text.lower()
    if any(w in lower for w in ["slow", "load", "speed"]):
        bot = "Your static site TTFB metrics look brilliant. Please trigger a DNS Cache Flush inside your diagnostics panel on the left to force refresh client-side resources."
    elif any(w in lower for w in ["design", "layout", "figma"]):
        bot = "We are currently completing the layout templates on the staging playground node. Please check the Staging Playgrounds status above to monitor latest wireframe commits."
    elif any(w in lower for w in ["billing", "invoice", "payment"]):
        bot = "Invoices INV-2026-902 is cleared. You can download the dynamic PDF ledger inside your ClientZone Overview panel."
    else:
        bot = "I have scanned your active project staging servers. All Nginx routing configs are perfectly secure. What else can I investigate?"

    st.session_state.support_chat.append({"sender": "bot", "text": bot, "time": "Just now"})
    st.session_state.is_chat_typing = False

def trigger_dns_flush():
    st.session_state.dns_flush_active = True
    st.session_state.support_chat.append({"sender": "system", "text": "SYSTEM TELEMETRY: Flushed dynamic DNS registers globally...", "time": "Just now"})
    time.sleep(2.5)
    st.session_state.support_chat.append({"sender": "bot", "text": "I have force-rebuilt your staging domain's Anycast records and invalidated static router caches. Staging site should reflect changes instantly.", "time": "Just now"})
    st.session_state.dns_flush_active = False

# ============================================================
# SIDEBAR — INTERACTIVE TREE (All widgets use unique keys)
# ============================================================
with st.sidebar:
    st.markdown('<span style="font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:0.05em;color:#64748b;">Project Staging Telemetry</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    search = st.text_input("Search server layers...", value=st.session_state.sidebar_search, key="sidebar_search_input")
    st.session_state.sidebar_search = search

    st.markdown("""<span style="font-size:0.6rem;color:#94a3b8;font-family:monospace;">Click layers to stream diagnostic health</span>""", unsafe_allow_html=True)
    st.markdown("<hr style='margin:0.5rem 0;border-color:#e2e8f0;'>", unsafe_allow_html=True)

    for node, depth in flatten_tree(NAVIGATION_DATA):
        has_children = bool(node.get("children"))
        is_expanded = st.session_state.expanded_nodes.get(node["id"], False)
        indent = "&nbsp;" * (depth * 4)

        cols = st.columns([1, 12])
        with cols[0]:
            if has_children:
                icon = "▼" if is_expanded else "▶"
                if st.button(icon, key=f"toggle_{node['id']}", help="Expand/collapse"):
                    st.session_state.expanded_nodes[node["id"]] = not is_expanded
                    st.rerun()
            else:
                st.markdown("<span style='color:#10b981;font-size:1.2rem;'>•</span>", unsafe_allow_html=True)

        with cols[1]:
            label = f"{indent}{node['label']}"
            if search and search.upper() in node["label"].upper():
                label = f"{indent}<span style='color:#fbbf24;font-weight:700;'>{node['label']}</span>"
            if st.button(label, key=f"select_{node['id']}"):
                st.session_state.selected_node = node
                st.session_state.current_tab = "node-view"
                st.session_state.noc_logs = [
                    f"Initiating deployment telemetry for node: {node['label']}...",
                    "Syncing live containers with Afrihost Docker registry...",
                    "Connection synchronized. Status: SECURE."
                ]
                st.rerun()

    st.markdown("<hr style='margin:0.5rem 0;border-color:#e2e8f0;'>", unsafe_allow_html=True)
    st.markdown('<span class="badge badge-dark">Managed Platform Systems</span>', unsafe_allow_html=True)
    st.markdown('<span style="font-size:0.6rem;color:#94a3b8;font-family:monospace;">ALL SEGMENTS COMPILING : SECURE</span>', unsafe_allow_html=True)

# ============================================================
# MAIN NAVIGATION — st.tabs with keys handled via session state
# ============================================================
if st.session_state.current_tab == "node-view" and st.session_state.selected_node:
    # NODE VIEW OVERRIDE
    if st.button("← Return to Home Portal", key="back_from_node"):
        st.session_state.current_tab = "home"
        st.session_state.selected_node = None
        st.rerun()

    node = st.session_state.selected_node
    info = CODE_GLOSSARY.get(node["id"], {"name": node["label"], "desc": "Standard high-performance cloud container node."})

    st.markdown(f"""
    <div class="mesh-bg" style="padding:2rem;border-radius:1.5rem;border-bottom:4px solid #fbbf24;margin-bottom:2rem;">
        <span style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.2em;color:#fbbf24;font-family:monospace;">Infrastructure Node Active</span>
        <h1 style="color:white;font-family:monospace;margin:0.5rem 0;">{node['label']}</h1>
        <p style="color:#a7f3d0;font-size:0.85rem;max-width:600px;">{info['desc']}</p>
        <span class="badge badge-green" style="margin-top:1rem;">● SECURE</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("<h3 style='font-size:1rem;font-weight:700;'>Dynamic Telemetry Gauges</h3>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("CPU Host Capacity", f"{st.session_state.noc_stats['cpu']}%", delta="Cores Secured", delta_color="normal")
        with c2:
            st.metric("Transit Throughput", f"{st.session_state.noc_stats['bandwidth']}M", delta="Mbps Speed", delta_color="normal")
        with c3:
            st.metric("Active Web Clients", f"{st.session_state.noc_stats['connections']:,}", delta="Tunnels IPv4", delta_color="normal")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-size:1rem;font-weight:700;'>Dynamic Server Interventions</h3>", unsafe_allow_html=True)
        st.markdown("<span style='font-size:0.8rem;color:#64748b;'>Force simulated modifications on this server cluster node.</span>", unsafe_allow_html=True)

        ic1, ic2 = st.columns(2)
        with ic1:
            if st.button("🗑 Purge Static Cache", key="purge_cache_btn"):
                st.session_state.noc_logs.insert(0, "ALERT: Cache purge successfully completed on staging container. TTL reset.")
                st.rerun()
        with ic2:
            failover_label = "Disable CDN Failover" if st.session_state.noc_stats["failoverActive"] else "Enable Standby CDN Mirror"
            if st.button(f"⚡ {failover_label}", key="failover_btn"):
                st.session_state.noc_stats["failoverActive"] = not st.session_state.noc_stats["failoverActive"]
                st.session_state.noc_logs.insert(0, f"ACTION TRIPPED: Node traffic routing redirected to standby {'European' if st.session_state.noc_stats['failoverActive'] else 'primary'} Cloud mirrors.")
                st.rerun()

    with col2:
        st.markdown("""
        <div class="panel-dark" style="height:100%;">
            <span style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.05em;color:#94a3b8;">● Node Log Stream</span>
            <span style="font-size:0.6rem;color:#64748b;float:right;">Live Telemetry</span>
            <hr style='border-color:#334155;margin:0.75rem 0;'>
        """, unsafe_allow_html=True)

        for log in st.session_state.noc_logs[:8]:
            ts = datetime.now().strftime("%H:%M:%S")
            st.markdown(f"""
            <div style="border-bottom:1px solid #334155;padding-bottom:0.5rem;margin-bottom:0.5rem;">
                <span style="font-size:0.6rem;color:#64748b;font-family:monospace;">[{ts}]</span><br>
                <span style="font-size:0.75rem;color:#e2e8f0;">{log}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
            <div style="background:#022c22;padding:0.75rem;border-radius:0.75rem;border:1px solid #334155;margin-top:1rem;">
                <span style="font-size:0.6rem;color:#34d399;font-family:monospace;text-transform:uppercase;">Node Integrity State</span>
                <span style="font-size:0.75rem;color:#fbbf24;float:right;font-weight:700;">100% SECURE</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    # STANDARD TABS
    tab_labels = ["🏠 HOME", "🎨 WEB DESIGN", "☁️ WEB HOSTING", "👤 CLIENTZONE"]
    tabs = st.tabs(tab_labels)

    # ============================================================
    # TAB 0: HOME
    # ============================================================
    with tabs[0]:
        st.markdown("""
        <div class="mesh-bg" style="padding:3rem 2rem;text-align:center;border-radius:0 0 2rem 2rem;border-bottom:4px solid #fbbf24;margin-bottom:2rem;">
            <span class="badge badge-dark" style="border:1px solid #fbbf24;margin-bottom:1rem;">👑 Premium Digital Architecture Agency</span>
            <h1 style="color:white;font-size:2.5rem;font-weight:900;line-height:1.1;">
                Bespoke Web Design & <br><span class="gold-text">High-Performance Cloud Hosting.</span>
            </h1>
            <p style="color:#a7f3d0;max-width:600px;margin:1rem auto;font-size:0.9rem;">
                Crafting beveled, responsive, and state-of-the-art web portals backed by Afrihost's elite tier-1 optical transit grid.
            </p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            <div class="glass">
                <h3 style="color:#022c22;font-size:1.25rem;font-weight:900;">Bespoke Web Design</h3>
                <p style="color:#64748b;font-size:0.85rem;">Custom hand-crafted layouts designed directly around your brand. Powered by high-efficiency frontend React modules.</p>
                <ul style="color:#334155;font-size:0.85rem;list-style:none;padding:0;">
                    <li>✅ Fully Responsive Mobile Optimization</li>
                    <li>✅ Custom Integrated Headless CMS Engines</li>
                    <li>✅ Core Web Vitals & Premium SEO Audit</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Configure Design Style Mockup", key="home_to_design", use_container_width=True):
                st.session_state.current_tab = "design"
                st.rerun()

        with c2:
            st.markdown("""
            <div class="glass">
                <h3 style="color:#022c22;font-size:1.25rem;font-weight:900;">Premium Cloud Web Hosting</h3>
                <p style="color:#64748b;font-size:0.85rem;">Blazing fast, secure Anycast DNS web containers. Solid raid-10 NVMe SSD architecture with Let's Encrypt shields.</p>
                <ul style="color:#334155;font-size:0.85rem;list-style:none;padding:0;">
                    <li>✅ Auto Let's Encrypt SSL Security Certs</li>
                    <li>✅ High Availability Docker Container Nodes</li>
                    <li>✅ DDoS Traffic Mitigating Intelligent Scrub</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Test Server Node Speed", key="home_to_hosting", use_container_width=True):
                st.session_state.current_tab = "hosting"
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Domain Checker
        st.markdown("""
        <div class="panel-dark" style="border:1px solid rgba(251,191,36,0.3);box-shadow:0 0 15px rgba(251,191,36,0.1);">
            <div style="text-align:center;max-width:600px;margin:0 auto;">
                <span class="badge badge-dark" style="border:1px solid rgba(251,191,36,0.3);color:#fbbf24;">Dynamic Domain Lookup</span>
                <h2 style="color:white;margin-top:1rem;">Secure Your Premium Server Alias</h2>
                <p style="color:#a7f3d0;font-size:0.85rem;">Instant validation across global ICANN registries & Afrihost staging databases.</p>
            </div>
        """, unsafe_allow_html=True)

        dc1, dc2, dc3 = st.columns([3, 1, 1])
        with dc1:
            st.text_input("Domain name", placeholder="your-luxury-enterprise", key="domain_input", value=st.session_state.domain_query)
        with dc2:
            st.selectbox("TLD", [".co.za", ".com", ".net", ".org"], index=0, key="domain_tld_select")
        with dc3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Analyze Domain", key="domain_check_btn", use_container_width=True):
                st.session_state.domain_query = st.session_state.domain_input
                st.session_state.domain_tld = st.session_state.domain_tld_select
                handle_domain_check()
                st.rerun()

        if st.session_state.domain_result:
            if st.session_state.domain_result == "checking":
                st.info("⏳ Checking domain availability...")
            elif st.session_state.domain_result == "available":
                st.success(f"✅ **{st.session_state.domain_query}{st.session_state.domain_tld}** is available for provisioning.")
                price = 199 if st.session_state.domain_tld == ".com" else 99
                if st.button(f"Acquire Address — R{price}", key="buy_domain_btn"):
                    st.session_state.selected_product = {"name": f"Domain registration: {st.session_state.domain_query}{st.session_state.domain_tld}", "price": price, "type": "domain"}
                    st.session_state.checkout_step = 1
                    st.rerun()
            else:
                st.error(f"❌ **{st.session_state.domain_query}{st.session_state.domain_tld}** is taken. Try **{st.session_state.domain_query}-staging{st.session_state.domain_tld}** instead.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ============================================================
    # TAB 1: WEB DESIGN
    # ============================================================
    with tabs[1]:
        st.markdown("""
        <div class="mesh-bg" style="padding:2rem;border-radius:1.5rem;border-bottom:4px solid #fbbf24;margin-bottom:2rem;">
            <span style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.1em;color:#fbbf24;font-family:monospace;">bespoke layout studio</span>
            <h2 style="color:white;margin:0.5rem 0;">Interactive Web Design Configurator</h2>
            <p style="color:#a7f3d0;font-size:0.85rem;">Dynamically adjust layout styles, select accent colors, configure key web structures.</p>
        </div>
        """, unsafe_allow_html=True)

        # Pricing Grid
        st.markdown("<h3 style='text-align:center;font-size:1.5rem;font-weight:900;'>Premium Curated Design Plans</h3>", unsafe_allow_html=True)
        p1, p2, p3 = st.columns(3)

        packages = [
            ("Standard Portfolio", "Launch / CV", 2500, "1-3 Premium Pages", "Figma High-Fidelity Prototype", "Fully Responsive Mobile CSS Grid", None, None),
            ("Corporate Growth Hub", "Corporate / SME", 4800, "Up to 8 Bespoke Page Layouts", "Figma Interactive Prototype Sync", "Core Web Vitals Optimization", "Basic Headless CMS Panel", "Dynamic Custom Forms Engine"),
            ("Enterprise E-Commerce Engine", "E-Commerce", 8500, "Unlimited Product Inventory pages", "Stripe / PayFast Gateways integrated", "Custom Inventory Manager Suite", "Automated S3 Image Compression", "Anycast Global Load Balancing"),
        ]

        for idx, (col, pkg) in enumerate(zip([p1, p2, p3], packages)):
            name, tag, price, f1, f2, f3, f4, f5 = pkg
            with col:
                border = "2px solid #fbbf24" if idx == 1 else "1px solid #e2e8f0"
                badge = "<span class='badge badge-amber'>Most Popular Tier</span>" if idx == 1 else f"<span class='badge' style='background:#f1f5f9;color:#334155;'>{tag}</span>"
                st.markdown(f"""
                <div style="background:white;border-radius:1.5rem;padding:1.5rem;border:{border};box-shadow:0 4px 6px -1px rgba(0,0,0,0.1);height:100%;display:flex;flex-direction:column;">
                    <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:1rem;">
                        {badge}
                        <div style="text-align:right;">
                            <span style="font-size:1.5rem;font-weight:900;font-family:monospace;">R{price:,}</span>
                            <span style="font-size:0.65rem;color:#94a3b8;display:block;">One-Time Config</span>
                        </div>
                    </div>
                    <h4 style="margin:0.5rem 0;color:#022c22;">{name}</h4>
                    <ul style="font-size:0.8rem;color:#334155;list-style:none;padding:0;margin:1rem 0;flex-grow:1;">
                        <li>✅ {f1}</li>
                        <li>✅ {f2}</li>
                        <li>✅ {f3}</li>
                        {f"<li>✅ {f4}</li>" if f4 else ""}
                        {f"<li>✅ {f5}</li>" if f5 else ""}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                btn_key = f"design_pkg_{idx}"
                if st.button("Choose " + name.split()[0], key=btn_key, use_container_width=True):
                    st.session_state.selected_product = {"name": f"Web Design: {name} Package", "price": price, "type": "design"}
                    st.session_state.checkout_step = 1
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Configurator
        st.markdown("<h3 style='text-align:center;'>Custom-Tailor Layout Settings</h3>", unsafe_allow_html=True)
        cfg1, cfg2 = st.columns([7, 5])

        with cfg1:
            st.markdown("""
            <div class="glass" style="height:100%;">
                <h4 style="margin-top:0;">Dynamic Browser Staging Preview</h4>
                <p style="font-size:0.8rem;color:#64748b;">A high-fidelity rendering of your custom site structure.</p>
            """, unsafe_allow_html=True)

            # Browser mockup using spans only (no divs) per user request
            accent_hex = {"gold":"#fbbf24", "emerald":"#10b981", "blue":"#3b82f6", "orange":"#f97316"}[st.session_state.accent_color]
            layout = st.session_state.layout_type
            proj = st.session_state.staging_project_name.upper()

            mockup_html = f"""
            <div style="background:#0f172a;border-radius:1rem;overflow:hidden;border:1px solid #334155;">
                <div style="background:#1e293b;padding:0.75rem 1rem;display:flex;align-items:center;gap:0.5rem;border-bottom:1px solid #334155;">
                    <span style="width:0.75rem;height:0.75rem;background:#ef4444;border-radius:50%;display:inline-block;"></span>
                    <span style="width:0.75rem;height:0.75rem;background:#eab308;border-radius:50%;display:inline-block;"></span>
                    <span style="width:0.75rem;height:0.75rem;background:#22c55e;border-radius:50%;display:inline-block;"></span>
                    <span style="background:#0f172a;color:#64748b;font-family:monospace;font-size:0.65rem;padding:0.25rem 1rem;border-radius:0.5rem;margin-left:auto;margin-right:auto;border:1px solid #334155;">
                        https://staging.{st.session_state.staging_project_name.lower().replace(" ", "-")}.co.za
                    </span>
                </div>
                <div style="background:white;padding:1.5rem;min-height:200px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:1rem;border-bottom:1px solid #e2e8f0;margin-bottom:1rem;">
                        <span style="font-weight:900;color:#0f172a;font-size:0.9rem;">{proj}</span>
                        <span style="font-size:0.7rem;font-weight:700;color:{accent_hex};">HOME</span>
                        <span style="font-size:0.7rem;font-weight:700;color:#64748b;">SERVICES</span>
                        <span style="font-size:0.7rem;font-weight:700;color:#64748b;">CONTACT</span>
                    </div>
            """

            if layout == "portfolio":
                mockup_html += """
                    <div style="text-align:center;padding:2rem 0;">
                        <h4 style="color:#0f172a;font-size:1.25rem;font-weight:900;margin:0;">Luxury Creator Portfolio</h4>
                        <p style="color:#64748b;font-size:0.75rem;max-width:300px;margin:0.5rem auto;">Showcasing bespoke photography and high-end graphic achievements.</p>
                        <div style="display:flex;gap:0.5rem;justify-content:center;margin-top:1rem;">
                            <span style="width:4rem;height:3rem;background:#f1f5f9;border-radius:0.5rem;display:inline-block;"></span>
                            <span style="width:4rem;height:3rem;background:#f1f5f9;border-radius:0.5rem;display:inline-block;"></span>
                            <span style="width:4rem;height:3rem;background:#f1f5f9;border-radius:0.5rem;display:inline-block;"></span>
                        </div>
                    </div>
                """
            elif layout == "corporate":
                mockup_html += """
                    <div style="padding:1rem 0;">
                        <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1rem;">
                            <span style="width:3rem;height:3rem;background:#f1f5f9;border-radius:0.5rem;display:inline-flex;align-items:center;justify-content:center;color:#94a3b8;font-size:1.25rem;">📊</span>
                            <div>
                                <h4 style="margin:0;color:#0f172a;font-size:0.9rem;">Enterprise Service Dashboard</h4>
                                <p style="margin:0;color:#94a3b8;font-size:0.7rem;">Optimized structure built for standard financial systems.</p>
                            </div>
                        </div>
                        <span style="height:1rem;background:#f8fafc;border-radius:0.5rem;display:block;margin-bottom:0.5rem;"></span>
                        <span style="height:1rem;background:#f8fafc;border-radius:0.5rem;display:block;width:83%;"></span>
                    </div>
                """
            else:  # ecommerce
                mockup_html += """
                    <div style="padding:1rem 0;text-align:center;">
                        <h4 style="color:#0f172a;font-size:0.9rem;font-weight:900;margin:0 0 1rem 0;">Premium Online Retail Hub</h4>
                        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.5rem;">
                            <span style="border:1px solid #e2e8f0;padding:0.75rem;border-radius:0.75rem;background:#f8fafc;display:inline-block;text-align:center;">
                                <span style="height:2rem;background:#e2e8f0;border-radius:0.5rem;display:block;margin-bottom:0.5rem;"></span>
                                <strong style="font-size:0.7rem;color:#0f172a;">Item A</strong>
                            </span>
                            <span style="border:1px solid #e2e8f0;padding:0.75rem;border-radius:0.75rem;background:#f8fafc;display:inline-block;text-align:center;">
                                <span style="height:2rem;background:#e2e8f0;border-radius:0.5rem;display:block;margin-bottom:0.5rem;"></span>
                                <strong style="font-size:0.7rem;color:#0f172a;">Item B</strong>
                            </span>
                            <span style="border:1px solid #e2e8f0;padding:0.75rem;border-radius:0.75rem;background:#f8fafc;display:inline-block;text-align:center;">
                                <span style="height:2rem;background:#e2e8f0;border-radius:0.5rem;display:block;margin-bottom:0.5rem;"></span>
                                <strong style="font-size:0.7rem;color:#0f172a;">Item C</strong>
                            </span>
                        </div>
                    </div>
                """

            mockup_html += f"""
                    <div style="display:flex;justify-content:space-between;align-items:center;padding-top:1rem;border-top:1px solid #e2e8f0;margin-top:1rem;font-size:0.6rem;color:#94a3b8;">
                        <span>Powered by Afrihost Premium Cluster</span>
                        <span>
                            {"<strong style='color:#047857;'>[CMS]</strong>" if st.session_state.cms_integration else ""}
                            {"<strong style='color:#d97706;'>[SEO]</strong>" if st.session_state.seo_optimization else ""}
                            {"<strong style='color:#2563eb;'>[FORMS]</strong>" if st.session_state.custom_forms else ""}
                        </span>
                    </div>
                </div>
            </div>
            """
            st.markdown(mockup_html, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with cfg2:
            st.markdown("<div class='glass' style='height:100%;'>", unsafe_allow_html=True)
            st.markdown("<h4 style='margin-top:0;'>Visual Specs Customization</h4>", unsafe_allow_html=True)

            st.text_input("Project Name", value=st.session_state.staging_project_name, key="project_name_input")
            st.session_state.staging_project_name = st.session_state.project_name_input

            st.markdown("<span style='font-size:0.75rem;font-weight:700;color:#64748b;'>Base Layout Configuration</span>", unsafe_allow_html=True)
            layout_opts = {"portfolio": "Portfolio (R2,500)", "corporate": "Corporate (R4,800)", "ecommerce": "E-Commerce (R8,500)"}
            layout_opts_list = list(layout_opts.keys())
            layout_choice = st.radio(
                "Layout", 
                options=layout_opts_list, 
                format_func=lambda x: layout_opts[x], 
                key="layout_seg", 
                index=layout_opts_list.index(st.session_state.layout_type),
                horizontal=True
            )
            st.session_state.layout_type = layout_choice

            st.markdown("<span style='font-size:0.75rem;font-weight:700;color:#64748b;margin-top:1rem;display:block;'>Brand Accent Color</span>", unsafe_allow_html=True)
            color_cols = st.columns(4)
            colors = [("gold", "#fbbf24", "Amber"), ("emerald", "#10b981", "Emerald"), ("blue", "#3b82f6", "Royal"), ("orange", "#f97316", "Orange")]
            for i, (cid, chex, clabel) in enumerate(colors):
                with color_cols[i]:
                    if st.button(clabel, key=f"color_{cid}", use_container_width=True):
                        st.session_state.accent_color = cid
                        st.rerun()
                    st.markdown(f"""<span style='width:1.5rem;height:1.5rem;background:{chex};border-radius:50%;display:block;margin:0.25rem auto;border:2px solid {"#022c22" if st.session_state.accent_color == cid else "#e2e8f0"};'></span>""", unsafe_allow_html=True)

            st.markdown("<span style='font-size:0.75rem;font-weight:700;color:#64748b;margin-top:1rem;display:block;'>Architecture Integrations</span>", unsafe_allow_html=True)
            st.checkbox("Headless CMS Pipeline (+R1,200)", value=st.session_state.cms_integration, key="cms_chk")
            st.session_state.cms_integration = st.session_state.cms_chk
            st.checkbox("Premium SEO Engineering (+R750)", value=st.session_state.seo_optimization, key="seo_chk")
            st.session_state.seo_optimization = st.session_state.seo_chk
            st.checkbox("Bespoke Forms Engine (+R450)", value=st.session_state.custom_forms, key="forms_chk")
            st.session_state.custom_forms = st.session_state.forms_chk

            total = calculate_design_price()
            monthly = calculate_hosting_monthly_price()
            st.markdown(f"""
            <div style="background:linear-gradient(to right, #022c22, #064e3b);color:white;padding:1.25rem;border-radius:1rem;margin-top:1rem;border:1px solid #065f46;">
                <span style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.1em;color:#fbbf24;font-family:monospace;">Estimated Project Cost</span>
                <div style="font-size:1.5rem;font-weight:900;font-family:monospace;margin:0.25rem 0;">R{total:,}</div>
                <span style="font-size:0.65rem;color:#a7f3d0;">Hosting: R{monthly}/pm thereafter</span>
                <button style="background:#fbbf24;color:#022c22;border:none;padding:0.75rem 1.5rem;border-radius:0.75rem;font-weight:900;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.05em;margin-top:0.75rem;cursor:pointer;width:100%;">
                    Order Design
                </button>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Order Design", key="order_design_btn", use_container_width=True):
                st.session_state.selected_product = {
                    "name": f"Custom Tailor Website: {st.session_state.staging_project_name} ({st.session_state.layout_type.upper()})",
                    "price": total,
                    "type": "design"
                }
                st.session_state.checkout_step = 1
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # ============================================================
    # TAB 2: WEB HOSTING
    # ============================================================
    with tabs[2]:
        st.markdown("""
        <div class="mesh-bg" style="padding:2rem;border-radius:1.5rem;border-bottom:4px solid #fbbf24;margin-bottom:2rem;">
            <span style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.1em;color:#fbbf24;font-family:monospace;">solid state cloud containers</span>
            <h2 style="color:white;margin:0.5rem 0;">NVMe SSD Cloud Hosting Suite</h2>
            <p style="color:#a7f3d0;font-size:0.85rem;">Deploy high-availability virtual private servers. Audit performance instantly using our localized TTFB and transit speedtester tool.</p>
            <span class="badge badge-green" style="margin-top:0.5rem;">● 99.99% UPTIME SLA</span>
        </div>
        """, unsafe_allow_html=True)

        # Billing Toggle
        st.markdown("<div style='text-align:center;margin-bottom:1.5rem;'>", unsafe_allow_html=True)
        billing_cols = st.columns([1, 2, 1])
        with billing_cols[1]:
            b1, b2 = st.columns(2)
            with b1:
                if st.button("Monthly Billing", key="bill_monthly", use_container_width=True, type="primary" if not st.session_state.is_annual_billing else "secondary"):
                    st.session_state.is_annual_billing = False
                    st.rerun()
            with b2:
                if st.button("Annual Save 15%", key="bill_annual", use_container_width=True, type="primary" if st.session_state.is_annual_billing else "secondary"):
                    st.session_state.is_annual_billing = True
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # Plans
        h1, h2, h3 = st.columns(3)
        host_plans = [
            ("SSD Starter", "Starter Sites", 99, "10 GB SSD", "1 vCPU Cores", "5 Databases"),
            ("NVMe Business", "Scale & Growth", 199, "50 GB SSD", "2 vCPU Cores", "25 Databases"),
            ("Premium Cloud Host", "Enterprise Cluster", 499, "200 GB SSD", "4 vCPU Cores", "Unlimited"),
        ]

        for idx, (col, plan) in enumerate(zip([h1, h2, h3], host_plans)):
            name, tag, base, disk, cores, dbs = plan
            price_info = get_hosting_price(base)
            with col:
                border = "2px solid #fbbf24" if idx == 1 else "1px solid #e2e8f0"
                badge = "<span class='badge badge-amber'>Best Business Choice</span>" if idx == 1 else f"<span class='badge' style='background:#f1f5f9;color:#334155;'>{tag}</span>"
                st.markdown(f"""
                <div style="background:white;border-radius:1.5rem;padding:1.5rem;border:{border};box-shadow:0 4px 6px -1px rgba(0,0,0,0.1);height:100%;display:flex;flex-direction:column;">
                    <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:1rem;">
                        {badge}
                        <div style="text-align:right;">
                            <span style="font-size:1.5rem;font-weight:900;font-family:monospace;">R{price_info['value']}</span>
                            <span style="font-size:0.65rem;color:#94a3b8;display:block;text-transform:lowercase;">{price_info['period_label']}</span>
                        </div>
                    </div>
                    <h4 style="margin:0.5rem 0;color:#022c22;">{name}</h4>
                    <div style="font-size:0.75rem;color:#334155;margin:1rem 0;flex-grow:1;font-family:monospace;">
                        <div style="display:flex;justify-content:space-between;padding:0.5rem 0;border-bottom:1px solid #f1f5f9;"><span style="color:#64748b;font-family:sans-serif;">NVMe Raid-10 Disk</span><strong>{disk}</strong></div>
                        <div style="display:flex;justify-content:space-between;padding:0.5rem 0;border-bottom:1px solid #f1f5f9;"><span style="color:#64748b;font-family:sans-serif;">Core Capacity</span><strong>{cores}</strong></div>
                        <div style="display:flex;justify-content:space-between;padding:0.5rem 0;border-bottom:1px solid #f1f5f9;"><span style="color:#64748b;font-family:sans-serif;">Bandwidth</span><strong style="color:#047857;">Unmetered</strong></div>
                        <div style="display:flex;justify-content:space-between;padding:0.5rem 0;border-bottom:1px solid #f1f5f9;"><span style="color:#64748b;font-family:sans-serif;">Databases</span><strong>{dbs}</strong></div>
                        <div style="display:flex;justify-content:space-between;padding:0.5rem 0;"><span style="color:#64748b;font-family:sans-serif;">Free SSL</span><strong style="color:#047857;">Included</strong></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Provision {name.split()[-1]}", key=f"host_btn_{idx}", use_container_width=True):
                    st.session_state.selected_product = {
                        "name": f"{name} Plan ({'Annual' if st.session_state.is_annual_billing else 'Monthly'})",
                        "price": price_info["value"],
                        "type": "hosting"
                    }
                    st.session_state.checkout_step = 1
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Speed Test
        st.markdown("<h3 style='text-align:center;'>Check Cloud Node Latencies</h3>", unsafe_allow_html=True)
        s1, s2 = st.columns([2, 1])

        with s1:
            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            st.markdown("<h4>Instant Cloud Node Speed Diagnostics</h4>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:0.8rem;color:#64748b;'>Select an Afrihost data center gateway to measure connection latencies.</p>", unsafe_allow_html=True)

            srv_cols = st.columns(4)
            for i, srv in enumerate(HOSTING_SERVERS):
                with srv_cols[i]:
                    is_sel = st.session_state.selected_server_id == srv["id"]
                    btn_type = "primary" if is_sel else "secondary"
                    if st.button(srv["name"].split(" ")[0] + " Hub", key=f"srv_{srv['id']}", use_container_width=True, type=btn_type):
                        st.session_state.selected_server_id = srv["id"]
                        st.session_state.hosting_test_state = "idle"
                        st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

            # Speed dial visualization
            target_srv = next(s for s in HOSTING_SERVERS if s["id"] == st.session_state.selected_server_id)
            progress_val = 0.0
            status_text = "Ready to test"

            if st.session_state.hosting_test_state == "pinging":
                progress_val = 0.15
                status_text = "Auditing TTFB..."
            elif st.session_state.hosting_test_state == "download":
                progress_val = min(0.5 + (st.session_state.hosting_results["download"] / 2000), 0.85)
                status_text = f"Downloading... {st.session_state.hosting_results['download']:.0f} Mbps"
            elif st.session_state.hosting_test_state == "upload":
                progress_val = min(0.85 + (st.session_state.hosting_results["upload"] / 1000), 0.99)
                status_text = f"Uploading... {st.session_state.hosting_results['upload']:.0f} Mbps"
            elif st.session_state.hosting_test_state == "complete":
                progress_val = 1.0
                status_text = f"Complete — {st.session_state.hosting_results['download']:.0f} Mbps Down"

            st.write(f"**{status_text}**")
            st.progress(progress_val)

            if st.session_state.hosting_test_state in ["idle", "complete"]:
                if st.button("▶ RUN SPEED TEST", key="run_speed_test_btn", use_container_width=True):
                    run_speed_test()
                    st.rerun()
            else:
                st.button("▶ RUN SPEED TEST", key="run_speed_test_btn_disabled", disabled=True, use_container_width=True)

            # Metrics
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric("Download", f"{st.session_state.hosting_results['download']:.0f} Mbps" if st.session_state.hosting_results['download'] else "--")
            with m2:
                st.metric("Upload", f"{st.session_state.hosting_results['upload']:.0f} Mbps" if st.session_state.hosting_results['upload'] else "--")
            with m3:
                st.metric("Ping", f"{st.session_state.hosting_results['ping']}ms" if st.session_state.hosting_results['ping'] else "--")
            with m4:
                st.metric("TTFB", st.session_state.hosting_results["ttfb"])

            st.markdown("</div>", unsafe_allow_html=True)

        with s2:
            st.markdown("""
            <div class="panel-dark" style="border:1px solid rgba(251,191,36,0.2);box-shadow:0 0 15px rgba(251,191,36,0.1);height:100%;">
                <span style="font-size:0.75rem;font-weight:700;color:#fbbf24;text-transform:uppercase;letter-spacing:0.1em;">Anycast Routing Edge</span>
                <h4 style="color:white;margin:0.5rem 0;font-size:1rem;">Microsecond Latency Response</h4>
                <p style="color:#a7f3d0;font-size:0.8rem;line-height:1.5;">Our dynamic Anycast DNS setups duplicate custom site nodes globally. When a customer queries staging addresses, DNS records point to the nearest physical datacenter cluster.</p>
                <div style="background:#022c22;padding:1rem;border-radius:0.75rem;border:1px solid rgba(251,191,36,0.2);margin-top:1rem;">
                    <span style="font-size:0.65rem;color:#fbbf24;font-family:monospace;text-transform:uppercase;">Global Health Status</span>
                    <span style="font-size:0.9rem;color:white;display:block;font-weight:700;margin-top:0.25rem;">100% Operational</span>
                    <p style="font-size:0.7rem;color:#94a3b8;margin:0.5rem 0 0 0;">DDoS mitigation shielding active. Zero traffic flow interruptions recorded.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # History
        if st.session_state.hosting_history:
            st.markdown("<h4 style='margin-top:2rem;'>Recent Test History</h4>", unsafe_allow_html=True)
            for h in st.session_state.hosting_history[:3]:
                st.markdown(f"""
                <span style="font-size:0.75rem;color:#64748b;font-family:monospace;">
                    {h['date']} — {h['server']} — Ping: {h['ping']} — ↓{h['download']} — ↑{h['upload']}
                </span>
                """, unsafe_allow_html=True)

    # ============================================================
    # TAB 3: CLIENTZONE
    # ============================================================
    with tabs[3]:
        st.markdown("""
        <div class="mesh-bg" style="padding:1.5rem 2rem;border-radius:1.5rem;border-bottom:4px solid #fbbf24;margin-bottom:1.5rem;">
            <span style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.2em;color:#fbbf24;font-family:monospace;">Client Control Panel</span>
            <h2 style="color:white;margin:0.5rem 0;">ClientZone Manager</h2>
            <p style="color:#a7f3d0;font-size:0.8rem;">Account: <strong>#AFR-90823-PRO</strong> • Elite Level Service Tier</p>
        </div>
        """, unsafe_allow_html=True)

        # Subtabs
        cz_options = ["Active Web Projects", "Active Cloud Servers", "Engineer Chat Support"]
        cz_default = st.session_state.client_zone_sub_tab.replace("_", " ").title()
        if cz_default not in cz_options:
            cz_default = "Active Web Projects"
        sub_tabs = st.radio(
            "Section", 
            options=cz_options, 
            key="cz_sub_tab_control", 
            index=cz_options.index(cz_default),
            horizontal=True
        )
        st.session_state.client_zone_sub_tab = sub_tabs.lower().replace(" ", "_")

        if st.session_state.client_zone_sub_tab in ["active_web_projects", "projects"]:
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown("<div class='glass'>", unsafe_allow_html=True)
                st.markdown("<h4>Your Web Design Milestones</h4>", unsafe_allow_html=True)
                st.markdown("""
                <div style="border-left:2px solid #e2e8f0;padding-left:1.5rem;margin-left:0.5rem;">
                    <div style="position:relative;margin-bottom:1.5rem;">
                        <span style="position:absolute;left:-2rem;top:0;width:1.5rem;height:1.5rem;background:#d1fae5;color:#065f46;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;">✓</span>
                        <strong style="font-size:0.85rem;color:#1f2937;">Figma Wireframes Completed</strong>
                        <p style="font-size:0.75rem;color:#64748b;margin:0.25rem 0;">Approved wireframes & styles mapping dynamic gold accents.</p>
                    </div>
                    <div style="position:relative;">
                        <span style="position:absolute;left:-2rem;top:0;width:1.5rem;height:1.5rem;background:#fbbf24;color:#022c22;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;">2</span>
                        <strong style="font-size:0.85rem;color:#1f2937;">Staging Site Development [ACTIVE - 85%]</strong>
                        <p style="font-size:0.75rem;color:#64748b;margin:0.25rem 0;">React components and Nginx reverse proxies loaded on sandbox environment.</p>
                        <span class="badge" style="background:#fffbeb;color:#b45309;border:1px solid #fcd34d;">Pending Client Review</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with c2:
                st.markdown("<div class='glass' style='margin-bottom:1rem;'>", unsafe_allow_html=True)
                st.markdown("<h4 style='margin-top:0;'>Staging Sandbox Control</h4>", unsafe_allow_html=True)
                if st.button("🚀 Launch Staging URL", key="launch_staging", use_container_width=True):
                    st.success("Redirecting to isolated dynamic web staging sandbox panel...")
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("<div class='glass'>", unsafe_allow_html=True)
                st.markdown("<h4 style='margin-top:0;'>Design Billing Overview</h4>", unsafe_allow_html=True)
                st.markdown("""
                <div style="display:flex;justify-content:space-between;align-items:center;padding:0.75rem 0;border-bottom:1px solid #e2e8f0;">
                    <div>
                        <span style="font-size:0.8rem;font-weight:700;color:#1f2937;display:block;">Staging Fee: INV-9022</span>
                        <span style="font-size:0.65rem;color:#94a3b8;">November 2026</span>
                    </div>
                    <span style="font-size:0.85rem;font-weight:900;color:#047857;font-family:monospace;">R2,500 Paid</span>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        elif st.session_state.client_zone_sub_tab == "active_cloud_servers":
            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            st.markdown("<h4>Cloud Host Telemetry Diagnostics</h4>", unsafe_allow_html=True)
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                st.metric("Active Container Host", "NVMe SSD Starter (RSA-WEB-1)", delta="SECURE", delta_color="normal")
            with sc2:
                st.metric("Disk Utilization", "4.2 GB / 10 GB (42%)", delta="NVMe RAID-10", delta_color="normal")
            with sc3:
                st.metric("Bandwidth This Month", "842 GB", delta="Unmetered", delta_color="normal")
            st.markdown("</div>", unsafe_allow_html=True)

        else:  # support chat
            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            chat_col, tool_col = st.columns([3, 1])

            with tool_col:
                st.markdown("<h4 style='margin-top:0;font-size:0.85rem;'>Diagnostic Tools</h4>", unsafe_allow_html=True)
                if st.button("🔄 DNS Cache Flush", key="dns_flush_btn", use_container_width=True):
                    trigger_dns_flush()
                    st.rerun()
                st.markdown("<p style='font-size:0.7rem;color:#64748b;'>Flush global dynamic Anycast registers</p>", unsafe_allow_html=True)

            with chat_col:
                st.markdown("""
                <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:1rem;padding-bottom:1rem;border-bottom:1px solid #e2e8f0;">
                    <span style="width:2.5rem;height:2.5rem;background:#022c22;color:#fbbf24;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:0.75rem;border:2px solid #fbbf24;">KB</span>
                    <div>
                        <span style="font-size:0.85rem;font-weight:700;color:#1f2937;display:block;">Kabelo - Senior Web Architect</span>
                        <span style="font-size:0.65rem;color:#94a3b8;font-family:monospace;text-transform:uppercase;">Premium Afrihost Support Gate</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Chat messages
                chat_container = st.container()
                with chat_container:
                    for msg in st.session_state.support_chat:
                        if msg["sender"] == "system":
                            st.markdown(f"""
                            <div style="text-align:center;margin:0.5rem 0;">
                                <span class="chat-system">{msg['text']}</span>
                            </div>
                            """, unsafe_allow_html=True)
                        elif msg["sender"] == "bot":
                            st.markdown(f"""
                            <div style="margin:0.5rem 0;">
                                <div class="chat-bot" style="display:inline-block;max-width:80%;">
                                    <span style="font-size:0.8rem;">{msg['text']}</span>
                                    <span style="font-size:0.6rem;color:#94a3b8;display:block;text-align:right;margin-top:0.25rem;">{msg['time']}</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="margin:0.5rem 0;text-align:right;">
                                <div class="chat-user" style="display:inline-block;max-width:80%;text-align:left;">
                                    <span style="font-size:0.8rem;">{msg['text']}</span>
                                    <span style="font-size:0.6rem;color:#fbbf24;display:block;text-align:right;margin-top:0.25rem;">{msg['time']}</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                    if st.session_state.is_chat_typing:
                        st.markdown("""
                        <div style="margin:0.5rem 0;">
                            <div class="chat-bot" style="display:inline-block;">
                                <span style="font-size:0.75rem;color:#94a3b8;font-family:monospace;">Typing response...</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                # Chat input
                st.text_input("Describe your server or design concern...", key="chat_input_field")
                if st.button("Send", key="send_chat_btn"):
                    st.session_state.message_input = st.session_state.chat_input_field
                    send_chat_message()
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# CHECKOUT MODAL — Simulated via conditional overlay
# ============================================================
if st.session_state.selected_product:
    st.markdown("""
    <div style="position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(2,44,34,0.85);backdrop-filter:blur(8px);z-index:9999;display:flex;align-items:center;justify-content:center;padding:1rem;">
        <div style="background:white;border-radius:2rem;width:100%;max-width:500px;overflow:hidden;box-shadow:0 25px 50px -12px rgba(0,0,0,0.5);border:1px solid #e2e8f0;">
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div style="background:#022c22;color:white;padding:1.5rem 2rem;display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #fbbf24;">
        <div>
            <span style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.1em;color:#fbbf24;font-family:monospace;">bespoke dynamic provisioning</span>
            <h3 style="margin:0.25rem 0;font-size:1.1rem;">Secure Provisioning Portal</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("✕ Close", key="close_checkout"):
        st.session_state.selected_product = None
        st.rerun()

    # Stepper
    step_cols = st.columns([1, 2, 1, 2, 1, 2, 1])
    for i, step in enumerate([1, 2, 3]):
        with step_cols[i * 2]:
            color = "#022c22" if st.session_state.checkout_step >= step else "#f1f5f9"
            text_color = "white" if st.session_state.checkout_step >= step else "#94a3b8"
            st.markdown(f"""
            <div style="width:2rem;height:2rem;background:{color};color:{text_color};border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:monospace;font-weight:900;font-size:0.85rem;margin:0 auto;">
                {step}
            </div>
            """, unsafe_allow_html=True)
        if i < 2:
            with step_cols[i * 2 + 1]:
                line_color = "#fbbf24" if st.session_state.checkout_step > step else "#e2e8f0"
                st.markdown(f"""
                <div style="height:2px;background:{line_color};margin-top:1rem;"></div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.checkout_step == 1:
        prod = st.session_state.selected_product
        st.markdown(f"""
        <div style="padding:0 2rem;">
            <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:1rem;padding:1rem;display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem;">
                <div>
                    <span style="font-size:0.6rem;text-transform:uppercase;letter-spacing:0.1em;color:#94a3b8;font-family:monospace;">Selected Product</span>
                    <span style="font-size:0.85rem;font-weight:900;color:#1f2937;display:block;margin-top:0.25rem;">{prod['name']}</span>
                </div>
                <span style="font-size:1.25rem;font-weight:900;color:#022c22;font-family:monospace;">R{prod['price']:,}{'/pm' if prod['type'] == 'hosting' else ''}</span>
            </div>
            <p style="font-size:0.8rem;color:#64748b;line-height:1.5;">
                This order will immediately establish an isolated development staging environment and automatically map the dynamic routing configurations onto our active Anycast DNS clusters.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Continue to Contact Specs →", key="checkout_to_step2", use_container_width=True):
            st.session_state.checkout_step = 2
            st.rerun()

    elif st.session_state.checkout_step == 2:
        st.markdown("<div style='padding:0 2rem;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='font-size:0.85rem;text-transform:uppercase;letter-spacing:0.1em;color:#64748b;margin-bottom:1rem;'>Provide Delivery Credentials</h4>", unsafe_allow_html=True)
        st.text_input("Full Name", value=st.session_state.form_data["name"], key="form_name")
        st.text_input("Email Address", value=st.session_state.form_data["email"], key="form_email")
        st.text_input("Company Name (Optional)", value=st.session_state.form_data["company"], key="form_company")
        st.markdown("</div>", unsafe_allow_html=True)

        bc1, bc2 = st.columns(2)
        with bc1:
            if st.button("← Back", key="checkout_back", use_container_width=True):
                st.session_state.checkout_step = 1
                st.rerun()
        with bc2:
            can_proceed = st.session_state.form_name and st.session_state.form_email
            if st.button("Acquire Product", key="checkout_acquire", disabled=not can_proceed, use_container_width=True):
                st.session_state.form_data = {
                    "name": st.session_state.form_name,
                    "email": st.session_state.form_email,
                    "company": st.session_state.form_company,
                    "phone": ""
                }
                st.session_state.checkout_step = 3
                st.rerun()

    elif st.session_state.checkout_step == 3:
        st.markdown(f"""
        <div style="padding:0 2rem;text-align:center;">
            <div style="width:4rem;height:4rem;background:#d1fae5;color:#065f46;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.5rem;margin:0 auto 1rem auto;">✓</div>
            <h3 style="color:#1f2937;margin:0.5rem 0;">Workspace Deployed Successfully!</h3>
            <p style="font-size:0.8rem;color:#64748b;max-width:350px;margin:0.5rem auto;line-height:1.5;">
                Staging environments are initialized. Your custom credentials and billing files have been compiled and sent to <strong>{st.session_state.form_data['email']}</strong>.
            </p>
            <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:1rem;padding:1rem;text-align:left;font-family:monospace;font-size:0.75rem;color:#334155;margin:1.5rem 0;">
                <div><strong>STAGING ID:</strong> #AFR-STAGE-{random.randint(10000, 99999)}</div>
                <div><strong>SERVICE:</strong> {st.session_state.selected_product['name']}</div>
                <div><strong>CLIENT:</strong> {st.session_state.form_data['name']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Enter ClientZone Sandbox", key="checkout_finish", use_container_width=True):
            st.session_state.selected_product = None
            st.session_state.current_tab = "clientzone"
            st.session_state.client_zone_sub_tab = "projects"
            st.rerun()

    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div style="background:#0f172a;color:white;padding:3rem 2rem 2rem 2rem;margin-top:3rem;border-top:4px solid #fbbf24;">
    <div style="max-width:1200px;margin:0 auto;display:grid;grid-template-columns:repeat(4,1fr);gap:2rem;">
        <div>
            <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:1rem;">
                <span style="background:#fbbf24;color:#022c22;font-weight:900;padding:0.25rem 0.75rem;border-radius:0.5rem;">A</span>
                <span style="font-weight:900;letter-spacing:0.05em;">AFRIHOST</span>
            </div>
            <p style="font-size:0.75rem;color:#94a3b8;line-height:1.5;">South Africa's elite decorated Web Studio and Cloud Hosting platform. Delivering robust hand-crafted portals and Anycast DNS cloud clusters since 1999.</p>
        </div>
        <div>
            <h4 style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.1em;color:#fbbf24;margin-bottom:1rem;font-family:monospace;">Studio Services</h4>
            <ul style="list-style:none;padding:0;font-size:0.75rem;color:#cbd5e1;line-height:2;">
                <li>Bespoke Design Layouts</li>
                <li>Headless CMS Integrations</li>
                <li>Domain DNS Registrations</li>
                <li>NVMe Cloud Hosting Tiers</li>
            </ul>
        </div>
        <div>
            <h4 style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.1em;color:#fbbf24;margin-bottom:1rem;font-family:monospace;">ClientZone Gateway</h4>
            <ul style="list-style:none;padding:0;font-size:0.75rem;color:#cbd5e1;line-height:2;">
                <li>Monitor Active Web Stages</li>
                <li>Server Health Overviews</li>
                <li>Dynamic DNS Caches</li>
                <li>Chat Web Architects</li>
            </ul>
        </div>
        <div>
            <h4 style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.1em;color:#fbbf24;margin-bottom:1rem;font-family:monospace;">Connect With Engineers</h4>
            <p style="font-size:0.75rem;color:#94a3b8;line-height:1.5;margin-bottom:1rem;">Our support team is online 24/7/365 with live human network engineers.</p>
            <span style="color:#fbbf24;font-size:1.25rem;">📞 📊 ⚙️</span>
        </div>
    </div>
    <div style="border-top:1px solid #1e293b;margin-top:2rem;padding-top:1.5rem;text-align:center;font-size:0.6rem;color:#64748b;font-family:monospace;letter-spacing:0.1em;">
        © 2026 AFRIHOST (PTY) LTD. ALL RIGHTS RESERVED. CLIENTZONE WEBENGINE v5.2.0.
    </div>
</div>
""", unsafe_allow_html=True)