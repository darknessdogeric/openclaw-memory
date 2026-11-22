# -*- coding: utf-8 -*-
"""v65：OTA 实爬（Playwright 两步法）
   第一步：携程搜索页 → 酒店列表（hotelId / 名称 / 展示价）
   第二步：酒店详情页 → 房型名称 / 面积 / 价格
   同时抓第三方对比页（携程国际站 + 攻略站）补足未上市品牌"""
import io, os, re, sys, json, time, traceback
T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "v65.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
sys.path.insert(0, r"D:\B166ER-openclaw\workspace")
from playwright.sync_api import sync_playwright

BRANDS = [
 ("居舍 Upper House", "成都"), ("尼依格罗 Niccolo", "成都"), ("瑞吉 St. Regis", "成都"),
 ("华尔道夫 Waldorf", "成都"), ("丽思卡尔顿 Ritz", "成都"), ("费尔蒙 Fairmont", "成都"),
 ("洲至奢选 Vignette", "成都"), ("君悦 Grand Hyatt", "成都"), ("丽笙精选 Radisson", "成都"),
 ("尼依格罗 Niccolo", "上海"), ("瑞吉 St. Regis", "上海"), ("康莱德 Conrad", "北京"),
 ("康莱德 Conrad", "上海"), ("文华东方 MO", "上海"), ("六善 Six Senses", "上海"),
 ("柏悦 Park Hyatt", "上海"), ("丽晶 Regent", "上海"), ("巴塞罗那 丽晶 Regent", "巴塞罗那"),
]
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
OUT = {}
with sync_playwright() as pw:
    br = pw.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
    ctx = br.new_context(user_agent=UA, locale="zh-CN", viewport={"width": 1440, "height": 900})
    pg = ctx.new_page()
    # ── 步骤一：搜索酒店 ──
    for name, city in BRANDS:
        key = "%s|%s" % (name, city)
        try:
            url = "https://hotels.ctrip.com/hotels/list?countryId=1&city=%d&keyword=%s" % (
                {"成都": 104, "上海": 2, "北京": 1, "巴塞罗那": 11658}.get(city, 104),
                name.replace(" ", "%20"))
            pg.goto(url, timeout=45000, wait_until="domcontentloaded")
            pg.wait_for_timeout(4200)
            html = pg.content()
            ids = re.findall(r'/hotels/(\d{5,8})\.html', html)
            names = re.findall(r'"hotelName":"([^"]{2,40})"', html)
            prices = re.findall(r'"price":"?(\d{3,5})', html)
            otel = {"ids": list(dict.fromkeys(ids))[:6], "names": list(dict.fromkeys(names))[:10],
                    "prices": list(dict.fromkeys(prices))[:14], "url": url}
            OUT.setdefault(key, otel)
            L("[搜索] %-22s %-5s ids=%s names=%s" % (name, city, otel["ids"][:4], otel["names"][:3]))
        except Exception as e:
            L("[搜索] %-22s %-5s FAIL %s" % (name, city, str(e)[:100]))
        time.sleep(1.1)
    # ── 步骤二：取房型（面积/价格）──
    L("")
    L("=== 房型面积与价格 ===")
    for key, otel in list(OUT.items()):
        got = []
        for hid in otel["ids"][:3]:
            try:
                u = "https://hotels.ctrip.com/hotels/%s.html" % hid
                pg.goto(u, timeout=45000, wait_until="domcontentloaded")
                pg.wait_for_timeout(3800)
                h = pg.content()
                # 携程内嵌 JSON：房型名 + 面积 + 价格
                for m in re.finditer(r'"roomName":"([^"]{2,30})"', h):
                    seg = h[m.start(): m.start() + 700]
                    a = re.search(r'"size":"?(\d{2,4}(?:\.\d)?)', seg)
                    p = re.search(r'"price":"?(\d{3,5})', seg)
                    if a:
                        got.append((m.group(1), a.group(1), p.group(1) if p else None))
                for m in re.finditer(r'([一-龥]{0,6}(?:豪华|高级|尊享|行政|商务|标准|大床|双床|套房)[一-龥]{0,8}房)', h):
                    seg = h[max(0, m.start() - 200): m.start() + 500]
                    a = re.search(r'(\d{2,4}(?:\.\d)?)\s*(?:㎡|平米)', seg)
                    p = re.search(r'[¥￥]\s?(\d[\d,]{2,6})', seg)
                    if a:
                        got.append((m.group(1)[:22], a.group(1), p.group(1) if p else None))
            except Exception as e:
                L("   [%s id%s] FAIL %s" % (key, hid, str(e)[:70]))
            time.sleep(0.9)
        seen = set(); uniq = []
        for g in got:
            k = (g[0], g[1])
            if k in seen: continue
            seen.add(k); uniq.append(g)
        otel["rooms"] = uniq[:26]
        L("[房型] %-28s %d 条 | %s" % (key, len(uniq), uniq[:6]))
    br.close()

json.dump(OUT, open(os.path.join(T, "v65_ota.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
L("")
L("完成：%d 组" % len(OUT))
L("DONE")
