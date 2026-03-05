#!/usr/bin/env python3
"""
美霖个人助手 - PWA手机应用启动脚本
专注于手机端PWA应用，删除所有exe相关功能
"""

import os
import sys
import subprocess
import webbrowser
import time
from datetime import datetime

def check_requirements():
    """检查必要的依赖"""
    print("检查依赖...")
    
    required_packages = ['streamlit', 'python-dotenv', 'requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ✗ {package}")
    
    if missing_packages:
        print(f"\n缺少依赖包: {', '.join(missing_packages)}")
        print("安装命令: pip install " + " ".join(missing_packages))
        return False
    
    return True

def check_pwa_files():
    """检查PWA所需文件"""
    print("\n检查PWA文件...")
    
    required_files = [
        'manifest.json',
        'service-worker.js',
        'app.py',
        'requirements.txt'
    ]
    
    required_dirs = ['icons']
    
    all_ok = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (缺失)")
            all_ok = False
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name) and os.path.isdir(dir_name):
            print(f"  ✓ {dir_name}/")
            # 检查图标文件
            icon_sizes = [72, 96, 128, 144, 152, 192, 384, 512]
            for size in icon_sizes:
                icon_file = f'{dir_name}/icon-{size}x{size}.png'
                if os.path.exists(icon_file):
                    print(f"    ✓ {icon_file}")
                else:
                    print(f"    ✗ {icon_file} (缺失)")
                    all_ok = False
        else:
            print(f"  ✗ {dir_name}/ (缺失)")
            all_ok = False
    
    return all_ok

def check_env_file():
    """检查环境配置文件"""
    print("\n检查配置文件...")
    
    if os.path.exists('.env'):
        print("  ✓ .env 文件存在")
        
        # 检查API密钥
        try:
            with open('.env', 'r', encoding='utf-8') as f:
                content = f.read()
                if 'DEEPSEEK_API_KEY' in content:
                    print("  ✓ DeepSeek API密钥已配置")
                else:
                    print("  ⚠ DeepSeek API密钥未配置")
                    print("    请编辑.env文件添加: DEEPSEEK_API_KEY=your_api_key")
        except:
            print("  ⚠ 无法读取.env文件")
    else:
        print("  ⚠ .env 文件不存在")
        print("    请创建.env文件并添加DeepSeek API密钥")
        print("    模板: DEEPSEEK_API_KEY=your_api_key_here")
    
    return True

def start_streamlit():
    """启动Streamlit应用"""
    print("\n" + "="*50)
    print("启动美霖个人助手 - PWA手机应用")
    print("="*50)
    
    # 获取当前目录的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, 'app.py')
    
    print(f"应用路径: {app_path}")
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n启动选项:")
    print("1. 自动打开浏览器")
    print("2. 显示网络URL（用于手机访问）")
    print("3. 显示二维码（如果可用）")
    print("\n按 Ctrl+C 停止应用")
    print("="*50)
    
    # 启动Streamlit
    cmd = [
        sys.executable, '-m', 'streamlit', 'run',
        'app.py',
        '--server.port', '8501',
        '--server.headless', 'false',
        '--server.enableCORS', 'true',
        '--server.enableXsrfProtection', 'true',
        '--browser.serverAddress', '0.0.0.0'
    ]
    
    try:
        # 启动Streamlit进程
        process = subprocess.Popen(cmd)
        
        # 等待Streamlit启动
        time.sleep(3)
        
        # 打开本地浏览器
        local_url = "http://localhost:8501"
        print(f"\n本地访问: {local_url}")
        print("正在打开浏览器...")
        webbrowser.open(local_url)
        
        print("\n手机访问指南:")
        print("1. 确保手机和电脑在同一WiFi网络")
        print("2. 查看上方输出的Network URL")
        print("3. 在手机浏览器中输入该URL")
        print("4. 点击'安装'按钮添加PWA应用到手机")
        
        print("\nPWA安装提示:")
        print("- Android Chrome: 点击地址栏右侧的安装图标")
        print("- iOS Safari: 点击分享按钮 → 添加到主屏幕")
        
        # 等待进程结束
        process.wait()
        
    except KeyboardInterrupt:
        print("\n\n应用已停止")
        if 'process' in locals():
            process.terminate()
    except Exception as e:
        print(f"\n启动失败: {str(e)}")
        return False
    
    return True

def main():
    """主函数"""
    print("="*50)
    print("美霖个人助手 - PWA手机应用")
    print("="*50)
    
    # 检查依赖
    if not check_requirements():
        print("\n请先安装缺失的依赖包")
        return
    
    # 检查PWA文件
    if not check_pwa_files():
        print("\nPWA文件不完整，请检查")
        return
    
    # 检查配置文件
    check_env_file()
    
    # 启动应用
    print("\n" + "="*50)
    input("按 Enter 键启动应用...")
    
    start_streamlit()

if __name__ == "__main__":
    main()