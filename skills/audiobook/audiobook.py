#!/usr/bin/env python3
"""CLI entry point for the audiobook skill.

Converts PDF or plain text files into M4B audiobooks using piper TTS.
"""

import argparse
import json
import logging
import shutil
import sys
import tempfile
from pathlib import Path

from assembler import assemble_m4b, check_ffmpeg_available, get_audio_duration_ms
from chapters import detect_chapters
from cleaner import clean_text
from extractor import extract, extract_cover_image
from models import BookMetadata, PipelineResult
from tts_piper import get_default_model, list_voices, synthesize_chapters

logger = logging.getLogger("audiobook")

MODELS_DIR = Path(__file__).parent / "models"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="audiobook",
        description="Convert PDF or text files into M4B audiobooks using piper TTS.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # --- convert subcommand ---
    conv = sub.add_parser("convert", help="Convert a file to M4B audiobook.")
    conv.add_argument(
        "file",
        type=str,
        help="Path to the input file (.pdf or .txt).",
    )
    conv.add_argument(
        "--voice",
        type=str,
        default=None,
        help="Piper model filename (e.g. es_ES-sharvard-medium.onnx). Default: auto by language.",
    )
    conv.add_argument(
        "--language",
        type=str,
        choices=["es", "en"],
        default="es",
        help="Text language: es (Spanish), en (English). Default: es.",
    )
    conv.add_argument(
        "--title",
        type=str,
        default=None,
        help="Audiobook title (default: input filename without extension).",
    )
    conv.add_argument(
        "--author",
        type=str,
        default="Desconocido",
        help='Author name (default: "Desconocido").',
    )
    conv.add_argument(
        "--cover",
        type=str,
        default=None,
        help="Cover image path (jpg/png).",
    )
    conv.add_argument(
        "--chapters-json",
        type=str,
        default=None,
        help="JSON file with manual chapter definitions.",
    )
    conv.add_argument(
        "--pages-per-chapter",
        type=int,
        default=10,
        help="Fallback: pages per chapter when auto-detection fails (default: 10).",
    )
    conv.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Output directory (default: current directory).",
    )
    conv.add_argument(
        "--dry-run",
        action="store_true",
        help="Extract and clean text, show detected chapters, but don't generate audio.",
    )
    conv.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed processing output.",
    )
    conv.add_argument(
        "--keep-temp",
        action="store_true",
        help="Keep temporary files (for debugging).",
    )
    conv.add_argument(
        "--models-dir",
        type=str,
        default=None,
        help=f"Directory with piper .onnx models (default: {MODELS_DIR}).",
    )

    # --- list-voices subcommand ---
    lv = sub.add_parser("list-voices", help="List available piper voice models.")
    lv.add_argument(
        "--models-dir",
        type=str,
        default=None,
        help=f"Directory with piper .onnx models (default: {MODELS_DIR}).",
    )

    return parser


