"""
Database setup and initialization for MyClean application
"""
import sqlite3
import os
from datetime import datetime
import hashlib

def create_database():
    """Create the SQLite database and tables"""
    db_path = "myclean.db"

    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Read and execute the schema
    with open('database_schema.sql', 'r') as f:
        schema_sql = f.read()

    # SQLite doesn't support SERIAL, so we need to modify the schema
    schema_sql = schema_sql.replace('SERIAL PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT')
    schema_sql = schema_sql.replace('TIMESTAMP DEFAULT CURRENT_TIMESTAMP', 'DATETIME DEFAULT CURRENT_TIMESTAMP')

    # Execute schema in parts (SQLite doesn't handle multiple statements well)
    statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]

    for statement in statements:
        if statement:
            try:
                cursor.execute(statement)
            except sqlite3.Error as e:
                print(f"Error executing statement: {e}")
                print(f"Statement: {statement[:100]}...")

    conn.commit()
    conn.close()
    print(f"Database created successfully at {db_path}")

def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def seed_test_data():
    """Add some test data to the database"""
    conn = sqlite3.connect("myclean.db")
    cursor = conn.cursor()

    # Create test users
    test_users = [
        ('customer@test.com', '1234567890', hash_password('password123'), 'John', 'Doe', True, False),
        ('provider@test.com', '0987654321', hash_password('password123'), 'Jane', 'Smith', True, True),
        ('admin@test.com', '1122334455', hash_password('admin123'), 'Admin', 'User', True, True)
    ]

    cursor.executemany('''
        INSERT INTO users (email, phone, password_hash, first_name, last_name, is_active, is_provider)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', test_users)

    # Create test orders
    test_orders = [
        ('XXX123', 1, 2, 1, 1, '2025-10-05', '11:00:00', '12:00:00', 21.00, 21.00, 'completed', 'Please handle with care', 'Delivered successfully'),
        ('XXX124', 1, 2, 1, 1, '2025-10-06', '14:00:00', '15:00:00', 21.00, 21.00, 'in_progress', 'Standard delivery', ''),
        ('XXX125', 1, 2, 2, 2, '2025-10-07', '10:00:00', '12:00:00', 25.00, 37.50, 'pending', 'Gift wrapping requested', '')
    ]

    cursor.executemany('''
        INSERT INTO orders (order_number, customer_id, provider_id, service_type_id, service_duration_id,
                          service_date, service_time_start, service_time_end, base_price, total_price,
                          status, customer_notes, provider_notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', test_orders)

    conn.commit()
    conn.close()
    print("Test data seeded successfully")

if __name__ == "__main__":
    create_database()
    seed_test_data()