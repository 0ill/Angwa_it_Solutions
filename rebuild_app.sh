#!/usr/bin/env bash
set -e

echo "==> Rebuilding ANGWA app from scratch"

# ----------------------------------------------------------------------
# 1. Create directories
# ----------------------------------------------------------------------
mkdir -p backend frontend pages utils tests .streamlit

# ----------------------------------------------------------------------
# 2. Write __init__.py files
# ----------------------------------------------------------------------
touch backend/__init__.py frontend/__init__.py utils/__init__.py

# ----------------------------------------------------------------------
# 3. Write backend/database.py (using the one from Step 3)
# ----------------------------------------------------------------------
cat > backend/database.py << 'PYEOF'
"""
backend/database.py – Turso data access layer
"""
import os
import json
import bcrypt
import libsql_client
from dotenv import load_dotenv
from typing import Optional, Any

load_dotenv()

_client = None

def _get_secret(key: str, default: Any = None) -> Any:
    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            try:
                return st.secrets[key]
            except KeyError:
                pass
    except Exception:
        pass
    return os.environ.get(key, default)

def get_client():
    global _client
    if _client is None:
        url = _get_secret("TURSO_URL")
        token = _get_secret("TURSO_TOKEN")
        if not url or not token:
            raise RuntimeError("TURSO_URL / TURSO_TOKEN not configured.")
        _client = libsql_client.create_client_sync(url, auth_token=token)
    return _client

def get_products(product_type: Optional[str] = None) -> list[dict]:
    client = get_client()
    if product_type:
        result = client.execute(
            "SELECT id, type, provider, name, speed_down, speed_up, price, is_popular, description FROM products WHERE type = ? ORDER BY price ASC",
            [product_type]
        )
    else:
        result = client.execute(
            "SELECT id, type, provider, name, speed_down, speed_up, price, is_popular, description FROM products ORDER BY type, price ASC"
        )
    products = []
    for row in result.rows:
        d = row.asdict()
        d["is_popular"] = bool(d["is_popular"])
        products.append(d)
    return products

def get_addons(product_type: Optional[str] = None) -> list[dict]:
    client = get_client()
    if product_type:
        result = client.execute(
            "SELECT id, product_type, name, price FROM addons WHERE product_type = ? ORDER BY price ASC",
            [product_type]
        )
    else:
        result = client.execute(
            "SELECT id, product_type, name, price FROM addons ORDER BY product_type, price ASC"
        )
    return [row.asdict() for row in result.rows]

def get_coverage_areas() -> list[dict]:
    client = get_client()
    result = client.execute("""
        SELECT id, area_name, city, province, status, provider, max_speed, infrastructure_ready, estimated_date
        FROM coverage_areas
        ORDER BY
            CASE status
                WHEN 'available' THEN 1
                WHEN 'coming_soon' THEN 2
                WHEN 'planned' THEN 3
            END, area_name
    """)
    areas = []
    for row in result.rows:
        d = row.asdict()
        d["infrastructure_ready"] = bool(d["infrastructure_ready"])
        areas.append(d)
    return areas

class EmailAlreadyExistsError(Exception):
    pass

def create_user(name: str, email: str, password: str) -> dict:
    client = get_client()
    email_norm = email.strip().lower()
    existing = client.execute("SELECT id FROM users WHERE email = ?", [email_norm])
    if existing.rows:
        raise EmailAlreadyExistsError(f"Email already registered: {email_norm}")
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    result = client.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        [name.strip(), email_norm, password_hash]
    )
    return {"id": result.last_insert_rowid, "name": name.strip(), "email": email_norm}

def get_user_by_email(email: str) -> Optional[dict]:
    client = get_client()
    result = client.execute(
        "SELECT id, name, email, password_hash, created_at FROM users WHERE email = ?",
        [email.strip().lower()]
    )
    if not result.rows:
        return None
    return result.rows[0].asdict()

def verify_user_password(email: str, password: str) -> Optional[dict]:
    user = get_user_by_email(email)
    if user is None:
        return None
    if bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
        return {"id": user["id"], "name": user["name"], "email": user["email"]}
    return None

def create_order(customer_name: str, customer_email: str, items: list[dict], subtotal: int,
                 customer_address: Optional[str] = None, currency: str = "ZAR",
                 user_id: Optional[int] = None, polar_checkout_id: Optional[str] = None) -> dict:
    client = get_client()
    items_json = json.dumps(items)
    result = client.execute(
        """INSERT INTO orders
           (user_id, customer_name, customer_email, customer_address,
            items_json, subtotal, currency, status, polar_checkout_id)
           VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?)""",
        [user_id, customer_name, customer_email, customer_address, items_json, subtotal, currency, polar_checkout_id]
    )
    return {"id": result.last_insert_rowid, "customer_name": customer_name, "customer_email": customer_email}
PYEOF
echo "✅ backend/database.py written"

