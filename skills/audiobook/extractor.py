"""Phase 1: Extract text from PDF or plain text files."""

import logging
from pathlib import Path

import pdfplumber

from models import Page

logger = logging.getLogger(__name__)

# Approximate characters per "page" when splitting plain text
TEXT_PAGE_SIZE = 3000


def extract(path: str | Path) -> list[Page]:
    """Extract text from a file, dispatching by extension.

    Supports .pdf and .txt files.

    Args:
        path: Path to the input file.

    Returns:
        List of Page objects.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If no text could be extracted or format is unsupported.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    ext = path.suffix.lower()
    if ext == ".pdf":
        return extract_pages(path)
    elif ext == ".txt":
        return extract_from_text(path)
    else:
        raise ValueError(
            f"Unsupported file format: '{ext}'. Use .pdf or .txt"
        )


def extract_pages(pdf_path: str | Path) -> list[Page]:
    """Extract text from each page of a PDF file."""
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    pages: list[Page] = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            if not text.strip():
                logger.warning("Page %d has no extractable text (scanned image?). Skipping.", i)
                continue
            pages.append(Page(number=i, text=text))
            logger.debug("Page %d: extracted %d characters.", i, len(text))

    if not pages:
        raise ValueError(
            f"No text could be extracted from '{pdf_path.name}'. "
            "The PDF may be scanned images. OCR is not supported."
        )

    logger.info("Extracted text from %d pages out of %d total.", len(pages), i)
    return pages


def extract_from_text(text_path: str | Path) -> list[Page]:
    """Read a plain text file and split it into page-sized chunks.

    Splits on paragraph boundaries (double newlines) to keep chunks
    coherent, targeting approximately TEXT_PAGE_SIZE characters per page.

    Args:
        text_path: Path to the .txt file.

    Returns:
        List of Page objects.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty.
    """
    text_path = Path(text_path)
    if not text_path.exists():
        raise FileNotFoundError(f"Text file not found: {text_path}")

    content = text_path.read_text(encoding="utf-8")
    if not content.strip():
        raise ValueError(f"Text file is empty: {text_path.name}")

    # Split by paragraphs (double newline)
    paragraphs = content.split("\n\n")
    pages: list[Page] = []
    current_text = ""
    page_num = 1

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        if current_text and len(current_text) + len(para) + 2 > TEXT_PAGE_SIZE:
            pages.append(Page(number=page_num, text=current_text))
            page_num += 1
            current_text = para
        else:
            if current_text:
                current_text += "\n\n" + para
            else:
                current_text = para

    if current_text.strip():
        pages.append(Page(number=page_num, text=current_text))

    logger.info("Split text file into %d pages (~%d chars each).", len(pages), TEXT_PAGE_SIZE)
    return pages


def extract_cover_image(pdf_path: str | Path, output_path: str | Path) -> Path | None:
    """Try to extract the first page as a cover image."""
    pdf_path = Path(pdf_path)
    output_path = Path(output_path)

    try:
        with pdfplumber.open(pdf_path) as pdf:
            first_page = pdf.pages[0]
            images = first_page.images
            if not images:
                logger.debug("No images found on first page for cover extraction.")
                return None

            img = first_page.to_image(resolution=150)
            img.save(str(output_path), format="PNG")
            logger.info("Cover image extracted to: %s", output_path)
            return output_path
    except Exception as e:
        logger.debug("Could not extract cover image: %s", e)
        return None
