# -*- coding: utf-8 -*-
"""地图 POI 探针：高德 / 百度 酒店检索"""
import sys, asyncio, json, re, io
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

OUT = r'D:\B166ER-OpenClaw\workspace\.tmp\map_probe.json'
res = []

TARGETS = [
  ("高德-成都酒店", "https://www.amap.com/search?query=%E9%85%92%E5%BA%97&city=%E6%88%90%E9%83%BD"),
  ("百度-成都酒店", "https://map.baidu.com/search/%E9%85%92%E5%BA%97/@11562918.11,3556807.58,12z?querytype=s&wd=%E9%85%92%E5%BA%97&c=75"),
]

async def go():
    async with async_playwright() as p:
        br = await p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled","--no-sandbox"])
        ctx = await br.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width":1440,"height":900}, locale="zh-CN")
        await ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
        for name, url in TARGETS:
            page = await ctx.new_page()
            rec = {"name": name, "url": url}
            try:
                r = await page.goto(url, timeout=45000, wait_until="domcontentloaded")
                await page.wait_for_timeout(8000)
                rec["status"] = r.status if r else None
                rec["final_url"] = page.url
                rec["title"] = (await page.title())[:80]
                txt = await page.inner_text("body")
                rec["text_len"] = len(txt)
                rec["text_head"] = txt[:400].replace("\n", " / ")
                counts = re.findall(r"[约共]?\s*(\d[\d,]{1,7})\s*(?:个|家|条)?(?:结果|地点|相关)?", txt)
                rec["num_like"] = counts[:20]
            except Exception as e:
                rec["error"] = type(e).__name__ + ": " + str(e)[:200]
            finally:
                await page.close()
            res.append(rec)
        await br.close()

asyncio.run(go())
with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("WROTE", OUT, len(res))
