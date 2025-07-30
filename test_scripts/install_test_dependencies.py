#!/usr/bin/env python3
"""
Test Dependencies Installation Script
安装测试依赖脚本
Usage: C:\\Python312\\python.exe install_test_dependencies.py
"""

import subprocess
import sys
import os

def install_package(package):
    """Install Python package / 安装Python包"""
    try:
        print(f"Installing {package}...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", package],
                              capture_output=True, text=True, check=True)
        print(f"✓ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {package} installation failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main function / 主函数"""
    print("MyClean Test Dependencies Installation Script")
    print("=" * 40)

    # Packages to install / 需要安装的包
    packages = [
        "requests>=2.31.0",
        "selenium>=4.15.0",
        "webdriver-manager>=4.0.0"
    ]

    success_count = 0
    total_count = len(packages)

    for package in packages:
        if install_package(package):
            success_count += 1

    print("\n" + "=" * 40)
    print(f"Installation completed: {success_count}/{total_count} packages installed successfully")

    if success_count == total_count:
        print("✅ All dependencies installed successfully!")
        print("\nNow you can run test scripts:")
        print("C:\\Python312\\python.exe test_myclean_simple.py")
        print("or")
        print("C:\\Python312\\python.exe test_myclean_app.py")
    else:
        print("❌ Some dependencies failed to install, please check network connection or Python environment")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
