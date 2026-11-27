# -*- coding: utf-8 -*-
import io, sys, os, re, json, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
EV = r"D:\B166ER-openclaw\workspace\output\book_纹样设计速查手册"
import requests
H={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
   "Accept-Language":"zh-CN,zh;q=0.9"}
CANDS=[("bookschina_纹样之美完整目录","https://m.bookschina.com/9317174.htm"),
       ("sanmin_纹样之美完整目录","https://www.sanmin.com.tw/product/index/013227577"),
       ("bookschina_纹样设计速查手册","https://www.bookschina.com/9614271.htm")]
for name,url in CANDS:
    try:
        r=requests.get(url,headers=H,timeout=40)
        t=r.text
        open(os.path.join(EV,name+".html"),"w",encoding="utf-8").write(t)
        s=re.sub(r"<script.*?</script>"," ",t,flags=re.S|re.I)
        s=re.sub(r"<style.*?</style>"," ",s,flags=re.S|re.I)
        s=re.sub(r"<br\s*/?>","\n",s,flags=re.I)
        s=re.sub(r"</(p|div|li|tr|h\d)>","\n",s,flags=re.I)
        s=re.sub(r"<[^>]+>"," ",s)
        s=s.replace("&nbsp;"," ").replace("&amp;","&")
        s=re.sub(r"[ \t\u3000]+"," ",s)
        s=re.sub(r"\n\s*\n+","\n",s)
        open(os.path.join(EV,name+".txt"),"w",encoding="utf-8").write(s)
        # 提取"词+页码"对
        pairs=re.findall(r"([\u4e00-\u9fff·]{2,20}?)\s*(\d{1,3})(?=[\s\u4e00-\u9fff]|$)", s)
        print("  %-32s rc=%-4s %8d B ｜ 文本 %6d 字符 ｜ 页码对 %d" % (name, r.status_code, len(t), len(s), len(pairs)))
    except Exception as e:
        print("  %-32s ★ %s" % (name, str(e)[:60]))
    time.sleep(0.8)
print()
# 检查 bookschina 抓到的目录里有多少章
for f in sorted(os.listdir(EV)):
    if f.endswith(".txt"):
        t=open(os.path.join(EV,f),encoding="utf-8").read()
        chs=re.findall(r"第[一二三四五六七八九十]+章\s*([^\n]{2,10})", t)
        if chs: print("  %-36s 抓到章节: %s" % (f, " / ".join(chs[:14])))
