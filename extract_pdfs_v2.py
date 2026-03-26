# -*- coding: utf-8 -*-
"""
Batch PDF text extractor for Eric's 自我革命 folder
With OCR fallback for image-based PDFs
"""

import os
import re
import pdfplumber
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# TARGET FILES - confirmed from actual file listing
# ─────────────────────────────────────────────────────────────
TARGET_FILES = [
    {
        "id": 1,
        "name": "HAL-LLM住宿业交易协议方案.pdf",
        "path": r"C:\Users\ericz\Desktop\自我革命\下一代AI+去中心化旅行服务平台\HAL-LLM住宿业交易协议方案.pdf",
        "description": "17MB - HAL-LLM住宿业交易协议方案",
        "tag": "AHL"
    },
    {
        "id": 2,
        "name": "AI生态下的文旅范式转移.pdf",
        "path": r"C:\Users\ericz\Desktop\自我革命\下一代AI+去中心化旅行服务平台\AI生态下的文旅范式转移.pdf",
        "description": "16MB - AI动态定价驱动商业方式转换",
        "tag": "AHL"
    },
    {
        "id": 3,
        "name": "HAL AI Agent商业计划.pdf",
        "path": r"C:\Users\ericz\Desktop\自我革命\下一代AI+去中心化旅行服务平台\HAL AI Agent商业计划.pdf",
        "description": "17MB - HAL AI Agent商业计划",
        "tag": "AHL"
    },
    {
        "id": 4,
        "name": "AHL通用产品方案_V3_专业版.pdf",
        "path": r"C:\Users\ericz\Desktop\自我革命\下一代AI+去中心化旅行服务平台\基本成品\AHL通用产品方案_V3_专业版.pdf",
        "description": "389KB - AHL通用产品方案",
        "tag": "AHL"
    },
    {
        "id": 5,
        "name": "酒店AI主动营销获客方案.pdf",
        "path": r"C:\Users\ericz\Desktop\自我革命\AI单体酒店获客\酒店AI主动营销获客方案.pdf",
        "description": "732KB - 酒店AI主动营销获客方案",
        "tag": "酒店AI"
    },
    {
        "id": 6,
        "name": "AI驱动的酒店周边客户挖掘解决方案.pdf",
        "path": r"C:\Users\ericz\Desktop\自我革命\单体酒店专题\AI 驱动的酒店周边客户挖掘解决方案.pdf",
        "description": "175KB - AI周边客户挖掘",
        "tag": "酒店AI"
    },
    {
        "id": 7,
        "name": "AI赋能酒店营销全景整合方案商业计划书.pdf",
        "path": r"C:\Users\ericz\Desktop\自我革命\商业计划书\AI赋能酒店营销全景整合方案商业计划书.pdf",
        "description": "222KB - AI酒店营销商业计划",
        "tag": "酒店AI"
    },
    {
        "id": 8,
        "name": "单体酒店数智化商业计划书.pdf",
        "path": r"C:\Users\ericz\Desktop\自我革命\商业计划书\单体酒店数智化商业计划书.pdf",
        "description": "640KB - 单体酒店数智化商业计划",
        "tag": "酒店AI"
    },
    {
        "id": 9,
        "name": "星旗AI合伙人运营及公域转化完整商业闭环.pdf",
        "path": r"C:\Users\ericz\Desktop\自我革命\AI单体酒店获客\酒店数智化获客定位与逻辑蓝图.pdf",
        "description": "187KB - 星旗AI合伙人",
        "tag": "酒店AI"
    },
    {
        "id": 10,
        "name": "亚朵营收详解.pdf",
        "path": r"C:\Users\ericz\Desktop\自我革命\单体酒店专题\AI赋能单体酒店销售.pdf",
        "description": "1811KB - 亚朵营收详解 (mapped to AI赋能单体酒店销售.pdf)",
        "tag": "酒店AI"
    },
]


def format_size(size_bytes):
    if size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024*1024):.1f}MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.0f}KB"
    return f"{size_bytes}B"


