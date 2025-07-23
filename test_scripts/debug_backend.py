#!/usr/bin/env python3
"""
调试后端API的脚本
"""

import requests
import json

BACKEND_URL = "http://localhost:8000"

def test_health():
    """测试健康检查"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/health")
        print(f"健康检查: {response.status_code}")
        print(f"响应: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"健康检查失败: {e}")
        return False

def test_services():
    """测试服务列表"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/services")
        print(f"服务列表: {response.status_code}")
        if response.status_code == 200:
            services = response.json()
            print(f"找到 {len(services)} 个服务")
            for service in services[:2]:
                print(f"  - {service['name']}: ${service['base_price']}")
        else:
            print(f"错误响应: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"服务列表测试失败: {e}")
        return False

def test_register():
    """测试用户注册"""
    user_data = {
        "email": "debug_test@example.com",
        "password": "password123",
        "first_name": "Debug",
        "last_name": "Test",
        "phone": "+1234567890"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/auth/register", json=user_data)
        print(f"用户注册: {response.status_code}")
        if response.status_code == 200:
            user = response.json()
            print(f"注册成功: {user['email']}")
        else:
            print(f"注册失败: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"注册测试失败: {e}")
        return False

def main():
    print("MyClean 后端调试脚本")
    print("=" * 30)
    
    print("\n1. 测试健康检查...")
    if not test_health():
        print("后端服务不可用")
        return
    
    print("\n2. 测试服务列表...")
    test_services()
    
    print("\n3. 测试用户注册...")
    test_register()
    
    print("\n调试完成")

if __name__ == "__main__":
    main()
