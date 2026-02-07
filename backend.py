from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from huggingface_hub import InferenceClient

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
checkpointer = InMemorySaver()

graph = StateGraph(ChatState)
graph.add_node("chat", chat_node)
graph.add_edge(START, "chat")
graph.add_edge("chat", END)

# ✅ THIS is what frontend imports
chatbot = graph.compile(checkpointer=checkpointer)


#For STREAMING

# for message_chunk, metadata in chatbot.stream(
#     {'messages': [HumanMessage(content = "write 500 words essay on cricket.")]},
#     config = {'configurable' : {'thread_id': 'thread-1'}},
#     stream_mode = 'messages'
# ):
#     if message_chunk.content:
#         print(message_chunk.content, end=" ", flush=True)



#To fetch messages using thread id

# CONFIG = {"configurable": {"thread_id": 'thread-1'}}


# response = chatbot.invoke(
#                 {'messages': [HumanMessage(content = 'Hi, my name is Yash.')]},
#                 config = CONFIG
# )

# print(chatbot.get_state(config=CONFIG).values['messages'])
