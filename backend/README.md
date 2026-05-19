# Career AI Backend

Production-ready AI/RAG backend for a career guidance and learning platform.

Built with **FastAPI · LangChain · LangGraph · Ollama (llama3) · ChromaDB · Sentence Transformers**

---

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── upload.py          # POST /upload
│   │   ├── chat.py            # POST /chat
│   │   ├── search.py          # POST /search
│   │   ├── skill_gap.py       # POST /skill-gap-analysis
│   │   └── documents.py       # GET /documents, DELETE /document/{id}
│   ├── services/
│   │   ├── embedding_service.py   # sentence-transformers wrapper
│   │   ├── ollama_service.py      # Ollama LLM wrapper (sync + streaming)
│   │   └── document_service.py    # file I/O, text extraction, chunking
│   ├── rag/
│   │   └── pipeline.py        # Full RAG pipeline (embed → retrieve → generate)
│   ├── workflows/
│   │   ├── rag_workflow.py        # LangGraph: query → retrieval → ranking → response
│   │   └── skill_gap_workflow.py  # LangGraph: skill extraction → gap → recommend → roadmap
│   ├── db/
│   │   └── chroma_client.py   # ChromaDB persistent client
│   ├── models/
│   │   └── schemas.py         # All Pydantic request/response models
│   ├── utils/
│   │   ├── logger.py          # Logging setup
│   │   └── sanitizer.py       # Input sanitization helpers
│   ├── config.py              # Settings loaded from .env
│   └── main.py                # FastAPI app, routers, lifespan hooks
├── chroma_db/                 # ChromaDB persistent storage (auto-created)
├── uploads/                   # Uploaded files (auto-created)
├── requirements.txt
├── .env.example               # Copy this to .env and fill in values
└── README.md
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| API Framework | FastAPI |
| LLM | Ollama (llama3) |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector Database | ChromaDB (persistent) |
| AI Orchestration | LangChain + LangGraph |
| Document Parsing | pypdf, python-docx |
| Runtime | Python 3.11 |

