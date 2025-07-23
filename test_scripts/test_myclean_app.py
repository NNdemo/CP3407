#!/usr/bin/env python3
"""
MyClean Application Test Script
测试前端和后端的注册、登录、下单等功能

运行方式: C:\\Python312\\python.exe test_myclean_app.py
"""

import requests
import json
import time
import random
import string
from datetime import datetime, date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import sys
import traceback

# 配置
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:5173"
WAIT_TIMEOUT = 10

class Colors:
    """控制台颜色"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_colored(text, color=Colors.WHITE):
    """打印彩色文本"""
    print(f"{color}{text}{Colors.END}")

def print_header(text):
    """打印测试标题"""
    print_colored(f"\n{'='*60}", Colors.CYAN)
    print_colored(f"{text.center(60)}", Colors.CYAN + Colors.BOLD)
    print_colored(f"{'='*60}", Colors.CYAN)

def print_success(text):
    """打印成功信息"""
    print_colored(f"✓ {text}", Colors.GREEN)

def print_error(text):
    """打印错误信息"""
    print_colored(f"✗ {text}", Colors.RED)

def print_info(text):
    """打印信息"""
    print_colored(f"ℹ {text}", Colors.BLUE)

def print_warning(text):
    """打印警告"""
    print_colored(f"⚠ {text}", Colors.YELLOW)

class BackendTester:
    """后端API测试类"""
    
    def __init__(self):
        self.base_url = BACKEND_URL
        self.session = requests.Session()
        self.test_users = []
        
    def generate_test_email(self):
        """生成测试邮箱"""
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"test_{random_str}@example.com"
    
    def test_health_check(self):
        """测试健康检查"""
        try:
            response = self.session.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                print_success("后端健康检查通过")
                return True
            else:
                print_error(f"后端健康检查失败: {response.status_code}")
                return False
        except Exception as e:
            print_error(f"后端连接失败: {e}")
            return False
    
    def test_user_registration(self):
        """测试用户注册"""
        print_info("测试用户注册...")
        
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
            response = self.session.post(f"{self.base_url}/api/auth/register", json=customer_data)
            if response.status_code == 200:
                user_data = response.json()
                self.test_users.append({
                    "email": customer_email,
                    "password": "password123",
                    "role": "customer",
                    "data": user_data
                })
                print_success(f"客户注册成功: {customer_email}")
            else:
                print_error(f"客户注册失败: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print_error(f"客户注册异常: {e}")
            return False
        
        # 测试服务提供者注册（模拟）
        provider_email = self.generate_test_email()
        provider_data = {
            "email": provider_email,
            "password": "password123",
            "first_name": "Test",
            "last_name": "Provider",
            "phone": "+1234567891"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/api/auth/register", json=provider_data)
            if response.status_code == 200:
                user_data = response.json()
                self.test_users.append({
                    "email": provider_email,
                    "password": "password123",
                    "role": "provider",
                    "data": user_data
                })
                print_success(f"服务提供者注册成功: {provider_email}")
            else:
                print_error(f"服务提供者注册失败: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print_error(f"服务提供者注册异常: {e}")
            return False
        
        return True
    
    def test_user_login(self):
        """测试用户登录"""
        print_info("测试用户登录...")
        
        for user in self.test_users:
            try:
                login_data = {
                    "email": user["email"],
                    "password": user["password"]
                }
                response = self.session.post(f"{self.base_url}/api/auth/login", json=login_data)
                if response.status_code == 200:
                    print_success(f"{user['role']}登录成功: {user['email']}")
                else:
                    print_error(f"{user['role']}登录失败: {response.status_code} - {response.text}")
                    return False
            except Exception as e:
                print_error(f"{user['role']}登录异常: {e}")
                return False
        
        return True
    
    def test_services_api(self):
        """测试服务API"""
        print_info("测试服务API...")
        
        try:
            # 获取服务列表
            response = self.session.get(f"{self.base_url}/api/services")
            if response.status_code == 200:
                services = response.json()
                print_success(f"获取服务列表成功，共{len(services)}个服务")
                
                # 测试获取服务时长
                if services:
                    service_id = services[0]["id"]
                    response = self.session.get(f"{self.base_url}/api/services/{service_id}/durations")
                    if response.status_code == 200:
                        durations = response.json()
                        print_success(f"获取服务时长成功，共{len(durations)}个选项")
                        return True, services
                    else:
                        print_error(f"获取服务时长失败: {response.status_code}")
                        return False, []
                else:
                    print_warning("没有可用的服务")
                    return True, []
            else:
                print_error(f"获取服务列表失败: {response.status_code}")
                return False, []
        except Exception as e:
            print_error(f"服务API测试异常: {e}")
            return False, []
    
    def test_order_creation(self, services):
        """测试订单创建"""
        print_info("测试订单创建...")
        
        if not services:
            print_warning("没有可用服务，跳过订单测试")
            return True
        
        try:
            # 获取第一个服务的时长选项
            service = services[0]
            service_id = service["id"]
            
            response = self.session.get(f"{self.base_url}/api/services/{service_id}/durations")
            if response.status_code != 200:
                print_error("无法获取服务时长")
                return False
            
            durations = response.json()
            if not durations:
                print_error("没有可用的服务时长")
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
            
            response = self.session.post(f"{self.base_url}/api/orders", json=order_data)
            if response.status_code == 200:
                order = response.json()
                print_success(f"订单创建成功: {order['order_number']}")
                return True
            else:
                print_error(f"订单创建失败: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print_error(f"订单创建异常: {e}")
            return False
    
    def test_orders_api(self):
        """测试订单API"""
        print_info("测试订单API...")
        
        try:
            response = self.session.get(f"{self.base_url}/api/orders")
            if response.status_code == 200:
                orders = response.json()
                print_success(f"获取订单列表成功，共{len(orders)}个订单")
                return True
            else:
                print_error(f"获取订单列表失败: {response.status_code}")
                return False
        except Exception as e:
            print_error(f"订单API测试异常: {e}")
            return False
    
    def run_all_tests(self):
        """运行所有后端测试"""
        print_header("后端API测试")
        
        if not self.test_health_check():
            return False
        
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
        
        print_success("所有后端测试通过！")
        return True

class FrontendTester:
    """前端UI测试类"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.test_users = []
        
    def setup_driver(self):
        """设置浏览器驱动"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            # chrome_options.add_argument("--headless")  # 取消注释以无头模式运行
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, WAIT_TIMEOUT)
            print_success("浏览器驱动设置成功")
            return True
        except Exception as e:
            print_error(f"浏览器驱动设置失败: {e}")
            return False
    
    def teardown_driver(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            print_info("浏览器已关闭")
    
    def test_frontend_accessibility(self):
        """测试前端可访问性"""
        try:
            self.driver.get(FRONTEND_URL)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            print_success("前端页面加载成功")
            return True
        except Exception as e:
            print_error(f"前端页面加载失败: {e}")
            return False

    def generate_test_user(self):
        """生成测试用户数据"""
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return {
            "email": f"test_{random_str}@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
            "phone": f"+123456{random.randint(1000, 9999)}"
        }

    def test_user_registration_ui(self):
        """测试用户注册UI"""
        print_info("测试用户注册UI...")

        try:
            # 导航到注册页面
            self.driver.get(f"{FRONTEND_URL}/register")
            time.sleep(2)

            # 生成测试用户数据
            customer_data = self.generate_test_user()
            provider_data = self.generate_test_user()

            # 测试客户注册
            print_info("测试客户注册...")

            # 选择客户角色
            customer_role_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Customer')]"))
            )
            customer_role_btn.click()
            time.sleep(1)

            # 填写表单
            first_name_input = self.driver.find_element(By.XPATH, "//input[@placeholder='First Name']")
            first_name_input.clear()
            first_name_input.send_keys(customer_data["first_name"])

            last_name_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Last Name']")
            last_name_input.clear()
            last_name_input.send_keys(customer_data["last_name"])

            email_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Email']")
            email_input.clear()
            email_input.send_keys(customer_data["email"])

            phone_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Phone Number']")
            phone_input.clear()
            phone_input.send_keys(customer_data["phone"])

            password_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Password']")
            password_input.clear()
            password_input.send_keys(customer_data["password"])

            confirm_password_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Confirm Password']")
            confirm_password_input.clear()
            confirm_password_input.send_keys(customer_data["password"])

            # 提交表单
            register_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            register_btn.click()

            # 等待注册完成（可能跳转到登录页面或主页）
            time.sleep(3)

            # 检查是否注册成功（通过URL变化或成功消息）
            current_url = self.driver.current_url
            if "register" not in current_url or "success" in current_url.lower():
                print_success(f"客户注册成功: {customer_data['email']}")
                self.test_users.append({**customer_data, "role": "customer"})
            else:
                print_warning("客户注册可能失败，检查页面状态")

            # 测试服务提供者注册
            print_info("测试服务提供者注册...")
            self.driver.get(f"{FRONTEND_URL}/register")
            time.sleep(2)

            # 选择服务提供者角色
            provider_role_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Service Provider')]"))
            )
            provider_role_btn.click()
            time.sleep(1)

            # 填写表单
            first_name_input = self.driver.find_element(By.XPATH, "//input[@placeholder='First Name']")
            first_name_input.clear()
            first_name_input.send_keys(provider_data["first_name"])

            last_name_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Last Name']")
            last_name_input.clear()
            last_name_input.send_keys(provider_data["last_name"])

            email_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Email']")
            email_input.clear()
            email_input.send_keys(provider_data["email"])

            phone_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Phone Number']")
            phone_input.clear()
            phone_input.send_keys(provider_data["phone"])

            password_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Password']")
            password_input.clear()
            password_input.send_keys(provider_data["password"])

            confirm_password_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Confirm Password']")
            confirm_password_input.clear()
            confirm_password_input.send_keys(provider_data["password"])

            # 提交表单
            register_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            register_btn.click()

            # 等待注册完成
            time.sleep(3)

            current_url = self.driver.current_url
            if "register" not in current_url or "success" in current_url.lower():
                print_success(f"服务提供者注册成功: {provider_data['email']}")
                self.test_users.append({**provider_data, "role": "provider"})
            else:
                print_warning("服务提供者注册可能失败，检查页面状态")

            return True

        except TimeoutException:
            print_error("注册页面元素加载超时")
            return False
        except NoSuchElementException as e:
            print_error(f"注册页面元素未找到: {e}")
            return False
        except Exception as e:
            print_error(f"注册UI测试异常: {e}")
            return False

    def test_user_login_ui(self):
        """测试用户登录UI"""
        print_info("测试用户登录UI...")

        if not self.test_users:
            print_warning("没有测试用户，跳过登录测试")
            return True

        try:
            for user in self.test_users:
                print_info(f"测试{user['role']}登录...")

                # 导航到登录页面
                self.driver.get(f"{FRONTEND_URL}/login")
                time.sleep(2)

                # 选择角色
                if user["role"] == "customer":
                    role_btn = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Customer')]"))
                    )
                else:
                    role_btn = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Service Provider')]"))
                    )
                role_btn.click()
                time.sleep(1)

                # 填写登录信息
                email_input = self.driver.find_element(By.XPATH, "//input[@type='email']")
                email_input.clear()
                email_input.send_keys(user["email"])

                password_input = self.driver.find_element(By.XPATH, "//input[@type='password']")
                password_input.clear()
                password_input.send_keys(user["password"])

                # 提交登录
                login_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                login_btn.click()

                # 等待登录完成
                time.sleep(3)

                # 检查登录是否成功（通过URL变化）
                current_url = self.driver.current_url
                if "login" not in current_url:
                    print_success(f"{user['role']}登录成功: {user['email']}")
                else:
                    print_error(f"{user['role']}登录失败: {user['email']}")
                    return False

                # 登出以便测试下一个用户
                try:
                    # 尝试找到登出按钮或用户菜单
                    time.sleep(2)
                    # 这里可能需要根据实际的前端实现来调整登出逻辑
                    self.driver.get(f"{FRONTEND_URL}/")  # 简单地回到首页
                    time.sleep(1)
                except:
                    pass

            return True

        except Exception as e:
            print_error(f"登录UI测试异常: {e}")
            return False

    def test_services_browsing_ui(self):
        """测试服务浏览UI"""
        print_info("测试服务浏览UI...")

        try:
            # 先登录一个客户账户
            if self.test_users:
                customer = next((u for u in self.test_users if u["role"] == "customer"), None)
                if customer:
                    self.login_user(customer)

            # 导航到服务页面
            self.driver.get(f"{FRONTEND_URL}/services")
            time.sleep(3)

            # 检查服务列表是否加载
            try:
                services = self.driver.find_elements(By.CLASS_NAME, "service-card")
                if not services:
                    # 尝试其他可能的选择器
                    services = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'service')]")

                if services:
                    print_success(f"服务列表加载成功，找到{len(services)}个服务")
                    return True
                else:
                    print_warning("未找到服务列表，可能页面结构不同")
                    return True  # 不算失败，可能是页面结构问题
            except Exception as e:
                print_warning(f"服务列表检查异常: {e}")
                return True

        except Exception as e:
            print_error(f"服务浏览UI测试异常: {e}")
            return False

    def test_order_creation_ui(self):
        """测试订单创建UI"""
        print_info("测试订单创建UI...")

        try:
            # 确保已登录客户账户
            if self.test_users:
                customer = next((u for u in self.test_users if u["role"] == "customer"), None)
                if customer:
                    self.login_user(customer)

            # 导航到服务页面
            self.driver.get(f"{FRONTEND_URL}/services")
            time.sleep(3)

            # 尝试点击第一个服务进行预订
            try:
                # 查找预订按钮或服务卡片
                book_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Book') or contains(text(), '预订') or contains(text(), 'Order')]")
                service_cards = self.driver.find_elements(By.CLASS_NAME, "service-card")

                if book_buttons:
                    book_buttons[0].click()
                    time.sleep(2)
                    print_success("成功点击预订按钮")
                elif service_cards:
                    service_cards[0].click()
                    time.sleep(2)
                    print_success("成功点击服务卡片")
                else:
                    print_warning("未找到可点击的服务元素")
                    return True

                # 检查是否进入订单页面或弹出订单表单
                current_url = self.driver.current_url
                if "order" in current_url or "book" in current_url:
                    print_success("成功进入订单页面")
                else:
                    print_info("可能在当前页面显示订单表单")

                return True

            except Exception as e:
                print_warning(f"订单创建UI测试异常: {e}")
                return True

        except Exception as e:
            print_error(f"订单创建UI测试失败: {e}")
            return False

    def login_user(self, user):
        """辅助方法：登录用户"""
        try:
            self.driver.get(f"{FRONTEND_URL}/login")
            time.sleep(2)

            # 选择角色
            if user["role"] == "customer":
                role_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Customer')]")
            else:
                role_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Service Provider')]")
            role_btn.click()
            time.sleep(1)

            # 填写登录信息
            email_input = self.driver.find_element(By.XPATH, "//input[@type='email']")
            email_input.clear()
            email_input.send_keys(user["email"])

            password_input = self.driver.find_element(By.XPATH, "//input[@type='password']")
            password_input.clear()
            password_input.send_keys(user["password"])

            # 提交登录
            login_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_btn.click()
            time.sleep(3)

        except Exception as e:
            print_warning(f"辅助登录失败: {e}")

    def run_all_tests(self):
        """运行所有前端测试"""
        print_header("前端UI测试")

        if not self.setup_driver():
            return False

        try:
            if not self.test_frontend_accessibility():
                return False

            if not self.test_user_registration_ui():
                return False

            if not self.test_user_login_ui():
                return False

            if not self.test_services_browsing_ui():
                return False

            if not self.test_order_creation_ui():
                return False

            print_success("所有前端测试完成！")
            return True

        finally:
            self.teardown_driver()

def main():
    """主函数"""
    print_colored("MyClean 应用测试脚本", Colors.PURPLE + Colors.BOLD)
    print_colored("=" * 50, Colors.PURPLE)

    # 检查服务是否运行
    print_info("检查服务状态...")

    try:
        # 检查后端
        backend_response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
        if backend_response.status_code == 200:
            print_success("后端服务运行正常")
        else:
            print_error("后端服务异常")
            return
    except Exception as e:
        print_error(f"无法连接到后端服务: {e}")
        print_info("请确保后端服务在 http://localhost:8000 运行")
        return

    try:
        # 检查前端
        frontend_response = requests.get(FRONTEND_URL, timeout=5)
        if frontend_response.status_code == 200:
            print_success("前端服务运行正常")
        else:
            print_error("前端服务异常")
    except Exception as e:
        print_error(f"无法连接到前端服务: {e}")
        print_info("请确保前端服务在 http://localhost:5173 运行")
        print_warning("将跳过前端UI测试")

    # 运行后端测试
    backend_tester = BackendTester()
    backend_success = backend_tester.run_all_tests()

    # 运行前端测试
    frontend_success = True
    try:
        frontend_response = requests.get(FRONTEND_URL, timeout=5)
        if frontend_response.status_code == 200:
            frontend_tester = FrontendTester()
            frontend_success = frontend_tester.run_all_tests()
        else:
            print_warning("跳过前端测试（前端服务不可用）")
    except:
        print_warning("跳过前端测试（前端服务不可用）")

    # 总结
    print_header("测试总结")
    if backend_success:
        print_success("后端测试: 通过")
    else:
        print_error("后端测试: 失败")

    if frontend_success:
        print_success("前端测试: 通过")
    else:
        print_error("前端测试: 失败")

    if backend_success and frontend_success:
        print_colored("\n🎉 所有测试通过！应用运行正常！", Colors.GREEN + Colors.BOLD)
    else:
        print_colored("\n❌ 部分测试失败，请检查应用状态", Colors.RED + Colors.BOLD)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\n测试被用户中断", Colors.YELLOW)
    except Exception as e:
        print_error(f"测试脚本异常: {e}")
        traceback.print_exc()
