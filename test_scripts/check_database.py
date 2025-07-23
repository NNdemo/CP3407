#!/usr/bin/env python3
"""
检查数据库结构和内容
"""

import sqlite3
import os

def check_database():
    db_path = "../backend/myclean.db"

    print(f"检查数据库: {db_path}")

    if not os.path.exists(db_path):
        print("❌ 数据库文件不存在")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 检查表结构
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"✓ 数据库连接成功，找到 {len(tables)} 个表:")
        for table in tables:
            print(f"  - {table[0]}")

        # 检查users表结构
        if ('users',) in tables:
            cursor.execute("PRAGMA table_info(users)")
            columns = cursor.fetchall()
            print(f"\n✓ users表结构 ({len(columns)} 列):")
            for col in columns:
                nullable = "NULL" if not col[3] else "NOT NULL"
                pk = "PRIMARY KEY" if col[5] else ""
                print(f"  {col[1]} {col[2]} {nullable} {pk}")

            # 检查users表数据
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            print(f"\n✓ users表中有 {count} 条记录")

            if count > 0:
                cursor.execute("SELECT id, email, first_name, last_name, is_provider FROM users LIMIT 5")
                users = cursor.fetchall()
                print("前5个用户:")
                for user in users:
                    print(f"  ID: {user[0]}, Email: {user[1]}, Name: {user[2]} {user[3]}, Provider: {user[4]}")
        else:
            print("❌ users表不存在")
            return False

        # 检查service_types表
        if ('service_types',) in tables:
            cursor.execute("SELECT COUNT(*) FROM service_types")
            count = cursor.fetchone()[0]
            print(f"\n✓ service_types表中有 {count} 条记录")

            if count > 0:
                cursor.execute("SELECT id, name, base_price FROM service_types LIMIT 3")
                services = cursor.fetchall()
                print("前3个服务:")
                for service in services:
                    print(f"  ID: {service[0]}, Name: {service[1]}, Price: ${service[2]}")
        else:
            print("❌ service_types表不存在")

        conn.close()
        return True

    except Exception as e:
        print(f"❌ 数据库检查失败: {e}")
        return False

if __name__ == "__main__":
    print("MyClean 数据库检查工具")
    print("=" * 30)
    success = check_database()
    if success:
        print("\n✅ 数据库检查完成")
    else:
        print("\n❌ 数据库检查失败")
