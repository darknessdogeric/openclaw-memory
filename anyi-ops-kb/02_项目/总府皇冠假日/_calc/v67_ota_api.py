# -*- coding: utf-8 -*-
"""v67：OTA 取价与房型（携程 soa2 API + 详情页双路径）
   沿用 ota_scraper/ctrip_detail_api.py 的调用范式，补齐：城市搜索→酒店ID→详情（房型面积/价格）
   输出：品牌 → 房型(名称/面积/价格)、城市、房量"""
import io, os, re, sys, json, time, urllib.request, urllib.error
T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "v67.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

HEAD = {"cid": "09031143413892357653", "ctok": "", "cver": "1.0", "lang": "01",
        "sid": "", "syscode": "09", "auth": "", "extension": []}
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

def post(url, payload, timeout=18, headers=None):
    h = {"Content-Type": "application/json", "User-Agent": UA,
         "Referer": "https://m.ctrip.com/", "Origin": "https://m.ctrip.com"}
    if headers: h.update(headers)
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=h)
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")[:400]
    except Exception as e:
        return -1, str(e)[:200]

def search_city(city_id, keyword):
    """携程移动端搜索 → 酒店列表"""
    urls = [
        ("https://m.ctrip.com/restapi/soa2/20591/json/searchHotel",
         {"cityId": int(city_id), "keyword": keyword, "pageIndex": 1, "pageSize": 20, "head": HEAD}),
        ("https://m.ctrip.com/restapi/soa2/13444/json/getHotelList",
         {"cityId": int(city_id), "keyword": keyword, "pageIndex": 1, "pageSize": 20, "head": HEAD}),
        ("https://m.ctrip.com/restapi/soa2/17992/json/getHotelList",
         {"cityId": int(city_id), "keyword": keyword, "pageIndex": 1, "pageSize": 20, "head": HEAD}),
    ]
    for u, p in urls:
        st, body = post(u, p)
        if st == 200 and len(body) > 300:
            L("   搜索端点命中 %s → %dB" % (u.split("/")[-1], len(body)))
            try:
                j = json.loads(body)
            except Exception:
                continue
            hits = []
            def walk(o):
                if isinstance(o, dict):
                    if ("hotelId" in o or "id" in o) and ("name" in o or "hotelName" in o):
                        hits.append(o)
                    for v in o.values(): walk(v)
                elif isinstance(o, list):
                    for v in o[:60]: walk(v)
            walk(j)
            return u, hits
        L("   端点 %s → %s %s" % (u.split("/")[-1], st, str(body)[:90]))
    return None, []

def detail(hotel_id):
    """详情 → 房型（名称/面积/价格）"""
    out = []
    for ep, extra in [("getHotelDetail", {"hotelId": int(hotel_id)}),
                      ("getHotelPriceList", {"hotelIds": [int(hotel_id)]})]:
        u = "https://m.ctrip.com/restapi/soa2/13444/json/" + ep
        st, body = post(u, dict(extra, head=HEAD))
        if st != 200 or len(body) < 200: continue
        try: j = json.loads(body)
        except Exception: continue
        rooms = []
        def walk(o):
            if isinstance(o, dict):
                nm = o.get("name") or o.get("roomName") or o.get("title")
                sz = o.get("size") or o.get("area") or o.get("roomSize") or o.get("areaInfo")
                pr = o.get("price") or o.get("displayPrice") or o.get("amount")
                if isinstance(sz, dict): sz = sz.get("size") or sz.get("value")
                if isinstance(pr, dict): pr = pr.get("amount") or pr.get("price")
                if nm and (sz or pr):
                    rooms.append({"room": str(nm)[:34], "size": sz, "price": pr})
                for v in o.values(): walk(v)
            elif isinstance(o, list):
                for v in o[:200]: walk(v)
        walk(j)
        if rooms: out += rooms
    # 去重
    seen = set(); uniq = []
    for r in rooms_dedup(out):
        k = (r["room"], str(r["size"]))
        if k in seen: continue
        seen.add(k); uniq.append(r)
    return uniq

def rooms_dedup(lst):
    seen = set(); out = []
    for r in lst:
        k = (r.get("room"), str(r.get("size")))
        if k in seen: continue
        seen.add(k); out.append(r)
    return out

TARGETS = [
 ("瑞吉 St. Regis", 104), ("居舍 Upper House", 104), ("尼依格罗 Niccolo", 104),
 ("洲至奢选 Vignette", 104), ("丽笙精选 Radisson", 104), ("君悦 Grand Hyatt", 104),
 ("康莱德 Conrad", 1), ("文华东方 MO", 2), ("六善 Six Senses", 2),
 ("柏悦 Park Hyatt", 2), ("丽晶 Regent", 2), ("康莱德 Conrad 成都", 104),
]
OUT = {}
for kw, cid in TARGETS:
    L("")
    L("=== %s（city %d）===" % (kw, cid))
    ep, hits = search_city(cid, kw)
    if not hits:
        L("   搜索无果")
        OUT[kw] = {"city": cid, "hotels": [], "rooms": []}
        continue
    got = []
    for h in hits[:6]:
        hid = h.get("hotelId") or h.get("id")
        nm = h.get("name") or h.get("hotelName")
        if not hid: continue
        rs = detail(hid)
        if rs:
            got.append({"hotelId": hid, "name": nm, "rooms": rs[:18]})
            L("   [%s] id=%s 房型 %d" % (str(nm)[:34], hid, len(rs)))
            for r in rs[:8]:
                L("      %-32s %s㎡  %s" % (r["room"], r["size"], r["price"]))
        time.sleep(0.5)
    OUT[kw] = {"city": cid, "hotels": got}
json.dump(OUT, open(os.path.join(T, "v67_ota.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
L("")
L("完成 %d 组｜有房型数据的酒店 %d 家"
  % (len(OUT), sum(len(v.get("hotels", [])) for v in OUT.values())))
L("DONE")
