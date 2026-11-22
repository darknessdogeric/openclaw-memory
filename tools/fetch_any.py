# -*- coding: utf-8 -*-
"""fetch_any.py v2 — 多级反爬抓取管道
tier1 Scrapling StealthyFetcher (camoufox/补丁浏览器)
tier2 Playwright 直连（chromium + stealth args）
tier3 curl_cffi (TLS 指纹伪装)
tier4 requests
timeout 一律毫秒
"""
import os, re, json, hashlib
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/126.0.0.0 Safari/537.36")
def clean(h):
    h = re.sub(r"(?is)<script.*?</script>|<style.*?</style>|<noscript.*?</noscript>|<!--.*?-->", " ", h or "")
    h = re.sub(r"(?s)<[^>]+>", " ", h)
    h = re.sub(r"[ \t\xa0\u3000]+", " ", h)
    h = re.sub(r"\n\s*\n\s*\n+", "\n\n", h)
    return h.strip()
def _t1(url, ms):
    try:
        from scrapling.fetchers import StealthyFetcher
        p = StealthyFetcher.fetch(url, headless=True, network_idle=True, timeout=ms,
                                 stealthy_headers=True, disable_resources=True)
        h = getattr(p, "html_content", None) or str(p)
        if h and len(h) > 1500:
            return h, "t1-stealthy"
    except Exception as e:
        pass
    return None, ""
def _t2(url, ms):
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            br = pw.chromium.launch(headless=True, args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox", "--disable-dev-shm-usage",
                "--disable-gpu", "--lang=zh-CN"])
            ctx = br.new_context(viewport={"width":1440,"height":900},
                user_agent=UA, locale="zh-CN", timezone_id="Asia/Shanghai")
            ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
            pg = ctx.new_page()
            pg.goto(url, wait_until="domcontentloaded", timeout=ms)
            pg.wait_for_timeout(2600)
            h = pg.content()
            br.close()
            if h and len(h) > 1500:
                return h, "t2-playwright"
    except Exception as e:
        pass
    return None, ""
def _t3(url, ms):
    try:
        from curl_cffi import requests as cr
        r = cr.get(url, impersonate="chrome", timeout=ms/1000,
                   headers={"User-Agent": UA, "Accept-Language":"zh-CN,zh;q=0.9",
                            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"})
        if r.status_code < 400 and len(r.text) > 1200:
            return r.text, "t3-curl_cffi"
    except Exception:
        pass
    return None, ""
def _t4(url, ms):
    try:
        import requests
        r = requests.get(url, timeout=ms/1000, headers={"User-Agent": UA,
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"})
        if r.status_code < 400 and len(r.text) > 1200:
            r.encoding = r.apparent_encoding or "utf-8"
            return r.text, "t4-requests"
    except Exception:
        pass
    return None, ""
def fetch_html(url, ms=45000, tiers=(1,2,3,4)):
    errs=[]
    for t in tiers:
        f = {1:_t1,2:_t2,3:_t3,4:_t4}[t]
        h, how = f(url, ms)
        if h:
            return h, how
        errs.append("t%d:fail" % t)
    return "", "|".join(errs)
def fetch_text(url, ms=45000, tiers=(1,2,3,4)):
    h, how = fetch_html(url, ms, tiers)
    return (clean(h) if h else ""), how
if __name__ == "__main__":
    import sys as _s
    OUT = r"D:\B166ER-openclaw\workspace\memory\_fetched"
    os.makedirs(OUT, exist_ok=True)
    for u in _s.argv[1:]:
        t, how = fetch_text(u)
        tag = hashlib.md5(u.encode()).hexdigest()[:8]
        open(os.path.join(OUT, tag + ".txt"), "w", encoding="utf-8").write(
            "# URL: " + u + "\n# METHOD: " + how + "\n# LEN: " + str(len(t)) + "\n\n" + t)
        print("%s len=%6d  %-16s %s" % (tag, len(t), how, u[:88]))
