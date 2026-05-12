# -*- coding: utf-8 -*-
"""携程价格: 详情页 + 移动API 双路径"""
import sys, os, time, re, urllib.request
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapling.fetchers import StealthyFetcher
from bs4 import BeautifulSoup
import concurrent.futures

try: loop = __import__('asyncio').get_running_loop()
except: loop = None

# ═══════════ 路径1: 酒店详情页 ═══════════
print("="*70)
print("路径1: 携程详情页 (hotel/84005623.html)")
print("="*70)
url_detail = "https://hotels.ctrip.com/hotel/84005623.html"
t0 = time.time()
def f1(): return StealthyFetcher.fetch(url_detail, headless=True, wait=10000)
if loop:
    with concurrent.futures.ThreadPoolExecutor() as ex:
        pd = ex.submit(f1).result(timeout=45)
else: pd = f1()
print(f"抓取: {time.time()-t0:.1f}s, HTML: {len(pd.html_content):,} chars")

soup = BeautifulSoup(pd.html_content, 'html.parser')
text = pd.get_all_text()

# 找价格
prices_detail = re.findall(r'[¥￥]\s*(\d{2,6})', text)
prices_qi = re.findall(r'(\d{3,6})\s*(?:元|起)', text)
print(f"¥价格: {prices_detail[:10]}")
print(f"XX元/起: {prices_qi[:10]}")

# 找script中的价格JSON
for s in soup.find_all('script'):
    txt = s.string or ''
    if 'price' in txt.lower() and len(txt) > 200:
        price_data = re.findall(r'"price"\s*:\s*(\d+\.?\d*)', txt)
        if price_data:
            print(f"Script price: {price_data[:10]}")

# ═══════════ 路径2: 移动端API ═══════════
print(f"\n{'='*70}")
print("路径2: 携程移动端API")
print("="*70)
# 已知hotel ID，尝试直接调用价格API
import json as _json

api_urls = [
    # 移动端酒店详情API
    ("https://m.ctrip.com/restapi/soa2/13444/json/getHotelDetail", 
     '{"hotelId":84005623,"head":{"cid":"09031143413892357653","ctok":"","cver":"1.0","lang":"01","sid":"","syscode":"09","auth":"","extension":[]}}'),
    # 酒店价格API
    ("https://m.ctrip.com/restapi/soa2/13444/json/getHotelPrice",
     '{"hotelId":84005623,"head":{"cid":"09031143413892357653","ctok":"","cver":"1.0","lang":"01","sid":"","syscode":"09","auth":"","extension":[]}}'),
    # 酒店列表价格  
    ("https://m.ctrip.com/restapi/soa2/13444/json/getHotelPriceList",
     '{"hotelIds":[84005623],"head":{"cid":"09031143413892357653","ctok":"","cver":"1.0","lang":"01","sid":"","syscode":"09","auth":"","extension":[]}}'),
]

for api_url, payload in api_urls:
    try:
        data = payload.encode('utf-8')
        req = urllib.request.Request(api_url, data=data, 
            headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=15)
        body = resp.read().decode('utf-8', errors='replace')
        print(f"\n  {api_url.split('/')[-1]}: {resp.status} ({len(body)}B)")
        if 'price' in body.lower() or 'rate' in body.lower():
            print(f"  ⭐ 含价格!")
            try:
                j = _json.loads(body)
                print(_json.dumps(j, ensure_ascii=False, indent=2)[:400])
            except:
                print(f"  {body[:300]}")
        else:
            print(f"  {body[:150]}")
    except Exception as e:
        print(f"  {api_url.split('/')[-1]}: {str(e)[:80]}")
