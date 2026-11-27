# -*- coding: utf-8 -*-
import io, sys, os, re, glob, json, shutil, hashlib, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
TB = os.path.join(ROOT,"toolbox")
CANON = os.path.join(ROOT,"skills","docx-md-bridge","scripts","md_to_docx.py")

print("="*100); print("### A. toolbox 规模核实（704 这个数字要验）"); print("="*100)
allpy = glob.glob(os.path.join(TB,"*.py"))
nonus = [p for p in allpy if not os.path.basename(p).startswith("_")]
sub = glob.glob(os.path.join(TB,"*","*.py"))
print("  toolbox 根目录 .py 总数: %d ｜ 其中非下划线: %d ｜ 下划线临时: %d" % (len(allpy), len(nonus), len(allpy)-len(nonus)))
print("  一级子目录 .py: %d" % len(sub))
print("  toolbox 根目录非 .py 文件: %d" % len([p for p in glob.glob(os.path.join(TB,"*")) if os.path.isfile(p)]))
print("  ★ 非下划线脚本前 30 个:")
for p in sorted(nonus)[:30]:
    print("     %-34s %6d B" % (os.path.basename(p), os.path.getsize(p)))

print()
print("="*100); print("### B. 合并：编号列表 + 分页标记 → 正本 docx-md-bridge"); print("="*100)
t = open(CANON, encoding="utf-8", errors="replace").read()
orig_len = len(t)
# 1) 正则
t = t.replace(
 "RE_CODE = re.compile(r'^```')",
 "RE_CODE = re.compile(r'^```')\nRE_OL   = re.compile(r'^(\\d+)[.)]\\s+(.*)$')   # 编号列表（2026-11-18 并入）\nRE_PB   = re.compile(r'^<!--\\s*pagebreak\\s*-->$', re.I)  # 分页标记（2026-11-18 并入）")
# 2) 分页处理（放在分隔线分支前）
t = t.replace(
 "          # 分隔线\n          if s == RE_HR:",
 "          # 分页标记\n          if RE_PB.match(s):\n              doc.add_page_break()\n              i += 1\n              is_first = False\n              continue\n          # 分隔线\n          if s == RE_HR:")
# 3) 编号列表（放在无序列表分支前）
t = t.replace(
 "          m = re.match(r'^[-*]\\s+(.*)', s)\n          if m:",
 "          mol = RE_OL.match(s)\n          if mol:\n              p = doc.add_paragraph()\n              pf = p.paragraph_format\n              pf.left_indent = Emu(600000)\n              pf.first_line_indent = Emu(-360000)\n              run = p.add_run(mol.group(1) + '. ' + mol.group(2))\n              set_font(run, BODY_FONT, 11)\n              i += 1\n              continue\n          m = re.match(r'^[-*+]\\s+(.*)', s)\n          if m:")
# 4) docstring 更新
t = t.replace("      - 支持代码块、表格、引用、列表",
              "      - 支持代码块、表格、引用、列表（无序 + 编号）\n      - 支持 <!-- pagebreak --> 分页标记")
t = t.replace("  - 无 emoji / 无装饰", "  - 无 emoji / 无装饰")
open(CANON,"w",encoding="utf-8",newline="\n").write(t)
import ast
ast.parse(t)
print("  正本已更新: %d B → %d B ｜ ast.parse 通过" % (orig_len, len(t)))

print()
print("="*100); print("### C. 验证：合并后的正本是否真能出编号列表与分页"); print("="*100)
TMP = os.path.join(ROOT,"output","_t"); os.makedirs(TMP, exist_ok=True)
MD = os.path.join(TMP,"canon.md")
open(MD,"w",encoding="utf-8").write(
 "# 标题\n\n段落。\n\n- 无序一\n- 无序二\n\n1. 编号一\n2. 编号二\n\n<!-- pagebreak -->\n\n分页后的段落。\n\n| A | B |\n|---|---|\n| 1 | 2 |\n")
out = os.path.join(TMP,"canon.docx")
if os.path.exists(out): os.remove(out)
import subprocess
r = subprocess.run([sys.executable, CANON, MD, out], capture_output=True, timeout=120)
print("  rc=%s 产出=%s %s" % (r.returncode, os.path.exists(out), r.stdout.decode("utf-8","replace").strip()[:60]))
if r.returncode != 0: print("  stderr:", r.stderr.decode("utf-8","replace")[-400:])
else:
    import docx
    d = docx.Document(out)
    txts = [x.text for x in d.paragraphs]
    print("  段落 %d ｜ 表格 %d ｜ 分页符 %d" % (len(txts), len(d.tables),
          sum(1 for x in d.element.body.iter() if x.tag.endswith('}br') and x.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type')=='page')))
    for k in ["• 无序一","1. 编号一","2. 编号二","分页后的段落。"]:
        print("     含 %-14s %s" % (k, any(k in x for x in txts)))

print()
print("="*100); print("### D. 归档旧克隆（先合并唯一内容 → 再归档 → 后删除）"); print("="*100)
ARC = os.path.join(TB,"_archive","legacy_docx_variants_2026-11-18")
os.makedirs(ARC, exist_ok=True)
CLONES = {
 "md_to_docx.py":       "编号列表(List Number)与原生 List Bullet 样式 —— 已并入正本 RE_OL；★ 『目录域』为误报（命中的是'根目录'二字）",
 "md_to_docx_clean.py": "无独有能力（正本并集已覆盖）",
 "md_to_docx_v1.0.py":  "无独有能力",
 "md_to_docx_v2.py":    "无独有能力",
 "md_to_docx_v3.py":    "无独有能力",
 "v4_to_docx.py":       "分页：原为一次性硬编码 add_page_break，非独立能力 —— 已在正本改为显式 <!-- pagebreak --> 标记",
}
man = {"date":"2026-11-18","rule":"先合并唯一内容 → 再归档 → 后删除（C06 同源治理）",
       "canonical":"skills/docx-md-bridge/scripts/md_to_docx.py","items":[]}
for name, note in CLONES.items():
    src = os.path.join(TB,name)
    if not os.path.exists(src):
        print("  ★ 缺 %s（可能已归档）" % name); continue
    b = open(src,"rb").read()
    dst = os.path.join(ARC,name)
    shutil.move(src,dst)
    man["items"].append({"file":name,"archived_to":os.path.relpath(dst,ROOT).replace(os.sep,"/"),
        "bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()[:16],"unique_preserved":note,
        "original_mtime":datetime.datetime.fromtimestamp(os.path.getmtime(dst)).strftime("%Y-%m-%d %H:%M:%S")})
    print("  ✔ %-24s → _archive/legacy_docx_variants_2026-11-18/  (%d B)" % (name, len(b)))
MP = os.path.join(ROOT,"output","audit_skills","legacy_docx_archive_manifest_2026-11-18.json")
os.makedirs(os.path.dirname(MP), exist_ok=True)
json.dump(man, open(MP,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("  清单落盘:", os.path.basename(MP))
print("  ★ 归档后 toolbox 根目录非下划线 .py: %d" % len([p for p in glob.glob(os.path.join(TB,"*.py")) if not os.path.basename(p).startswith("_")]))
