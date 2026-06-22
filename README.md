# 🤖 DocuMind AI

> AI-powered multi-PDF chat assistant with memory, voice interaction, and RAG-based document retrieval using LangChain, Gemini, Ollama, and ChromaDB.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green)
![Gemini](https://img.shields.io/badge/Gemini-AI-orange)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black)

---

## 📌 Overview

DocuMind AI is an intelligent document assistant that allows users to upload multiple PDF files and interact with them through natural language conversations. It leverages Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs) to provide context-aware answers, conversational memory, voice interaction, and efficient semantic search.

---

## ✨ Features

- Multi-PDF Upload Support
- Chat with Documents
- Conversational Memory
- Semantic Search using ChromaDB
- Gemini + Ollama Integration
- RAG-based Document Retrieval
- Voice Input
- Text-to-Speech Response
- Pin Chats
- Archive Conversations
- Rename & Delete Chats
- Export Conversations to TXT/PDF
- Modern Streamlit UI
- Source-aware Responses

---

## 🛠 Tech Stack

### Frontend
- Streamlit

### AI & LLM
- Google Gemini
- Ollama

### Framework
- LangChain

### Vector Database
- ChromaDB

### Embeddings
- Sentence Transformers

### Voice Features
- gTTS
- Streamlit Mic Recorder

### Backend
- Python

---

## 🏗 Architecture

```text
PDF Files
    ↓
Text Extraction
    ↓
Chunking
    ↓
Embeddings
    ↓
ChromaDB Vector Store
    ↓
Retriever (RAG)
    ↓
Gemini / Ollama
    ↓
AI Response
```

---

## 📂 Project Structure

```text
DocuMind-AI/
│
├── app.py
├── chat_manager.py
├── embeddings.py
├── gemini_chat.py
├── pdf_processor.py
├── vector_store.py
├── rag.py
├── requirements.txt
├── .gitignore
├── chat_data/
└── chroma_db/
```

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/sakshikal532004/DocuMind-AI.git

cd DocuMind-AI
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

---

## ▶ Run Application

```bash
streamlit run app.py
```

---

## 📸 Screenshots

### Home Page
Upload PDFs and interact intelligently.
<img width="1865" height="842" alt="image" src="https://github.com/user-attachments/assets/e930c56a-491b-4a9d-a273-7bf2f95e1795" />


### Chat Interface
Ask questions from uploaded documents.
<img width="1817" height="767" alt="image" src="https://github.com/user-attachments/assets/a82674c5-2729-44ca-a1d3-7acd5bbe443a" />


### Multi Chat Support
Rename, Pin, Archive and Manage Conversations.
<img width="856" height="756" alt="image" src="https://github.com/user-attachments/assets/b3cd3dee-e29b-4629-96b6-765bb6084be2" />


---

## Future Improvements

- Multi-language Support
- Analytics Dashboard
- Notes Generation
- Quiz Generation
- DOCX Support
- Cloud Deployment
- User Authentication
- Shareable Chat Sessions

---

## 👨‍💻 Author

**Sakshi Kalyankar**

- GitHub: https://github.com/sakshikal532004
- LinkedIn: www.linkedin.com/in/sakshi-kalyankar

---

## License

© 2026 Sakshi Kalyankar. All rights reserved.
