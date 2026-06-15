import os
import json
from datetime import datetime, timedelta
from typing import List, Optional
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from jose import JWTError, jwt
from passlib.context import CryptContext
import libsql_client

# ---------- Configuration ----------
TURSO_URL = os.environ["TURSO_URL"]
TURSO_TOKEN = os.environ["TURSO_TOKEN"]
SECRET_KEY = os.environ["SECRET_KEY"]          # generate with: openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7     # 7 days

# ---------- Database connection ----------
@contextmanager
def get_db():
    client = libsql_client.create_client_sync(TURSO_URL, auth_token=TURSO_TOKEN)
    try:
        yield client
    finally:
        client.close()

# ---------- Password hashing ----------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# ---------- JWT ----------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    with get_db() as client:
        rows = client.execute("SELECT id, name, email FROM users WHERE id = ?", [user_id]).rows
        if not rows:
            raise credentials_exception
        row = rows[0]
        return {"id": row[0], "name": row[1], "email": row[2]}

# ---------- Pydantic models ----------
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str

class OrderItem(BaseModel):
    cartId: str
    type: str
    id: str
    name: str
    price: int
    addons: dict

class OrderCreate(BaseModel):
    items: List[OrderItem]
    total: int

class OrderOut(BaseModel):
    id: int
    items: str
    total: int
    status: str
    created_at: str

# ---------- FastAPI app ----------
app = FastAPI(title="ANGWA Backend API")

# CORS – allow your Streamlit frontend URL (set environment variable or use wildcard for dev)
FRONTEND_URL = os.environ.get("FRONTEND_URL", "*")
origins = [
    FRONTEND_URL,
    "http://localhost:8501",
    "https://*.streamlit.app",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Public endpoints ----------
@app.get("/products")
def get_all_products():
    """Return all products grouped by type – optional, if you want to fetch from backend instead of direct Turso."""
    with get_db() as client:
        # Host
        host_rows = client.execute("SELECT id, provider, name, speed_down, speed_up, price, is_popular, description FROM products WHERE type = 'host'").rows
        host_products = []
        for row in host_rows:
            host_products.append({
                "id": row[0],
                "provider": row[1],
                "name": row[2],
                "down": row[3],
                "up": row[4],
                "price": row[5] // 100,
                "isPopular": bool(row[6]),
                "description": row[7]
            })
        # Cloud
        cloud_rows = client.execute("SELECT id, name, price, is_popular, description FROM products WHERE type = 'cloud'").rows
        cloud_products = []
        for row in cloud_rows:
            storage = row[1].split('(')[-1].replace(')', '') if '(' in row[1] else ""
            cloud_products.append({
                "id": row[0],
                "name": row[1],
                "storage": storage,
                "price": row[2] // 100,
                "isPopular": bool(row[3]),
                "description": row[4]
            })
        # Design – simplified
        design_rows = client.execute("SELECT id, name, price, is_popular, description FROM products WHERE type = 'design'").rows
        design_products = []
        for row in design_rows:
            design_products.append({
                "id": row[0],
                "name": row[1],
                "price": row[2] // 100,
                "isPopular": bool(row[3]),
                "description": row[4]
            })
        # Addons
        addon_rows = client.execute("SELECT product_type, name, price FROM addons").rows
        addons = {}
        for row in addon_rows:
            ptype = row[0]
            addons.setdefault(ptype, []).append({"name": row[1], "price": row[2] // 100})

        return {
            "host": host_products,
            "cloud": cloud_products,
            "design": design_products,
            "addons": addons
        }

@app.get("/coverage")
def get_coverage():
    with get_db() as client:
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
        coverage = []
        for row in rows:
            coverage.append({
                "name": row[0],
                "city": row[1],
                "province": row[2],
                "status": row[3],
                "provider": row[4],
                "max_speed": row[5],
                "infrastructure_ready": bool(row[6]) if row[6] is not None else False,
                "estimated_date": row[7]
            })
        return coverage

# ---------- Authentication endpoints ----------
@app.post("/register", response_model=Token)
def register(user: UserRegister):
    with get_db() as client:
        existing = client.execute("SELECT id FROM users WHERE email = ?", [user.email]).rows
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed = get_password_hash(user.password)
        client.execute(
            "INSERT INTO users (name, email, hashed_password) VALUES (?, ?, ?)",
            [user.name, user.email, hashed]
        )
        new_user = client.execute("SELECT id FROM users WHERE email = ?", [user.email]).rows[0]
        user_id = new_user[0]
        access_token = create_access_token(data={"sub": str(user_id)})
        return {"access_token": access_token, "token_type": "bearer"}

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with get_db() as client:
        rows = client.execute("SELECT id, email, hashed_password FROM users WHERE email = ?", [form_data.username]).rows
        if not rows:
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        user_id, email, hashed = rows[0]
        if not verify_password(form_data.password, hashed):
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        access_token = create_access_token(data={"sub": str(user_id)})
        return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=UserOut)
def get_me(current_user: dict = Depends(get_current_user)):
    return current_user

# ---------- Orders ----------
@app.get("/orders")
def get_orders(current_user: dict = Depends(get_current_user)):
    with get_db() as client:
        rows = client.execute(
            "SELECT id, items, total, status, created_at FROM orders WHERE user_id = ? ORDER BY created_at DESC",
            [current_user["id"]]
        ).rows
        orders = []
        for row in rows:
            orders.append({
                "id": row[0],
                "items": row[1],
                "total": row[2] // 100,
                "status": row[3],
                "date": row[4]
            })
        return orders

@app.post("/orders")
def create_order(order: OrderCreate, current_user: dict = Depends(get_current_user)):
    items_json = json.dumps([item.dict() for item in order.items])
    total_cents = order.total * 100
    with get_db() as client:
        client.execute(
            "INSERT INTO orders (user_id, items, total, status) VALUES (?, ?, ?, ?)",
            [current_user["id"], items_json, total_cents, "pending"]
        )
        return {"id": client.execute("SELECT last_insert_rowid()").rows[0][0], "status": "created"}

# Health check endpoint (useful for Render)
@app.get("/health")
def health():
    return {"status": "ok"}