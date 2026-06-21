"""
backend/database.py

Central data-access layer for the ANGWA app, backed by Turso (libsql).
Replaces the legacy monolith's ad-hoc inline queries with typed,
parameterized functions.

Works in two contexts:
- Inside Streamlit (app.py, frontend/*.py)        -> reads st.secrets
- Outside Streamlit (webhook_handler.py, tests)    -> reads .env via os.environ
"""

import os
import json
from typing import Optional, Any

from dotenv import load_dotenv
import bcrypt
import libsql_client

load_dotenv()  # no-op if .env doesn't exist; harmless if already loaded

_client: Optional[libsql_client.ClientSync] = None


def _get_secret(key: str, default: Any = None) -> Any:
    """Read a config value: prefer Streamlit secrets when available,
    otherwise fall back to environment variables."""
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


def get_client() -> libsql_client.ClientSync:
    """Return a cached singleton libsql client connected to Turso."""
    global _client
    if _client is None:
        url = _get_secret("TURSO_URL")
        token = _get_secret("TURSO_TOKEN")
        if not url or not token:
            raise RuntimeError(
                "TURSO_URL / TURSO_TOKEN not configured. "
                "Check .env or .streamlit/secrets.toml."
            )
        _client = libsql_client.create_client_sync(url, auth_token=token)
    return _client


def close_client() -> None:
    """Close the underlying connection. Mainly useful in tests/scripts."""
    global _client
    if _client is not None:
        _client.close()
        _client = None


# ---------------------------------------------------------------------------
# Products / Addons / Coverage  (read-only, public catalog data)
# ---------------------------------------------------------------------------

def get_products(product_type: Optional[str] = None) -> list[dict]:
    """Fetch products, optionally filtered by type ('host' | 'cloud' | 'design')."""
    client = get_client()
    if product_type:
        result = client.execute(
            "SELECT id, type, provider, name, speed_down, speed_up, price, "
            "is_popular, description FROM products WHERE type = ? ORDER BY price ASC",
            [product_type],
        )
    else:
        result = client.execute(
            "SELECT id, type, provider, name, speed_down, speed_up, price, "
            "is_popular, description FROM products ORDER BY type, price ASC"
        )
    products = []
    for row in result.rows:
        d = row.asdict()
        d["is_popular"] = bool(d["is_popular"])
        products.append(d)
    return products


def get_addons(product_type: Optional[str] = None) -> list[dict]:
    """Fetch add-ons, optionally filtered by product_type."""
    client = get_client()
    if product_type:
        result = client.execute(
            "SELECT id, product_type, name, price FROM addons "
            "WHERE product_type = ? ORDER BY price ASC",
            [product_type],
        )
    else:
        result = client.execute(
            "SELECT id, product_type, name, price FROM addons "
            "ORDER BY product_type, price ASC"
        )
    return [row.asdict() for row in result.rows]


def get_coverage_areas() -> list[dict]:
    """Fetch all coverage areas, ordered: available -> coming_soon -> planned."""
    client = get_client()
    result = client.execute("""
        SELECT id, area_name, city, province, status, provider,
               max_speed, infrastructure_ready, estimated_date
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


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

class EmailAlreadyExistsError(Exception):
    pass


def create_user(name: str, email: str, password: str) -> dict:
    """Create a new user with a bcrypt-hashed password.
    Raises EmailAlreadyExistsError if the email is already registered."""
    client = get_client()
    email_norm = email.strip().lower()

    existing = client.execute("SELECT id FROM users WHERE email = ?", [email_norm])
    if existing.rows:
        raise EmailAlreadyExistsError(f"Email already registered: {email_norm}")

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    result = client.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        [name.strip(), email_norm, password_hash],
    )
    return {"id": result.last_insert_rowid, "name": name.strip(), "email": email_norm}


def get_user_by_email(email: str) -> Optional[dict]:
    client = get_client()
    result = client.execute(
        "SELECT id, name, email, password_hash, created_at FROM users WHERE email = ?",
        [email.strip().lower()],
    )
    if not result.rows:
        return None
    return result.rows[0].asdict()


def verify_user_password(email: str, password: str) -> Optional[dict]:
    """Return the user dict (without password_hash) if credentials are
    valid, otherwise None."""
    user = get_user_by_email(email)
    if user is None:
        return None
    if bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
        return {"id": user["id"], "name": user["name"], "email": user["email"]}
    return None


def delete_user(user_id: int) -> None:
    """Hard delete a user. Used for tests / admin cleanup."""
    client = get_client()
    client.execute("DELETE FROM users WHERE id = ?", [user_id])


# ---------------------------------------------------------------------------
# Orders
# ---------------------------------------------------------------------------

VALID_ORDER_STATUSES = {"pending", "paid", "failed", "refunded", "cancelled"}


def create_order(
    customer_name: str,
    customer_email: str,
    items: list[dict],
    subtotal: int,
    customer_address: Optional[str] = None,
    currency: str = "ZAR",
    user_id: Optional[int] = None,
    polar_checkout_id: Optional[str] = None,
) -> dict:
    """Create a new order in 'pending' status. `items` is a list of cart
    line items (stored as JSON). `subtotal` is in cents."""
    client = get_client()
    # Convert items list to JSON string for storage
    items_json = json.dumps(items)
    result = client.execute(
        """INSERT INTO orders
           (user_id, customer_name, customer_email, customer_address,
            items_json, subtotal, currency, status, polar_checkout_id)
           VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?)""",
        [user_id, customer_name, customer_email, customer_address, items_json, subtotal, currency, polar_checkout_id],
    )
    return {"id": result.last_insert_rowid, "customer_name": customer_name, "customer_email": customer_email}
