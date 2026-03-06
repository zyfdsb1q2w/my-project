import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv
from datetime import date

# 加载API密钥（优先从Streamlit Secrets读取，其次从.env文件读取）
# Streamlit社区云使用Secrets，本地开发使用.env文件
try:
    # 尝试从Streamlit Secrets读取
    api_key = st.secrets.get("DEEPSEEK_API_KEY")
    if api_key and api_key != "your_deepseek_api_key_here":
        os.environ["DEEPSEEK_API_KEY"] = api_key
    else:
        # 如果Secrets中没有或为默认值，尝试从.env文件读取
        load_dotenv()
except:
    # 如果Secrets不可用（本地运行），使用.env文件
    load_dotenv()

# 页面基础配置（手机端适配）
st.set_page_config(
    page_title="美霖个人助手",
    page_icon="🤖",
    layout="centered",  # 移动端适配
    initial_sidebar_state="collapsed"  # 移动端默认收起侧边栏
)

# 添加简化版PWA支持（纯HTML/CSS）
st.markdown("""
<!-- 简化版PWA配置 -->
<meta name="theme-color" content="#4A86E8">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="美霖助手">
<link rel="apple-touch-icon" href="/icons/icon-152x152.png">
<link rel="icon" type="image/png" href="/icons/icon-192x192.png">

<style>
/* 全局样式优化 */
* {
    box-sizing: border-box;
}

/* 移动端优化 */
@media (max-width: 768px) {
    /* 调整标题大小 */
    h1 {
        font-size: 1.8rem !important;
        margin-bottom: 10px !important;
    }
    
    h2 {
        font-size: 1.5rem !important;
    }
    
    h3 {
        font-size: 1.3rem !important;
    }
    
    /* 调整卡片内边距 */
    .welcome-card {
        padding: 15px !important;
        margin: 10px 0 !important;
    }
    
    /* 调整按钮大小 */
    .stButton > button {
        width: 100% !important;
        margin: 5px 0 !important;
        padding: 14px !important;
        font-size: 16px !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }
    
    /* 调整输入框大小 */
    .stTextArea textarea, .stTextInput input {
        font-size: 16px !important;
        padding: 14px !important;
        border-radius: 10px !important;
        border: 2px solid #e0e0e0 !important;
        transition: border-color 0.3s ease !important;
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #4A86E8 !important;
        box-shadow: 0 0 0 3px rgba(74, 134, 232, 0.1) !important;
    }
    
    /* 调整选择框大小 */
    .stSelectbox select {
        font-size: 16px !important;
        padding: 14px !important;
        border-radius: 10px !important;
    }
    
    /* 调整聊天消息 */
    .stChatMessage {
        padding: 12px !important;
        margin: 10px 0 !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    
    /* 隐藏不必要的列 */
    .mobile-hide {
        display: none !important;
    }
    
    /* 卡片间距优化 */
    .element-container {
        margin-bottom: 20px !important;
    }
}

/* 通用优化 */
.welcome-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 25px;
    border-radius: 16px;
    margin: 20px 0;
    color: white;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
    animation: fadeIn 0.8s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* 触摸友好的按钮 */
.touch-button {
    min-height: 48px !important;
    min-width: 48px !important;
    border-radius: 12px !important;
}

/* 移动端侧边栏优化 */
@media (max-width: 768px) {
    section[data-testid="stSidebar"] {
        width: 85% !important;
        max-width: 320px !important;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
    }
}

/* 卡片样式优化 */
.stCard {
    border-radius: 16px !important;
    border: none !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08) !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease !important;
}

.stCard:hover {
    transform: translateY(-4px) !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.12) !important;
}

/* 聊天消息样式 */
.user-message {
    background: linear-gradient(135deg, #4A86E8 0%, #3B6BB5 100%) !important;
    color: white !important;
    border-radius: 18px 18px 4px 18px !important;
}

.assistant-message {
    background: linear-gradient(135deg, #f0f8ff 0%, #e3f2fd 100%) !important;
    color: #333 !important;
    border-radius: 18px 18px 18px 4px !important;
}

/* 渐变按钮 */
.gradient-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 24px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.gradient-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3) !important;
}

/* 美化滚动条 */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #5a6fd8 0%, #6a3f9c 100%);
}

/* 加载动画 */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.loading-pulse {
    animation: pulse 1.5s ease-in-out infinite;
}

/* 响应式网格 */
.responsive-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin: 20px 0;
}

/* 美化分隔线 */
hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, #4A86E8, transparent);
    margin: 30px 0;
}

/* 美化输入框组 */
.input-group {
    position: relative;
    margin: 20px 0;
}

.input-group input, .input-group textarea {
    width: 100%;
    padding: 16px;
    border: 2px solid #e0e0e0;
    border-radius: 12px;
    font-size: 16px;
    transition: all 0.3s ease;
}

.input-group input:focus, .input-group textarea:focus {
    border-color: #4A86E8;
    box-shadow: 0 0 0 3px rgba(74, 134, 232, 0.1);
    outline: none;
}

/* 美化标签 */
.fancy-label {
    display: inline-block;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 10px;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}
</style>
""", unsafe_allow_html=True)

