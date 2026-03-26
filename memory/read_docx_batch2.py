import json
from docx import Document
import os

with open(r'C:\Users\ericz\.openclaw\workspace\memory\docx_files.json', 'r', encoding='utf-8') as f:
    files = json.load(f)

# Map task names to actual file paths
task_mapping = {
    "AI+实体酒店解决方案.docx": "AI+实体酒店解决计划.docx",
    "AI酒店行业应用方案.docx": "AI酒店行业应用趋势.docx",
    "下一代AI+去中心化旅行平台商业计划.docx": "下一代AI+去中心化旅游平台商业计划.docx",
    "单体酒店数智化商业计划书.docx": "单体酒店数智化商业计划书.docx",
    "亚朵营收分析商业计划书.docx": None,  # does not exist
    "AI赋能酒店营销.docx": "AI赋能酒店营销.docx",
    "AI赋能酒店收益.docx": None,  # does not exist
    "AI赋能酒店前厅.docx": None,  # does not exist (has 房务 not 前厅)
    "AI赋能酒店人资.docx": "AI赋能酒店人资.docx",
    "酒店直客全生命周期数字化.docx": "酒店直客全生命周期数字化.docx",
}

results = []
for task_name, actual_name in task_mapping.items():
    if actual_name is None:
        results.append({
            'task_name': task_name,
            'status': 'NOT_FOUND',
            'reason': 'file does not exist on disk'
        })
        continue
    
    matched = [f for f in files if f['name'] == actual_name]
    if matched:
        f = matched[0]
        try:
            doc = Document(f['full'])
            text = '\n'.join([p.text for p in doc.paragraphs if p.text.strip()])
            results.append({
                'task_name': task_name,
                'status': 'OK',
                'full_path': f['full'],
                'rel_path': f['rel'],
                'name': f['name'],
                'size_kb': f['size_kb'],
                'text_len': len(text),
                'preview': text[:500]
            })
        except Exception as e:
            results.append({
                'task_name': task_name,
                'status': 'ERROR',
                'error': str(e),
                'full_path': f['full']
            })
    else:
        results.append({
            'task_name': task_name,
            'status': 'NOT_FOUND',
            'actual_name_searched': actual_name
        })

with open(r'C:\Users\ericz\.openclaw\workspace\memory\docx_content_batch2.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Processed {len(results)} files")
for r in results:
    print(f"{r['status']}|{r['task_name']}")
