import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

# --- THE FIX FOR 2026 ---
# Import from langchain_classic instead of langchain
from langchain_classic.agents import create_openai_functions_agent, AgentExecutor
from langchain_classic.memory import ConversationBufferMemory
# ------------------------

from langchain import hub

class ArnavAI:
    def __init__(self):
        # Access keys from Streamlit Secrets
        api_key = st.secrets["OPENAI_API_KEY"]
        tavily_key = st.secrets["TAVILY_API_KEY"]
        
        self.llm = ChatOpenAI(model="gpt-4o", openai_api_key=api_key, temperature=0.3)
        os.environ["TAVILY_API_KEY"] = tavily_key
        self.search = TavilySearchResults(k=3)
        self.tools = [self.search]

        if "memory" not in st.session_state:
            st.session_state.memory = ConversationBufferMemory(
                memory_key="chat_history", 
                return_messages=True
            )

        prompt = hub.pull("hwchase17/openai-functions-agent")
        
        # This now works perfectly because of the langchain_classic import
        agent = create_openai_functions_agent(self.llm, self.tools, prompt)
        self.executor = AgentExecutor(
            agent=agent, 
            tools=self.tools, 
            memory=st.session_state.memory, 
            verbose=True,
            handle_parsing_errors=True
        )

    def get_response(self, user_input):
        try:
            return self.executor.invoke({"input": user_input})["output"]
        except Exception as e:
            return f"Arnav AI 3.0 Core Error: {str(e)}"
