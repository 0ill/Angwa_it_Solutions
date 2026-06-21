-- ============================================================
-- ANGWA schema for Turso (libsql / SQLite dialect)
-- ============================================================

PRAGMA foreign_keys = ON;

-- ---------- Products (host / cloud / design plans) ----------
CREATE TABLE IF NOT EXISTS products (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    type            TEXT NOT NULL CHECK (type IN ('host','cloud','design')),
    provider        TEXT,
    name            TEXT NOT NULL,
    speed_down      INTEGER,
    speed_up        INTEGER,
    price           INTEGER NOT NULL,            -- stored in cents
    is_popular      INTEGER NOT NULL DEFAULT 0,   -- 0/1 boolean
    description     TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_products_type ON products(type);

-- ---------- Add-ons (per product_type) ----------
CREATE TABLE IF NOT EXISTS addons (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    product_type    TEXT NOT NULL,
    name            TEXT NOT NULL,
    price           INTEGER NOT NULL,             -- cents
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_addons_type ON addons(product_type);

-- ---------- Fibre coverage areas ----------
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

-- ---------- Users (ClientZone accounts) ----------
CREATE TABLE IF NOT EXISTS users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    email           TEXT NOT NULL UNIQUE,
    password_hash   TEXT NOT NULL,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- ---------- Orders (linked to Polar checkouts) ----------
CREATE TABLE IF NOT EXISTS orders (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id             INTEGER REFERENCES users(id),
    customer_name       TEXT NOT NULL,
    customer_email      TEXT NOT NULL,
    customer_address    TEXT,
    items_json          TEXT NOT NULL,             -- JSON-encoded cart snapshot
    subtotal            INTEGER NOT NULL,          -- cents
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

-- ---------- Webhook events (idempotency log for Polar webhooks) ----------
CREATE TABLE IF NOT EXISTS webhook_events (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    polar_event_id      TEXT NOT NULL UNIQUE,
    event_type          TEXT NOT NULL,
    payload_json        TEXT NOT NULL,
    processed_at        TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ============================================================
-- Seed data (idempotent: only inserts if the row doesn't exist)
-- ============================================================

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
