"""盘点 B166ER 实际信源矩阵的全貌"""
import yaml
from pathlib import Path

# === 1. 酒店行业 28 信源 (hotel_sources.py) ===
hotel_src_path = Path(r'D:\B166ER-OpenClaw\workspace\toolbox\hotel_sources.py')
print('=== 1. 酒店行业 28 信源 (hotel_sources.py) ===')
src_count = hotel_src_path.read_text(encoding='utf-8').count('"credibility":')
print(f'  hotel_sources.py 中的信源数: {src_count}')

# === 2. TrendRadar RSS (config.yaml) ===
print('\n=== 2. TrendRadar RSS 信源 (config.yaml) ===')
with open(r'D:\B166ER-OpenClaw\workspace\trendradar\config\config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
rss_feeds = config.get('rss', {}).get('feeds', [])
enabled_rss = [f for f in rss_feeds if f.get('enabled', True)]
print(f'  RSS 总配置: {len(rss_feeds)} 个')
print(f'  RSS 已启用: {len(enabled_rss)} 个')

# Group by [X]
cats = {}
for f in enabled_rss:
    name = f.get('name', '?')
    if name.startswith('[') and ']' in name:
        cat = name[1:name.index(']')]
        rest = name[name.index(']')+1:].strip()
    else:
        cat = 'X'
        rest = name
    cats.setdefault(cat, []).append(rest)
for cat in sorted(cats.keys()):
    print(f'  [{cat}] {len(cats[cat])} 个: {", ".join(cats[cat][:5])}{"..." if len(cats[cat]) > 5 else ""}')

# === 3. TrendRadar 平台 (config.yaml) ===
print('\n=== 3. TrendRadar 平台热搜 (config.yaml) ===')
plat_sources = config.get('platforms', {}).get('sources', [])
print(f'  平台: {len(plat_sources)} 个')
for p in plat_sources:
    print(f'  - {p.get("id")}: {p.get("name")}')

# === 4. frequency_words 关键词覆盖 ===
print('\n=== 4. frequency_words.txt 关键词覆盖 ===')
fw_path = Path(r'D:\B166ER-OpenClaw\workspace\trendradar\config\frequency_words.txt')
fw_content = fw_path.read_text(encoding='utf-8')
sections = fw_content.split('# ============')
print(f'  分段数: {len(sections)}')
total_kw = sum(len(s.split(",")) for s in sections)
print(f'  关键词总数: ~{total_kw}')

# === 总计 ===
print('\n=== 总计 ===')
total = src_count + len(enabled_rss) + len(plat_sources)
print(f'  酒店行业 (hotel_sources.py): {src_count}')
print(f'  RSS (enabled):                {len(enabled_rss)}')
print(f'  平台热搜:                       {len(plat_sources)}')
print(f'  -- 广义信源总数: {total}')
print(f'  -- 加 frequency_words: ~{total_kw} 关键词 增强覆盖')