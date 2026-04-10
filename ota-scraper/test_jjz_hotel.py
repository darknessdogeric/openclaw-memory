# -*- coding: utf-8 -*-
import urllib.request, ssl, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

hotel_urls = [
    ("Main Ctrip (73690948)", "https://r.jina.ai/https://hotels.ctrip.com/hotels/73690948.html"),
    ("Main Ctrip HTTP", "http://r.jina.ai/http://hotels.ctrip.com/hotels/73690948.html"),
    ("Corporate Ctrip", "https://r.jina.ai/https://hotels.corporatetravel.ctrip.com/hotels/73690948.html"),
    ("Mobile Ctrip", "https://r.jina.ai/https://wap.ctrip.com/html5/hotel/hoteldetail/dianping/73690948.html"),
]

for name, url in hotel_urls:
    print("="*60)
    print(name)
    print("="*60)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        content = resp.read().decode("utf-8", errors="ignore")
        print("Status: %d, Length: %d" % (resp.status, len(content)))
        
        # Check for bot detection
        if '404' in content[:200] or 'Bad Request' in content[:200]:
            print("  [ERROR] Invalid URL or 404")
        
        # Look for key data
        has_name = "锦江嘉州" in content or "锦江" in content
        print("  Has 锦江 keyword: " + str(has_name))
        
        # Prices
        prices = re.findall(r'¥\s*(\d+)', content)
        valid_prices = [p for p in prices if 80 < int(p) < 2000]
        if valid_prices:
            print("  Prices found: " + ", ".join(valid_prices[:8]))
        
        # Scores
        scores = re.findall(r'(\d\.\d)\s*(?:分|分满意)', content)
        if scores:
            print("  Scores found: " + ", ".join(scores[:5]))
        
        # Extract text content for review
        # Remove HTML tags and show meaningful text
        text_lines = [l.strip() for l in content.split('\n') if len(l.strip()) > 10]
        meaningful = [l for l in text_lines if not l.startswith('http') and len(l) > 5][:15]
        print("  Content preview:")
        for line in meaningful[:8]:
            print("    " + line[:80])
        
        print()
    except Exception as e:
        print("Error: " + str(e))
        print()
