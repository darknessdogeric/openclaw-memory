# -*- coding: utf-8 -*-
import io, sys, os, re, ast, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
MD2 = os.path.join(ROOT,"toolbox","md2docx.py")

# ============ 1. 修排版器：加列表分支（纯文字段落、无符号、缩进2字符） ============
t = open(MD2, encoding="utf-8", errors="replace").read()
OLD = '''        p = d.add_paragraph(); spacing(p, 2, 4, 1.45)
        add_md_runs(p, s); i += 1
    d.save(out_path)'''
NEW = '''        if s.startswith("- ") or s.startswith("\\u2022 "):
            # ★ 列表：公文范式要求纯文字段落、无项目符号；缩进 2 字符
            p = d.add_paragraph(); spacing(p, 2, 4, 1.45)
            p.paragraph_format.left_indent = Cm(0.74)
            add_md_runs(p, s[2:]); i += 1; continue
        p = d.add_paragraph(); spacing(p, 2, 4, 1.45)
        add_md_runs(p, s); i += 1
    d.save(out_path)'''
assert OLD in t, "md2docx.py 兜底分支未命中"
t2 = t.replace(OLD, NEW, 1)
ast.parse(t2)
open(MD2,"w",encoding="utf-8",newline="\n").write(t2)
print("✔ md2docx.py 已加列表分支（纯文字段落、缩进 2 字符、无符号）｜ %d B → %d B" % (len(t), len(t2)))

# ============ 2. 重渲染 + 回读（检查器修正：alltxt 含表格单元格） ============
KB4 = os.path.join(ROOT,"anyi-ops-kb","04_方法论")
MD  = os.path.join(KB4,"B166ER_技能库与范式库深度审计报告_v1.0_2026-11-18.md")
OUT = os.path.join(KB4,"B166ER_技能库与范式库深度审计报告_v1.0_2026-11-18.docx")
TMP = os.path.join(ROOT,"output","_t"); os.makedirs(TMP, exist_ok=True)
lines = open(MD, encoding="utf-8").read().split("\n")
body = "\n".join(lines[1:]) if lines and lines[0].startswith("# ") else "\n".join(lines)
tmpmd = os.path.join(TMP,"audit_report_body.md")
open(tmpmd,"w",encoding="utf-8",newline="\n").write(body)
r = subprocess.run([sys.executable, MD2, tmpmd, OUT,
   "--title","B166ER 技能库与范式库深度审计报告",
   "--subtitle","审计日期 2026 年 11 月 18 日 ｜ 技能库 3 处目录 ＋ 范式库 4 类来源 ｜ 全量程序化清点 ＋ 内容级取证 ＋ 实跑验证"],
   capture_output=True, timeout=240)
print("  渲染 rc=%s %s" % (r.returncode, r.stdout.decode("utf-8","replace").strip()[:120]))
print()
print("="*100); print("回读校验（检查器已修正：正文＋表格全量取文本）"); print("="*100)
import docx
d = docx.Document(OUT)
ps = [p.text.strip() for p in d.paragraphs if p.text.strip()]
cells = [c.text.strip() for t2_ in d.tables for r_ in t2_.rows for c in r_.cells]
alltxt = "\n".join(ps) + "\n" + "\n".join(cells)
print("  文件 %d B ｜ 段落 %d ｜ 表格 %d ｜ 表行 %d" % (os.path.getsize(OUT), len(ps), len(d.tables), sum(len(t.rows) for t in d.tables)))
# ① Markdown 残留（段落级）
res_md = [x for x in ps if re.search(r"(\*\*|^#{1,6}\s|\|---|^[-*]\s|^>\s)", x)]
print("  ① Markdown 残留: %d 处" % len(res_md))
for x in res_md[:5]: print("       ★ %s" % x[:88])
# ② emoji
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F]")
print("  ② emoji 残留: %d 段" % len([x for x in ps if EMOJI.search(x)]))
# ③ 骨架
need = ["一、审计结论先行","二、完整性的真实状况","三、闲置裁决","四、GitHub 补装","五、固定工作流与调用逻辑",
        "六、同源治理","七、我在这次审计中犯的错","八、已落成的防护","九、尚未解决的事","十、一句话总结"]
miss = [n for n in need if not any(n in x for x in ps)]
print("  ③ 骨架序列: %d/%d" % (len(need)-len(miss), len(need)))
for m in miss: print("       ★ 缺 %s" % m)
# ④ 关键数字（含表格）
KEY = ["150","25","19","271","185","16","134","79","42"]
print("  ④ 关键数字: %s" % {k:(k in alltxt) for k in KEY})
# ⑤ 表格
if d.tables:
    t0 = d.tables[0]
    bad = [r for tb in d.tables for r in tb.rows if all(set(c.text.strip())<=set("-:| ") for c in r.cells)]
    print("  ⑤ 首表 %d 行 × %d 列 ｜ 表头 %s ｜ 分隔行误入 %d" % (len(t0.rows), len(t0.columns),
          " | ".join(c.text for c in t0.rows[0].cells), len(bad)))
# ⑥ 字体
fonts=set()
for p in d.paragraphs[:50]:
    for run in p.runs:
        if run.font.name: fonts.add(run.font.name)
print("  ⑥ 字体样本: %s" % ", ".join(sorted(fonts)))
# ⑦ 列表已转为纯文字段落
lst = [x for x in ps if x.startswith("- ") or x.startswith("• ")]
print("  ⑦ 列表符号残留: %d 段" % len(lst))
for x in lst[:3]: print("       ★ %s" % x[:80])
ok = (not res_md) and (not miss) and (not lst) and (not bad)
print()
print("  ⇒ 回读结论: %s" % ("通过" if ok else "★仍有问题"))
