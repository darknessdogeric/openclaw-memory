# -*- coding: utf-8 -*-
import urllib.request, urllib.parse, ssl, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Target: Leshan hotel list on Ctrip
# leshan city id seems to be 38 (similar to guiyang 38 pattern)
url = "https://r.jina.ai/http://hotels.ctrip.com/hotel/leshan38.html"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    resp = urllib.request.urlopen(req, timeout=20, context=ctx)
    content = resp.read().decode("utf-8", errors="ignore")
    print("Got %d chars of content" % len(content))
    
    # Save full content
    with open("ctrip_leshan_content.txt", "w", encoding="utf-8") as f:
        f.write(content)
    print("Saved to ctrip_leshan_content.txt")
    
    # Extract hotel names
    hotel_names = re.findall(r'<a[^>]+href="/hotel/[^"]*"[^>]*>([^<]{4,30})</a>', content)
    print("\nHotel names found (%d):" % len(set(hotel_names)))
    for n in list(set(hotel_names))[:20]:
        if len(n) > 3 and not n.startswith('http'):
            print("  " + n)
    
    # Extract prices
    prices = re.findall(r'[¥￥]?\s*(\d{3,5})\s*(?:元|起)?', content)
    valid_prices = [p for p in prices if 80 < int(p) < 2000]
    print("\nPrices found (%d valid):" % len(valid_prices))
    print("  " + ", ".join(valid_prices[:15]))
    
    # Extract scores
    scores = re.findall(r'(\d\.\d)\s*(?:分|分满意)', content)
    print("\nScores found (%d):" % len(scores))
    print("  " + ", ".join(scores[:10]))
    
    # Look for 锦江嘉州
    if "锦江" in content or "嘉州" in content:
        print("\n[FOUND] Page mentions '锦江' or '嘉州'!")
        idx = content.find("锦江")
        if idx > 0:
            print("  Context: ..." + content[max(0,idx-50):idx+100] + "...")
    else:
        print("\n[NOT FOUND] '锦江' not found in page")
    
    # Show first 1000 chars of content
    print("\n--- Content Preview ---")
    print(content[:1000])
    
except Exception as e:
    print("Error: " + str(e))
