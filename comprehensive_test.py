#!/usr/bin/env python3
"""
MyClean项目全面功能测试
"""

import requests
import json
import random
import string
from datetime import datetime, date, timedelta

BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:5173"

def log(message, level="INFO"):
    """日志输出"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    colors = {
        "INFO": "\033[94m",
        "SUCCESS": "\033[92m",
        "ERROR": "\033[91m",
        "WARNING": "\033[93m"
    }
    color = colors.get(level, "")
    print(f"{color}[{timestamp}] {level}: {message}\033[0m")

def generate_test_email():
    """生成测试邮箱"""
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{random_str}@example.com"

def test_backend_health():
    """测试后端健康状态"""
    log("测试后端健康状态...")
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            log(f"✓ 后端健康检查通过: {data['status']}", "SUCCESS")
            return True
        else:
            log(f"✗ 后端健康检查失败: {response.status_code}", "ERROR")
            return False
    except Exception as e:
        log(f"✗ 后端连接失败: {e}", "ERROR")
        return False

def test_frontend_health():
    """测试前端健康状态"""
    log("测试前端健康状态...")
    try:
        response = requests.get(FRONTEND_URL, timeout=10)
        if response.status_code == 200:
            log("✓ 前端页面可访问", "SUCCESS")
            return True
        else:
            log(f"✗ 前端页面访问失败: {response.status_code}", "ERROR")
            return False
    except Exception as e:
        log(f"✗ 前端连接失败: {e}", "ERROR")
        return False

def test_user_registration():
    """测试用户注册功能"""
    log("测试用户注册功能...")
    
    # 测试客户注册
    customer_email = generate_test_email()
    customer_data = {
        "email": customer_email,
        "password": "password123",
        "first_name": "Test",
        "last_name": "Customer",
        "phone": "+1234567890"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/auth/register", json=customer_data, timeout=10)
        if response.status_code == 200:
            user_data = response.json()
            log(f"✓ 客户注册成功: {customer_email}", "SUCCESS")
            log(f"  用户ID: {user_data['id']}, 是否提供者: {user_data['is_provider']}", "INFO")
            return True, customer_data
        else:
            log(f"✗ 客户注册失败: {response.status_code} - {response.text}", "ERROR")
            return False, None
    except Exception as e:
        log(f"✗ 客户注册异常: {e}", "ERROR")
        return False, None

def test_user_login(user_data):
    """测试用户登录功能"""
    log("测试用户登录功能...")
    
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/auth/login", json=login_data, timeout=10)
        if response.status_code == 200:
            login_result = response.json()
            log(f"✓ 用户登录成功: {user_data['email']}", "SUCCESS")
            log(f"  用户ID: {login_result['id']}, 角色: {'提供者' if login_result['is_provider'] else '客户'}", "INFO")
            return True
        else:
            log(f"✗ 用户登录失败: {response.status_code} - {response.text}", "ERROR")
            return False
    except Exception as e:
        log(f"✗ 用户登录异常: {e}", "ERROR")
        return False

def test_services_api():
    """测试服务API"""
    log("测试服务API...")
    
    try:
        # 获取服务列表
        response = requests.get(f"{BACKEND_URL}/api/services", timeout=10)
        if response.status_code == 200:
            services = response.json()
            log(f"✓ 获取服务列表成功，共{len(services)}个服务", "SUCCESS")
            
            # 显示服务详情
            for i, service in enumerate(services[:3]):
                log(f"  服务{i+1}: {service['name']} - ${service['base_price']} ({service['category_name']})", "INFO")
            
            # 测试获取服务时长
            if services:
                service_id = services[0]["id"]
                response = requests.get(f"{BACKEND_URL}/api/services/{service_id}/durations", timeout=10)
                if response.status_code == 200:
                    durations = response.json()
                    log(f"✓ 获取服务时长成功，共{len(durations)}个选项", "SUCCESS")
                    for duration in durations[:2]:
                        log(f"  时长: {duration['duration_label']} (倍数: {duration['price_multiplier']})", "INFO")
                    return True, services
                else:
                    log(f"✗ 获取服务时长失败: {response.status_code}", "ERROR")
                    return False, []
            else:
                log("⚠ 没有可用的服务", "WARNING")
                return True, []
        else:
            log(f"✗ 获取服务列表失败: {response.status_code}", "ERROR")
            return False, []
    except Exception as e:
        log(f"✗ 服务API测试异常: {e}", "ERROR")
        return False, []

def test_order_creation(services):
    """测试订单创建功能"""
    log("测试订单创建功能...")
    
    if not services:
        log("⚠ 没有可用服务，跳过订单测试", "WARNING")
        return True
    
    try:
        # 获取第一个服务的时长选项
        service = services[0]
        service_id = service["id"]
        
        response = requests.get(f"{BACKEND_URL}/api/services/{service_id}/durations", timeout=10)
        if response.status_code != 200:
            log("✗ 无法获取服务时长", "ERROR")
            return False
        
        durations = response.json()
        if not durations:
            log("✗ 没有可用的服务时长", "ERROR")
            return False
        
        # 创建订单
        tomorrow = (datetime.now() + timedelta(days=1)).date()
        order_data = {
            "service_type_id": service_id,
            "service_duration_id": durations[0]["id"],
            "service_date": tomorrow.isoformat(),
            "service_time_start": "10:00:00",
            "customer_notes": "功能测试订单"
        }
        
        response = requests.post(f"{BACKEND_URL}/api/orders", json=order_data, timeout=10)
        if response.status_code == 200:
            order = response.json()
            log(f"✓ 订单创建成功: {order['order_number']}", "SUCCESS")
            log(f"  服务: {order['service_type_name']}", "INFO")
            log(f"  日期: {order['service_date']} {order['service_time_start']}", "INFO")
            log(f"  价格: ${order['total_price']}", "INFO")
            return True
        else:
            log(f"✗ 订单创建失败: {response.status_code} - {response.text}", "ERROR")
            return False
    except Exception as e:
        log(f"✗ 订单创建异常: {e}", "ERROR")
        return False

def test_orders_api():
    """测试订单查询API"""
    log("测试订单查询API...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/api/orders", timeout=10)
        if response.status_code == 200:
            orders = response.json()
            log(f"✓ 获取订单列表成功，共{len(orders)}个订单", "SUCCESS")
            
            # 显示最近的订单
            for i, order in enumerate(orders[:2]):
                log(f"  订单{i+1}: {order['order_number']} - {order['service_type_name']} (${order['total_price']})", "INFO")
            
            return True
        else:
            log(f"✗ 获取订单列表失败: {response.status_code}", "ERROR")
            return False
    except Exception as e:
        log(f"✗ 订单API测试异常: {e}", "ERROR")
        return False

def main():
    """主测试函数"""
    print("MyClean 项目全面功能测试")
    print("=" * 50)
    
    test_results = []
    
    # 1. 测试后端健康状态
    result = test_backend_health()
    test_results.append(("后端健康检查", result))
    if not result:
        log("后端服务不可用，停止测试", "ERROR")
        return
    
    # 2. 测试前端健康状态
    result = test_frontend_health()
    test_results.append(("前端健康检查", result))
    
    # 3. 测试用户注册
    result, user_data = test_user_registration()
    test_results.append(("用户注册", result))
    if not result:
        log("用户注册失败，跳过后续测试", "ERROR")
        return
    
    # 4. 测试用户登录
    result = test_user_login(user_data)
    test_results.append(("用户登录", result))
    
    # 5. 测试服务API
    result, services = test_services_api()
    test_results.append(("服务API", result))
    
    # 6. 测试订单创建
    result = test_order_creation(services)
    test_results.append(("订单创建", result))
    
    # 7. 测试订单查询
    result = test_orders_api()
    test_results.append(("订单查询", result))
    
    # 总结
    print("\n" + "=" * 50)
    log("功能测试总结:", "INFO")
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✓ 通过" if result else "✗ 失败"
        level = "SUCCESS" if result else "ERROR"
        log(f"{status} - {test_name}", level)
        if result:
            passed += 1
    
    log(f"\n测试结果: {passed}/{total} 项通过", "SUCCESS" if passed == total else "WARNING")
    
    if passed == total:
        log("🎉 所有功能测试通过！项目运行正常！", "SUCCESS")
    else:
        log(f"⚠️ {total - passed} 项测试失败，请检查相关功能", "WARNING")

if __name__ == "__main__":
    main()
