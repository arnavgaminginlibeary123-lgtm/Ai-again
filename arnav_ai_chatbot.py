import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

class ArnavAI:
    def __init__(self):
        # 1. Access keys from Streamlit Secrets
        api_key = st.secrets["OPENAI_API_KEY"]
        tavily_key = st.secrets["TAVILY_API_KEY"]
        
        # 2. Setup LLM & Internet Tool
        os.environ["TAVILY_API_KEY"] = tavily_key
        self.llm = ChatOpenAI(model="gpt-4o", openai_api_key=api_key, temperature=0.3)
        self.tools = [TavilySearchResults(k=3)]
        
        # 3. Bind tools to the model (The Modern 2026 way)
        llm_with_tools = self.llm.bind_tools(self.tools)

        # 4. Create the high-level system prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are Arnav AI 3.0, a high-level intelligence created by Arnav Srivastava. "
                       "You have real-time internet access. Provide brilliant and accurate answers."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # 5. Build the Agent Chain (No helper function needed!)
        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_tool_messages(x["intermediate_steps"]),
                "chat_history": lambda x: x.get("chat_history", []),
            }
            | prompt
            | llm_with_tools
            | OpenAIToolsAgentOutputParser()
        )

        # 6. Initialize Executor with Memory
        if "memory" not in st.session_state:
            st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

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
            return f"Arnav AI 3.0 encountered a core error: {str(e)}"
