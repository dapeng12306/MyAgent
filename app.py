import streamlit as st
from agent_backend import run_my_agents

# 页面基础设置
st.set_page_config(page_title="智启星图-全天候AI伴学导师", page_icon="🎓", layout="wide")

st.title("🎓 智启星图：全天候AI伴学导师系统")
st.markdown("---")
st.markdown("**研发单位**：本团队独立研发 (大赛盲审专用版)")
st.markdown("**核心技术**：Multi-Agent 协同架构 | 动态学情记忆数据库 | 知识图谱实时检索")
st.markdown("**系统角色**：🧠复盘心理师 | 📚学习委员 | ☕生活助理 | 👨‍💼大管家")
st.markdown("---")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("模拟学生输入，例如：今天高数好难完全听不懂，有点焦虑，今晚还要熬夜复习...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("系统正在进行：学情记忆读取 ➡️ 心理状态评估 ➡️ 个性化知识检索 ➡️ 综合方案生成..."):
            final_plan = run_my_agents(user_input)
            result_str = str(final_plan) 
            st.markdown(result_str)
            st.session_state.chat_history.append({"role": "assistant", "content": result_str})