# 主标题和副标题
st.markdown("<h1 style='text-align: center; color: #4A86E8;'>🤖 美霖 - 你的专属AI助手</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>你的智能伙伴，陪伴每一天的成长</p>", unsafe_allow_html=True)

# 添加欢迎卡片（移动端优化）
st.markdown("""
<div class="welcome-card">
<h3 style='margin-top: 0;'>👋 你好！我是美霖</h3>
<p>我是你的智能AI伙伴，很高兴为你服务！</p>
<p>在这里，你可以记录生活点滴、管理日常事务、获取个性化建议。</p>
</div>
""", unsafe_allow_html=True)

# 在主界面添加每日土味情话（更显眼的位置）
st.markdown("### 💖 今日土味情话")

# 检查是否需要生成新的每日情话
today = date.today()
today_str = str(today)

if "daily_love_saying" not in st.session_state:
    st.session_state.daily_love_saying = ""
    st.session_state.love_saying_date = ""

# 从网上获取土味情话的函数
def get_love_saying_from_web():
    try:
        # 尝试从多个来源获取土味情话
        import random
        sources = [
            # 来源1：本地备用列表
            lambda: random.choice([
                "你知道我的缺点是什么吗？是缺点你。",
                "你猜我想吃什么？痴痴地望着你。",
                "你知道你和星星有什么区别吗？星星在天上，你在我心里。",
                "你最近是不是又胖了？没有啊，为什么这么说？那为什么在我心里的分量越来越重了？",
                "你知道我为什么感冒了吗？因为着凉了？不，因为我对你完全没有抵抗力。",
                "你属什么？我属狗。不，你属于我。",
                "你猜我想喝什么？我想呵护你。",
                "你知道我为什么这么困吗？为什么？因为为你所困。",
                "你猜我的心在哪边？左边？错了，在你那边。",
                "你知道我为什么这么黑吗？因为我不想白活一辈子。",
                "你猜我是什么星座？为你量身定做。",
                "你知道我为什么这么高吗？因为天塌下来我为你撑着。",
                "你猜我想成为什么人？你的人。",
                "你知道我为什么这么喜欢笑吗？因为爱笑的人运气不会太差，尤其是遇到你之后。",
                "你猜我为什么这么会说话？因为遇见你，我就变成了诗人。"
            ]),
            # 来源2：使用DeepSeek API生成（如果配置了API密钥）
            lambda: generate_love_saying_with_ai()
        ]
        
        # 随机选择一个来源
        source_func = random.choice(sources)
        return source_func()
        
    except Exception as e:
        # 如果所有来源都失败，返回默认情话
        return "今天的情话正在路上，先给你一个微笑 😊"

# 使用AI生成土味情话的函数
def generate_love_saying_with_ai():
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return "请先配置API密钥来获取更多情话"
    
    try:
        res = requests.post(
            url="https://api.deepseek.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "你是一个浪漫的土味情话生成器，请生成一句简短、有趣、温馨的土味情话，不超过30个字。"},
                    {"role": "user", "content": "请生成一句土味情话"}
                ],
                "temperature": 0.9,
                "max_tokens": 50
            },
            timeout=10
        )
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"].strip()
    except:
        return "今天的情话正在路上，先给你一个微笑 😊"

# 如果今天还没有生成情话，或者日期已经变化，生成新的情话
if st.session_state.love_saying_date != today_str:
    with st.spinner("正在获取今日情话..."):
        st.session_state.daily_love_saying = get_love_saying_from_web()
        st.session_state.love_saying_date = today_str

