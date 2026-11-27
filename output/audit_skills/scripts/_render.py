# -*- coding: utf-8 -*-
import io, sys, os, re, shutil, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
KB4 = os.path.join(ROOT,"anyi-ops-kb","04_方法论")
MD  = os.path.join(KB4,"B166ER_技能库与范式库深度审计报告_v1.0_2026-11-18.md")
OUT = os.path.join(KB4,"B166ER_技能库与范式库深度审计报告_v1.0_2026-11-18.docx")
TMP = os.path.join(ROOT,"output","_t"); os.makedirs(TMP, exist_ok=True)

# 渲染用副本：去掉正文里的首行标题（改用 --title），避免标题重复
lines = open(MD, encoding="utf-8").read().split("\n")
body = "\n".join(lines[1:]) if lines and lines[0].startswith("# ") else "\n".join(lines)
tmpmd = os.path.join(TMP,"audit_report_body.md")
open(tmpmd,"w",encoding="utf-8",newline="\n").write(body)

r = subprocess.run([sys.executable, os.path.join(ROOT,"toolbox","md2docx.py"), tmpmd, OUT,
                    "--title","B166ER 技能库与范式库深度审计报告",
                    "--subtitle","审计日期 2026 年 11 月 18 日 ｜ 技能库 3 处目录 ＋ 范式库 4 类来源 ｜ 全量程序化清点 ＋ 内容级取证 ＋ 实跑验证"],
                   capture_output=True, timeout=240)
print("渲染 rc=%s" % r.returncode)
print((r.stdout or r.stderr).decode("utf-8","replace").strip()[:300])
print()
print("="*100); print("回读校验"); print("="*100)
import docx
d = docx.Document(OUT)
ps = [p.text.strip() for p in d.paragraphs if p.text.strip()]
alltxt = "\n".join(ps)
tbl_rows = sum(len(t.rows) for t in d.tables)
print("  文件 %d B ｜ 段落 %d ｜ 表格 %d ｜ 表行 %d" % (os.path.getsize(OUT), len(ps), len(d.tables), tbl_rows))
print("  首段: %s" % ps[0][:60])
print("  次段: %s" % ps[1][:80] if len(ps)>1 else "")
# 校验 1：Markdown 残留
res_md = [x for x in ps if re.search(r"(\*\*|^#{1,6}\s|\|---|^[-*]\s)", x)]
print("  ① Markdown 残留（全文数 * 与 #，不只查段首）: %d 处" % (alltxt.count("*") + alltxt.count("##")))
for x in res_md[:5]: print("       ★ %s" % x[:90])
# 校验 2：emoji 残留
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F]")
emo = [x for x in ps if EMOJI.search(x)]
print("  ② emoji 残留: %d 段" % len(emo))
for x in emo[:3]: print("       ★ %s" % x[:80])
# 校验 3：骨架完整性（10 个一级章节）
need = ["一、审计结论先行","二、完整性的真实状况","三、闲置裁决","四、GitHub 补装","五、固定工作流与调用逻辑",
        "六、同源治理","七、我在这次审计中犯的错","八、已落成的防护","九、尚未解决的事","十、一句话总结"]
miss = [n for n in need if not any(n in x for x in ps)]
print("  ③ 骨架序列: %d/%d 章节在位" % (len(need)-len(miss), len(need)))
for m in miss: print("       ★ 缺: %s" % m)
# 校验 4：关键数字
KEY = ["150","25","19","271","185","16","134"]
print("  ④ 关键数字在位: %s" % {k: (k in alltxt) for k in KEY})
# 校验 5：表格内容抽查（确认分隔行没被当成数据行）
if d.tables:
    t0 = d.tables[0]
    print("  ⑤ 首表 %d 行 × %d 列；表头: %s" % (len(t0.rows), len(t0.columns),
          " | ".join(c.text for c in t0.rows[0].cells)))
    bad = [r for t in d.tables for r in t.rows if all(set(c.text.strip())<=set("-:| ") for c in r.cells)]
    print("     分隔行误入数据行: %d 处 %s" % (len(bad), "★需修" if bad else "无"))
# 校验 6：字体检查
fonts = set()
for p in d.paragraphs[:40]:
    for run in p.runs:
        if run.font.name: fonts.add(run.font.name)
print("  ⑥ 正文字体样本: %s" % ", ".join(sorted(fonts)))
ok = (len(res_md)==0 and len(emo)==0 and not miss and not bad)
print()
print("  ⇒ 回读结论: %s" % ("通过" if ok else "★有问题，须修"))
