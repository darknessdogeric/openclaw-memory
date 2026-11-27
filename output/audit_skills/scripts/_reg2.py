# -*- coding: utf-8 -*-
import io, sys, os, re, glob, json, shutil, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
TB = os.path.join(ROOT, "toolbox")
REGJ = os.path.join(ROOT, "output", "audit_skills", "SKILL_REGISTRY.json")

print("="*94); print("### A. toolbox 里到底有几个 md→docx 变体（重复造轮子的实证）"); print("="*94)
fam = [p for p in sorted(glob.glob(os.path.join(TB,"*.py")))
      if re.search(r"(docx|md2docx|md_to_docx|md2gongwen)", os.path.basename(p), re.I)]
for p in fam:
    t = open(p, encoding="utf-8", errors="replace").read()
    head = next((l.strip() for l in t.split("\n")[:6] if l.strip() and not l.strip().startswith("#")), "")
    fonts = sorted(set(re.findall(r"['\"](等线|宋体|黑体|微软雅黑|方正小标宋简体)['\"]", t)))
    print("   %-30s %6d B ｜ 字体 %-22s %s" % (os.path.basename(p), len(t), ",".join(fonts) or "-", head[:40]))
print("   → 同族 %d 个；加上 skills/docx-md-bridge = %d 套" % (len(fam), len(fam)+1))

print()
print("="*94); print("### B. 今天新造的 6 个工具 —— 注册进技能层（让它们可被路由）"); print("="*94)
NEW = {
 "self-check-assertions": {
   "files": ["toolbox/selfcheck.py"],
   "desc": "把每条教训写成可 PASS/FAIL 的断言并自动执行：编码完整性、HOT 层上限与时效、索引一致性、分层非空、正本唯一、不重复造轮子、技能可路由、日志不膨胀、日记被读回、纠错已下沉、PREFLIGHT 存在、信息图三层质检。触发：交付前自检、回归断言、失败即拦、selfcheck、每条教训如何变成机器可执行的规则。"},
 "skill-registry-router": {
   "files": ["toolbox/skill_router.py"],
   "desc": "技能与工具路由：按任务类型检索既有技能/工具，命中即用不得自建；含自建前查重（--check）与固定工作流表。触发：动手前查有没有现成工具、选哪个技能、任务到技能的映射、避免重复造轮子。"},
 "evolution-scan": {
   "files": ["toolbox/evolution_scan.py","toolbox/evolution_watch.py","toolbox/evolution_watch_trigger2.js","toolbox/evolution_scan_payload.js"],
   "desc": "自进化扫描与缺席告警：周期性跑断言并写扫描记录（eval/），并由独立探测器按「缺席>8 天 / 连续 2 次未全绿」触发告警。触发：让自进化从靠记性变成制度保证、周期回归、缺席检测、eval 断链修复。"},
 "doc-encoding-repair": {
   "files": ["toolbox/fix_mixed_encoding.py"],
   "desc": "混合编码与文件完整性修复：结构化切分识别 UTF-8/GB18030 混合块，逐字符安全解码，保留字节原件，不可逆者标注留痕。触发：文件读不出来、U+FFFD 乱码、PowerShell 追加破坏 UTF-8、编码损坏批量修复。"},
 "topology-infographic": {
   "files": ["toolbox/make_topology.py"],
   "desc": "信息拓扑图生成器：单一 SVG 源出 3:4 与 9:16 两版，自动三层质检（盒模型/SVG 元素级重叠·越界·压曲线·死白/视觉核验）。触发：把系统结构画成拓扑图、机制可视化、9:16 手机长图、认知拓扑、信息架构图。"},
}
mk = 0
for name, spec in NEW.items():
    d = os.path.join(ROOT, "skills", name)
    os.makedirs(d, exist_ok=True)
    for rel in spec["files"]:
        src = os.path.join(ROOT, rel.replace("/", os.sep))
        if not os.path.exists(src):
            print("   ★ 缺源:", rel); continue
        shutil.copy2(src, os.path.join(d, os.path.basename(rel)))
    skill = """---
name: %s
description: %s
---

# %s

> **来源**：`%s`（2026-11-17 自进化重构中从一次性脚本沉淀为技能）
> **用法**：见同目录脚本；`python <脚本> --help`

## 何时用

%s

## 边界（不要越界）

- 本技能只负责"%s"这一件事；相邻能力走其它技能（见 `skills/` 与 `output/audit_skills/WORKFLOWS.json`）
- **动手前先跑 `python toolbox/skill_router.py --task "<任务>"`**，命中既有技能就用既有技能，**不要自建同类工具**
""" % (name, spec["desc"], name, " / ".join(spec["files"]), spec["desc"], name.split("-")[0])
    open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8", newline="\n").write(skill)
    mk += 1
    print("   ✔ %-26s %d 个文件" % (name, len(spec["files"])))
