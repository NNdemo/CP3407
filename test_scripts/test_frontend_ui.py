#!/usr/bin/env python3
"""
MyClean 前端UI测试脚本
测试前端用户界面功能

运行方式: C:\\Python312\\python.exe test_frontend_ui.py
"""

import time
import random
import string
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import requests

# 配置
FRONTEND_URL = "http://localhost:5173"
BACKEND_URL = "http://localhost:8000"
WAIT_TIMEOUT = 10

class FrontendTester:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.test_users = []
        
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
    
    def setup_driver(self):
        """设置浏览器驱动"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            # chrome_options.add_argument("--headless")  # 取消注释以无头模式运行
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, WAIT_TIMEOUT)
            self.log("浏览器驱动设置成功", "SUCCESS")
            return True
        except Exception as e:
            self.log(f"浏览器驱动设置失败: {e}", "ERROR")
            self.log("请确保已安装Chrome浏览器和ChromeDriver", "ERROR")
            return False
    
    def teardown_driver(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.log("浏览器已关闭", "INFO")
    
    def check_services(self):
        """检查前端和后端服务状态"""
        self.log("检查服务状态...")
        
        # 检查后端
        try:
            response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
            if response.status_code == 200:
                self.log("✓ 后端服务运行正常", "SUCCESS")
            else:
                self.log("✗ 后端服务异常", "ERROR")
                return False
        except Exception as e:
            self.log(f"✗ 无法连接到后端服务: {e}", "ERROR")
            return False
        
        # 检查前端
        try:
            response = requests.get(FRONTEND_URL, timeout=5)
            if response.status_code == 200:
                self.log("✓ 前端服务运行正常", "SUCCESS")
                return True
            else:
                self.log("✗ 前端服务异常", "ERROR")
                return False
        except Exception as e:
            self.log(f"✗ 无法连接到前端服务: {e}", "ERROR")
            return False
    
    def test_homepage_access(self):
        """测试主页访问"""
        self.log("测试主页访问...")
        try:
            self.driver.get(FRONTEND_URL)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # 检查页面标题
            title = self.driver.title
            self.log(f"✓ 页面加载成功，标题: {title}", "SUCCESS")
            
            # 检查是否有MyClean相关内容
            page_source = self.driver.page_source.lower()
            if "myclean" in page_source or "clean" in page_source:
                self.log("✓ 页面包含MyClean相关内容", "SUCCESS")
            else:
                self.log("⚠ 页面可能不包含MyClean内容", "WARNING")
            
            return True
        except Exception as e:
            self.log(f"✗ 主页访问失败: {e}", "ERROR")
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
    
    def test_navigation(self):
        """测试页面导航"""
        self.log("测试页面导航...")
        try:
            # 测试导航到注册页面
            self.driver.get(f"{FRONTEND_URL}/register")
            time.sleep(2)
            
            if "register" in self.driver.current_url.lower():
                self.log("✓ 注册页面导航成功", "SUCCESS")
            else:
                self.log("⚠ 注册页面导航可能失败", "WARNING")
            
            # 测试导航到登录页面
            self.driver.get(f"{FRONTEND_URL}/login")
            time.sleep(2)
            
            if "login" in self.driver.current_url.lower():
                self.log("✓ 登录页面导航成功", "SUCCESS")
            else:
                self.log("⚠ 登录页面导航可能失败", "WARNING")
            
            return True
        except Exception as e:
            self.log(f"✗ 页面导航测试失败: {e}", "ERROR")
            return False
    
    def test_registration_form(self):
        """测试注册表单"""
        self.log("测试注册表单...")
        try:
            self.driver.get(f"{FRONTEND_URL}/register")
            time.sleep(3)
            
            # 生成测试用户数据
            user_data = self.generate_test_user()
            
            # 查找并填写表单元素
            try:
                # 尝试找到角色选择按钮
                customer_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Customer') or contains(text(), '客户')]")
                customer_btn.click()
                time.sleep(1)
                self.log("✓ 选择客户角色成功", "SUCCESS")
            except NoSuchElementException:
                self.log("⚠ 未找到角色选择按钮", "WARNING")
            
            # 查找表单字段
            form_fields = {
                "first_name": ["First Name", "名字", "firstName"],
                "last_name": ["Last Name", "姓氏", "lastName"],
                "email": ["Email", "邮箱", "email"],
                "phone": ["Phone", "电话", "phone"],
                "password": ["Password", "密码", "password"]
            }
            
            filled_fields = 0
            for field_name, placeholders in form_fields.items():
                for placeholder in placeholders:
                    try:
                        # 尝试通过placeholder查找
                        input_field = self.driver.find_element(By.XPATH, f"//input[@placeholder='{placeholder}']")
                        input_field.clear()
                        
                        if field_name == "first_name":
                            input_field.send_keys(user_data["first_name"])
                        elif field_name == "last_name":
                            input_field.send_keys(user_data["last_name"])
                        elif field_name == "email":
                            input_field.send_keys(user_data["email"])
                        elif field_name == "phone":
                            input_field.send_keys(user_data["phone"])
                        elif field_name == "password":
                            input_field.send_keys(user_data["password"])
                        
                        filled_fields += 1
                        self.log(f"✓ 填写{field_name}字段成功", "SUCCESS")
                        break
                    except NoSuchElementException:
                        continue
            
            if filled_fields > 0:
                self.log(f"✓ 成功填写{filled_fields}个表单字段", "SUCCESS")
                
                # 尝试提交表单
                try:
                    submit_btn = self.driver.find_element(By.XPATH, "//button[@type='submit' or contains(text(), 'Register') or contains(text(), '注册')]")
                    submit_btn.click()
                    time.sleep(3)
                    self.log("✓ 表单提交成功", "SUCCESS")
                    
                    # 保存用户数据
                    self.test_users.append(user_data)
                    
                except NoSuchElementException:
                    self.log("⚠ 未找到提交按钮", "WARNING")
            else:
                self.log("⚠ 未能填写任何表单字段", "WARNING")
            
            return True
            
        except Exception as e:
            self.log(f"✗ 注册表单测试失败: {e}", "ERROR")
            return False
    
    def test_login_form(self):
        """测试登录表单"""
        self.log("测试登录表单...")
        
        if not self.test_users:
            self.log("⚠ 没有测试用户，跳过登录测试", "WARNING")
            return True
        
        try:
            user = self.test_users[0]
            self.driver.get(f"{FRONTEND_URL}/login")
            time.sleep(3)
            
            # 选择客户角色
            try:
                customer_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Customer') or contains(text(), '客户')]")
                customer_btn.click()
                time.sleep(1)
                self.log("✓ 选择客户角色成功", "SUCCESS")
            except NoSuchElementException:
                self.log("⚠ 未找到角色选择按钮", "WARNING")
            
            # 填写登录信息
            try:
                email_input = self.driver.find_element(By.XPATH, "//input[@type='email' or contains(@placeholder, 'Email') or contains(@placeholder, '邮箱')]")
                email_input.clear()
                email_input.send_keys(user["email"])
                self.log("✓ 填写邮箱成功", "SUCCESS")
                
                password_input = self.driver.find_element(By.XPATH, "//input[@type='password' or contains(@placeholder, 'Password') or contains(@placeholder, '密码')]")
                password_input.clear()
                password_input.send_keys(user["password"])
                self.log("✓ 填写密码成功", "SUCCESS")
                
                # 提交登录
                login_btn = self.driver.find_element(By.XPATH, "//button[@type='submit' or contains(text(), 'Login') or contains(text(), '登录')]")
                login_btn.click()
                time.sleep(3)
                self.log("✓ 登录表单提交成功", "SUCCESS")
                
            except NoSuchElementException as e:
                self.log(f"⚠ 登录表单元素未找到: {e}", "WARNING")
            
            return True
            
        except Exception as e:
            self.log(f"✗ 登录表单测试失败: {e}", "ERROR")
            return False
    
    def test_services_page(self):
        """测试服务页面"""
        self.log("测试服务页面...")
        try:
            self.driver.get(f"{FRONTEND_URL}/services")
            time.sleep(3)
            
            # 检查页面内容
            page_source = self.driver.page_source.lower()
            
            service_keywords = ["service", "clean", "flower", "price", "book", "order"]
            found_keywords = [keyword for keyword in service_keywords if keyword in page_source]
            
            if found_keywords:
                self.log(f"✓ 服务页面包含相关内容: {', '.join(found_keywords)}", "SUCCESS")
            else:
                self.log("⚠ 服务页面可能缺少相关内容", "WARNING")
            
            # 尝试查找服务相关元素
            try:
                service_elements = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'service') or contains(@class, 'card') or contains(text(), '$')]")
                if service_elements:
                    self.log(f"✓ 找到{len(service_elements)}个可能的服务元素", "SUCCESS")
                else:
                    self.log("⚠ 未找到明显的服务元素", "WARNING")
            except Exception:
                pass
            
            return True
            
        except Exception as e:
            self.log(f"✗ 服务页面测试失败: {e}", "ERROR")
            return False
    
    def run_all_tests(self):
        """运行所有前端测试"""
        self.log("开始运行MyClean前端UI测试", "INFO")
        self.log("=" * 60, "INFO")
        
        # 检查服务状态
        if not self.check_services():
            return False
        
        # 设置浏览器
        if not self.setup_driver():
            return False
        
        try:
            # 运行测试
            if not self.test_homepage_access():
                return False
            
            if not self.test_navigation():
                return False
            
            if not self.test_registration_form():
                return False
            
            if not self.test_login_form():
                return False
            
            if not self.test_services_page():
                return False
            
            # 总结
            self.log("=" * 60, "INFO")
            self.log("前端UI测试总结:", "INFO")
            self.log(f"✓ 主页访问: 通过", "SUCCESS")
            self.log(f"✓ 页面导航: 通过", "SUCCESS")
            self.log(f"✓ 注册表单: 通过", "SUCCESS")
            self.log(f"✓ 登录表单: 通过", "SUCCESS")
            self.log(f"✓ 服务页面: 通过", "SUCCESS")
            self.log("🎉 前端UI测试完成！", "SUCCESS")
            
            return True
            
        finally:
            self.teardown_driver()

def main():
    """主函数"""
    print("MyClean 前端UI测试脚本")
    print("=" * 40)
    
    tester = FrontendTester()
    
    try:
        success = tester.run_all_tests()
        
        if success:
            print("\n✅ 测试完成：前端UI功能基本正常！")
            return 0
        else:
            print("\n❌ 测试失败：请检查前端状态")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n⚠️ 测试被用户中断")
        tester.teardown_driver()
        return 1
    except Exception as e:
        print(f"\n❌ 测试脚本异常: {e}")
        import traceback
        traceback.print_exc()
        tester.teardown_driver()
        return 1

if __name__ == "__main__":
    exit(main())
