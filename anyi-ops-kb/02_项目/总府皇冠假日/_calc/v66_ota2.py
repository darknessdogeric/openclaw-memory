# -*- coding: utf-8 -*-
"""v66：OTA 实爬 v2 —— 携程详情页 __INITIAL_STATE__ 内嵌 JSON 取房型（名称/面积/价格）
   已知可用 URL 形态：https://hotels.ctrip.com/hotels/detail/?hotelId=XXXX
   同时覆盖 m.ctrip.com 移动端与 trip.com 国际站作为备份"""
import io, os, re, sys, json, time, traceback
T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "v66.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
sys.path.insert(0, r"D:\B166ER-openclaw\workspace")
from playwright.sync_api import sync_playwright

# hotelId 来源：trip.com 国际站 URL 与公开检索
HOTELS = [
 ("成都瑞吉 St. Regis", "1066373", "chengdu-hotel-detail-1066373/the-st-regis-chengdu"),
 ("成都洲至奢选(原费尔蒙棕榈泉)", "6434054", "chengdu-hotel-detail-6434054/fairmont-chengdu"),
 ("成都居舍 Upper House", "4199753", "chengdu-hotel-detail-4199753/chengdu-courtyard-hotel"),
 ("康莱德 Conrad 北京", "849324", ""),
 ("成都尼依格罗 Niccolo", "1632603", ""),
]
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

def walk(o, out, key=None):
    """递归找含 size/price/name 的房型字典"""
    if isinstance(o, dict):
        if ("size" in o or "area" in o or "roomSize" in o) and any(
                k in o for k in ("price", "displayPrice", "priceInfo", "amount")):
            out.append(o)
        for k, v in o.items():
            walk(v, out, k)
    elif isinstance(o, list):
        for v in o:
            walk(v, out, key)

def dig(o, keys, depth=0):
    """按键名深挖"""
    hits = []
    if depth > 14: return hits
    if isinstance(o, dict):
        for k, v in o.items():
            if k in keys: hits.append(v)
            if isinstance(v, (dict, list)): hits += dig(v, keys, depth + 1)
    elif isinstance(o, list):
        for v in o[:80]:
            if isinstance(v, (dict, list)): hits += dig(v, keys, depth + 1)
    return hits

OUT = {}
with sync_playwright() as pw:
    br = pw.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
    ctx = br.new_context(user_agent=UA, locale="zh-CN",
                         viewport={"width": 1440, "height": 900},
                         extra_http_headers={"Accept-Language": "zh-CN,zh;q=0.9"})
    pg = ctx.new_page()
    for name, hid, slug in HOTELS:
        rec = {"hotelId": hid, "rooms": [], "hotel_meta": {}, "url": ""}
        for url in ([f"https://hotels.ctrip.com/hotels/detail/?hotelId={hid}"] if not slug else []) + \
                   ([f"https://hotels.ctrip.com/hotels/detail/?hotelId={hid}",
                     f"https://hk.trip.com/hotels/{slug}/"] if slug else []):
            try:
                pg.goto(url, timeout=45000, wait_until="domcontentloaded")
                pg.wait_for_timeout(5200)
                pg.mouse.wheel(0, 3000); pg.wait_for_timeout(2200)
                h = pg.content()
                rec["url"] = pg.url
                # 1) __INITIAL_STATE__
                m = re.search(r"window\.__INITIAL_STATE__\s*=\s*(\{.*?\});?\s*</script>", h, re.S)
                if not m:
                    m = re.search(r"__INITIAL_STATE__\s*=\s*(\{.*?\})\s*;?\s*window\.", h, re.S)
                rooms = []
                if m:
                    raw = m.group(1)
                    raw = re.sub(r"undefined", "null", raw)
                    try:
                        data = json.loads(raw)
                    except Exception:
                        data = None
                    if data:
                        for node in dig(data, ("roomList", "RoomList", "roomInfo", "roomData")):
                            rr = []
                            walk(node, rr)
                            rooms += rr
                        meta = dig(data, ("hotelInfo", "hotelName", "positionName", "hotelId", "commentScore", "commentCount"))
                        rec["hotel_meta"] = [str(x)[:120] for x in meta[:6]] if meta else []
                # 2) 正文正则兜底：面积 + 价格相邻
                for mm in re.finditer(r'(\d{2,4}(?:\.\d)?)\s*(?:㎡|平米|平方)\s*米', h):
                    seg = h[max(0, mm.start() - 320): mm.start() + 420]
                    nm = re.search(r'"(?:name|roomName|title)":"([^"]{2,28})"', seg)
                    pr = re.search(r'"(?:price|displayPrice|amount)":\s*"?(\d{3,6})', seg)
                    if nm:
                        rooms.append({"room": nm.group(1), "size": mm.group(1),
                                      "price": pr.group(1) if pr else None})
                # 去重
                seen = set(); uniq = []
                for r0 in rooms:
                    k = (str(r0.get("name") or r0.get("room"))[:24], str(r0.get("size") or r0.get("area")))
                    if k in seen: continue
                    seen.add(k); uniq.append(r0)
                if uniq:
                    rec["rooms"] = uniq[:40]
                    break
            except Exception as e:
                L("   [%s] %s FAIL %s" % (name, url[:60], str(e)[:80]))
            time.sleep(1.0)
        OUT[name] = rec
        L("[OTA] %-26s 房型 %d 条 | url=%s" % (name, len(rec["rooms"]), rec["url"][:70]))
        for r0 in rec["rooms"][:12]:
            nm = r0.get("name") or r0.get("room") or r0.get("title")
            sz = r0.get("size") or r0.get("area") or r0.get("roomSize")
            pr = r0.get("price") or r0.get("displayPrice") or r0.get("amount")
            L("      %-30s %s㎡  %s" % (str(nm)[:30], sz, pr))
    br.close()

json.dump(OUT, open(os.path.join(T, "v66_ota.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
L("")
L("完成 %d 家" % len(OUT))
L("DONE")
