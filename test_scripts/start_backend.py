#!/usr/bin/env python3
"""
Backend Service Startup Script
启动后端服务的脚本
"""

import subprocess
import sys
import os

def main():
    """Start backend service / 启动后端服务"""
    print("Starting MyClean backend service...")

    # Switch to backend directory / 切换到backend目录
    backend_dir = os.path.join(os.path.dirname(__file__), "..", "backend")
    os.chdir(backend_dir)

    # Start service / 启动服务
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\nService stopped")
    except Exception as e:
        print(f"Startup failed: {e}")

if __name__ == "__main__":
    main()
