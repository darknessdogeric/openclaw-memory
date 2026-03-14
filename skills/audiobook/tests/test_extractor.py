"""Tests for the extractor module."""

import tempfile
from pathlib import Path

import pytest

from extractor import extract, extract_from_text, TEXT_PAGE_SIZE
from models import Page


class TestExtractFromText:
    def test_short_text_single_page(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Hello, this is a short text.")
            f.flush()
            pages = extract_from_text(f.name)
        assert len(pages) == 1
        assert pages[0].number == 1
        assert "Hello" in pages[0].text
        Path(f.name).unlink()

    def test_long_text_multiple_pages(self):
        # Create text longer than TEXT_PAGE_SIZE
        paragraphs = [f"Paragraph {i}. " + "x" * 500 for i in range(20)]
        content = "\n\n".join(paragraphs)
        assert len(content) > TEXT_PAGE_SIZE

        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(content)
            f.flush()
            pages = extract_from_text(f.name)
        assert len(pages) > 1
        # Each page should be roughly TEXT_PAGE_SIZE or less
        for page in pages:
            assert len(page.text) <= TEXT_PAGE_SIZE + 600  # some tolerance for paragraph boundary
        Path(f.name).unlink()

    def test_empty_file_raises(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("   \n\n   ")
            f.flush()
            with pytest.raises(ValueError, match="empty"):
                extract_from_text(f.name)
        Path(f.name).unlink()

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            extract_from_text("/nonexistent/file.txt")


class TestExtractDispatch:
    def test_txt_dispatch(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Some text content here.")
            f.flush()
            pages = extract(f.name)
        assert len(pages) >= 1
        Path(f.name).unlink()

    def test_unsupported_format(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".doc", delete=False) as f:
            f.write("data")
            f.flush()
            with pytest.raises(ValueError, match="Unsupported"):
                extract(f.name)
        Path(f.name).unlink()

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            extract("/nonexistent/file.pdf")
