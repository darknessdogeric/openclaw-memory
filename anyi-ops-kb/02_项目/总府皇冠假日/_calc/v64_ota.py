# -*- coding: utf-8 -*-
"""v64：OTA 实爬 —— 携程房型（名称/面积/价格）+ 各品牌成都房价
   目标：为「品牌客房面积要求 → 房量 → 收入」链条建立可核验底座"""
import io, os, re, sys, json, time, traceback
T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "v64.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
sys.path.insert(0, r"D:\B166ER-openclaw\workspace")

TARGETS = [
 # (品牌, 城市, 携程/OTA url, 用途)
 ("居舍 Upper House","成都","https://hotels.ctrip.com/hotels/4199753.html","房价+房型面积"),
 ("尼依格罗 Niccolo","成都","https://it.trip.com/hotels/chengdu-hotel-detail-100693667/oaks-chengdu-at-cultural-heritage-park/","对照"),
 ("成都院子酒店","成都","https://hotels.ctrip.com/hotels/4199753.html","对照"),
 ("Conrad 康莱德","北京","https://hotels.ctrip.com/hotels/849324.html","品牌基础房面积"),
 ("St. Regis 瑞吉","成都","https://hotels.ctrip.com/hotels/436875.html","房价+房型面积"),
 ("Six Senses 六善","成都","https://hotels.ctrip.com/hotels/436875.html","房价+房型面积"),
 ("Park Hyatt 柏悦","成都","https://hotels.ctrip.com/hotels/436875.html","房价+房型面积"),
]
# 携程搜索页取房价（房型面积与房价分两路）
SEARCHES = [
 ("成都 居舍 Upper House 房价 房型 面积", "居舍"),
 ("成都 尼依格罗 房价 房型 面积", "尼依格罗"),
 ("成都 瑞吉 St.Regis 房价 房型 面积", "瑞吉"),
 ("成都 华尔道夫 房价 房型 面积", "华尔道夫"),
 ("成都 丽思卡尔顿 房价 房型 面积", "丽思卡尔顿"),
 ("成都 费尔蒙 洲至奢选 棕榈泉 房价 房型 面积", "洲至奢选"),
 ("成都 君悦 群光 房价 房型 面积", "君悦"),
 ("成都 玛珀 瑯珀 房价 房型 面积", "瑯珀"),
 ("成都 丽笙精选 酒店 房价", "丽笙精选"),
 ("Conrad 康莱德 基础房 面积 46平米 最小客房", "康莱德面积"),
 ("St.Regis 瑞吉 最小客房面积 平米", "瑞吉面积"),
 ("Park Hyatt 柏悦 最小客房面积 平米 成都", "柏悦面积"),
 ("Six Senses 六善 客房面积 平米 最小", "六善面积"),
 ("Mandarin Oriental 文华东方 客房面积 平米 最小", "文华东方面积"),
 ("Regent 丽晶 客房面积 平米 全大户型 成都", "丽晶面积"),
 ("LXR 希尔顿 客房面积 平米 品牌标准", "LXR面积"),
 ("Sofitel 索菲特 成都 房价 房型面积", "Sofitel"),
 ("成都 春熙路 voco 房价 房型面积", "voco"),
]

import requests
from bs4 import BeautifulSoup
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
     "Accept-Language": "zh-CN,zh;q=0.9", "Referer": "https://hotels.ctrip.com/"}

def clean(s): return re.sub(r"\s+", " ", (s or "")).strip()

# ── 路线A：搜索页取房价（snippet 抓取）──
PRICES = {}
def route_search():
    from scrap_tools import smart_search
    for q, tag in SEARCHES:
        try:
            txt = smart_search(q)
            if not txt: continue
            lines = [l for l in txt.split("\n") if l.strip()]
            hits = []
            for l in lines:
                m = re.findall(r"(\d[\d,]{2,6})\s*元", l)
                m2 = re.findall(r"([¥￥]\s?\d[\d,]{2,6})", l)
                a = re.findall(r"(\d{2,4})\s*(?:㎡|平米|平方)", l)
                if m or m2 or a:
                    hits.append((l.strip()[:200], m[:6], m2[:6], a[:4]))
            PRICES[tag] = hits[:14]
            L("   [%s] %s → %d 条" % (tag, q[:26], len(hits)))
            for h in hits[:6]:
                L("      %s | 元%s | %s | ㎡%s" % (h[0][:110], h[1], h[2], h[3]))
        except Exception as e:
            L("   [%s] FAIL %s" % (tag, str(e)[:90]))
        time.sleep(0.6)

L("=== 路线A：搜索页取价 ===")
try:
    route_search()
except Exception:
    L(traceback.format_exc()[:1500])

# ── 路线B：直接抓携程酒店页（取房型名+面积+价格）──
HOTELS = [
 ("成都瑞吉","https://hotels.ctrip.com/hotels/1720408.html"),
 ("成都居舍","https://hotels.ctrip.com/hotels/4199753.html"),
 ("成都尼依格罗","https://hotels.ctrip.com/hotels/1632603.html"),
 ("成都华尔道夫","https://hotels.ctrip.com/hotels/436875.html"),
]
ROOMS = {}
def route_ota():
    for name, url in HOTELS:
        try:
            r = requests.get(url, headers=H, timeout=25)
            soup = BeautifulSoup(r.text, "lxml")
            title = clean(soup.title.text) if soup.title else ""
            body = r.text
            # 房型：形如 "豪华客房|46㎡|¥1500" 或 附近文本
            found = []
            for m in re.finditer(r"([一-龥A-Za-z]{2,12}(?:客房|套房|大床房|双床房|标准间|行政)[^|<\n]{0,24})", body):
                ctx = body[m.start(): m.start() + 260]
                area = re.search(r"(\d{2,4}(?:\.\d)?)\s*(?:㎡|平米|平方)", ctx)
                price = re.search(r"[¥￥]\s?(\d[\d,]{2,6})", ctx)
                if area or price:
                    found.append((m.group(1)[:22], area.group(1) if area else None,
                                  price.group(1) if price else None))
            # 去重
            seen = set(); uniq = []
            for f in found:
                k = (f[0], f[1])
                if k in seen: continue
                seen.add(k); uniq.append(f)
            ROOMS[name] = dict(url=url, status=r.status_code, title=title[:70], rooms=uniq[:40])
            L("   [%s] HTTP %s｜%s｜房型条目 %d" % (name, r.status_code, title[:46], len(uniq)))
            for u in uniq[:14]:
                L("      %-24s %s㎡  %s元" % (u[0], u[1] or "-", u[2] or "-"))
        except Exception as e:
            L("   [%s] FAIL %s" % (name, str(e)[:90]))
        time.sleep(1.0)

L("")
L("=== 路线B：携程房型直抓 ===")
try:
    route_ota()
except Exception:
    L(traceback.format_exc()[:1200])

json.dump(dict(prices=PRICES, rooms=ROOMS), open(os.path.join(T, "v64_ota.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
L("")
L("=== 汇总 ===")
L("价格组 %d｜OTA 房型组 %d" % (len(PRICES), len(ROOMS)))
L("DONE")
