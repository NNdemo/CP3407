#!/usr/bin/env python3
"""
Database Structure and Content Checker
检查数据库结构和内容
"""

import sqlite3
import os

def check_database():
    db_path = "../backend/myclean.db"

    print(f"Checking database: {db_path}")

    if not os.path.exists(db_path):
        print("❌ Database file does not exist")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check table structure / 检查表结构
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"✓ Database connection successful, found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")

        # Check users table structure / 检查users表结构
        if ('users',) in tables:
            cursor.execute("PRAGMA table_info(users)")
            columns = cursor.fetchall()
            print(f"\n✓ Users table structure ({len(columns)} columns):")
            for col in columns:
                nullable = "NULL" if not col[3] else "NOT NULL"
                pk = "PRIMARY KEY" if col[5] else ""
                print(f"  {col[1]} {col[2]} {nullable} {pk}")

            # Check users table data / 检查users表数据
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            print(f"\n✓ Users table has {count} records")

            if count > 0:
                cursor.execute("SELECT id, email, first_name, last_name, is_provider FROM users LIMIT 5")
                users = cursor.fetchall()
                print("First 5 users:")
                for user in users:
                    print(f"  ID: {user[0]}, Email: {user[1]}, Name: {user[2]} {user[3]}, Provider: {user[4]}")
        else:
            print("❌ Users table does not exist")
            return False

        # Check service_types table / 检查service_types表
        if ('service_types',) in tables:
            cursor.execute("SELECT COUNT(*) FROM service_types")
            count = cursor.fetchone()[0]
            print(f"\n✓ Service_types table has {count} records")

            if count > 0:
                cursor.execute("SELECT id, name, base_price FROM service_types LIMIT 3")
                services = cursor.fetchall()
                print("First 3 services:")
                for service in services:
                    print(f"  ID: {service[0]}, Name: {service[1]}, Price: ${service[2]}")
        else:
            print("❌ Service_types table does not exist")

        conn.close()
        return True

    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False

if __name__ == "__main__":
    print("MyClean Database Check Tool")
    print("=" * 30)
    success = check_database()
    if success:
        print("\n✅ Database check completed")
    else:
        print("\n❌ Database check failed")