def cmd_convert(args) -> int:
    """Run the full conversion pipeline."""
    input_path = Path(args.file)
    if not input_path.exists():
        logger.error("File not found: %s", input_path)
        return 1

    models_dir = Path(args.models_dir) if args.models_dir else MODELS_DIR

    # Resolve voice model
    if args.voice:
        model_file = models_dir / args.voice
        speaker_id = None
    else:
        model_name, speaker_id = get_default_model(args.language)
        model_file = models_dir / model_name

    # Pre-flight checks (skip for dry-run)
    if not args.dry_run:
        try:
            check_ffmpeg_available()
        except RuntimeError as e:
            logger.error("%s", e)
            return 1

        if not model_file.exists():
            logger.error(
                "Piper model not found: %s\n"
                "Run 'make setup-models' or download manually to %s",
                model_file, models_dir,
            )
            return 1

    # Resolve metadata
    title = args.title or input_path.stem
    metadata = BookMetadata(
        title=title,
        author=args.author,
        cover_path=args.cover,
        language=args.language,
    )

    # Output path
    output_dir = Path(args.output_dir) if args.output_dir else Path.cwd()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{title}.m4a"

    # Temp directory
    temp_dir = Path(tempfile.mkdtemp(prefix="audiobook_"))
    logger.info("Temporary directory: %s", temp_dir)

    try:
        # Phase 1: Extract text
        logger.info("Phase 1: Extracting text from %s...", input_path.suffix)
        pages = extract(input_path)
        logger.info("Extracted %d pages.", len(pages))

        # Phase 2a: Clean text
        logger.info("Phase 2a: Cleaning text...")
        cleaned_pages = clean_text(pages, language=args.language)

        # Phase 2b: Detect chapters
        logger.info("Phase 2b: Detecting chapters...")
        chapters = detect_chapters(
            cleaned_pages,
            pages_per_chapter=args.pages_per_chapter,
            chapters_json=args.chapters_json,
        )
        logger.info("Detected %d chapters.", len(chapters))

        # Dry run: just show results
        if args.dry_run:
            print(f"\nDry run for: {input_path.name}")
            print(f"Pages extracted: {len(pages)}")
            print(f"Pages after cleaning: {len(cleaned_pages)}")
            print(f"Chapters detected: {len(chapters)}\n")
            for i, ch in enumerate(chapters, 1):
                word_count = len(ch.text.split())
                print(f"  {i}. {ch.title} (page {ch.start_page}, {word_count} words)")
            print()
            return 0

        # Try to extract cover if not provided and input is PDF
        if not metadata.cover_path and input_path.suffix.lower() == ".pdf":
            cover_path = temp_dir / "cover.png"
            extracted = extract_cover_image(input_path, cover_path)
            if extracted:
                metadata.cover_path = str(extracted)

        # Phase 3: TTS
        logger.info("Phase 3: Synthesizing speech with piper...")
        chapter_audios = synthesize_chapters(
            chapters,
            model_path=model_file,
            speaker_id=speaker_id,
            temp_dir=temp_dir,
        )

        # Phase 4: Assemble M4B
        logger.info("Phase 4: Assembling M4B audiobook...")
        m4b_path = assemble_m4b(
            chapter_audios,
            metadata=metadata,
            output_path=output_path,
            temp_dir=temp_dir,
        )

        # Calculate total duration
        total_duration_ms = sum(ch.duration_ms for ch in chapter_audios)

        result = PipelineResult(
            output_path=str(m4b_path),
            num_chapters=len(chapter_audios),
            total_duration_ms=total_duration_ms,
            file_size_bytes=m4b_path.stat().st_size,
        )

        # Print JSON result for the agent to parse
        duration_s = result.total_duration_ms / 1000
        duration_str = f"{int(duration_s // 3600)}h{int((duration_s % 3600) // 60):02d}m" if duration_s >= 3600 else f"{int(duration_s // 60)}m{int(duration_s % 60):02d}s"
        size_mb = result.file_size_bytes / (1024 * 1024)

        output_json = {
            "output_path": result.output_path,
            "duration": duration_str,
            "chapters": result.num_chapters,
            "size_mb": round(size_mb, 1),
        }
        print(json.dumps(output_json, ensure_ascii=False))
        return 0

    except Exception as e:
        logger.error("Pipeline failed: %s", e)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

    finally:
        if not args.keep_temp:
            shutil.rmtree(temp_dir, ignore_errors=True)
            logger.debug("Cleaned up temp directory: %s", temp_dir)
        else:
            logger.info("Temp files preserved at: %s", temp_dir)


def cmd_list_voices(args) -> int:
    """List available voice models."""
    models_dir = Path(args.models_dir) if args.models_dir else MODELS_DIR
    voices = list_voices(models_dir)

    if not voices:
        print(f"No models found in {models_dir}")
        print("Run 'make setup-models' to download default models.")
        return 0

    print(f"Available models in {models_dir}:")
    for v in voices:
        print(f"  {v}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    # Configure logging
    log_level = logging.DEBUG if getattr(args, "verbose", False) else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s",
    )

    if args.command == "convert":
        return cmd_convert(args)
    elif args.command == "list-voices":
        return cmd_list_voices(args)
    else:
        logger.error("Unknown command: %s", args.command)
        return 1


if __name__ == "__main__":
    sys.exit(main())
