import docx, os

files = [
    (r'C:\Users\ericz\Desktop\产业发展部\项目\新启航酒旅\审议《关于安逸酒店集团有限责任共公司与四川新启航酒旅企业管理有限公司签订酒店品牌运营及酒旅新零售合作框架协议》得议案.docx', '_parsed_xqh_议案.txt'),
    (r'C:\Users\ericz\Desktop\产业发展部\项目\新启航酒旅\安逸-新启航-酒店品牌运营及酒旅新零售合作框架协议（20260831）.docx', '_parsed_xqh_协议.txt'),
]

for src, dst in files:
    if not os.path.exists(src):
        print(f'MISSING: {src}')
        continue
    d = docx.Document(src)
    out = [f'=== {os.path.basename(src)} ===', f'段落数:{len(d.paragraphs)} 表格数:{len(d.tables)}', '']
    for i, p in enumerate(d.paragraphs):
        t = p.text.strip()
        if t:
            out.append(f'[{i:03d}] {t}')
    for ti, tb in enumerate(d.tables):
        out.append(f'-- 表格{ti} ({len(tb.rows)}r x {len(tb.columns)}c) --')
        for ri, row in enumerate(tb.rows):
            cells = [c.text.strip().replace(chr(10), ' / ') for c in row.cells]
            out.append(f'  [{ri}] ' + ' | '.join(cells))
    target = os.path.join(os.path.dirname(src), dst)
    with open(target, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    print(f'WROTE: {dst} ({len(out)} lines)')