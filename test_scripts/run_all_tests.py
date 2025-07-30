#!/usr/bin/env python3
"""
MyClean Comprehensive Test Script
MyClean 应用综合测试脚本
Run all tests and generate detailed reports
运行所有测试并生成详细报告

Usage: C:\\Python312\\python.exe run_all_tests.py
"""

import subprocess
import sys
import time
import requests
from datetime import datetime

# Configuration / 配置
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:5173"

class TestSuite:
    def __init__(self):
        self.results = {}
        self.start_time = None
        self.end_time = None

    def log(self, message, level="INFO"):
        """Log output / 日志输出"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {
            "INFO": "\033[94m",     # Blue / 蓝色
            "SUCCESS": "\033[92m",  # Green / 绿色
            "ERROR": "\033[91m",    # Red / 红色
            "WARNING": "\033[93m",  # Yellow / 黄色
            "HEADER": "\033[95m"    # Purple / 紫色
        }
        end_color = "\033[0m"
        color = colors.get(level, "")
        print(f"{color}[{timestamp}] {level}: {message}{end_color}")

    def print_header(self, text):
        """Print header / 打印标题"""
        self.log("=" * 60, "HEADER")
        self.log(text.center(60), "HEADER")
        self.log("=" * 60, "HEADER")

    def check_services(self):
        """Check service status / 检查服务状态"""
        self.log("Checking service status...", "INFO")
        
        services_status = {
            "backend": False,
            "frontend": False
        }
        
        # Check backend / 检查后端
        try:
            response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
            if response.status_code == 200:
                services_status["backend"] = True
                self.log("✓ Backend service running normally", "SUCCESS")
            else:
                self.log(f"✗ Backend service error (status code: {response.status_code})", "ERROR")
        except Exception as e:
            self.log(f"✗ Cannot connect to backend service: {e}", "ERROR")

        # Check frontend / 检查前端
        try:
            response = requests.get(FRONTEND_URL, timeout=5)
            if response.status_code == 200:
                services_status["frontend"] = True
                self.log("✓ Frontend service running normally", "SUCCESS")
            else:
                self.log(f"✗ Frontend service error (status code: {response.status_code})", "ERROR")
        except Exception as e:
            self.log(f"✗ Cannot connect to frontend service: {e}", "ERROR")

        return services_status

    def run_test_script(self, script_name, description):
        """Run test script / 运行测试脚本"""
        self.log(f"Running {description}...", "INFO")
        
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
                self.log(f"✓ {description} passed", "SUCCESS")
            else:
                self.log(f"✗ {description} failed (return code: {result.returncode})", "ERROR")
                if result.stderr:
                    self.log(f"Error message: {result.stderr[:200]}...", "ERROR")

            return success

        except subprocess.TimeoutExpired:
            self.log(f"✗ {description} timeout", "ERROR")
            self.results[script_name] = {
                "success": False,
                "description": description,
                "output": "",
                "error": "Test timeout",
                "return_code": -1
            }
            return False
        except Exception as e:
            self.log(f"✗ {description} exception: {e}", "ERROR")
            self.results[script_name] = {
                "success": False,
                "description": description,
                "output": "",
                "error": str(e),
                "return_code": -1
            }
            return False

    def generate_report(self):
        """Generate test report / 生成测试报告"""
        self.print_header("Test Report")
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results.values() if r["success"])
        failed_tests = total_tests - passed_tests
        
        # Basic statistics / 基本统计
        self.log(f"Test start time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}", "INFO")
        self.log(f"Test end time: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}", "INFO")
        duration = (self.end_time - self.start_time).total_seconds()
        self.log(f"Total test duration: {duration:.1f} seconds", "INFO")
        self.log("", "INFO")

        self.log(f"Total tests: {total_tests}", "INFO")
        self.log(f"Passed tests: {passed_tests}", "SUCCESS")
        self.log(f"Failed tests: {failed_tests}", "ERROR" if failed_tests > 0 else "INFO")
        self.log("", "INFO")
        
        # Detailed results / 详细结果
        self.log("Detailed test results:", "INFO")
        for script, result in self.results.items():
            status = "✓ Passed" if result["success"] else "✗ Failed"
            level = "SUCCESS" if result["success"] else "ERROR"
            self.log(f"{status} - {result['description']} ({script})", level)

        # Overall results / 总体结果
        self.log("", "INFO")
        if failed_tests == 0:
            self.log(" All tests passed! MyClean application running normally!", "SUCCESS")
            return True
        else:
            self.log(f" {failed_tests} tests failed, please check application status", "ERROR")
            return False

    def save_detailed_report(self):
        """Save detailed report to file / 保存详细报告到文件"""
        try:
            with open("test_report.txt", "w", encoding="utf-8") as f:
                f.write("MyClean Application Test Report\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Test time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')} - {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Test duration: {(self.end_time - self.start_time).total_seconds():.1f} seconds\n\n")

                for script, result in self.results.items():
                    f.write(f"\n{'='*30}\n")
                    f.write(f"Test script: {script}\n")
                    f.write(f"Description: {result['description']}\n")
                    f.write(f"Result: {'Passed' if result['success'] else 'Failed'}\n")
                    f.write(f"Return code: {result['return_code']}\n")

                    if result['output']:
                        f.write(f"\nOutput:\n{result['output']}\n")

                    if result['error']:
                        f.write(f"\nError:\n{result['error']}\n")

            self.log("Detailed report saved to test_report.txt", "INFO")
        except Exception as e:
            self.log(f"Failed to save report: {e}", "WARNING")
    
    def run_all_tests(self):
        """Run all tests / 运行所有测试"""
        self.start_time = datetime.now()

        self.print_header("MyClean Comprehensive Test")

        # Check service status / 检查服务状态
        services = self.check_services()

        # Define test scripts / 定义测试脚本
        tests = [
            ("test_backend_only.py", "Backend API Function Test"),
        ]

        # Add frontend test if frontend service is available / 如果前端服务可用，添加前端测试
        if services["frontend"]:
            tests.append(("test_frontend_ui.py", "Frontend UI Function Test"))
        else:
            self.log("Frontend service unavailable, skipping frontend UI test", "WARNING")

        # Run tests / 运行测试
        self.log("", "INFO")
        for script, description in tests:
            self.run_test_script(script, description)
            time.sleep(1)  # Test interval / 测试间隔

        self.end_time = datetime.now()

        # Generate report / 生成报告
        success = self.generate_report()
        self.save_detailed_report()

        return success

def main():
    """Main function / 主函数"""
    print("MyClean Comprehensive Test Suite")
    print("=" * 40)
    print("This script will run all available tests")
    print("Please ensure backend and frontend services are running")
    print("")

    # Ask user to continue / 询问用户是否继续
    try:
        user_input = input("Press Enter to continue, or type 'q' to exit: ").strip().lower()
        if user_input == 'q':
            print("Test cancelled")
            return 0
    except KeyboardInterrupt:
        print("\nTest cancelled")
        return 0

    # Run tests / 运行测试
    test_suite = TestSuite()

    try:
        success = test_suite.run_all_tests()
        return 0 if success else 1

    except KeyboardInterrupt:
        print("\n\n Test interrupted by user")
        return 1
    except Exception as e:
        print(f"\n Test suite exception: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
