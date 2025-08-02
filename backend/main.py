"""
FastAPI backend for MyClean service booking application
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import sqlite3
import hashlib
from datetime import datetime, date, time, timedelta
import json

app = FastAPI(title="MyClean API", description="Service booking API for MyClean", version="1.0.0")

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect("myclean.db")
    conn.row_factory = sqlite3.Row
    return conn

# Pydantic models for request/response
class UserCreate(BaseModel):
    email: str
    phone: Optional[str] = None
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    phone: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    is_provider: bool

class ServiceType(BaseModel):
    id: int
    name: str
    description: Optional[str]
    base_price: float
    duration_minutes: int
    category_name: str
    is_active: bool = True

class ServiceDuration(BaseModel):
    id: int
    duration_minutes: int
    duration_label: str
    price_multiplier: float

class OrderCreate(BaseModel):
    service_type_id: int
    service_duration_id: int
    service_date: date
    service_time_start: time
    customer_notes: Optional[str] = None

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    base_price: Optional[float] = None
    duration_minutes: Optional[int] = None
    is_active: Optional[bool] = None

class ServiceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category_name: str
    base_price: float
    duration_minutes: int = 60
    is_active: bool = True

class OrderResponse(BaseModel):
    id: int
    order_number: str
    customer_name: str
    service_date: date
    service_time_start: time
    service_time_end: time
    total_price: float
    status: str
    service_type_name: str

# Utility functions
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def generate_order_number() -> str:
    import random
    import string
    return 'XXX' + ''.join(random.choices(string.digits, k=3))

# Authentication endpoints
@app.post("/api/auth/register", response_model=UserResponse)
async def register(user: UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if user already exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (user.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    hashed_password = hash_password(user.password)
    cursor.execute("""
        INSERT INTO users (email, phone, password_hash, first_name, last_name)
        VALUES (?, ?, ?, ?, ?)
    """, (user.email, user.phone, hashed_password, user.first_name, user.last_name))

    user_id = cursor.lastrowid
    conn.commit()

    # Return user data
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()

    return UserResponse(
        id=user_data["id"],
        email=user_data["email"],
        phone=user_data["phone"],
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        is_provider=user_data["is_provider"]
    )

@app.post("/api/auth/login", response_model=UserResponse)
async def login(user: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (user.email,))
    user_data = cursor.fetchone()
    conn.close()

    if not user_data or not verify_password(user.password, user_data["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return UserResponse(
        id=user_data["id"],
        email=user_data["email"],
        phone=user_data["phone"],
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        is_provider=user_data["is_provider"]
    )

# Service endpoints
@app.get("/api/services", response_model=List[ServiceType])
async def get_services(include_inactive: bool = False):
    conn = get_db_connection()
    cursor = conn.cursor()

    # For provider management, include inactive services
    # For customer browsing, only show active services
    if include_inactive:
        cursor.execute("""
            SELECT st.id, st.name, st.description, st.base_price, st.duration_minutes,
                   sc.name as category_name, st.is_active
            FROM service_types st
            JOIN service_categories sc ON st.category_id = sc.id
            ORDER BY st.is_active DESC, st.name ASC
        """)
    else:
        cursor.execute("""
            SELECT st.id, st.name, st.description, st.base_price, st.duration_minutes,
                   sc.name as category_name, st.is_active
            FROM service_types st
            JOIN service_categories sc ON st.category_id = sc.id
            WHERE st.is_active = 1
            ORDER BY st.name ASC
        """)

    services = []
    for row in cursor.fetchall():
        services.append(ServiceType(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            base_price=row["base_price"],
            duration_minutes=row["duration_minutes"],
            category_name=row["category_name"],
            is_active=bool(row["is_active"])
        ))

    conn.close()
    return services

@app.get("/api/services/{service_id}/durations", response_model=List[ServiceDuration])
async def get_service_durations(service_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, duration_minutes, duration_label, price_multiplier
        FROM service_durations
        WHERE service_type_id = ?
    """, (service_id,))

    durations = []
    for row in cursor.fetchall():
        durations.append(ServiceDuration(
            id=row["id"],
            duration_minutes=row["duration_minutes"],
            duration_label=row["duration_label"],
            price_multiplier=row["price_multiplier"]
        ))

    conn.close()
    return durations

