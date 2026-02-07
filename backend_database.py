from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, START, END
from huggingface_hub import InferenceClient
import sqlite3

# -----------------------------
# State
# -----------------------------
class ChatState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

# -----------------------------
# Model
# -----------------------------
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2"
)

# -----------------------------
# Node
# -----------------------------
def chat_node(state: ChatState):
    messages = state["messages"]

    hf_messages = []
    for m in messages:
        if isinstance(m, HumanMessage):
            hf_messages.append({"role": "user", "content": m.content})
        elif isinstance(m, AIMessage):
            hf_messages.append({"role": "assistant", "content": m.content})

    response = client.chat.completions.create(
        messages=hf_messages,
        
    )

    return {
        "messages": [
            AIMessage(content=response.choices[0].message.content)
        ]
    }

# -----------------------------
# Graph
# -----------------------------

conn = sqlite3.connect(database='chatbot.db', check_same_thread=False) #Create SQLite Database
checkpointer = SqliteSaver(conn=conn) #Build connection between SqliteSaver & SQLite DB

graph = StateGraph(ChatState)
graph.add_node("chat", chat_node)
graph.add_edge(START, "chat")
graph.add_edge("chat", END)

# THIS is what frontend imports
chatbot = graph.compile(checkpointer=checkpointer)



#Test Database
# CONFIG = {"configurable": {"thread_id": 'thread-2'}}

# response = chatbot.invoke(
#                 {'messages': [HumanMessage(content = 'Add 25 in the previous answer')]},
#                 config = CONFIG
#             )

# print(response)



#Function to get all the unique threads

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)

