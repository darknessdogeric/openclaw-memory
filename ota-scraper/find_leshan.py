# -*- coding: utf-8 -*-
import urllib.request, ssl, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Try to find Leshan on Ctrip
# ershan page showed interesting results - let me check it
urls_to_try = [
    ("ershan_html", "https://r.jina.ai/http://hotels.ctrip.com/hotel/ershan.html"),
    ("leshan0_html", "https://r.jina.ai/http://hotels.ctrip.com/hotel/leshan0.html"),
    ("leshan_html", "https://r.jina.ai/http://hotels.ctrip.com/hotel/leshan.html"),
    ("emeishan", "https://r.jina.ai/http://hotels.ctrip.com/hotel/emeishan.html"),
    ("songjiagang", "https://r.jina.ai/http://hotels.ctrip.com/hotel/songjiagang.html"),
    ("leshan_specific", "https://r.jina.ai/http://hotels.ctrip.com/hotel/leshan38/138411.html"),
]

for name, url in urls_to_try:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=12, context=ctx)
        content = resp.read().decode("utf-8", errors="ignore")
        print("=== %s (%d chars) ===" % (name, len(content)))
        
        # Get title
        title_m = re.search(r'Title:\s*([^\n]+)', content)
        if title_m:
            print("  Title: " + title_m.group(1)[:80])
        
        # Check city keywords
        cities = {"乐山": False, "贵阳": False, "峨眉山": False, "宋家岗": False, "凯里": False, "黔东南": False}
        for c in cities:
            cities[c] = c in content
        print("  Cities: " + str(cities))
        
        # Find hotel names in links
        hotels = re.findall(r'hotel/[^"\']+">([^<]{2,20})</a>', content)
        unique_hotels = list(set([h for h in hotels if len(h) > 3 and not h.startswith('http')]))[:8]
        if unique_hotels:
            print("  Hotels: " + ", ".join(unique_hotels))
        
        # Find prices
        prices = re.findall(r'¥\s*(\d+)', content)
        prices = [p for p in prices if 80 < int(p) < 2000]
        if prices:
            print("  Prices: " + ", ".join(prices[:8]))
        
        # Look for JJJZ hotel
        jjiz = "锦江" in content or "嘉州" in content or "jjjz" in content.lower() or "jjiazhou" in content.lower()
        print("  Has JJJZ hotel: " + str(jjiz))
        
        print()
    except Exception as e:
        print("=== %s: ERROR %s" % (name, str(e)[:50]))
        print()
