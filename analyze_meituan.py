import re, json

with open('cache/ota_monitor/meituan_sample_pw.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 找 script 标签中的 JSON
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
print(f'Script标签数: {len(scripts)}')
for i, s in enumerate(scripts):
    if len(s) > 500:
        has_hotel = 'hotel' in s.lower() or 'poi' in s.lower() or 'room' in s.lower() or 'price' in s.lower()
        print(f'\n--- Script[{i}] ({len(s):,} chars) has_hotel={has_hotel} ---')
        if has_hotel:
            print(s[:800])
            # 尝试找 JSON 结构
            for key in ['poiList','hotelList','data','list','rooms','hotel','poiInfos']:
                idx = s.find(f'"{key}"')
                if idx >= 0:
                    print(f'  >>> found "{key}" at pos {idx}')
                    chunk = s[idx:idx+400]
                    print(f'  {chunk}')
                    break

# 也搜下全文中的关键字段
print('\n\n=== 全文关键词扫描 ===')
for kw in ['hotelName','hotel_name','poiName','roomPrice','price','rating','comment','address','roomList']:
    cnt = html.count(kw)
    if cnt > 0:
        print(f'  "{kw}": {cnt} occurrences')
