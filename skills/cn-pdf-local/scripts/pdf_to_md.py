"""
cn-pdf-local v2.0

本地 PDF → Markdown（升级版）
  - 数字 PDF：pymupdf4llm (多栏/表格/标题层级) [默认] 或 pdfplumber + PyMuPDF (基础)
  - 扫描 PDF：pdf2image + pytesseract (本地 OCR)
  - 图片抽取：PyMuPDF get_images (嵌入图保存到 sidecar 目录)
  - 公式识别：pix2tex (可选,需 torch)
  - OCR 增强：paddleocr (可选,本地推理版,需 paddlepaddle)

输出 Markdown + JSON sidecar

绝对原则：
  - 不上传任何文件到任何云端
  - 不使用任何外部 API token
  - 所有处理在 Eric 的工作空间本地完成

环境兼容性：
  - 测试环境: Python 3.14 + Windows
  - paddleocr/paddlepaddle: Python 3.14 暂无 wheel，需 Python 3.9-3.12
  - pix2tex: 需 torch，Python 3.14 暂无 wheel
  - 故默认实现仅使用 pymupdf4llm + pdfplumber + pytesseract
"""
import sys, io, os, re, json, argparse
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ===== 工具可用性检测 =====
TOOLS = {
    'pymupdf4llm': False,
    'fitz': False,
    'pdfplumber': False,
    'pdf2image': False,
    'pytesseract': False,
    'tesseract_binary': False,  # 单独检查 tesseract 二进制
    'pillow': False,
    'pix2tex': False,
    'paddleocr': False,
}

try:
    import pymupdf4llm
    TOOLS['pymupdf4llm'] = True
except ImportError:
    pass

try:
    import fitz  # PyMuPDF
    TOOLS['fitz'] = True
except ImportError:
    pass

try:
    import pdfplumber
    TOOLS['pdfplumber'] = True
except ImportError:
    pass

try:
    from pdf2image import convert_from_path
    TOOLS['pdf2image'] = True
except ImportError:
    pass

try:
    import pytesseract
    TOOLS['pytesseract'] = True
    # 检查 tesseract 二进制
    try:
        pytesseract.get_tesseract_version()
        TOOLS['tesseract_binary'] = True
    except Exception:
        TOOLS['tesseract_binary'] = False
except ImportError:
    pass

try:
    from PIL import Image
    TOOLS['pillow'] = True
except ImportError:
    pass

try:
    from pix2tex.cli import LatexOCR
    TOOLS['pix2tex'] = True
except ImportError:
    pass

try:
    from paddleocr import PaddleOCR
    TOOLS['paddleocr'] = True
except ImportError:
    pass


def detect_scan_type(pdf_path):
    """检测 PDF 是数字型还是扫描型（前 3 页字符数）"""
    if not TOOLS['fitz']:
        return 'unknown'
    doc = fitz.open(pdf_path)
    n = min(3, doc.page_count)
    if n == 0:
        doc.close()
        return 'empty'
    total = 0
    for i in range(n):
        total += len(doc[i].get_text().strip())
    doc.close()
    avg = total / n
    if avg < 50:
        return 'scanned'
    return 'digital'


def extract_metadata(pdf_path):
    if not TOOLS['fitz']:
        return {}
    doc = fitz.open(pdf_path)
    md = dict(doc.metadata or {})
    md['_page_count'] = doc.page_count
    md['_file_size_mb'] = round(os.path.getsize(pdf_path) / 1024 / 1024, 2)
    doc.close()
    return md


def extract_images(pdf_path, out_dir, page_idx):
    """抽取嵌入图片到 sidecar 目录"""
    if not TOOLS['fitz']:
        return []
    out = []
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    for pidx in page_idx:
        if pidx >= doc.page_count:
            continue
        page = doc[pidx]
        imgs = page.get_images(full=True)
        for iidx, img_info in enumerate(imgs):
            xref = img_info[0]
            try:
                base = doc.extract_image(xref)
                ext = base['ext']
                fname = f'p{pidx + 1}_img{iidx + 1}.{ext}'
                fpath = os.path.join(out_dir, fname)
                with open(fpath, 'wb') as f:
                    f.write(base['image'])
                out.append({
                    'page': pidx + 1,
                    'image_index': iidx + 1,
                    'filename': fname,
                    'size_bytes': len(base['image']),
                    'width': base.get('width'),
                    'height': base.get('height'),
                })
            except Exception as e:
                out.append({'page': pidx + 1, 'image_index': iidx + 1, 'error': str(e)})
    doc.close()
    return out


