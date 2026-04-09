"""
OTA Scraper - Multi-Approach Tester
Strategy: Jina Reader (no browser) -> Playwright Stealth (local IP) -> Proxy if needed
"""
import urllib.request, urllib.error, time, json, re, sys

def jina_read(url, timeout=15):
    """Use Jina AI reader to get clean HTML text"""
    try:
        req = urllib.request.Request(
            'https://r.jina.ai/' + url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/plain',
            }
        )
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return f"[JINA ERROR] {e}"

def extract_hotel_data(text, source):
    """Extract hotel name, price, score from text"""
    results = {}
    lines = [l.strip() for l in text.split('\n') if len(l.strip()) > 5]
    
    # Try to find hotel name
    for line in lines[:20]:
        if any(k in line for k in ['酒店', 'Hotel', 'hotel']):
            results['name'] = line[:80]
            break
    
    # Try to find price
    price_pattern = re.compile(r'[¥￥$]?\s*(\d+(?:\.\d+)?)\s*(?:元|/晚|起)?')
    for line in lines:
        m = price_pattern.search(line)
        if m and 50 < float(m.group(1)) < 10000:
            results['price'] = m.group(1)
            break
    
    # Try to find score
    score_pattern = re.compile(r'(\d+\.?\d*)\s*分')
    for line in lines:
        m = score_pattern.search(line)
        if m and 3 < float(m.group(1)) < 5.5:
            results['score'] = m.group(1)
            break
    
    return results

def test_jina_on_ctrip():
    """Test Jina on Ctrip hotel page"""
    print("\n=== Test 1: Jina Reader on 携程 ===")
    url = "https://you.ctrip.com/hotel/china3/24745.html"
    text = jina_read(url)
    data = extract_hotel_data(text, 'ctrip')
    print(f"  URL: {url}")
    print(f"  Text length: {len(text)} chars")
    print(f"  Extracted: {data}")
    if text and len(text) > 100:
        print(f"  Preview: {text[:200]}")
    return len(text) > 200

def test_jina_on_qunar():
    """Test Jina on Qunar hotel search"""
    print("\n=== Test 2: Jina Reader on 去哪儿 ===")
    url = "https://www.qunar.com/hotel/"
    text = jina_read(url)
    data = extract_hotel_data(text, 'qunar')
    print(f"  URL: {url}")
    print(f"  Text length: {len(text)} chars")
    print(f"  Extracted: {data}")
    return len(text) > 200

def test_ctrip_hotel_detail():
    """Test a specific Ctrip hotel detail page"""
    print("\n=== Test 3: Jina Reader on 携程酒店详情 ===")
    # 锦江嘉州宾馆 - from previous context
    url = "https://you.ctrip.com/hotel/leshan34/138411.html"
    text = jina_read(url)
    data = extract_hotel_data(text, 'ctrip_detail')
    print(f"  URL: {url}")
    print(f"  Text length: {len(text)} chars")
    print(f"  Extracted: {data}")
    if text and len(text) > 100:
        print(f"  Preview: {text[:300]}")
    return len(text) > 200

def test_ctrip_search():
    """Test Ctrip hotel search results"""
    print("\n=== Test 4: Jina Reader on 携程搜索页 ===")
    # Search for 乐山 酒店
    url = "https://you.ctrip.com/hotel/leshan34.html"
    text = jina_read(url)
    data = extract_hotel_data(text, 'ctrip_search')
    print(f"  URL: {url}")
    print(f"  Text length: {len(text)} chars")
    print(f"  Extracted: {data}")
    return len(text) > 200

if __name__ == '__main__':
    print("=" * 60)
    print("OTA Scraper - Jina Reader Approach Test")
    print("=" * 60)
    
    results = []
    results.append(("携程酒店", test_ctrip_hotel_detail()))
    results.append(("携程搜索", test_ctrip_search()))
    results.append(("去哪儿", test_jina_on_qunar()))
    
    print("\n" + "=" * 60)
    print("RESULTS:")
    for name, ok in results:
        status = "✅ PASS" if ok else "❌ FAIL"
        print(f"  {status}  {name}")
    print("=" * 60)
