import streamlit as st
from backend_database import chatbot
from langchain_core.messages import HumanMessage
import uuid 
from backend_database import retrieve_all_threads




#************************************************UTILITY FUNCTIONS*******************************************************************

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id


def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id) 

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id  # This is the current thread
    add_thread(st.session_state['thread_id']) # Stores this thread in chat_threads
    st.session_state['message_history'] = [] # make message_history EMPTY

def load_conversation(thread_id):
    state = chatbot.get_state(
        config={"configurable": {"thread_id": thread_id}}
    )

    if not state or "messages" not in state.values:
        return []   # empty chat, no messages yet

    return state.values["messages"]




#*************************************************SESSION SETUP*********************************************************************

# session_state is a dictionary to store conversation even when the code runs again from start, until we manually refresh or rerun
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = [] #starts empty


if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()  # generate one thread


if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])



#*************************************************SIDEBAR UI*************************************************************************

st.sidebar.title("🤖 BrainyBot")
st.sidebar.caption("Memory-enabled AI assistant")

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')


for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        #Formatting
        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role': role, 'content': msg.content})

        st.session_state['message_history'] = temp_messages



#****************************************************MAIN UI**************************************************************************

#Loading Conversation History
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])



user_input = st.chat_input('Type here')

if user_input:

    st.session_state['message_history'].append({'role':'user', 'content':user_input})
    with st.chat_message('user'):
        st.text(user_input)


    CONFIG = {"configurable": {"thread_id": st.session_state['thread_id']}}


    
    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content = user_input)]},
                config = CONFIG,
                stream_mode = 'messages'
            )

        )
    
    st.session_state['message_history'].append({'role':'assistant', 'content': ai_message})
