"""Tests for the chapter detection module."""

import json
import tempfile
from pathlib import Path

import pytest

from chapters import (
    _chapters_by_page_count,
    _detect_by_patterns,
    detect_chapters,
)
from models import Page


class TestDetectByPatterns:
    def test_detects_capitulo_pattern(self):
        pages = [
            Page(number=1, text="Introducción del libro.\n\nAlgo de contexto."),
            Page(number=2, text="Capítulo 1: El comienzo\n\nContenido del cap 1."),
            Page(number=5, text="Capítulo 2: El desarrollo\n\nContenido del cap 2."),
        ]
        chapters = _detect_by_patterns(pages)
        assert len(chapters) >= 2
        assert any("1" in ch.title for ch in chapters)
        assert any("2" in ch.title for ch in chapters)

    def test_detects_chapter_english(self):
        pages = [
            Page(number=1, text="Chapter 1: The Beginning\n\nContent of chapter 1."),
            Page(number=5, text="Chapter 2: The Middle\n\nContent of chapter 2."),
            Page(number=10, text="Chapter 3: The End\n\nContent of chapter 3."),
        ]
        chapters = _detect_by_patterns(pages)
        assert len(chapters) >= 3

    def test_detects_parte_pattern(self):
        pages = [
            Page(number=1, text="Parte 1\n\nContenido de la primera parte."),
            Page(number=10, text="Parte 2\n\nContenido de la segunda parte."),
        ]
        chapters = _detect_by_patterns(pages)
        assert len(chapters) >= 2

    def test_no_patterns_returns_empty(self):
        pages = [
            Page(number=1, text="Just some regular text without any chapter markers."),
            Page(number=2, text="More regular text here."),
        ]
        chapters = _detect_by_patterns(pages)
        assert len(chapters) == 0

    def test_creates_preamble_for_content_before_first_chapter(self):
        pages = [
            Page(
                number=1,
                text=(
                    "This is a long preamble that contains enough text "
                    "to be considered significant content before the first "
                    "chapter marker appears in the document. It should be "
                    "captured as an introduction chapter."
                ),
            ),
            Page(number=3, text="Capítulo 1: Inicio\n\nContenido del capítulo."),
            Page(number=6, text="Capítulo 2: Final\n\nContenido final."),
        ]
        chapters = _detect_by_patterns(pages)
        assert len(chapters) >= 2


class TestChaptersByPageCount:
    def test_groups_by_page_count(self):
        pages = [Page(number=i, text=f"Content page {i}") for i in range(1, 21)]
        chapters = _chapters_by_page_count(pages, pages_per_chapter=5)
        assert len(chapters) == 4
        assert chapters[0].title == "Capítulo 1"
        assert chapters[3].title == "Capítulo 4"
        assert chapters[0].start_page == 1

    def test_handles_remainder(self):
        pages = [Page(number=i, text=f"Content page {i}") for i in range(1, 8)]
        chapters = _chapters_by_page_count(pages, pages_per_chapter=3)
        assert len(chapters) == 3
        assert chapters[2].start_page == 7

    def test_single_chapter(self):
        pages = [Page(number=i, text=f"Content page {i}") for i in range(1, 4)]
        chapters = _chapters_by_page_count(pages, pages_per_chapter=10)
        assert len(chapters) == 1


class TestDetectChapters:
    def test_uses_json_when_provided(self):
        pages = [
            Page(number=1, text="Page 1 content."),
            Page(number=2, text="Page 2 content."),
            Page(number=3, text="Page 3 content."),
        ]
        chapters_def = [
            {"title": "Prólogo", "start_page": 1, "end_page": 2},
            {"title": "Capítulo Uno", "start_page": 3, "end_page": 3},
        ]

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(chapters_def, f)
            json_path = f.name

        try:
            chapters = detect_chapters(pages, chapters_json=json_path)
            assert len(chapters) == 2
            assert chapters[0].title == "Prólogo"
            assert chapters[1].title == "Capítulo Uno"
            assert "Page 1" in chapters[0].text
            assert "Page 3" in chapters[1].text
        finally:
            Path(json_path).unlink()

    def test_falls_back_to_page_count(self):
        pages = [
            Page(number=i, text=f"Regular content on page {i}.")
            for i in range(1, 11)
        ]
        chapters = detect_chapters(pages, pages_per_chapter=3)
        assert len(chapters) == 4

    def test_empty_pages(self):
        chapters = detect_chapters([])
        assert chapters == []

    def test_pattern_detection_takes_priority(self):
        pages = [
            Page(number=1, text="Capítulo 1: Primero\n\nContenido uno."),
            Page(number=5, text="Capítulo 2: Segundo\n\nContenido dos."),
        ]
        chapters = detect_chapters(pages, pages_per_chapter=1)
        assert any("1" in ch.title or "Primero" in ch.title for ch in chapters)
