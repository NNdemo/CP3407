#!/usr/bin/env python3
"""
MyClean 后端API测试脚本
仅测试后端API功能，不需要前端运行

运行方式: C:\\Python312\\python.exe test_backend_only.py
"""

import requests
import json
import time
import random
import string
from datetime import datetime, date, timedelta
import subprocess
import sys
import os

# 配置
BACKEND_URL = "http://localhost:8000"

class BackendTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_users = []
        self.backend_process = None
        
    def log(self, message, level="INFO"):
        """简单的日志输出"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {
            "INFO": "",
            "SUCCESS": "\033[92m",  # 绿色
            "ERROR": "\033[91m",    # 红色
            "WARNING": "\033[93m"   # 黄色
        }
        end_color = "\033[0m" if level in colors else ""
        color = colors.get(level, "")
        print(f"[{timestamp}] {color}{level}: {message}{end_color}")
    
    def start_backend(self):
        """启动后端服务"""
        self.log("启动后端服务...")
        try:
            backend_dir = os.path.join(os.path.dirname(__file__), "..", "backend")
            main_py = os.path.join(backend_dir, "main.py")
            
            if not os.path.exists(main_py):
                self.log("找不到backend/main.py文件", "ERROR")
                return False
            
            # 启动后端进程
            self.backend_process = subprocess.Popen(
                [sys.executable, main_py],
                cwd=backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # 等待服务启动
            self.log("等待后端服务启动...")
            for i in range(10):
                time.sleep(2)
                try:
                    response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
                    if response.status_code == 200:
                        self.log("后端服务启动成功", "SUCCESS")
                        return True
                except:
                    continue
            
            self.log("后端服务启动超时", "ERROR")
            return False
            
        except Exception as e:
            self.log(f"启动后端服务失败: {e}", "ERROR")
            return False
    
    def stop_backend(self):
        """停止后端服务"""
        if self.backend_process:
            self.log("停止后端服务...")
            self.backend_process.terminate()
            self.backend_process.wait()
            self.log("后端服务已停止", "INFO")
    
    def generate_test_email(self):
        """生成测试邮箱"""
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"test_{random_str}@example.com"
    
    def test_health_check(self):
        """测试健康检查"""
        self.log("测试后端健康状态...")
        try:
            response = self.session.get(f"{BACKEND_URL}/api/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log(f"✓ 后端健康检查通过: {data.get('status', 'unknown')}", "SUCCESS")
                return True
            else:
                self.log(f"✗ 后端健康检查失败: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"✗ 后端连接失败: {e}", "ERROR")
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
                    login_result = response.json()
                    self.log(f"✓ {user['role']}登录成功: {user['email']}", "SUCCESS")
                    self.log(f"  用户ID: {login_result.get('id')}, 是否提供者: {login_result.get('is_provider')}", "INFO")
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
                
                # 显示服务详情
                for service in services[:3]:  # 只显示前3个
                    self.log(f"  服务: {service['name']} - ${service['base_price']} ({service['category_name']})", "INFO")
                
                # 测试获取服务时长
                if services:
                    service_id = services[0]["id"]
                    response = self.session.get(f"{BACKEND_URL}/api/services/{service_id}/durations", timeout=10)
                    if response.status_code == 200:
                        durations = response.json()
                        self.log(f"✓ 获取服务时长成功，共{len(durations)}个选项", "SUCCESS")
                        for duration in durations:
                            self.log(f"  时长: {duration['duration_label']} (倍数: {duration['price_multiplier']})", "INFO")
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
                "customer_notes": "测试订单 - 自动化测试创建"
            }
            
            response = self.session.post(f"{BACKEND_URL}/api/orders", json=order_data, timeout=10)
            if response.status_code == 200:
                order = response.json()
                self.log(f"✓ 订单创建成功: {order['order_number']}", "SUCCESS")
                self.log(f"  服务: {order['service_type_name']}", "INFO")
                self.log(f"  日期: {order['service_date']} {order['service_time_start']}", "INFO")
                self.log(f"  价格: ${order['total_price']}", "INFO")
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
                
                # 显示最近的订单
                for order in orders[:2]:  # 只显示前2个
                    self.log(f"  订单: {order['order_number']} - {order['service_type_name']} (${order['total_price']})", "INFO")
                
                return True
            else:
                self.log(f"✗ 获取订单列表失败: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"✗ 订单API测试异常: {e}", "ERROR")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        self.log("开始运行MyClean后端API测试", "INFO")
        self.log("=" * 60, "INFO")
        
        # 检查后端是否已经运行
        if not self.test_health_check():
            self.log("后端服务未运行，尝试启动...", "WARNING")
            if not self.start_backend():
                return False
        
        try:
            # 运行测试
            if not self.test_user_registration():
                return False
            
            if not self.test_user_login():
                return False
            
            success, services = self.test_services_api()
            if not success:
                return False
            
            if not self.test_order_creation(services):
                return False
            
            if not self.test_orders_api():
                return False
            
            # 总结
            self.log("=" * 60, "INFO")
            self.log("测试总结:", "INFO")
            self.log(f"✓ 后端健康检查: 通过", "SUCCESS")
            self.log(f"✓ 用户注册: 通过 ({len(self.test_users)}个用户)", "SUCCESS")
            self.log(f"✓ 用户登录: 通过", "SUCCESS")
            self.log(f"✓ 服务API: 通过", "SUCCESS")
            self.log(f"✓ 订单功能: 通过", "SUCCESS")
            self.log("🎉 所有后端API测试通过！", "SUCCESS")
            
            return True
            
        finally:
            # 如果是我们启动的后端，则停止它
            if self.backend_process:
                self.stop_backend()

def main():
    """主函数"""
    print("MyClean 后端API测试脚本")
    print("=" * 40)
    
    tester = BackendTester()
    
    try:
        success = tester.run_all_tests()
        
        if success:
            print("\n✅ 测试完成：后端API功能正常！")
            return 0
        else:
            print("\n❌ 测试失败：请检查后端状态")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n⚠️ 测试被用户中断")
        tester.stop_backend()
        return 1
    except Exception as e:
        print(f"\n❌ 测试脚本异常: {e}")
        import traceback
        traceback.print_exc()
        tester.stop_backend()
        return 1

if __name__ == "__main__":
    exit(main())
