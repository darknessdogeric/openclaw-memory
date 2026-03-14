"""Phase 3: Text-to-speech synthesis using piper TTS engine."""

import io
import logging
import re
import wave
from pathlib import Path

from models import Chapter, ChapterAudio

logger = logging.getLogger(__name__)

# Default models per language: (model_filename, speaker_id)
DEFAULT_MODELS: dict[str, tuple[str, int | None]] = {
    "es": ("es_ES-sharvard-medium.onnx", 1),
    "en": ("en_GB-cori-high.onnx", None),
}


def get_default_model(language: str) -> tuple[str, int | None]:
    """Get the default piper model and speaker ID for a language.

    Args:
        language: Language code ('es' or 'en').

    Returns:
        Tuple of (model_filename, speaker_id). speaker_id may be None
        for single-speaker models.
    """
    if language not in DEFAULT_MODELS:
        raise ValueError(
            f"No default model for language '{language}'. "
            f"Available: {', '.join(DEFAULT_MODELS.keys())}"
        )
    return DEFAULT_MODELS[language]


def load_voice(model_path: str | Path, speaker_id: int | None = None):
    """Load a piper voice model.

    Args:
        model_path: Path to the .onnx model file.
        speaker_id: Optional speaker ID for multi-speaker models.

    Returns:
        PiperVoice instance ready for synthesis.
    """
    from piper import PiperVoice

    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(f"Piper model not found: {model_path}")

    json_path = model_path.with_suffix(".onnx.json")
    if not json_path.exists():
        raise FileNotFoundError(
            f"Piper model config not found: {json_path}. "
            "The .onnx.json file must be next to the .onnx file."
        )

    logger.info("Loading piper model: %s", model_path.name)
    voice = PiperVoice.load(str(model_path))
    return voice


def normalize_initials(text: str) -> str:
    """Remove periods from initials/acronyms so TTS spells them without sentence pauses.

    J.G. Ballard -> J G Ballard, A.C.M.E. -> A C M E
    """
    def _strip_dots(m: re.Match) -> str:
        return m.group(0).replace(".", " ").strip()

    # Chain of 2+ initials: J.G., A.C.M.E.
    text = re.sub(r'\b(?:[A-ZÁÉÍÓÚÜÑ]\.){2,}', _strip_dots, text)
    # Single initial before a capitalized word: K. Le Guin
    text = re.sub(r'\b([A-ZÁÉÍÓÚÜÑ])\.(?=\s+[A-ZÁÉÍÓÚÜÑ])', r'\1', text)
    return text


DEFAULT_PAUSE_MS = 600
COMMA_PAUSE_MS = 300
SEMICOLON_PAUSE_MS = 600
PARAGRAPH_PAUSE_MS = 1000


def _split_clauses(text: str) -> list[tuple[str, int]]:
    """Split text into clauses on punctuation, returning (clause, pause_ms) pairs.

    Each clause keeps its trailing punctuation. The pause_ms indicates how
    much silence to insert AFTER that clause:
    - Period, ! , ? -> DEFAULT_PAUSE_MS (600ms)
    - Semicolon, colon -> SEMICOLON_PAUSE_MS (600ms)
    - Comma -> COMMA_PAUSE_MS (300ms)
    - Last clause -> 0 (no trailing pause)
    """
    # Split keeping the delimiter attached to the preceding text
    # Matches: . ! ? ; : ,  followed by whitespace
    parts = re.split(r'(?<=[.!?;:,])\s+', text)
    parts = [p.strip() for p in parts if p.strip()]

    result: list[tuple[str, int]] = []
    for i, part in enumerate(parts):
        if i == len(parts) - 1:
            pause = 0
        elif part.endswith((",",)):
            pause = COMMA_PAUSE_MS
        elif part.endswith((";", ":")):
            pause = SEMICOLON_PAUSE_MS
        else:
            # . ! ? or anything else
            pause = DEFAULT_PAUSE_MS
        result.append((part, pause))
    return result


def _silence_bytes(ms: int, sample_rate: int = 22050) -> bytes:
    """Generate raw PCM int16 silence of the given duration."""
    n_samples = int(sample_rate * ms / 1000)
    return b"\x00\x00" * n_samples


def _paragraph_silence_bytes(sample_rate: int = 22050) -> bytes:
    """Generate silence for paragraph breaks."""
    return _silence_bytes(PARAGRAPH_PAUSE_MS, sample_rate)


def _synthesize_to_pcm(text: str, voice, syn_config) -> bytes:
    """Synthesize text and return raw PCM int16 bytes (no WAV header)."""
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        voice.synthesize_wav(text, w, syn_config=syn_config)
    buf.seek(44)  # skip WAV header
    return buf.read()


