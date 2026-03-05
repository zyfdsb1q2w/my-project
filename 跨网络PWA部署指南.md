# 跨网络PWA部署指南

当手机和电脑不在同一WiFi网络时，有以下几种解决方案可以将美霖个人助手安装到手机上。

## 📡 解决方案概览

### 方案1：使用公网IP或域名（推荐）
### 方案2：使用内网穿透工具
### 方案3：使用云服务器部署
### 方案4：使用静态文件托管
### 方案5：使用移动热点

## 🔧 方案1：使用公网IP或域名

### 前提条件
- 路由器支持端口转发
- 有公网IP地址（或动态域名）

### 步骤
1. **获取公网IP**
   ```bash
   # 在电脑上查看公网IP
   curl ifconfig.me
   # 或访问：https://whatismyipaddress.com/
   ```

2. **路由器端口转发**
   - 登录路由器管理界面（通常192.168.1.1）
   - 找到"端口转发"或"虚拟服务器"
   - 添加规则：
     - 外部端口：8501
     - 内部IP：你的电脑IP（如192.168.12.47）
     - 内部端口：8501
     - 协议：TCP

3. **启动应用**
   ```bash
   python start_pwa.py
   ```

4. **手机访问**
   - 在手机浏览器输入：`http://你的公网IP:8501`
   - 按照PWA安装步骤操作

### 优点
- 永久可用
- 任何网络都能访问

### 缺点
- 需要公网IP
- 需要配置路由器

## 🔧 方案2：使用内网穿透工具

### 推荐工具
1. **ngrok**（最简单）
2. **frp**（免费开源）
3. **花生壳**（国内稳定）

### 使用ngrok步骤
1. **注册ngrok账号**
   - 访问：https://ngrok.com/
   - 注册并获取authtoken

2. **下载ngrok**
   ```bash
   # Windows下载
   # 访问：https://ngrok.com/download
   ```

3. **配置ngrok**
   ```bash
   # 解压后运行
   ngrok authtoken 你的token
   ```

4. **启动内网穿透**
   ```bash
   # 启动Streamlit应用
   python start_pwa.py
   
   # 在另一个终端启动ngrok
   ngrok http 8501
   ```

5. **获取公网地址**
   - ngrok会显示类似：`https://xxxx.ngrok.io`
   - 在手机浏览器访问这个地址

### 使用frp步骤
1. **下载frp**
   ```bash
   # 从GitHub下载：https://github.com/fatedier/frp
   ```

2. **配置服务器端（需要一台云服务器）**
   ```ini
   # frps.ini
   [common]
   bind_port = 7000
   ```

3. **配置客户端**
   ```ini
   # frpc.ini
   [common]
   server_addr = 你的服务器IP
   server_port = 7000
   
   [web]
   type = tcp
   local_ip = 127.0.0.1
   local_port = 8501
   remote_port = 8501
   ```

4. **启动**
   ```bash
   # 服务器
   ./frps -c frps.ini
   
   # 客户端
   ./frpc -c frpc.ini
   ```

## 🔧 方案3：使用云服务器部署

### 推荐平台
1. **Vercel**（免费，简单）
2. **Railway**（免费额度）
3. **Heroku**（免费）
4. **阿里云/腾讯云**（国内）

### 使用Vercel部署步骤
1. **创建GitHub仓库**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/你的用户名/美霖助手.git
   git push -u origin main
   ```

2. **部署到Vercel**
   - 访问：https://vercel.com/
   - 导入GitHub仓库
   - 配置环境变量（DEEPSEEK_API_KEY）
   - 自动部署

3. **访问应用**
   - Vercel会提供域名：`https://美霖助手.vercel.app`
   - 手机访问该域名安装PWA

