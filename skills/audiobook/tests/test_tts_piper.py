"""Tests for the piper TTS module."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tts_piper import (
    COMMA_PAUSE_MS,
    DEFAULT_MODELS,
    DEFAULT_PAUSE_MS,
    SEMICOLON_PAUSE_MS,
    _silence_bytes,
    _split_clauses,
    get_default_model,
    list_voices,
    normalize_initials,
    synthesize_chapter,
    synthesize_chapters,
)
from models import Chapter


class TestNormalizeInitials:
    def test_double_initials(self):
        result = normalize_initials("J.G. Ballard")
        assert result == "J G Ballard"

    def test_triple_initials(self):
        result = normalize_initials("A.C.M.E. Corp")
        assert result == "A C M E Corp"

    def test_single_initial_before_name(self):
        result = normalize_initials("Ursula K. Le Guin")
        assert result == "Ursula K Le Guin"

    def test_no_initials(self):
        text = "This is normal text without initials."
        result = normalize_initials(text)
        assert result == text

    def test_preserves_sentence_periods(self):
        text = "This is a sentence. And another one."
        result = normalize_initials(text)
        assert result == text

    def test_spanish_initials(self):
        result = normalize_initials("Á.É. García")
        assert result == "Á É García"


class TestGetDefaultModel:
    def test_spanish(self):
        model, speaker = get_default_model("es")
        assert model == "es_ES-sharvard-medium.onnx"
        assert speaker == 1

    def test_english(self):
        model, speaker = get_default_model("en")
        assert model == "en_GB-cori-high.onnx"
        assert speaker is None

    def test_unknown_language(self):
        with pytest.raises(ValueError, match="No default model"):
            get_default_model("fr")


class TestListVoices:
    def test_lists_onnx_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "model_a.onnx").touch()
            (Path(tmpdir) / "model_b.onnx").touch()
            (Path(tmpdir) / "model_a.onnx.json").touch()  # config, should not appear
            voices = list_voices(tmpdir)
            assert voices == ["model_a.onnx", "model_b.onnx"]

    def test_empty_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            voices = list_voices(tmpdir)
            assert voices == []

    def test_nonexistent_dir(self):
        voices = list_voices("/nonexistent/path")
        assert voices == []


class TestSplitClauses:
    def test_sentences_get_default_pause(self):
        result = _split_clauses("First. Second. Third.")
        assert result == [
            ("First.", DEFAULT_PAUSE_MS),
            ("Second.", DEFAULT_PAUSE_MS),
            ("Third.", 0),
        ]

    def test_commas_get_comma_pause(self):
        result = _split_clauses("Hola, mundo, aqui.")
        assert result == [
            ("Hola,", COMMA_PAUSE_MS),
            ("mundo,", COMMA_PAUSE_MS),
            ("aqui.", 0),
        ]

    def test_semicolons_get_semicolon_pause(self):
        result = _split_clauses("Primero; segundo; tercero.")
        assert result == [
            ("Primero;", SEMICOLON_PAUSE_MS),
            ("segundo;", SEMICOLON_PAUSE_MS),
            ("tercero.", 0),
        ]

    def test_mixed_punctuation(self):
        result = _split_clauses("Hola, mundo; esto es. Genial!")
        assert result == [
            ("Hola,", COMMA_PAUSE_MS),
            ("mundo;", SEMICOLON_PAUSE_MS),
            ("esto es.", DEFAULT_PAUSE_MS),
            ("Genial!", 0),
        ]

    def test_single_clause(self):
        result = _split_clauses("Just one clause.")
        assert result == [("Just one clause.", 0)]

    def test_empty_string(self):
        result = _split_clauses("")
        assert result == []


class TestSilenceBytes:
    def test_600ms_silence(self):
        silence = _silence_bytes(600, sample_rate=22050)
        expected_samples = int(22050 * 600 / 1000)
        assert len(silence) == expected_samples * 2  # 2 bytes per sample

    def test_zero_silence(self):
        silence = _silence_bytes(0)
        assert len(silence) == 0

    def test_pause_constants(self):
        assert DEFAULT_PAUSE_MS == 600
        assert COMMA_PAUSE_MS == 300
        assert SEMICOLON_PAUSE_MS == 600


class TestSynthesizeChapter:
    @patch("tts_piper.load_voice")
    def test_synthesize_writes_wav(self, mock_load_voice):
        """Test that synthesize_chapter writes a WAV file using mocked piper."""
        mock_voice = MagicMock()

        def fake_synthesize_wav(text, wav_out, syn_config=None):
            wav_out.setnchannels(1)
            wav_out.setsampwidth(2)
            wav_out.setframerate(22050)
            wav_out.writeframes(b"\x00\x00" * 1000)

        mock_voice.synthesize_wav.side_effect = fake_synthesize_wav

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test.wav"
            result = synthesize_chapter(
                "Hello world", mock_voice, output_path
            )
            assert result == output_path
            assert output_path.exists()
            assert output_path.stat().st_size > 0

    @patch("tts_piper.load_voice")
    def test_synthesize_empty_output_raises(self, mock_load_voice):
        """Test that empty output raises an error."""
        mock_voice = MagicMock()

        def fake_synthesize_wav_empty(text, wav_out, syn_config=None):
            # Set params but write no frames — simulates empty audio
            wav_out.setnchannels(1)
            wav_out.setsampwidth(2)
            wav_out.setframerate(22050)

        mock_voice.synthesize_wav.side_effect = fake_synthesize_wav_empty

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test.wav"
            with pytest.raises(RuntimeError, match="no audio"):
                synthesize_chapter("Hello", mock_voice, output_path)


class TestSynthesizeChapters:
    @patch("tts_piper.load_voice")
    def test_synthesize_multiple_chapters(self, mock_load_voice):
        """Test synthesizing multiple chapters with mocked piper."""
        mock_voice = MagicMock()

        def fake_synthesize_wav(text, wav_out, syn_config=None):
            wav_out.setnchannels(1)
            wav_out.setsampwidth(2)
            wav_out.setframerate(22050)
            wav_out.writeframes(b"\x00\x00" * 500)

        mock_voice.synthesize_wav.side_effect = fake_synthesize_wav
        mock_load_voice.return_value = mock_voice

        chapters = [
            Chapter(title="Chapter 1", text="First chapter text.", start_page=1),
            Chapter(title="Chapter 2", text="Second chapter text.", start_page=5),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            model_path = Path(tmpdir) / "fake_model.onnx"
            model_path.touch()
            json_path = model_path.with_suffix(".onnx.json")
            json_path.touch()

            results = synthesize_chapters(
                chapters, model_path=model_path, temp_dir=tmpdir
            )
            assert len(results) == 2
            assert results[0].title == "Chapter 1"
            assert results[1].title == "Chapter 2"
            for r in results:
                assert Path(r.audio_path).exists()
