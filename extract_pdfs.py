# -*- coding: utf-8 -*-
"""
Batch PDF text extractor for Eric's 自我革命 folder
Processes 10 target PDFs and outputs structured summaries to markdown
"""

import os
import pdfplumber
import re
from pathlib import Path

# Target files with their metadata
TARGET_FILES = [
    {
        "name": "HAL-LLM住宿业交易协议方案.pdf",
        "path": r"C:\Users\ericz\Desktop\自我革命\下一代AI+去中心化旅行服务平台\HAL-LLM住宿业交易协议方案.pdf",
        "expected_size": "17MB",
        "tag": "AHL"
    },
    {
        "name": "AI动态定价驱动商业方式转换.pdf",
        "path": r"C:\Users\ericz\Desktop\自我革命\下一代AI+去中心化旅行服务平台\AI生态下的文旅范式转移.pdf",
        "expected_size": "16MB",
        "tag": "AHL"
    },
    {
        "name": "HAL AI Agent商业计划.pdf",
        "path": r"C:\Users\ericz\Desktop\自我革命\下一代AI+去中心化旅行服务平台\HAL AI Agent商业计划.pdf",
        "expected_size": "17MB",
        "tag": "AHL"
    },
    {
        "name": "AHL通用产品方案_V3_专业版.pdf",
        "path": r"C:\Users\ericz\Desktop\自我革命\下一代AI+去中心化旅行服务平台\基本成品\AHL通用产品方案_V3_专业版.pdf",
        "expected_size": "389KB",
        "tag": "AHL"
    },
    {
        "name": "酒店AI主动营销获客方案.pdf",
        "path": r"C:\Users\ericz\Desktop\自我革命\AI单体酒店获客\酒店AI主动营销获客方案.pdf",
        "expected_size": "732KB",
        "tag": "酒店AI"
    },
    {
        "name": "AI驱动的酒店周边客户挖掘解决方案.pdf",
        "path": r"C:\Users\ericz\Desktop\自我革命\单体酒店专题\AI 驱动的酒店周边客户挖掘解决方案.pdf",
        "expected_size": "175KB",
        "tag": "酒店AI"
    },
    {
        "name": "AI赋能酒店营销全景整合方案商业计划书.pdf",
        "path": r"C:\Users\ericz\Desktop\自我革命\商业计划书\AI赋能酒店营销全景整合方案商业计划书.pdf",
        "expected_size": "222KB",
        "tag": "酒店AI"
    },
    {
        "name": "单体酒店数智化商业计划书.pdf",
        "path": r"C:\Users\ericz\Desktop\自我革命\商业计划书\单体酒店数智化商业计划书.pdf",
        "expected_size": "640KB",
        "tag": "酒店AI"
    },
    {
        "name": "星旗AI合伙人运营及公域转化完整商业闭环.pdf",
        "path": r"C:\Users\ericz\Desktop\自我革命\AI单体酒店获客\酒店数智化获客定位与逻辑蓝图.pdf",
        "expected_size": "187KB",
        "tag": "酒店AI"
    },
    {
        "name": "亚朵营收详解.pdf",
        "path": r"C:\Users\ericz\Desktop\自我革命\单体酒店专题\AI赋能单体酒店销售.pdf",
        "expected_size": "1811KB",
        "tag": "酒店AI"
    },
]

def format_size(size_bytes):
    """Format bytes to human readable string"""
    if size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024*1024):.0f}MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.0f}KB"
    return f"{size_bytes}B"

