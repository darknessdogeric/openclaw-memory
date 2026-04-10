# -*- coding: utf-8 -*-
import urllib.request, ssl, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://r.jina.ai/http://hotels.ctrip.com/hotel/leshan0.html"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    resp = urllib.request.urlopen(req, timeout=15, context=ctx)
    content = resp.read().decode("utf-8", errors="ignore")
    
    # Find all text around '锦江'
    while "锦江" in content:
        idx = content.find("锦江")
        snippet = content[max(0,idx-100):idx+200]
        print("--- snippet ---")
        print(snippet)
        print()
        content = content[idx+3:]  # move past this occurrence
    
    # Also look for hotel detail page URLs
    print("\n\n=== HOTEL DETAIL URLs ===")
    detail_urls = re.findall(r'/hotel/[^"\']+/\d+', content)
    unique = list(set(detail_urls))
    print("Found %d detail URLs:" % len(unique))
    for u in unique[:10]:
        print("  " + u)
    
except Exception as e:
    print("Error: " + str(e))
