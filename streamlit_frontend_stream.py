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


 

    
    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content = user_input)]},
                config = {'configurable' : {'thread_id': 'thread-1'}},
                stream_mode = 'messages'
            )

        )
    
    st.session_state['message_history'].append({'role':'assistant', 'content': ai_message})