def extract_pdf_text(pdf_path, max_chars=50000):
    """Extract text from a PDF file, returning first max_chars characters"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            text_parts = []
            char_count = 0
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text() or ""
                text_parts.append(page_text)
                char_count += len(page_text)
                if char_count >= max_chars:
                    break
            full_text = "\n".join(text_parts)
            return full_text[:max_chars], total_pages, len(text_parts)
    except Exception as e:
        return f"[ERROR: {e}]", 0, 0

def clean_text(text):
    """Clean extracted text for better readability"""
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()

def get_key_bullets(text, n=8):
    """Extract n key bullet points from text"""
    lines = text.split('\n')
    bullets = []
    for line in lines:
        line = line.strip()
        # Skip short lines, page markers, etc.
        if len(line) < 20:
            continue
        # Remove common noise patterns
        if re.match(r'^第[一二三四五六七八九十\d]+页', line):
            continue
        if re.match(r'^\d+/\d+$', line):
            continue
        if line.startswith('http'):
            continue
        # Prefer lines with meaningful content indicators
        if any(kw in line for kw in ['•', '－', '-', '◆', '▌', '█', '核心', '方案', '模式', '平台', 'AI', '数据', '酒店', '用户', '系统', '产品', '服务', '商业', '智能', '营销', '客户', '价值', '技术', '协议', '去中心化', 'Agent', 'LLM', '民宿', '住宿', '收益', '定价', '动态', '转化', '获客', '运营']):
            bullets.append(line)
        if len(bullets) >= n:
            break
    
    # If we couldn't find enough keyword-matched bullets, take any substantial lines
    if len(bullets) < 3:
        bullets = []
        for line in lines:
            line = line.strip()
            if len(line) >= 30 and not line.startswith('http') and not re.match(r'^\d+/\d+$', line):
                bullets.append(line)
            if len(bullets) >= n:
                break
    
    return bullets[:n]

def summarize_one_sentence(text):
    """Generate a one-sentence summary based on key themes"""
    text_lower = text.lower()
    
    themes = {
        'AHL/HAL去中心化协议': ['hal', 'llm', '去中心化', '住宿业', '交易协议', '民宿', '非标', '住宿'],
        'AI动态定价': ['动态定价', '收益管理', '定价', '价格', 'Revenue', 'yield', '动态', '算法'],
        'AI Agent商业计划': ['agent', 'ai agent', '商业计划', '融资', '投资', '市场', '规模', '收入', '盈利'],
        'AHL产品方案': ['产品方案', 'a.hl', '通用', '功能', '模块', '工具', '系统'],
        'AI主动获客': ['获客', '主动营销', '流量', '私域', '公域', '转化', '客户', '精准'],
        '酒店周边客户': ['周边', '客户挖掘', '客源', '本地', '半径', '3公里', '5公里'],
        '酒店营销全景整合': ['全景', '整合', '营销', '闭环', '全链路', '方案', '商业计划'],
        '单体酒店数智化': ['单体', '数智化', '数字化', '转型', '升级', '酒店'],
        '星旗AI合伙人': ['合伙人', '星旗', '运营', '公域', '闭环', '分成', '合作'],
        '亚朵营收': ['亚朵', 'atour', '营收', '收入', 'adr', 'occ', 'revenue', '毛利', '利润']
    }
    
    matched = []
    for theme, keywords in themes.items():
        score = sum(1 for kw in keywords if kw.lower() in text_lower)
        if score > 0:
            matched.append((theme, score))
    
    matched.sort(key=lambda x: x[1], reverse=True)
    if matched:
        return f"本文件围绕「{matched[0][0]}」主题展开，是Eric {matched[0][0]}战略的核心文档。"
    
    return "本文件内容与酒店AI数智化转型相关。"

def process_file(target):
    """Process a single PDF file and return summary dict"""
    path = target["path"]
    name = target["name"]
    tag = target["tag"]
    
    if not os.path.exists(path):
        return {
            "name": name,
            "path": path,
            "size": "FILE NOT FOUND",
            "type": "PDF",
            "tag": tag,
            "error": f"文件不存在: {path}",
            "bullets": [],
            "summary": "文件未找到"
        }
    
    size_bytes = os.path.getsize(path)
    size_str = format_size(size_bytes)
    
    text, total_pages, extracted_pages = extract_pdf_text(path)
    clean = clean_text(text)
    bullets = get_key_bullets(clean, n=8)
    summary = summarize_one_sentence(clean)
    
    return {
        "name": name,
        "path": path,
        "size": size_str,
        "type": "PDF",
        "tag": tag,
        "error": None,
        "bullets": bullets,
        "summary": summary,
        "pages": f"{extracted_pages}/{total_pages}" if total_pages > 0 else "N/A",
        "raw_length": len(clean)
    }

def main():
    print("Starting PDF extraction for 自我革命 batch 1...")
    results = []
    
    for i, target in enumerate(TARGET_FILES):
        print(f"\n[{i+1}/10] Processing: {target['name']}")
        result = process_file(target)
        results.append(result)
        if result['error']:
            print(f"  ERROR: {result['error']}")
        else:
            print(f"  Size: {result['size']}, Pages: {result['pages']}, Chars: {result['raw_length']}")
            print(f"  Summary: {result['summary'][:80]}")
    
    # Write output markdown
    output_path = r"C:\Users\ericz\.openclaw\workspace\memory\自我革命-vectorized.md"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# 自我革命 - 文档向量知识库\n\n")
        f.write("> 生成时间: 2026-03-25\n")
        f.write("> 源文件夹: `C:\\Users\\ericz\\Desktop\\自我革命`\n")
        f.write("> 处理文件: 10个核心PDF文档\n\n")
        
        # File inventory
        f.write("## 📁 FILE_INVENTORY (文件清单)\n\n")
        f.write("| # | 文件名 | 大小 | 类型 | 项目标签 |\n")
        f.write("|---|--------|------|------|----------|\n")
        for i, r in enumerate(results):
            tag_emoji = {"AHL": "🔵", "酒店AI": "🟢", "康养": "🟡", "重宾": "🟠", "其他": "⚪"}.get(r['tag'], "⚪")
            status = "✅" if not r['error'] else "❌"
            f.write(f"| {i+1} | {r['name']} | {r['size']} | PDF | {tag_emoji} {r['tag']} {status} |\n")
        
        f.write("\n---\n\n")
        
        # Individual file summaries
        for i, r in enumerate(results):
            f.write(f"## {i+1}. {r['name']}\n\n")
            f.write(f"- **路径**: {r['path']}\n")
            f.write(f"- **大小**: {r['size']}\n")
            f.write(f"- **类型**: {r['type']}\n")
            f.write(f"- **项目标签**: {r['tag']}\n")
            if r.get('pages'):
                f.write(f"- **页数**: {r['pages']}\n")
            f.write(f"- **提取字符数**: {r['raw_length']}\n")
            f.write(f"- **一句话总结**: {r['summary']}\n")
            f.write(f"- **核心内容**:\n")
            if r['error']:
                f.write(f"  - ⚠️ 文件处理错误: {r['error']}\n")
            elif r['bullets']:
                for b in r['bullets']:
                    b = b.strip()
                    if b:
                        # Truncate very long lines
                        if len(b) > 200:
                            b = b[:200] + "..."
                        f.write(f"  - {b}\n")
            else:
                f.write(f"  - (未能提取到有效内容)\n")
            f.write(f"\n---\n\n")
    
    print(f"\n✅ Done! Output written to: {output_path}")
    return results

if __name__ == "__main__":
    results = main()
    print("\n=== RESULTS SUMMARY ===")
    for r in results:
        status = "OK" if not r['error'] else f"ERROR: {r['error']}"
        print(f"  {r['name']}: {status}")
