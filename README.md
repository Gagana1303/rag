#  Scripture RAG System

A Retrieval-Augmented Generation (RAG) system to query scriptures like Mahabharata, Ramayana, and Puranas using:

- FastAPI (Backend)
- Qdrant (Vector Database)
- Ollama (Local LLM)
- Redis (Caching)

---

##  Features

- Upload scripture PDFs
- Extract, clean, and chunk text
- Store embeddings in Qdrant
- Ask natural language questions
- Fast responses using Redis caching
- Fully local (no API cost)

---

##  Architecture

User → FastAPI → Redis (cache check)  
       ↓  
    Qdrant (vector search)  
       ↓  
    Ollama (LLM)  
       ↓  
    Response  

---

##  Setup Instructions

1. Clone Repository

```bash
git clone <your-repo-url>
cd backend

---

2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate

---

3. Install Dependencies

```bash
pip install -r requirements.txt

---

4. External Dependencies

Install Ollama
Download: https://ollama.com
```bash
ollama pull phi

---

5. Start Qdrant (Vector DB)

```bash
docker run -p 6333:6333 -v qdrant_data:/qdrant/storage qdrant/qdrant

---

 6. Run Backend

```bash
uvicorn app.main:app --reload

---

7. Run Frontend

npm install
npm start

## How to Test
- Start Qdrant + Ollama
- Run backend
- Run frontend
- Upload a PDF
- Ask a question
