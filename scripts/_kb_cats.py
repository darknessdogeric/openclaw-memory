import os
cats = {'personality':0,'hotel':0,'ai':0,'game':0,'finance':0,'fundraising':0,'aesthetic':0,'token':0,'tools':0,'daily':0,'other':0}
for root,dirs,files in os.walk('memory'):
    for f in files:
        if f.endswith('.md'):
            fp = os.path.join(root,f)
            sz = os.path.getsize(fp)
            nm = f.lower()
            if 'soul' in nm or 'user' in nm or 'identity' in nm or 'memory' in nm or 'agents' in nm.lower(): cats['personality']+=sz
            elif 'hotel' in nm or 'ota' in nm or 'pms' in nm or 'sop' in nm or 'hl' in nm or 'homestay' in nm or 'resort' in nm or 'apartment' in nm: cats['hotel']+=sz
            elif 'ai' in nm or 'llm' in nm: cats['ai']+=sz
            elif 'game' in nm: cats['game']+=sz
            elif 'finance' in nm or 'quant' in nm or 'secur' in nm or 'pric' in nm: cats['finance']+=sz
            elif 'fund' in nm or 'startup' in nm: cats['fundraising']+=sz
            elif 'aes' in nm or 'music' in nm: cats['aesthetic']+=sz
            elif 'token' in nm: cats['token']+=sz
            elif 'skill' in nm or 'B166ER' in nm or 'auto' in nm or 'upgrade' in nm or '检查' in nm: cats['tools']+=sz
            elif any(d in nm for d in ['2026-03','2026-04','2026-05','2026-02','2026-']): cats['daily']+=sz
            else: cats['other']+=sz

for k,v in sorted(cats.items(), key=lambda x:-x[1]):
    name = {'personality':'SOUL/MEMORY/USER','hotel':'酒店行业知识','ai':'AI/LLM技术','game':'博弈论决策','finance':'金融/定价','fundraising':'创业融资','aesthetic':'审美/音乐','token':'Token经济','tools':'工具/SOP','daily':'日记/日报','other':'其他'}[k]
    print(f'{name:>20}: {v//1024:>4}KB')
total = sum(cats.values())
print(f'{"TOTAL":>20}: {total//1024:>4}KB')
