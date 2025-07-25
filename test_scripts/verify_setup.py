#!/usr/bin/env python3
"""
验证测试脚本设置是否正确
"""

import os
import sys

def check_file_exists(filepath, description):
    """检查文件是否存在"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (文件不存在)")
        return False

def main():
    """主函数"""
    print("MyClean 测试脚本设置验证")
    print("=" * 40)
    
    # 获取当前目录
    current_dir = os.path.dirname(__file__)
    print(f"当前目录: {current_dir}")
    print()
    
    # 检查测试脚本
    test_scripts = [
        ("test_backend_only.py", "后端API测试脚本"),
        ("test_myclean_simple.py", "简化版测试脚本"),
        ("test_frontend_ui.py", "前端UI测试脚本"),
        ("test_myclean_app.py", "完整测试脚本"),
        ("run_all_tests.py", "综合测试套件"),
    ]
    
    print("🔧 核心测试脚本:")
    script_count = 0
    for script, desc in test_scripts:
        if check_file_exists(os.path.join(current_dir, script), desc):
            script_count += 1
    
    # 检查辅助工具
    tools = [
        ("install_test_dependencies.py", "依赖安装脚本"),
        ("debug_backend.py", "后端调试工具"),
        ("fix_database.py", "数据库修复工具"),
        ("check_database.py", "数据库检查工具"),
        ("start_backend.py", "后端启动脚本"),
    ]
    
    print("\n🛠️ 辅助工具脚本:")
    tool_count = 0
    for tool, desc in tools:
        if check_file_exists(os.path.join(current_dir, tool), desc):
            tool_count += 1
    
    # 检查文档文件
    docs = [
        ("readme.md", "主要说明文档"),
        ("README_测试说明.md", "详细测试说明"),
        ("测试结果报告.md", "测试结果报告"),
        ("快速测试指南.md", "快速指南"),
    ]
    
    print("\n📚 文档文件:")
    doc_count = 0
    for doc, desc in docs:
        if check_file_exists(os.path.join(current_dir, doc), desc):
            doc_count += 1
    
    # 检查配置文件
    configs = [
        ("test_requirements.txt", "测试依赖配置"),
    ]
    
    print("\n📄 配置文件:")
    config_count = 0
    for config, desc in configs:
        if check_file_exists(os.path.join(current_dir, config), desc):
            config_count += 1
    
    # 检查后端目录和文件
    backend_dir = os.path.join(current_dir, "..", "backend")
    backend_files = [
        ("main.py", "后端主程序"),
        ("myclean.db", "数据库文件"),
        ("requirements.txt", "后端依赖"),
    ]
    
    print("\n🗄️ 后端文件:")
    backend_count = 0
    for file, desc in backend_files:
        if check_file_exists(os.path.join(backend_dir, file), desc):
            backend_count += 1
    
    # 总结
    print("\n" + "=" * 40)
    print("📊 设置验证总结:")
    print(f"✅ 核心测试脚本: {script_count}/{len(test_scripts)}")
    print(f"✅ 辅助工具脚本: {tool_count}/{len(tools)}")
    print(f"✅ 文档文件: {doc_count}/{len(docs)}")
    print(f"✅ 配置文件: {config_count}/{len(configs)}")
    print(f"✅ 后端文件: {backend_count}/{len(backend_files)}")
    
    total_files = len(test_scripts) + len(tools) + len(docs) + len(configs) + len(backend_files)
    found_files = script_count + tool_count + doc_count + config_count + backend_count
    
    print(f"\n总计: {found_files}/{total_files} 文件正常")
    
    if found_files == total_files:
        print("\n🎉 所有文件设置正确！可以开始测试。")
        print("\n推荐运行:")
        print("C:\\Python312\\python.exe test_backend_only.py")
        return True
    else:
        print(f"\n⚠️ 有 {total_files - found_files} 个文件缺失，请检查设置。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
