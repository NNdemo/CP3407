#!/usr/bin/env python3
"""
MyClean Application Simple Test Script
简化版测试脚本，专注于核心功能测试
Simplified test script focusing on core functionality testing

Usage: C:\\Python312\\python.exe test_myclean_simple.py
"""

import requests
import json
import time
import random
import string
from datetime import datetime, date, timedelta

# Configuration / 配置
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:5173"

class TestRunner:
    def __init__(self):
        self.session = requests.Session()
        self.test_users = []

    def log(self, message, level="INFO"):
        """Simple log output / 简单的日志输出"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def generate_test_email(self):
        """生成测试邮箱"""
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"test_{random_str}@example.com"
    
    def test_backend_health(self):
        """测试后端健康状态"""
        self.log("测试后端健康状态...")
        try:
            response = self.session.get(f"{BACKEND_URL}/api/health", timeout=10)
            if response.status_code == 200:
                self.log("✓ 后端健康检查通过", "SUCCESS")
                return True
            else:
                self.log(f"✗ 后端健康检查失败: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"✗ 后端连接失败: {e}", "ERROR")
            return False
    
    def test_frontend_health(self):
        """测试前端健康状态"""
        self.log("测试前端健康状态...")
        try:
            response = self.session.get(FRONTEND_URL, timeout=10)
            if response.status_code == 200:
                self.log("✓ 前端页面可访问", "SUCCESS")
                return True
            else:
                self.log(f"✗ 前端页面访问失败: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"✗ 前端连接失败: {e}", "ERROR")
            return False
    
    def test_user_registration(self):
        """测试用户注册"""
        self.log("测试用户注册...")
        
        # 测试客户注册
        customer_email = self.generate_test_email()
        customer_data = {
            "email": customer_email,
            "password": "password123",
            "first_name": "Test",
            "last_name": "Customer",
            "phone": "+1234567890"
        }
        
        try:
            response = self.session.post(f"{BACKEND_URL}/api/auth/register", json=customer_data, timeout=10)
            if response.status_code == 200:
                user_data = response.json()
                self.test_users.append({
                    "email": customer_email,
                    "password": "password123",
                    "role": "customer",
                    "data": user_data
                })
                self.log(f"✓ 客户注册成功: {customer_email}", "SUCCESS")
            else:
                self.log(f"✗ 客户注册失败: {response.status_code} - {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"✗ 客户注册异常: {e}", "ERROR")
            return False
        
        # 测试服务提供者注册
        provider_email = self.generate_test_email()
        provider_data = {
            "email": provider_email,
            "password": "password123",
            "first_name": "Test",
            "last_name": "Provider",
            "phone": "+1234567891"
        }
        
        try:
            response = self.session.post(f"{BACKEND_URL}/api/auth/register", json=provider_data, timeout=10)
            if response.status_code == 200:
                user_data = response.json()
                self.test_users.append({
                    "email": provider_email,
                    "password": "password123",
                    "role": "provider",
                    "data": user_data
                })
                self.log(f"✓ 服务提供者注册成功: {provider_email}", "SUCCESS")
            else:
                self.log(f"✗ 服务提供者注册失败: {response.status_code} - {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"✗ 服务提供者注册异常: {e}", "ERROR")
            return False
        
        return True
    
    def test_user_login(self):
        """测试用户登录"""
        self.log("测试用户登录...")
        
        for user in self.test_users:
            try:
                login_data = {
                    "email": user["email"],
                    "password": user["password"]
                }
                response = self.session.post(f"{BACKEND_URL}/api/auth/login", json=login_data, timeout=10)
                if response.status_code == 200:
                    self.log(f"✓ {user['role']}登录成功: {user['email']}", "SUCCESS")
                else:
                    self.log(f"✗ {user['role']}登录失败: {response.status_code} - {response.text}", "ERROR")
                    return False
            except Exception as e:
                self.log(f"✗ {user['role']}登录异常: {e}", "ERROR")
                return False
        
        return True
    
    def test_services_api(self):
        """测试服务API"""
        self.log("测试服务API...")
        
        try:
            # 获取服务列表
            response = self.session.get(f"{BACKEND_URL}/api/services", timeout=10)
            if response.status_code == 200:
                services = response.json()
                self.log(f"✓ 获取服务列表成功，共{len(services)}个服务", "SUCCESS")
                
                # 测试获取服务时长
                if services:
                    service_id = services[0]["id"]
                    response = self.session.get(f"{BACKEND_URL}/api/services/{service_id}/durations", timeout=10)
                    if response.status_code == 200:
                        durations = response.json()
                        self.log(f"✓ 获取服务时长成功，共{len(durations)}个选项", "SUCCESS")
                        return True, services
                    else:
                        self.log(f"✗ 获取服务时长失败: {response.status_code}", "ERROR")
                        return False, []
                else:
                    self.log("⚠ 没有可用的服务", "WARNING")
                    return True, []
            else:
                self.log(f"✗ 获取服务列表失败: {response.status_code}", "ERROR")
                return False, []
        except Exception as e:
            self.log(f"✗ 服务API测试异常: {e}", "ERROR")
            return False, []
    
    def test_order_creation(self, services):
        """测试订单创建"""
        self.log("测试订单创建...")
        
        if not services:
            self.log("⚠ 没有可用服务，跳过订单测试", "WARNING")
            return True
        
        try:
            # 获取第一个服务的时长选项
            service = services[0]
            service_id = service["id"]
            
            response = self.session.get(f"{BACKEND_URL}/api/services/{service_id}/durations", timeout=10)
            if response.status_code != 200:
                self.log("✗ 无法获取服务时长", "ERROR")
                return False
            
            durations = response.json()
            if not durations:
                self.log("✗ 没有可用的服务时长", "ERROR")
                return False
            
            # 创建订单
            tomorrow = (datetime.now() + timedelta(days=1)).date()
            order_data = {
                "service_type_id": service_id,
                "service_duration_id": durations[0]["id"],
                "service_date": tomorrow.isoformat(),
                "service_time_start": "10:00:00",
                "customer_notes": "测试订单"
            }
            
            response = self.session.post(f"{BACKEND_URL}/api/orders", json=order_data, timeout=10)
            if response.status_code == 200:
                order = response.json()
                self.log(f"✓ 订单创建成功: {order['order_number']}", "SUCCESS")
                return True
            else:
                self.log(f"✗ 订单创建失败: {response.status_code} - {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"✗ 订单创建异常: {e}", "ERROR")
            return False
    
    def test_orders_api(self):
        """测试订单API"""
        self.log("测试订单API...")
        
        try:
            response = self.session.get(f"{BACKEND_URL}/api/orders", timeout=10)
            if response.status_code == 200:
                orders = response.json()
                self.log(f"✓ 获取订单列表成功，共{len(orders)}个订单", "SUCCESS")
                return True
            else:
                self.log(f"✗ 获取订单列表失败: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"✗ 订单API测试异常: {e}", "ERROR")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        self.log("开始运行MyClean应用测试", "INFO")
        self.log("=" * 50, "INFO")
        
        # 测试后端健康状态
        if not self.test_backend_health():
            self.log("后端服务不可用，停止测试", "ERROR")
            return False
        
        # 测试前端健康状态
        frontend_ok = self.test_frontend_health()
        
        # 测试用户注册
        if not self.test_user_registration():
            self.log("用户注册测试失败", "ERROR")
            return False
        
        # 测试用户登录
        if not self.test_user_login():
            self.log("用户登录测试失败", "ERROR")
            return False
        
        # 测试服务API
        success, services = self.test_services_api()
        if not success:
            self.log("服务API测试失败", "ERROR")
            return False
        
        # 测试订单创建
        if not self.test_order_creation(services):
            self.log("订单创建测试失败", "ERROR")
            return False
        
        # 测试订单API
        if not self.test_orders_api():
            self.log("订单API测试失败", "ERROR")
            return False
        
        # 总结
        self.log("=" * 50, "INFO")
        self.log("测试总结:", "INFO")
        self.log(f"✓ 后端服务: 正常", "SUCCESS")
        if frontend_ok:
            self.log(f"✓ 前端服务: 正常", "SUCCESS")
        else:
            self.log(f"⚠ 前端服务: 异常", "WARNING")
        self.log(f"✓ 用户注册: 通过 ({len(self.test_users)}个用户)", "SUCCESS")
        self.log(f"✓ 用户登录: 通过", "SUCCESS")
        self.log(f"✓ 服务API: 通过", "SUCCESS")
        self.log(f"✓ 订单功能: 通过", "SUCCESS")
        self.log("🎉 所有核心功能测试通过！", "SUCCESS")
        
        return True

def main():
    """主函数"""
    print("MyClean 应用测试脚本")
    print("=" * 30)
    
    tester = TestRunner()
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ 测试完成：应用运行正常！")
    else:
        print("\n❌ 测试失败：请检查应用状态")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️ 测试被用户中断")
        exit(1)
    except Exception as e:
        print(f"\n❌ 测试脚本异常: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
