"""
webhook_handler.py – FastAPI app for Polar webhooks.
"""

import os
import json
import hmac
import hashlib
from fastapi import FastAPI, Request, HTTPException, Header
from dotenv import load_dotenv
from backend.database import get_client
from utils.email import send_order_confirmation

load_dotenv()

app = FastAPI(title="ANGWA Webhook Handler")

WEBHOOK_SECRET = os.environ.get("POLAR_WEBHOOK_SECRET", "")
if not WEBHOOK_SECRET:
    print("WARNING: POLAR_WEBHOOK_SECRET not set. Signatures will not be verified.")

def verify_signature(payload: bytes, signature: str) -> bool:
    if not WEBHOOK_SECRET:
        return True
    computed = hmac.new(
        WEBHOOK_SECRET.encode("utf-8"),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed, signature)

@app.post("/webhook")
async def polar_webhook(
    request: Request,
    x_polar_signature: str = Header(None, alias="X-Polar-Signature"),
):
    raw_body = await request.body()
    if x_polar_signature and not verify_signature(raw_body, x_polar_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    event_type = payload.get("type")
    if not event_type:
        raise HTTPException(status_code=400, detail="Missing event type")

    if event_type == "order.paid":
        order_data = payload.get("data", {})
        polar_order_id = order_data.get("id")
        customer_email = order_data.get("customer_email")
        customer_name = order_data.get("customer_name", "Customer")
        metadata = order_data.get("metadata", {})
        order_id = metadata.get("order_id")

        if order_id:
            client = get_client()
            # Update order status
            client.execute(
                "UPDATE orders SET status = 'paid', polar_order_id = ?, updated_at = datetime('now') WHERE id = ?",
                [polar_order_id, order_id]
            )
            # Fetch order details to send email
            rows = client.execute(
                "SELECT customer_name, customer_email, items_json, subtotal FROM orders WHERE id = ?",
                [order_id]
            )
            if rows.rows:
                row = rows.rows[0]
                items = json.loads(row[2]) if row[2] else []
                total = row[3] / 100  # cents to R
                items_summary = ", ".join([f"{i.get('name', 'Item')} (R{i.get('price', 0):.2f})" for i in items])
                send_order_confirmation(
                    to_email=row[1],
                    order_id=order_id,
                    customer_name=row[0],
                    total=total,
                    items_summary=items_summary
                )
        print(f"Order paid: {polar_order_id}")
        return {"status": "ok"}

    # Ignore other events
    return {"status": "ignored"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# ========== AUTHENTICATION ENDPOINTS ==========
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from backend.database import create_user, verify_user_password, get_user_by_email
import jwt
from datetime import datetime, timedelta
import os

# JWT settings
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/auth/register", response_model=Token)
async def register(user: UserCreate):
    try:
        user_dict = create_user(user.name, user.email, user.password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = verify_user_password(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Add /orders endpoint to fetch user orders
@app.get("/orders")
async def get_orders(token: str = Depends(oauth2_scheme)):
    # Get user from token
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    # Fetch orders
    client = get_client()
    rows = client.execute(
        "SELECT id, created_at, status, subtotal, items_json FROM orders WHERE user_id = ? ORDER BY created_at DESC",
        [user["id"]]
    )
    orders = []
    for row in rows.rows:
        orders.append({
            "id": row[0],
            "created_at": row[1],
            "status": row[2],
            "total": row[3],
            "items": json.loads(row[4]) if row[4] else []
        })
    return orders

# Add POST /orders endpoint to create an order (requires auth)
@app.post("/orders")
async def create_order_endpoint(order_data: dict, token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    # order_data should contain items and total
    items = order_data.get("items", [])
    total = order_data.get("total", 0)
    # Create order
    from backend.database import create_order
    order = create_order(
        customer_name=user["name"],
        customer_email=user["email"],
        items=items,
        subtotal=int(total * 100),  # convert to cents
        user_id=user["id"]
    )
    return order
