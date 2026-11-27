# -*- coding: utf-8 -*-
import io, sys, os, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
EV = r"D:\B166ER-openclaw\workspace\output\book_纹样设计速查手册"
t = open(os.path.join(EV,"cppinfo_国家出版发行信息公共服务平台.txt"), encoding="utf-8").read()
lines = [l.strip() for l in t.split("\n") if l.strip()]
print("=== cppinfo 纯文本行数 %d；尾部 25 行 ===" % len(lines))
for l in lines[-25:]: print("   ", l[:120])
print()
raw = open(os.path.join(EV,"cppinfo_国家出版发行信息公共服务平台.html"), encoding="utf-8", errors="replace").read()
print("=== raw HTML %d 字符 ===" % len(raw))
print("  含 ajax/api/url 线索:")
for m in re.finditer(r"(?:url\s*:\s*['\"][^'\"]{4,120}['\"]|ajax\([^)]*\)|/[A-Za-z0-9_/\.\-]{4,60}\.(?:do|json|action|list)[^'\"]{0,20})", raw):
    print("   ", m.group(0)[:130])
for m in re.finditer(r"catalog|content|catalogList|getContent|bookInfo|detail[A-Za-z]*", raw, re.I):
    s=max(0,m.start()-60); print("   ctx:", raw[s:m.end()+60].replace("\n"," ")[:150])
    break
print()
print("=== 章节名是否出现 ===")
chs = ["云纹","几何纹","莲纹","牡丹纹","宝相花纹","缠枝纹","瓜果纹","龙纹","凤纹","兽面纹","飞鸟纹","蝶纹","人物纹"]
for c in chs:
    print("   %-8s %s" % (c, "出现" if c in raw else "—"))
