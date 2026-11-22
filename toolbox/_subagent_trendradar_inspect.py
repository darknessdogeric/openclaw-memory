"""Inspect raw scan results"""
import json
d = json.load(open(r'D:\B166ER-OpenClaw\workspace\toolbox\_subagent_trendradar_raw.json', encoding='utf-8'))

# Topics
x = d[0]
print('=== TOP 15 TOPICS (auto_extract daily) ===')
for i, t in enumerate(x['data']['topics'], 1):
    print(f"  {i:2d}. {t['keyword']:20s} freq={t['frequency']:3d} matched={t['matched_news']:3d} trend={t['trend']}")

# Hotel
print()
print('=== HOTEL SENTIMENT ===')
print(json.dumps(d[1]['data'], ensure_ascii=False, indent=2))

# AI
print()
print('=== AI SENTIMENT (data array) ===')
ai = d[2]['data']['data']
print('count:', len(ai))
if ai:
    print('sample[0]:')
    print(json.dumps(ai[0], ensure_ascii=False, indent=2)[:800])

# REITs
print()
print('=== REITs TREND (data) ===')
print(json.dumps(d[3]['data']['data'], ensure_ascii=False, indent=2)[:2000])

# Oil
print()
print('=== OIL TREND (data) ===')
print(json.dumps(d[4]['data']['data'], ensure_ascii=False, indent=2)[:2000])

# Latest news
print()
print('=== LATEST NEWS (first 5 items) ===')
ln = d[5]['data']['data']
print('count:', len(ln))
for i, n in enumerate(ln[:5], 1):
    print(f'  [{i}]', json.dumps(n, ensure_ascii=False)[:400])