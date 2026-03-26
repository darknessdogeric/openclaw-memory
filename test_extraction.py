# -*- coding: utf-8 -*-
"""
PDF OCR fallback: try pymupdf/pypdf2 for image-based PDFs
"""
import os
import sys

# Try pymupdf as fallback
try:
    import fitz  # PyMuPDF
    HAS_FITZ = True
except:
    HAS_FITZ = False

def extract_with_fitz(pdf_path, max_chars=30000):
    """Use PyMuPDF to extract text (better for some scanned PDFs)"""
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        text_parts = []
        char_count = 0
        for page in doc:
            text = page.get_text() or ""
            text_parts.append(text)
            char_count += len(text)
            if char_count >= max_chars:
                break
        doc.close()
        return "\n".join(text_parts)[:max_chars], total_pages
    except Exception as e:
        return f"[PyMuPDF Error: {e}]", 0

def extract_with_pdfplumber(pdf_path, max_chars=30000):
    """Extract using pdfplumber"""
    import pdfplumber
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            text_parts = []
            char_count = 0
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text_parts.append(page_text)
                char_count += len(page_text)
                if char_count >= max_chars:
                    break
            return "\n".join(text_parts)[:max_chars], total_pages
    except Exception as e:
        return f"[pdfplumber Error: {e}]", 0

def test_large_pdfs():
    """Test extraction on the 3 large PDFs"""
    base = r"C:\Users\ericz\Desktop\自我革命\下一代AI+去中心化旅行服务平台"
    
    files_to_test = [
        (r"C:\Users\ericz\Desktop\自我革命\下一代AI+去中心化旅行服务平台\AI生态下的文旅范式转移.pdf", "AI动态定价(假设)"),
        (r"C:\Users\ericz\Desktop\自我革命\下一代AI+去中心化旅行服务平台\HAL AI Agent商业计划.pdf", "HAL AI Agent商业计划"),
        (r"C:\Users\ericz\Desktop\自我革命\商业计划书\单体酒店数智化商业计划书.pdf", "单体酒店数智化商业计划书"),
    ]
    
    print(f"PyMuPDF available: {HAS_FITZ}")
    print()
    
    for path, label in files_to_test:
        if not os.path.exists(path):
            print(f"[{label}] FILE NOT FOUND: {path}")
            continue
        
        size = os.path.getsize(path)
        print(f"[{label}] Size: {size/1024/1024:.1f}MB")
        
        # Try pdfplumber
        text, pages = extract_with_pdfplumber(path, 5000)
        print(f"  pdfplumber: {len(text)} chars, {pages} pages")
        if text and len(text) > 100:
            print(f"  Sample: {text[:200]}")
        
        # Try PyMuPDF if available
        if HAS_FITZ:
            text2, pages2 = extract_with_fitz(path, 5000)
            print(f"  PyMuPDF: {len(text2)} chars, {pages2} pages")
            if text2 and len(text2) > 100:
                print(f"  Sample: {text2[:200]}")

if __name__ == "__main__":
    test_large_pdfs()
