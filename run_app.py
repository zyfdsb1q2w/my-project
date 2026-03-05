import os
import subprocess
import sys

def install_dependencies():
    """安装项目依赖"""
    print("正在安装项目依赖...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("依赖安装完成！")

def run_streamlit_app():
    """运行Streamlit应用"""
    print("正在启动美林公主的AI助手...")
    subprocess.run(["streamlit", "run", "app.pv", "--server.port", "8501", "--server.address", "0.0.0.0"])

if __name__ == "__main__":
    # 检查是否已安装依赖
    try:
        import streamlit
        import requests
        import dotenv
    except ImportError:
        install_dependencies()
    
    run_streamlit_app()