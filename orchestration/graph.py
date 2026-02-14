"""LangGraph orchestration for end-to-end compliance QA."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, TypedDict

from langgraph.graph import END, StateGraph

from ingestion.ocr import OCRExtractor
from ingestion.transcriber import Transcriber
from ingestion.video_processor import VideoProcessor
from llm.compliance_validator import ComplianceReport, ComplianceValidator
from rag.retriever import ComplianceRetriever


class ComplianceState(TypedDict, total=False):
    """State object carried between LangGraph nodes."""

    video_path: Path
    audio_path: Path
    frame_paths: List[Path]
    transcript: str
    ocr_text: str
    evidence_text: str
    retrieved_rules: str
    report: Dict[str, Any]


video_processor = VideoProcessor()
transcriber = Transcriber()
ocr_extractor = OCRExtractor(enabled=True)
retriever = ComplianceRetriever()
validator = ComplianceValidator()


def extract_media_node(state: ComplianceState) -> ComplianceState:
    video_path = state["video_path"]
    audio_path = video_processor.extract_audio(video_path)
    frame_paths = video_processor.extract_frames(video_path)
    return {"audio_path": audio_path, "frame_paths": frame_paths}


def transcribe_node(state: ComplianceState) -> ComplianceState:
    transcript = transcriber.transcribe(state["audio_path"])
    return {"transcript": transcript}


def ocr_node(state: ComplianceState) -> ComplianceState:
    ocr_text = ocr_extractor.extract_text(state["frame_paths"])
    return {"ocr_text": ocr_text}


def merge_evidence_node(state: ComplianceState) -> ComplianceState:
    evidence = f"Transcript:\n{state.get('transcript', '')}\n\nOCR:\n{state.get('ocr_text', '')}".strip()
    return {"evidence_text": evidence}


def retrieve_rules_node(state: ComplianceState) -> ComplianceState:
    docs = retriever.retrieve(state["evidence_text"], k=5)
    rules = "\n\n".join(doc.page_content for doc in docs)
    return {"retrieved_rules": rules}


def validate_compliance_node(state: ComplianceState) -> ComplianceState:
    result: ComplianceReport = validator.validate(
        evidence=state["evidence_text"],
        rules_context=state["retrieved_rules"],
    )
    return {"report": result.model_dump()}


def build_graph():
    """Compile and return the LangGraph pipeline."""

    graph = StateGraph(ComplianceState)

    graph.add_node("extract_media", extract_media_node)
    graph.add_node("transcribe", transcribe_node)
    graph.add_node("ocr", ocr_node)
    graph.add_node("merge_evidence", merge_evidence_node)
    graph.add_node("retrieve_rules", retrieve_rules_node)
    graph.add_node("validate_compliance", validate_compliance_node)

    graph.set_entry_point("extract_media")
    graph.add_edge("extract_media", "transcribe")
    graph.add_edge("transcribe", "ocr")
    graph.add_edge("ocr", "merge_evidence")
    graph.add_edge("merge_evidence", "retrieve_rules")
    graph.add_edge("retrieve_rules", "validate_compliance")
    graph.add_edge("validate_compliance", END)

    return graph.compile()
