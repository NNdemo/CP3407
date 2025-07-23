#!/usr/bin/env python3
"""
安装测试依赖脚本
运行方式: C:\\Python312\\python.exe install_test_dependencies.py
"""

import subprocess
import sys
import os

def install_package(package):
    """安装Python包"""
    try:
        print(f"正在安装 {package}...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", package], 
                              capture_output=True, text=True, check=True)
        print(f"✓ {package} 安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {package} 安装失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def main():
    """主函数"""
    print("MyClean 测试依赖安装脚本")
    print("=" * 40)
    
    # 需要安装的包
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
    print(f"安装完成: {success_count}/{total_count} 个包安装成功")
    
    if success_count == total_count:
        print("✅ 所有依赖安装成功！")
        print("\n现在可以运行测试脚本:")
        print("C:\\Python312\\python.exe test_myclean_simple.py")
        print("或")
        print("C:\\Python312\\python.exe test_myclean_app.py")
    else:
        print("❌ 部分依赖安装失败，请检查网络连接或Python环境")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