def clean_text(s):
    """prettify：清理页眉页脚/页码/多余空行"""
    if not s:
        return ''
    s = re.sub(r'^\s*[-\d]+\s*$', '', s, flags=re.M)
    s = re.sub(r'^第\s*[\d一二三四五六七八九十]+\s*页\s*$', '', s, flags=re.M)
    s = re.sub(r'^Page\s+\d+\s*$', '', s, flags=re.M | re.I)
    s = re.sub(r'\n{3,}', '\n\n', s)
    s = re.sub(r'[ \t]+\n', '\n', s)
    return s.strip()


def extract_tables_digital(pdf_path, page_idx):
    """用 pdfplumber 抽表格（增强版：先尝试 pymupdf4llm 抽出的表格，失败回退 pdfplumber）"""
    if not TOOLS['pdfplumber']:
        return []
    out = []
    with pdfplumber.open(pdf_path) as pdf:
        for i in page_idx:
            if i >= len(pdf.pages):
                continue
            page = pdf.pages[i]
            try:
                tables = page.extract_tables()
                for ti, t in enumerate(tables):
                    if t:
                        # 清理空单元格
                        cleaned = [[(c or '').strip() for c in row] for row in t]
                        out.append({
                            'page': i + 1,
                            'table_index': ti,
                            'rows': len(cleaned),
                            'cols': max(len(r) for r in cleaned) if cleaned else 0,
                            'data': cleaned,
                        })
            except Exception:
                pass
    return out


def ocr_page(pdf_path, page_idx, dpi=200, lang='chi_sim+eng', prefer='tesseract'):
    """OCR 单页（扫描型 PDF）

    prefer: 'tesseract' (默认) 或 'paddleocr'
    """
    # 优先用 paddleocr（精度高）
    if prefer == 'paddleocr' and TOOLS['paddleocr']:
        try:
            ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
            # paddleocr 需要图像输入
            from pdf2image import convert_from_path
            images = convert_from_path(pdf_path, dpi=dpi, first_page=page_idx + 1, last_page=page_idx + 1)
            if images:
                result = ocr.ocr(images[0], cls=True)
                lines = [line[1][0] for line in result[0]] if result and result[0] else []
                return '\n'.join(lines)
        except Exception as e:
            return f'[paddleocr 错误: {e}]'

    # 默认用 pytesseract
    if not TOOLS['pdf2image']:
        return '[OCR 失败：未安装 pdf2image]'
    if not TOOLS['pytesseract'] or not TOOLS['tesseract_binary']:
        return '[OCR 失败：未安装 pytesseract 或 tesseract 二进制]'
    try:
        images = convert_from_path(pdf_path, dpi=dpi, first_page=page_idx + 1, last_page=page_idx + 1)
        if not images:
            return ''
        text = pytesseract.image_to_string(images[0], lang=lang)
        return text
    except Exception as e:
        return f'[OCR 错误: {e}]'


def parse_page_range(spec):
    if not spec:
        return None
    out = []
    for part in spec.split(','):
        part = part.strip()
        if '-' in part:
            a, b = part.split('-', 1)
            a, b = int(a.strip()) - 1, int(b.strip()) - 1
            out.extend(range(a, b + 1))
        else:
            out.append(int(part) - 1)
    return sorted(set(out))


def extract_via_pymupdf4llm(pdf_path, page_idx, prettify=True):
    """用 pymupdf4llm 提取（多栏/表格/标题层级）"""
    if not TOOLS['pymupdf4llm']:
        return None
    try:
        # pymupdf4llm.to_markdown 支持页码列表（1-based）
        pages_1based = [p + 1 for p in page_idx]
        md = pymupdf4llm.to_markdown(pdf_path, pages=pages_1based)
        if prettify:
            md = clean_text(md)
        return md
    except Exception as e:
        print(f'  pymupdf4llm 失败: {e}')
        return None


