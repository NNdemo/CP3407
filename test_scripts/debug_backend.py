#!/usr/bin/env python3
"""
Backend API Debug Script
调试后端API的脚本
"""

import requests
import json

BACKEND_URL = "http://localhost:8000"

def test_health():
    """Test health check / 测试健康检查"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/health")
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_services():
    """Test service list / 测试服务列表"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/services")
        print(f"Service list: {response.status_code}")
        if response.status_code == 200:
            services = response.json()
            print(f"Found {len(services)} services")
            for service in services[:2]:
                print(f"  - {service['name']}: ${service['base_price']}")
        else:
            print(f"Error response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Service list test failed: {e}")
        return False

def test_register():
    """Test user registration / 测试用户注册"""
    user_data = {
        "email": "debug_test@example.com",
        "password": "password123",
        "first_name": "Debug",
        "last_name": "Test",
        "phone": "+1234567890"
    }

    try:
        response = requests.post(f"{BACKEND_URL}/api/auth/register", json=user_data)
        print(f"User registration: {response.status_code}")
        if response.status_code == 200:
            user = response.json()
            print(f"Registration successful: {user['email']}")
        else:
            print(f"Registration failed: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Registration test failed: {e}")
        return False

def main():
    print("MyClean Backend Debug Script")
    print("=" * 30)

    print("\n1. Testing health check...")
    if not test_health():
        print("Backend service unavailable")
        return

    print("\n2. Testing service list...")
    test_services()

    print("\n3. Testing user registration...")
    test_register()

    print("\nDebug completed")

if __name__ == "__main__":
    main()