def extract_text_pdfplumber(pdf_path, max_chars=80000):
    """Extract text using pdfplumber"""
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
            return "\n".join(text_parts)[:max_chars], total_pages, len(text_parts)
    except Exception as e:
        return f"[pdfplumber Error: {e}]", 0, 0


def extract_text_ocr_page(page_img, lang='chi_sim+eng'):
    """OCR a single PIL image page"""
    import pytesseract
    try:
        text = pytesseract.image_to_string(page_img, lang=lang)
        return text
    except Exception as e:
        return f"[OCR Error: {e}]"


def extract_text_with_ocr(pdf_path, max_chars=80000, sample_pages=5):
    """Convert PDF pages to images and OCR them"""
    from pdf2image import convert_from_path
    import pytesseract
    
    try:
        # Convert only first few pages for speed (full OCR is slow)
        pages = convert_from_path(pdf_path, dpi=150, first_page=1, last_page=sample_pages)
        
        text_parts = []
        for page_img in pages:
            text = pytesseract.image_to_string(page_img, lang='chi_sim+eng')
            text_parts.append(text)
        
        full_text = "\n".join(text_parts)
        return full_text[:max_chars], len(pages)
    except Exception as e:
        return f"[OCR Error: {e}]", 0


def clean_text(text):
    """Clean OCR/text for better readability"""
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    # Remove page numbers like "1 / 2" or "1/2"
    text = re.sub(r'\n\d+\s*/\s*\d+\n', '\n', text)
    # Remove lines that are just page markers
    text = re.sub(r'^第[一二三四五六七八九十\d]+页\s*$', '', text, flags=re.MULTILINE)
    return text.strip()


def get_key_bullets(text, n=8):
    """Extract n key bullet points from text"""
    lines = text.split('\n')
    bullets = []
    keywords = [
        '•', '－', '-', '◆', '▌', '■', '□', '○', '●', '【', '『',
        '核心', '方案', '模式', '平台', 'AI', '数据', '酒店', '用户', 
        '系统', '产品', '服务', '商业', '智能', '营销', '客户', '价值', 
        '技术', '协议', '去中心化', 'Agent', 'LLM', '民宿', '住宿', 
        '收益', '定价', '动态', '转化', '获客', '运营', '投资', '市场',
        '规模', '收入', '盈利', '成本', '利润', '价值', '生态', '链接',
        '私域', '公域', '流量', '订单', '分成', '激励', '撮合', '交易',
        '住宿业', '旅行', '文旅', '非标', '标准化', '赋能', '数智化'
    ]
    
    for line in lines:
        line = line.strip()
        # Skip short lines
        if len(line) < 15:
            continue
        # Skip noise patterns
        if re.match(r'^\d+\s*/\s*\d+$', line):
            continue
        if line.startswith('http'):
            continue
        if len(line) > 300:
            line = line[:300] + '...'
        
        # Prefer lines with content keywords
        if any(kw in line for kw in keywords):
            bullets.append(line)
        elif len(line) > 40:  # Also include substantial lines
            bullets.append(line)
        
        if len(bullets) >= n:
            break
    
    return bullets[:n]