def extract_via_fitz_blocks(pdf_path, page_idx, prettify=True):
    """用 PyMuPDF 块排序提取（单栏准确，多栏弱）"""
    if not TOOLS['fitz']:
        return None
    out = []
    doc = fitz.open(pdf_path)
    for pidx in page_idx:
        if pidx >= doc.page_count:
            continue
        page = doc[pidx]
        blocks = page.get_text('blocks')
        blocks_sorted = sorted(blocks, key=lambda b: (round(b[1] / 30), b[0]))
        text = '\n\n'.join(b[4].rstrip() for b in blocks_sorted if b[4].strip())
        if prettify:
            text = clean_text(text)
        out.append((pidx + 1, text))
    doc.close()
    return out


def detect_formulas(text):
    """启发式检测公式区域（统计数学符号密度）"""
    if not text:
        return []
    # 数学符号特征
    math_symbols = set('∑∏∫∂∇≈≠≤≥±×÷∈∉⊂⊃∪∩√∞∠∝∑∬∭∮')
    formula_keywords = ('lim', 'sin', 'cos', 'tan', 'log', 'ln', 'exp', '→', '⇒', '⇔', '∑', '∏', '∫')
    formula_lines = []
    lines = text.split('\n')
    for i, line in enumerate(lines):
        score = sum(1 for c in line if c in math_symbols)
        score += sum(2 for kw in formula_keywords if kw in line)
        if score >= 3:
            formula_lines.append({'line_no': i + 1, 'text': line, 'symbol_density': score})
    return formula_lines


