import streamlit as st

# Emergency Debug Check
if st.sidebar.button("System Health Check"):
    key = st.secrets.get("OPENAI_API_KEY")
    if not key:
        st.sidebar.error("❌ Secrets not found! Check your Advanced Settings.")
    elif not key.startswith("sk-"):
        st.sidebar.error("❌ Key format is wrong! It must start with 'sk-'.")
    else:
        st.sidebar.success(f"✅ Key loaded! (Length: {len(key)})")

import streamlit as st
from arnav_ai_chatbot import ArnavAI

st.set_page_config(page_title="Arnav AI 3.0", page_icon="🚀")

st.title("🤖 Arnav AI 3.0")
st.caption("Made by Arnav Srivastava | Level 3.0 Intelligence | Internet Access")

# Initialize the AI
if "bot" not in st.session_state:
    st.session_state.bot = ArnavAI()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask me anything about the world..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.session_state.bot.get_response(prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
