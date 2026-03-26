# -*- coding: utf-8 -*-
import pdfplumber, os, json

files = [
    (r'C:\Users\ericz\Desktop\自我革命\下一代AI+去中心化旅行服务平台\基本成品\AHL通用产品方案_V3_专业版.pdf', 'AHL产品方案'),
    (r'C:\Users\ericz\Desktop\自我革命\单体酒店专题\AI 驱动的酒店周边客户挖掘解决方案.pdf', 'AI周边客户挖掘'),
    (r'C:\Users\ericz\Desktop\自我革命\商业计划书\AI赋能酒店营销全景整合方案商业计划书.pdf', '酒店营销全景整合'),
    (r'C:\Users\ericz\Desktop\自我革命\商业计划书\单体酒店数智化商业计划书.pdf', '单体酒店数智化'),
    (r'C:\Users\ericz\Desktop\自我革命\AI单体酒店获客\酒店数智化获客定位与逻辑蓝图.pdf', '星旗AI合伙人'),
]

output_base = r'C:\Users\ericz\.openclaw\workspace\temp_extracted'
os.makedirs(output_base, exist_ok=True)

results = []

for path, label in files:
    if not os.path.exists(path):
        results.append({'label': label, 'status': 'NOT FOUND', 'text': ''})
        continue
    
    size = os.path.getsize(path)
    with pdfplumber.open(path) as pdf:
        total_pages = len(pdf.pages)
        text_parts = []
        for page in pdf.pages:
            t = page.extract_text() or ''
            text_parts.append(t)
    
    full_text = '\n'.join(text_parts)
    
    # Save to file
    out_file = os.path.join(output_base, '%s.txt' % label)
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    results.append({
        'label': label,
        'status': 'OK',
        'size': size,
        'pages': total_pages,
        'chars': len(full_text),
        'text': full_text[:3000],  # First 3000 chars
        'out_file': out_file
    })
    print('[%s] %dKB, %d pages, %d chars -> %s' % (label, size//1024, total_pages, len(full_text), out_file))

# Save results JSON
json_out = os.path.join(output_base, 'extraction_results.json')
with open(json_out, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print('\nResults saved to:', json_out)
