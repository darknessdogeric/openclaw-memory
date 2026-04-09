# -*- coding: utf-8 -*-
import urllib.request, urllib.parse, ssl, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Test Jina on different hotel search URLs
test_urls = [
    ("Ctrip hotel search", "https://r.jina.ai/http://hotels.ctrip.com/hotel/search?city=%E4%B9%90%E5%B1%B1&checkIn=2026-04-10&checkOut=2026-04-11&rooms=1"),
    ("Ctrip hotel leshan", "https://r.jina.ai/http://hotels.ctrip.com/hotel/leshan38.html"),
]

for name, url in test_urls:
    print("Testing: " + name)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        content = resp.read().decode("utf-8", errors="ignore")
        print("  Status: %d, Length: %d" % (resp.status, len(content)))
        print("  Preview: " + content[:400])
        print()
    except Exception as e:
        print("  Error: " + str(e))
        print()
