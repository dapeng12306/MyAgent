# 文件名：app.py
import streamlit as st
from agent_backend import run_my_agents # 把刚才写的后台逻辑引进来

# 1. 设置网页标题和图标
st.set_page_config(page_title="我的AI私域管家", page_icon="🤖")
st.title("🤖 个人AI多智能体管家")
st.markdown("你的专属团队：👨‍💼大管家 | 📚学习委员 | ☕生活助理")

# 2. 记住之前的聊天记录（防止刷新就没了）
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 把过去的聊天记录显示在屏幕上
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 3. 接收主人输入的打字框
user_input = st.chat_input("告诉管家你今天的想法，例如：我今天下午想学点Python，晚上想吃点清淡的。")

if user_input:
    # 第一步：把主人的话显示出来，并记在小本本上
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 第二步：召唤AI团队开始干活！
    with st.chat_message("assistant"):
        with st.spinner("👨‍💼管家正在召集学习委员和生活助理开会，请稍等大约1-2分钟..."):
            # 调用后台函数
            final_plan = run_my_agents(user_input)
            
            # 由于最新版crewai返回的是一个对象，我们需要把它转成字符串
            result_str = str(final_plan) 
            
            # 显示结果，并记在小本本上
            st.markdown(result_str)
            st.session_state.chat_history.append({"role": "assistant", "content": result_str})