def synthesize_chapter(text: str, voice, output_path: str | Path,
                       speaker_id: int | None = None,
                       pause_ms: int = DEFAULT_PAUSE_MS) -> Path:
    """Synthesize a single chapter's text to a WAV file.

    Splits text into sentences and inserts silence between them for
    more natural pacing (piper doesn't pause enough on periods alone).

    Args:
        text: The chapter text to synthesize.
        voice: A loaded PiperVoice instance.
        output_path: Path where the WAV file will be written.
        speaker_id: Optional speaker ID for multi-speaker models.
        pause_ms: Milliseconds of silence between sentences.

    Returns:
        Path to the generated WAV file.
    """
    output_path = Path(output_path)

    # Normalize initials for cleaner pronunciation
    text = normalize_initials(text)

    # Build synthesis config with optional speaker ID
    syn_config = None
    if speaker_id is not None:
        from piper.config import SynthesisConfig
        syn_config = SynthesisConfig(speaker_id=speaker_id)

    # Split into paragraphs, then clauses, synthesize each with silence gaps
    paragraphs = re.split(r'\n\s*\n', text)
    chunks: list[bytes] = []
    paragraph_silence = _paragraph_silence_bytes()

    for pi, paragraph in enumerate(paragraphs):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        clauses = _split_clauses(paragraph)
        for clause_text, clause_pause in clauses:
            pcm = _synthesize_to_pcm(clause_text, voice, syn_config)
            if pcm:
                chunks.append(pcm)
                if clause_pause > 0:
                    chunks.append(_silence_bytes(clause_pause))
        # Add paragraph pause between paragraphs
        if pi < len(paragraphs) - 1 and chunks:
            chunks.append(paragraph_silence)

    if not chunks:
        raise RuntimeError("Piper produced no audio output")

    # Write combined PCM as WAV
    combined = b"".join(chunks)
    audio_buffer = io.BytesIO()
    with wave.open(audio_buffer, "wb") as wav_out:
        wav_out.setnchannels(1)
        wav_out.setsampwidth(2)
        wav_out.setframerate(22050)
        wav_out.writeframes(combined)

    output_path.write_bytes(audio_buffer.getvalue())
    logger.debug("WAV written: %s (%d bytes)", output_path, output_path.stat().st_size)
    return output_path


def synthesize_chapters(
    chapters: list[Chapter],
    model_path: str | Path,
    speaker_id: int | None = None,
    temp_dir: str | Path | None = None,
) -> list[ChapterAudio]:
    """Synthesize all chapters to WAV audio files.

    Args:
        chapters: List of chapters to synthesize.
        model_path: Path to the piper .onnx model.
        speaker_id: Optional speaker ID for multi-speaker models.
        temp_dir: Directory for output WAV files.

    Returns:
        List of ChapterAudio objects with paths to generated WAV files.
    """
    import tempfile

    if temp_dir is None:
        temp_dir = Path(tempfile.mkdtemp(prefix="audiobook_tts_"))
    else:
        temp_dir = Path(temp_dir)
        temp_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Loading piper model...")
    voice = load_voice(model_path, speaker_id)

    total_words = sum(len(ch.text.split()) for ch in chapters)
    processed_words = 0
    results: list[ChapterAudio] = []
    errors: list[str] = []

    for i, chapter in enumerate(chapters, start=1):
        word_count = len(chapter.text.split())
        pct = (processed_words / total_words * 100) if total_words > 0 else 0

        logger.info(
            "[%d/%d] %s (%d words) - %.0f%% complete",
            i, len(chapters), chapter.title, word_count, pct,
        )

        output_file = temp_dir / f"chapter_{i:03d}.wav"

        try:
            synthesize_chapter(chapter.text, voice, output_file, speaker_id)
            results.append(ChapterAudio(
                title=chapter.title,
                audio_path=str(output_file),
            ))
        except Exception as e:
            error_msg = f"TTS error for '{chapter.title}': {e}"
            logger.error(error_msg)
            errors.append(error_msg)

        processed_words += word_count

    if errors:
        logger.warning(
            "%d chapter(s) failed during TTS. Successfully processed %d/%d.",
            len(errors), len(results), len(chapters),
        )

    if not results:
        raise RuntimeError("All chapters failed during TTS synthesis.")

    logger.info("TTS complete: %d audio files generated.", len(results))
    return results


def list_voices(models_dir: str | Path) -> list[str]:
    """List available piper voice models in a directory.

    Args:
        models_dir: Directory containing .onnx model files.

    Returns:
        List of model filenames (without path).
    """
    models_dir = Path(models_dir)
    if not models_dir.exists():
        return []
    return sorted(p.name for p in models_dir.glob("*.onnx"))
