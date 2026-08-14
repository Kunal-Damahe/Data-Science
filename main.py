"""FastAPI entrypoint for the Multi-Modal Compliance QA Pipeline."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel, HttpUrl

from config import get_settings
from ingestion.video_processor import VideoProcessor
from orchestration.graph import build_graph, retriever
from rag.vector_store import ComplianceVectorStore

settings = get_settings()

if settings.langsmith_tracing:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = settings.langsmith_project
    # TODO: Set LANGSMITH_API_KEY in your .env file.
    os.environ["LANGCHAIN_API_KEY"] = settings.langsmith_api_key


app = FastAPI(title=settings.app_name)
video_processor = VideoProcessor()
pipeline = build_graph()


class AnalyzeURLRequest(BaseModel):
    """Payload for YouTube analysis endpoint."""

    youtube_url: HttpUrl


class AnalyzeResponse(BaseModel):
    """Structured response returned to API clients."""

    violations: list[str]
    risk_score: int
    summary: str
    recommendations: list[str]


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "env": settings.app_env}


@app.post("/rules/build-index")
def build_rules_index(rule_file_path: Optional[str] = None) -> dict:
    """Build FAISS index from compliance rules text file and refresh the retriever."""

    path = Path(rule_file_path) if rule_file_path else None
    ComplianceVectorStore().build_index(path)
    retriever.refresh()
    return {"status": "index_built", "path": str(settings.vector_store_dir)}


@app.post("/analyze/upload", response_model=AnalyzeResponse)
async def analyze_uploaded_video(file: UploadFile = File(...)) -> AnalyzeResponse:
    """Analyze an uploaded video for policy violations."""

    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file must have a name.")

    safe_name = Path(file.filename).name
    if not safe_name or safe_name in {".", ".."}:
        raise HTTPException(status_code=400, detail="Uploaded file has an invalid name.")

    destination = settings.upload_dir / f"{uuid4().hex}_{safe_name}"
    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = pipeline.invoke({"video_path": destination})
    return AnalyzeResponse(**result["report"])


@app.post("/analyze/youtube", response_model=AnalyzeResponse)
def analyze_youtube_video(payload: AnalyzeURLRequest) -> AnalyzeResponse:
    """Download and analyze video from YouTube URL."""

    try:
        video_path = video_processor.download_youtube_video(str(payload.youtube_url))
        result = pipeline.invoke({"video_path": video_path})
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Analysis failed: {exc}") from exc

    return AnalyzeResponse(**result["report"])
