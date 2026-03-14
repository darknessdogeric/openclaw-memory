"""Data models for the audiobook pipeline."""

from dataclasses import dataclass, field


@dataclass
class Page:
    """A single page extracted from the PDF."""
    number: int
    text: str


@dataclass
class Chapter:
    """A detected or manually defined chapter."""
    title: str
    text: str
    start_page: int


@dataclass
class BookMetadata:
    """Metadata for the output audiobook."""
    title: str = "Untitled"
    author: str = "Desconocido"
    cover_path: str | None = None
    language: str = "es"


@dataclass
class ChapterAudio:
    """A chapter with its associated audio file and duration."""
    title: str
    audio_path: str
    duration_ms: int = 0


@dataclass
class PipelineResult:
    """Summary of the full pipeline execution."""
    output_path: str
    num_chapters: int
    total_duration_ms: int
    file_size_bytes: int
    errors: list[str] = field(default_factory=list)
