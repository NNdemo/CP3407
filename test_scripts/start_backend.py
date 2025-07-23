#!/usr/bin/env python3
"""
启动后端服务的脚本
"""

import subprocess
import sys
import os

def main():
    """启动后端服务"""
    print("启动MyClean后端服务...")
    
    # 切换到backend目录
    backend_dir = os.path.join(os.path.dirname(__file__), "..", "backend")
    os.chdir(backend_dir)
    
    # 启动服务
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n服务已停止")
    except Exception as e:
        print(f"启动失败: {e}")

if __name__ == "__main__":
    main()