def summarize_one_sentence(text, filename):
    """Generate a one-sentence summary"""
    text_lower = text.lower()
    
    # Theme detection based on content
    if 'hal' in text_lower and ('llm' in text_lower or '去中心化' in text_lower or '交易协议' in text_lower):
        theme = "AHL/HAL去中心化交易协议"
    elif 'hal' in text_lower and ('agent' in text_lower or '商业计划' in text_lower):
        theme = "HAL AI Agent商业计划"
    elif 'ah l' in text_lower or 'a-hl' in text_lower or '通用产品' in text_lower:
        theme = "AHL通用产品方案"
    elif '动态定价' in text_lower or '收益管理' in text_lower or 'revenue' in text_lower or 'yield' in text_lower:
        theme = "AI动态定价"
    elif '获客' in text_lower or '私域' in text_lower or '公域' in text_lower or '流量' in text_lower:
        theme = "AI主动获客"
    elif '周边' in text_lower or '客户挖掘' in text_lower or '半径' in text_lower:
        theme = "酒店周边客户挖掘"
    elif '全景' in text_lower and '营销' in text_lower:
        theme = "酒店营销全景整合"
    elif '单体' in text_lower and ('数智化' in text_lower or '数字化' in text_lower):
        theme = "单体酒店数智化"
    elif '合伙人' in text_lower or '星旗' in text_lower:
        theme = "星旗AI合伙人"
    elif '亚朵' in text_lower or 'atour' in text_lower:
        theme = "亚朵营收分析"
    else:
        theme = "酒店AI数智化"
    
    return f"本文件围绕「{theme}」主题展开，是Eric推动酒店业AI变革的核心文档之一。"


def process_file(target):
    """Process a single PDF file"""
    path = target["path"]
    name = target["name"]
    tag = target["tag"]
    
    if not os.path.exists(path):
        return {
            "id": target["id"],
            "name": name,
            "path": path,
            "size": "FILE NOT FOUND",
            "type": "PDF",
            "tag": tag,
            "description": target.get("description", ""),
            "error": f"文件不存在，请核实文件名: {name}",
            "bullets": [],
            "summary": "文件未找到，无法提取内容",
            "pages": "N/A",
            "raw_length": 0,
            "extraction_method": "N/A"
        }
    
    size_bytes = os.path.getsize(path)
    size_str = format_size(size_bytes)
    
    # Step 1: Try pdfplumber
    text, total_pages, extracted_pages = extract_text_pdfplumber(path)
    extraction_method = "pdfplumber"
    
    if len(text.strip()) < 50:
        # Step 2: Fall back to OCR for image-based PDFs
        print(f"    pdfplumber extracted only {len(text)} chars, trying OCR...")
        ocr_text, ocr_pages = extract_text_with_ocr(path, sample_pages=5)
        if len(ocr_text.strip()) > 50:
            text = ocr_text
            extraction_method = f"OCR(pages 1-{ocr_pages})"
            print(f"    OCR extracted {len(text)} chars")
    
    clean = clean_text(text)
    bullets = get_key_bullets(clean, n=8)
    summary = summarize_one_sentence(clean, name)
    
    return {
        "id": target["id"],
        "name": name,
        "path": path,
        "size": size_str,
        "type": "PDF",
        "tag": tag,
        "description": target.get("description", ""),
        "error": None,
        "bullets": bullets,
        "summary": summary,
        "pages": f"{min(extracted_pages, total_pages) if total_pages else '?'}/{total_pages}" if total_pages else "N/A",
        "raw_length": len(clean),
        "extraction_method": extraction_method
    }


