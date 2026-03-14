"""Tests for the assembler module."""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from assembler import (
    _escape_ffmeta,
    _write_ffmetadata,
    check_ffmpeg_available,
)
from models import BookMetadata, ChapterAudio


class TestCheckFfmpegAvailable:
    @patch("shutil.which", return_value=None)
    def test_ffmpeg_not_found(self, mock_which):
        with pytest.raises(RuntimeError, match="ffmpeg is not installed"):
            check_ffmpeg_available()

    @patch("shutil.which", side_effect=lambda cmd: "/usr/bin/ffmpeg" if cmd == "ffmpeg" else None)
    def test_ffprobe_not_found(self, mock_which):
        with pytest.raises(RuntimeError, match="ffprobe is not installed"):
            check_ffmpeg_available()

    @patch("shutil.which", return_value="/usr/bin/ffmpeg")
    def test_both_found(self, mock_which):
        # Should not raise
        check_ffmpeg_available()


class TestEscapeFfmeta:
    def test_escapes_equals(self):
        assert _escape_ffmeta("a=b") == "a\\=b"

    def test_escapes_semicolon(self):
        assert _escape_ffmeta("a;b") == "a\\;b"

    def test_escapes_hash(self):
        assert _escape_ffmeta("a#b") == "a\\#b"

    def test_no_special_chars(self):
        assert _escape_ffmeta("Simple Title") == "Simple Title"


class TestWriteFfmetadata:
    def test_writes_metadata_file(self):
        chapters = [
            ChapterAudio(title="Ch 1", audio_path="/tmp/ch1.wav", duration_ms=60000),
            ChapterAudio(title="Ch 2", audio_path="/tmp/ch2.wav", duration_ms=120000),
        ]
        metadata = BookMetadata(title="Test Book", author="Author")

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "ffmetadata.txt"
            _write_ffmetadata(chapters, metadata, output)

            content = output.read_text()
            assert ";FFMETADATA1" in content
            assert "title=Test Book" in content
            assert "artist=Author" in content
            assert "[CHAPTER]" in content
            assert "START=0" in content
            assert "END=60000" in content
            assert "START=60000" in content
            assert "END=180000" in content

    def test_chapter_timing_is_cumulative(self):
        chapters = [
            ChapterAudio(title="A", audio_path="/tmp/a.wav", duration_ms=10000),
            ChapterAudio(title="B", audio_path="/tmp/b.wav", duration_ms=20000),
            ChapterAudio(title="C", audio_path="/tmp/c.wav", duration_ms=30000),
        ]
        metadata = BookMetadata(title="T", author="A")

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "meta.txt"
            _write_ffmetadata(chapters, metadata, output)

            content = output.read_text()
            # Chapter B should start at 10000 and end at 30000
            assert "START=10000" in content
            assert "END=30000" in content
            # Chapter C should start at 30000 and end at 60000
            assert "START=30000" in content
            assert "END=60000" in content


class TestInstallMessage:
    @patch("shutil.which", return_value=None)
    def test_error_mentions_apt_get(self, mock_which):
        """Verify the error message says apt-get, not brew."""
        with pytest.raises(RuntimeError, match="apt-get"):
            check_ffmpeg_available()
