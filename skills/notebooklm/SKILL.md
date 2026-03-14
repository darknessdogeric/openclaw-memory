---
name: notebooklm
description: Intelligent document analysis and synthesis tool inspired by Google NotebookLM. Upload multiple documents (PDF, TXT, MD, etc.) and get AI-powered summaries, insights, and interactive Q&A based on your sources.
---

# NotebookLM Skill

An intelligent document analysis and synthesis tool that allows you to upload multiple documents and interact with them through AI-powered summaries, insights, and Q&A.

## Features

- 📄 **Multi-format Support**: PDF, TXT, MD, DOCX, HTML
- 🧠 **Smart Summarization**: Auto-generate summaries from multiple sources
- 🔗 **Source Synthesis**: Connect insights across documents
- 💬 **Interactive Q&A**: Ask questions based on your documents
- 📝 **Note Generation**: Create structured notes and outlines
- 🏷️ **Auto-tagging**: Automatic topic and keyword extraction
- 🔍 **Semantic Search**: Find relevant content across all sources

## Usage

### Command Line
```bash
# Analyze a single document
notebooklm analyze document.pdf

# Create a notebook from multiple sources
notebooklm create-notebook "Project Research" --sources doc1.pdf doc2.md doc3.txt

# Ask questions about your documents
notebooklm ask "What are the main findings?" --notebook "Project Research"

# Generate summary
notebooklm summarize --notebook "Project Research" --format bullet

# Export notes
notebooklm export --notebook "Project Research" --format markdown
```

### Python API
```python
from notebooklm import NotebookLM, Document

# Create a notebook
notebook = NotebookLM.create("My Research")

# Add documents
notebook.add_document("paper.pdf")
notebook.add_document("notes.md")

# Generate summary
summary = notebook.generate_summary()

# Ask questions
answer = notebook.ask("What is the main conclusion?")

# Create structured notes
notes = notebook.create_notes(template="academic")
```

## Supported Formats

| Format | Support | Notes |
|--------|---------|-------|
| PDF | ✅ Full | Text extraction, OCR for scanned |
| Markdown | ✅ Full | Preserves structure |
| TXT | ✅ Full | Plain text |
| DOCX | ✅ Full | Word documents |
| HTML | ✅ Partial | Web pages |
| EPUB | ⚠️ Basic | E-books |

## Output Formats

- **Summary**: Executive summary, bullet points, narrative
- **Notes**: Structured notes, outlines, flashcards
- **Export**: Markdown, PDF, JSON

## Installation

```bash
pip install -r requirements.txt

# Optional: Install OCR support
pip install pytesseract
# And install Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki
```

## Configuration

Create `~/.notebooklm/config.json`:
```json
{
  "default_model": "gpt-4",
  "chunk_size": 1000,
  "chunk_overlap": 200,
  "max_tokens": 4000,
  "temperature": 0.3
}
```

## Notes

- Documents are processed locally for privacy
- Large documents are automatically chunked
- Source attribution is maintained in all outputs
