# -*- coding: utf-8 -*-
import urllib.request, ssl, re, json, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Ctrip hotel domestic city list - usually at this URL
city_list_url = "https://r.jina.ai/http://hotels.ctrip.com Domestic/HotelList"
# Try both
test_urls = [
    "https://r.jina.ai/http://hotels.ctrip.com Domestic/HotelList",
    "https://r.jina.ai/http://pages.ctrip.com/hotelapi/htllist", 
    # Try Ctrip's suggested URL pattern
    "https://r.jina.ai/http://hotels.ctrip.com/hotel/china/leshan.html",
    "https://r.jina.ai/http://hotels.ctrip.com/hotel/list/leshan.html",
]

for url in test_urls:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=10, context=ctx)
        content = resp.read().decode("utf-8", errors="ignore")
        print("URL: %s" % url[-40:])
        print("  Status: %d, Length: %d" % (resp.status, len(content)))
        # Look for Leshan
        if "乐山" in content:
            print("  [FOUND] 乐山 in content!")
            idx = content.find("乐山")
            print("  Context: " + content[max(0,idx-30):idx+50])
        elif len(content) > 100:
            print("  Content preview: " + content[100:400])
        print()
    except Exception as e:
        print("URL: %s" % url[-40:])
        print("  Error: " + str(e)[:50])
        print()