print("   → 新建技能 %d 个" % mk)

print()
print("="*94); print("### C. 建工具索引（防再次出现未登记的轮子）"); print("="*94)
TOOLS = {}
for p in sorted(glob.glob(os.path.join(TB,"*.py"))):
    b = os.path.basename(p)
    if b.startswith("_"): continue
    t = open(p, encoding="utf-8", errors="replace").read()
    purpose = next((l.strip() for l in t.split("\n")[:8] if l.strip() and not l.strip().startswith("#")), "")[:150]
    TOOLS["toolbox/"+b] = {"bytes": len(t), "purpose": purpose, "skill_equivalent": "", "scope_note": ""}
# 已知对应关系
MAP = {
 "toolbox/md2docx.py": ("docx-md-bridge", "★研判报告排版变体（宋体/黑体/纸色主题）。**通用 md→docx 请用 skills/docx-md-bridge**"),
 "toolbox/md_to_docx.py": ("docx-md-bridge", "旧克隆，已被 docx-md-bridge 取代"),
 "toolbox/md_to_docx_clean.py": ("docx-md-bridge", "旧克隆，已被 docx-md-bridge 取代"),
 "toolbox/md_to_docx_v1.0.py": ("docx-md-bridge", "旧克隆，已被 docx-md-bridge 取代"),
 "toolbox/md_to_docx_v2.py": ("docx-md-bridge", "旧克隆，已被 docx-md-bridge 取代"),
 "toolbox/md_to_docx_v3.py": ("docx-md-bridge", "旧克隆，已被 docx-md-bridge 取代"),
 "toolbox/md2gongwen_docx.py": ("gongwen-docx-cn", "公文版式（旧克隆）"),
 "toolbox/v4_to_docx.py": ("docx-md-bridge", "旧克隆"),
 "toolbox/selfcheck.py": ("self-check-assertions", "自检断言执行器（本技能正主）"),
 "toolbox/skill_router.py": ("skill-registry-router", "技能路由（本技能正主）"),
 "toolbox/evolution_scan.py": ("evolution-scan", "扫描器（本技能正主）"),
 "toolbox/evolution_watch.py": ("evolution-scan", "缺席探测器（本技能正主）"),
 "toolbox/fix_mixed_encoding.py": ("doc-encoding-repair", "编码修复器（本技能正主）"),
 "toolbox/make_topology.py": ("topology-infographic", "拓扑图生成器（本技能正主）"),
}
for k,(sk,note) in MAP.items():
    if k in TOOLS:
        TOOLS[k]["skill_equivalent"] = sk; TOOLS[k]["scope_note"] = note
TI = os.path.join(ROOT, "output", "audit_skills", "TOOL_INDEX.json")
json.dump(TOOLS, open(TI,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("   工具索引: %d 个工具 → %s" % (len(TOOLS), os.path.basename(TI)))
dupe = [k for k,v in TOOLS.items() if v["skill_equivalent"] and v["skill_equivalent"] != "" and "取代" in v["scope_note"]]
print("   ★ 已标记为『旧克隆，应被取代』: %d 个" % len(dupe))
for k in dupe: print("      ", k)
