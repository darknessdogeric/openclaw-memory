# -*- coding: utf-8 -*-
"""_starfix.py - 清除报告正文中的 ★ 装饰符号并统一检查范围

★ 原因：回读检出 emoji 残留 1 段，但我的 ok 判定漏了 emoji 项 → 检查器自己放水
★ 根因：★ (U+2605) 属 \u2600-\u27BF 区间，被 emoji 检测命中；且 v1.0 我只扫段落不扫表格 → 范围不一致
★ 处理：按公文范式「无装饰符号」，从 md 正文中去除 ★（不靠放宽判据）
"""
import io
import sys
import os
import re
import json
import subprocess

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
KB4 = os.path.join(ROOT, "anyi-ops-kb", "04_方法论")
MD = os.path.join(KB4, "B166ER_技能库与范式库深度审计报告_v1.1_2026-11-18.md")

t = open(MD, encoding="utf-8").read()
before = t.count("★")
# 去除 ★ 及其后紧跟的空格；清理连续空格与行首空格
t = re.sub(r"★\s*", "", t)
t = re.sub(r"[ \t]{2,}", " ", t)
t = re.sub(r"^[ \t]+", "", t, flags=re.M)
t = re.sub(r"\|\s+\|", "| |", t)
t = re.sub(r"\n{3,}", "\n\n", t)
open(MD, "w", encoding="utf-8", newline="\n").write(t)
print("★ 去除 %d 处（余 %d）｜ md %d B" % (before, t.count("★"), len(t.encode("utf-8"))))

# 重渲染
OUT = MD[:-3] + ".docx"
TMP = os.path.join(ROOT, "output", "_t")
os.makedirs(TMP, exist_ok=True)
lines = t.split("\n")
body = "\n".join(lines[1:]) if lines and lines[0].startswith("# ") else "\n".join(lines)
tmpmd = os.path.join(TMP, "audit_report_v11_body.md")
open(tmpmd, "w", encoding="utf-8", newline="\n").write(body)
r = subprocess.run([sys.executable, os.path.join(ROOT, "toolbox", "md2docx.py"), tmpmd, OUT,
                    "--title", "B166ER 技能库与范式库深度审计报告",
                    "--subtitle", "v1.1（含工具层治理）｜ 审计日期 2026 年 11 月 18 日 ｜ 技能库 3 处目录 ＋ 范式库 4 类来源 ＋ toolbox 工具层"],
                   capture_output=True, timeout=300)
print("渲染 rc=%s %s" % (r.returncode, (r.stdout or r.stderr).decode("utf-8", "replace").strip()[:120]))
if r.returncode != 0:
    raise SystemExit(1)

import docx

d = docx.Document(OUT)
ps = [p.text.strip() for p in d.paragraphs if p.text.strip()]
cells = [c.text.strip() for tb in d.tables for rr in tb.rows for c in rr.cells]
alltxt = "\n".join(ps) + "\n" + "\n".join(cells)
print()
print("=" * 100)
print("回读校验（★ 检查范围已统一：正文段落 ＋ 全部表格单元格）")
print("=" * 100)
print("  文件 %d B ｜ 段落 %d ｜ 表格 %d ｜ 表行 %d"
      % (os.path.getsize(OUT), len(ps), len(d.tables), sum(len(tb.rows) for tb in d.tables)))
res_md = [x for x in ps if re.search(r"(\*\*|^#{1,6}\s|\|---|^[-*]\s|^>\s)", x)]
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F]")
emo_p = [x for x in ps if EMOJI.search(x)]
emo_c = [x for x in cells if EMOJI.search(x)]
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
checks = [
    ("① Markdown 残留", len(res_md), "处"),
    ("② emoji 残留（正文）", len(emo_p), "段"),
    ("②b emoji 残留（表格）", len(emo_c), "格"),
    ("③ 骨架缺失", len(miss), "节"),
    ("④ 关键数字缺失", len(missk), "个"),
    ("⑤ 分隔行误入数据行", len(bad), "处"),
    ("⑦ 列表符号残留", len(lst), "段"),
]
for name, n, unit in checks:
    print("  %-22s %d %s %s" % (name, n, unit, "" if n == 0 else "★"))
for x in (res_md + emo_p + emo_c + lst)[:6]:
    print("       ★ %s" % x[:88])
for m in miss:
    print("       ★ 缺 %s" % m)
if missk:
    print("       ★ 缺数字 %s" % missk)
print("  ⑥ 字体样本: %s" % ", ".join(sorted(fonts)))
print()
ok = all(n == 0 for _, n, _ in checks)
print("  ⇒ 回读结论: %s" % ("通过" if ok else "★仍有问题，须修"))
