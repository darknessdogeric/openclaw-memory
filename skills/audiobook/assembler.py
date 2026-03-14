"""Phase 4: Assemble chapter audio files into an M4B audiobook with ffmpeg."""

import json
import logging
import shutil
import subprocess
from pathlib import Path

from models import BookMetadata, ChapterAudio

logger = logging.getLogger(__name__)


def check_ffmpeg_available() -> None:
    """Check that ffmpeg and ffprobe are available."""
    if not shutil.which("ffmpeg"):
        raise RuntimeError(
            "ffmpeg is not installed. Install it with: apt-get install ffmpeg"
        )
    if not shutil.which("ffprobe"):
        raise RuntimeError(
            "ffprobe is not installed (should come with ffmpeg). "
            "Install ffmpeg with: apt-get install ffmpeg"
        )


def get_audio_duration_ms(audio_path: str | Path) -> int:
    """Get the duration of an audio file in milliseconds using ffprobe."""
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            str(audio_path),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed for '{audio_path}': {result.stderr}")

    data = json.loads(result.stdout)
    duration_secs = float(data["format"]["duration"])
    return int(duration_secs * 1000)


def assemble_m4b(
    chapter_audios: list[ChapterAudio],
    metadata: BookMetadata,
    output_path: str | Path,
    temp_dir: str | Path,
) -> Path:
    """Assemble chapter audio files into a single M4B audiobook."""
    check_ffmpeg_available()

    temp_dir = Path(temp_dir)
    output_path = Path(output_path)

    # Step 1: Get durations for each chapter
    logger.info("Probing chapter durations...")
    cumulative_ms = 0
    for ch_audio in chapter_audios:
        duration = get_audio_duration_ms(ch_audio.audio_path)
        ch_audio.duration_ms = duration
        cumulative_ms += duration
        logger.debug(
            "  %s: %.1f seconds", ch_audio.title, duration / 1000
        )

    total_duration_s = cumulative_ms / 1000
    logger.info("Total duration: %.1f minutes (%.0f seconds)", total_duration_s / 60, total_duration_s)

    # Step 2: Concatenate all audio files
    concat_m4a = temp_dir / "audiobook_concat.m4a"
    _concatenate_audio(chapter_audios, concat_m4a, temp_dir)

    # Step 3: Generate FFMETADATA
    metadata_file = temp_dir / "ffmetadata.txt"
    _write_ffmetadata(chapter_audios, metadata, metadata_file)

    # Step 4: Apply metadata, optional cover, and create M4B
    _apply_metadata_and_finalize(concat_m4a, metadata_file, metadata, output_path, temp_dir)

    logger.info("M4B created: %s (%.1f MB)", output_path, output_path.stat().st_size / (1024 * 1024))
    return output_path


def _concatenate_audio(
    chapter_audios: list[ChapterAudio],
    output_path: Path,
    temp_dir: Path,
) -> None:
    """Concatenate chapter WAV files into a single AAC file."""
    concat_list = temp_dir / "concat_list.txt"
    lines = []
    for ch in chapter_audios:
        safe_path = ch.audio_path.replace("'", "'\\''")
        lines.append(f"file '{safe_path}'")
    concat_list.write_text("\n".join(lines), encoding="utf-8")

    logger.info("Concatenating %d audio files to AAC...", len(chapter_audios))

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c:a", "aac",
        "-b:a", "128k",
        str(output_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg concat failed:\n{result.stderr}")


def _write_ffmetadata(
    chapter_audios: list[ChapterAudio],
    metadata: BookMetadata,
    output_path: Path,
) -> None:
    """Write an FFMETADATA1 file with book info and chapter markers."""
    lines = [
        ";FFMETADATA1",
        f"title={_escape_ffmeta(metadata.title)}",
        f"artist={_escape_ffmeta(metadata.author)}",
        f"album={_escape_ffmeta(metadata.title)}",
        "",
    ]

    cumulative_ms = 0
    for ch in chapter_audios:
        start = cumulative_ms
        end = cumulative_ms + ch.duration_ms
        lines.extend([
            "[CHAPTER]",
            "TIMEBASE=1/1000",
            f"START={start}",
            f"END={end}",
            f"title={_escape_ffmeta(ch.title)}",
            "",
        ])
        cumulative_ms = end

    output_path.write_text("\n".join(lines), encoding="utf-8")
    logger.debug("FFMETADATA written to: %s", output_path)


def _escape_ffmeta(value: str) -> str:
    """Escape special characters for FFMETADATA format."""
    # Escape backslashes first, then other special chars
    return value.replace("\\", "\\\\").replace("=", "\\=").replace(";", "\\;").replace("#", "\\#")


def _apply_metadata_and_finalize(
    audio_path: Path,
    metadata_path: Path,
    metadata: BookMetadata,
    output_path: Path,
    temp_dir: Path,
) -> None:
    """Apply metadata to the audio file and create final M4B."""
    cmd = [
        "ffmpeg", "-y",
        "-i", str(audio_path),
        "-i", str(metadata_path),
    ]

    if metadata.cover_path and Path(metadata.cover_path).exists():
        cmd.extend(["-i", str(metadata.cover_path)])
        cmd.extend([
            "-map", "0:a",
            "-map", "2:v",
            "-disposition:v:0", "attached_pic",
        ])
    else:
        cmd.extend(["-map", "0:a"])

    cmd.extend([
        "-map_metadata", "1",
        "-codec", "copy",
        str(output_path),
    ])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg metadata application failed:\n{result.stderr}")
