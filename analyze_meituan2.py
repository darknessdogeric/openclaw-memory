import re

with open('cache/ota_monitor/meituan_sample_curl.html', 'r', encoding='utf-8') as f:
    html = f.read()

print(f'curl_cffi 样本: {len(html):,} chars')

# 找 script 标签中的 JSON
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
print(f'Script标签数: {len(scripts)}')

for i, s in enumerate(scripts):
    has_hotel = 'hotel' in s.lower() or 'poi' in s.lower() or 'room' in s.lower() or 'price' in s.lower()
    if has_hotel and len(s) > 300:
        print(f'\nScript[{i}] ({len(s):,} chars):')
        # 找JSON数据
        for kw in ['poiList','hotelList','\"list\"','\"data\"','\"hotel\"','\"rooms\"','\"roomPrice\"','poiInfos']:
            idx = s.find(f'"{kw}"')
            if idx >= 0:
                print(f'  >>> "{kw}" at pos {idx}')
                print(f'  {s[max(0,idx-20):idx+300]}')

# 全文关键词扫描
print('\n\n=== 全文关键词扫描 ===')
for kw in ['hotelName','hotel_name','poiName','roomPrice','price','rating','comment','address','roomList','hotelId','poiId']:
    cnt = html.count(kw)
    if cnt > 0:
        print(f'  "{kw}": {cnt} occurrences')

# 看看是不是有搜索表单
if 'search' in html.lower():
    searches = re.findall(r'(?:action|href|data-url|data-link)[^=]*=[\"\']([^\"\']*search[^\"\']*)', html, re.IGNORECASE)
    print(f'\n搜索URL候选: {searches[:5]}')
