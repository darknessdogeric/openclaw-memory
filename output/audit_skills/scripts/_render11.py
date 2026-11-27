# -*- coding: utf-8 -*-
"""_render11.py - 渲染审计报告 v1.1 并做回读六项校验"""
import io
import sys
import os
import re
import subprocess

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
KB4 = os.path.join(ROOT, "anyi-ops-kb", "04_方法论")
MD = os.path.join(KB4, "B166ER_技能库与范式库深度审计报告_v1.1_2026-11-18.md")
OUT = os.path.join(KB4, "B166ER_技能库与范式库深度审计报告_v1.1_2026-11-18.docx")
TMP = os.path.join(ROOT, "output", "_t")
os.makedirs(TMP, exist_ok=True)

lines = open(MD, encoding="utf-8").read().split("\n")
body = "\n".join(lines[1:]) if lines and lines[0].startswith("# ") else "\n".join(lines)
tmpmd = os.path.join(TMP, "audit_report_v11_body.md")
open(tmpmd, "w", encoding="utf-8", newline="\n").write(body)

r = subprocess.run([sys.executable, os.path.join(ROOT, "toolbox", "md2docx.py"), tmpmd, OUT,
                    "--title", "B166ER 技能库与范式库深度审计报告",
                    "--subtitle", "v1.1（含工具层治理）｜ 审计日期 2026 年 11 月 18 日 ｜ 技能库 3 处目录 ＋ 范式库 4 类来源 ＋ toolbox 工具层"],
                   capture_output=True, timeout=300)
print("渲染 rc=%s %s" % (r.returncode, (r.stdout or r.stderr).decode("utf-8", "replace").strip()[:150]))
if r.returncode != 0:
    raise SystemExit(1)

import docx

d = docx.Document(OUT)
ps = [p.text.strip() for p in d.paragraphs if p.text.strip()]
cells = [c.text.strip() for t in d.tables for rr in t.rows for c in rr.cells]
alltxt = "\n".join(ps) + "\n" + "\n".join(cells)
print()
print("=" * 100)
print("回读校验")
print("=" * 100)
print("  文件 %d B ｜ 段落 %d ｜ 表格 %d ｜ 表行 %d"
      % (os.path.getsize(OUT), len(ps), len(d.tables), sum(len(t.rows) for t in d.tables)))
print("  首段: %s" % ps[0][:60])
res_md = [x for x in ps if re.search(r"(\*\*|^#{1,6}\s|\|---|^[-*]\s|^>\s)", x)]
print("  ① Markdown 残留: %d 处" % len(res_md))
for x in res_md[:4]:
    print("       ★ %s" % x[:88])
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F]")
print("  ② emoji 残留: %d 段" % len([x for x in ps if EMOJI.search(x)]))
need = ["一、审计结论先行", "二、完整性的真实状况", "三、闲置裁决", "四、GitHub 补装",
        "五、固定工作流与调用逻辑", "六、工具层治理", "七、同源治理", "八、我在这次审计中犯的错",
        "九、已落成的防护", "十、尚未解决的事", "十一、一句话总结"]
miss = [n for n in need if not any(n in x for x in ps)]
print("  ③ 骨架序列: %d/%d" % (len(need) - len(miss), len(need)))
for m in miss:
    print("       ★ 缺 %s" % m)
KEY = ["152", "27", "22", "417", "271", "185", "16", "281", "284", "134", "79", "42", "150"]
missk = [k for k in KEY if k not in alltxt]
print("  ④ 关键数字: %d/%d 在位" % (len(KEY) - len(missk), len(KEY)))
if missk:
    print("       ★ 缺: %s" % missk)
bad = [rr for t in d.tables for rr in t.rows if all(set(c.text.strip()) <= set("-:| ") for c in rr.cells)]
print("  ⑤ 分隔行误入数据行: %d" % len(bad))
fonts = set()
for p in d.paragraphs[:50]:
    for run in p.runs:
        if run.font.name:
            fonts.add(run.font.name)
print("  ⑥ 字体样本: %s" % ", ".join(sorted(fonts)))
lst = [x for x in ps if x.startswith("- ") or x.startswith("• ")]
print("  ⑦ 列表符号残留: %d 段" % len(lst))
for x in lst[:3]:
    print("       ★ %s" % x[:80])
ok = (not res_md) and (not miss) and (not missk) and (not bad) and (not lst)
print()
print("  ⇒ 回读结论: %s" % ("通过" if ok else "★仍有问题，须修"))
