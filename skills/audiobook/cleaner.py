"""Phase 2a: Clean and normalize extracted text for TTS."""

import logging
import re
from collections import Counter

from models import Page

logger = logging.getLogger(__name__)

# Abbreviation replacements by language
ABBREVIATIONS: dict[str, dict[str, str]] = {
    "es": {
        r"\bpág\.": "página",
        r"\bpágs\.": "páginas",
        r"\bnº\b": "número",
        r"\bNº\b": "Número",
        r"\bSr\.": "Señor",
        r"\bSra\.": "Señora",
        r"\bSres\.": "Señores",
        r"\bDr\.": "Doctor",
        r"\bDra\.": "Doctora",
        r"\bProf\.": "Profesor",
        r"\bUd\.": "Usted",
        r"\bUds\.": "Ustedes",
        r"\bVd\.": "Usted",
        r"\bVds\.": "Ustedes",
        r"\betc\.": "etcétera",
        r"\bEd\.": "Editorial",
        r"\bvol\.": "volumen",
        r"\bcap\.": "capítulo",
        r"\bfig\.": "figura",
        r"\bej\.": "ejemplo",
        r"\btel\.": "teléfono",
        r"\bapdo\.": "apartado",
    },
    "en": {
        r"\bDr\.": "Doctor",
        r"\bMr\.": "Mister",
        r"\bMrs\.": "Misses",
        r"\bMs\.": "Miss",
        r"\bProf\.": "Professor",
        r"\betc\.": "etcetera",
        r"\bvol\.": "volume",
        r"\bch\.": "chapter",
        r"\bfig\.": "figure",
        r"\bno\.": "number",
        r"\bpp\.": "pages",
        r"\bed\.": "edition",
    },
}

# Pattern to match URLs
URL_PATTERN = re.compile(
    r"https?://[^\s\)\]\}>\"']+|www\.[^\s\)\]\}>\"']+", re.IGNORECASE
)

# Pattern to match bibliographic references like [1], [2, 3], (Author, 2020)
BIBREF_PATTERN = re.compile(
    r"\[\d+(?:\s*[,;–-]\s*\d+)*\]"
    r"|\(\w+(?:\s+(?:et\s+al\.?|y\s+\w+))?,\s*\d{4}[a-z]?\)"
)


def clean_text(
    pages: list[Page],
    language: str = "es",
    remove_urls: bool = True,
) -> list[Page]:
    """Apply all cleaning steps to the extracted pages."""
    if not pages:
        return pages

    # Step 1: Detect and remove repetitive headers/footers across pages
    headers_footers = _detect_repetitive_lines(pages)
    if headers_footers:
        logger.info(
            "Detected %d repetitive header/footer patterns to remove.",
            len(headers_footers),
        )

    cleaned_pages = []
    for page in pages:
        text = page.text

        # Remove repetitive headers/footers
        text = _remove_repetitive_lines(text, headers_footers)

        # Remove standalone page numbers
        text = _remove_page_numbers(text)

        # Rejoin hyphenated words across line breaks
        text = _rejoin_hyphenated_words(text)

        # Normalize typographic characters
        text = _normalize_typography(text)

        # Expand abbreviations
        text = _expand_abbreviations(text, language)

        # Remove URLs and bibliographic references
        if remove_urls:
            text = _remove_urls_and_refs(text)

        # Collapse excessive whitespace
        text = _collapse_whitespace(text)

        if text.strip():
            cleaned_pages.append(Page(number=page.number, text=text.strip()))

    logger.info("Cleaned %d pages (started with %d).", len(cleaned_pages), len(pages))
    return cleaned_pages


def _detect_repetitive_lines(pages: list[Page], threshold: float = 0.3) -> set[str]:
    """Detect lines that appear in >threshold fraction of pages (likely headers/footers)."""
    line_counts: Counter[str] = Counter()
    total_pages = len(pages)

    for page in pages:
        lines = page.text.strip().split("\n")
        candidate_lines: set[str] = set()

        for line in lines[:3] + lines[-3:]:
            stripped = line.strip()
            if stripped and len(stripped) < 80:
                candidate_lines.add(stripped)

        for line in candidate_lines:
            line_counts[line] += 1

    return {
        line
        for line, count in line_counts.items()
        if count / total_pages > threshold and total_pages > 2
    }


def _remove_repetitive_lines(text: str, repetitive: set[str]) -> str:
    """Remove lines identified as repetitive headers/footers."""
    if not repetitive:
        return text
    lines = text.split("\n")
    return "\n".join(line for line in lines if line.strip() not in repetitive)


def _remove_page_numbers(text: str) -> str:
    """Remove lines that are only a page number (1-4 digits)."""
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if re.fullmatch(r"\d{1,4}", stripped):
            continue
        if re.fullmatch(r"[-–—.·\s]*\d{1,4}[-–—.·\s]*", stripped):
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def _rejoin_hyphenated_words(text: str) -> str:
    """Rejoin words split across lines with a hyphen."""
    return re.sub(r"(\w)-\n(\s*)([a-záéíóúüñ])", r"\1\3", text)


def _normalize_typography(text: str) -> str:
    """Normalize typographic characters for better TTS pronunciation."""
    replacements = {
        "\u201c": '"',
        "\u201d": '"',
        "\u2018": "'",
        "\u2019": "'",
        "\u00ab": '"',
        "\u00bb": '"',
        "\u2014": ", ",
        "\u2013": ", ",
        "\u2026": "...",
        "\u00a0": " ",
        "\u200b": "",
        "\u200c": "",
        "\u200d": "",
        "\ufeff": "",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def _expand_abbreviations(text: str, language: str) -> str:
    """Expand common abbreviations for better TTS pronunciation."""
    abbrevs = ABBREVIATIONS.get(language, {})
    for pattern, replacement in abbrevs.items():
        text = re.sub(pattern, replacement, text)
    return text


def _remove_urls_and_refs(text: str) -> str:
    """Remove URLs and bibliographic references."""
    text = URL_PATTERN.sub("", text)
    text = BIBREF_PATTERN.sub("", text)
    return text


def _collapse_whitespace(text: str) -> str:
    """Collapse excessive whitespace and blank lines."""
    text = re.sub(r"[^\S\n]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text
