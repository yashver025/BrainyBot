import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage


st.set_page_config(
    page_title="BrainyBot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 BrainyBot")
st.caption("A memory-enabled AI chatbot powered by LangGraph + Mistral")


CONFIG = {"configurable": {"thread_id": "streamlit-chat"}}

# session_state is a dictionary to store conversation even when the code runs again from start, until we manually refresh or rerun
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])



user_input = st.chat_input('Type here')

if user_input:

    st.session_state['message_history'].append({'role':'user', 'content':user_input})
    with st.chat_message('user'):
        st.text(user_input)


    response = chatbot.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config= CONFIG
    )

    ai_message = response["messages"][-1].content

    st.session_state['message_history'].append({'role':'assistant', 'content': ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)