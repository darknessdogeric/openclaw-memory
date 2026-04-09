# -*- coding: utf-8 -*-
import urllib.request, ssl, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Test the found corporate Ctrip URLs with Jina
test_urls = [
    ("Corporate Ctrip detail", "http://hotels.corporatetravel.hotels.ctrip.com/hotels/detailPage?hotelId=15829637"),
    ("Corporate Ctrip pic", "https://hotels.corporatetravel.ctrip.com/pic-pid15b15c6e0349428ab53f135a34d62385/18374.html"),
]

for name, url in test_urls:
    print("=== " + name + " ===")
    try:
        jina_url = "https://r.jina.ai/" + url
        req = urllib.request.Request(jina_url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        content = resp.read().decode("utf-8", errors="ignore")
        print("Status: %d, Length: %d" % (resp.status, len(content)))
        
        # Look for hotel name, price, score
        if "锦江" in content or "嘉州" in content:
            print("  [FOUND] 锦江/嘉州 mentioned!")
            idx = content.find("锦江") if "锦江" in content else content.find("嘉州")
            print("  Context: " + content[max(0,idx-50):idx+100])
        
        # Extract prices
        prices = re.findall(r'¥\s*(\d+)', content)
        if prices:
            valid = [p for p in prices if 80 < int(p) < 2000]
            print("  Prices: " + ", ".join(valid[:8]))
        
        # Extract scores
        scores = re.findall(r'(\d\.\d)\s*(?:分|分满意)', content)
        if scores:
            print("  Scores: " + ", ".join(scores[:5]))
        
        # Show preview
        print("  Preview: " + content[:400].replace('\n', ' '))
        print()
        
    except Exception as e:
        print("Error: " + str(e))
        print()
