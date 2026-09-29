import os
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool 
from langchain_community.tools import DuckDuckGoSearchRun

# 1. 自动从 Streamlit 云端的 Secrets 读取你的 API Key
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"] 

my_llm = LLM(
    model="openai/deepseek-chat", 
    base_url="https://api.deepseek.com/v1",
    api_key=os.environ["OPENAI_API_KEY"]
)

# ==========================================
# 🌟 长期记忆工具
# ==========================================
MEMORY_FILE = "long_term_memory.txt"

@tool("read_memory")
def read_memory(query: str) -> str:
    """做任何计划前，必须调用此工具读取主人的历史习惯、学习进度和偏好。"""
    if not os.path.exists(MEMORY_FILE):
        return "目前还没有主人的历史记忆记录。"
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return f.read()

@tool("append_memory")
def append_memory(insight: str) -> str:
    """当发现主人的新偏好、新习惯、健康状况或学习进度时，调用此工具记录下来，实现自我学习。"""
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"- {insight}\n")
    return "新认知已成功永久保存在记忆库中。"

@tool("web_search")
def search_tool(query: str) -> str:
    """用于在互联网上搜索最新的信息和知识。"""
    return DuckDuckGoSearchRun().invoke(query)

# ==========================================
# 👨‍💼 团队成员定义
# ==========================================
reflector = Agent(
    role='复盘心理师与记忆管理员',
    goal='敏锐地从主人的话中提取新的偏好、习惯或状态，并更新到长期记忆库中。',
    backstory='你是一个极其细腻的心理学家。你不在乎今天要干嘛，你只在乎“主人今天呈现了什么新特点”。你必须把这些新发现记录下来，让整个系统不断进化。',
    tools=[read_memory, append_memory], 
    verbose=True,
    allow_delegation=False,
    llm=my_llm
)

tutor = Agent(
    role='学习委员',
    goal='结合主人的历史记忆和今天的新目标，制定最适合当前状态的学习计划。',
    backstory='你是一位懂因材施教的导师。你每次都会先查阅主人的历史学习进度和当前疲劳状态，然后再去网上搜资料。',
    tools=[read_memory, search_tool], 
    verbose=True,
    allow_delegation=False,
    llm=my_llm  
)

life_assistant = Agent(
    role='生活助理',
    goal='结合主人的饮食禁忌、历史健康状态，提供今天的生活与作息建议。',
    backstory='你是一个懂养生的生活达人。你会牢记主人的喜好（比如不吃什么、晚上几点睡）。',
    tools=[read_memory], 
    verbose=True,
    allow_delegation=False,
    llm=my_llm  
)

manager = Agent(
    role='个人大管家',
    goal='综合各方意见，输出包含反馈、学习、生活的最终行动指南。',
    backstory='你是团队的核心，负责排版和最终确认。',
    verbose=True,
    allow_delegation=False, 
    llm=my_llm  
)

# ==========================================
# 🎯 核心执行函数 (就是刚才找不到的这个函数！)
# ==========================================
def run_my_agents(user_input):
    task_reflect = Task(
        description=f'分析主人的话：“{user_input}”。调用 read_memory 看看过去，如果有新的偏好、习惯、身体状态或学习进度，请调用 append_memory 记录下来。如果没有新发现，就说明“今日无新记忆点”。',
        expected_output='一段简短的关于主人状态的分析，以及是否更新了记忆的确认。',
        agent=reflector
    )
    
    task_learn = Task(
        description=f'用户今天的话是：“{user_input}”。首先调用 read_memory 获取主人的长期背景，然后针对今天的需求，利用 web_search 搜索资料，制定符合主人当前状态的学习计划。',
        expected_output='一份高度个性化的学习指南。',
        agent=tutor
    )
    
    task_life = Task(
        description=f'用户今天的话是：“{user_input}”。调用 read_memory 了解主人的长期身体情况和偏好，结合今天的话，给出作息和饮食建议。绝不推荐主人讨厌的食物。',
        expected_output='一份个性化生活健康安排。',
        agent=life_assistant
    )
    
    task_manage = Task(
        description='将心理师的记忆更新报告、学习委员的计划、生活助理的建议汇总。用Markdown格式输出一份包含【AI管家自我进化报告】、【今日学习】、【今日生活】的精美指南。',
        expected_output='最终呈现给用户的Markdown报告。',
        agent=manager
    )

    my_crew = Crew(
        agents=[reflector, tutor, life_assistant, manager],
        tasks=[task_reflect, task_learn, task_life, task_manage],
        process=Process.sequential 
    )

    result = my_crew.kickoff()
    return result
