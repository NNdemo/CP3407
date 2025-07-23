#!/usr/bin/env python3
"""
MyClean 应用综合测试脚本
运行所有测试并生成详细报告

运行方式: C:\\Python312\\python.exe run_all_tests.py
"""

import subprocess
import sys
import time
import requests
from datetime import datetime

# 配置
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:5173"

class TestSuite:
    def __init__(self):
        self.results = {}
        self.start_time = None
        self.end_time = None
        
    def log(self, message, level="INFO"):
        """日志输出"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {
            "INFO": "\033[94m",     # 蓝色
            "SUCCESS": "\033[92m",  # 绿色
            "ERROR": "\033[91m",    # 红色
            "WARNING": "\033[93m",  # 黄色
            "HEADER": "\033[95m"    # 紫色
        }
        end_color = "\033[0m"
        color = colors.get(level, "")
        print(f"{color}[{timestamp}] {level}: {message}{end_color}")
    
    def print_header(self, text):
        """打印标题"""
        self.log("=" * 60, "HEADER")
        self.log(text.center(60), "HEADER")
        self.log("=" * 60, "HEADER")
    
    def check_services(self):
        """检查服务状态"""
        self.log("检查服务状态...", "INFO")
        
        services_status = {
            "backend": False,
            "frontend": False
        }
        
        # 检查后端
        try:
            response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
            if response.status_code == 200:
                services_status["backend"] = True
                self.log("✓ 后端服务运行正常", "SUCCESS")
            else:
                self.log(f"✗ 后端服务异常 (状态码: {response.status_code})", "ERROR")
        except Exception as e:
            self.log(f"✗ 无法连接到后端服务: {e}", "ERROR")
        
        # 检查前端
        try:
            response = requests.get(FRONTEND_URL, timeout=5)
            if response.status_code == 200:
                services_status["frontend"] = True
                self.log("✓ 前端服务运行正常", "SUCCESS")
            else:
                self.log(f"✗ 前端服务异常 (状态码: {response.status_code})", "ERROR")
        except Exception as e:
            self.log(f"✗ 无法连接到前端服务: {e}", "ERROR")
        
        return services_status
    
    def run_test_script(self, script_name, description):
        """运行测试脚本"""
        self.log(f"运行 {description}...", "INFO")
        
        try:
            result = subprocess.run(
                [sys.executable, script_name],
                capture_output=True,
                text=True,
                timeout=120  # 2分钟超时
            )
            
            success = result.returncode == 0
            self.results[script_name] = {
                "success": success,
                "description": description,
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
            
            if success:
                self.log(f"✓ {description} 通过", "SUCCESS")
            else:
                self.log(f"✗ {description} 失败 (返回码: {result.returncode})", "ERROR")
                if result.stderr:
                    self.log(f"错误信息: {result.stderr[:200]}...", "ERROR")
            
            return success
            
        except subprocess.TimeoutExpired:
            self.log(f"✗ {description} 超时", "ERROR")
            self.results[script_name] = {
                "success": False,
                "description": description,
                "output": "",
                "error": "测试超时",
                "return_code": -1
            }
            return False
        except Exception as e:
            self.log(f"✗ {description} 异常: {e}", "ERROR")
            self.results[script_name] = {
                "success": False,
                "description": description,
                "output": "",
                "error": str(e),
                "return_code": -1
            }
            return False
    
    def generate_report(self):
        """生成测试报告"""
        self.print_header("测试报告")
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results.values() if r["success"])
        failed_tests = total_tests - passed_tests
        
        # 基本统计
        self.log(f"测试开始时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}", "INFO")
        self.log(f"测试结束时间: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}", "INFO")
        duration = (self.end_time - self.start_time).total_seconds()
        self.log(f"测试总耗时: {duration:.1f} 秒", "INFO")
        self.log("", "INFO")
        
        self.log(f"总测试数: {total_tests}", "INFO")
        self.log(f"通过测试: {passed_tests}", "SUCCESS")
        self.log(f"失败测试: {failed_tests}", "ERROR" if failed_tests > 0 else "INFO")
        self.log("", "INFO")
        
        # 详细结果
        self.log("详细测试结果:", "INFO")
        for script, result in self.results.items():
            status = "✓ 通过" if result["success"] else "✗ 失败"
            level = "SUCCESS" if result["success"] else "ERROR"
            self.log(f"{status} - {result['description']} ({script})", level)
        
        # 总体结果
        self.log("", "INFO")
        if failed_tests == 0:
            self.log("🎉 所有测试通过！MyClean应用运行正常！", "SUCCESS")
            return True
        else:
            self.log(f"❌ {failed_tests} 个测试失败，请检查应用状态", "ERROR")
            return False
    
    def save_detailed_report(self):
        """保存详细报告到文件"""
        try:
            with open("test_report.txt", "w", encoding="utf-8") as f:
                f.write("MyClean 应用测试报告\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"测试时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')} - {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"测试耗时: {(self.end_time - self.start_time).total_seconds():.1f} 秒\n\n")
                
                for script, result in self.results.items():
                    f.write(f"\n{'='*30}\n")
                    f.write(f"测试脚本: {script}\n")
                    f.write(f"描述: {result['description']}\n")
                    f.write(f"结果: {'通过' if result['success'] else '失败'}\n")
                    f.write(f"返回码: {result['return_code']}\n")
                    
                    if result['output']:
                        f.write(f"\n输出:\n{result['output']}\n")
                    
                    if result['error']:
                        f.write(f"\n错误:\n{result['error']}\n")
            
            self.log("详细报告已保存到 test_report.txt", "INFO")
        except Exception as e:
            self.log(f"保存报告失败: {e}", "WARNING")
    
    def run_all_tests(self):
        """运行所有测试"""
        self.start_time = datetime.now()
        
        self.print_header("MyClean 应用综合测试")
        
        # 检查服务状态
        services = self.check_services()
        
        # 定义测试脚本
        tests = [
            ("test_backend_only.py", "后端API功能测试"),
        ]
        
        # 如果前端服务可用，添加前端测试
        if services["frontend"]:
            tests.append(("test_frontend_ui.py", "前端UI功能测试"))
        else:
            self.log("前端服务不可用，跳过前端UI测试", "WARNING")
        
        # 运行测试
        self.log("", "INFO")
        for script, description in tests:
            self.run_test_script(script, description)
            time.sleep(1)  # 测试间隔
        
        self.end_time = datetime.now()
        
        # 生成报告
        success = self.generate_report()
        self.save_detailed_report()
        
        return success

def main():
    """主函数"""
    print("MyClean 应用综合测试套件")
    print("=" * 40)
    print("此脚本将运行所有可用的测试")
    print("请确保后端和前端服务正在运行")
    print("")
    
    # 询问用户是否继续
    try:
        user_input = input("按 Enter 继续，或输入 'q' 退出: ").strip().lower()
        if user_input == 'q':
            print("测试已取消")
            return 0
    except KeyboardInterrupt:
        print("\n测试已取消")
        return 0
    
    # 运行测试
    test_suite = TestSuite()
    
    try:
        success = test_suite.run_all_tests()
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 测试被用户中断")
        return 1
    except Exception as e:
        print(f"\n❌ 测试套件异常: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