def pdf_to_markdown(src_pdf, dst_md, page_ranges=None, prettify=True,
                    lang='chi_sim+eng', use_ocr_for_scanned=True,
                    extract_images_flag=True, ocr_engine='tesseract',
                    use_pymupdf4llm=True):
    """主函数：PDF → Markdown + JSON sidecar"""
    src_pdf = str(Path(src_pdf).resolve())
    dst_md = str(Path(dst_md).resolve())
    dst_json = re.sub(r'\.md$', '.json', dst_md)
    dst_img_dir = re.sub(r'\.md$', '_images', dst_md)

    if not os.path.exists(src_pdf):
        print(f'错误：找不到文件 {src_pdf}')
        return False

    # 元数据
    meta = extract_metadata(src_pdf)
    scan_type = detect_scan_type(src_pdf)
    print(f'检测: scan_type={scan_type}, pages={meta.get("_page_count")}, '
          f'size={meta.get("_file_size_mb")} MB')

    # 页码范围
    page_idx = parse_page_range(page_ranges) if page_ranges else list(range(meta.get('_page_count', 0)))
    print(f'解析页码: {len(page_idx)} 页')

    # 路径选择
    if scan_type == 'scanned':
        path = 'ocr'
        ocr_engine_used = ocr_engine
    else:
        path = 'digital_pymupdf4llm' if (use_pymupdf4llm and TOOLS['pymupdf4llm']) else 'digital_fitz'

    # ===== 主解析 =====
    pages_data = []
    md_lines = [f'# {os.path.basename(src_pdf)} · 解析结果', '']
    md_lines.append(f'- **类型**：{scan_type}')
    md_lines.append(f'- **路径**：{path}')
    md_lines.append(f'- **总页数**：{meta.get("_page_count")}')
    md_lines.append(f'- **本次解析页数**：{len(page_idx)}')
    md_lines.append(f'- **生成时间**：{__import__("datetime").datetime.now().isoformat(timespec="seconds")}')

    # 工具状态
    enabled_tools = [k for k, v in TOOLS.items() if v]
    disabled_tools = [k for k, v in TOOLS.items() if not v]
    md_lines.append(f'- **已启用工具**：{", ".join(enabled_tools) if enabled_tools else "（无）"}')
    if disabled_tools:
        md_lines.append(f'- **未启用**：{", ".join(disabled_tools)}')
    md_lines.append('')
    md_lines.append('---')
    md_lines.append('')

    if path == 'ocr':
        # OCR 路径
        if scan_type == 'scanned' and not use_ocr_for_scanned:
            md_lines.append('⚠️ 扫描型 PDF 但 use_ocr_for_scanned=False — 输出可能为空')
        for i, idx in enumerate(page_idx):
            text = ocr_page(src_pdf, idx, lang=lang, prefer=ocr_engine)
            if prettify:
                text = clean_text(text)
            if not text:
                text = '[空白页或 OCR 无结果]'

            formula_regions = detect_formulas(text)
            page_record = {'page': idx + 1, 'char_count': len(text), 'text': text,
                           'formula_regions': formula_regions}
            pages_data.append(page_record)
            md_lines.append(f'## 第 {idx + 1} 页')
            md_lines.append('')
            md_lines.append(text)
            md_lines.append('')
            if formula_regions:
                md_lines.append(f'> 🔢 检测到 {len(formula_regions)} 处公式（启发式）')
                md_lines.append('')
            if (i + 1) % 5 == 0:
                print(f'  进度: {i + 1}/{len(page_idx)}')
    else:
        # 数字 PDF
        if path == 'digital_pymupdf4llm':
            # 用 pymupdf4llm 一次性解析所有页（更高效）
            md_full = extract_via_pymupdf4llm(src_pdf, page_idx, prettify=prettify)
            if md_full:
                # 拆分到 pages_data（按页）
                # pymupdf4llm 输出用 markdown 锚点分隔各页（如果有）
                # 但 to_markdown(pages=[...]) 不一定会分隔，先全部塞第 1 页记录
                # 改进：分别调用每页（更准确但慢）
                for i, idx in enumerate(page_idx):
                    md_single = extract_via_pymupdf4llm(src_pdf, [idx], prettify=prettify)
                    if md_single:
                        formula_regions = detect_formulas(md_single)
                        page_record = {'page': idx + 1, 'char_count': len(md_single),
                                       'text': md_single, 'formula_regions': formula_regions}
                        pages_data.append(page_record)
                        md_lines.append(f'## 第 {idx + 1} 页')
                        md_lines.append('')
                        md_lines.append(md_single)
                        md_lines.append('')
                        if formula_regions:
                            md_lines.append(f'> 🔢 检测到 {len(formula_regions)} 处公式（启发式）')
                            md_lines.append('')
                        if (i + 1) % 5 == 0:
                            print(f'  进度: {i + 1}/{len(page_idx)}')
            else:
                # 回退 fitz
                print('  回退到 PyMuPDF 块排序')
                path = 'digital_fitz'
                fitz_result = extract_via_fitz_blocks(src_pdf, page_idx, prettify=prettify)
                if fitz_result:
                    for pidx, text in fitz_result:
                        formula_regions = detect_formulas(text)
                        page_record = {'page': pidx, 'char_count': len(text), 'text': text,
                                       'formula_regions': formula_regions}
                        pages_data.append(page_record)
                        md_lines.append(f'## 第 {pidx} 页')
                        md_lines.append('')
                        md_lines.append(text)
                        md_lines.append('')
                        if formula_regions:
                            md_lines.append(f'> 🔢 检测到 {len(formula_regions)} 处公式（启发式）')
                            md_lines.append('')
        elif path == 'digital_fitz':
            fitz_result = extract_via_fitz_blocks(src_pdf, page_idx, prettify=prettify)
            if fitz_result:
                for pidx, text in fitz_result:
                    formula_regions = detect_formulas(text)
                    page_record = {'page': pidx, 'char_count': len(text), 'text': text,
                                   'formula_regions': formula_regions}
                    pages_data.append(page_record)
                    md_lines.append(f'## 第 {pidx} 页')
                    md_lines.append('')
                    md_lines.append(text)
                    md_lines.append('')
                    if formula_regions:
                        md_lines.append(f'> 🔢 检测到 {len(formula_regions)} 处公式（启发式）')
                        md_lines.append('')

    # ===== 表格抽取（数字型 PDF）=====
    tables = []
    if path.startswith('digital') and TOOLS['pdfplumber'] and page_idx:
        print(f'  抽表格中...')
        tables = extract_tables_digital(src_pdf, page_idx)
        if tables:
            md_lines.append('---')
            md_lines.append('')
            md_lines.append(f'## 表格汇总（{len(tables)} 个）')
            md_lines.append('')
            for t in tables:
                md_lines.append(f'### 第 {t["page"]} 页 · 表格 {t["table_index"] + 1} ({t["rows"]}×{t["cols"]})')
                md_lines.append('')
                # Markdown 表格
                if t['cols'] > 0:
                    header = '| ' + ' | '.join([f'列{j+1}' for j in range(t['cols'])]) + ' |'
                    sep = '|' + '|'.join([' --- '] * t['cols']) + '|'
                    md_lines.append(header)
                    md_lines.append(sep)
                    for row in t['data']:
                        cells = [str(c).replace('|', '\\|').replace('\n', ' ').strip() for c in row]
                        while len(cells) < t['cols']:
                            cells.append('')
                        md_lines.append('| ' + ' | '.join(cells) + ' |')
                    md_lines.append('')

    # ===== 图片抽取 =====
    images = []
    if extract_images_flag and TOOLS['fitz'] and page_idx:
        print(f'  抽图片中...')
        images = extract_images(src_pdf, dst_img_dir, page_idx)
        if images:
            md_lines.append('---')
            md_lines.append('')
            md_lines.append(f'## 嵌入图片（{len(images)} 张，保存到 `{os.path.basename(dst_img_dir)}/`）')
            md_lines.append('')
            for img in images:
                if 'error' in img:
                    md_lines.append(f'- 第 {img["page"]} 页 · 图 {img["image_index"]} · ❌ {img["error"]}')
                else:
                    rel_path = os.path.join(os.path.basename(dst_img_dir), img['filename'])
                    md_lines.append(f'- 第 {img["page"]} 页 · 图 {img["image_index"]} · '
                                    f'`{rel_path}` ({img["width"]}×{img["height"]}, '
                                    f'{img["size_bytes"]//1024} KB)')
            md_lines.append('')

    # ===== 写入 =====
    Path(dst_md).parent.mkdir(parents=True, exist_ok=True)
    with open(dst_md, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    sidecar = {
        'source_pdf': src_pdf,
        'scan_type': scan_type,
        'extract_path': path,
        'metadata': meta,
        'total_pages_in_pdf': meta.get('_page_count'),
        'pages_parsed': len(page_idx),
        'page_ranges': page_ranges,
        'prettify': prettify,
        'tools_used': TOOLS,
        'tables': tables,
        'images': images,
        'pages': pages_data,
        'generated_at': __import__("datetime").datetime.now().isoformat(timespec="seconds"),
    }
    with open(dst_json, 'w', encoding='utf-8') as f:
        json.dump(sidecar, f, ensure_ascii=False, indent=2)

    print(f'✅ 完成')
    print(f'   Markdown: {dst_md}')
    print(f'   JSON:     {dst_json}')
    if images:
        print(f'   图片目录: {dst_img_dir}/ ({len(images)} 张)')
    print(f'   表格:     {len(tables)} 个')
    return True


def main():
    ap = argparse.ArgumentParser(
        description='本地 PDF → Markdown 解析（无云端上传，纯本地，pymupdf4llm 增强版）'
    )
    ap.add_argument('src_pdf', help='输入 PDF 路径')
    ap.add_argument('dst_md', help='输出 Markdown 路径（.json 同步生成）')
    ap.add_argument('--pages', default=None, help='页码范围，如 "1-5,10,15-20"')
    ap.add_argument('--no-prettify', action='store_true', help='不清理页眉页脚')
    ap.add_argument('--lang', default='chi_sim+eng', help='OCR 语言（扫描型 PDF）')
    ap.add_argument('--no-ocr', action='store_true', help='扫描型 PDF 也不 OCR')
    ap.add_argument('--no-images', action='store_true', help='不抽取嵌入图片')
    ap.add_argument('--ocr-engine', default='tesseract', choices=['tesseract', 'paddleocr'],
                    help='OCR 引擎（默认 tesseract）')
    ap.add_argument('--no-pymupdf4llm', action='store_true',
                    help='不用 pymupdf4llm，回退到 PyMuPDF 块排序（更快但不支持多栏）')
    args = ap.parse_args()

    pdf_to_markdown(
        args.src_pdf,
        args.dst_md,
        page_ranges=args.pages,
        prettify=not args.no_prettify,
        lang=args.lang,
        use_ocr_for_scanned=not args.no_ocr,
        extract_images_flag=not args.no_images,
        ocr_engine=args.ocr_engine,
        use_pymupdf4llm=not args.no_pymupdf4llm,
    )


if __name__ == '__main__':
    main()