---

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.11 | [python.org](https://python.org) |
| Ollama | latest | [ollama.com](https://ollama.com) |
| llama3 model | — | `ollama pull llama3` |

> ⚠️ Python 3.12+ is supported. Python 3.14 is NOT supported (pydantic-core requires ≤3.13).

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/VickySource/path-pilot-ai.git
cd path-pilot-ai/backend
```

### 2. Create a virtual environment with Python 3.11

```bash
# Windows
py -3.11 -m venv venv
venv\Scripts\activate

# macOS / Linux
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
# Copy the example file
copy .env.example .env   # Windows
cp .env.example .env     # macOS/Linux

# Edit .env if needed (defaults work for local development)
```

### 5. Start Ollama

```bash
# In a separate terminal — keep this running
ollama serve

# Pull the model (one-time download, ~4 GB)
ollama pull llama3
```

> If you see `bind: Only one usage of each socket address` — Ollama is already running. Skip this step.

### 6. Start the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API is now live at **http://localhost:8000**

| URL | Description |
|-----|-------------|
| http://localhost:8000/docs | Swagger UI (interactive) |
| http://localhost:8000/redoc | ReDoc documentation |
| http://localhost:8000/health | Health check |

---

## API Endpoints

### POST /upload
Upload a PDF, DOCX, or TXT file for indexing.

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@/path/to/document.pdf"
```

**Response:**
```json
{
  "success": true,
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "document.pdf",
  "total_chunks": 42,
  "message": "Document indexed successfully with 42 chunks."
}
```

---

### POST /chat
Ask a question grounded in your indexed documents.

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What skills do I need to become a data scientist?",
    "conversation_history": [],
    "document_id": null
  }'
```

**Response:**
```json
{
  "answer": "To become a data scientist, you need...",
  "sources": [
    {
      "document_id": "550e8400-...",
      "source_file": "guide.pdf",
      "chunk_index": 3,
      "content_preview": "Data scientists require...",
      "relevance_score": 0.87
    }
  ],
  "query": "What skills do I need to become a data scientist?",
  "model_used": "llama3"
}
```

---

### POST /search
Semantic similarity search over indexed documents.

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning algorithms",
    "top_k": 5,
    "score_threshold": 0.3
  }'
```

---

### POST /skill-gap-analysis
Analyse the gap between current skills and a target role.

```bash
curl -X POST http://localhost:8000/skill-gap-analysis \
  -H "Content-Type: application/json" \
  -d '{
    "current_skills": ["Python", "SQL", "Excel", "Statistics"],
    "target_role": "Machine Learning Engineer"
  }'
```

**Response:**
```json
{
  "target_role": "Machine Learning Engineer",
  "current_skills": ["Python", "SQL", "Excel", "Statistics"],
  "required_skills": ["Python", "TensorFlow", "PyTorch", "Docker", "MLOps"],
  "missing_skills": ["TensorFlow", "PyTorch", "Docker", "Kubernetes", "MLOps"],
  "matching_skills": ["Python", "SQL", "Statistics"],
  "gap_percentage": 62.5,
  "courses": [
    {
      "title": "Deep Learning Specialization",
      "platform": "Coursera",
      "skill_covered": "TensorFlow",
      "estimated_duration": "4 weeks",
      "difficulty": "Intermediate"
    }
  ],
  "projects": [
    {
      "title": "Build an Image Classifier",
      "description": "Train a CNN on CIFAR-10 dataset",
      "skills_practiced": ["PyTorch", "Deep Learning"],
      "difficulty": "Intermediate"
    }
  ],
  "roadmap": [
    {
      "step": 1,
      "title": "Master Deep Learning Frameworks",
      "description": "Learn TensorFlow and PyTorch fundamentals",
      "duration": "4 weeks",
      "skills": ["TensorFlow", "PyTorch"]
    }
  ],
  "summary": "With your Python and statistics background, you are well-positioned..."
}
```

---

### GET /documents
List all indexed documents.

```bash
curl http://localhost:8000/documents
```

---

### DELETE /document/{id}
Delete a document and all its chunks.

```bash
curl -X DELETE http://localhost:8000/document/550e8400-e29b-41d4-a716-446655440000
```

---

## Architecture

```
User Request
     │
     ▼
FastAPI Router
     │
     ├── /upload ──► DocumentService (extract + chunk)
     │                    └──► EmbeddingService ──► ChromaDB
     │
     ├── /chat ───► RAGPipeline
     │                   ├── EmbeddingService (embed query)
     │                   ├── ChromaDB (retrieve top-k chunks)
     │                   └── OllamaService (generate answer)
     │
     ├── /search ──► EmbeddingService ──► ChromaDB
     │
     └── /skill-gap-analysis ──► LangGraph Workflow
                                      ├── Node 1: skill_extraction  (LLM)
                                      ├── Node 2: gap_analysis       (LLM)
                                      ├── Node 3: recommendations    (LLM)
                                      └── Node 4: roadmap_generation (LLM)
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `llama3` | LLM model name |
| `OLLAMA_TIMEOUT` | `120` | Request timeout (seconds) |
| `CHROMA_PERSIST_DIR` | `./chroma_db` | ChromaDB storage path |
| `CHROMA_COLLECTION_NAME` | `career_docs` | Collection name |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence transformer model |
| `CHUNK_SIZE` | `1000` | Characters per chunk |
| `CHUNK_OVERLAP` | `200` | Overlap between chunks |
| `UPLOAD_DIR` | `./uploads` | File upload directory |
| `MAX_FILE_SIZE_MB` | `20` | Max upload size in MB |
| `ALLOWED_EXTENSIONS` | `pdf,docx,txt` | Allowed file types |
| `TOP_K_RESULTS` | `5` | Default retrieval count |
| `SCORE_THRESHOLD` | `0.3` | Minimum similarity score |

---

## Team

This backend was built as part of the **Path Pilot AI** project.

| Member | Branch |
|--------|--------|
| Tejaswini | `dev/tejaswini` |

---

## Troubleshooting

**Ollama not reachable**
```bash
ollama serve
ollama list  # verify llama3 is downloaded
```

**Model not found**
```bash
ollama pull llama3
```

**pydantic-core build error**
You are on Python 3.14. Use Python 3.11 instead:
```bash
py -3.11 -m venv venv
```

**ChromaDB reset**
```bash
# Windows
Remove-Item -Recurse -Force chroma_db

# macOS/Linux
rm -rf chroma_db/
```

**Slow first request**
The sentence-transformer model downloads on first use (~90 MB). Subsequent requests are fast.