# ----------------------------------------------------------------------
# 4. Write backend/schema.sql (full schema and seed)
# ----------------------------------------------------------------------
cat > backend/schema.sql << 'EOF'
-- ============================================================
-- ANGWA schema for Turso (libsql / SQLite dialect)
-- ============================================================

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS products (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    type            TEXT NOT NULL CHECK (type IN ('host','cloud','design')),
    provider        TEXT,
    name            TEXT NOT NULL,
    speed_down      INTEGER,
    speed_up        INTEGER,
    price           INTEGER NOT NULL,
    is_popular      INTEGER NOT NULL DEFAULT 0,
    description     TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_products_type ON products(type);

CREATE TABLE IF NOT EXISTS addons (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    product_type    TEXT NOT NULL,
    name            TEXT NOT NULL,
    price           INTEGER NOT NULL,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_addons_type ON addons(product_type);

CREATE TABLE IF NOT EXISTS coverage_areas (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    area_name               TEXT NOT NULL,
    city                    TEXT NOT NULL,
    province                TEXT NOT NULL,
    status                  TEXT NOT NULL CHECK (status IN ('available','coming_soon','planned')),
    provider                TEXT,
    max_speed               INTEGER,
    infrastructure_ready    INTEGER NOT NULL DEFAULT 0,
    estimated_date          TEXT,
    created_at              TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_coverage_status ON coverage_areas(status);

CREATE TABLE IF NOT EXISTS users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    email           TEXT NOT NULL UNIQUE,
    password_hash   TEXT NOT NULL,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

CREATE TABLE IF NOT EXISTS orders (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id             INTEGER REFERENCES users(id),
    customer_name       TEXT NOT NULL,
    customer_email      TEXT NOT NULL,
    customer_address    TEXT,
    items_json          TEXT NOT NULL,
    subtotal            INTEGER NOT NULL,
    currency            TEXT NOT NULL DEFAULT 'ZAR',
    status              TEXT NOT NULL DEFAULT 'pending'
                        CHECK (status IN ('pending','paid','failed','refunded','cancelled')),
    polar_checkout_id   TEXT,
    polar_order_id      TEXT,
    created_at          TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at          TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_orders_email ON orders(customer_email);
CREATE INDEX IF NOT EXISTS idx_orders_polar_checkout ON orders(polar_checkout_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);

CREATE TABLE IF NOT EXISTS webhook_events (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    polar_event_id      TEXT NOT NULL UNIQUE,
    event_type          TEXT NOT NULL,
    payload_json        TEXT NOT NULL,
    processed_at        TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Seed data
INSERT INTO products (type, provider, name, speed_down, speed_up, price, is_popular, description)
SELECT 'host', 'Openserve', 'Fibre 50/50', 50, 50, 69900, 0, 'Symmetrical 50Mbps fibre line, ideal for browsing and streaming.'
WHERE NOT EXISTS (SELECT 1 FROM products WHERE type='host' AND name='Fibre 50/50');

INSERT INTO products (type, provider, name, speed_down, speed_up, price, is_popular, description)
SELECT 'host', 'Openserve', 'Fibre 100/100', 100, 100, 89900, 1, 'Symmetrical 100Mbps fibre line, great for households with multiple devices.'
WHERE NOT EXISTS (SELECT 1 FROM products WHERE type='host' AND name='Fibre 100/100');

INSERT INTO products (type, provider, name, speed_down, speed_up, price, is_popular, description)
SELECT 'host', 'Vumatel', 'Fibre 200/200', 200, 200, 129900, 0, 'Symmetrical 200Mbps fibre line for power users and small offices.'
WHERE NOT EXISTS (SELECT 1 FROM products WHERE type='host' AND name='Fibre 200/200');

INSERT INTO products (type, name, price, is_popular, description)
SELECT 'cloud', 'Cloud Storage Lite (100GB)', 4900, 0, 'Secure encrypted cloud backup with 100GB of storage.'
WHERE NOT EXISTS (SELECT 1 FROM products WHERE type='cloud' AND name='Cloud Storage Lite (100GB)');

INSERT INTO products (type, name, price, is_popular, description)
SELECT 'cloud', 'Cloud Storage Pro (500GB)', 9900, 1, 'Secure encrypted cloud backup with 500GB of storage and faster sync speeds.'
WHERE NOT EXISTS (SELECT 1 FROM products WHERE type='cloud' AND name='Cloud Storage Pro (500GB)');

INSERT INTO products (type, name, price, is_popular, description)
SELECT 'design', 'Obsidian Luxe', 899900, 1, 'Cinematic luxury layout with gold obsidian accents for premium brands.'
WHERE NOT EXISTS (SELECT 1 FROM products WHERE type='design' AND name='Obsidian Luxe');

INSERT INTO products (type, name, price, is_popular, description)
SELECT 'design', 'Neo Tech Emerald', 699900, 0, 'High-tech neon architecture, ideal for software and gaming brands.'
WHERE NOT EXISTS (SELECT 1 FROM products WHERE type='design' AND name='Neo Tech Emerald');

INSERT INTO products (type, name, price, is_popular, description)
SELECT 'design', 'Alabaster Minimal', 499900, 0, 'Clean, crisp, minimalist layout for extreme legibility and e-commerce elegance.'
WHERE NOT EXISTS (SELECT 1 FROM products WHERE type='design' AND name='Alabaster Minimal');

INSERT INTO addons (product_type, name, price)
SELECT 'host', 'Static IP Address', 4900
WHERE NOT EXISTS (SELECT 1 FROM addons WHERE product_type='host' AND name='Static IP Address');

INSERT INTO addons (product_type, name, price)
SELECT 'host', 'Wi-Fi 6 Router Rental', 9900
WHERE NOT EXISTS (SELECT 1 FROM addons WHERE product_type='host' AND name='Wi-Fi 6 Router Rental');

INSERT INTO addons (product_type, name, price)
SELECT 'design', 'Logo Design Package', 149900
WHERE NOT EXISTS (SELECT 1 FROM addons WHERE product_type='design' AND name='Logo Design Package');

INSERT INTO coverage_areas (area_name, city, province, status, provider, max_speed, infrastructure_ready, estimated_date)
SELECT 'Sandton CBD', 'Johannesburg', 'Gauteng', 'available', 'Vumatel', 1000, 1, NULL
WHERE NOT EXISTS (SELECT 1 FROM coverage_areas WHERE area_name='Sandton CBD');

INSERT INTO coverage_areas (area_name, city, province, status, provider, max_speed, infrastructure_ready, estimated_date)
SELECT 'Century City', 'Cape Town', 'Western Cape', 'available', 'Openserve', 1000, 1, NULL
WHERE NOT EXISTS (SELECT 1 FROM coverage_areas WHERE area_name='Century City');

INSERT INTO coverage_areas (area_name, city, province, status, provider, max_speed, infrastructure_ready, estimated_date)
SELECT 'Hatfield', 'Pretoria', 'Gauteng', 'coming_soon', 'Vumatel', 500, 0, '2026-09-01'
WHERE NOT EXISTS (SELECT 1 FROM coverage_areas WHERE area_name='Hatfield');

INSERT INTO coverage_areas (area_name, city, province, status, provider, max_speed, infrastructure_ready, estimated_date)
SELECT 'Kroonstad Central', 'Kroonstad', 'Free State', 'planned', 'Openserve', 200, 0, '2027-01-01'
WHERE NOT EXISTS (SELECT 1 FROM coverage_areas WHERE area_name='Kroonstad Central');
EOF
echo "✅ backend/schema.sql written"

# ----------------------------------------------------------------------
# 5. Write frontend page modules (with the HTML you provided)
# ----------------------------------------------------------------------
# home.py
cat > frontend/home.py << 'PYEOF'
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
PYEOF

# host.py (abbreviated – you provided the full content; I'll include it all)
# To keep the script manageable, I'll include the full HTML from your earlier message.
# I'll use a here-doc with the exact content.

cat > frontend/host.py << 'PYEOF'
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
PYEOF

# design.py
cat > frontend/design.py << 'PYEOF'
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
PYEOF

# cloud.py
cat > frontend/cloud.py << 'PYEOF'
def get_cloud_html():
    return """
<!-- ==================== PAGE: CLOUD ==================== -->
<div id="page-cloud" class="page-view hidden">

<!-- Cloud Hero Section -->
<section class="relative bg-gradient-to-br from-brand-black via-brand-slateBlack to-brand-black text-white overflow-hidden py-20 border-b border-white/10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10"><div class="inline-flex items-center gap-2 bg-white/5 border border-white/10 px-4 py-2 rounded-full text-brand-gold text-xs font-medium tracking-widest uppercase mb-6">ANGWA Cloud Vault</div><h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight">Symmetrical <span class="text-transparent bg-clip-text bg-gradient-to-r from-brand-gold to-brand-goldLight">Cloud-Filling</span></h1><p class="mt-4 text-gray-400 max-w-2xl mx-auto">Military-grade encrypted storage with identical upload/download speeds via our fibre backbone. Sync massive datasets, collaborate in real-time, and keep your data safe on South African servers.</p><div class="flex flex-wrap justify-center gap-4 mt-8"><a href="#cloud-storage" class="glossy-gold text-brand-black px-7 py-3 rounded-full font-bold text-xs uppercase tracking-wider shadow-md">View Storage Plans</a><a href="#cloud-filling" class="glossy-green text-white px-7 py-3 rounded-full font-bold text-xs uppercase tracking-wider shadow-md">Test Sync Pipeline</a></div></div>
</section>

<!-- Cloud Filling Interactive Pipeline -->
<section id="cloud-filling" class="py-20 bg-brand-black text-white relative border-b border-white/10">
    <div class="absolute inset-0 pointer-events-none opacity-20"><div class="absolute top-1/4 right-1/4 w-[400px] h-[400px] bg-brand-gold rounded-full filter blur-[150px] animate-pulse"></div></div>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div class="grid lg:grid-cols-12 gap-12 items-center">
            <div class="lg:col-span-5 space-y-6 text-center lg:text-left"><div class="inline-flex items-center gap-2 bg-white/5 border border-white/10 px-4 py-2 rounded-full text-brand-gold text-xs font-medium tracking-widest uppercase"><i class="fa-solid fa-cloud-arrow-up"></i> Service 03: Cloud Filling</div><h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight">Upstream Spliced <br><span class="text-transparent bg-clip-text bg-gradient-to-r from-brand-gold via-brand-goldLight to-brand-goldDark">Cloud-Filling Grid.</span></h2><p class="text-sm text-gray-400 leading-relaxed">Say goodbye to sluggish cloud sync delays. With ANGWA's symmetrical fiber lines, uploads run at identical speeds to your downloads. Instantly map, sync, and deploy media directories directly to external storage platforms.</p><div class="space-y-3.5 text-xs text-gray-300"><div class="flex items-center gap-3"><i class="fa-brands fa-dropbox text-blue-400 text-lg"></i><span>Dropbox Integration: Automated multi-thread background uploads.</span></div><div class="flex items-center gap-3"><i class="fa-brands fa-google-drive text-green-400 text-lg"></i><span>Google Drive Integration: Smooth file splicing and real-time handshakes.</span></div></div></div>
            <div class="lg:col-span-7"><div class="glass-dark rounded-3xl p-6 sm:p-8 border border-white/10 relative overflow-hidden shadow-2xl"><div class="flex items-center justify-between mb-6 pb-4 border-b border-white/5"><div><h4 class="font-bold text-sm">Direct-To-Cloud Filling Terminal</h4><p class="text-[10px] text-gray-500">Live test connection speed metrics</p></div><span class="text-[10px] bg-brand-green/10 text-brand-green border border-brand-green/20 px-2.5 py-1 rounded-full uppercase font-bold tracking-wider"><i class="fa-solid fa-link animate-pulse"></i> Symmetrical Active</span></div><div class="bg-black/40 rounded-2xl p-6 border border-white/5 space-y-5"><div class="flex items-center justify-between text-xs"><span class="text-gray-400">Target Server Connection</span><div class="flex gap-2"><button onclick="triggerCloudSync('dropbox')" class="bg-blue-500/20 hover:bg-blue-500 text-blue-400 hover:text-white transition-all text-[10px] font-bold tracking-wide px-3 py-1.5 rounded-lg flex items-center gap-1"><i class="fa-brands fa-dropbox"></i> Dropbox</button><button onclick="triggerCloudSync('google')" class="bg-green-500/20 hover:bg-green-500 text-green-400 hover:text-white transition-all text-[10px] font-bold tracking-wide px-3 py-1.5 rounded-lg flex items-center gap-1"><i class="fa-brands fa-google-drive"></i> Google Drive</button></div></div><div class="space-y-2"><div class="flex justify-between text-[10px] font-mono text-gray-500 uppercase"><span>Sync Transmission Rate:</span><span class="text-brand-green font-bold" id="panel-sync-rate">0 Mbps</span></div><div class="w-full bg-brand-slateBlack h-2.5 rounded-full overflow-hidden border border-white/5 relative"><div id="panel-progress-bar" class="bg-gradient-to-r from-brand-gold to-brand-green h-full rounded-full transition-all duration-300" style="width: 0%"></div></div><div class="flex justify-between text-[9px] text-gray-500"><span id="panel-sync-status">Inactive - Select pipeline platform to initiate sync</span><span id="panel-sync-timer"></span></div></div></div><div class="mt-5 text-center text-[10px] text-gray-500 flex items-center justify-center gap-2"><i class="fa-solid fa-network-wired text-brand-gold"></i><span>Bypasses local ISP throttling locks completely.</span></div></div></div>
        </div>
    </div>
</section>

<!-- Cloud Storage Vault Plans (Dynamic) -->
<section id="cloud-storage" class="py-20 bg-brand-lightBg relative overflow-hidden border-t border-black/5">
    <div class="absolute top-0 right-0 w-[500px] h-[500px] bg-brand-gold/5 rounded-full filter blur-[160px] pointer-events-none"></div>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div class="text-center max-w-3xl mx-auto mb-16 space-y-4"><span class="text-brand-gold uppercase font-black tracking-widest text-xs px-3.5 py-1 bg-brand-gold/10 rounded-full inline-block">ANGWA Secure Cloud Storage</span><h2 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-brand-black">ANGWA Cloud Vault Plans</h2><p class="text-gray-500 text-sm leading-relaxed">Military-grade encrypted storage powered by our symmetrical fibre backbone. Upload, sync, and access at full gigabit speeds — all data hosted on South African servers.</p><div class="flex flex-wrap justify-center gap-3 pt-2"><span class="flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wider text-gray-500 bg-white border border-black/5 px-3.5 py-1.5 rounded-full shadow-sm"><i class="fa-solid fa-shield-halved text-brand-gold"></i> AES-256 Encrypted</span><span class="flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wider text-gray-500 bg-white border border-black/5 px-3.5 py-1.5 rounded-full shadow-sm"><i class="fa-solid fa-bolt text-brand-gold"></i> Fibre-Speed Sync</span><span class="flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wider text-gray-500 bg-white border border-black/5 px-3.5 py-1.5 rounded-full shadow-sm"><i class="fa-solid fa-rotate text-brand-gold"></i> Auto Backup</span><span class="flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wider text-gray-500 bg-white border border-black/5 px-3.5 py-1.5 rounded-full shadow-sm"><i class="fa-solid fa-server text-brand-gold"></i> SA-Based Servers</span></div></div>
        <div id="cloud-plans-container" class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6"></div>
    </div>
</section>

<!-- Cloud Integrations & Security -->
<section class="py-20 bg-brand-slateBlack text-white border-t border-white/10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid md:grid-cols-2 gap-12 items-center"><div><h2 class="text-2xl font-extrabold">Integrated with Leading Platforms</h2><p class="text-sm text-gray-400 mt-2">Seamlessly sync your Dropbox, Google Drive, and custom S3 buckets with our symmetrical backbone. No throttling, instant file availability.</p><ul class="mt-4 space-y-2 text-xs"><li class="flex items-center gap-2"><i class="fa-regular fa-circle-check text-brand-green"></i> Real-time file versioning & restore</li><li class="flex items-center gap-2"><i class="fa-regular fa-circle-check text-brand-green"></i> Zero-knowledge encryption optional</li><li class="flex items-center gap-2"><i class="fa-regular fa-circle-check text-brand-green"></i> 24/7 dedicated cloud support</li></ul></div><div class="glass-dark p-6 rounded-2xl"><div class="text-brand-gold text-5xl mb-4"><i class="fa-solid fa-shield-halved"></i></div><h3 class="font-bold text-white">SOC 2 Type II Compliant</h3><p class="text-xs text-gray-400 mt-1">All data encrypted at rest and in transit. Hosted in ISO 27001 certified data centers within South Africa.</p></div></div></div>
</section>

<!-- Support & FAQs Section (Cloud Page) -->
<section id="faq" class="py-20 bg-brand-lightBg">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8"><div class="text-center mb-16 space-y-4"><span class="text-brand-goldDark uppercase font-black tracking-widest text-xs px-3.5 py-1 bg-brand-gold/10 rounded-full">Help & Support</span><h2 class="text-3xl font-bold tracking-tight text-brand-black">Fibre FAQ Knowledge-Base</h2><p class="text-gray-500 text-xs">Everything you need to know about setting up ANGWA Fibre.</p></div><div class="space-y-4"><div class="bg-white border border-black/5 rounded-2xl overflow-hidden shadow-sm"><button class="w-full px-6 py-4.5 text-left font-bold text-sm flex items-center justify-between text-brand-black hover:text-brand-goldDark transition-colors" onclick="toggleFaq(this)"><span>How long is the typical installation cycle?</span><i class="fa-solid fa-chevron-down transition-transform"></i></button><div class="px-6 pb-5 text-xs text-gray-500 hidden leading-relaxed border-t border-black/5 pt-4">After ordering, the designated carrier infrastructure partner (Openserve, Vumatel, Frogfoot, etc.) will schedule your installation date. Connection takes 2-5 working days depending on setup dynamics.</div></div><div class="bg-white border border-black/5 rounded-2xl overflow-hidden shadow-sm"><button class="w-full px-6 py-4.5 text-left font-bold text-sm flex items-center justify-between text-brand-black hover:text-brand-goldDark transition-colors" onclick="toggleFaq(this)"><span>Are there hidden administration fees?</span><i class="fa-solid fa-chevron-down transition-transform"></i></button><div class="px-6 pb-5 text-xs text-gray-500 hidden leading-relaxed border-t border-black/5 pt-4">Absolutely zero. All connection logistics, fiber equipment setup fees, and baseline Wi-Fi 6 hardware distribution options are completely pre-paid by us.</div></div><div class="bg-white border border-black/5 rounded-2xl overflow-hidden shadow-sm"><button class="w-full px-6 py-4.5 text-left font-bold text-sm flex items-center justify-between text-brand-black hover:text-brand-goldDark transition-colors" onclick="toggleFaq(this)"><span>How does the double money-back guarantee work?</span><i class="fa-solid fa-chevron-down transition-transform"></i></button><div class="px-6 pb-5 text-xs text-gray-500 hidden leading-relaxed border-t border-black/5 pt-4">If you are unsatisfied with connection speeds, drop rates, or support queues within the initial 30 days of setup, notify us. We'll terminate the line and issue a complete premium refund, doubled.</div></div><div class="bg-white border border-black/5 rounded-2xl overflow-hidden shadow-sm"><button class="w-full px-6 py-4.5 text-left font-bold text-sm flex items-center justify-between text-brand-black hover:text-brand-goldDark transition-colors" onclick="toggleFaq(this)"><span>What termination terms are applicable?</span><i class="fa-solid fa-chevron-down transition-transform"></i></button><div class="px-6 pb-5 text-xs text-gray-500 hidden leading-relaxed border-t border-black/5 pt-4">Our packages are based on calendar-month schedules. Simply submit a cancellation notice 30 days prior. Hardware must be returned within 14 business days of line termination.</div></div></div></div>
</section>

</div><!-- END page-cloud -->
"""
PYEOF

# clientzone.py
cat > frontend/clientzone.py << 'PYEOF'
def get_clientzone_html():
    return """
<!-- ClientZone Modal (Login + Portal) -->
<div id="clientzone-modal" class="fixed inset-0 z-50 overflow-y-auto hidden" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-center justify-center min-h-screen p-4">
        <div class="fixed inset-0 bg-brand-black/80 backdrop-blur-md transition-opacity" onclick="closeClientZone()"></div>
        <div class="bg-brand-slateBlack text-white rounded-3xl max-w-4xl w-full border border-white/10 relative z-10 shadow-2xl max-h-[90vh] overflow-y-auto">
            
            <!-- LOGIN VIEW (visible by default) -->
            <div id="cz-login-view" class="p-6 space-y-6">
                <div class="text-center space-y-2">
                    <div class="h-14 w-14 bg-brand-gold/10 text-brand-gold rounded-full flex items-center justify-center text-2xl mx-auto"><i class="fa-solid fa-user-shield"></i></div>
                    <h4 class="font-bold text-2xl text-white">ANGWA ClientZone</h4>
                    <p class="text-xs text-gray-400">Sign in to manage your services</p>
                </div>
                <div class="space-y-4 text-xs max-w-sm mx-auto">
                    <div>
                        <label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Email address</label>
                        <input type="email" id="cz-email" placeholder="client@example.com" class="w-full px-4 py-2.5 bg-brand-darkGray border border-white/10 rounded-xl text-white focus:ring-2 focus:ring-brand-gold">
                    </div>
                    <div>
                        <label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Password</label>
                        <input type="password" id="cz-password" placeholder="••••••••" class="w-full px-4 py-2.5 bg-brand-darkGray border border-white/10 rounded-xl text-white focus:ring-2 focus:ring-brand-gold">
                    </div>
                    <button onclick="submitClientZone()" class="w-full glossy-gold text-brand-black py-3 rounded-full font-bold uppercase tracking-wider text-xs">Sign in</button>
                    <div class="text-center text-[9px] text-gray-500">
                        No account? <button onclick="closeClientZone(); openRegisterModal()" class="text-brand-gold hover:underline">Create one</button>
                    </div>
                </div>
            </div>

            <!-- PORTAL VIEW (hidden until login) -->
            <div id="cz-portal-view" class="hidden p-6">
                <!-- Portal Header -->
                <div class="flex items-center justify-between border-b border-white/10 pb-4 mb-4">
                    <div class="flex items-center gap-3">
                        <div class="h-10 w-10 bg-brand-gold/15 rounded-full flex items-center justify-center text-brand-gold text-lg"><i class="fa-solid fa-user"></i></div>
                        <div>
                            <div class="font-bold text-white text-sm" id="cz-user-name">User</div>
                            <div class="text-[10px] text-gray-400" id="cz-user-email">user@example.com</div>
                        </div>
                    </div>
                    <button onclick="logoutClientZone()" class="text-xs text-gray-400 hover:text-red-400 transition-colors"><i class="fa-solid fa-sign-out-alt mr-1"></i> Logout</button>
                </div>

                <!-- Tabs -->
                <div class="flex border-b border-white/10 mb-6 text-xs font-bold uppercase tracking-wider">
                    <button class="cz-tab-btn px-4 py-2 text-brand-gold border-b-2 border-brand-gold" data-tab="dashboard">Dashboard</button>
                    <button class="cz-tab-btn px-4 py-2 text-gray-400 hover:text-white border-b-2 border-transparent" data-tab="orders">Orders</button>
                    <button class="cz-tab-btn px-4 py-2 text-gray-400 hover:text-white border-b-2 border-transparent" data-tab="profile">Profile</button>
                    <button class="cz-tab-btn px-4 py-2 text-gray-400 hover:text-white border-b-2 border-transparent" data-tab="support">Support</button>
                </div>

                <!-- Tab Content -->
                <div id="cz-tab-content" class="text-sm">
                    <!-- Dashboard -->
                    <div id="cz-dashboard" class="cz-tab-panel">
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                            <div class="bg-brand-darkGray/40 p-4 rounded-xl border border-white/5">
                                <div class="text-gray-400 text-[10px] uppercase">Active Services</div>
                                <div class="text-2xl font-bold text-brand-gold" id="cz-service-count">3</div>
                            </div>
                            <div class="bg-brand-darkGray/40 p-4 rounded-xl border border-white/5">
                                <div class="text-gray-400 text-[10px] uppercase">Total Orders</div>
                                <div class="text-2xl font-bold text-white" id="cz-order-count">5</div>
                            </div>
                            <div class="bg-brand-darkGray/40 p-4 rounded-xl border border-white/5">
                                <div class="text-gray-400 text-[10px] uppercase">Support Tickets</div>
                                <div class="text-2xl font-bold text-brand-green" id="cz-ticket-count">2</div>
                            </div>
                        </div>
                        <div class="bg-brand-darkGray/30 p-4 rounded-xl border border-white/5">
                            <h5 class="font-bold text-sm mb-2">Recent Activity</h5>
                            <ul class="space-y-2 text-xs text-gray-400">
                                <li class="flex justify-between border-b border-white/5 pb-2"><span>Order #1234 – Fibre 100Mbps</span><span class="text-brand-green">Completed</span></li>
                                <li class="flex justify-between border-b border-white/5 pb-2"><span>Order #1235 – Design Luxe</span><span class="text-brand-gold">In Progress</span></li>
                                <li class="flex justify-between"><span>Support ticket #56 – Billing</span><span class="text-gray-500">Open</span></li>
                            </ul>
                        </div>
                    </div>

                    <!-- Orders -->
                    <div id="cz-orders" class="cz-tab-panel hidden">
                        <div class="bg-brand-darkGray/30 p-4 rounded-xl border border-white/5">
                            <h5 class="font-bold text-sm mb-3">Order History</h5>
                            <div id="cz-orders-list" class="space-y-3 text-xs">
                                <!-- Dynamic orders will be inserted here -->
                                <div class="text-gray-400">Loading orders...</div>
                            </div>
                        </div>
                    </div>

                    <!-- Profile -->
                    <div id="cz-profile" class="cz-tab-panel hidden">
                        <div class="bg-brand-darkGray/30 p-4 rounded-xl border border-white/5 space-y-4">
                            <h5 class="font-bold text-sm">Edit Profile</h5>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                                <div>
                                    <label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Full Name</label>
                                    <input type="text" id="cz-profile-name" placeholder="Your name" class="w-full px-3 py-2 bg-brand-darkGray border border-white/10 rounded-lg text-white focus:ring-1 focus:ring-brand-gold">
                                </div>
                                <div>
                                    <label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Email</label>
                                    <input type="email" id="cz-profile-email" placeholder="email@example.com" class="w-full px-3 py-2 bg-brand-darkGray border border-white/10 rounded-lg text-white focus:ring-1 focus:ring-brand-gold" disabled>
                                </div>
                                <div>
                                    <label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Phone</label>
                                    <input type="tel" id="cz-profile-phone" placeholder="+27 12 345 6789" class="w-full px-3 py-2 bg-brand-darkGray border border-white/10 rounded-lg text-white focus:ring-1 focus:ring-brand-gold">
                                </div>
                                <div>
                                    <label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Address</label>
                                    <input type="text" id="cz-profile-address" placeholder="Your address" class="w-full px-3 py-2 bg-brand-darkGray border border-white/10 rounded-lg text-white focus:ring-1 focus:ring-brand-gold">
                                </div>
                            </div>
                            <button onclick="saveProfile()" class="glossy-gold text-brand-black px-6 py-2 rounded-full font-bold text-[10px] uppercase tracking-wider">Save Changes</button>
                        </div>
                    </div>

                    <!-- Support -->
                    <div id="cz-support" class="cz-tab-panel hidden">
                        <div class="bg-brand-darkGray/30 p-4 rounded-xl border border-white/5 space-y-4">
                            <h5 class="font-bold text-sm">Contact Support</h5>
                            <div class="space-y-3 text-xs">
                                <div>
                                    <label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Subject</label>
                                    <input type="text" id="cz-support-subject" placeholder="Brief issue summary" class="w-full px-3 py-2 bg-brand-darkGray border border-white/10 rounded-lg text-white focus:ring-1 focus:ring-brand-gold">
                                </div>
                                <div>
                                    <label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Message</label>
                                    <textarea id="cz-support-message" rows="4" placeholder="Describe your issue..." class="w-full px-3 py-2 bg-brand-darkGray border border-white/10 rounded-lg text-white focus:ring-1 focus:ring-brand-gold"></textarea>
                                </div>
                                <button onclick="submitSupportTicket()" class="glossy-green text-white px-6 py-2 rounded-full font-bold text-[10px] uppercase tracking-wider">Submit Ticket</button>
                            </div>
                            <div class="border-t border-white/10 pt-4 mt-4">
                                <h6 class="font-bold text-xs mb-2">Recent Tickets</h6>
                                <ul id="cz-support-tickets" class="space-y-2 text-xs text-gray-400">
                                    <li class="flex justify-between"><span>#56 – Billing issue</span><span class="text-brand-gold">Open</span></li>
                                    <li class="flex justify-between"><span>#55 – Installation delay</span><span class="text-brand-green">Resolved</span></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Close button (visible in both views) -->
            <div class="absolute top-4 right-4">
                <button onclick="closeClientZone()" class="text-gray-400 hover:text-white text-xl"><i class="fa-solid fa-circle-xmark"></i></button>
            </div>
        </div>
    </div>
</div>
"""
PYEOF

echo "✅ Frontend modules written"

# ----------------------------------------------------------------------
# 6. Write app.py (with correct imports and full HTML shell)
# ----------------------------------------------------------------------
cat > app.py << 'PYEOF'
import streamlit as st
import streamlit.components.v1 as components
import libsql_client
import json
from frontend import home, host, design, cloud, clientzone

# ---------- Turso Connection ----------
@st.cache_resource
def get_turso_connection():
    url = st.secrets["TURSO_URL"]
    token = st.secrets["TURSO_TOKEN"]
    return libsql_client.create_client_sync(url, auth_token=token)

def fetch_products():
    client = get_turso_connection()
    host_rows = client.execute("SELECT id, provider, name, speed_down, speed_up, price, is_popular, description FROM products WHERE type = 'host'").rows
    package_data = []
    for row in host_rows:
        package_data.append({
            "id": row[0],
            "provider": row[1],
            "name": row[2],
            "down": row[3],
            "up": row[4],
            "price": row[5] // 100,
            "isPopular": bool(row[6]),
            "description": row[7]
        })
    cloud_rows = client.execute("SELECT id, name, price, is_popular, description FROM products WHERE type = 'cloud'").rows
    cloud_data = []
    for row in cloud_rows:
        storage = row[1].split('(')[-1].replace(')', '') if '(' in row[1] else ""
        cloud_data.append({
            "id": row[0],
            "name": row[1],
            "storage": storage,
            "price": row[2] // 100,
            "isPopular": bool(row[3]),
            "description": row[4]
        })
    design_rows = client.execute("SELECT id, name, price, is_popular, description FROM products WHERE type = 'design'").rows
    design_data = {}
    for row in design_rows:
        name_lower = row[1].lower()
        if "luxe" in name_lower:
            key = "luxe"
            logo_text = "OBSIDIAN."
            logo_class = "text-brand-gold"
            badge_text = "Cinematic Luxury Layout"
            badge_class = "bg-brand-gold/10 text-brand-gold border-brand-gold/20"
            title = "Slick. Cinematic.<br><span class='text-brand-gold'>Gold Obsidian Accent.</span>"
            desc = "Designed with luxury aesthetics. Highly interactive bento architecture mapped for corporate powerbrands and creatives."
            time_text = "4-6 Business Days Delivery"
            btn_class = "glossy-gold text-brand-black"
            viewport_bg = "bg-black text-white border border-brand-gold/20"
        elif "emerald" in name_lower:
            key = "emerald"
            logo_text = "NEO TECH."
            logo_class = "text-brand-green"
            badge_text = "High Tech Neon Architecture"
            badge_class = "bg-brand-green/10 text-brand-green border-brand-green/20"
            title = "Fast. Minimalist.<br><span class='text-brand-green'>Futuristic Tech Splicing.</span>"
            desc = "An advanced neon layout structured with high-tech coding styles. Ideal for software platforms and gaming setups."
            time_text = "3-5 Business Days Delivery"
            btn_class = "glossy-green text-white"
            viewport_bg = "bg-[#0d0d0e] text-white border border-brand-green/20"
        else:
            key = "minimal"
            logo_text = "ALABASTER."
            logo_class = "text-white"
            badge_text = "Fluid Minimalist Canvas"
            badge_class = "bg-white/10 text-white border-white/20"
            title = "Clean. Crisp.<br><span class='text-gray-300'>Alabaster Structure.</span>"
            desc = "Clean light elements over a solid gray grid. Designed for extreme legibility, crisp typography, and e-commerce elegance."
            time_text = "5-7 Business Days Delivery"
            btn_class = "glossy-black text-white"
            viewport_bg = "bg-white text-brand-slateBlack border border-black/10"
        design_data[key] = {
            "id": f"design-{key}",
            "price": row[2] // 100,
            "logoText": logo_text,
            "logoClass": logo_class,
            "badgeText": badge_text,
            "badgeClass": badge_class,
            "title": title,
            "desc": desc,
            "timeText": time_text,
            "btnClass": btn_class,
            "viewportBg": viewport_bg
        }
    addon_rows = client.execute("SELECT product_type, name, price FROM addons").rows
    addon_data = {}
    for row in addon_rows:
        ptype = row[0]
        name = row[1]
        price_rand = row[2] // 100
        if ptype not in addon_data:
            addon_data[ptype] = []
        addon_data[ptype].append({"name": name, "price": price_rand})
    return package_data, cloud_data, design_data, addon_data

def fetch_coverage_areas():
    client = get_turso_connection()
    rows = client.execute("""
        SELECT area_name, city, province, status, provider, max_speed, infrastructure_ready, estimated_date
        FROM coverage_areas
        ORDER BY 
            CASE status 
                WHEN 'available' THEN 1 
                WHEN 'coming_soon' THEN 2 
                WHEN 'planned' THEN 3 
            END, area_name
    """).rows
    coverage_data = []
    for row in rows:
        coverage_data.append({
            "name": row[0],
            "city": row[1],
            "province": row[2],
            "status": row[3],
            "provider": row[4],
            "max_speed": row[5],
            "infrastructure_ready": bool(row[6]) if row[6] is not None else False,
            "estimated_date": row[7]
        })
    return coverage_data

package_data, cloud_data, design_data, addon_data = fetch_products()
coverage_data = fetch_coverage_areas()

package_json = json.dumps(package_data)
cloud_json = json.dumps(cloud_data)
design_json = json.dumps(design_data)
addon_json = json.dumps(addon_data)
coverage_json = json.dumps(coverage_data)

api_base_url = st.secrets.get("API_BASE_URL", "https://your-app.onrender.com")

st.set_page_config(
    page_title="ANGWA | Symmetrical Pure Light Fibre",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        [data-testid="stHeader"], .stAppHeader, footer, .viewerBadge, [data-testid="stDecoration"] {
            display: none !important;
            height: 0 !important;
            width: 0 !important;
        }
        .stApp {
            padding: 0 !important;
            margin: 0 !important;
            background-color: #000000 !important;
            overflow: hidden !important;
            width: 100vw !important;
            height: 100vh !important;
        }
        .main .block-container {
            padding: 0 !important;
            max-width: 100vw !important;
            max-height: 100vh !important;
            margin: 0 !important;
            display: flex !important;
            flex-direction: column !important;
            flex: 1 !important;
        }
        [data-testid="stAppViewContainer"] { padding: 0 !important; }
        [data-testid="stAppViewBlockContainer"] { padding: 0 !important; }
        [data-testid="stMain"] { padding: 0 !important; }
        [data-testid="stMainBlockContainer"] {
            padding: 0 !important;
            margin: 0 !important;
            max-width: none !important;
            max-height: none !important;
            width: 100% !important;
        }
        iframe {
            border: none !important;
            display: block;
            width: 100% !important;
            height: 100vh !important;
        }
    </style>
""", unsafe_allow_html=True)

html_content = f"""
<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
    <title>ANGWA | Symmetrical Pure Light Fibre</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        brand: {{
                            black: '#000000',
                            slateBlack: '#0D0D0E',
                            darkGray: '#1C1C1E',
                            gold: '#D4AF37',
                            goldLight: '#F3E5AB',
                            goldDark: '#AA7C11',
                            green: '#30D158',
                            greenDark: '#248A36',
                            white: '#FFFFFF',
                            lightBg: '#F5F5F7'
                        }}
                    }},
                    fontFamily: {{
                        sans: ['SF Pro Display', '-apple-system', 'BlinkMacSystemFont', 'Inter', 'sans-serif'],
                    }}
                }}
            }}
        }}
    </script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script defer data-auto-init src="https://cdn.jsdelivr.net/npm/@polar-sh/checkout@latest/dist/embed.global.js"></script>
    <style>
        body {{ font-family: 'Inter', -apple-system, sans-serif; background-color: #F5F5F7; }}
        .glass-dark {{ background: rgba(22, 22, 23, 0.75); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); }}
        .glass-light {{ background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(20px); border: 1px solid rgba(0, 0, 0, 0.06); }}
        .glossy-gold {{
            background: linear-gradient(180deg, #F9E7B9 0%, #D4AF37 40%, #A37F1A 100%);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.4), 0 4px 15px rgba(212, 175, 55, 0.35);
            text-shadow: 0 1px 1px rgba(0, 0, 0, 0.15);
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .glossy-gold:hover {{
            background: linear-gradient(180deg, #FFF0D0 0%, #E5C158 40%, #B89326 100%);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.5), 0 6px 20px rgba(212, 175, 55, 0.5);
            transform: translateY(-1px);
        }}
        .glossy-green {{
            background: linear-gradient(180deg, #34E065 0%, #30D158 50%, #22993F 100%);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.4), 0 4px 15px rgba(48, 209, 88, 0.3);
            text-shadow: 0 1px 1px rgba(0, 0, 0, 0.15);
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .glossy-green:hover {{
            background: linear-gradient(180deg, #4AF078 0%, #39E067 50%, #2AA849 100%);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.5), 0 6px 20px rgba(48, 209, 88, 0.45);
            transform: translateY(-1px);
        }}
        .glossy-black {{
            background: linear-gradient(180deg, #3A3A3C 0%, #1C1C1E 50%, #000000 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.15), 0 4px 12px rgba(0, 0, 0, 0.4);
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .glossy-black:hover {{
            background: linear-gradient(180deg, #4A4A4C 0%, #2C2C2E 50%, #101012 100%);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.25), 0 6px 18px rgba(0, 0, 0, 0.5);
            transform: translateY(-1px);
        }}
        @keyframes sweep {{
            0% {{ transform: translateX(-100%) rotate(30deg); }}
            100% {{ transform: translateX(300%) rotate(30deg); }}
        }}
        .sheen-effect::after {{
            content: '';
            position: absolute;
            top: -50%;
            left: -60%;
            width: 30%;
            height: 200%;
            background: linear-gradient(to right, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0.3) 50%, rgba(255, 255, 255, 0) 100%);
            transform: rotate(30deg);
            animation: sweep 4.5s infinite ease-in-out;
        }}
        .gold-sheen-border {{ border: 1px solid rgba(212, 175, 55, 0.3); box-shadow: 0 0 25px rgba(212, 175, 55, 0.08); }}
        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-track {{ background: #000000; }}
        ::-webkit-scrollbar-thumb {{ background: rgba(255, 255, 255, 0.25); border-radius: 10px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: rgba(212, 175, 55, 0.6); }}
        @keyframes bounce-small {{ 0%,100% {{ transform: scale(1); }} 50% {{ transform: scale(1.2); }} }}
        .cart-bounce {{ animation: bounce-small 0.4s ease-in-out; }}
        
        /* Responsive Navigation */
        @media (max-width: 1024px) {{
            .nav-gap {{
                gap: 0.75rem !important;
            }}
            .nav-btn {{
                padding: 0.5rem !important;
                font-size: 0.7rem !important;
            }}
            .nav-btn i {{
                font-size: 0.8rem !important;
            }}
        }}
        @media (max-width: 768px) {{
            .nav-gap {{
                gap: 0.5rem !important;
                flex-wrap: wrap !important;
                justify-content: center !important;
            }}
            .nav-btn {{
                padding: 0.4rem 0.6rem !important;
                font-size: 0.65rem !important;
            }}
            .nav-btn i {{
                font-size: 0.75rem !important;
            }}
            .header-container {{
                flex-wrap: wrap !important;
                height: auto !important;
                padding-top: 0.5rem !important;
                padding-bottom: 0.5rem !important;
            }}
        }}
        @media (max-width: 640px) {{
            .nav-btn span {{
                display: none !important;
            }}
            .nav-btn i {{
                margin-right: 0 !important;
                font-size: 1rem !important;
            }}
            .nav-btn {{
                padding: 0.5rem !important;
            }}
        }}
    </style>
</head>
<body class="text-brand-slateBlack antialiased text-sm transition-all duration-300">

<!-- Sidebar Drawer Backdrop Overlay -->
<div id="sidebar-backdrop" class="fixed inset-0 bg-brand-black/80 backdrop-blur-sm z-40 hidden transition-all duration-300 opacity-0" onclick="toggleSidebar()"></div>

<!-- Sliding Sidebar Drawer Menu -->
<aside id="sidebar-drawer" class="fixed left-0 top-0 h-screen w-80 bg-brand-slateBlack border-r border-white/10 z-50 p-6 flex flex-col justify-between shadow-2xl transition-transform duration-300 transform -translate-x-full">
    <div class="space-y-8">
        <div class="flex items-center justify-between border-b border-white/5 pb-5">
            <a href="#home-hero" class="flex items-center gap-2.5 group" onclick="toggleSidebar()">
                <div class="h-8 w-8 bg-gradient-to-b from-brand-goldLight via-brand-gold to-brand-goldDark rounded-lg flex items-center justify-center text-brand-black font-black text-lg tracking-tight shadow-md transition-transform group-hover:rotate-6">A</div>
                <span class="text-sm font-bold tracking-tight text-white uppercase flex flex-col gap-0.5">ANGWA<span class="text-brand-gold">.</span></span>
            </a>
            <button onclick="toggleSidebar()" class="h-8 w-8 rounded-full border border-white/10 text-gray-400 hover:text-white flex items-center justify-center transition-colors hover:border-brand-gold/40"><i class="fa-solid fa-xmark text-sm"></i></button>
        </div>
        <nav class="flex flex-col gap-3 text-[11px] tracking-widest font-extrabold uppercase pt-2">
            <a href="#why-angwa" class="sidebar-nav-link text-gray-300 hover:text-brand-gold transition-all duration-300 py-3 border-l-2 border-transparent pl-3 flex items-center gap-2.5" onclick="toggleSidebar()"><i class="fa-solid fa-circle-info text-brand-gold text-xs w-4"></i> Who We Are</a>
            <button onclick="triggerLeadershipNotice(); toggleSidebar();" class="sidebar-nav-link text-left text-gray-300 hover:text-brand-gold transition-all duration-300 py-3 border-l-2 border-transparent pl-3 flex items-center gap-2.5"><i class="fa-solid fa-users text-brand-gold text-xs w-4"></i> Our Leadership</button>
            <div class="flex flex-col">
                <button onclick="toggleSidebarSubmenu('services-submenu')" class="sidebar-nav-link text-left text-gray-300 hover:text-brand-gold transition-all duration-300 py-3 border-l-2 border-transparent pl-3 flex items-center justify-between w-full">
                    <span class="flex items-center gap-2.5"><i class="fa-solid fa-network-wired text-brand-gold text-xs w-4"></i> Services</span>
                    <i class="fa-solid fa-chevron-down text-[9px] text-gray-500 mr-3 transition-transform duration-200" id="services-submenu-arrow"></i>
                </button>
                <div id="services-submenu" class="hidden flex flex-col gap-2 pl-9 pt-1 pb-2 text-[10px] text-gray-400 font-bold lowercase tracking-normal">
                    <a href="#services" onclick="toggleSidebar()" class="hover:text-brand-gold transition-colors py-1.5 flex items-center gap-2"><span class="h-1.5 w-1.5 rounded-full bg-brand-gold"></span> build environment</a>
                    <div class="flex flex-col">
                        <button onclick="toggleSidebarSubmenu('advisory-submenu')" class="text-left hover:text-brand-gold transition-colors py-1.5 flex items-center justify-between w-full">
                            <span class="flex items-center gap-2"><span class="h-1.5 w-1.5 rounded-full bg-brand-gold"></span> advisory & management</span>
                            <i class="fa-solid fa-chevron-down text-[8px] text-gray-500 mr-1 transition-transform duration-200" id="advisory-submenu-arrow"></i>
                        </button>
                        <div id="advisory-submenu" class="hidden flex flex-col gap-1 pl-5 pt-1 pb-1 text-[9px] text-gray-500 font-bold lowercase tracking-normal border-l border-brand-gold/20 ml-1">
                            <div class="flex flex-col">
                                <button onclick="toggleSidebarSubmenu('it-submenu')" class="text-left hover:text-brand-gold transition-colors py-1.5 flex items-center justify-between w-full">
                                    <span class="flex items-center gap-2"><i class="fa-solid fa-microchip text-brand-gold/70 text-[8px] w-3"></i> information technology</span>
                                    <i class="fa-solid fa-chevron-down text-[7px] text-gray-600 mr-1 transition-transform duration-200" id="it-submenu-arrow"></i>
                                </button>
                                <div id="it-submenu" class="hidden flex flex-col gap-1 pl-4 pt-1 pb-1 text-[9px] text-gray-600 font-bold lowercase tracking-normal border-l border-brand-gold/15 ml-1.5">
                                    <a href="#" onclick="showPage('host'); toggleSidebar();" class="hover:text-brand-gold transition-colors py-1.5 flex items-center gap-2"><i class="fa-solid fa-server text-brand-gold/50 text-[7px] w-3"></i> host</a>
                                    <a href="#" onclick="showPage('design'); toggleSidebar();" class="hover:text-brand-gold transition-colors py-1.5 flex items-center gap-2"><i class="fa-solid fa-pen-nib text-brand-gold/50 text-[7px] w-3"></i> web design</a>
                                    <a href="#" onclick="showPage('cloud'); toggleSidebar();" class="hover:text-brand-gold transition-colors py-1.5 flex items-center gap-2"><i class="fa-solid fa-cloud text-brand-gold/50 text-[7px] w-3"></i> cloud</a>
                                </div>
                            </div>
                            <a href="#services" onclick="toggleSidebar()" class="hover:text-brand-gold transition-colors py-1.5 flex items-center gap-2"><i class="fa-solid fa-building text-brand-gold/70 text-[8px] w-3"></i> properties</a>
                        </div>
                    </div>
                </div>
            </div>
            <div class="flex flex-col">
                <button onclick="toggleSidebarSubmenu('client-submenu')" class="sidebar-nav-link text-left text-gray-300 hover:text-brand-gold transition-all duration-300 py-3 border-l-2 border-transparent pl-3 flex items-center justify-between w-full">
                    <span class="flex items-center gap-2.5"><i class="fa-solid fa-user-gear text-brand-gold text-xs w-4"></i> Client</span>
                    <i class="fa-solid fa-chevron-down text-[9px] text-gray-500 mr-3 transition-transform duration-200" id="client-submenu-arrow"></i>
                </button>
                <div id="client-submenu" class="hidden flex flex-col gap-2 pl-9 pt-1 pb-2 text-[10px] text-gray-400 font-bold lowercase tracking-normal">
                    <button onclick="triggerClientPortal('commercial')" class="text-left hover:text-brand-gold transition-colors py-1.5 flex items-center gap-2 w-full"><span class="h-1.5 w-1.5 rounded-full bg-brand-gold"></span> commercial & industry</button>
                    <button onclick="triggerClientPortal('government')" class="text-left hover:text-brand-gold transition-colors py-1.5 flex items-center gap-2 w-full"><span class="h-1.5 w-1.5 rounded-full bg-brand-gold"></span> government</button>
                </div>
            </div>
            <a href="#design-suite" class="sidebar-nav-link text-gray-300 hover:text-brand-gold transition-all duration-300 py-3 border-l-2 border-transparent pl-3 flex items-center gap-2.5" onclick="toggleSidebar()"><i class="fa-solid fa-compass-drafting text-brand-gold text-xs w-4"></i> Project</a>
            <a href="#why-angwa" class="sidebar-nav-link text-gray-300 hover:text-brand-gold transition-all duration-300 py-3 border-l-2 border-transparent pl-3 flex items-center gap-2.5" onclick="toggleSidebar()"><i class="fa-solid fa-building text-brand-gold text-xs w-4"></i> Corporate</a>
            <button onclick="triggerBlogsModal(); toggleSidebar();" class="sidebar-nav-link text-left text-gray-300 hover:text-brand-gold transition-all duration-300 py-3 border-l-2 border-transparent pl-3 flex items-center gap-2.5"><i class="fa-solid fa-newspaper text-brand-gold text-xs w-4"></i> Blogs</button>
            <a href="#faq" class="sidebar-nav-link text-gray-300 hover:text-brand-gold transition-all duration-300 py-3 border-l-2 border-transparent pl-3 flex items-center gap-2.5" onclick="toggleSidebar()"><i class="fa-solid fa-address-book text-brand-gold text-xs w-4"></i> Contacts</a>
        </nav>
    </div>
    <div class="space-y-3.5 border-t border-white/5 pt-6">
        <a href="#coverage" class="w-full text-center glossy-green text-white py-3.5 rounded-xl font-bold text-[10px] uppercase tracking-wider shadow-md flex items-center justify-center gap-2" onclick="toggleSidebar()"><i class="fa-solid fa-compass"></i><span>Check Coverage</span></a>
        <button onclick="triggerClientZone(); toggleSidebar();" class="w-full text-center glossy-gold text-brand-black py-3.5 rounded-xl font-bold text-[10px] uppercase tracking-wider shadow-md flex items-center justify-center gap-2"><i class="fa-solid fa-user-shield"></i><span>ClientZone</span></button>
    </div>
</aside>

<!-- Promo Bar -->
<div class="bg-gradient-to-r from-brand-black via-[#1C1C1E] to-brand-black text-white py-2.5 px-4 text-center text-xs md:text-sm font-medium tracking-wide flex items-center justify-center gap-2.5 border-b border-brand-gold/20">
    <span class="bg-gradient-to-r from-brand-gold via-brand-goldLight to-brand-goldDark text-brand-black text-[10px] px-2.5 py-0.5 rounded-full uppercase font-black tracking-wider shadow-sm animate-pulse">PROMO</span>
    <span class="text-slate-300">Zero Setup Fees, Free Premium Wi-Fi 6 Router & 30-Day Money-Back Guarantee!</span>
</div>

<!-- Apple style Navigation Header -->
<header class="sticky top-0 z-40 bg-brand-slateBlack/90 backdrop-blur-md border-b border-white/10 shadow-lg transition-all duration-300">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2 header-container flex items-center justify-between">
        <div class="flex items-center gap-3 shrink-0">
            <button onclick="toggleSidebar()" class="text-white hover:text-brand-gold transition-colors focus:outline-none h-10 w-10 rounded-xl border border-white/10 hover:border-brand-gold/30 flex items-center justify-center bg-white/5 shadow-inner"><i class="fa-solid fa-bars text-lg"></i></button>
            <a href="#home-hero" class="flex items-center gap-2 group">
                <div class="h-8 w-8 bg-gradient-to-b from-brand-goldLight via-brand-gold to-brand-goldDark rounded-lg flex items-center justify-center text-brand-black font-black text-lg tracking-tight shadow-md transition-transform group-hover:rotate-6 shrink-0">A</div>
                <span id="dynamic-nav-badge" class="text-xs sm:text-sm font-extrabold tracking-tight text-white uppercase transition-all duration-300 min-w-[130px] inline-block opacity-100 transform translate-y-0">ANGWA<span class="text-brand-gold">.</span></span>
            </a>
        </div>
        
        <!-- Responsive Navigation (always visible, wraps on mobile) -->
        <nav class="flex items-center gap-3 lg:gap-5 text-xs text-white font-extrabold uppercase tracking-widest nav-gap">
            <button onclick="showPage('home')" id="nav-home" class="nav-page-btn hover:text-brand-gold transition-colors py-2 flex items-center gap-1.5 nav-btn"><i class="fa-solid fa-house text-brand-gold text-sm"></i><span>Home</span></button>
            <button onclick="showPage('host')" id="nav-host" class="nav-page-btn hover:text-brand-gold transition-colors py-2 flex items-center gap-1.5 nav-btn"><i class="fa-solid fa-server text-brand-gold text-sm"></i><span>HOST</span></button>
            <button onclick="showPage('design')" id="nav-design" class="nav-page-btn hover:text-brand-gold transition-colors py-2 flex items-center gap-1.5 nav-btn"><i class="fa-solid fa-pen-nib text-brand-gold text-sm"></i><span>DESIGN</span></button>
            <button onclick="showPage('cloud')" id="nav-cloud" class="nav-page-btn hover:text-brand-gold transition-colors py-2 flex items-center gap-1.5 nav-btn"><i class="fa-solid fa-cloud text-brand-gold text-sm"></i><span>CLOUD</span></button>
            <div class="relative group">
                <button class="flex items-center gap-1.5 hover:text-brand-gold transition-colors focus:outline-none py-2 uppercase nav-btn"><i class="fa-solid fa-ellipsis-h text-brand-gold"></i><span>MORE</span><i class="fa-solid fa-chevron-down text-[9px] text-gray-500"></i></button>
                <div class="absolute left-0 mt-1 w-64 rounded-xl glass-dark shadow-2xl py-2 border border-white/10 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 transform translate-y-1 group-hover:translate-y-0 z-50 normal-case">
                    <button onclick="alertModal('Engineers workspace, database access, and analytics dashboard loaded.');" class="w-full text-left px-4 py-2 text-[10px] text-white hover:bg-white/10 hover:text-brand-gold transition-all flex items-center gap-2"><i class="fa-solid fa-microchip text-brand-gold"></i> Engineers</button>
                    <button onclick="alertModal('Architect blueprint environment and 3D schematic rendering pipeline initialized.');" class="w-full text-left px-4 py-2 text-[10px] text-white hover:bg-white/10 hover:text-brand-gold transition-all flex items-center gap-2"><i class="fa-solid fa-draw-polygon text-brand-gold"></i> architect</button>
                    <button onclick="alertModal('Occupational health & safety safety logs and regulatory compliance checklists loaded.');" class="w-full text-left px-4 py-2 text-[10px] text-white hover:bg-white/10 hover:text-brand-gold transition-all flex items-center gap-2"><i class="fa-solid fa-helmet-safety text-brand-gold"></i> occupational health & safety</button>
                    <button onclick="alertModal('Social facilitators outreach campaign metrics and community alignment matrix opened.');" class="w-full text-left px-4 py-2 text-[10px] text-white hover:bg-white/10 hover:text-brand-gold transition-all flex items-center gap-2"><i class="fa-solid fa-handshake text-brand-gold"></i> social facilitators</button>
                    <button onclick="alertModal('Quantity surveyors cost-estimation engine and project billing ledger updated.');" class="w-full text-left px-4 py-2 text-[10px] text-white hover:bg-white/10 hover:text-brand-gold transition-all flex items-center gap-2"><i class="fa-solid fa-calculator text-brand-gold"></i> quantity surveyors</button>
                    <button onclick="alertModal('Developer repository sync-state, cloud hosting cluster, and SLA logs active.');" class="w-full text-left px-4 py-2 text-[10px] text-white hover:bg-white/10 hover:text-brand-gold transition-all flex items-center gap-2"><i class="fa-solid fa-code text-brand-gold"></i> developer</button>
                </div>
            </div>
        </nav>
        
        <div class="flex items-center gap-2 shrink-0">
            <div class="relative">
                <button onclick="toggleNotificationDropdown(event)" class="text-white hover:text-brand-gold transition-colors h-10 w-10 rounded-xl border border-white/10 hover:border-brand-gold/30 flex items-center justify-center bg-white/5 shadow-inner"><i class="fa-solid fa-bell text-sm"></i><span id="notify-pulse-dot" class="absolute top-2.5 right-2.5 h-2 w-2 bg-brand-green rounded-full shadow-[0_0_8px_#30D158] animate-pulse"></span></button>
                <div id="notify-dropdown-panel" class="hidden absolute right-0 mt-3.5 w-76 rounded-2xl glass-dark shadow-2xl p-4 border border-white/10 z-50">
                    <h5 class="text-[10px] font-black text-brand-gold tracking-widest uppercase mb-3">Live Symmetrical Alerts</h5>
                    <div class="space-y-2.5 text-[10px] text-gray-300">
                        <div class="p-2.5 bg-white/5 rounded-xl border border-white/5 hover:border-brand-gold/20 transition-all flex items-start gap-2.5"><i class="fa-solid fa-gift text-brand-gold mt-0.5 shrink-0"></i><div><span class="font-bold text-white block">Wi-Fi 6 Router Active!</span>Free pre-configured hardware included in your package.</div></div>
                        <div class="p-2.5 bg-white/5 rounded-xl border border-white/5 hover:border-brand-gold/20 transition-all flex items-start gap-2.5"><i class="fa-solid fa-plug-circle-check text-brand-green mt-0.5 shrink-0"></i><div><span class="font-bold text-white block">Local Grid Upgraded</span>Symmetrical transmission rates optimized across network pools.</div></div>
                    </div>
                </div>
            </div>
            <div class="relative">
                <button id="cart-btn" onclick="toggleCartDropdown(event)" class="text-white hover:text-brand-gold transition-colors h-10 w-10 rounded-xl border border-white/10 hover:border-brand-gold/30 flex items-center justify-center bg-white/5 shadow-inner"><i class="fa-solid fa-bag-shopping text-sm"></i><span id="header-cart-badge" class="absolute -top-1 -right-1 h-4.5 w-4.5 bg-brand-gold text-brand-black rounded-full text-[9px] font-black flex items-center justify-center hidden">0</span></button>
                <div id="cart-dropdown-panel" class="hidden absolute right-0 mt-3.5 w-80 rounded-2xl glass-dark shadow-2xl p-4 border border-white/10 z-50 text-white">
                    <h5 class="text-[10px] font-black text-brand-gold tracking-widest uppercase mb-3 flex items-center justify-between"><span>Your Configured Bag</span><button onclick="clearCart()" class="text-gray-400 hover:text-red-400 text-[8px] tracking-normal font-bold">Clear All</button></h5>
                    <div id="cart-dropdown-content" class="text-[10px] text-gray-400 text-center py-4 space-y-3"><i class="fa-solid fa-basket-shopping text-2xl text-gray-600 block"></i><span>No products added yet.</span></div>
                </div>
            </div>
            <button onclick="triggerClientZone()" class="glossy-gold text-brand-black px-4 lg:px-5 py-2 rounded-full font-bold text-xs shadow-md flex items-center gap-1.5 shrink-0"><i class="fa-solid fa-user-shield"></i><span class="hidden sm:inline">ClientZone</span><span class="sm:hidden"><i class="fa-solid fa-user-shield"></i></span></button>
        </div>
    </div>
</header>

{home.get_home_html()}

{host.get_host_html()}

{design.get_design_html()}

{cloud.get_cloud_html()}

<!-- Sign Up Modal -->
<div id="signup-modal" class="fixed inset-0 z-50 overflow-y-auto hidden" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0"><div class="fixed inset-0 bg-brand-black/80 backdrop-blur-md transition-opacity" aria-hidden="true" onclick="closeModal()"></div><span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span><div class="inline-block align-bottom bg-brand-slateBlack text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-xl sm:w-full rounded-3xl border border-white/10 text-white"><div class="bg-brand-darkGray px-6 py-5 flex items-center justify-between border-b border-white/5"><div><span class="text-[10px] uppercase tracking-widest text-brand-gold font-bold block">Checkout Process</span><h3 class="text-md font-bold">Fast-Track Secure Order</h3></div><button onclick="closeModal()" class="text-gray-400 hover:text-white transition-colors text-xl"><i class="fa-solid fa-circle-xmark"></i></button></div><div class="bg-black/40 px-6 py-3 flex items-center justify-between text-[10px] font-bold text-gray-500 uppercase tracking-wider"><span id="step-indicator-2" class="text-brand-gold flex items-center gap-1.5"><span class="h-4.5 w-4.5 rounded-full bg-brand-gold/20 text-brand-gold flex items-center justify-center text-[9px] font-black">1</span> Delivery Details</span><span id="step-indicator-3" class="flex items-center gap-1.5"><span class="h-4.5 w-4.5 rounded-full bg-white/5 text-gray-500 flex items-center justify-center text-[9px] font-black">2</span> Order Verification</span></div><div class="p-6"><div id="modal-step-2" class="space-y-4"><h4 class="font-bold text-xs text-white uppercase tracking-wider">Subscriber Connection Information</h4><div class="space-y-3 text-xs"><div><label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Full Subscriber Name</label><input type="text" id="cust-name" placeholder="e.g. Lerato Ndlovu" class="w-full px-4 py-2.5 bg-brand-darkGray border border-white/10 rounded-xl text-white focus:ring-2 focus:ring-brand-gold focus:outline-none"></div><div><label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Primary Email Contact</label><input type="email" id="cust-email" placeholder="e.g. lerato@domain.co.za" class="w-full px-4 py-2.5 bg-brand-darkGray border border-white/10 rounded-xl text-white focus:ring-2 focus:ring-brand-gold focus:outline-none"></div><div><label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Setup / Installation Address</label><input type="text" id="cust-address" placeholder="e.g. Unit 5, Sandhurst Ridge Complex" class="w-full px-4 py-2.5 bg-brand-darkGray border border-white/10 rounded-xl text-white focus:ring-2 focus:ring-brand-gold focus:outline-none"></div></div></div><div id="modal-step-3" class="space-y-4 hidden"><div class="text-center space-y-2 py-4"><div class="h-14 w-14 bg-brand-green/10 text-brand-green rounded-full flex items-center justify-center text-2xl mx-auto shadow-inner"><i class="fa-regular fa-circle-check"></i></div><h4 class="font-black text-base text-white">Setup Configurations Verified</h4><p class="text-[11px] text-gray-400 max-w-sm mx-auto">No upfront setup charges are required. Launch your checkout via Polar.sh below to register monthly allocations.</p></div><div class="bg-brand-darkGray/60 p-4 rounded-2xl border border-white/5 space-y-2.5 text-xs text-gray-300"><div class="font-bold text-[10px] uppercase tracking-widest text-brand-gold border-b border-white/5 pb-2">Active Cart Items</div><div id="modal-verification-summary" class="space-y-2"></div><div class="flex justify-between border-t border-white/10 pt-2.5 text-sm font-bold"><span class="text-white">Active Checkout Subtotal:</span><span class="text-brand-gold" id="summary-total-price">R0.00</span></div></div></div></div><div class="bg-brand-darkGray px-6 py-4 flex items-center justify-between border-t border-white/5"><button id="modal-back-btn" onclick="prevStep()" class="text-xs font-bold tracking-wider uppercase text-gray-400 hover:text-white transition-colors hidden"><i class="fa-solid fa-chevron-left mr-1"></i> Back</button><span class="text-xs font-bold text-white">Checkout Total: <span class="text-brand-gold font-black" id="modal-footer-price">R0.00</span></span><div id="modal-next-btn-container"><button id="modal-next-btn" onclick="nextStep()" class="glossy-gold text-brand-black px-6 py-2.5 rounded-full font-bold text-xs tracking-wider uppercase shadow-md">Continue <i class="fa-solid fa-chevron-right ml-1"></i></button></div></div></div></div>
</div>

<!-- Cloud Sync Dialog -->
<div id="cloud-sync-modal" class="fixed inset-0 z-50 overflow-y-auto hidden" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-center justify-center min-h-screen p-4"><div class="fixed inset-0 bg-brand-black/80 backdrop-blur-md transition-opacity" onclick="closeCloudModal()"></div><div class="bg-brand-slateBlack text-white p-8 rounded-3xl max-w-sm w-full space-y-6 text-center border border-white/10 relative z-10 overflow-hidden"><div class="absolute -top-12 -right-12 h-32 w-32 bg-brand-gold/10 rounded-full filter blur-xl"></div><div class="h-16 w-16 bg-brand-gold/15 text-brand-gold rounded-full flex items-center justify-center text-3xl mx-auto shadow-inner border border-brand-gold/20"><i id="cloud-icon" class="fa-brands fa-dropbox"></i></div><div class="space-y-2"><h4 class="font-bold text-md text-white">Cloud Filling Simulation</h4><p id="cloud-sync-status" class="text-xs text-gray-400 leading-relaxed">Initializing secure Dropbox high-speed fiber mapping pipeline...</p></div><div class="bg-black/40 p-4 rounded-2xl border border-white/5 space-y-3"><div class="flex justify-between text-[10px] uppercase font-bold text-gray-500"><span>Speed Transfer Rate</span><span class="text-brand-green">1,000 Mbps</span></div><div class="w-full bg-brand-darkGray rounded-full h-2 overflow-hidden border border-white/10"><div id="cloud-progress-bar" class="bg-brand-green h-full rounded-full transition-all duration-300" style="width: 0%"></div></div><div class="flex justify-between text-[10px] text-gray-400"><span>Synced 50GB project files</span><span id="cloud-timer-val">Calculating...</span></div></div><button onclick="closeCloudModal()" class="w-full glossy-gold text-brand-black py-2.5 rounded-full font-bold text-xs uppercase tracking-wider">Close Sync Pipeline</button></div></div>
</div>

{clientzone.get_clientzone_html()}

<!-- Register Modal -->
<div id="register-modal" class="fixed inset-0 z-50 overflow-y-auto hidden" aria-labelledby="modal-title" role="dialog">
    <div class="flex items-center justify-center min-h-screen p-4"><div class="fixed inset-0 bg-brand-black/80 backdrop-blur-md" onclick="closeRegisterModal()"></div><div class="bg-brand-slateBlack text-white p-6 rounded-3xl max-w-md w-full space-y-5 border border-white/10 relative z-10"><div class="text-center space-y-2"><div class="h-12 w-12 bg-brand-gold/10 text-brand-gold rounded-full flex items-center justify-center text-xl mx-auto"><i class="fa-solid fa-user-plus"></i></div><h4 class="font-bold text-lg">Create ANGWA Account</h4><p class="text-xs text-gray-400">Access your fibre orders, invoices, and support tickets.</p></div><div class="space-y-3 text-xs"><div><label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Full name</label><input type="text" id="reg-name" placeholder="e.g. Thabo Nkosi" class="w-full px-4 py-2.5 bg-brand-darkGray border border-white/10 rounded-xl text-white focus:ring-2 focus:ring-brand-gold"></div><div><label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Email address</label><input type="email" id="reg-email" placeholder="thabo@example.com" class="w-full px-4 py-2.5 bg-brand-darkGray border border-white/10 rounded-xl text-white focus:ring-2 focus:ring-brand-gold"></div><div><label class="block text-[10px] font-bold uppercase text-gray-400 mb-1">Password</label><input type="password" id="reg-password" placeholder="••••••••" class="w-full px-4 py-2.5 bg-brand-darkGray border border-white/10 rounded-xl text-white focus:ring-2 focus:ring-brand-gold"></div></div><button onclick="registerUser()" class="w-full glossy-gold text-brand-black py-3 rounded-full font-bold uppercase tracking-wider text-xs">Create account</button><div class="text-center text-[9px] text-gray-500">Already have an account? <button onclick="closeRegisterModal(); triggerClientZone()" class="text-brand-gold hover:underline">Sign in</button></div></div></div>
</div>

<!-- Blogs Simulated Modal -->
<div id="blogs-modal" class="fixed inset-0 z-50 overflow-y-auto hidden" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-center justify-center min-h-screen p-4"><div class="fixed inset-0 bg-brand-black/80 backdrop-blur-md transition-opacity" onclick="closeBlogsModal()"></div><div class="bg-brand-slateBlack text-white p-8 rounded-3xl max-w-lg w-full space-y-6 border border-white/10 relative z-10 max-h-[90vh] overflow-y-auto"><div class="flex justify-between items-center border-b border-white/5 pb-4"><h4 class="font-bold text-lg text-brand-gold">ANGWA Symmetrical Blogs</h4><button onclick="closeBlogsModal()" class="text-gray-400 hover:text-white"><i class="fa-solid fa-xmark"></i></button></div><div class="space-y-6 text-xs text-gray-300"><div class="space-y-2"><span class="text-[9px] bg-brand-gold/20 text-brand-gold font-bold px-2 py-0.5 rounded uppercase">Networking</span><h5 class="text-white font-bold text-sm">Why Symmetrical Speeds Matter for Hybrid Workspace Architecture</h5><p class="leading-relaxed text-gray-400">Discover how identical upstream outputs boost video conferencing protocols and render standard copper DSL obsolete.</p></div><div class="space-y-2 border-t border-white/5 pt-4"><span class="text-[9px] bg-brand-green/20 text-brand-green font-bold px-2 py-0.5 rounded uppercase">Web Infrastructure</span><h5 class="text-white font-bold text-sm">Responsive Splicing: How Hand-Coded Portfolios Dominate Search Engines</h5><p class="leading-relaxed text-gray-400">A guide on optimizing website structures to achieve a 99/99 performance score on Google Lighthouse.</p></div><div class="space-y-2 border-t border-white/5 pt-4"><span class="text-[9px] bg-brand-gold/20 text-brand-gold font-bold px-2 py-0.5 rounded uppercase">Cloud Sync</span><h5 class="text-white font-bold text-sm">Maximizing Backups: Integrating Dropbox & Google Drive directly into Optical Grids</h5><p class="leading-relaxed text-gray-400">Bypassing ISP throttles to sync immense database structures under single second thresholds.</p></div></div></div></div>
</div>

<!-- Toast Notification -->
<div id="order-toast" class="fixed bottom-6 right-6 z-50 bg-brand-slateBlack text-white px-6 py-4 rounded-2xl shadow-2xl border border-brand-gold/30 flex items-center gap-4 hidden max-w-sm"><div class="h-10 w-10 bg-brand-gold/15 text-brand-gold rounded-xl flex items-center justify-center text-xl shrink-0"><i class="fa-solid fa-paper-plane"></i></div><div class="text-xs"><h5 class="font-bold text-white">Pre-order Registered!</h5><p class="text-gray-400 mt-0.5">Please check your inbox. Our support crew will contact you soon.</p></div><button onclick="hideOrderToast()" class="text-gray-500 hover:text-white transition-colors"><i class="fa-solid fa-xmark"></i></button></div>

<!-- Float Support Panel -->
<div class="fixed bottom-6 left-6 z-40">
    <button onclick="toggleLiveChat()" class="h-12 w-12 bg-gradient-to-b from-brand-goldLight via-brand-gold to-brand-goldDark text-brand-black rounded-full flex items-center justify-center text-xl shadow-xl hover:scale-105 transition-all relative"><i class="fa-solid fa-headset"></i><span class="absolute top-0 right-0 h-3.5 w-3.5 bg-brand-green border-2 border-brand-black rounded-full flex items-center justify-center text-[7px] font-bold text-white">1</span></button>
    <div id="chat-popup" class="hidden absolute bottom-16 left-0 bg-brand-slateBlack border border-white/10 rounded-2xl shadow-2xl w-76 overflow-hidden text-xs text-white"><div class="bg-brand-darkGray p-4 flex items-center gap-3 border-b border-white/5"><div class="h-9 w-9 bg-brand-gold/15 rounded-full flex items-center justify-center text-brand-gold shadow-inner"><i class="fa-solid fa-circle-user text-md"></i></div><div><h5 class="font-bold">Fibre Agent Sipho</h5><p class="text-[9px] text-brand-green font-semibold flex items-center gap-1"><span class="h-1.5 w-1.5 rounded-full bg-brand-green block animate-pulse"></span> Symmetrical Carrier Advisor</p></div></div><div class="p-4 space-y-4 max-h-52 overflow-y-auto bg-brand-black/40 text-gray-300" id="chat-messages"><div class="bg-brand-darkGray/60 p-3 rounded-2xl border border-white/5 text-gray-300 max-w-[85%] leading-relaxed">Good day! Let me help you find the best month-to-month fibre setup or premium custom design templates. Where are you located?</div></div><div class="p-2.5 bg-brand-darkGray border-t border-white/5 flex items-center gap-1.5"><input type="text" id="chat-input" placeholder="Type message..." class="flex-1 bg-brand-black border border-white/10 px-3 py-2 rounded-xl text-xs focus:outline-none focus:ring-1 focus:ring-brand-gold text-white placeholder-gray-500" onkeydown="handleChatSubmit(event)"><button onclick="sendChatMessage()" class="h-8 w-8 bg-brand-gold text-brand-black rounded-lg flex items-center justify-center hover:bg-brand-goldLight transition-colors"><i class="fa-solid fa-paper-plane text-xs"></i></button></div></div>
</div>

<!-- Footer -->
<footer class="bg-brand-black text-gray-500 py-16 border-t border-white/10 text-xs">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-8"><div class="col-span-2 space-y-4"><a href="#" class="flex items-center gap-2"><div class="h-7 w-7 bg-brand-gold rounded-md flex items-center justify-center text-brand-black font-black text-sm shadow-md">A</div><span class="text-lg font-bold text-white tracking-wider">ANGWA.</span></a><p class="leading-relaxed text-gray-400">ANGWA is a licensed provider of optical fibre connections and digital bespoke web environments in South Africa. Operating across the main national carrier frameworks to bring symmetrical speeds directly to you.</p><div class="flex items-center gap-3 pt-2 text-gray-400"><a href="#" class="hover:text-brand-gold transition-colors"><i class="fa-brands fa-facebook"></i></a><a href="#" class="hover:text-brand-gold transition-colors"><i class="fa-brands fa-x-twitter"></i></a><a href="#" class="hover:text-brand-gold transition-colors"><i class="fa-brands fa-instagram"></i></a><a href="#" class="hover:text-brand-gold transition-colors"><i class="fa-brands fa-linkedin"></i></a></div></div><div><h5 class="text-white text-[10px] font-bold uppercase tracking-wider mb-4">Hosting Products</h5><ul class="space-y-2"><li><a href="#packages" onclick="setMainCategory('hostings'); setSubCategory('shared')" class="hover:text-white transition-colors">Shared Hosting</a></li><li><a href="#packages" onclick="setMainCategory('hostings'); setSubCategory('cloudhosting')" class="hover:text-white transition-colors">Cloud Hosting</a></li><li><a href="#packages" onclick="setMainCategory('hostings'); setSubCategory('reseller')" class="hover:text-white transition-colors">Reseller Hosting</a></li><li><a href="#packages" onclick="setMainCategory('hostings'); setSubCategory('dedicated')" class="hover:text-white transition-colors">Dedicated Servers</a></li></ul></div><div><h5 class="text-white text-[10px] font-bold uppercase tracking-wider mb-4">Domains & Emails</h5><ul class="space-y-2"><li><a href="#packages" onclick="setMainCategory('domains'); setSubCategory('domains')" class="hover:text-white transition-colors">Domain Registration</a></li><li><a href="#packages" onclick="setMainCategory('domains'); setSubCategory('pointing')" class="hover:text-white transition-colors">Domain Pointing</a></li><li><a href="#packages" onclick="setMainCategory('emails'); setSubCategory('emails')" class="hover:text-white transition-colors">Email Hosting</a></li><li><a href="#packages" onclick="setMainCategory('emails'); setSubCategory('free_domain')" class="hover:text-white transition-colors">Free Domain Offer</a></li></ul></div><div><h5 class="text-white text-[10px] font-bold uppercase tracking-wider mb-4">Support & Care</h5><ul class="space-y-2"><li><a href="#" class="hover:text-white transition-colors">Client Zone Login</a></li><li><a href="#" class="hover:text-white transition-colors">Help Centre</a></li><li><a href="#" class="hover:text-white transition-colors">Network Status Map</a></li><li><a href="#" class="hover:text-white transition-colors">Contact Support</a></li></ul></div></div><div class="mt-12 pt-8 border-t border-white/5 text-center text-[10px] text-gray-600 space-y-2"><p>© 2026 ANGWA Proprietary Limited. All rights reserved. Registered ICASA carrier frameworks.</p><p>Designed for maximum speed simulation based on physical optical fibre networks locally deployed.</p></div></div>
</footer>

<script>
    // ==================== DYNAMIC DATA FROM TURSO ====================
    const packageData = {package_json};
    const cloudStorageData = {cloud_json};
    const designData = {design_json};
    const addonData = {addon_json};
    const coverageAreas = {coverage_json};

    // ==================== BACKEND API URL ====================
    const API_BASE = "{api_base_url}";

    // ==================== UPDATED PRODUCTS ====================

    // Internet Services (new category)
    const internetProducts = {{
        fibre: [
            {{ id: "fibre_starter", name: "Pure Fibre Starter", description: "10Mbps symmetrical fibre – uncapped, unshaped, and ready for heavy usage.", price: 412.10, features: ["10Mbps", "Uncapped", "Free Wi-Fi 6 Router", "Free Installation"], isPopular: false, category: "fibre", type: "internet" }},
            {{ id: "fibre_basic", name: "Pure Fibre Basic", description: "20Mbps symmetrical fibre – ideal for small households and light streaming.", price: 518.70, features: ["20Mbps", "Uncapped", "Free Wi-Fi 6 Router", "Free Installation"], isPopular: false, category: "fibre", type: "internet" }},
            {{ id: "fibre_standard", name: "Pure Fibre Standard", description: "50Mbps – perfect for families, HD streaming, and home offices.", price: 648.70, features: ["50Mbps", "Uncapped", "Free Wi-Fi 6 Router", "Free Installation"], isPopular: true, category: "fibre", type: "internet" }},
            {{ id: "fibre_advanced", name: "Pure Fibre Advanced", description: "100Mbps – power through 4K streaming, gaming, and large file transfers.", price: 908.70, features: ["100Mbps", "Uncapped", "Free Wi-Fi 6 Router", "Free Installation"], isPopular: false, category: "fibre", type: "internet" }},
            {{ id: "fibre_pro", name: "Pure Fibre Pro", description: "250Mbps – serious bandwidth for multiple heavy users and servers.", price: 1298.70, features: ["250Mbps", "Uncapped", "Free Wi-Fi 6 Router", "Free Installation"], isPopular: false, category: "fibre", type: "internet" }},
            {{ id: "fibre_ultra", name: "Pure Fibre Ultra", description: "500Mbps – extreme speed for large businesses and high-density environments.", price: 1948.70, features: ["500Mbps", "Uncapped", "Free Wi-Fi 6 Router", "Free Installation"], isPopular: false, category: "fibre", type: "internet" }},
            {{ id: "fibre_extreme", name: "Pure Fibre Extreme", description: "1Gbps – the ultimate symmetrical fibre experience, zero limits.", price: 2598.70, features: ["1000Mbps", "Uncapped", "Free Wi-Fi 6 Router", "Free Installation"], isPopular: false, category: "fibre", type: "internet" }}
        ],
        prepaid: [
            {{ id: "prepaid_fibre", name: "Prepaid Fibre", description: "Prepaid fibre access – pay as you go, no contracts, great for temporary setups.", price: 284.70, features: ["Prepaid", "No contract", "Flexible"], isPopular: false, category: "prepaid", type: "internet" }}
        ],
        wireless: [
            {{ id: "wireless_20", name: "Pure Wireless 20Mbps", description: "Up to 20Mbps fixed wireless – affordable and reliable.", price: 76.70, features: ["Up to 20Mbps", "Fixed Wireless", "No fibre required"], isPopular: false, category: "wireless", type: "internet" }},
            {{ id: "wireless_50", name: "Pure Wireless 50Mbps", description: "Up to 50Mbps – solid performance for streaming and browsing.", price: 161.20, features: ["Up to 50Mbps", "Fixed Wireless", "No fibre required"], isPopular: false, category: "wireless", type: "internet" }},
            {{ id: "wireless_100", name: "Pure Wireless 100Mbps", description: "Up to 100Mbps – high-speed wireless for heavy users.", price: 388.70, features: ["Up to 100Mbps", "Fixed Wireless", "No fibre required"], isPopular: true, category: "wireless", type: "internet" }},
            {{ id: "wireless_plus", name: "Pure Wireless Plus", description: "Uncapped wireless – unlimited data at consistent speeds.", price: 388.70, features: ["Uncapped", "Fixed Wireless", "No fibre required"], isPopular: false, category: "wireless", type: "internet" }}
        ],
        lte: [
            {{ id: "lte_10", name: "Pure LTE 10Mbps", description: "Up to 10Mbps LTE – mobile connectivity for on-the-go.", price: 63.70, features: ["Up to 10Mbps", "Mobile LTE", "Portable"], isPopular: false, category: "lte", type: "internet" }}
        ],
        airmobile: [
            {{ id: "airmobile_starter", name: "AirMobile Prepaid Starter", description: "1GB data + R10 airtime – perfect for occasional use.", price: 37.70, features: ["1GB Data", "R10 Airtime", "Prepaid"], isPopular: true, category: "airmobile", type: "internet" }},
            {{ id: "airmobile_data", name: "AirMobile Prepaid Data Only", description: "500MB data – light browsing and messaging.", price: 32.50, features: ["500MB Data", "Prepaid"], isPopular: false, category: "airmobile", type: "internet" }}
        ],
        voip: [
            {{ id: "voip_starter", name: "Pure VoIP Starter", description: "Voice over IP service – clear calls over your internet connection.", price: 65.00, features: ["VoIP", "Unlimited calls", "Low latency"], isPopular: false, category: "voip", type: "internet" }}
        ],
        devices: [
            {{ id: "device_5g", name: "ZTE G5TS 5G Router", description: "High-performance 5G router – get the fastest mobile speeds.", price: 1948.70, features: ["5G Router", "Wi-Fi 6", "Unlocked"], isPopular: false, category: "devices", type: "internet" }}
        ]
    }};

    // Hosting products (shared, cloud, reseller, dedicated, rack, whmcs) – updated with new entries
    const hostingProducts = {{
        shared: [
            {{ id: "shared_linux_silver", name: "Linux Silver", description: "2GB storage, 50 email accounts – great for personal sites.", price: 109.20, features: ["2GB Storage", "50 Emails", "cPanel"], isPopular: false, category: "shared", type: "hosting" }},
            {{ id: "shared_windows_starter", name: "Windows Starter", description: "Windows-based hosting with Plesk control panel.", price: 141.70, features: ["Windows", "Plesk", "1GB RAM"], isPopular: false, category: "shared", type: "hosting" }},
            // Keep existing shared products for variety
            {{ id: "shared_1", name: "Starter Shared", description: "Perfect for small websites and blogs. Includes free SSL, 10GB SSD, and cPanel.", price: 99, features: ["10 GB SSD", "Free SSL", "cPanel", "10k monthly visits"], isPopular: false, category: "shared", type: "hosting" }},
            {{ id: "shared_2", name: "Business Shared", description: "Ideal for growing businesses with higher traffic. 50GB SSD, daily backups, and priority support.", price: 199, features: ["50 GB SSD", "Daily Backups", "Priority Support", "50k monthly visits"], isPopular: true, category: "shared", type: "hosting" }},
            {{ id: "shared_3", name: "Pro Shared", description: "High-performance shared hosting with 100GB SSD, advanced caching, and free CDN.", price: 299, features: ["100 GB SSD", "Free CDN", "Advanced Caching", "200k monthly visits"], isPopular: false, category: "shared", type: "hosting" }}
        ],
        cloudhosting: [
            {{ id: "cloud_bronze", name: "Cloud Bronze (Self Managed)", description: "100GB HDD, 1 vCPU, 2GB RAM – scalable cloud.", price: 598.00, features: ["100GB HDD", "1 vCPU", "2GB RAM", "Self Managed"], isPopular: false, category: "cloudhosting", type: "hosting" }},
            {{ id: "cloud_managed", name: "Cloud Hosting Managed", description: "Fully managed cloud – we handle everything for you.", price: 2080.00, features: ["Managed", "24/7 Support", "Scalable"], isPopular: true, category: "cloudhosting", type: "hosting" }},
            // Keep existing cloud products
            {{ id: "cloud_1", name: "Cloud Starter", description: "Scalable cloud hosting with 2 vCPU, 4GB RAM, and 50GB SSD. Pay-as-you-grow.", price: 399, features: ["2 vCPU", "4 GB RAM", "50 GB SSD", "Auto-scaling"], isPopular: false, category: "cloudhosting", type: "hosting" }},
            {{ id: "cloud_2", name: "Cloud Business", description: "Enterprise-grade cloud with 4 vCPU, 8GB RAM, 100GB SSD, and load balancing.", price: 699, features: ["4 vCPU", "8 GB RAM", "100 GB SSD", "Load Balancer"], isPopular: true, category: "cloudhosting", type: "hosting" }},
            {{ id: "cloud_3", name: "Cloud Enterprise", description: "Maximum performance: 8 vCPU, 16GB RAM, 250GB SSD, dedicated environment.", price: 1299, features: ["8 vCPU", "16 GB RAM", "250 GB SSD", "Dedicated Environment"], isPopular: false, category: "cloudhosting", type: "hosting" }}
        ],
        reseller: [
            {{ id: "reseller_1", name: "Reseller Lite", description: "Start your hosting business. 50GB storage, white-label cPanel, and free WHMCS.", price: 499, features: ["50 GB Storage", "White-label cPanel", "WHMCS Included", "100 cPanel accounts"], isPopular: false, category: "reseller", type: "hosting" }},
            {{ id: "reseller_2", name: "Reseller Pro", description: "Grow with 200GB storage, branded nameservers, and priority support.", price: 899, features: ["200 GB Storage", "Branded Nameservers", "Priority Support", "500 cPanel accounts"], isPopular: true, category: "reseller", type: "hosting" }},
            {{ id: "reseller_3", name: "Reseller Ultimate", description: "Unlimited storage, free client management tools, and dedicated account manager.", price: 1499, features: ["Unlimited Storage", "Client Management", "Dedicated Manager", "Unlimited accounts"], isPopular: false, category: "reseller", type: "hosting" }}
        ],
        dedicated: [
            {{ id: "dedicated_1", name: "Dedicated X1", description: "Entry-level dedicated server: Intel Xeon E-2234, 16GB RAM, 2x480GB SSD.", price: 1999, features: ["Intel Xeon E-2234", "16 GB RAM", "2x480 GB SSD", "1 Gbps Unmetered"], isPopular: false, category: "dedicated", type: "hosting" }},
            {{ id: "dedicated_2", name: "Dedicated X2", description: "Mid-range power: Intel Xeon Silver, 32GB RAM, 2x1TB NVMe, hardware RAID.", price: 3499, features: ["Intel Xeon Silver", "32 GB RAM", "2x1 TB NVMe", "Hardware RAID"], isPopular: true, category: "dedicated", type: "hosting" }},
            {{ id: "dedicated_3", name: "Dedicated X3", description: "Ultimate performance: Dual Xeon Gold, 64GB RAM, 4x1TB NVMe, 10Gbps uplink.", price: 5999, features: ["Dual Xeon Gold", "64 GB RAM", "4x1 TB NVMe", "10 Gbps Uplink"], isPopular: false, category: "dedicated", type: "hosting" }}
        ],
        rack: [
            {{ id: "rack_1", name: "Rack 1U", description: "Colocation: 1U rack space, 1A power, 1Gbps port, 5TB transfer.", price: 1499, features: ["1U Rack Space", "1A Power", "1 Gbps Port", "5 TB Transfer"], isPopular: false, category: "rack", type: "hosting" }},
            {{ id: "rack_2", name: "Rack 2U", description: "2U rack space, 2A power, 10Gbps port, unmetered bandwidth, remote hands.", price: 2999, features: ["2U Rack Space", "2A Power", "10 Gbps Port", "Unmetered Bandwidth"], isPopular: true, category: "rack", type: "hosting" }},
            {{ id: "rack_3", name: "Rack Cabinet", description: "Full 42U cabinet, 10A power, 10Gbps fiber, 24/7 onsite support, SLA.", price: 7999, features: ["42U Cabinet", "10A Power", "10 Gbps Fiber", "24/7 Onsite Support"], isPopular: false, category: "rack", type: "hosting" }}
        ],
        whmcs: [
            {{ id: "whmcs_1", name: "WHMCS Starter", description: "Billing automation for up to 250 clients. Includes support and updates.", price: 1599, features: ["250 Clients", "Invoicing", "Support System", "Monthly Updates"], isPopular: false, category: "whmcs", type: "hosting", isOneTime: true }},
            {{ id: "whmcs_2", name: "WHMCS Professional", description: "Unlimited clients, automated provisioning, mobile app, and 24/7 priority support.", price: 2999, features: ["Unlimited Clients", "Auto Provisioning", "Mobile App", "Priority Support"], isPopular: true, category: "whmcs", type: "hosting", isOneTime: true }},
            {{ id: "whmcs_3", name: "WHMCS Enterprise", description: "Full suite including custom modules, dedicated onboarding, and API access.", price: 5999, features: ["Custom Modules", "Dedicated Onboarding", "API Access", "SLA"], isPopular: false, category: "whmcs", type: "hosting", isOneTime: true }}
        ]
    }};

    // Domains – updated with new extensions and prices
    const domainProducts = {{
        domains: [
            {{ id: "domain_coza", name: ".CO.ZA", description: "South Africa's trusted domain for local businesses.", price: 256.10, features: ["Local Presence", "Free Privacy", "DNS Management"], isPopular: true, type: "domain", period: "year" }},
            {{ id: "domain_com", name: ".COM", description: "The most popular domain extension worldwide.", price: 375.70, features: ["Global Recognition", "Free Privacy", "DNS Management"], isPopular: true, type: "domain", period: "year" }},
            {{ id: "domain_net", name: ".NET", description: "Ideal for networking, tech, and infrastructure companies.", price: 427.70, features: ["Tech Focused", "Free Privacy", "DNS Management"], isPopular: false, type: "domain", period: "year" }},
            {{ id: "domain_org", name: ".ORG", description: "Perfect for non-profits, communities, and open source projects.", price: 325.00, features: ["Non-profit", "Free Privacy", "DNS Management"], isPopular: false, type: "domain", period: "year" }},
            {{ id: "domain_africa", name: ".AFRICA", description: "Pan-African domain – show your continental presence.", price: 310.70, features: ["Africa", "Free Privacy", "DNS Management"], isPopular: false, type: "domain", period: "year" }},
            {{ id: "domain_online", name: ".ONLINE", description: "Modern and versatile domain for any online venture.", price: 195.00, features: ["Modern", "Free Privacy", "DNS Management"], isPopular: false, type: "domain", period: "year" }},
            {{ id: "domain_store", name: ".STORE", description: "Perfect for e-commerce and retail websites.", price: 130.00, features: ["E-commerce", "Free Privacy", "DNS Management"], isPopular: false, type: "domain", period: "year" }},
            {{ id: "domain_site", name: ".SITE", description: "Generic domain for any website project.", price: 273.00, features: ["Versatile", "Free Privacy", "DNS Management"], isPopular: false, type: "domain", period: "year" }},
            {{ id: "domain_tech", name: ".TECH", description: "Highlight your tech-focused brand or startup.", price: 429.00, features: ["Tech", "Free Privacy", "DNS Management"], isPopular: false, type: "domain", period: "year" }}
        ],
        pointing: [
            {{ id: "pointing_basic", name: "Domain Pointing Basic", description: "Forward your domain to any existing website. Includes 5 forwarding rules.", price: 49, features: ["5 Forwarding Rules", "Masking Option", "Email Notifications"], isPopular: true, type: "domain", period: "year" }},
            {{ id: "pointing_pro", name: "Domain Pointing Pro", description: "Advanced domain forwarding with analytics and geo-targeting.", price: 99, features: ["Unlimited Rules", "Geo-Targeting", "Analytics Dashboard"], isPopular: false, type: "domain", period: "year" }}
        ]
    }};

    // Email products (unchanged, but we can add "Domain Email Bronze" if needed)
    const emailProducts = {{
        emails: [
            {{ id: "email_basic", name: "Email Lite", description: "Professional email hosting with 5GB storage per mailbox.", price: 29, features: ["5 GB Storage", "Webmail Access", "Mobile Sync", "Anti-Spam"], isPopular: false, type: "email", perUser: true, period: "month" }},
            {{ id: "email_pro", name: "Email Pro", description: "10GB storage, calendar, contacts, and advanced collaboration tools.", price: 49, features: ["10 GB Storage", "Calendar & Contacts", "Collaboration Tools", "24/7 Support"], isPopular: true, type: "email", perUser: true, period: "month" }},
            {{ id: "email_business", name: "Email Business", description: "Unlimited storage, archiving, eDiscovery, and compliance features.", price: 99, features: ["Unlimited Storage", "Archiving", "eDiscovery", "Compliance Tools"], isPopular: false, type: "email", perUser: true, period: "month" }}
        ],
        free_domain: [
            {{ id: "free_domain_offer", name: "Free Domain for 1 Year", description: "Get a free .com, .co.za, or .net domain when you sign up for any annual hosting plan.", price: 0, features: ["Free .COM/.CO.ZA/.NET", "Free Privacy Protection", "DNS Management"], isPopular: true, type: "email", isPromo: true }}
        ]
    }};

    // Design products (unchanged)
    const designProducts = {{
        custom: [
            {{ id: "design_luxe", name: "Luxe Obsidian", description: "Ultra-premium dark luxury theme with golden highlights, glassmorphism layers, and cinematic depth.", price: 11699, features: ["10 Pages", "99 Speed Index", "Glassmorphism", "Cinematic Layout"], isPopular: true, type: "design", previewKey: "luxe" }},
            {{ id: "design_emerald", name: "Emerald Neo", description: "High-tech neon layout with bright green highlights, deep carbon structures, clean code.", price: 7149, features: ["5 Pages", "Clean Code", "Neon Effects", "Tech Focused"], isPopular: false, type: "design", previewKey: "emerald" }},
            {{ id: "design_minimal", name: "Minimal Alabaster", description: "Ultra-clean light theme with crisp typography, soft gray backdrops, fluid grid.", price: 5199, features: ["3 Pages", "Fluid Grid", "Typography Focus", "E-commerce Ready"], isPopular: false, type: "design", previewKey: "minimal" }}
        ],
        ecom: [
            {{ id: "ecom_basic", name: "eCommerce Basic", description: "Fully functional online store with product catalog, cart, and secure checkout.", price: 8999, features: ["Up to 50 Products", "Payment Gateway", "Inventory Management", "Order Tracking"], isPopular: true, type: "ecom" }},
            {{ id: "ecom_pro", name: "eCommerce Pro", description: "Advanced eCommerce solution with multi-currency, abandoned cart recovery, and analytics.", price: 14999, features: ["Unlimited Products", "Multi-Currency", "Abandoned Cart", "Analytics Dashboard"], isPopular: false, type: "ecom" }},
            {{ id: "ecom_enterprise", name: "eCommerce Enterprise", description: "Scalable enterprise platform with custom workflows, API access, and dedicated support.", price: 29999, features: ["Custom Workflows", "API Access", "Dedicated Support", "High Volume"], isPopular: false, type: "ecom" }}
        ],
        sitebuilder: [
            {{ id: "builder_starter", name: "SiteBuilder Starter", description: "Drag-and-drop website builder with 50+ templates, mobile responsive, and free SSL.", price: 199, features: ["50+ Templates", "Drag & Drop", "Free SSL", "Mobile Responsive"], isPopular: false, type: "sitebuilder", period: "month" }},
            {{ id: "builder_pro", name: "SiteBuilder Pro", description: "Advanced builder with custom domains, eCommerce tools, and priority support.", price: 399, features: ["Custom Domains", "eCommerce Tools", "Priority Support", "Analytics"], isPopular: true, type: "sitebuilder", period: "month" }},
            {{ id: "builder_business", name: "SiteBuilder Business", description: "Unlimited sites, team collaboration, white-label options, and premium templates.", price: 799, features: ["Unlimited Sites", "Team Collaboration", "White-label", "Premium Templates"], isPopular: false, type: "sitebuilder", period: "month" }}
        ]
    }};

    // ==================== COVERAGE SEARCH FUNCTIONS ====================
    function searchCoverage(searchTerm) {{
        if (!searchTerm || searchTerm.trim() === '') return [];
        const term = searchTerm.toLowerCase().trim();
        return coverageAreas.filter(area => 
            area.name.toLowerCase().includes(term) ||
            area.city.toLowerCase().includes(term)
        );
    }}

    function setupSearchAutocomplete() {{
        const inputField = document.getElementById('area-search');
        const dropDownContainer = document.getElementById('search-dropdown');
        if (!inputField) return;
        
        inputField.addEventListener('input', () => {{
            const inputVal = inputField.value.trim();
            dropDownContainer.innerHTML = '';
            if (!inputVal) {{
                dropDownContainer.classList.add('hidden');
                return;
            }}
            
            const matches = searchCoverage(inputVal);
            
            if (matches.length === 0) {{
                dropDownContainer.innerHTML = `<div class="p-3.5 text-xs text-gray-400">📍 No coverage data found. Contact us to check availability!</div>`;
            }} else {{
                matches.slice(0, 8).forEach(match => {{
                    const itemDiv = document.createElement('div');
                    itemDiv.className = "p-3 hover:bg-white/5 cursor-pointer flex justify-between items-center transition-all border-b border-white/5 last:border-b-0";
                    
                    let statusBadge = '';
                    let statusColor = '';
                    if (match.status === 'available') {{
                        statusBadge = '✓ Available';
                        statusColor = 'bg-brand-green/10 text-brand-green';
                    }} else if (match.status === 'coming_soon') {{
                        statusBadge = '⏰ Coming Soon';
                        statusColor = 'bg-brand-gold/10 text-brand-gold';
                    }} else {{
                        statusBadge = '📋 Planned';
                        statusColor = 'bg-gray-500/10 text-gray-400';
                    }}
                    
                    itemDiv.innerHTML = `
                        <div>
                            <div class="font-bold text-white text-sm">${{match.name}}</div>
                            <div class="text-[10px] text-gray-500">${{match.city}}, ${{match.province}}</div>
                        </div>
                        <div class="text-[9px] ${{statusColor}} font-bold px-2 py-0.5 rounded-full uppercase tracking-wide">
                            ${{statusBadge}}
                        </div>
                    `;
                    
                    itemDiv.onclick = () => {{
                        inputField.value = match.name;
                        dropDownContainer.classList.add('hidden');
                        displaySearchResult(match);
                    }};
                    
                    dropDownContainer.appendChild(itemDiv);
                }});
                
                if (matches.length > 8) {{
                    const moreDiv = document.createElement('div');
                    moreDiv.className = "p-2 text-center text-[10px] text-gray-500";
                    moreDiv.innerHTML = `<i class="fas fa-ellipsis-h"></i> ${{matches.length - 8}} more results`;
                    dropDownContainer.appendChild(moreDiv);
                }}
            }}
            
            dropDownContainer.classList.remove('hidden');
        }});
        
        document.addEventListener('click', (e) => {{
            if (!inputField.contains(e.target) && !dropDownContainer.contains(e.target)) {{
                dropDownContainer.classList.add('hidden');
            }}
        }});
    }}

    function triggerSearch() {{
        const searchVal = document.getElementById('area-search').value.trim();
        if (!searchVal) {{
            displaySearchFeedback("🏠 Please enter a suburb, city, or street name to check coverage.", false);
            return;
        }}
        
        const matches = searchCoverage(searchVal);
        
        if (matches.length === 0) {{
            displaySearchFeedback(`
                <div class="text-center">
                    <i class="fas fa-map-marked-alt text-2xl mb-2 block"></i>
                    <strong>No coverage found for "${{searchVal}}"</strong><br>
                    <span class="text-xs">Our network is expanding monthly. <button onclick="openInterestForm()" class="text-brand-gold underline">Notify me when available</button></span>
                </div>
            `, false);
            return;
        }}
        
        displaySearchResult(matches[0]);
        
        if (matches.length > 1) {{
            const resultsDiv = document.getElementById('search-result');
            const otherAreas = matches.slice(1, 4);
            const otherHtml = `
                <div class="mt-3 pt-3 border-t border-white/10">
                    <div class="text-[10px] text-gray-500 mb-2">📍 Also available in:</div>
                    <div class="flex flex-wrap gap-2">
                        ${{otherAreas.map(area => `
                            <button onclick="displaySearchResult(${{JSON.stringify(area).replace(/"/g, '&quot;')}})" 
                                    class="text-[9px] bg-white/5 hover:bg-white/10 px-2 py-1 rounded-full transition-colors">
                                ${{area.name}}
                            </button>
                        `).join('')}}
                    </div>
                </div>
            `;
            resultsDiv.insertAdjacentHTML('beforeend', otherHtml);
        }}
    }}

    function displaySearchResult(area) {{
        const resultsDiv = document.getElementById('search-result');
        resultsDiv.classList.remove('hidden');
        
        if (area.status === 'available') {{
            const maxSpeedDisplay = area.max_speed ? `${{area.max_speed}} Mbps` : 'Gigabit';
            
            resultsDiv.className = "mt-6 p-5 rounded-2xl border border-brand-green/20 bg-brand-green/5 text-gray-300";
            resultsDiv.innerHTML = `
                <div class="flex items-start gap-3 text-xs">
                    <div class="h-10 w-10 bg-brand-green/15 rounded-xl flex items-center justify-center text-brand-green text-xl shrink-0 shadow-inner">
                        <i class="fa-solid fa-tower-cell"></i>
                    </div>
                    <div class="space-y-2 flex-1">
                        <div class="flex items-center justify-between flex-wrap gap-2">
                            <h5 class="font-bold text-white text-base">✓ ${{area.name}} is Fibre Ready!</h5>
                            <span class="text-[9px] bg-brand-green/20 text-brand-green px-2 py-0.5 rounded-full">${{area.provider}}</span>
                        </div>
                        <p class="text-gray-400 text-sm leading-relaxed">
                            ${{area.provider}} fibre infrastructure is live in ${{area.name}}. 
                            Get symmetrical speeds up to <span class="text-white font-bold">${{maxSpeedDisplay}}</span>.
                        </p>
                        <div class="grid grid-cols-2 gap-3 text-[10px] text-gray-400 bg-black/20 p-2 rounded-lg">
                            <div><i class="fas fa-arrow-up text-brand-green mr-1"></i> Symmetrical Upload/Download</div>
                            <div><i class="fas fa-infinity text-brand-gold mr-1"></i> Uncapped & Unshaped</div>
                            <div><i class="fas fa-wifi text-brand-green mr-1"></i> Free Wi-Fi 6 Router</div>
                            <div><i class="fas fa-tools text-brand-gold mr-1"></i> Free Installation</div>
                        </div>
                        <div class="pt-2 flex gap-3">
                            <button onclick="autoSelectProvider('${{area.provider}}')" class="bg-brand-green hover:bg-brand-greenDark text-white px-5 py-2.5 rounded-full font-bold text-[10px] tracking-wider uppercase transition-colors shadow-md">
                                <i class="fas fa-tags mr-1"></i> View Packages
                            </button>
                            <button onclick="openCheckoutModal()" class="glossy-gold text-brand-black px-5 py-2.5 rounded-full font-bold text-[10px] tracking-wider uppercase transition-colors shadow-md">
                                <i class="fas fa-bolt mr-1"></i> Order Now
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }} else if (area.status === 'coming_soon') {{
            resultsDiv.className = "mt-6 p-5 rounded-2xl border border-brand-gold/20 bg-brand-gold/5 text-gray-300";
            resultsDiv.innerHTML = `
                <div class="flex items-start gap-3 text-xs">
                    <div class="h-10 w-10 bg-brand-gold/15 rounded-xl flex items-center justify-center text-brand-gold text-xl shrink-0 shadow-inner">
                        <i class="fa-solid fa-clock"></i>
                    </div>
                    <div class="space-y-2 flex-1">
                        <h5 class="font-bold text-white text-base">🚀 Coming Soon to ${{area.name}}!</h5>
                        <p class="text-gray-400 text-sm">
                            ${{area.provider}} is deploying fibre infrastructure in your area.
                            Estimated availability: <span class="text-brand-gold font-bold">${{area.estimated_date || 'TBA'}}</span>
                        </p>
                        <div class="bg-black/30 p-3 rounded-lg">
                            <p class="text-[10px] text-gray-400">
                                <i class="fas fa-gift text-brand-gold mr-1"></i> 
                                <strong>Pre-registration bonus:</strong> 20% off first 3 months + free installation
                            </p>
                        </div>
                        <div class="pt-2">
                            <button onclick="openPreRegister('${{area.name}}')" class="glossy-gold text-brand-black px-5 py-2.5 rounded-full font-bold text-[10px] tracking-wider uppercase transition-colors shadow-md">
                                <i class="fas fa-envelope mr-1"></i> Pre-Register Interest
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }} else {{
            resultsDiv.className = "mt-6 p-5 rounded-2xl border border-gray-500/20 bg-gray-500/5 text-gray-300";
            resultsDiv.innerHTML = `
                <div class="flex items-start gap-3 text-xs">
                    <div class="h-10 w-10 bg-gray-500/15 rounded-xl flex items-center justify-center text-gray-400 text-xl shrink-0 shadow-inner">
                        <i class="fa-solid fa-draw-polygon"></i>
                    </div>
                    <div class="space-y-2 flex-1">
                        <h5 class="font-bold text-white text-base">📋 Planned Coverage: ${{area.name}}</h5>
                        <p class="text-gray-400 text-sm">
                            ${{area.provider}} has ${{area.name}} in their rollout plan.
                            Target: <span class="text-brand-gold font-bold">${{area.estimated_date || 'To be confirmed'}}</span>
                        </p>
                        <div class="bg-black/30 p-3 rounded-lg">
                            <p class="text-[10px] text-gray-400">
                                <i class="fas fa-users text-brand-gold mr-1"></i> 
                                Help us prioritize: each interest expression accelerates deployment
                            </p>
                        </div>
                        <div class="pt-2">
                            <button onclick="openExpressInterest('${{area.name}}')" class="glossy-black text-white px-5 py-2.5 rounded-full font-bold text-[10px] tracking-wider uppercase transition-colors shadow-md">
                                <i class="fas fa-thumbs-up mr-1"></i> Express Interest
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }}
    }}

    function displaySearchFeedback(msg, isSuccess) {{
        const resultsDiv = document.getElementById('search-result');
        resultsDiv.classList.remove('hidden');
        resultsDiv.className = isSuccess 
            ? "mt-6 p-4 rounded-2xl border border-brand-green/20 bg-brand-green/5 text-brand-green text-xs font-semibold" 
            : "mt-6 p-4 rounded-2xl border border-red-500/20 bg-red-500/5 text-red-400 text-xs font-semibold";
        resultsDiv.innerHTML = msg;
    }}

    function openPreRegister(areaName) {{
        const modal = document.createElement('div');
        modal.className = "fixed inset-0 z-[200] flex items-center justify-center p-4 bg-brand-black/90 backdrop-blur-md";
        modal.innerHTML = `
            <div class="bg-brand-darkGray rounded-3xl max-w-md w-full p-6 border border-brand-gold/20 text-white shadow-2xl">
                <div class="text-center mb-4">
                    <div class="h-12 w-12 bg-brand-gold/15 rounded-full flex items-center justify-center text-brand-gold text-xl mx-auto">
                        <i class="fas fa-bell"></i>
                    </div>
                    <h3 class="text-xl font-bold mt-3">Pre-Register for ${{areaName}}</h3>
                    <p class="text-sm text-gray-400 mt-1">Get notified when fibre arrives + exclusive launch discount</p>
                </div>
                <div class="space-y-3">
                    <input type="text" id="prereg-name" placeholder="Full name" class="w-full px-4 py-3 bg-brand-black border border-white/10 rounded-xl text-white focus:ring-2 focus:ring-brand-gold">
                    <input type="email" id="prereg-email" placeholder="Email address" class="w-full px-4 py-3 bg-brand-black border border-white/10 rounded-xl text-white focus:ring-2 focus:ring-brand-gold">
                    <input type="tel" id="prereg-phone" placeholder="Phone number (optional)" class="w-full px-4 py-3 bg-brand-black border border-white/10 rounded-xl text-white focus:ring-2 focus:ring-brand-gold">
                </div>
                <div class="flex gap-3 mt-6">
                    <button onclick="submitPreRegister('${{areaName}}')" class="flex-1 glossy-gold text-brand-black py-3 rounded-xl font-bold text-sm">Submit</button>
                    <button onclick="this.closest('.fixed').remove()" class="flex-1 glossy-black text-white py-3 rounded-xl font-bold text-sm">Cancel</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }}

    function submitPreRegister(areaName) {{
        const name = document.getElementById('prereg-name')?.value || '';
        const email = document.getElementById('prereg-email')?.value;
        const phone = document.getElementById('prereg-phone')?.value || '';
        
        if (!email) {{
            alertModal("Please enter your email address.");
            return;
        }}
        
        console.log(`Pre-registration for ${{areaName}}:`, {{ name, email, phone }});
        
        document.querySelector('.fixed[style*="z-index: 200"]')?.remove();
        
        const success = document.createElement('div');
        success.className = "fixed bottom-6 right-6 z-50 bg-brand-green text-brand-black px-6 py-3 rounded-xl shadow-lg text-sm font-bold animate-bounce";
        success.innerHTML = `<i class="fas fa-check-circle mr-2"></i> Registered! We'll notify you when ${{areaName}} goes live.`;
        document.body.appendChild(success);
        setTimeout(() => success.remove(), 5000);
    }}

    function openExpressInterest(areaName) {{
        openPreRegister(areaName);
    }}

    function openInterestForm() {{
        openPreRegister("your area");
    }}

    function autoSelectProvider(providerName) {{
        // Not used for hosting, but keep for compatibility
        setMainCategory('hostings');
        setSubCategory('shared');
        showPage('host');
        document.getElementById('packages').scrollIntoView({{ behavior: 'smooth' }});
    }}

    // ==================== AUTHENTICATION ====================
    function getAuthToken() {{
        return localStorage.getItem("access_token");
    }}

    function setAuthToken(token) {{
        if (token) localStorage.setItem("access_token", token);
        else localStorage.removeItem("access_token");
    }}

    function isAuthenticated() {{
        return !!getAuthToken();
    }}

    async function authenticatedFetch(endpoint, options = {{}}) {{
        const token = getAuthToken();
        if (!token) throw new Error("Not authenticated");
        const headers = {{
            "Authorization": `Bearer ${{token}}`,
            "Content-Type": "application/json",
            ...options.headers
        }};
        const response = await fetch(`${{API_BASE}}${{endpoint}}`, {{ ...options, headers }});
        if (response.status === 401) {{
            setAuthToken(null);
            alertModal("Session expired. Please log in again.");
            triggerClientZone();
            throw new Error("Unauthorized");
        }}
        return response;
    }}

    async function registerUser() {{
        const name = document.getElementById("reg-name")?.value.trim();
        const email = document.getElementById("reg-email")?.value.trim();
        const password = document.getElementById("reg-password")?.value;
        if (!name || !email || !password) {{
            alertModal("Please fill all fields.");
            return;
        }}
        try {{
            const response = await fetch(`${{API_BASE}}/auth/register`, {{
                method: "POST",
                headers: {{ "Content-Type": "application/json" }},
                body: JSON.stringify({{ name, email, password }})
            }});
            const data = await response.json();
            if (!response.ok) throw new Error(data.detail || "Registration failed");
            setAuthToken(data.access_token);
            closeRegisterModal();
            await loadUserDashboard();
            alertModal("Account created and logged in successfully!");
        }} catch (err) {{
            alertModal(err.message);
        }}
    }}

    async function loginUser(email, password) {{
        const formData = new URLSearchParams();
        formData.append("username", email);
        formData.append("password", password);
        const response = await fetch(`${{API_BASE}}/auth/login`, {{
            method: "POST",
            headers: {{ "Content-Type": "application/x-www-form-urlencoded" }},
            body: formData
        }});
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || "Login failed");
        setAuthToken(data.access_token);
        return true;
    }}

    // ==================== CLIENT ZONE PORTAL FUNCTIONS ====================
    
    async function loadUserDashboard() {{
        if (!isAuthenticated()) return;
        try {{
            const userResp = await authenticatedFetch("/auth/me");
            const user = await userResp.json();
            const ordersResp = await authenticatedFetch("/orders");
            const orders = await ordersResp.json();

            // Show portal view, hide login
            document.getElementById('cz-login-view').classList.add('hidden');
            document.getElementById('cz-portal-view').classList.remove('hidden');

            // Fill user info
            document.getElementById('cz-user-name').textContent = user.name || 'User';
            document.getElementById('cz-user-email').textContent = user.email;
            document.getElementById('cz-profile-name').value = user.name || '';
            document.getElementById('cz-profile-email').value = user.email;
            document.getElementById('cz-profile-phone').value = user.phone || '';
            document.getElementById('cz-profile-address').value = user.address || '';

            // Update stats
            const activeServices = orders.filter(o => o.status === 'active' || o.status === 'completed').length;
            document.getElementById('cz-service-count').textContent = activeServices;
            document.getElementById('cz-order-count').textContent = orders.length;

            // Populate orders list
            const ordersList = document.getElementById('cz-orders-list');
            if (orders.length === 0) {{
                ordersList.innerHTML = '<div class="text-gray-400">No orders yet.</div>';
            }} else {{
                ordersList.innerHTML = orders.map(order => `
                    <div class="bg-brand-darkGray/40 p-3 rounded-lg border border-white/5 flex justify-between items-center">
                        <div>
                            <div class="font-bold text-white text-xs">Order #${{order.id}}</div>
                            <div class="text-[10px] text-gray-400">${{order.items.length}} items • ${{new Date(order.created_at).toLocaleDateString()}}</div>
                        </div>
                        <div class="text-right">
                            <div class="text-brand-gold font-bold text-xs">R${{(order.total/100).toFixed(2)}}</div>
                            <div class="text-[9px] uppercase ${{order.status === 'completed' ? 'text-brand-green' : 'text-brand-gold'}}">${{order.status}}</div>
                        </div>
                    </div>
                `).join('');
            }}

            // Show modal
            document.getElementById('clientzone-modal').classList.remove('hidden');

            // Set default tab
            switchClientZoneTab('dashboard');

        }} catch (err) {{
            alertModal("Could not load dashboard: " + err.message);
        }}
    }}

    function switchClientZoneTab(tabName) {{
        // Hide all panels
        document.querySelectorAll('.cz-tab-panel').forEach(p => p.classList.add('hidden'));
        // Show selected panel
        const panel = document.getElementById('cz-' + tabName);
        if (panel) panel.classList.remove('hidden');

        // Update tab button styles
        document.querySelectorAll('.cz-tab-btn').forEach(btn => {{
            btn.classList.remove('text-brand-gold', 'border-brand-gold');
            btn.classList.add('text-gray-400', 'border-transparent');
            if (btn.dataset.tab === tabName) {{
                btn.classList.remove('text-gray-400', 'border-transparent');
                btn.classList.add('text-brand-gold', 'border-brand-gold');
            }}
        }});
    }}

    function logoutClientZone() {{
        setAuthToken(null);
        closeClientZone();
        alertModal("You have been logged out.");
    }}

    function saveProfile() {{
        // Dummy – in real implementation, send to backend
        alertModal("Profile updated successfully!");
    }}

    function submitSupportTicket() {{
        const subject = document.getElementById('cz-support-subject').value.trim();
        const message = document.getElementById('cz-support-message').value.trim();
        if (!subject || !message) {{
            alertModal("Please fill in both subject and message.");
            return;
        }}
        // Dummy – in real implementation, send to backend
        alertModal("Support ticket submitted! We'll respond within 24 hours.");
        document.getElementById('cz-support-subject').value = '';
        document.getElementById('cz-support-message').value = '';
    }}

    function closeClientZone() {{
        const modal = document.getElementById('clientzone-modal');
        modal.classList.add('hidden');
        // Reset to login view so next open shows login
        document.getElementById('cz-login-view').classList.remove('hidden');
        document.getElementById('cz-portal-view').classList.add('hidden');
        // Reset tab to dashboard
        switchClientZoneTab('dashboard');
        // Clear form fields
        document.getElementById('cz-email').value = '';
        document.getElementById('cz-password').value = '';
    }}

    async function submitClientZone() {{
        const email = document.getElementById("cz-email")?.value.trim();
        const password = document.getElementById("cz-password")?.value;
        if (!email || !password) {{
            alertModal("Please enter email and password.");
            return;
        }}
        try {{
            await loginUser(email, password);
            closeClientZone(); // close login modal
            await loadUserDashboard(); // opens portal
        }} catch (err) {{
            alertModal(err.message);
        }}
    }}

    function openRegisterModal() {{
        document.getElementById('register-modal').classList.remove('hidden');
    }}

    function closeRegisterModal() {{
        document.getElementById('register-modal').classList.add('hidden');
    }}

    function triggerClientZone() {{
        if (isAuthenticated()) {{
            loadUserDashboard();
        }} else {{
            // Ensure the modal has the correct login form (in case it was reset)
            document.getElementById('cz-login-view').classList.remove('hidden');
            document.getElementById('cz-portal-view').classList.add('hidden');
            document.getElementById('clientzone-modal').classList.remove('hidden');
        }}
    }}

    // Attach tab click listeners after DOM ready
    document.addEventListener('DOMContentLoaded', function() {{
        document.querySelectorAll('.cz-tab-btn').forEach(btn => {{
            btn.addEventListener('click', function() {{
                switchClientZoneTab(this.dataset.tab);
            }});
        }});
    }});

    // ==================== GLOBAL VARIABLES ====================
    let cart = [];
    let currentMainCategory = 'all';
    let currentSubCategory = 'all';
    let currentDesignCategory = 'all';
    let currentModalStep = 2;

    // ==================== HELPER FUNCTIONS ====================
    function toggleNotificationDropdown(event) {{ event.stopPropagation(); const panel = document.getElementById('notify-dropdown-panel'); const cartPanel = document.getElementById('cart-dropdown-panel'); panel.classList.toggle('hidden'); cartPanel.classList.add('hidden'); const pulse = document.getElementById('notify-pulse-dot'); if(pulse) pulse.remove(); }}
    function toggleCartDropdown(event) {{ event.stopPropagation(); const panel = document.getElementById('cart-dropdown-panel'); const notifyPanel = document.getElementById('notify-dropdown-panel'); panel.classList.toggle('hidden'); notifyPanel.classList.add('hidden'); }}
    document.addEventListener('click', (event) => {{ const notifyPanel = document.getElementById('notify-dropdown-panel'); const cartPanel = document.getElementById('cart-dropdown-panel'); if(notifyPanel && !notifyPanel.contains(event.target)) notifyPanel.classList.add('hidden'); if(cartPanel && !cartPanel.contains(event.target)) cartPanel.classList.add('hidden'); }});

    function addToCart(type, itemId) {{
        let itemObject = null;
        // Search in internet products
        for (let cat in internetProducts) {{
            const found = internetProducts[cat].find(p => p.id == itemId);
            if (found) {{
                itemObject = {{ 
                    cartId: 'internet-'+itemId+'-'+Date.now(), 
                    type: 'internet', 
                    id: found.id, 
                    name: found.name, 
                    price: found.price, 
                    category: found.category,
                    addons: {{}}
                }};
                break;
            }}
        }}
        // Search in hosting products
        if (!itemObject) {{
            for (let cat in hostingProducts) {{
                const found = hostingProducts[cat].find(p => p.id == itemId);
                if (found) {{
                    itemObject = {{ 
                        cartId: 'host-'+itemId+'-'+Date.now(), 
                        type: 'host', 
                        id: found.id, 
                        name: found.name, 
                        price: found.price, 
                        category: found.category,
                        addons: {{ extra_storage: false, priority: false }}
                    }};
                    break;
                }}
            }}
        }}
        // Search in domain products
        if (!itemObject) {{
            for (let cat in domainProducts) {{
                const found = domainProducts[cat].find(p => p.id == itemId);
                if (found) {{
                    itemObject = {{ 
                        cartId: 'domain-'+itemId+'-'+Date.now(), 
                        type: 'domain', 
                        id: found.id, 
                        name: found.name, 
                        price: found.price, 
                        category: found.type,
                        period: found.period || 'year',
                        addons: {{}}
                    }};
                    break;
                }}
            }}
        }}
        // Search in email products
        if (!itemObject) {{
            for (let cat in emailProducts) {{
                const found = emailProducts[cat].find(p => p.id == itemId);
                if (found) {{
                    itemObject = {{ 
                        cartId: 'email-'+itemId+'-'+Date.now(), 
                        type: 'email', 
                        id: found.id, 
                        name: found.name, 
                        price: found.price, 
                        category: found.type,
                        addons: {{}}
                    }};
                    break;
                }}
            }}
        }}
        // Search in design products
        if (!itemObject) {{
            for (let cat in designProducts) {{
                const found = designProducts[cat].find(p => p.id == itemId);
                if (found) {{
                    itemObject = {{ 
                        cartId: 'design-'+itemId+'-'+Date.now(), 
                        type: 'design', 
                        id: found.id, 
                        name: found.name, 
                        price: found.price, 
                        category: found.type,
                        addons: {{}}
                    }};
                    break;
                }}
            }}
        }}
        if(itemObject) {{ 
            cart.push(itemObject); 
            updateCartUI(); 
            animateCartIcon(); 
            showPreorderToast(itemObject.name + " Added to Cart!"); 
        }}
    }}
    
    function directBuy(type, itemId) {{ 
        cart = []; 
        addToCart(type, itemId); 
        openCheckoutModal(); 
    }}
    
    function removeFromCart(cartId) {{ 
        cart = cart.filter(item => item.cartId !== cartId); 
        updateCartUI(); 
    }}
    
    function clearCart() {{ 
        cart = []; 
        updateCartUI(); 
    }}
    
    function toggleCartAddon(cartId, addonKey, checked) {{ 
        const item = cart.find(i => i.cartId === cartId); 
        if(item) {{ 
            item.addons[addonKey] = checked; 
            updateCartUI(); 
        }} 
    }}
    
    function animateCartIcon() {{ 
        const btn = document.getElementById('cart-btn'); 
        if(btn) {{ 
            btn.classList.add('cart-bounce','border-brand-gold'); 
            setTimeout(() => btn.classList.remove('cart-bounce'),400); 
        }} 
    }}
    
    function showPreorderToast(message) {{ 
        const toast = document.getElementById('order-toast'); 
        const toastText = toast.querySelector('p'); 
        const toastHeader = toast.querySelector('h5'); 
        toastHeader.innerText = "Shopping Bag Updated"; 
        toastText.innerText = message; 
        toast.classList.remove('hidden'); 
        setTimeout(() => toast.classList.add('hidden'),5000); 
    }}
    
    function updateCartUI() {{
        const badge = document.getElementById('header-cart-badge'); 
        const content = document.getElementById('cart-dropdown-content');
        if(cart.length===0) {{ 
            badge.classList.add('hidden'); 
            badge.innerText='0'; 
            content.className="text-[10px] text-gray-400 text-center py-4 space-y-3"; 
            content.innerHTML=`<i class="fa-solid fa-basket-shopping text-2xl text-gray-600 block"></i><span>No products added yet.</span>`; 
            return; 
        }}
        badge.classList.remove('hidden'); 
        badge.innerText=cart.length; 
        let html=`<div class="max-h-76 overflow-y-auto space-y-3.5 pr-1.5 scrollbar-thin">`; 
        let subtotal=0;
        cart.forEach(item => {{
            let itemTotal=item.price; 
            let addoneSection='';
            if(item.type==='host') {{ 
                if(item.addons.extra_storage) itemTotal+=129; 
                if(item.addons.priority) itemTotal+=64; 
                addoneSection=`<div class="grid grid-cols-2 gap-2 mt-2 pt-2 border-t border-white/5 text-[8px] text-gray-400"><label class="flex items-center gap-1 cursor-pointer"><input type="checkbox" onchange="toggleCartAddon('${{item.cartId}}', 'extra_storage', this.checked)" ${{item.addons.extra_storage ? 'checked' : ''}} class="h-3 w-3 bg-brand-slateBlack border-white/10 rounded accent-brand-gold text-brand-black"><span>Extra Storage (+R129)</span></label><label class="flex items-center gap-1 cursor-pointer"><input type="checkbox" onchange="toggleCartAddon('${{item.cartId}}', 'priority', this.checked)" ${{item.addons.priority ? 'checked' : ''}} class="h-3 w-3 bg-brand-slateBlack border-white/10 rounded accent-brand-gold text-brand-black"><span>Priority Support (+R64)</span></label></div>`; 
            }}
            else if(item.type==='domain') {{
                addoneSection = `<div class="mt-2 pt-2 border-t border-white/5 text-[8px] text-gray-400 text-center">${{item.period ? 'Billed annually' : 'One-time'}}</div>`;
            }}
            else if(item.type==='email') {{
                if(item.price === 0) {{
                    addoneSection = `<div class="mt-2 pt-2 border-t border-white/5 text-[8px] text-brand-green text-center">✓ Promotional Offer - Limited Time</div>`;
                }} else {{
                    addoneSection = `<div class="mt-2 pt-2 border-t border-white/5 text-[8px] text-gray-400 text-center">Per user / month</div>`;
                }}
            }}
            else if(item.type==='design') {{
                addoneSection = `<div class="mt-2 pt-2 border-t border-white/5 text-[8px] text-gray-400 text-center">Once-off payment, includes source code</div>`;
            }}
            else if(item.type==='internet') {{
                addoneSection = `<div class="mt-2 pt-2 border-t border-white/5 text-[8px] text-gray-400 text-center">${{item.category === 'fibre' ? 'Monthly recurring' : (item.category === 'devices' ? 'One-time purchase' : 'Monthly subscription')}}</div>`;
            }}
            subtotal+=itemTotal;
            html+=`<div class="p-3 bg-white/5 rounded-xl border border-white/5 flex flex-col justify-between"><div class="flex justify-between items-start gap-2"><div class="text-left"><span class="font-bold text-white block truncate max-w-[150px]">${{item.name}}</span><span class="text-[8px] text-gray-500 uppercase block tracking-wider">${{item.type==='host'?'Hosting':(item.type==='domain'?'Domain':(item.type==='email'?'Email':(item.type==='design'?'Design':'Internet')))}}</span></div><div class="flex items-center gap-2"><span class="font-extrabold text-brand-gold shrink-0">R${{itemTotal.toFixed(2)}}</span><button onclick="removeFromCart('${{item.cartId}}')" class="text-gray-500 hover:text-red-400 text-xs transition-colors"><i class="fa-solid fa-trash-can"></i></button></div></div>${{addoneSection}}</div>`;
        }});
        html+=`</div><div class="border-t border-white/10 pt-3 mt-3 space-y-3.5"><div class="flex justify-between text-xs font-bold"><span>Cart Subtotal:</span><span class="text-brand-gold text-sm font-black">R${{subtotal.toFixed(2)}}</span></div><button onclick="openCheckoutModal()" class="w-full text-center glossy-gold text-brand-black py-2.5 rounded-xl font-bold text-[9px] uppercase tracking-wider shadow-md">Proceed to Checkout</button></div>`;
        content.className="text-[10px] text-gray-300 text-left"; 
        content.innerHTML=html;
    }}

    function toggleSidebar() {{ 
        const drawer = document.getElementById('sidebar-drawer'); 
        const backdrop = document.getElementById('sidebar-backdrop'); 
        if(drawer.classList.contains('-translate-x-full')) {{ 
            drawer.classList.remove('-translate-x-full'); 
            backdrop.classList.remove('hidden'); 
            setTimeout(()=>backdrop.classList.add('opacity-100'),50); 
        }} else {{ 
            drawer.classList.add('-translate-x-full'); 
            backdrop.classList.remove('opacity-100'); 
            setTimeout(()=>backdrop.classList.add('hidden'),300); 
        }} 
    }}

    const PAGES = ['home', 'host', 'design', 'cloud'];
    function showPage(pageName) {{
        PAGES.forEach(p => {{ 
            const el = document.getElementById('page-'+p); 
            if(el) el.classList.add('hidden'); 
            const btn = document.getElementById('nav-'+p); 
            if(btn) btn.classList.remove('text-brand-gold'); 
        }});
        const target = document.getElementById('page-'+pageName); 
        if(target) target.classList.remove('hidden');
        const activeBtn = document.getElementById('nav-'+pageName); 
        if(activeBtn) activeBtn.classList.add('text-brand-gold');
        window.scrollTo(0,0);
        if(pageName === 'host') renderProducts();
        if(pageName === 'design') renderDesignProducts();
        if(pageName === 'cloud') renderCloudPlans();
    }}

    // Host page functions
    function setMainCategory(category) {{
        currentMainCategory = category;
        currentSubCategory = 'all';
        document.querySelectorAll('.main-cat-tab').forEach(tab => tab.className = "main-cat-tab flex-1 px-5 py-2.5 rounded-xl font-bold text-xs tracking-wider uppercase transition-all text-gray-500 hover:bg-white/50");
        const activeTab = document.getElementById(`tab-${{category}}`);
        if(activeTab) activeTab.className = "main-cat-tab flex-1 px-5 py-2.5 rounded-xl font-bold text-xs tracking-wider uppercase transition-all text-brand-goldDark bg-white shadow-sm";
        
        // Update subcategory filters based on main category
        const subFiltersDiv = document.getElementById('subcategory-filters');
        if (!subFiltersDiv) return;
        
        if (category === 'hostings') {{
            subFiltersDiv.innerHTML = `
                <button onclick="setSubCategory('shared')" id="sub-shared" class="sub-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-black/10 bg-white text-gray-600 hover:border-brand-gold transition-all shadow-sm">Shared</button>
                <button onclick="setSubCategory('cloudhosting')" id="sub-cloudhosting" class="sub-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-black/10 bg-white text-gray-600 hover:border-brand-gold transition-all shadow-sm">Cloud</button>
                <button onclick="setSubCategory('reseller')" id="sub-reseller" class="sub-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-black/10 bg-white text-gray-600 hover:border-brand-gold transition-all shadow-sm">Reseller Hosting</button>
                <button onclick="setSubCategory('dedicated')" id="sub-dedicated" class="sub-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-black/10 bg-white text-gray-600 hover:border-brand-gold transition-all shadow-sm">Dedicated Hosting</button>
                <button onclick="setSubCategory('rack')" id="sub-rack" class="sub-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-black/10 bg-white text-gray-600 hover:border-brand-gold transition-all shadow-sm">Rack Hosting</button>
                <button onclick="setSubCategory('whmcs')" id="sub-whmcs" class="sub-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-black/10 bg-white text-gray-600 hover:border-brand-gold transition-all shadow-sm">WHMCS</button>
            `;
        }} else if (category === 'domains') {{
            subFiltersDiv.innerHTML = `
                <button onclick="setSubCategory('domains')" id="sub-domains" class="sub-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-black/10 bg-white text-gray-600 hover:border-brand-gold transition-all shadow-sm">Domains</button>
                <button onclick="setSubCategory('pointing')" id="sub-pointing" class="sub-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-black/10 bg-white text-gray-600 hover:border-brand-gold transition-all shadow-sm">Pointing</button>
            `;
        }} else if (category === 'emails') {{
            subFiltersDiv.innerHTML = `
                <button onclick="setSubCategory('emails')" id="sub-emails" class="sub-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-black/10 bg-white text-gray-600 hover:border-brand-gold transition-all shadow-sm">Emails</button>
                <button onclick="setSubCategory('free_domain')" id="sub-free_domain" class="sub-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-black/10 bg-white text-gray-600 hover:border-brand-gold transition-all shadow-sm">Free domain for 1 year</button>
            `;
        }} else if (category === 'internet') {{
            subFiltersDiv.innerHTML = `
                <button onclick="setSubCategory('fibre')" id="sub-fibre" class="sub-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-black/10 bg-white text-gray-600 hover:border-brand-gold transition-all shadow-sm">Fibre</button>
                <button onclick="setSubCategory('prepaid')" id="sub-prepaid" class="sub-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-black/10 bg-white text-gray-600 hover:border-brand-gold transition-all shadow-sm">Prepaid Fibre</button>
                <button onclick="setSubCategory('wireless')" id="sub-wireless" class="sub-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-black/10 bg-white text-gray-600 hover:border-brand-gold transition-all shadow-sm">Wireless</button>
                <button onclick="setSubCategory('lte')" id="sub-lte" class="sub-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-black/10 bg-white text-gray-600 hover:border-brand-gold transition-all shadow-sm">LTE</button>
                <button onclick="setSubCategory('airmobile')" id="sub-airmobile" class="sub-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-black/10 bg-white text-gray-600 hover:border-brand-gold transition-all shadow-sm">AirMobile</button>
                <button onclick="setSubCategory('voip')" id="sub-voip" class="sub-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-black/10 bg-white text-gray-600 hover:border-brand-gold transition-all shadow-sm">VoIP</button>
                <button onclick="setSubCategory('devices')" id="sub-devices" class="sub-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-black/10 bg-white text-gray-600 hover:border-brand-gold transition-all shadow-sm">Devices</button>
            `;
        }} else if (category === 'all') {{
            subFiltersDiv.innerHTML = `<div class="text-xs text-gray-400">Select a product category above to filter</div>`;
        }}
        
        // Highlight all sub filter if none selected
        if (currentSubCategory === 'all') {{
            setSubCategory('all');
        }} else {{
            setSubCategory(currentSubCategory);
        }}
        renderProducts();
    }}
    
    function setSubCategory(subCat) {{
        currentSubCategory = subCat;
        // Update active state on sub-filter buttons
        document.querySelectorAll('.sub-filter-btn').forEach(btn => {{
            btn.className = "sub-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-black/10 bg-white text-gray-600 hover:border-brand-gold transition-all shadow-sm";
        }});
        const activeBtn = document.getElementById(`sub-${{subCat}}`);
        if (activeBtn) activeBtn.className = "sub-filter-btn px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase border border-brand-black bg-brand-black text-white transition-all shadow-sm";
        renderProducts();
    }}
    
    function renderProducts() {{
        const container = document.getElementById('packages-container');
        if(!container) return;
        container.innerHTML = '';
        let products = [];
        
        if (currentMainCategory === 'all') {{
            for (let cat in hostingProducts) {{
                products.push(...hostingProducts[cat]);
            }}
            for (let cat in domainProducts) {{
                products.push(...domainProducts[cat]);
            }}
            for (let cat in emailProducts) {{
                products.push(...emailProducts[cat]);
            }}
            for (let cat in internetProducts) {{
                products.push(...internetProducts[cat]);
            }}
        }} else if (currentMainCategory === 'hostings') {{
            if (currentSubCategory === 'all') {{
                for (let cat in hostingProducts) {{
                    products.push(...hostingProducts[cat]);
                }}
            }} else if (hostingProducts[currentSubCategory]) {{
                products = [...hostingProducts[currentSubCategory]];
            }}
        }} else if (currentMainCategory === 'domains') {{
            if (currentSubCategory === 'all') {{
                for (let cat in domainProducts) {{
                    products.push(...domainProducts[cat]);
                }}
            }} else if (domainProducts[currentSubCategory]) {{
                products = [...domainProducts[currentSubCategory]];
            }}
        }} else if (currentMainCategory === 'emails') {{
            if (currentSubCategory === 'all') {{
                for (let cat in emailProducts) {{
                    products.push(...emailProducts[cat]);
                }}
            }} else if (emailProducts[currentSubCategory]) {{
                products = [...emailProducts[currentSubCategory]];
            }}
        }} else if (currentMainCategory === 'internet') {{
            if (currentSubCategory === 'all') {{
                for (let cat in internetProducts) {{
                    products.push(...internetProducts[cat]);
                }}
            }} else if (internetProducts[currentSubCategory]) {{
                products = [...internetProducts[currentSubCategory]];
            }}
        }}
        
        if(products.length===0) {{ 
            container.innerHTML=`<div class="col-span-full text-center py-16 bg-white rounded-3xl border border-black/5 shadow-inner"><i class="fa-solid fa-triangle-exclamation text-4xl text-brand-gold mb-4"></i><p class="font-bold text-brand-black text-sm">No products found.</p><p class="text-xs text-gray-400 mt-1">Please select a different category.</p></div>`; 
            return; 
        }}
        
        products.forEach(plan => {{
            const isOneTime = plan.isOneTime || false;
            const priceSuffix = isOneTime ? 'once-off' : (plan.period === 'year' ? '/year' : (plan.perUser ? '/user/month' : '/month'));
            // For internet products, adjust price suffix
            let actualPriceSuffix = priceSuffix;
            if (plan.type === 'internet') {{
                if (plan.category === 'fibre' || plan.category === 'prepaid' || plan.category === 'wireless' || plan.category === 'lte' || plan.category === 'airmobile' || plan.category === 'voip') {{
                    actualPriceSuffix = '/month';
                }} else if (plan.category === 'devices') {{
                    actualPriceSuffix = 'once-off';
                }}
            }}
            const popBadge = plan.isPopular ? `<div class="absolute -top-3.5 left-6 bg-gradient-to-r from-brand-gold via-brand-goldLight to-brand-goldDark text-brand-black text-[9px] uppercase font-black px-3.5 py-1.5 rounded-full tracking-wider shadow-sm">Most Popular</div>` : '';
            let typeLabel = '';
            if (plan.type === 'hosting' || (plan.category && hostingProducts[plan.category])) typeLabel = 'Hosting';
            else if (plan.type === 'domain') typeLabel = 'Domain';
            else if (plan.type === 'email') typeLabel = 'Email';
            else if (plan.type === 'design') typeLabel = 'Design';
            else if (plan.type === 'internet') typeLabel = 'Internet';
            else typeLabel = 'Product';
            
            const cardHtml = `<div class="bg-white rounded-3xl p-7 relative flex flex-col justify-between hover:shadow-xl hover:scale-[1.01] transition-all duration-300 border border-black/5 shadow-sm">${{popBadge}}<div class="space-y-4"><div class="flex items-center justify-between"><span class="text-[10px] font-bold uppercase tracking-wider text-brand-goldDark flex items-center gap-1.5"><span class="h-2 w-2 rounded-full bg-brand-gold shadow-[0_0_6px_#D4AF37]"></span>${{typeLabel}}</span><span class="text-[9px] uppercase font-bold bg-brand-lightBg px-3 py-1 rounded-full text-gray-500">${{plan.features ? plan.features.length : 3}} Features</span></div><div><h3 class="text-lg font-extrabold text-brand-black tracking-tight">${{plan.name}}</h3><div class="mt-2"><span class="text-2xl font-black text-brand-black tracking-tight">R${{typeof plan.price === 'number' ? plan.price.toFixed(2) : plan.price}}</span><span class="text-[10px] text-gray-500 font-bold uppercase tracking-wider ml-1">/${{actualPriceSuffix}}</span></div></div><p class="text-xs text-gray-500 leading-relaxed min-h-[60px]">${{plan.description}}</p><ul class="space-y-2 text-xs text-gray-600 border-t border-black/5 pt-4">${{plan.features ? plan.features.map(f => `<li class="flex items-center gap-2"><i class="fa-regular fa-circle-check text-brand-green text-[10px]"></i> ${{f}}</li>`).join('') : '<li class="flex items-center gap-2"><i class="fa-regular fa-circle-check text-brand-green text-[10px]"></i> Full feature set included</li>'}}</ul></div><div class="mt-8 pt-5 border-t border-black/5 flex flex-col gap-3"><div class="grid grid-cols-2 gap-2 mt-1"><button onclick="directBuy('${{plan.type === 'hosting' ? 'host' : (plan.type === 'domain' ? 'domain' : (plan.type === 'email' ? 'email' : (plan.type === 'design' ? 'design' : 'internet')))}}', '${{plan.id}}')" class="glossy-gold text-brand-black py-2.5 rounded-full font-bold text-[10px] tracking-wider uppercase shadow-md flex items-center justify-center gap-1.5"><span>Buy Now</span> <i class="fa-solid fa-bolt text-[9px]"></i></button><button onclick="addToCart('${{plan.type === 'hosting' ? 'host' : (plan.type === 'domain' ? 'domain' : (plan.type === 'email' ? 'email' : (plan.type === 'design' ? 'design' : 'internet')))}}', '${{plan.id}}')" class="glossy-black text-white py-2.5 rounded-full font-bold text-[10px] tracking-wider uppercase shadow-md flex items-center justify-center gap-1.5 hover:text-brand-gold"><span>Add to Bag</span> <i class="fa-solid fa-bag-shopping text-[9px] text-brand-gold"></i></button></div></div></div>`;
            container.innerHTML += cardHtml;
        }});
    }}

    // Design page functions (unchanged)
    function setDesignCategory(category) {{
        currentDesignCategory = category;
        document.querySelectorAll('.design-cat-tab').forEach(tab => tab.className = "design-cat-tab flex-1 px-5 py-2.5 rounded-xl font-bold text-xs tracking-wider uppercase transition-all text-gray-500 hover:bg-white/50");
        const activeTab = document.getElementById(`design-tab-${{category}}`);
        if(activeTab) activeTab.className = "design-cat-tab flex-1 px-5 py-2.5 rounded-xl font-bold text-xs tracking-wider uppercase transition-all text-brand-goldDark bg-white shadow-sm";
        renderDesignProducts();
    }}

    function renderDesignProducts() {{
        const container = document.getElementById('design-products-container');
        if(!container) return;
        container.innerHTML = '';
        let products = [];
        
        if (currentDesignCategory === 'all') {{
            for (let cat in designProducts) {{
                products.push(...designProducts[cat]);
            }}
        }} else if (currentDesignCategory === 'design') {{
            products = [...designProducts.custom];
        }} else if (currentDesignCategory === 'ecom') {{
            products = [...designProducts.ecom];
        }} else if (currentDesignCategory === 'sitebuilder') {{
            products = [...designProducts.sitebuilder];
        }}
        
        // Also add the design selector cards for the sandbox (from original designData)
        const selectorCardsDiv = document.getElementById('design-selector-cards');
        if (selectorCardsDiv) {{
            // Create selector cards for custom design products only
            selectorCardsDiv.innerHTML = '';
            designProducts.custom.forEach(plan => {{
                const previewKey = plan.previewKey;
                const isSelected = (previewKey === 'luxe');
                const borderClass = isSelected ? (previewKey === 'luxe' ? 'border-brand-gold/40' : (previewKey === 'emerald' ? 'border-brand-green/40' : 'border-white/30')) : 'border-white/5';
                const bgClass = isSelected ? 'bg-brand-darkGray/60' : 'bg-brand-darkGray/20';
                const priceDisplay = plan.price.toFixed(2);
                const card = `
                    <div id="card-design-${{previewKey}}" onclick="selectWebDesign('${{previewKey}}')" class="design-selector-card cursor-pointer p-5 rounded-2xl border ${{bgClass}} ${{borderClass}} shadow-lg hover:border-brand-gold/50 transition-all duration-300 relative overflow-hidden mb-4">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-xs font-bold ${{previewKey === 'luxe' ? 'text-brand-gold' : (previewKey === 'emerald' ? 'text-brand-green' : 'text-white')}} tracking-widest uppercase flex items-center gap-2">
                                <i class="fa-solid ${{previewKey === 'luxe' ? 'fa-gem' : (previewKey === 'emerald' ? 'fa-bolt' : 'fa-seedling')}}"></i> ${{plan.name}}
                            </span>
                            ${{plan.isPopular ? '<span class="text-[9px] bg-brand-gold/15 text-brand-gold px-2.5 py-0.5 rounded font-bold uppercase tracking-wider">Most Popular</span>' : ''}}
                        </div>
                        <p class="text-xs text-gray-400 leading-relaxed mb-3">${{plan.description.substring(0, 80)}}...</p>
                        <div class="border-t border-white/5 pt-3 mt-3 flex flex-col gap-2.5">
                            <div class="flex items-center justify-between">
                                <div><span class="text-xl font-extrabold text-white">R${{priceDisplay}}</span><span class="text-[9px] text-gray-500 uppercase font-bold tracking-wider block">Once-off Setup</span></div>
                            </div>
                            <div class="grid grid-cols-2 gap-2 mt-1">
                                <button onclick="directBuy('design', '${{plan.id}}'); event.stopPropagation();" class="glossy-gold text-brand-black text-[10px] font-black uppercase tracking-wider py-2.5 rounded-full shadow-md flex items-center justify-center gap-1.5">
                                    <span>Buy Now</span> <i class="fa-solid fa-bolt text-[8px]"></i>
                                </button>
                                <button onclick="addToCart('design', '${{plan.id}}'); event.stopPropagation();" class="glossy-black text-white text-[10px] font-black uppercase tracking-wider py-2.5 rounded-full shadow-md flex items-center justify-center gap-1.5 hover:text-brand-gold">
                                    <span>Add to Bag</span> <i class="fa-solid fa-bag-shopping text-[8px] text-brand-gold"></i>
                                </button>
                            </div>
                        </div>
                        <div class="flex items-center gap-3 text-[9px] text-gray-500 font-semibold uppercase mt-3">
                            ${{plan.features.map(f => `<span><i class="fa-solid fa-circle-check text-brand-green mr-1"></i> ${{f}}</span>`).join('')}}
                        </div>
                    </div>
                `;
                selectorCardsDiv.innerHTML += card;
            }});
        }}
        
        if(products.length===0) {{ 
            container.innerHTML=`<div class="col-span-full text-center py-16 bg-white rounded-3xl border border-black/5 shadow-inner"><i class="fa-solid fa-triangle-exclamation text-4xl text-brand-gold mb-4"></i><p class="font-bold text-brand-black text-sm">No design products found.</p><p class="text-xs text-gray-400 mt-1">Please select a different category.</p></div>`; 
            return; 
        }}
        
        products.forEach(plan => {{
            const isOneTime = plan.period !== 'month';
            const priceSuffix = isOneTime ? 'once-off' : '/month';
            const popBadge = plan.isPopular ? `<div class="absolute -top-3.5 left-6 bg-gradient-to-r from-brand-gold via-brand-goldLight to-brand-goldDark text-brand-black text-[9px] uppercase font-black px-3.5 py-1.5 rounded-full tracking-wider shadow-sm">Most Popular</div>` : '';
            let typeLabel = '';
            if (plan.type === 'design') typeLabel = 'Custom Design';
            else if (plan.type === 'ecom') typeLabel = 'eCommerce';
            else if (plan.type === 'sitebuilder') typeLabel = 'SiteBuilder';
            
            const cardHtml = `<div class="bg-white rounded-3xl p-7 relative flex flex-col justify-between hover:shadow-xl hover:scale-[1.01] transition-all duration-300 border border-black/5 shadow-sm">${{popBadge}}<div class="space-y-4"><div class="flex items-center justify-between"><span class="text-[10px] font-bold uppercase tracking-wider text-brand-goldDark flex items-center gap-1.5"><span class="h-2 w-2 rounded-full bg-brand-gold shadow-[0_0_6px_#D4AF37]"></span>${{typeLabel}}</span><span class="text-[9px] uppercase font-bold bg-brand-lightBg px-3 py-1 rounded-full text-gray-500">${{plan.features ? plan.features.length : 3}} Features</span></div><div><h3 class="text-lg font-extrabold text-brand-black tracking-tight">${{plan.name}}</h3><div class="mt-2"><span class="text-2xl font-black text-brand-black tracking-tight">R${{plan.price.toFixed(2)}}</span><span class="text-[10px] text-gray-500 font-bold uppercase tracking-wider ml-1">/${{priceSuffix}}</span></div></div><p class="text-xs text-gray-500 leading-relaxed min-h-[60px]">${{plan.description}}</p><ul class="space-y-2 text-xs text-gray-600 border-t border-black/5 pt-4">${{plan.features ? plan.features.map(f => `<li class="flex items-center gap-2"><i class="fa-regular fa-circle-check text-brand-green text-[10px]"></i> ${{f}}</li>`).join('') : '<li class="flex items-center gap-2"><i class="fa-regular fa-circle-check text-brand-green text-[10px]"></i> Full feature set included</li>'}}</ul></div><div class="mt-8 pt-5 border-t border-black/5 flex flex-col gap-3"><div class="grid grid-cols-2 gap-2 mt-1"><button onclick="directBuy('design', '${{plan.id}}')" class="glossy-gold text-brand-black py-2.5 rounded-full font-bold text-[10px] tracking-wider uppercase shadow-md flex items-center justify-center gap-1.5"><span>Buy Now</span> <i class="fa-solid fa-bolt text-[9px]"></i></button><button onclick="addToCart('design', '${{plan.id}}')" class="glossy-black text-white py-2.5 rounded-full font-bold text-[10px] tracking-wider uppercase shadow-md flex items-center justify-center gap-1.5 hover:text-brand-gold"><span>Add to Bag</span> <i class="fa-solid fa-bag-shopping text-[9px] text-brand-gold"></i></button></div></div></div>`;
            container.innerHTML += cardHtml;
        }});
    }}

    function renderCloudPlans() {{
        const container = document.getElementById('cloud-plans-container');
        if(!container) return;
        container.innerHTML = '';
        cloudStorageData.forEach(plan => {{
            const card = `
                <div class="bg-white rounded-3xl p-7 border border-black/5 shadow-sm hover:shadow-xl hover:scale-[1.02] transition-all duration-300 flex flex-col justify-between relative">
                    ${{plan.isPopular ? '<div class="absolute -top-3.5 left-6 bg-gradient-to-r from-brand-gold via-brand-goldLight to-brand-goldDark text-brand-black text-[9px] uppercase font-black px-3.5 py-1.5 rounded-full tracking-wider shadow-sm">Most Popular</div>' : ''}}
                    <div class="space-y-4">
                        <div class="h-12 w-12 bg-brand-gold/10 rounded-2xl flex items-center justify-center text-brand-goldDark text-xl"><i class="fa-solid fa-cloud-arrow-up"></i></div>
                        <div><h3 class="text-base font-extrabold text-brand-black">${{plan.name}}</h3><div class="flex items-baseline gap-1 mt-1"><span class="text-4xl font-black text-brand-black">${{plan.storage}}</span></div></div>
                        <p class="text-xs text-gray-500 leading-relaxed">${{plan.description || 'Secure encrypted storage with instant fibre-speed sync across all devices.'}}</p>
                        <ul class="space-y-2 text-xs text-gray-600 border-t border-black/5 pt-4"><li class="flex items-center gap-2"><i class="fa-solid fa-circle-check text-brand-green text-[10px]"></i> AES-256 Encrypted</li><li class="flex items-center gap-2"><i class="fa-solid fa-circle-check text-brand-green text-[10px]"></i> Fibre-Speed Upload</li><li class="flex items-center gap-2"><i class="fa-solid fa-circle-check text-brand-green text-[10px]"></i> Cross-Device Sync</li></ul>
                    </div>
                    <div class="mt-6 pt-5 border-t border-black/5 space-y-3"><div><span class="text-2xl font-black text-brand-black">R${{plan.price}}</span><span class="text-[9px] text-gray-400 font-bold uppercase block tracking-wider">per month</span></div><div class="grid grid-cols-2 gap-2"><button onclick="directBuy('cloud', '${{plan.id}}')" class="glossy-gold text-brand-black py-2.5 rounded-full font-bold text-[10px] tracking-wider uppercase shadow-md flex items-center justify-center gap-1.5"><span>Buy Now</span><i class="fa-solid fa-bolt text-[9px]"></i></button><button onclick="addToCart('cloud', '${{plan.id}}')" class="glossy-black text-white py-2.5 rounded-full font-bold text-[10px] tracking-wider uppercase shadow-md flex items-center justify-center gap-1.5 hover:text-brand-gold"><span>Add to Bag</span><i class="fa-solid fa-bag-shopping text-[9px] text-brand-gold"></i></button></div></div>
                </div>`;
            container.innerHTML += card;
        }});
    }}

    function selectWebDesign(themeKey) {{ 
        const data = designData[themeKey]; 
        if(!data) return; 
        document.querySelectorAll('.design-selector-card').forEach(card => {{ 
            card.className = "design-selector-card cursor-pointer p-5 rounded-2xl border bg-brand-darkGray/20 border-white/5 shadow-lg hover:border-brand-gold/50 transition-all duration-300 relative overflow-hidden"; 
        }}); 
        const activeCard = document.getElementById(`card-design-${{themeKey}}`); 
        if(activeCard) {{ 
            const borderClass = themeKey==='luxe' ? 'border-brand-gold/40' : (themeKey==='emerald' ? 'border-brand-green/40' : 'border-white/30'); 
            activeCard.className = `design-selector-card cursor-pointer p-5 rounded-2xl border bg-brand-darkGray/60 ${{borderClass}} shadow-lg transition-all duration-300 relative overflow-hidden`; 
        }} 
        const viewport = document.getElementById('live-web-viewport'); 
        viewport.className = `${{data.viewportBg}} p-6 sm:p-10 rounded-2xl min-h-[420px] flex flex-col justify-between transition-all duration-500 relative overflow-hidden`; 
        const logoEl = document.getElementById('mockup-logo'); 
        logoEl.className = `text-xs font-black tracking-tight flex items-center gap-1.5 ${{data.logoClass}}`; 
        logoEl.innerHTML = `<span class="h-5 w-5 bg-gradient-to-r ${{themeKey==='luxe' ? 'from-brand-gold to-brand-goldDark text-brand-black' : (themeKey==='emerald' ? 'from-brand-green to-brand-greenDark text-white' : 'from-white to-gray-400 text-brand-black')}} rounded-md flex items-center justify-center text-[10px] font-black">${{themeKey.substring(0,1).toUpperCase()}}</span> <span>${{data.logoText}}</span>`; 
        const badgeEl = document.getElementById('mockup-badge'); 
        badgeEl.innerText = data.badgeText; 
        badgeEl.className = `inline-block text-[8px] tracking-widest font-bold uppercase px-2.5 py-1 rounded-full ${{data.badgeClass}}`; 
        document.getElementById('mockup-title').innerHTML = data.title; 
        document.getElementById('mockup-desc').innerText = data.desc; 
        document.getElementById('mockup-time').innerText = data.timeText; 
        const btnEl = document.getElementById('mockup-btn'); 
        btnEl.className = `${{data.btnClass}} text-[10px] font-black tracking-wider uppercase px-5 py-2.5 rounded-full shadow-md flex items-center gap-1.5`; 
    }}
    
    function simulateReload() {{ 
        const viewport = document.getElementById('live-web-viewport'); 
        viewport.style.opacity='0.1'; 
        viewport.style.transform='scale(0.98)'; 
        setTimeout(()=>{{ viewport.style.opacity='1'; viewport.style.transform='scale(1)'; }},300); 
    }}

    function toggleFaq(btn) {{ 
        const containerBox = btn.nextElementSibling; 
        const indicatorIcon = btn.querySelector('i'); 
        if(containerBox.classList.contains('hidden')) {{ 
            containerBox.classList.remove('hidden'); 
            indicatorIcon.className = "fa-solid fa-chevron-up transition-transform text-brand-gold"; 
        }} else {{ 
            containerBox.classList.add('hidden'); 
            indicatorIcon.className = "fa-solid fa-chevron-down transition-transform"; 
        }} 
    }}

    // Checkout modal functions with auth check
    function openCheckoutModal() {{
        if (!isAuthenticated()) {{
            alertModal("Please log in to proceed with checkout.");
            triggerClientZone();
            return;
        }}
        if (cart.length === 0) {{
            alertModal("Your Shopping Bag is empty. Please add a product first!");
            return;
        }}
        currentModalStep = 2;
        updateModalStepsUI();
        let totalVal = 0;
        const summaryContainer = document.getElementById('modal-verification-summary');
        summaryContainer.innerHTML = '';
        cart.forEach(item => {{
            let itemTotal = item.price;
            let addonTexts = [];
            if (item.type === 'host') {{
                if (item.addons.extra_storage) {{ itemTotal += 129; addonTexts.push("Extra Storage (+R129)"); }}
                if (item.addons.priority) {{ itemTotal += 64; addonTexts.push("Priority Support (+R64)"); }}
            }}
            totalVal += itemTotal;
            const row = document.createElement('div');
            row.className = "flex justify-between items-start text-xs border-b border-white/5 pb-2 last:border-b-0";
            row.innerHTML = `<div><span class="font-bold text-white block">${{item.name}}</span><span class="text-[8px] text-gray-500">${{addonTexts.join(' / ') || 'Standard'}}</span></div><span class="font-extrabold text-brand-gold shrink-0">R${{itemTotal.toFixed(2)}}</span>`;
            summaryContainer.appendChild(row);
        }});
        document.getElementById('modal-footer-price').innerText = `R${{totalVal.toFixed(2)}}`;
        document.getElementById('summary-total-price').innerText = `R${{totalVal.toFixed(2)}}`;
        document.getElementById('signup-modal').classList.remove('hidden');
    }}

    async function createOrder() {{
        if (!isAuthenticated()) return;
        const items = cart.map(item => ({{
            cartId: item.cartId,
            type: item.type,
            id: item.id,
            name: item.name,
            price: item.price,
            addons: item.addons
        }}));
        let total = 0;
        cart.forEach(item => {{
            let itemTotal = item.price;
            if (item.type === 'host') {{
                if (item.addons.extra_storage) itemTotal += 129;
                if (item.addons.priority) itemTotal += 64;
            }}
            total += itemTotal;
        }});
        try {{
            const response = await authenticatedFetch("/orders", {{
                method: "POST",
                body: JSON.stringify({{ items, total }})
            }});
            if (response.ok) {{
                console.log("Order created successfully");
            }} else {{
                console.error("Failed to create order");
            }}
        }} catch (err) {{
            console.error(err);
        }}
    }}

    function updateModalStepsUI() {{
        document.getElementById('modal-step-2').classList.add('hidden');
        document.getElementById('modal-step-3').classList.add('hidden');
        document.getElementById(`modal-step-${{currentModalStep}}`).classList.remove('hidden');
        const backBtn = document.getElementById('modal-back-btn');
        if (currentModalStep === 2) backBtn.classList.add('hidden');
        else backBtn.classList.remove('hidden');
        let totalVal = 0;
        cart.forEach(item => {{
            let itemTotal = item.price;
            if (item.type === 'host') {{ if (item.addons.extra_storage) itemTotal += 129; if (item.addons.priority) itemTotal += 64; }}
            totalVal += itemTotal;
        }});
        let checkoutLink = `https://sandbox.polar.sh/checkout/new?org=angwa&amount=${{Math.round(totalVal)}}`;
        const nextBtnContainer = document.getElementById('modal-next-btn-container');
        if (currentModalStep === 3) {{
            nextBtnContainer.innerHTML = `<a href="${{checkoutLink}}" id="modal-next-btn" data-polar-checkout data-polar-checkout-theme="dark" class="glossy-green text-white px-6 py-2.5 rounded-full font-bold text-xs tracking-wider uppercase shadow-md inline-flex items-center gap-1.5 cursor-pointer no-underline select-none"><span>Pay with Polar</span> <i class="fa-solid fa-shield-halved text-brand-gold text-[10px]"></i></a>`;
            if (window.PolarEmbedCheckout) setTimeout(() => window.PolarEmbedCheckout.init(), 60);
        }} else {{
            nextBtnContainer.innerHTML = `<button id="modal-next-btn" onclick="nextStep()" class="glossy-gold text-brand-black px-6 py-2.5 rounded-full font-bold text-xs tracking-wider uppercase shadow-md">Continue <i class="fa-solid fa-chevron-right ml-1"></i></button>`;
        }}
        const ind2 = document.getElementById('step-indicator-2');
        const ind3 = document.getElementById('step-indicator-3');
        if (currentModalStep === 2) {{
            ind2.className = "text-brand-gold flex items-center gap-1.5";
            ind2.querySelector('span').className = "h-4.5 w-4.5 rounded-full bg-brand-gold/20 text-brand-gold flex items-center justify-center text-[9px] font-black";
            ind3.className = "text-gray-500 flex items-center gap-1.5";
            ind3.querySelector('span').className = "h-4.5 w-4.5 rounded-full bg-white/5 text-gray-500 flex items-center justify-center text-[9px]";
        }} else {{
            ind2.className = "text-brand-green flex items-center gap-1.5";
            ind2.querySelector('span').className = "h-4.5 w-4.5 rounded-full bg-brand-green/20 text-brand-green flex items-center justify-center text-[9px] font-black";
            ind3.className = "text-brand-gold flex items-center gap-1.5";
            ind3.querySelector('span').className = "h-4.5 w-4.5 rounded-full bg-brand-gold/20 text-brand-gold flex items-center justify-center text-[9px] font-black";
        }}
    }}

    function closeModal() {{ document.getElementById('signup-modal').classList.add('hidden'); }}

    async function nextStep() {{
        if (currentModalStep === 2) {{
            const nameInput = document.getElementById('cust-name').value.trim();
            const emailInput = document.getElementById('cust-email').value.trim();
            const addrInput = document.getElementById('cust-address').value.trim();
            if (!nameInput || !emailInput || !addrInput) {{
                alertModal("Please complete all setup destination fields before progressing.");
                return;
            }}
            currentModalStep = 3;
            updateModalStepsUI();
        }} else if (currentModalStep === 3) {{
            closeModal();
            await createOrder();
            showOrderToast();
            clearCart();
        }}
    }}

    function prevStep() {{
        if (currentModalStep > 2) {{
            currentModalStep--;
            updateModalStepsUI();
        }}
    }}

    function alertModal(msg) {{ 
        const alertBox=document.createElement('div'); 
        alertBox.className="fixed inset-0 bg-brand-black/70 z-[100] flex items-center justify-center p-4 backdrop-blur-sm"; 
        alertBox.innerHTML=`<div class="bg-brand-darkGray p-6 rounded-3xl max-w-sm w-full space-y-4 text-center border border-white/10 text-white shadow-2xl"><div class="h-12 w-12 bg-brand-gold/15 text-brand-gold rounded-full flex items-center justify-center text-xl mx-auto"><i class="fa-solid fa-triangle-exclamation"></i></div><h4 class="font-bold text-sm tracking-wide">Action Required</h4><p class="text-[11px] text-gray-400 leading-relaxed">${{msg}}</p><button onclick="this.parentElement.parentElement.remove()" class="w-full glossy-gold text-brand-black py-2.5 rounded-full font-bold text-xs uppercase tracking-wider">Acknowledge</button></div>`; 
        document.body.appendChild(alertBox); 
    }}
    
    function triggerLeadershipNotice() {{ 
        const noticeBox=document.createElement('div'); 
        noticeBox.className="fixed inset-0 bg-brand-black/70 z-[100] flex items-center justify-center p-4 backdrop-blur-sm"; 
        noticeBox.innerHTML=`<div class="bg-brand-darkGray p-6 rounded-3xl max-w-sm w-full space-y-4 text-center border border-white/10 text-white shadow-2xl"><div class="h-12 w-12 bg-brand-gold/15 text-brand-gold rounded-full flex items-center justify-center text-xl mx-auto"><i class="fa-solid fa-users"></i></div><h4 class="font-bold text-sm tracking-wide">ANGWA Executive Board</h4><p class="text-[11px] text-gray-400 leading-relaxed">Our comprehensive Board bios & investor portfolio records are securely archived on page. Reach out to our direct support desk to get a copy.</p><button onclick="this.parentElement.parentElement.remove()" class="w-full glossy-gold text-brand-black py-2.5 rounded-full font-bold text-xs uppercase tracking-wider">Acknowledge</button></div>`; 
        document.body.appendChild(noticeBox); 
    }}
    
    function showOrderToast() {{ 
        const toast=document.getElementById('order-toast'); 
        toast.classList.remove('hidden'); 
        setTimeout(()=>hideOrderToast(),6500); 
    }}
    
    function hideOrderToast() {{ 
        document.getElementById('order-toast').classList.add('hidden'); 
    }}

    function triggerCloudSync(provider) {{ 
        const cloudIcon=document.getElementById('cloud-icon'); 
        const statusText=document.getElementById('cloud-sync-status'); 
        const progress=document.getElementById('cloud-progress-bar'); 
        const timer=document.getElementById('cloud-timer-val'); 
        const panelRate=document.getElementById('panel-sync-rate'); 
        const panelProgress=document.getElementById('panel-progress-bar'); 
        const panelStatus=document.getElementById('panel-sync-status'); 
        const panelTimer=document.getElementById('panel-sync-timer'); 
        if(provider==='dropbox') {{ 
            if(cloudIcon) cloudIcon.className="fa-brands fa-dropbox text-blue-400"; 
            if(statusText) statusText.innerText="Connecting to Dropbox Fibre pipeline..."; 
            panelStatus.innerText="Splicing optical connection to Dropbox central nodes..."; 
        }} else {{ 
            if(cloudIcon) cloudIcon.className="fa-brands fa-google-drive text-green-400"; 
            if(statusText) statusText.innerText="Connecting to Google Drive high-speed backup system..."; 
            panelStatus.innerText="Securing direct cloud handshake with Google clusters..."; 
        }} 
        document.getElementById('cloud-sync-modal').classList.remove('hidden'); 
        panelRate.innerText="1,000 Mbps"; 
        let width=0; 
        if(progress) progress.style.width='0%'; 
        panelProgress.style.width='0%'; 
        if(timer) timer.innerText="6.2 seconds remaining"; 
        panelTimer.innerText="6.2s left"; 
        const interval=setInterval(()=>{{ 
            width+=10; 
            if(progress) progress.style.width=`${{width}}%`; 
            panelProgress.style.width=`${{width}}%`; 
            const timeLeft=Math.max(0,((100-width)/15).toFixed(1)); 
            if(timer) timer.innerText=`${{timeLeft}} seconds remaining`; 
            panelTimer.innerText=`${{timeLeft}}s left`; 
            if(width===40) {{ 
                if(statusText) statusText.innerText="Encrypting file systems with symmetrical light speed..."; 
                panelStatus.innerText="Sending secure multi-threaded file chunks..."; 
            }} else if(width===80) {{ 
                if(statusText) statusText.innerText="Finalizing cloud handshake metrics..."; 
                panelStatus.innerText="Assembling directory structures on destination server..."; 
            }} 
            if(width>=100) {{ 
                clearInterval(interval); 
                if(statusText) statusText.innerText="Sync complete! 50GB file database successfully uploaded in 0.8 seconds."; 
                panelStatus.innerText="Upload complete! 50GB mapped successfully in 0.8s."; 
                if(timer) timer.innerText="Success - 0.0 seconds remaining"; 
                panelTimer.innerText="Success"; 
                panelRate.innerText="0 Mbps (Idle)"; 
            }} 
        }},250); 
    }}
    
    function closeCloudModal() {{ 
        document.getElementById('cloud-sync-modal').classList.add('hidden'); 
    }}

    function triggerBlogsModal() {{ 
        document.getElementById('blogs-modal').classList.remove('hidden'); 
    }}
    
    function closeBlogsModal() {{ 
        document.getElementById('blogs-modal').classList.add('hidden'); 
    }}

    function toggleSidebarSubmenu(id) {{ 
        const el=document.getElementById(id); 
        const arrow=document.getElementById(id+'-arrow'); 
        if(el.classList.contains('hidden')) {{ 
            el.classList.remove('hidden'); 
            if(arrow) arrow.classList.add('rotate-180'); 
        }} else {{ 
            el.classList.add('hidden'); 
            if(arrow) arrow.classList.remove('rotate-180'); 
        }} 
    }}

    function triggerClientPortal(type) {{ 
        toggleSidebar(); 
        const welcomeBox=document.createElement('div'); 
        welcomeBox.className="fixed inset-0 bg-brand-black/70 z-[100] flex items-center justify-center p-4 backdrop-blur-sm"; 
        welcomeBox.innerHTML=`<div class="bg-brand-darkGray p-6 rounded-3xl max-w-sm w-full space-y-4 text-center border border-white/10 text-white shadow-2xl"><div class="h-12 w-12 bg-brand-gold/15 text-brand-gold rounded-full flex items-center justify-center text-xl mx-auto"><i class="fa-solid fa-user-shield"></i></div><h4 class="font-bold text-sm tracking-wide capitalize">${{type}} Client Portal</h4><p class="text-[11px] text-gray-400 leading-relaxed">Secure gateway gateway authentication is active for authorized ${{type}} networks. Please authenticate within the ClientZone.</p><button onclick="this.parentElement.parentElement.remove(); triggerClientZone();" class="w-full glossy-gold text-brand-black py-2.5 rounded-full font-bold text-xs uppercase tracking-wider">Access ClientZone</button></div>`; 
        document.body.appendChild(welcomeBox); 
    }}

    function toggleLiveChat() {{ 
        const chatBox=document.getElementById('chat-popup'); 
        if(chatBox.classList.contains('hidden')) chatBox.classList.remove('hidden'); 
        else chatBox.classList.add('hidden'); 
    }}
    
    function handleChatSubmit(event) {{ 
        if(event.key==='Enter') sendChatMessage(); 
    }}
    
    function sendChatMessage() {{ 
        const inputField=document.getElementById('chat-input'); 
        const userMsg=inputField.value.trim(); 
        if(!userMsg) return; 
        const chatMessagesContainer=document.getElementById('chat-messages'); 
        const divUser=document.createElement('div'); 
        divUser.className="bg-gradient-to-r from-brand-goldDark to-brand-gold text-brand-black font-semibold p-3 rounded-2xl text-[11px] max-w-[85%] self-end ml-auto mb-2.5 leading-relaxed shadow-sm"; 
        divUser.innerText=userMsg; 
        chatMessagesContainer.appendChild(divUser); 
        inputField.value=''; 
        chatMessagesContainer.scrollTop=chatMessagesContainer.scrollHeight; 
        setTimeout(()=>{{ 
            const divAgent=document.createElement('div'); 
            divAgent.className="bg-brand-darkGray/60 p-3 rounded-2xl border border-white/5 text-gray-300 max-w-[85%] mb-2.5 leading-relaxed"; 
            const lowerInput=userMsg.toLowerCase(); 
            if(lowerInput.includes('price')||lowerInput.includes('cost')||lowerInput.includes('rand')) divAgent.innerText="Our hosting plans start from R99/m for shared hosting. Dedicated servers from R1999/m. Domains from R89/year. Which product are you interested in?"; 
            else if(lowerInput.includes('domain')) divAgent.innerText="We offer .com, .co.za, .org, .net domains starting from R89/year. Would you like to check availability for a specific domain?"; 
            else if(lowerInput.includes('email')) divAgent.innerText="Professional email hosting from R29/user/month. Includes webmail, mobile sync, and anti-spam protection."; 
            else divAgent.innerText="I can help you find the right product. Tell me if you need hosting, a domain, or email services."; 
            chatMessagesContainer.appendChild(divAgent); 
            chatMessagesContainer.scrollTop=chatMessagesContainer.scrollHeight; 
        }},1100); 
    }}

    function setupScrollSpy() {{ 
        const badgeEl = document.getElementById('dynamic-nav-badge'); 
        const observerOptions = {{ root: null, rootMargin: '-35% 0px -45% 0px', threshold: 0 }}; 
        const observer = new IntersectionObserver((entries) => {{ 
            entries.forEach(entry => {{ 
                if(entry.isIntersecting) {{ 
                    const id = entry.target.id; 
                    let htmlContent = ''; 
                    if(id==='home-hero') htmlContent = `ANGWA<span class="text-brand-gold">.</span>`; 
                    else if(id==='packages') htmlContent = `ANGWA HOST<span class="text-brand-gold">.</span>`; 
                    else if(id==='design-products') htmlContent = `ANGWA DESIGN<span class="text-brand-gold">.</span>`; 
                    else if(id==='cloud-filling') htmlContent = `ANGWA CLOUD<span class="text-brand-gold">.</span>`; 
                    if(badgeEl) {{ 
                        badgeEl.style.opacity='0'; 
                        badgeEl.style.transform='translateY(-4px)'; 
                        setTimeout(()=>{{ 
                            if(htmlContent) badgeEl.innerHTML = htmlContent; 
                            badgeEl.style.opacity='1'; 
                            badgeEl.style.transform='translateY(0)'; 
                        }},150); 
                    }} 
                }} 
            }}); 
        }}, observerOptions); 
        document.querySelectorAll('#home-hero, #packages, #design-products, #cloud-filling').forEach(section => observer.observe(section)); 
    }}

    // Initialization
    document.addEventListener('DOMContentLoaded', () => {{
        showPage('home');
        renderProducts();
        renderDesignProducts();
        renderCloudPlans();
        setupSearchAutocomplete();
        setupScrollSpy();
        selectWebDesign('luxe');
        setMainCategory('all');
        setDesignCategory('all');
    }});
</script>

</body>
</html>
"""

components.html(html_content, height=2800, width=None, scrolling=True)
PYEOF
echo "✅ app.py written"

# ----------------------------------------------------------------------
# 7. Create requirements.txt
# ----------------------------------------------------------------------
cat > requirements.txt << 'EOF'
streamlit>=1.38.0
libsql-client>=0.3.1
python-dotenv>=1.0.1
fastapi>=0.115.0
uvicorn[standard]>=0.30.6
requests>=2.32.3
pydantic>=2.9.2
email-validator>=2.2.0
bcrypt>=4.2.0
python-multipart>=0.0.9
pytest>=8.3.3
httpx>=0.27.2
EOF
echo "✅ requirements.txt written"

# ----------------------------------------------------------------------
# 8. Create .env.example
# ----------------------------------------------------------------------
cat > .env.example << 'EOF'
# Turso database
TURSO_URL=https://your-database.turso.io
TURSO_TOKEN=your-turso-auth-token

# Polar.sh
POLAR_ORG_SLUG=your-org-slug
POLAR_ACCESS_TOKEN=your-polar-access-token
POLAR_WEBHOOK_SECRET=your-webhook-secret
POLAR_SERVER=production
POLAR_CUSTOM_PRODUCT_ID=custom
POLAR_SUCCESS_URL=https://your-app.onrender.com/thank-you
POLAR_CANCEL_URL=https://your-app.onrender.com

# SMTP email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=your-email@gmail.com

# API base URL (for frontend)
API_BASE_URL=https://your-app.onrender.com
EOF
echo "✅ .env.example written"

# ----------------------------------------------------------------------
# 9. Write a simple Dockerfile (optional but included)
# ----------------------------------------------------------------------
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501 8000

CMD ["sh", "-c", "uvicorn webhook_handler:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 8501 --server.address 0.0.0.0"]
EOF
echo "✅ Dockerfile written"

echo ""
echo "==> All files have been rebuilt from scratch."
echo "Now run: streamlit run app.py"
echo "Make sure your .env or secrets.toml has TURSO_URL and TURSO_TOKEN set."