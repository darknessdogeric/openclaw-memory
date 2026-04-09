# -*- coding: utf-8 -*-
import urllib.request, urllib.parse, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

query = urllib.parse.quote('锦江嘉州宾馆 携程')
url = f'https://r.jina.ai/http://www.baidu.com/s?wd={query}'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    resp = urllib.request.urlopen(req, timeout=15)
    content = resp.read().decode('utf-8', errors='ignore')
    
    # Find URLs with ctrip
    ctrip = re.findall(r'https?://[^\s"\'<>]*ctrip[^\s"\'<>]*', content)
    
    # Find URLs with hotel/hotels
    hotel = re.findall(r'https?://[^\s"\'<>]*(?:hotel|hotels)[^\s"\'<>]*', content)
    
    print('Results from Baidu search via Jina:')
    print('URLs with ctrip: %d' % len(ctrip))
    for u in ctrip[:5]:
        print('  ' + u[:100])
    print('URLs with hotel: %d' % len(hotel))
    for u in hotel[:3]:
        print('  ' + u[:100])
    print('')
    print('Content preview (first 600 chars):')
    print(content[:600])
    
    # Save full content
    with open('baidu_search_content.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    print('\nSaved to baidu_search_content.txt')
    
except Exception as e:
    print('Error: ' + str(e))
