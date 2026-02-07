from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, START, END
from huggingface_hub import InferenceClient
import sqlite3
import uuid

# =============================
# Database
# =============================
conn = sqlite3.connect("chatbot.db", check_same_thread=False)
cursor = conn.cursor()

# Threads metadata table
cursor.execute("""
CREATE TABLE IF NOT EXISTS threads (
    thread_id TEXT PRIMARY KEY,
    title TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# =============================
# LangGraph State
# =============================
class ChatState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

# =============================
# Model
# =============================
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2"
)

# =============================
# Node
# =============================
def chat_node(state: ChatState):
    messages = state["messages"]

    hf_messages = []
    for m in messages:
        if isinstance(m, HumanMessage):
            hf_messages.append({"role": "user", "content": m.content})
        elif isinstance(m, AIMessage):
            hf_messages.append({"role": "assistant", "content": m.content})

    response = client.chat.completions.create(
        messages=hf_messages
    )

    return {
        "messages": [
            AIMessage(content=response.choices[0].message.content)
        ]
    }

# =============================
# Graph
# =============================
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)
graph.add_node("chat", chat_node)
graph.add_edge(START, "chat")
graph.add_edge("chat", END)

chatbot = graph.compile(checkpointer=checkpointer)

# =============================
# Thread Management
# =============================

def create_thread(title="New Chat"):
    tid = str(uuid.uuid4())
    cursor.execute(
        "INSERT INTO threads (thread_id, title) VALUES (?, ?)",
        (tid, title)
    )
    conn.commit()
    return tid

def update_thread_title(thread_id, first_message):
    words = first_message.strip().split()

    # take only first 5 words
    short_title = " ".join(words[:5])

    # add ellipsis if message was longer
    if len(words) > 4:
        short_title += "…"

    # hard cap length (for perfect sidebar alignment)
    #

    cursor.execute(
        "UPDATE threads SET title=? WHERE thread_id=?",
        (short_title, thread_id)
    )
    conn.commit()


def retrieve_all_threads():
    cursor.execute("""
        SELECT thread_id, title
        FROM threads
        ORDER BY created_at DESC
    """)
    rows = cursor.fetchall()
    return [{"thread_id": r[0], "title": r[1]} for r in rows]


def delete_thread(thread_id: str):
    cursor = conn.cursor()

    # delete thread metadata
    cursor.execute(
        "DELETE FROM threads WHERE thread_id = ?",
        (thread_id,)
    )

    # delete LangGraph checkpoints (FIXED)
    cursor.execute("""
        DELETE FROM checkpoints
        WHERE json_extract(metadata, '$.configurable.thread_id') = ?
    """, (thread_id,))

    conn.commit()
