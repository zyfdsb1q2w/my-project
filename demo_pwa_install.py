#!/usr/bin/env python3
"""
PWA安装演示脚本
展示如何将美霖个人助手安装到手机
"""

import os
import sys
import subprocess
import webbrowser
import time
import socket

def get_local_ip():
    """获取本地IP地址"""
    try:
        # 创建一个socket连接到外部服务器（但不发送数据）
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "192.168.x.x"

def print_pwa_info():
    """打印PWA相关信息"""
    print("=" * 60)
    print("美霖个人助手 - PWA手机安装演示")
    print("=" * 60)
    
    local_ip = get_local_ip()
    
    print("\n📱 PWA安装原理：")
    print("PWA（渐进式Web应用）是现代浏览器的标准功能，允许将网站")
    print("安装到手机主屏幕，获得类似原生应用的体验。")
    
    print("\n✅ 技术可行性：")
    print("1. ✅ Android Chrome：完全支持PWA安装")
    print("2. ✅ iOS Safari（iOS 11.3+）：支持添加到主屏幕")
    print("3. ✅ 所有现代浏览器：Edge、Firefox等")
    
    print("\n🔧 我们的实现：")
    print("1. ✅ manifest.json：定义应用名称、图标、主题色")
    print("2. ✅ service-worker.js：提供离线功能和缓存")
    print("3. ✅ 多种尺寸图标：适配不同设备")
    print("4. ✅ PWA meta标签：告诉浏览器这是可安装应用")
    
    print("\n📲 安装步骤演示：")
    print(f"1. 在电脑上启动应用（端口8501）")
    print(f"2. 手机访问：http://{local_ip}:8501")
    print("3. 浏览器会自动检测到PWA并显示安装提示")
    
    print("\n📱 具体安装方法：")
    print("【Android Chrome】")
    print("  1. 打开Chrome浏览器访问应用")
    print("  2. 地址栏右侧会出现'安装'图标 ⬇️")
    print("  3. 点击安装，确认添加到主屏幕")
    print("  4. 应用图标出现在手机桌面")
    
    print("\n【iOS Safari】")
    print("  1. 打开Safari浏览器访问应用")
    print("  2. 点击底部分享按钮 📤")
    print("  3. 滑动找到'添加到主屏幕'")
    print("  4. 点击添加，确认名称")
    print("  5. 应用图标出现在手机桌面")
    
    print("\n🎯 安装后的体验：")
    print("1. 📱 类似原生应用的图标和启动画面")
    print("2. 🚀 快速启动，无需打开浏览器")
    print("3. 📶 支持部分离线功能")
    print("4. 🔄 自动更新，无需手动下载")
    
    print("\n🔍 验证PWA配置：")
    print("1. 打开Chrome开发者工具（F12）")
    print("2. 切换到'Application'标签")
    print("3. 查看'Manifest'和'Service Workers'")
    print("4. 应该能看到我们的PWA配置")
    
    return local_ip

def start_demo_server(local_ip):
    """启动演示服务器"""
    print("\n" + "=" * 60)
    print("启动演示服务器...")
    print("=" * 60)
    
    # 启动Streamlit
    cmd = [
        sys.executable, '-m', 'streamlit', 'run',
        'app.py',
        '--server.port', '8501',
        '--server.headless', 'false',
        '--server.enableCORS', 'true',
        '--server.enableXsrfProtection', 'true'
    ]
    
    try:
        # 启动进程
        process = subprocess.Popen(cmd)
        
        # 等待启动
        time.sleep(3)
        
        print(f"\n✅ 服务器已启动！")
        print(f"   本地访问：http://localhost:8501")
        print(f"   手机访问：http://{local_ip}:8501")
        
        print("\n📱 现在可以在手机上：")
        print("1. 确保手机和电脑在同一WiFi网络")
        print(f"2. 在手机浏览器中输入：http://{local_ip}:8501")
        print("3. 按照上面的安装步骤操作")
        
        print("\n🔍 验证PWA功能：")
        print("1. 页面加载后，查看地址栏是否有安装图标")
        print("2. 或点击浏览器菜单查看'安装'选项")
        
        print("\n⏳ 服务器运行中...")
        print("按 Ctrl+C 停止演示")
        
        # 打开本地浏览器
        webbrowser.open("http://localhost:8501")
        
        # 保持运行
        process.wait()
        
    except KeyboardInterrupt:
        print("\n\n演示结束")
        if 'process' in locals():
            process.terminate()
    except Exception as e:
        print(f"\n启动失败：{str(e)}")

def main():
    """主函数"""
    # 打印PWA信息
    local_ip = print_pwa_info()
    
    # 确认启动
    print("\n" + "=" * 60)
    input("按 Enter 键启动演示服务器...")
    
    # 启动服务器
    start_demo_server(local_ip)

if __name__ == "__main__":
    main()