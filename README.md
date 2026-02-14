# Multi-Modal Compliance QA Pipeline

Production-style starter implementation for video compliance auditing using FastAPI + LangGraph + Gemini + FAISS.

## Folder Structure

```text
.
├── config.py
├── main.py
├── requirements.txt
├── .env.example
├── data/
│   └── compliance_rules.txt
├── ingestion/
│   ├── __init__.py
│   ├── video_processor.py
│   ├── transcriber.py
│   └── ocr.py
├── rag/
│   ├── __init__.py
│   ├── vector_store.py
│   └── retriever.py
├── llm/
│   ├── __init__.py
│   └── compliance_validator.py
├── orchestration/
│   ├── __init__.py
│   └── graph.py
└── frontend/
    ├── __init__.py
    └── streamlit_app.py
```

## Pipeline Flow

1. Upload video file (or pass YouTube URL).
2. Download/process video with `yt-dlp` + `ffmpeg`.
3. Extract audio and transcribe via Whisper.
4. Extract frames and run optional OCR with easyOCR.
5. Merge transcript and OCR text into a single evidence payload.
6. Retrieve relevant compliance rules from FAISS (Gemini embeddings).
7. Validate compliance with Gemini chat model.
8. Return structured JSON:
   - `violations`
   - `risk_score`
   - `summary`
   - `recommendations`

## Setup

### 1) Install OS dependencies

You need `ffmpeg` installed and available in PATH.

### 2) Create and activate virtual environment

```bash
python3.9 -m venv .venv
source .venv/bin/activate
```

### 3) Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4) Configure environment variables

```bash
cp .env.example .env
```

Fill in:
- `GOOGLE_API_KEY`
- `LANGSMITH_API_KEY`

### 5) Build initial vector index

```bash
uvicorn main:app --reload
# in another terminal
curl -X POST http://localhost:8000/rules/build-index
```

### 6) Run backend

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 7) Run frontend

```bash
streamlit run frontend/streamlit_app.py
```

## API Endpoints

- `GET /health`
- `POST /rules/build-index`
- `POST /analyze/upload` (multipart upload)
- `POST /analyze/youtube` (JSON `{ "youtube_url": "..." }`)

## Notes

- easyOCR is optional; if import fails, OCR is skipped automatically.
- SQLAlchemy and Redis are listed as optional dependencies for future persistence/caching extensions.
- LangSmith tracing is enabled by env flags and API key.
