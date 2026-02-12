---
name: doc-reader
description: Read and extract content from various document formats including DOCX, PDF, TXT, MD, JSON, XML, HTML, CSV. Use when the user wants to read document files that are not plain text, or when working with Word documents, PDFs, or other file formats. Automatically detects file type and extracts readable content.
---

# Document Reader Skill

This skill enables reading content from various document formats.

## Supported Formats

- `.docx` - Microsoft Word documents
- `.pdf` - PDF documents
- `.txt`, `.md`, `.json`, `.xml`, `.html`, `.csv` - Text-based formats

## Usage

Use the extraction script to read document content:

```bash
python "C:\Users\Administrator\.openclaw\workspace\skills\doc-reader\scripts\extract_doc.py" <file_path>
```

### Examples

**Read a Word document:**
```python
python "C:\Users\Administrator\.openclaw\workspace\skills\doc-reader\scripts\extract_doc.py" "C:\Users\Administrator\Desktop\简历及身份证件\简历文件.docx"
```

**Read a PDF:**
```python
python "C:\Users\Administrator\.openclaw\workspace\skills\doc-reader\scripts\extract_doc.py" "C:\Users\Administrator\Desktop\简历及身份证件\Zhangshi.pdf"
```

## Installation Requirements

If extraction fails due to missing dependencies:

```bash
pip install python-docx PyPDF2
```

## Workflow

1. Check if file path is provided by user
2. Determine file extension
3. Run extraction script via exec tool
4. Handle any errors (missing dependencies, corrupted files, etc.)
5. Present extracted content to user

## Error Handling

- If dependencies are missing, guide user to install them
- If file is corrupted or password-protected, inform user
- For scanned PDFs without OCR, note that text extraction may fail
