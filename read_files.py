# -*- coding: utf-8 -*-
import os
import json

# Try to import PyPDF2 for PDF reading
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("PyPDF2 not available, using basic file info only")

# Read the explored data
with open('C:/Users/ericz/.openclaw/workspace/priority_explored.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Key files to read from each folder (selecting smaller, readable PDFs)
key_files = {
    '管理项目': [
        '张实主导酒店类项目展示.pdf',
        '2-中旅睿景酒店产品理念及设计原则.pdf',
        '酒店项目土建期策划方案.pdf',
        '酒店管理公司相关业务及取费标准.doc',
    ],
    '运营文件': [
        '2023年度年度经营业绩责任书-张实_20230706_0001.pdf',
        '酒店数字化线上运营思路及体系建设.pdf',
        '酒店经营半年经营情况分析.pdf',
    ],
    '中旅酒店相关内容': [
        '中旅各品牌酒店标准组织架构.pdf',
        'FO-SOP-FD-072客户偏好设置.doc',
    ],
    '中酒拓展': [
        '附件2：中高端有限服务酒店技术服务工作清单.pdf',
        '附件1：中旅酒店中高端有限服务酒店发展政策（2024）.pdf',
    ],
    '主要经营数据': [
        '主要经营数据3月.xlsx',
    ],
    '自我革命': [
        '下一代AI+去中心化旅行服务平台可行性研究.pdf',
        'AI赋能单体酒店营销全景整合方案：从被动接单到主动狩猎的全链路智能化转型.pdf',
        '重宾国际AI赋能方案.pdf',
        '单体酒店全面数字化+AI智能化转型通用实施方案.pdf',
    ],
    '襄阳共享国际文件': [
        '张实简历.pdf',
        '骏瑞大酒店项目前期定位策划咨询服务内容.pdf',
    ],
}

def read_pdf_basic(filepath):
    """Try to read PDF content"""
    if not PDF_AVAILABLE:
        return "[PDF reading not available]"
    
    try:
        with open(filepath, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            num_pages = len(pdf_reader.pages)
            
            # Extract text from first few pages
            text = ""
            for i in range(min(5, num_pages)):
                try:
                    page = pdf_reader.pages[i]
                    text += page.extract_text() + "\n"
                except:
                    pass
            
            return {
                'pages': num_pages,
                'preview': text[:2000] if text else "[No text extractable]"
            }
    except Exception as e:
        return {'error': str(e)}

def read_doc_basic(filepath):
    """Get basic info about doc files"""
    try:
        size = os.path.getsize(filepath)
        return {'size': size, 'note': 'DOC file - content extraction requires additional tools'}
    except Exception as e:
        return {'error': str(e)}

results = {}

for folder_name, files in key_files.items():
    print(f"\n{'='*60}")
    print(f"Processing: {folder_name}")
    print('='*60)
    
    folder_data = data.get(folder_name, {})
    folder_path = folder_data.get('path', '')
    
    results[folder_name] = {
        'folder': folder_name,
        'files_read': []
    }
    
    for filename in files:
        filepath = os.path.join(folder_path, filename)
        
        if not os.path.exists(filepath):
            print(f"  [NOT FOUND] {filename}")
            continue
        
        size_mb = os.path.getsize(filepath) / (1024*1024)
        print(f"  [READING] {filename} ({size_mb:.2f} MB)")
        
        if filename.endswith('.pdf'):
            content = read_pdf_basic(filepath)
        elif filename.endswith('.doc') or filename.endswith('.docx'):
            content = read_doc_basic(filepath)
        else:
            content = {'note': 'File type not supported for reading'}
        
        results[folder_name]['files_read'].append({
            'name': filename,
            'size_mb': round(size_mb, 2),
            'content': content
        })

# Save results
with open('C:/Users/ericz/.openclaw/workspace/files_content.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n\nResults saved to files_content.json")
