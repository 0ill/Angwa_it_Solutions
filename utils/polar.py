"""
utils/polar.py – Polar.sh API helpers.
"""

import os
import json
import httpx
from dotenv import load_dotenv

load_dotenv()

POLAR_ORG_SLUG = os.environ.get("POLAR_ORG_SLUG")
POLAR_ACCESS_TOKEN = os.environ.get("POLAR_ACCESS_TOKEN")
POLAR_SERVER = os.environ.get("POLAR_SERVER", "sandbox")
POLAR_API_BASE = "https://api.polar.sh" if POLAR_SERVER == "production" else "https://sandbox-api.polar.sh"

HEADERS = {
    "Authorization": f"Bearer {POLAR_ACCESS_TOKEN}",
    "Content-Type": "application/json",
}

def create_checkout(
    product_id: str,
    customer_email: str,
    customer_name: str = None,
    customer_address: dict = None,
    success_url: str = None,
    cancel_url: str = None,
    metadata: dict = None,
):
    """Create a Polar checkout session."""
    url = f"{POLAR_API_BASE}/v1/checkouts"
    payload = {
        "product_id": product_id,
        "customer_email": customer_email,
        "success_url": success_url or os.environ.get("POLAR_SUCCESS_URL", "https://your-app.onrender.com/thank-you"),
        "cancel_url": cancel_url or os.environ.get("POLAR_CANCEL_URL", "https://your-app.onrender.com"),
        "metadata": metadata or {},
    }
    if customer_name:
        payload["customer_name"] = customer_name
    if customer_address:
        payload["customer_address"] = customer_address

    with httpx.Client() as client:
        response = client.post(url, json=payload, headers=HEADERS)
        response.raise_for_status()
        return response.json()

def create_order_checkout(
    order_items: list,
    customer_email: str,
    customer_name: str,
    customer_address: str = None,
    success_url: str = None,
    cancel_url: str = None,
):
    """Create a checkout for a custom order (multiple items)."""
    custom_product_id = os.environ.get("POLAR_CUSTOM_PRODUCT_ID", "custom")
    total_cents = sum(item.get("price", 0) * 100 for item in order_items)  # prices are in R
    metadata = {
        "items": json.dumps(order_items),
        "total_cents": str(total_cents),
    }
    return create_checkout(
        product_id=custom_product_id,
        customer_email=customer_email,
        customer_name=customer_name,
        customer_address={"line1": customer_address} if customer_address else None,
        success_url=success_url,
        cancel_url=cancel_url,
        metadata=metadata,
    )
