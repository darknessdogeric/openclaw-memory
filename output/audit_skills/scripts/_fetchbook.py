# -*- coding: utf-8 -*-
import io, sys, os, re, json, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
EV = os.path.join(ROOT,"output","book_纹样设计速查手册")
os.makedirs(EV, exist_ok=True)
import requests
H={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
URLS = [
 ("cppinfo_国家出版发行信息公共服务平台", "https://book.cppinfo.cn/Encyclopedias/home/index?id=4722198"),
 ("ouc_中国海洋大学馆藏目录", "https://opac.ouc.edu.cn/mspace/searchDetailLocal/m9fb46a0f1101e3af4b817cbf89a37988"),
 ("zyufl_越秀外国语学院_纹样之美目录", "https://opac.zyufl.edu.cn/mspace/searchDetailLocal/m8ca11222f6837951eea0e51095b3e920"),
 ("hnlib_海宁市图书馆", "https://reader.hnlib.com/Book/Detail/684206"),
 ("megbook_编辑推荐与内容简介", "https://www.megbook.com.hk/mall/detail.jsp?proID=4017068"),
]
out = {}
for name, url in URLS:
    try:
        r = requests.get(url, headers=H, timeout=45)
        txt = r.text
        open(os.path.join(EV, name+".html"), "w", encoding="utf-8").write(txt)
        # 去标签
        s = re.sub(r"<script.*?</script>", " ", txt, flags=re.S|re.I)
        s = re.sub(r"<style.*?</style>", " ", s, flags=re.S|re.I)
        s = re.sub(r"<[^>]+>", "\n", s)
        s = re.sub(r"&nbsp;?", " ", s)
        s = re.sub(r"[ \t]+", " ", s)
        s = re.sub(r"\n{2,}", "\n", s)
        open(os.path.join(EV, name+".txt"), "w", encoding="utf-8").write(s)
        out[name] = {"url": url, "status": r.status_code, "chars": len(s)}
        print("  ✔ %-34s rc=%s  %d 字符" % (name, r.status_code, len(s)))
    except Exception as e:
        out[name] = {"url": url, "error": str(e)[:80]}
        print("  ★ %-34s 失败 %s" % (name, str(e)[:70]))
    time.sleep(0.6)
json.dump(out, open(os.path.join(EV,"fetch_log.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print()
print("落盘:", EV)
