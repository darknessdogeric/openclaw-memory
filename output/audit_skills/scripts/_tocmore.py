# -*- coding: utf-8 -*-
import io, sys, os, re, json, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
EV = r"D:\B166ER-openclaw\workspace\output\book_纹样设计速查手册"
import requests
H={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
   "Accept-Language":"zh-CN,zh;q=0.9"}
CANDS = [
 ("ptpress_出版社官网", "http://www.ptpress.com.cn/search?keyword=%E7%BA%B9%E6%A0%B7%E8%AE%BE%E8%AE%A1%E9%80%9F%E6%9F%A5%E6%89%8B%E5%86%8C"),
 ("jd_京东", "https://item.jd.com/1000000000000.html"),
 ("dangdang_当当", "http://search.dangdang.com/?key=%E7%BA%B9%E6%A0%B7%E8%AE%BE%E8%AE%A1%E9%80%9F%E6%9F%A5%E6%89%8B%E5%86%8C"),
 ("cppinfo_api1", "https://book.cppinfo.cn/Encyclopedias/home/getCatalog?id=4722198"),
 ("cppinfo_api2", "https://book.cppinfo.cn/Encyclopedias/home/catalog?id=4722198"),
 ("weread_微信读书搜索", "https://weread.qq.com/web/search/books?keyword=%E7%BA%B9%E6%A0%B7%E8%AE%BE%E8%AE%A1%E9%80%9F%E6%9F%A5%E6%89%8B%E5%86%8C"),
 ("kongfz_孔夫子", "https://search.kongfz.com/product_result/?key=%E7%BA%B9%E6%A0%B7%E8%AE%BE%E8%AE%A1%E9%80%9F%E6%9F%A5%E6%89%8B%E5%86%8C"),
 ("douban_豆瓣搜索", "https://search.douban.com/book/subject_search?search_text=%E7%BA%B9%E6%A0%B7%E8%AE%BE%E8%AE%A1%E9%80%9F%E6%9F%A5%E6%89%8B%E5%86%8C"),
]
PAT = re.compile(r"\b(\d{4})[·・\.\-]\s*([^\s，,。|]{2,14}纹)")
for name,url in CANDS:
    try:
        r = requests.get(url, headers=H, timeout=35)
        t = r.text
        open(os.path.join(EV, name+".html"),"w",encoding="utf-8").write(t)
        hits = PAT.findall(t)
        ids = sorted({int(x[0]) for x in hits})
        print("  %-24s rc=%-4s %8d B ｜ 编号纹样 %4d 条 ｜ 编号区间 %s" % (
            name, r.status_code, len(t), len(hits),
            ("%04d-%04d" % (ids[0], ids[-1])) if ids else "—"))
        if hits:
            open(os.path.join(EV, name+"_编号纹样.txt"),"w",encoding="utf-8").write(
                "\n".join("%s·%s" % (a,b) for a,b in hits))
    except Exception as e:
        print("  %-24s ★ %s" % (name, str(e)[:60]))
    time.sleep(0.8)
