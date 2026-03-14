#!/usr/bin/env bash
# check_deps.sh — Verify that all nano-pdf prerequisites are installed.
# Exit code 0 = all good, 1 = something is missing.

set -euo pipefail

MISSING=0

echo "=== Nano-PDF Dependency Check ==="
echo ""

# 1. nano-pdf CLI
if command -v nano-pdf &>/dev/null; then
    echo "✅ nano-pdf     $(nano-pdf --version 2>/dev/null || echo '(installed)')"
else
    echo "❌ nano-pdf     NOT FOUND"
    echo "   Install:  pip install nano-pdf"
    echo "   Or run:   uvx nano-pdf edit <file> <page> \"<prompt>\""
    MISSING=1
fi

# 2. poppler (pdftotext / pdftoppm)
if command -v pdftoppm &>/dev/null || command -v pdftotext &>/dev/null; then
    echo "✅ poppler      $(pdftoppm -v 2>&1 | head -1 || echo '(installed)')"
else
    echo "❌ poppler      NOT FOUND"
    case "$(uname -s)" in
        Darwin) echo "   Install:  brew install poppler" ;;
        Linux)  echo "   Install:  sudo apt-get install poppler-utils" ;;
        MINGW*|MSYS*|CYGWIN*) echo "   Install:  choco install poppler" ;;
        *)      echo "   Install:  see https://poppler.freedesktop.org/" ;;
    esac
    MISSING=1
fi

# 3. tesseract OCR
if command -v tesseract &>/dev/null; then
    echo "✅ tesseract    $(tesseract --version 2>&1 | head -1)"
else
    echo "❌ tesseract    NOT FOUND"
    case "$(uname -s)" in
        Darwin) echo "   Install:  brew install tesseract" ;;
        Linux)  echo "   Install:  sudo apt-get install tesseract-ocr" ;;
        MINGW*|MSYS*|CYGWIN*) echo "   Install:  choco install tesseract" ;;
        *)      echo "   Install:  see https://github.com/tesseract-ocr/tesseract" ;;
    esac
    MISSING=1
fi

# 4. GEMINI_API_KEY
echo ""
if [ -n "${GEMINI_API_KEY:-}" ]; then
    echo "✅ GEMINI_API_KEY is set"
else
    echo "❌ GEMINI_API_KEY is NOT set"
    echo "   A paid Google Gemini API key is required (free tier does not support image generation)."
    echo "   Get one at: https://aistudio.google.com/api-keys"
    echo "   Then run:   export GEMINI_API_KEY=\"your_key_here\""
    MISSING=1
fi

echo ""
if [ "$MISSING" -eq 0 ]; then
    echo "🎉 All dependencies are installed. Ready to edit PDFs!"
    exit 0
else
    echo "⚠️  Some dependencies are missing. Install them and re-run this check."
    exit 1
fi
