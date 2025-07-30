#!/usr/bin/env python3
"""
Test Script Setup Verification
验证测试脚本设置是否正确
"""

import os
import sys

def check_file_exists(filepath, description):
    """Check if file exists / 检查文件是否存在"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (File not found)")
        return False

def main():
    """Main function / 主函数"""
    print("MyClean Test Script Setup Verification")
    print("=" * 40)

    # Get current directory / 获取当前目录
    current_dir = os.path.dirname(__file__)
    print(f"Current directory: {current_dir}")
    print()

    # Check test scripts / 检查测试脚本
    test_scripts = [
        ("test_backend_only.py", "Backend API Test Script"),
        ("test_myclean_simple.py", "Simple Test Script"),
        ("test_frontend_ui.py", "Frontend UI Test Script"),
        ("test_myclean_app.py", "Complete Test Script"),
        ("run_all_tests.py", "Comprehensive Test Suite"),
    ]

    print("🔧 Core Test Scripts:")
    script_count = 0
    for script, desc in test_scripts:
        if check_file_exists(os.path.join(current_dir, script), desc):
            script_count += 1

    # Check auxiliary tools / 检查辅助工具
    tools = [
        ("install_test_dependencies.py", "Dependency Installation Script"),
        ("debug_backend.py", "Backend Debug Tool"),
        ("fix_database.py", "Database Repair Tool"),
        ("check_database.py", "Database Check Tool"),
        ("start_backend.py", "Backend Startup Script"),
    ]
    
    print("\n🛠️ Auxiliary Tool Scripts:")
    tool_count = 0
    for tool, desc in tools:
        if check_file_exists(os.path.join(current_dir, tool), desc):
            tool_count += 1

    # Check documentation files / 检查文档文件
    docs = [
        ("readme.md", "Main Documentation"),
        ("README_测试说明.md", "Detailed Test Instructions"),
        ("测试结果报告.md", "Test Result Report"),
        ("快速测试指南.md", "Quick Test Guide"),
    ]

    print("\n📚 Documentation Files:")
    doc_count = 0
    for doc, desc in docs:
        if check_file_exists(os.path.join(current_dir, doc), desc):
            doc_count += 1

    # Check configuration files / 检查配置文件
    configs = [
        ("test_requirements.txt", "Test Dependencies Configuration"),
    ]

    print("\n📄 Configuration Files:")
    config_count = 0
    for config, desc in configs:
        if check_file_exists(os.path.join(current_dir, config), desc):
            config_count += 1

    # Check backend directory and files / 检查后端目录和文件
    backend_dir = os.path.join(current_dir, "..", "backend")
    backend_files = [
        ("main.py", "Backend Main Program"),
        ("myclean.db", "Database File"),
        ("requirements.txt", "Backend Dependencies"),
    ]

    print("\n🗄️ Backend Files:")
    backend_count = 0
    for file, desc in backend_files:
        if check_file_exists(os.path.join(backend_dir, file), desc):
            backend_count += 1

    # Summary / 总结
    print("\n" + "=" * 40)
    print("📊 Setup Verification Summary:")
    print(f"✅ Core test scripts: {script_count}/{len(test_scripts)}")
    print(f"✅ Auxiliary tool scripts: {tool_count}/{len(tools)}")
    print(f"✅ Documentation files: {doc_count}/{len(docs)}")
    print(f"✅ Configuration files: {config_count}/{len(configs)}")
    print(f"✅ Backend files: {backend_count}/{len(backend_files)}")

    total_files = len(test_scripts) + len(tools) + len(docs) + len(configs) + len(backend_files)
    found_files = script_count + tool_count + doc_count + config_count + backend_count

    print(f"\nTotal: {found_files}/{total_files} files normal")

    if found_files == total_files:
        print("\n🎉 All files configured correctly! Ready to start testing.")
        print("\nRecommended to run:")
        print("C:\\Python312\\python.exe test_backend_only.py")
        return True
    else:
        print(f"\n⚠️ {total_files - found_files} files missing, please check setup.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
