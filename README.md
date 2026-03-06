# 美霖个人助手 - Streamlit应用

一个基于DeepSeek API的个人AI助手，专为手机端优化的Streamlit应用，支持PWA安装和Streamlit社区云部署。

## ✨ 功能特点

### 🤖 AI智能助手
- 集成DeepSeek API，提供智能对话
- 支持自定义AI行为规则
- 实时聊天，自然语言交互
- **美林公主专属回复**：询问美林公主相关话题触发特别回复

### 💖 生活记录
- **每日土味情话**：20+精选情话，每天随机显示，支持AI生成
- **目标记录**：设定、追踪、完成个人目标
- **心情记录**：记录每日心情，查看历史记录
- **记事本功能**：记录每日备忘和想法
- **个性化建议**：获取生活、学习、心情调节建议

### 📱 移动端优化
- **PWA支持**：可安装到手机主屏幕，类似原生应用
- **响应式设计**：自动适配手机屏幕
- **触摸优化**：大按钮、大字体，便于手机操作
- **侧边栏优化**：移动端友好侧边栏设计

### ⚙️ 数据安全
- **会话存储**：所有数据保存在浏览器Session Storage
- **隐私保护**：不会上传任何数据到服务器
- **本地处理**：AI对话通过API处理，其他功能完全本地

## 🚀 快速开始（本地运行）

### 环境要求
- Python 3.8+
- 稳定的网络连接
- DeepSeek API密钥

### 安装步骤

1. **克隆或下载项目**
   ```bash
   git clone https://github.com/zyfdsb1q2w/my-project.git
   cd MyPersonalAI
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置API密钥**
   - 创建 `.env` 文件，添加以下内容：
     ```
     DEEPSEEK_API_KEY=your_api_key_here
     ```
   - 或者使用Streamlit Secrets（推荐用于部署）

4. **启动应用**
   ```bash
   streamlit run app.py
   ```

5. **访问应用**
   - 本地访问：http://localhost:8501
   - 手机访问：http://电脑IP:8501（需同一WiFi）

## ☁️ Streamlit社区云部署

### 部署优势
- **完全免费**：无需付费
- **一键部署**：直接从GitHub部署
- **自动更新**：每次推送到GitHub自动重新部署
- **全球CDN**：快速访问
- **内置监控**：查看应用使用情况

### 部署步骤

#### 步骤1：GitHub准备
1. 确保所有代码已提交到GitHub仓库
2. 检查 `.gitignore` 文件是否包含敏感文件

#### 步骤2：Streamlit社区云部署
1. 访问 [Streamlit Community Cloud](https://share.streamlit.io/)
2. 使用GitHub账号登录
3. 点击"New app"
4. 选择你的仓库和分支（main）
5. 选择主文件路径（app.py）
6. 点击"Deploy"

#### 步骤3：配置API密钥（重要！）
1. 在Streamlit云中，进入你的应用
2. 点击"Settings"（设置）
3. 点击"Secrets"（密钥）
4. 添加以下键值对：
   ```toml
   DEEPSEEK_API_KEY = "your_actual_deepseek_api_key"
   ```
5. 点击"Save"（保存）

#### 步骤4：访问部署的应用
- 部署完成后，你会获得一个URL，如：`https://your-app-name.streamlit.app`
- 分享这个URL给其他人使用

## 📱 PWA安装指南

### Android Chrome
1. 访问应用页面（本地或Streamlit云）
2. 地址栏右侧出现"安装"图标 ⬇️
3. 点击安装
4. 确认添加到主屏幕

### iOS Safari
1. 访问应用页面
2. 点击底部分享按钮 📤
3. 滑动找到"添加到主屏幕"
4. 点击添加，确认名称

## 🎨 美林公主专属功能
### 触发关键词
- 美林、美林公主、美霖、美霖公主
- meilin、公主、princess
- 王雨、最喜欢、特别、珍贵
### 专属回复
当询问美林公主相关话题时，AI会：
1. 用温柔真诚的语气描述美林公主的美好品质
2. 表达王雨对她的珍视和喜爱
3. 随机返回完整回复或简短情话

## 📁 项目结构

