import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_tool_calling_agent, AgentExecutor # Fixed Import
from langchain.memory import ConversationBufferMemory
from langchain import hub

class ArnavAI:
    def __init__(self):
        # Access keys securely
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

        # Updated prompt for tool calling
        prompt = hub.pull("hwchase17/openai-tools-agent")
        
        # Build the agent the modern way
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        self.executor = AgentExecutor(
            agent=agent, 
            tools=self.tools, 
            memory=st.session_state.memory, 
            verbose=True
        )

    def get_response(self, user_input):
        return self.executor.invoke({"input": user_input})["output"]
