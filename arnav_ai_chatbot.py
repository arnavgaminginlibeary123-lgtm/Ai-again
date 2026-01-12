import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain import hub

class ArnavAI:
    def __init__(self):
        # Accessing keys safely from Streamlit Secrets
        api_key = st.secrets["OPENAI_API_KEY"]
        tavily_key = st.secrets["TAVILY_API_KEY"]
        
        # 1. Level 3.0 Brain
        self.llm = ChatOpenAI(model="gpt-4o", openai_api_key=api_key, temperature=0.3)

        # 2. Internet Tool
        os.environ["TAVILY_API_KEY"] = tavily_key
        self.search = TavilySearchResults(k=3)
        self.tools = [self.search]

        # 3. Memory
        if "memory" not in st.session_state:
            st.session_state.memory = ConversationBufferMemory(
                memory_key="chat_history", 
                return_messages=True
            )

        # 4. Identity Prompt
        prompt = hub.pull("hwchase17/openai-functions-agent")
        prompt.messages[0].content = (
            "You are Arnav AI 3.0, a high-level artificial intelligence made by Arnav Srivastava. "
            "You have full internet access to provide real-time data. "
            "Be precise, professional, and brilliant."
        )

        # 5. Agent Executor
        agent = create_openai_functions_agent(self.llm, self.tools, prompt)
        self.executor = AgentExecutor(
            agent=agent, 
            tools=self.tools, 
            memory=st.session_state.memory, 
            verbose=True
        )

    def get_response(self, user_input):
        return self.executor.invoke({"input": user_input})["output"]
