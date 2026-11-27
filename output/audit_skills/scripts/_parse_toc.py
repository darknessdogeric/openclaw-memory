# -*- coding: utf-8 -*-
"""_parse_toc.py - 把抓到的目录解析成机器可读纹样索引

★ 源1：《纹样之美》（北京大学出版社，同作者姊妹版）完整目录 444 个"纹样名+页码"对
★ 源2：《纹样设计速查手册》（人民邮电出版社）13 章结构 + 编号表开头 0001-0072
★ 输出 output/book_纹样设计速查手册/纹样索引.json
"""
import io
import sys
import os
import re
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
EV = r"D:\B166ER-openclaw\workspace\output\book_纹样设计速查手册"

# ---------- 繁简转换（尽力而为） ----------
T2S = {}
try:
    import zhconv
    def conv(s):
        return zhconv.convert(s, "zh-cn")
    print("  繁简转换: zhconv ✔")
except Exception:
    try:
        from opencc import OpenCC
        _cc = OpenCC("t2s")
        def conv(s):
            return _cc.convert(s)
        print("  繁简转换: opencc ✔")
    except Exception:
        MAP = str.maketrans("紋樣華麗龍鳳鳥蟲獸蝶人物幾何雲氣連續變形團窠龜背如意萬字方勝鎖子盤腸纏枝寶相蓮牡丹瓜果獸面編織簡單", "纹样华丽龙凤鸟虫兽蝶人物几何云气连续变形团窠龟背如意万字方胜锁子盘肠缠枝宝相莲牡丹瓜果兽面编织简单")
        def conv(s):
            return s.translate(MAP)
        print("  繁简转换: 手工映射（部分字可能不全）")

# ---------- 源1：sanmin《纹样之美》目录 ----------
s = open(os.path.join(EV, "sanmin_纹样之美完整目录.txt"), encoding="utf-8").read()
s = s.replace("\n", " ")
# 章节切分
CH_RE = re.compile(r"第([一二三四五六七八九十]+)章\s*([^0-9]{2,8}?)(?=[新商春六宋明常龍鳳寶纏雲回盤鎖萬方龜如八幾團如])")
marks = []
for m in re.finditer(r"第([一二三四五六七八九十]+)章\s*([^\d]{2,8})", s):
    marks.append((m.start(), m.group(1), m.group(2).strip()))
print("  《纹样之美》抓到章: %s" % ", ".join("%s·%s" % (c, conv(t)) for _, c, t in marks[:10]))

CN = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
items = []
# 逐字扫：名字（中文）+ 页码
i = 0
cur_ch = None
for m in re.finditer(r"第([一二三四五六七八九十]+)章\s*([^\d]{2,8})", s):
    items.append((m.start(), m.end(), CN.get(m.group(1)), conv(m.group(2).strip())))
# 名字+页码
pat = re.compile(r"([\u4e00-\u9fff·]{2,14}?)(\d{1,3})(?![0-9])")
out = []
for m in pat.finditer(s):
    name = m.group(1)
    page = int(m.group(2))
    if page < 1 or page > 300:
        continue
    # 去掉尾部误吞的章节字
    name = re.sub(r"第[一二三四五六七八九十]+章.*$", "", name)
    name = re.sub(r"[一-鿿]{0,2}頁$", "", name)
    if len(name) < 2:
        continue
    # 定位所属章
    ch = None
    for st, en, cn, ct in items:
        if st <= m.start():
            ch = (cn, ct)
        else:
            break
    out.append({"name": conv(name), "name_raw": name, "page": page,
                "chapter_no": ch[0] if ch else None, "chapter": ch[1] if ch else None})
# 去重保序
seen = set()
clean = []
for r in out:
    k = (r["name"], r["page"])
    if k in seen:
        continue
    seen.add(k)
    clean.append(r)
print("  《纹样之美》解析出条目: %d" % len(clean))
bys = {}
for r in clean:
    bys.setdefault(r["chapter"], []).append(r)
for c, rs in bys.items():
    ps = [x["page"] for x in rs]
    print("     %-8s %3d 条 ｜ 页码 %d-%d" % (conv(c or "?"), len(rs), min(ps), max(ps)))

# ---------- 源2：cppinfo《纹样设计速查手册》编号表 ----------
cp = open(os.path.join(EV, "cppinfo_国家出版发行信息公共服务平台.txt"), encoding="utf-8").read()
numbered = []
for m in re.finditer(r"(\d{4})[·・\.\-]\s*([^\s，,。|]{2,14}纹)", cp):
    numbered.append({"no": int(m.group(1)), "name": m.group(2), "chapter": "云纹"})
chaps13 = re.findall(r"第([一二三四五六七八九十]+)章\s*([^\n]{2,8})", cp)
print()
print("  《纹样设计速查手册》13 章: %s" % " / ".join("%s·%s" % (c, conv(t.strip())) for c, t in chaps13))
print("  编号表已抓到: %d 条（编号 %04d-%04d）" % (len(numbered), numbered[0]["no"], numbered[-1]["no"]))

meta = {
    "title": "纹样设计速查手册",
    "author": "红糖美学 著",
    "publisher": "人民邮电出版社（绘客）",
    "pub_date": "2024-08",
    "isbn": "9787115643353",
    "pages": 328,
    "price": 129.00,
    "clc": "J51-62",
    "keywords": "纹样设计-手册",
    "scale": "1200多个中国传统纹样，13 大类，全彩铜版，32 开",
    "sibling": {"title": "纹样之美：中国传统经典纹样速查手册", "publisher": "北京大学出版社",
                "pub_date": "2024", "isbn": "978-7-301-34428-6", "pages": 239,
                "note": "同作者姊妹版，目录更细（带页码），第一章为纹样简史"},
}
payload = {"meta": meta,
           "chapters_13": [{"no": c, "title": conv(t.strip())} for c, t in chaps13],
           "index_meihua": clean,
           "numbered_4722198": numbered,
           "sources": [
               {"name": "国家出版发行信息公共服务平台", "url": "https://book.cppinfo.cn/Encyclopedias/home/index?id=4722198",
                "use": "权威书目信息 + 13 章结构 + 编号表开头"},
               {"name": "三民網路書店", "url": "https://www.sanmin.com.tw/product/index/013227577",
                "use": "《纹样之美》完整目录（含页码），用于反推纹样分布与页序"},
               {"name": "香港大書城", "url": "https://www.megbook.com.hk/mall/detail.jsp?proID=4017068",
                "use": "出版社编辑推荐 8 条 + 内容简介 + 作者简介"},
           ]}
out_p = os.path.join(EV, "纹样索引.json")
json.dump(payload, open(out_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print()
print("  索引落盘:", os.path.basename(out_p), os.path.getsize(out_p), "B")
