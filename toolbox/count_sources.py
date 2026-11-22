import yaml
with open(r'D:\B166ER-OpenClaw\workspace\trendradar\config\config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# RSS
rss = config.get('rss', {})
feeds = rss.get('feeds', [])
enabled_feeds = [f for f in feeds if f.get('enabled', True)]

print(f'=== RSS feeds ===')
print(f'  Total configured: {len(feeds)}')
print(f'  Enabled: {len(enabled_feeds)}')

# Group by [X] prefix (A=hotel, B=macro, C=AI, D=geo)
cats = {}
for f in enabled_feeds:
    name = f.get('name', '?')
    # Extract [X] prefix
    if name.startswith('[') and ']' in name:
        cat = name[1:name.index(']')]
        rest = name[name.index(']')+1:].strip()
    else:
        cat = 'X'
        rest = name
    cats.setdefault(cat, []).append(rest)

print(f'\n=== By category ===')
for cat in sorted(cats.keys()):
    print(f'  [{cat}] {len(cats[cat])} sources:')
    for n in cats[cat]:
        print(f'    - {n}')

# Platforms
platforms = config.get('platforms', {})
plat_sources = platforms.get('sources', [])
print(f'\n=== Platforms: {len(plat_sources)} ===')
for p in plat_sources:
    print(f'  - {p.get("id")}: {p.get("name")}')