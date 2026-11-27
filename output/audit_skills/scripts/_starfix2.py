# -*- coding: utf-8 -*-
"""_starfix2.py - 修生成器（安全去星）→ 重新生成 v1.1 → 重渲染 → 完整回读校验

★ 上一版清理正则里的 \s 匹配换行，把表格行间换行吃掉 → 6 张表被压扁
★ 本版：只从生成器源头改，去星号用 [ \t]* 绝不碰换行；表格格式完全不动
"""
import io
import sys
import os
import re
import subprocess

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
KB4 = os.path.join(ROOT, "anyi-ops-kb", "04_方法论")
GEN = os.path.join(ROOT, "output", "audit_skills", "scripts", "_mkreport11.py")

# ---------- 1. 修生成器：安全去星 ----------
g = open(GEN, encoding="utf-8", errors="replace").read()
OLD = 'open(V11, "w", encoding="utf-8", newline="\\n").write(R)'
NEW = ('R = re.sub(r"\\u2605[ \\t]*", "", R)          # 去装饰符号；[ \\t]* 绝不碰换行\n'
       'R = re.sub(r"[ \\t]{2,}", " ", R)\n'
       'R = re.sub(r"^[ \\t]+", "", R, flags=re.M)\n'
       'open(V11, "w", encoding="utf-8", newline="\\n").write(R)')
if OLD in g:
    g = g.replace(OLD, NEW, 1)
    open(GEN, "w", encoding="utf-8", newline="\n").write(g)
    print("✔ 生成器已改为安全去星")
else:
    print("· 生成器已是安全版（或模式未命中）")

# ---------- 2. 重新生成 ----------
r = subprocess.run([sys.executable, GEN], capture_output=True, timeout=300)
print(r.stdout.decode("utf-8", "replace").strip())
if r.returncode != 0:
    print(r.stderr.decode("utf-8", "replace")[-600:])
    raise SystemExit(1)

MD = os.path.join(KB4, "B166ER_技能库与范式库深度审计报告_v1.1_2026-11-18.md")
t = open(MD, encoding="utf-8").read()
print("  md: %d B ｜ 表格行 %d ｜ ★ 残留 %d" % (len(t.encode("utf-8")), len(re.findall(r"^\|---", t, re.M)), t.count("★")))

# ---------- 3. 重渲染 ----------
OUT = MD[:-3] + ".docx"
TMP = os.path.join(ROOT, "output", "_t")
os.makedirs(TMP, exist_ok=True)
lines = t.split("\n")
body = "\n".join(lines[1:]) if lines and lines[0].startswith("# ") else "\n".join(lines)
tmpmd = os.path.join(TMP, "audit_report_v11_body.md")
open(tmpmd, "w", encoding="utf-8", newline="\n").write(body)
r2 = subprocess.run([sys.executable, os.path.join(ROOT, "toolbox", "md2docx.py"), tmpmd, OUT,
                     "--title", "B166ER 技能库与范式库深度审计报告",
                     "--subtitle", "v1.1（含工具层治理）｜ 审计日期 2026 年 11 月 18 日 ｜ 技能库 3 处目录 ＋ 范式库 4 类来源 ＋ toolbox 工具层"],
                    capture_output=True, timeout=300)
print("  渲染 rc=%s %s" % (r2.returncode, (r2.stdout or r2.stderr).decode("utf-8", "replace").strip()[:120]))
if r2.returncode != 0:
    raise SystemExit(1)

# ---------- 4. 完整回读（检查范围统一：段落 ＋ 全部单元格） ----------
import docx

d = docx.Document(OUT)
ps = [p.text.strip() for p in d.paragraphs if p.text.strip()]
cells = [c.text.strip() for tb in d.tables for rr in tb.rows for c in rr.cells]
alltxt = "\n".join(ps) + "\n" + "\n".join(cells)
print()
print("=" * 100)
print("回读校验")
print("=" * 100)
print("  文件 %d B ｜ 段落 %d ｜ 表格 %d ｜ 表行 %d"
      % (os.path.getsize(OUT), len(ps), len(d.tables), sum(len(tb.rows) for tb in d.tables)))
res_md = [x for x in ps if re.search(r"(\*\*|^#{1,6}\s|\|---|^[-*]\s|^>\s)", x)]
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F]")
emo = [x for x in (ps + cells) if EMOJI.search(x)]
need = ["一、审计结论先行", "二、完整性的真实状况", "三、闲置裁决", "四、GitHub 补装",
        "五、固定工作流与调用逻辑", "六、工具层治理", "七、同源治理", "八、我在这次审计中犯的错",
        "九、已落成的防护", "十、尚未解决的事", "十一、一句话总结"]
miss = [n for n in need if not any(n in x for x in ps)]
KEY = ["152", "27", "22", "417", "271", "185", "16", "281", "284", "134", "79", "42", "150"]
missk = [k for k in KEY if k not in alltxt]
bad = [rr for tb in d.tables for rr in tb.rows if all(set(c.text.strip()) <= set("-:| ") for c in rr.cells)]
lst = [x for x in ps if x.startswith("- ") or x.startswith("• ")]
fonts = set()
for p in d.paragraphs[:50]:
    for run in p.runs:
        if run.font.name:
            fonts.add(run.font.name)
checks = [("① Markdown 残留", len(res_md)), ("② emoji 残留", len(emo)),
          ("③ 骨架缺失", len(miss)), ("④ 关键数字缺失", len(missk)),
          ("⑤ 分隔行误入数据行", len(bad)), ("⑥ 列表符号残留", len(lst))]
for name, n in checks:
    print("  %-22s %d %s" % (name, n, "" if n == 0 else "★"))
for x in (res_md + emo + lst)[:6]:
    print("       ★ %s" % x[:88])
for m in miss:
    print("       ★ 缺 %s" % m)
if missk:
    print("       ★ 缺数字 %s" % missk)
print("  ⑦ 字体样本: %s" % ", ".join(sorted(fonts)))
print()
ok = all(n == 0 for _, n in checks) and len(d.tables) >= 6
print("  ⇒ 回读结论: %s" % ("通过" if ok else "★仍有问题，须修"))