```
MyPersonalAI/
├── app.py              # Streamlit主应用文件
├── requirements.txt    # Python依赖包
├── .streamlit/         # Streamlit配置目录
│   └── secrets.toml   # Streamlit Secrets模板
├── .env.example       # 环境变量模板
├── README.md          # 项目说明
├── .gitignore         # Git忽略文件
├── icons/             # PWA应用图标
│   ├── icon-72x72.png
│   ├── icon-96x96.png
│   ├── icon-128x128.png
│   ├── icon-144x144.png
│   ├── icon-152x152.png
│   ├── icon-192x192.png
│   ├── icon-384x384.png
│   └── icon-512x512.png
└── 其他辅助文件/
    ├── start_pwa.py
    ├── demo_pwa_install.py
    ├── generate_icons.py
    ├── run_app.py
    └── 使用指南文档
```

## 🔧 技术架构

### 前端
- **Streamlit**：Web应用框架
- **PWA技术**：渐进式Web应用
- **响应式CSS**：移动端适配
- **Service Worker**：离线支持（通过Streamlit静态文件服务）

### 后端
- **Python**：后端逻辑
- **DeepSeek API**：AI能力
- **Streamlit Session State**：会话状态管理

### 部署
- **Streamlit Community Cloud**：主部署平台
- **GitHub Integration**：自动部署
- **环境变量管理**：Streamlit Secrets

## 🔄 更新与维护

### 本地开发
1. 修改代码
2. 测试本地运行
3. 提交到GitHub
4. Streamlit云自动重新部署

### 数据备份
- 应用数据存储在浏览器会话中
- 刷新页面会重置数据（设计如此）
- 重要数据建议手动记录

## ❓ 常见问题

### Q1: AI聊天无法使用
- 检查Streamlit Secrets中是否配置了API密钥
- 确认API密钥有效且未过期
- 检查网络连接

### Q2: PWA无法安装
- 确保使用HTTPS访问（Streamlit云自动提供）
- 清除浏览器缓存后重试
- 检查设备是否支持PWA

### Q3: 应用加载缓慢
- Streamlit云首次加载可能需要一些时间
- 后续访问会缓存资源，加载更快
- 确保网络连接稳定

### Q4: 如何更新应用
1. 修改本地代码
2. 提交到GitHub
3. Streamlit云会自动检测并重新部署
4. 等待几分钟后刷新页面

## ⚡ 使用技巧

### 移动端优化
- 点击左上角菜单图标展开侧边栏
- 所有按钮都经过触摸优化
- 输入框自动放大，便于输入

### 功能快速访问
1. **每日情话**：主界面最上方
2. **目标记录**：主界面中部
3. **心情记录**：侧边栏中
4. **AI聊天**：主界面最下方
5. **规则设置**：侧边栏顶部

### 美林公主测试
- 输入："美林公主怎么样？"
- 输入："王雨最喜欢谁？"
- 输入："说说美林公主"

## 🎯 成功标志

1. ✅ 应用正常显示，界面美观
2. ✅ 每日情话随机显示
3. ✅ 可以添加/删除规则
4. ✅ 可以记录和管理目标
5. ✅ 可以记录和查看心情
6. ✅ AI聊天功能正常（需API密钥）
7. ✅ PWA可以安装到手机主屏幕
8. ✅ 美林公主专属回复正常触发
9. ✅ Streamlit云部署成功

## 📞 技术支持

### 问题反馈
1. 查看浏览器控制台（F12）
2. 检查Streamlit云日志
3. 确认API密钥配置正确

### 故障排除
- **重启应用**：关闭后重新打开
- **清除缓存**：浏览器设置中清除网站数据
- **重新部署**：在Streamlit云中重新部署

## 🎉 开始使用

现在你可以：
1. **本地测试**：`streamlit run app.py`
2. **部署到云**：通过Streamlit社区云一键部署
3. **安装到手机**：享受随时随地的个人助手
4. **个性化定制**：添加自己的规则和目标

## 📄 许可证

本项目仅供个人学习使用，请遵守DeepSeek API的使用条款。

---

**祝您使用愉快！🤖💕**

*美霖个人助手 v3.0 - Streamlit社区云部署版*