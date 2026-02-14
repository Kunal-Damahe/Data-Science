"""Video ingestion utilities (upload and YouTube URL support)."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List

from config import get_settings


class VideoProcessor:
    """Handles video download, audio extraction, and frame extraction."""

    def __init__(self) -> None:
        self.settings = get_settings()

    def download_youtube_video(self, youtube_url: str) -> Path:
        """Download a YouTube video locally using yt-dlp and return the file path."""

        output_template = str(self.settings.upload_dir / "%(id)s.%(ext)s")
        cmd = [
            "yt-dlp",
            "-f",
            "mp4/bestvideo+bestaudio/best",
            "-o",
            output_template,
            youtube_url,
        ]
        subprocess.run(cmd, check=True)

        # Grab most recently modified downloaded file as output.
        candidates = sorted(self.settings.upload_dir.glob("*"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not candidates:
            raise FileNotFoundError("yt-dlp did not produce an output file.")
        return candidates[0]

    def extract_audio(self, video_path: Path) -> Path:
        """Extract mono 16k WAV audio for Whisper from a video using ffmpeg."""

        output_audio = self.settings.audio_dir / f"{video_path.stem}.wav"
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-ac",
            "1",
            "-ar",
            "16000",
            str(output_audio),
        ]
        subprocess.run(cmd, check=True)
        return output_audio

    def extract_frames(self, video_path: Path) -> List[Path]:
        """Extract frames every N seconds for OCR processing."""

        frame_dir = self.settings.frame_dir / video_path.stem
        frame_dir.mkdir(parents=True, exist_ok=True)
        output_pattern = str(frame_dir / "frame_%05d.jpg")

        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-vf",
            f"fps=1/{self.settings.frame_extract_every_n_seconds}",
            output_pattern,
        ]
        subprocess.run(cmd, check=True)

        frames = sorted(frame_dir.glob("*.jpg"))[: self.settings.max_frames_for_ocr]
        return frames
