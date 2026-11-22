r"""
图片文字识别（OCR）v1.0 — Tesseract 中文版
============================================
**依赖**：pytesseract + Tesseract-OCR + 用户级 tessdata（chi_sim）

**安装状态**（2026-10-02）：
- Tesseract: `C:\Program Files\Tesseract-OCR\tesseract.exe`
- 用户 tessdata: `C:\Users\ericz\tessdata\`（chi_sim / chi_sim_vert / eng / osd）

用法:
    from anyi_reports.ocr_image import ocr_image, ocr_to_file

    text = ocr_image(r'C:\path\img.png')                    # 中英混合
    text = ocr_image(r'C:\path\img.png', lang='chi_sim')    # 纯中文
    ocr_to_file(img, out_txt)                                # 写文件

CLI:
    python ocr_image.py input.png [output.txt]
"""
import sys, os
from pathlib import Path

# 强制用户级 tessdata（Program Files 不可写）
os.environ.setdefault('TESSDATA_PREFIX', r'C:\Users\ericz\tessdata')

import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def ocr_image(img_path, lang='chi_sim+eng', psm=None):
    """
    识别图片文字

    :param img_path: 图片路径
    :param lang: 'chi_sim+eng'(默认中英) / 'chi_sim'(纯中文) / 'eng'(纯英文)
    :param psm: Tesseract PSM 模式（可选，默认自动）
    :return: 识别文本 (str)
    """
    img = Image.open(str(img_path))
    config = f'--psm {psm}' if psm else ''
    return pytesseract.image_to_string(img, lang=lang, config=config)


def ocr_to_file(img_path, out_txt=None, lang='chi_sim+eng'):
    """识别并写文件（默认同名 .txt）"""
    text = ocr_image(img_path, lang=lang)
    if out_txt is None:
        out_txt = str(Path(img_path).with_suffix('.ocr.txt'))
    Path(out_txt).write_text(text, encoding='utf-8')
    return text, out_txt


def ocr_pdf(pdf_path, out_txt=None, lang='chi_sim+eng', dpi=200):
    """PDF → 逐页 OCR（需 pypdf + pdf2image 或 PyMuPDF）"""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        raise RuntimeError('需要 PyMuPDF: pip install pymupdf')
    doc = fitz.open(str(pdf_path))
    parts = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=dpi)
        img = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        txt = pytesseract.image_to_string(img, lang=lang)
        parts.append(f'===== 第 {i+1} 页 =====\n{txt}')
    full = '\n\n'.join(parts)
    if out_txt:
        Path(out_txt).write_text(full, encoding='utf-8')
    return full


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) < 2:
        print('用法: python ocr_image.py input.png [output.txt]')
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    t, p = ocr_to_file(inp, out)
    print(f'[OK] {p}  ({len(t)} chars)')
    print('---')
    print(t)
