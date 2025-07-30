#!/usr/bin/env python3
"""
Database Repair Tool
修复数据库问题
"""

import sqlite3
import os
import hashlib

def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_fresh_database():
    """Create fresh database / 创建全新的数据库"""
    db_path = "../backend/myclean.db"

    # Remove existing database / 删除现有数据库
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Removed old database")

    # Create new database / 创建新数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create users table / 创建users表
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(255) UNIQUE NOT NULL,
            phone VARCHAR(20),
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            is_active BOOLEAN DEFAULT 1,
            is_provider BOOLEAN DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create service_categories table / 创建service_categories表
    cursor.execute('''
        CREATE TABLE service_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create service_types table / 创建service_types表
    cursor.execute('''
        CREATE TABLE service_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER REFERENCES service_categories(id),
            name VARCHAR(100) NOT NULL,
            description TEXT,
            base_price DECIMAL(10,2),
            duration_minutes INTEGER,
            is_active BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create service_durations table / 创建service_durations表
    cursor.execute('''
        CREATE TABLE service_durations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_type_id INTEGER REFERENCES service_types(id),
            duration_minutes INTEGER NOT NULL,
            duration_label VARCHAR(50) NOT NULL,
            price_multiplier DECIMAL(3,2) DEFAULT 1.00,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create orders table / 创建orders表
    cursor.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number VARCHAR(20) UNIQUE NOT NULL,
            customer_id INTEGER REFERENCES users(id),
            provider_id INTEGER REFERENCES users(id),
            service_type_id INTEGER REFERENCES service_types(id),
            service_duration_id INTEGER REFERENCES service_durations(id),
            service_date DATE NOT NULL,
            service_time_start TIME NOT NULL,
            service_time_end TIME NOT NULL,
            base_price DECIMAL(10,2) NOT NULL,
            total_price DECIMAL(10,2) NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            customer_notes TEXT,
            provider_notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            confirmed_at DATETIME,
            completed_at DATETIME
        )
    ''')
    
    # Insert initial data / 插入初始数据
    print("Inserting initial data...")

    # Insert service categories / 插入服务分类
    categories = [
        ('Flowers', 'Fresh flowers and bouquet delivery services'),
        ('Cleaning', 'Professional cleaning services'),
        ('Gifts', 'Special occasion gifts and arrangements')
    ]
    cursor.executemany('INSERT INTO service_categories (name, description) VALUES (?, ?)', categories)
    
    # Insert service types / 插入服务类型
    services = [
        (1, 'Fresh Flowers', 'Beautiful fresh flower arrangements', 21.00, 60),
        (1, 'Dried Flowers', 'Long-lasting dried flower arrangements', 25.00, 60),
        (1, 'Designer Vases', 'Custom designer vase arrangements', 35.00, 90),
        (2, 'House Cleaning', 'Complete house cleaning service', 50.00, 120),
        (2, 'Office Cleaning', 'Professional office cleaning', 40.00, 90),
        (3, 'Aroma Candles', 'Scented candles for special occasions', 15.00, 30)
    ]
    cursor.executemany('''
        INSERT INTO service_types (category_id, name, description, base_price, duration_minutes)
        VALUES (?, ?, ?, ?, ?)
    ''', services)
    
    # Insert service durations / 插入服务时长
    durations = [
        (1, 60, '1 hour', 1.00),
        (1, 120, '2 hours', 1.50),
        (2, 90, '1.5 hours', 1.00),
        (2, 180, '3 hours', 1.80),
        (3, 30, '30 minutes', 1.00),
        (4, 120, '2 hours', 1.00),
        (4, 240, '4 hours', 1.75),
        (5, 90, '1.5 hours', 1.00),
        (5, 180, '3 hours', 1.60),
        (6, 30, '30 minutes', 1.00)
    ]
    cursor.executemany('''
        INSERT INTO service_durations (service_type_id, duration_minutes, duration_label, price_multiplier)
        VALUES (?, ?, ?, ?)
    ''', durations)
    
    # Insert test users / 插入测试用户
    test_users = [
        ('customer@test.com', '1234567890', hash_password('password123'), 'John', 'Doe', 1, 0),
        ('provider@test.com', '0987654321', hash_password('password123'), 'Jane', 'Smith', 1, 1)
    ]
    cursor.executemany('''
        INSERT INTO users (email, phone, password_hash, first_name, last_name, is_active, is_provider)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', test_users)
    
    conn.commit()
    conn.close()
    
    print("✅ Database created successfully!")
    return True

def test_database():
    """Test database / 测试数据库"""
    db_path = "../backend/myclean.db"

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Test queries / 测试查询
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM service_types")
        service_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM service_durations")
        duration_count = cursor.fetchone()[0]

        print(f"✅ Database test successful:")
        print(f"  - Users: {user_count}")
        print(f"  - Services: {service_count}")
        print(f"  - Duration options: {duration_count}")

        conn.close()
        return True

    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def main():
    print("MyClean Database Repair Tool")
    print("=" * 30)

    if create_fresh_database():
        test_database()
        print("\n🎉 Database repair completed!")
    else:
        print("\n❌ Database repair failed")

if __name__ == "__main__":
    main()
