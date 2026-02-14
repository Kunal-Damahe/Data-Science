"""Whisper transcription module."""

from pathlib import Path

import whisper

from config import get_settings


class Transcriber:
    """Speech-to-text transcriber powered by OpenAI Whisper."""

    def __init__(self) -> None:
        settings = get_settings()
        self.model = whisper.load_model(settings.whisper_model_size)

    def transcribe(self, audio_path: Path) -> str:
        """Transcribe audio and return plain text transcript."""

        result = self.model.transcribe(str(audio_path))
        return result.get("text", "").strip()
