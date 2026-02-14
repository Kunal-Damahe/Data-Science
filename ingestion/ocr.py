"""OCR extraction from video frames."""

from pathlib import Path
from typing import Iterable, List


class OCRExtractor:
    """OCR adapter using easyOCR (optional)."""

    def __init__(self, enabled: bool = True) -> None:
        self.enabled = enabled
        self.reader = None
        if enabled:
            try:
                import easyocr

                self.reader = easyocr.Reader(["en"], gpu=False)
            except ImportError:
                self.enabled = False

    def extract_text(self, frame_paths: Iterable[Path]) -> str:
        """Run OCR on a list of frames and return concatenated text."""

        if not self.enabled or self.reader is None:
            return ""

        snippets: List[str] = []
        for frame_path in frame_paths:
            result = self.reader.readtext(str(frame_path), detail=0)
            if result:
                snippets.append(" ".join(result))
        return "\n".join(snippets)
