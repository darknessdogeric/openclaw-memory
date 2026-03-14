"""Phase 2b: Detect and segment chapters from cleaned text."""

import json
import logging
import re
from pathlib import Path

from models import Chapter, Page

logger = logging.getLogger(__name__)

# Patterns for chapter detection, ordered by specificity
CHAPTER_PATTERNS: list[re.Pattern[str]] = [
    # "Capítulo N" / "Chapter N" with optional title
    re.compile(
        r"^\s*(cap[ií]tulo|chapter)\s+(\d+|[IVXLC]+)"
        r"(?:\s*[:.\-–—]\s*(.+))?$",
        re.IGNORECASE | re.MULTILINE,
    ),
    # "Parte N" / "Part N" / "Sección N" / "Section N"
    re.compile(
        r"^\s*(parte|part|secci[oó]n|section)\s+(\d+|[IVXLC]+)"
        r"(?:\s*[:.\-–—]\s*(.+))?$",
        re.IGNORECASE | re.MULTILINE,
    ),
    # Standalone Roman numerals on their own line
    re.compile(
        r"^\s*([IVXLC]{1,10})\s*$",
        re.MULTILINE,
    ),
    # All-caps lines surrounded by blank lines (likely section titles)
    re.compile(
        r"(?<=\n\n)\s*([A-ZÁÉÍÓÚÜÑ][A-ZÁÉÍÓÚÜÑ\s,]{4,60})\s*(?=\n\n)",
    ),
]


def detect_chapters(
    pages: list[Page],
    pages_per_chapter: int = 10,
    chapters_json: str | Path | None = None,
) -> list[Chapter]:
    """Detect chapters from pages using heuristics or manual definition."""
    if not pages:
        return []

    # Strategy 1: Manual JSON
    if chapters_json is not None:
        logger.info("Using manual chapter definitions from JSON.")
        return _chapters_from_json(pages, chapters_json)

    # Strategy 2: Pattern-based detection
    chapters = _detect_by_patterns(pages)
    if chapters:
        logger.info("Detected %d chapters by text patterns.", len(chapters))
        return chapters

    # Strategy 3: Fallback by pages
    logger.info(
        "No chapter patterns detected. Using fallback: %d pages per chapter.",
        pages_per_chapter,
    )
    return _chapters_by_page_count(pages, pages_per_chapter)


def _chapters_from_json(pages: list[Page], json_path: str | Path) -> list[Chapter]:
    """Build chapters from a manual JSON definition."""
    json_path = Path(json_path)
    with open(json_path) as f:
        definitions = json.load(f)

    page_map = {p.number: p.text for p in pages}
    chapters = []

    for defn in definitions:
        title = defn["title"]
        start = defn["start_page"]
        end = defn["end_page"]
        text_parts = [
            page_map[n] for n in range(start, end + 1) if n in page_map
        ]
        if text_parts:
            chapters.append(Chapter(
                title=title,
                text="\n\n".join(text_parts),
                start_page=start,
            ))

    return chapters


def _detect_by_patterns(pages: list[Page]) -> list[Chapter]:
    """Detect chapters by scanning text for common heading patterns."""
    full_text = ""
    page_offsets: list[tuple[int, int, int]] = []

    for page in pages:
        start = len(full_text)
        full_text += page.text + "\n\n"
        page_offsets.append((start, len(full_text), page.number))

    markers: list[tuple[int, str]] = []

    for pattern in CHAPTER_PATTERNS[:3]:
        for match in pattern.finditer(full_text):
            pos = match.start()
            title = _build_title_from_match(match)
            markers.append((pos, title))

    if not markers:
        for match in CHAPTER_PATTERNS[3].finditer(full_text):
            pos = match.start()
            title = _build_title_from_match(match)
            markers.append((pos, title))

    if not markers:
        return []

    markers.sort(key=lambda m: m[0])
    markers = _deduplicate_markers(markers, min_distance=10)

    strong_pattern = re.compile(
        r"cap[ií]tulo|chapter|parte|part|secci[oó]n|section", re.IGNORECASE
    )
    if len(markers) < 2:
        if not strong_pattern.search(markers[0][1]):
            return []

    chapters = []
    for i, (pos, title) in enumerate(markers):
        if i + 1 < len(markers):
            end_pos = markers[i + 1][0]
        else:
            end_pos = len(full_text)

        chapter_text = full_text[pos:end_pos].strip()
        lines = chapter_text.split("\n", 1)
        if len(lines) > 1:
            chapter_text = lines[1].strip()

        start_page = _offset_to_page(pos, page_offsets)

        chapters.append(Chapter(
            title=title,
            text=chapter_text,
            start_page=start_page,
        ))

    if markers[0][0] > 200:
        preamble_text = full_text[: markers[0][0]].strip()
        if preamble_text:
            chapters.insert(0, Chapter(
                title="Introducción",
                text=preamble_text,
                start_page=pages[0].number,
            ))

    return chapters


def _build_title_from_match(match: re.Match[str]) -> str:
    """Build a chapter title from a regex match."""
    groups = match.groups()

    if len(groups) >= 3 and groups[2]:
        keyword = groups[0]
        number = groups[1]
        subtitle = groups[2].strip()
        return f"{keyword.title()} {number} - {subtitle}"
    elif len(groups) >= 2:
        keyword = groups[0]
        number = groups[1]
        if re.fullmatch(r"[IVXLC]+", keyword):
            return f"Capítulo {keyword}"
        return f"{keyword.title()} {number}"
    else:
        return match.group(0).strip().title()


def _offset_to_page(offset: int, page_offsets: list[tuple[int, int, int]]) -> int:
    """Find which page number corresponds to a text offset."""
    for start, end, page_num in page_offsets:
        if start <= offset < end:
            return page_num
    return page_offsets[-1][2] if page_offsets else 1


def _deduplicate_markers(
    markers: list[tuple[int, str]], min_distance: int = 100
) -> list[tuple[int, str]]:
    """Remove markers that are too close together."""
    if not markers:
        return markers

    deduped = [markers[0]]
    for pos, title in markers[1:]:
        if pos - deduped[-1][0] >= min_distance:
            deduped.append((pos, title))
        else:
            if len(title) > len(deduped[-1][1]):
                deduped[-1] = (pos, title)

    return deduped


def _chapters_by_page_count(pages: list[Page], pages_per_chapter: int) -> list[Chapter]:
    """Group pages into chapters by count (fallback strategy)."""
    chapters = []
    for i in range(0, len(pages), pages_per_chapter):
        chunk = pages[i : i + pages_per_chapter]
        chapter_num = (i // pages_per_chapter) + 1
        chapters.append(Chapter(
            title=f"Capítulo {chapter_num}",
            text="\n\n".join(p.text for p in chunk),
            start_page=chunk[0].number,
        ))
    return chapters