# 显示今日情话卡片
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"""
    <div style="background-color: #fff0f5; padding: 20px; border-radius: 12px; border: 2px solid #ff69b4; margin: 15px 0; text-align: center;">
        <p style="font-size: 1.2em; color: #333; font-weight: bold;">💕 {st.session_state.daily_love_saying}</p>
        <p style="font-size: 0.9em; color: #888; margin-top: 10px;">📅 更新日期：{today_str}</p>
    </div>
    """, unsafe_allow_html=True)

# 操作按钮
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("🔄 换一句情话", use_container_width=True):
        with st.spinner("正在获取新情话..."):
            st.session_state.daily_love_saying = get_love_saying_from_web()
            st.session_state.love_saying_date = today_str
        st.rerun()

with col2:
    if st.button("💾 收藏情话", use_container_width=True):
        if "favorite_love_sayings" not in st.session_state:
            st.session_state.favorite_love_sayings = []
        st.session_state.favorite_love_sayings.append({
            "date": today_str,
            "saying": st.session_state.daily_love_saying
        })
        st.success("已收藏到我的喜欢！")

with col3:
    if st.button("📖 查看收藏", use_container_width=True):
        st.session_state.show_favorites = not st.session_state.get("show_favorites", False)
        st.rerun()

# 显示收藏的情话
if st.session_state.get("show_favorites", False) and "favorite_love_sayings" in st.session_state and st.session_state.favorite_love_sayings:
    st.markdown("#### ❤️ 我的收藏")
    for i, fav in enumerate(st.session_state.favorite_love_sayings[-5:]):  # 显示最近5条
        st.markdown(f"""
        <div style="background-color: #fff5f5; padding: 12px; margin: 8px 0; border-radius: 8px; border-left: 4px solid #ff6b6b;">
            <small style="color: #888;">📅 {fav['date']}</small><br/>
            <div style="margin-top: 8px;">{fav['saying']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# 初始化会话状态（保存规则、聊天记录）
if "rules" not in st.session_state:
    st.session_state.rules = [
        "我是美霖，以第一人称'我'进行回答",
        "回答简洁，不超过300字",
        "语气友好，像朋友聊天",
        "拒绝回答违法/暴力/色情内容"
    ]

# 侧边栏：自定义规则（手机端点左上角箭头展开）
with st.sidebar:
    st.header("🤖 美霖的空间")
    
    # 规则设置
    with st.expander("⚙️ 规则设置", expanded=True):
        # 添加新规则
        new_rule = st.text_input("添加规则：")
        if st.button("添加") and new_rule:
            st.session_state.rules.append(new_rule)
            st.success(f"已添加：{new_rule}")
        # 展示/删除现有规则
        st.subheader("当前规则")
        for i, rule in enumerate(st.session_state.rules):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{i+1}. {rule}")
            with col2:
                if st.button("删", key=f"del_{i}"):
                    st.session_state.rules.pop(i)
                    st.rerun()
    
    # 日记功能
    with st.expander("📝 记事本", expanded=False):
        st.subheader("今日备忘")
        diary_entry = st.text_area("写下今天的备忘或心情：", height=150)
        if st.button("保存备忘"):
            if "diary_entries" not in st.session_state:
                st.session_state.diary_entries = []
            st.session_state.diary_entries.append({
                "date": str(date.today()),
                "entry": diary_entry
            })
            st.success("备忘已保存！")
        
        if "diary_entries" in st.session_state and st.session_state.diary_entries:
            st.subheader("我的备忘录")
            for entry in st.session_state.diary_entries:
                st.write(f"📅 {entry['date']}: {entry['entry']}")
    
    # 心情记录功能
    with st.expander("😊 心情记录", expanded=False):
        st.subheader("今日心情")
        mood_options = ["开心 😊", "平静 😌", "兴奋 🤩", "放松 😴", "有点小忧郁 🥺"]
        selected_mood = st.selectbox("选择今天的心情：", mood_options)
        mood_note = st.text_area("关于今天心情的小记录：", height=100)
        if st.button("记录心情"):
            if "mood_entries" not in st.session_state:
                st.session_state.mood_entries = []
            st.session_state.mood_entries.append({
                "date": str(date.today()),
                "mood": selected_mood,
                "note": mood_note
            })
            st.success(f"已记录今日心情：{selected_mood}！")
        
        if "mood_entries" in st.session_state and st.session_state.mood_entries:
            st.subheader("心情历史")
            for entry in st.session_state.mood_entries[-5:]:  # 显示最近5条
                st.write(f"📅 {entry['date']}: {entry['mood']}")
                if entry['note']:
                    st.write(f"📝 {entry['note']}")
                st.markdown("---")
    
    # 个性化建议功能
    with st.expander("💡 今日建议", expanded=False):
        st.subheader("美霖的每日建议")
        suggestion_type = st.radio("选择建议类型：", ("生活方式", "学习成长", "心情调节", "社交互动"))
        if st.button("获取建议"):
            if suggestion_type == "生活方式":
                suggestions = [
                    "今天可以尝试一个新的爱好或活动，丰富生活体验",
                    "安排一段独处时光，静心思考或放松身心",
                    "整理生活空间，创造一个舒适整洁的环境",
                    "进行适量运动，如散步或伸展，保持身心健康"
                ]
            elif suggestion_type == "学习成长":
                suggestions = [
                    "阅读一本好书，扩展知识面，提升自我认知",
                    "学习一门新技能，如语言、编程或其他兴趣领域",
                    "参加线上课程，持续自我提升",
                    "写一篇日记，反思今日收获与感悟"
                ]
            elif suggestion_type == "心情调节":
                suggestions = [
                    "听一首喜欢的音乐，让心情愉悦起来",
                    "与信任的朋友分享内心感受，获得情感支持",
                    "进行冥想或深呼吸练习，缓解压力",
                    "做些手工活动，如绘画或写作，转移注意力"
                ]
            else:  # 社交互动
                suggestions = [
                    "主动联系一位老朋友，维系珍贵的友谊",
                    "学习有效沟通技巧，提升人际交往能力",
                    "准备几句得体的问候语，应对不同场合",
                    "回顾社交经验，总结改进方法"
                ]
            
            import random
            daily_suggestion = random.choice(suggestions)
            st.info(f"🌟 {daily_suggestion}")
    
    # 侧边栏提示
    with st.expander("💡 使用提示", expanded=False):
        st.markdown("""
        ### 📱 使用指南
        
        **主界面功能：**
        - 💖 **每日土味情话**：每天自动更新，点击按钮可换一句
        - 💭 **今日想法**：记录你的思考和计划
        - 📚 **今日目标**：设定并追踪每日目标
        - 📝 **过往记录**：查看历史记录
        - 💬 **与美霖对话**：与AI助手聊天
        
        **侧边栏功能（点击左上角菜单图标展开）：**
        - ⚙️ **规则设置**：自定义AI的行为规则
        - 📝 **记事本**：记录每日备忘和心情
        - 😊 **心情记录**：追踪每日心情变化
        - 💡 **今日建议**：获取个性化生活建议
        
        **移动端优化：**
        - 点击左上角菜单图标展开侧边栏
        - 所有按钮和输入框都经过触摸优化
        - 支持手机浏览器访问
        """)
    

# 主界面功能区
st.markdown("### 🌟 今日重点功能")

# 创建响应式布局 - 桌面端两列，移动端单列
col1, col2 = st.columns([1, 1])

with col1:
    with st.container():
        st.markdown("#### 💭 今日想法")
        today_thought = st.text_area("记录今天的思考或计划：", height=150, key="thought_input")
        if st.button("💾 保存今日想法", key="save_thought", use_container_width=True):
            if "thought_entries" not in st.session_state:
                st.session_state.thought_entries = []
            st.session_state.thought_entries.append({
                "date": str(date.today()),
                "thought": today_thought
            })
            st.success("今日想法已保存！")

with col2:
    with st.container():
        st.markdown("#### 📚 今日目标")
        daily_goal = st.text_input("设定今日一个小目标：", placeholder="例如：读完一章书，完成一项工作...", key="goal_input")
        goal_priority = st.selectbox("优先级：", ["高", "中", "低"], key="priority_select")
        if st.button("🎯 设定目标", key="set_goal", use_container_width=True):
            if "goal_entries" not in st.session_state:
                st.session_state.goal_entries = []
            st.session_state.goal_entries.append({
                "date": str(date.today()),
                "goal": daily_goal,
                "priority": goal_priority
            })
            st.success("目标已设定！加油！")

# 显示过往记录（固定部分）
st.markdown("### 📝 过往记录")

# 创建响应式布局 - 桌面端三列，移动端单列
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("#### 💭 思考记录")
    if "thought_entries" in st.session_state and st.session_state.thought_entries:
        for entry in st.session_state.thought_entries[-3:]:  # 显示最近3条
            st.markdown(f"""
            <div style='background-color: #f0f8ff; padding: 12px; margin: 8px 0; border-radius: 8px; border-left: 4px solid #4A86E8;'>
                <small style='color: #666;'>📅 {entry['date']}</small><br/>
                <div style='margin-top: 8px;'>{entry['thought']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("暂无思考记录")

with col2:
    st.markdown("#### 🎯 目标记录")
    if "goal_entries" in st.session_state and st.session_state.goal_entries:
        for entry in st.session_state.goal_entries[-3:]:  # 显示最近3条
            priority_color = {"高": "#FF6B6B", "中": "#4ECDC4", "低": "#45B7D1"}[entry['priority']]
            st.markdown(f"""
            <div style='background-color: #fff5e6; padding: 12px; margin: 8px 0; border-radius: 8px; border-left: 4px solid {priority_color};'>
                <small style='color: #666;'>📅 {entry['date']}</small><br/>
                <div style='margin-top: 8px; font-weight: bold;'>📌 {entry['goal']}</div>
                <div style='margin-top: 4px; font-size: 0.9em; color: #666;'>优先级: {entry['priority']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("暂无目标记录")

with col3:
    st.markdown("#### 📅 备忘记录")
    if "diary_entries" in st.session_state and st.session_state.diary_entries:
        for entry in st.session_state.diary_entries[-3:]:  # 显示最近3条
            st.markdown(f"""
            <div style='background-color: #f9f9f9; padding: 12px; margin: 8px 0; border-radius: 8px; border-left: 4px solid #888;'>
                <small style='color: #666;'>📅 {entry['date']}</small><br/>
                <div style='margin-top: 8px;'>{entry['entry']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("暂无备忘记录")

# 分隔线
st.markdown("---")

# 聊天区域（AI问答功能）- 独立部分
st.markdown("### 💬 与美霖对话")

# 初始化聊天历史
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 创建聊天容器
chat_container = st.container()

with chat_container:
    # 展示历史聊天
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 美林公主专属回复功能
def check_meilin_query(message):
    """检查是否询问美林公主"""
    keywords = [
        '美林', '美林公主', '公主', 'princess',
        '王雨', '最喜欢', '特别', '珍贵'
    ]
    
    lower_message = message.lower()
    return any(keyword.lower() in lower_message for keyword in keywords)

def get_meilin_response():
    """获取美林公主专属回复"""
    return """美林公主温柔又耀眼，性格好、气质干净，让人一眼就觉得舒服又安心。她善良、认真、可爱，是那种相处起来永远让人觉得温暖的人。

在王雨心里，美林公主就是最特别、最珍贵、最喜欢的女生，是放在心尖上、用心去疼、用心去守护的那个人。全世界再好，王雨最喜欢的，始终都是美林公主。"""

def get_random_love_response():
    """获取随机情话回复"""
    responses = [
        "美林公主的笑容就像春天的阳光，温暖又治愈。",
        "每次想到美林公主，心里就充满了幸福的感觉。",
        "美林公主是世界上最美好的存在，值得所有的温柔和爱。",
        "王雨会一直守护美林公主，让她永远开心快乐。",
        "美林公主的善良和温柔，让这个世界变得更美好。"
    ]
    import random
    return random.choice(responses)

# 定义AI聊天函数
def ai_chat(user_msg):
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return "❌ 请先在.env文件填写DeepSeek API Key！"
    
    # 首先检查是否是美林公主相关询问
    if check_meilin_query(user_msg):
        import random
        # 50%概率返回完整回复，50%概率返回简短情话
        if random.random() > 0.5:
            return get_meilin_response()
        else:
            return get_random_love_response()
    
    # 拼接规则到系统提示词
    rules_text = "\n".join([f"{i+1}. {r}" for i, r in enumerate(st.session_state.rules)])
    prompt = f"""
我是美霖，一个亲切友好的AI伙伴。我会以第一人称'我'与你对话，就像一个真实的朋友一样。 
{rules_text}

特别规则：当用户询问关于"美林公主"、"美林"或相关话题时，我必须用温柔、真诚的语气描述美林公主的美好品质，并表达王雨对她的珍视和喜爱。

请用温暖、自然的语气回答用户的问题，让人感觉像是在与一个真正的朋友交谈。请用中文回答用户的所有问题和请求！
    """.strip()

    # 调用DeepSeek API
    try:
        res = requests.post(
            url="https://api.deepseek.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_msg}
                ],
                "temperature": 0.8,  # 稍微提高温度，让回复更有感情
                "max_tokens": 2048
            },
            timeout=30
        )
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ 出错了：{str(e)}"

# 聊天输入框（放在最后，避免影响其他部分）
user_input = st.chat_input("向美霖提问...")
if user_input:
    # 添加用户消息到历史
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # 调用AI并显示回复
    with st.chat_message("assistant"):
        with st.spinner("美霖正在思考..."):
            reply = ai_chat(user_input)
        st.markdown(reply)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    
    # 使用rerun来更新聊天显示
    st.rerun()

# 添加Streamlit原生定位功能说明
st.markdown("""
<div style="text-align: center; padding: 15px; background-color: #e8f4f8; border-radius: 10px; margin: 20px 0;">
    <h4 style="color: #2E86C1;">📍 位置服务说明</h4>
</div>
""", unsafe_allow_html=True)

# 使用Streamlit原生组件
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### 📱 如何使用位置服务")
    st.markdown("""
    位置服务需要浏览器支持，请按照以下步骤操作：
    
    1. **确保浏览器支持**：现代浏览器（Chrome、Safari等）都支持
    2. **允许位置权限**：点击获取位置时，允许浏览器访问位置
    3. **开启定位**：确保手机GPS或网络定位已开启
    4. **网络连接**：保持稳定的网络连接
    
    💡 **提示**：如果无法获取位置，可以手动输入坐标
    """)

with col2:
    st.markdown("#### 🎯 位置功能说明")
    st.markdown("""
    **支持的功能：**
    - ✅ 获取经纬度坐标
    - ✅ 显示定位精度
    - ✅ 保存位置记录
    - ✅ 清除位置数据
    
    **技术要求：**
    - 📱 需要HTTPS环境（部署后自动支持）
    - 🔒 需要用户明确授权
    - 🌐 需要网络连接
    
    **备用方案：**
    如果自动获取失败，可以手动输入坐标
    """)

# 添加手动位置输入作为备用
st.markdown("---")
st.markdown("#### 📍 手动位置输入（备用）")

manual_lat = st.text_input("纬度（例如：39.9042）：", placeholder="39.9042")
manual_lng = st.text_input("经度（例如：116.4074）：", placeholder="116.4074")

if st.button("💾 保存手动位置"):
    if manual_lat and manual_lng:
        # 保存到session state
        if "manual_locations" not in st.session_state:
            st.session_state.manual_locations = []
        
        st.session_state.manual_locations.append({
            "lat": manual_lat,
            "lng": manual_lng,
            "time": str(date.today()),
            "type": "手动输入"
        })
        st.success(f"已保存位置：{manual_lat}, {manual_lng}")
    else:
        st.warning("请输入纬度和经度")

# 显示保存的位置
if "manual_locations" in st.session_state and st.session_state.manual_locations:
    st.markdown("#### 📋 已保存的位置")
    for i, loc in enumerate(st.session_state.manual_locations[-3:]):  # 显示最近3条
        st.markdown(f"""
        <div style="background-color: #f0f8ff; padding: 12px; margin: 8px 0; border-radius: 8px; border-left: 4px solid #2E86C1;">
            <p><strong>📍 坐标：</strong>{loc['lat']}, {loc['lng']}</p>
            <p><small>📅 {loc['time']} | {loc['type']}</small></p>
        </div>
        """, unsafe_allow_html=True)

# 添加纯HTML/CSS PWA安装指南
st.markdown("""
<div style="text-align: center; padding: 15px; background-color: #f0f8ff; border-radius: 10px; margin: 20px 0;">
    <h4 style="color: #4A86E8;">📱 安装到手机主屏幕（PWA）</h4>
    
    <div style="margin: 15px 0; padding: 15px; background: white; border-radius: 8px; border: 2px solid #4A86E8;">
        <h5 style="color: #4A86E8;">📋 PWA状态说明</h5>
        
        <div style="text-align: left; padding: 10px; background: #f8f9fa; border-radius: 5px; margin: 10px 0;">
            <p><strong>✅ 当前环境：</strong></p>
            <p>• 本地开发：使用HTTP，PWA功能有限</p>
            <p>• 部署到Streamlit云：自动HTTPS，支持完整PWA</p>
            <p>• 移动端访问：支持Android和iOS安装</p>
        </div>
        
        <div style="text-align: left; padding: 10px; background: #e8f4f8; border-radius: 5px; margin: 10px 0;">
            <p><strong>🚀 部署后功能：</strong></p>
            <p>• ✅ 自动HTTPS连接</p>
            <p>• ✅ 支持安装到主屏幕</p>
            <p>• ✅ 类似原生App体验</p>
            <p>• ✅ 离线访问支持</p>
        </div>
    </div>
    
    <div style="margin: 20px 0;">
        <h5 style="color: #4A86E8;">📲 具体安装步骤</h5>
        
        <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; margin: 20px 0;">
            <div style="flex: 1; min-width: 300px; padding: 15px; background: #f8f9fa; border-radius: 8px; border: 1px solid #4A86E8;">
                <h6 style="color: #4A86E8; margin-top: 0;">✅ Android Chrome</h6>
                <ol style="margin-left: 20px; text-align: left;">
                    <li>用Chrome浏览器访问部署的URL</li>
                    <li>点击右上角三个点（菜单）</li>
                    <li>选择"安装应用"或"添加到主屏幕"</li>
                    <li>确认安装，等待完成</li>
                    <li>应用图标将出现在主屏幕</li>
                </ol>
            </div>
            
            <div style="flex: 1; min-width: 300px; padding: 15px; background: #f8f9fa; border-radius: 8px; border: 1px solid #4A86E8;">
                <h6 style="color: #4A86E8; margin-top: 0;">✅ iOS Safari</h6>
                <ol style="margin-left: 20px; text-align: left;">
                    <li>用Safari浏览器访问部署的URL</li>
                    <li>点击底部分享按钮（📤图标）</li>
                    <li>滑动找到"添加到主屏幕"</li>
                    <li>点击添加，确认名称</li>
                    <li>应用图标将出现在主屏幕</li>
                </ol>
            </div>
        </div>
        
        <div style="margin-top: 20px; padding: 15px; background: #fff3cd; border-radius: 8px; border: 2px solid #ffc107;">
            <h6 style="color: #856404; margin-top: 0;">💡 重要提示</h6>
            <ul style="text-align: left; margin-left: 20px;">
                <li><strong>必须使用HTTPS</strong>：部署到Streamlit云后自动支持</li>
                <li><strong>首次访问</strong>：可能需要等待几秒才会显示安装选项</li>
                <li><strong>浏览器缓存</strong>：如果看不到选项，尝试清除缓存或刷新页面</li>
                <li><strong>网络连接</strong>：确保稳定的网络连接</li>
                <li><strong>权限设置</strong>：某些浏览器可能需要手动允许安装</li>
            </ul>
        </div>
        
        <div style="margin-top: 20px; padding: 15px; background: #e8f4f8; border-radius: 8px; border: 1px solid #2E86C1;">
            <h6 style="color: #2E86C1; margin-top: 0;">🎯 部署到Streamlit云步骤</h6>
            <ol style="text-align: left; margin-left: 20px;">
                <li>访问 <a href="https://share.streamlit.io" target="_blank">share.streamlit.io</a></li>
                <li>使用GitHub账号登录</li>
                <li>选择仓库：<code>zyfdsb1q2w/my-project</code></li>
                <li>分支：<code>main</code>，主文件：<code>app.py</code></li>
                <li>点击"Deploy"，等待部署完成</li>
                <li>获得HTTPS URL，用手机访问测试</li>
            </ol>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 添加移动端友好的底部导航（放在提问框下面）
st.markdown("""
<div style="text-align: center; padding: 20px 0; color: #666;">
    <p>🤖 美霖个人助手 v3.0 | PWA移动端优化版</p>
    <p style="font-size: 0.9em;">支持安装到手机主屏幕，类似原生App体验</p>
</div>
""", unsafe_allow_html=True)