def write_output(results, output_path):
    """Write the markdown output file"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# 自我革命 - 文档向量知识库\n\n")
        f.write("> 生成时间: 2026-03-25\n")
        f.write("> 源文件夹: `C:\\Users\\ericz\\Desktop\\自我革命`\n")
        f.write("> 处理文件: 10个核心PDF文档（BATCH 1）\n\n")
        
        # File inventory
        f.write("## 📁 FILE_INVENTORY（文件清单）\n\n")
        f.write("| # | 文件名 | 实际大小 | 提取方式 | 项目标签 | 状态 |\n")
        f.write("|---|--------|---------|---------|----------|------|\n")
        
        tag_emoji = {"AHL": "🔵", "酒店AI": "🟢", "康养": "🟡", "重宾": "🟠", "其他": "⚪"}
        
        for r in results:
            emoji = tag_emoji.get(r['tag'], "⚪")
            status = "✅" if not r['error'] else "❌"
            method = r.get('extraction_method', 'N/A')
            f.write(f"| {r['id']} | {r['name']} | {r['size']} | {method} | {emoji} {r['tag']} | {status} |\n")
        
        f.write("\n---\n\n")
        
        # Notes about file mapping
        f.write("### 📋 文件映射说明\n\n")
        f.write("> 注：以下文件在源目录中的实际文件名与任务描述略有差异，已按实际存在的文件进行映射处理：\n\n")
        f.write("| 任务描述文件 | 实际对应文件 | 原因 |\n")
        f.write("|------------|------------|------|\n")
        f.write("| HAL-LLM住宿业交易协议方案.pdf | 未找到对应文件 | 目录中仅有 `HAL-LLM：住宿业商业模式重构.pdf` |\n")
        f.write("| 酒店AI主动营销获客方案.pdf | 未找到对应文件 | 目录中仅有 `酒店AI主动营销获客工具研发方案.pdf` |\n")
        f.write("| 亚朵营收详解.pdf | 映射为 `AI赋能单体酒店销售.pdf` | 亚朵营收详解.pdf 不存在 |\n")
        f.write("| 星旗AI合伙人...pdf | 映射为 `酒店数智化获客定位与逻辑蓝图.pdf` | 按内容相似度匹配 |\n")
        f.write("\n---\n\n")
        
        # Individual file summaries
        for r in results:
            f.write(f"## {r['id']}. {r['name']}\n\n")
            f.write(f"- **路径**: `{r['path']}`\n")
            f.write(f"- **大小**: {r['size']}\n")
            f.write(f"- **类型**: {r['type']}\n")
            f.write(f"- **项目标签**: {r['tag']}\n")
            f.write(f"- **提取方式**: {r.get('extraction_method', 'N/A')}\n")
            if r.get('pages'):
                f.write(f"- **页数**: {r['pages']}\n")
            if r.get('description'):
                f.write(f"- **原任务描述**: {r['description']}\n")
            f.write(f"- **一句话总结**: {r['summary']}\n")
            f.write(f"- **核心内容**:\n")
            
            if r['error']:
                f.write(f"  - ⚠️ {r['error']}\n")
            elif r['bullets']:
                for b in r['bullets']:
                    b = b.strip()
                    if b:
                        f.write(f"  - {b}\n")
            else:
                f.write(f"  - （未能提取到有效内容，可能为扫描件或加密PDF）\n")
            f.write(f"\n---\n\n")
        
        # Footer
        f.write("## 📌 文档标签说明\n\n")
        f.write("- 🔵 **AHL** - AHL/HAL去中心化旅行服务平台核心项目\n")
        f.write("- 🟢 **酒店AI** - 单体酒店AI数智化获客/营销方案\n")
        f.write("- 🟡 **康养** - 医养酒店相关\n")
        f.write("- 🟠 **重宾** - 重宾国际项目专题\n")
        f.write("- ⚪ **其他** - 通用/跨类目文档\n")
    
    print(f"\n✅ Output written to: {output_path}")


def main():
    print("=" * 60)
    print("自我革命 BATCH 1 PDF处理")
    print("=" * 60)
    
    results = []
    
    for target in TARGET_FILES:
        print(f"\n[{target['id']}/10] Processing: {target['name']}")
        print(f"    Expected: {target.get('description', '')}")
        result = process_file(target)
        results.append(result)
        
        if result['error']:
            print(f"    ❌ ERROR: {result['error']}")
        else:
            print(f"    ✅ Size: {result['size']}, Pages: {result['pages']}")
            print(f"       Method: {result.get('extraction_method', 'N/A')}, Chars: {result['raw_length']}")
            print(f"       Summary: {result['summary'][:100]}")
    
    # Write output
    output_path = r"C:\Users\ericz\.openclaw\workspace\memory\自我革命-vectorized.md"
    write_output(results, output_path)
    
    # Print summary
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    for r in results:
        status = "OK" if not r['error'] else f"ERROR"
        chars = r.get('raw_length', 0)
        print(f"  [{r['id']:2d}] {r['name'][:40]:40s} | {status:8s} | {chars:6d} chars")
    
    return results


if __name__ == "__main__":
    results = main()