@app.put("/api/services/{service_id}")
async def update_service(service_id: int, service_update: ServiceUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if service exists
    cursor.execute("SELECT id FROM service_types WHERE id = ?", (service_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Service not found")

    # Build update query dynamically based on provided fields
    update_fields = []
    update_values = []

    if service_update.name is not None:
        update_fields.append("name = ?")
        update_values.append(service_update.name)

    if service_update.description is not None:
        update_fields.append("description = ?")
        update_values.append(service_update.description)

    if service_update.base_price is not None:
        update_fields.append("base_price = ?")
        update_values.append(service_update.base_price)

    if service_update.duration_minutes is not None:
        update_fields.append("duration_minutes = ?")
        update_values.append(service_update.duration_minutes)

    if service_update.is_active is not None:
        update_fields.append("is_active = ?")
        update_values.append(service_update.is_active)

    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    # Add service_id for WHERE clause
    update_values.append(service_id)

    query = f"UPDATE service_types SET {', '.join(update_fields)} WHERE id = ?"
    cursor.execute(query, update_values)

    conn.commit()
    conn.close()

    return {"message": "Service updated successfully", "service_id": service_id}

@app.post("/api/services", response_model=ServiceType)
async def create_service(service: ServiceCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get category_id from category_name
    cursor.execute("SELECT id FROM service_categories WHERE name = ?", (service.category_name,))
    category = cursor.fetchone()
    if not category:
        raise HTTPException(status_code=400, detail=f"Category '{service.category_name}' not found")

    category_id = category["id"]

    # Create new service
    cursor.execute("""
        INSERT INTO service_types (category_id, name, description, base_price, duration_minutes, is_active)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (category_id, service.name, service.description, service.base_price, service.duration_minutes, service.is_active))

    service_id = cursor.lastrowid
    conn.commit()

    # Return the created service
    cursor.execute("""
        SELECT st.id, st.name, st.description, st.base_price, st.duration_minutes,
               sc.name as category_name, st.is_active
        FROM service_types st
        JOIN service_categories sc ON st.category_id = sc.id
        WHERE st.id = ?
    """, (service_id,))

    service_data = cursor.fetchone()
    conn.close()

    return ServiceType(
        id=service_data["id"],
        name=service_data["name"],
        description=service_data["description"],
        base_price=service_data["base_price"],
        duration_minutes=service_data["duration_minutes"],
        category_name=service_data["category_name"],
        is_active=bool(service_data["is_active"])
    )

# Order endpoints
@app.post("/api/orders", response_model=OrderResponse)
async def create_order(order: OrderCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get service and duration details for pricing
    cursor.execute("""
        SELECT st.base_price, st.name, sd.duration_minutes, sd.price_multiplier
        FROM service_types st
        JOIN service_durations sd ON sd.service_type_id = st.id
        WHERE st.id = ? AND sd.id = ?
    """, (order.service_type_id, order.service_duration_id))

    service_data = cursor.fetchone()
    if not service_data:
        raise HTTPException(status_code=404, detail="Service or duration not found")

    # Calculate pricing and end time
    base_price = service_data["base_price"]
    total_price = base_price * service_data["price_multiplier"]
    duration_minutes = service_data["duration_minutes"]

    # Calculate end time
    start_datetime = datetime.combine(order.service_date, order.service_time_start)
    end_datetime = start_datetime + timedelta(minutes=duration_minutes)
    service_time_end = end_datetime.time()

    # Generate order number
    order_number = generate_order_number()

    # Create order (using customer_id = 1 for demo, in real app this would come from auth)
    cursor.execute("""
        INSERT INTO orders (order_number, customer_id, service_type_id, service_duration_id,
                          service_date, service_time_start, service_time_end, base_price, total_price,
                          customer_notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (order_number, 1, order.service_type_id, order.service_duration_id,
          str(order.service_date), str(order.service_time_start), str(service_time_end),
          base_price, total_price, order.customer_notes))

    order_id = cursor.lastrowid
    conn.commit()

    # Get customer name for response
    cursor.execute("SELECT first_name, last_name FROM users WHERE id = 1")
    customer = cursor.fetchone()
    customer_name = f"{customer['first_name']} {customer['last_name']}" if customer else "Unknown"

    conn.close()

    return OrderResponse(
        id=order_id,
        order_number=order_number,
        customer_name=customer_name,
        service_date=order.service_date,
        service_time_start=order.service_time_start,
        service_time_end=service_time_end,
        total_price=total_price,
        status="pending",
        service_type_name=service_data["name"]
    )

@app.get("/api/orders", response_model=List[OrderResponse])
async def get_orders(status: Optional[str] = None):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT o.id, o.order_number, o.service_date, o.service_time_start, o.service_time_end,
               o.total_price, o.status, st.name as service_type_name,
               u.first_name, u.last_name
        FROM orders o
        JOIN users u ON o.customer_id = u.id
        JOIN service_types st ON o.service_type_id = st.id
    """

    params = []
    if status and status != "all":
        if status == "in_progress":
            query += " WHERE o.status = 'in_progress'"
        elif status == "completed":
            query += " WHERE o.status = 'completed'"
        else:
            query += " WHERE o.status = ?"
            params.append(status)

    query += " ORDER BY o.created_at DESC"

    cursor.execute(query, params)

    orders = []
    for row in cursor.fetchall():
        customer_name = f"{row['first_name']} {row['last_name']}" if row['first_name'] else "Unknown"
        orders.append(OrderResponse(
            id=row["id"],
            order_number=row["order_number"],
            customer_name=customer_name,
            service_date=datetime.strptime(row["service_date"], "%Y-%m-%d").date(),
            service_time_start=datetime.strptime(row["service_time_start"], "%H:%M:%S").time(),
            service_time_end=datetime.strptime(row["service_time_end"], "%H:%M:%S").time(),
            total_price=row["total_price"],
            status=row["status"],
            service_type_name=row["service_type_name"]
        ))

    conn.close()
    return orders

@app.get("/api/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT o.id, o.order_number, o.service_date, o.service_time_start, o.service_time_end,
               o.total_price, o.status, st.name as service_type_name,
               u.first_name, u.last_name
        FROM orders o
        JOIN users u ON o.customer_id = u.id
        JOIN service_types st ON o.service_type_id = st.id
        WHERE o.id = ?
    """, (order_id,))

    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Order not found")

    customer_name = f"{row['first_name']} {row['last_name']}" if row['first_name'] else "Unknown"

    conn.close()
    return OrderResponse(
        id=row["id"],
        order_number=row["order_number"],
        customer_name=customer_name,
        service_date=datetime.strptime(row["service_date"], "%Y-%m-%d").date(),
        service_time_start=datetime.strptime(row["service_time_start"], "%H:%M:%S").time(),
        service_time_end=datetime.strptime(row["service_time_end"], "%H:%M:%S").time(),
        total_price=row["total_price"],
        status=row["status"],
        service_type_name=row["service_type_name"]
    )

# Order status update endpoint
@app.put("/api/orders/{order_id}/status")
async def update_order_status(order_id: int, status: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Validate status
    valid_statuses = ['pending', 'confirmed', 'in_progress', 'completed', 'cancelled']
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")

    # Check if order exists
    cursor.execute("SELECT id, status FROM orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update order status
    update_time = datetime.now().isoformat()
    cursor.execute("""
        UPDATE orders
        SET status = ?, updated_at = ?, confirmed_at = ?, completed_at = ?
        WHERE id = ?
    """, (
        status,
        update_time,
        update_time if status == 'confirmed' else None,
        update_time if status == 'completed' else None,
        order_id
    ))

    # Add to status history
    cursor.execute("""
        INSERT INTO order_status_history (order_id, old_status, new_status, changed_by, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (order_id, order['status'], status, 1, update_time))  # Using user_id = 1 for demo

    conn.commit()
    conn.close()

    return {"message": "Order status updated successfully", "order_id": order_id, "new_status": status}

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)