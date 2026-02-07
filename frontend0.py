from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from backend0 import (
    chatbot,
    retrieve_all_threads,
    create_thread,
    update_thread_title,
    delete_thread
)
from langchain_core.messages import HumanMessage, AIMessage

st.markdown("""
<style>
.active-chat button {
    background-color: #ff4b4b !important;
    color: white !important;
    border-radius: 8px !important;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="BrainyBot", page_icon="🤖", layout="wide")

# =============================
# Utility
# =============================
def load_conversation(thread_id):
    state = chatbot.get_state(
        config={"configurable": {"thread_id": thread_id}}
    )
    if not state or "messages" not in state.values:
        return []
    return state.values["messages"]


# =============================
# Session Setup
# =============================
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    threads = retrieve_all_threads()

    if len(threads) > 0:
        # load most recent chat
        st.session_state["thread_id"] = threads[0]["thread_id"]
        messages = load_conversation(st.session_state["thread_id"])

        temp = []
        for msg in messages:
            role = "user" if isinstance(msg, HumanMessage) else "assistant"
            temp.append({"role": role, "content": msg.content})

        st.session_state["message_history"] = temp
    else:
        # no chats exist yet → create first one
        st.session_state["thread_id"] = create_thread()


# =============================
# Sidebar
# =============================
st.sidebar.header("🤖 BrainyBot")
st.sidebar.caption("Memory-enabled AI assistant")

if st.sidebar.button("➕ New Chat"):
    st.session_state["thread_id"] = create_thread()
    st.session_state["message_history"] = []

st.sidebar.header("Your Conversations")

for thread in retrieve_all_threads():
    col1, col2 = st.sidebar.columns([4, 1])

    if col1.button(thread["title"], key=thread["thread_id"]):
        st.session_state["thread_id"] = thread["thread_id"]
        messages = load_conversation(thread["thread_id"])

        temp = []
        for msg in messages:
            role = "user" if isinstance(msg, HumanMessage) else "assistant"
            temp.append({"role": role, "content": msg.content})
        st.session_state["message_history"] = temp

    if col2.button("🗑", key=f"del_{thread['thread_id']}"):
        delete_thread(thread["thread_id"])

        # reset UI if current thread was deleted
        if st.session_state["thread_id"] == thread["thread_id"]:
            st.session_state["thread_id"] = create_thread()
            st.session_state["message_history"] = []

        st.rerun()


# =============================
# Main UI
# =============================
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input("Ask anything")

if user_input:
    st.session_state["message_history"].append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.text(user_input)

    # update title only once
    if len(st.session_state["message_history"]) == 1:
        update_thread_title(st.session_state["thread_id"], user_input)

    
    #CONFIG = {"configurable": {"thread_id": st.session_state["thread_id"]}}


    #For LangSmith we have to add metadata about threads for seperate tracing
    CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {
            "thread_id": st.session_state["thread_id"]
        },
        "run_name": "chat_turn",
    }

    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            chunk.content
            for chunk, _ in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
            )
            if chunk.content
        )

    st.session_state["message_history"].append(
        {"role": "assistant", "content": ai_message}
    )