### 创建部署配置文件
创建`vercel.json`：
```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

## 🔧 方案4：使用静态文件托管

### 将应用转换为静态网站
1. **安装Streamlit静态导出工具**
   ```bash
   pip install streamlit-static-export
   ```

2. **导出静态文件**
   ```bash
   streamlit export app.py
   ```

3. **托管静态文件**
   - GitHub Pages
   - Netlify
   - Cloudflare Pages

4. **配置PWA**
   - 确保manifest.json和service-worker.js正确引用
   - 图标文件路径正确

## 🔧 方案5：使用移动热点

### 最简单的方法
1. **电脑开启移动热点**
   - Windows：设置 → 网络和Internet → 移动热点
   - 设置热点名称和密码

2. **手机连接热点**
   - 在手机WiFi设置中连接电脑热点

3. **启动应用**
   ```bash
   python start_pwa.py
   ```

4. **获取电脑在热点网络中的IP**
   ```bash
   ipconfig
   # 查看"无线局域网适配器 WLAN"的IPv4地址
   ```

5. **手机访问**
   - 在手机浏览器输入：`http://热点IP:8501`

## 📱 PWA安装步骤（通用）

无论使用哪种方案，PWA安装步骤相同：

### Android Chrome
1. 访问应用URL
2. 地址栏右侧出现"安装"图标 ⬇️
3. 点击安装
4. 确认添加到主屏幕

### iOS Safari
1. 访问应用URL
2. 点击底部分享按钮 📤
3. 滑动找到"添加到主屏幕"
4. 点击添加，确认名称

## 🔧 快速测试方案

### 使用临时公网服务
1. **使用localhost.run**
   ```bash
   # 安装
   pip install localhost-run
   
   # 启动
   localhost-run --port 8501
   ```

2. **使用serveo.net**
   ```bash
   ssh -R 80:localhost:8501 serveo.net
   ```

3. **使用LocalXpose**
   ```bash
   # 下载：https://localxpose.io/
   ./loclx tunnel http --to localhost:8501
   ```

## 📊 方案对比

| 方案 | 难度 | 成本 | 稳定性 | 推荐度 |
|------|------|------|--------|--------|
| 移动热点 | ⭐ | 免费 | 临时 | ⭐⭐⭐⭐ |
| 内网穿透 | ⭐⭐ | 免费/付费 | 中等 | ⭐⭐⭐⭐ |
| 云服务器 | ⭐⭐⭐ | 免费/付费 | 高 | ⭐⭐⭐⭐⭐ |
| 公网IP | ⭐⭐⭐⭐ | 免费 | 高 | ⭐⭐⭐ |
| 静态托管 | ⭐⭐ | 免费 | 高 | ⭐⭐⭐ |

## 🚀 推荐方案

### 临时使用：移动热点
- 最简单快速
- 无需配置

### 长期使用：云服务器部署
- 永久可用
- 专业稳定
- 支持自动更新

### 开发测试：内网穿透
- 方便调试
- 支持HTTPS

## 📝 实施步骤

### 第一步：选择方案
根据你的需求选择合适方案

### 第二步：配置环境
按照对应方案的步骤配置

### 第三步：测试访问
在手机上测试能否访问

### 第四步：安装PWA
按照PWA安装步骤安装到手机

### 第五步：验证功能
测试应用各项功能是否正常

## 🔍 故障排除

### 无法访问
1. 检查防火墙设置
2. 确认端口是否正确
3. 验证网络连接

### PWA无法安装
1. 确保manifest.json配置正确
2. 使用HTTPS（某些浏览器要求）
3. 清除浏览器缓存

### 应用功能异常
1. 检查API密钥配置
2. 验证网络连接
3. 查看控制台错误信息

## 📞 技术支持

### 获取帮助
1. 查看错误日志
2. 搜索相关文档
3. 联系技术支持

### 社区资源
- GitHub Issues
- Stack Overflow
- 相关技术论坛

---

**总结：** 即使手机和电脑不在同一WiFi，也有多种方法可以将美霖个人助手安装到手机上。推荐从最简单的移动热点开始，如果需要长期使用，考虑云服务器部署。