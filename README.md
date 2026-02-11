# BrainyBot

BrainyBot is an intelligent, memory-enabled AI conversational assistant built with modern NLP tools and stateful orchestration. It supports multi-turn interactions, persistent conversation threads, and real-time responses. BrainyBot integrates a Retrieval-Augmented Generation (RAG) pipeline with FAISS vector search and a custom FastMCP tool (e.g., Expense Tracker), allowing contextual querying of uploaded documents and external data operations.

---

## 🧠 Features

* Stateful conversation memory with thread persistence
* Multi-thread chat management (create, select, delete)
* Retrieval-Augmented Generation (RAG) for document querying
* FAISS vector search with Hugging Face embeddings
* Custom MCP integration (Expense Tracker)
* Real-time streaming responses
* Metadata-enabled tracing
* Clean and responsive Streamlit UI

---

## 🚀 Getting Started

### 📦 Prerequisites

Before running BrainyBot, make sure you have:

* Python 3.9+
* A Hugging Face API key
* `.env` file with your API credentials

---

## 📁 Project Structure

```
BrainyBot/
├── backend0.py            # Backend logic & LLM integration
├── frontend0.py           # Streamlit frontend
├── chatbot.db             # SQLite DB for conversation threads
├── requirements.txt       # Python dependencies
└── README.md              # Project overview (this file)
```

---

## 💡 How It Works

1. **Frontend (Streamlit)**

   * Renders a UI for interactive chat
   * Lists chat threads
   * Handles user input and display of AI responses

2. **Backend (LangGraph + LLM)**

   * Manages conversation state
   * Streams responses via Hugging Face Inference API
   * Persists conversations in SQLite

3. **RAG + FAISS**

   * Embeds uploaded documents
   * Stores vectors in FAISS
   * Retrieves relevant context for queries

4. **MCP (FastMCP)**

   * Integrates custom tools like Expense Tracker
   * Allows tool invocation during conversations

---

## 🛠 Installation

1. Clone this repo:

```bash
git clone https://github.com/yashver025/BrainyBot
cd BrainyBot
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Add your environment variables:

Create a `.env` file with:

```
HUGGINGFACE_API_KEY=your_api_key_here
```

---

## ▶️ Run the App

Start the Streamlit UI:

```bash
streamlit run frontend0.py
```

Open your browser at:

```
http://localhost:8501
```

---

## 🧪 Usage

* Select or create a new chat thread
* Ask anything in the chat box
* Upload a PDF (if RAG is enabled) for contextual responses
* Invoke the custom Expense Tracker via natural language

---

## 📈 Tech Stack

* Python
* Streamlit
* LangGraph
* LangChain Core
* FastMCP
* FAISS
* Hugging Face Inference API (Mistral-7B-Instruct)
* SQLite
* dotenv

---

## 📌 Notes

* Ensure you have a valid Hugging Face API key.
* RAG requires document embeddings to be preloaded for semantic search.
* MCP tools must be registered and available to be invoked via the assistant.

---

