# -*- coding: utf-8 -*-
import io, sys, os, re, glob, json, hashlib, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
BASES = {"WS": os.path.join(ROOT,"skills"), "HOME": os.path.join(HOME,"skills"), "CLAUDE": os.path.join(HOME,".claude","skills")}
def nm_of(p):
    b = open(p,"rb").read()
    m = re.search(rb"^name:\s*(\S+)", b, re.M)
    return (m.group(1).decode("utf-8","replace") if m else os.path.basename(os.path.dirname(p))), b

print("="*94); print("### A. 27 组「内容冲突」—— 是不是只是 CRLF/LF 差异？"); print("="*94)
idx = {}
for lab, base in BASES.items():
    if not os.path.isdir(base): continue
    for f in glob.glob(os.path.join(base,"**","SKILL.md"), recursive=True):
        n, b = nm_of(f)
        idx.setdefault(n, []).append((lab, f, b))
crlf_only = 0; real_diff = []
for n, lst in idx.items():
    if len(lst) < 2: continue
    norm = {hashlib.md5(b.replace(b"\r\n", b"\n")).hexdigest() for _,_,b in lst}
    if len(norm) == 1:
        crlf_only += 1
    else:
        real_diff.append((n, [(l, len(b)) for l,_,b in lst]))
print("  归一化行尾后完全一致（即非真冲突）: %d 组" % crlf_only)
print("  ★ 真正内容不同: %d 组" % len(real_diff))
for n, d in real_diff[:20]:
    print("     %-32s %s" % (n[:32], " | ".join("%s %dB" % x for x in d)))

print()
print("="*94); print("### B. 17 组「真缺失引用文件」—— 文件去哪了？"); print("="*94)
MISS = ["business-intelligence","goal-management","hotel-new-media","hotel-private-domain",
        "hotel-revenue-management","memory-recall","startup-fundraising","strategic-decision-making",
        "diagram-design","gongwen-docx-cn","open-design","paradigm-router","ppt-visual-editor",
        "wayfinding-signage","wewrite-review","arkcli-api-explorer","Get笔记"]
for skill in MISS:
    # 该技能在三个位置的 SKILL.md 里分别引用了哪些缺失物
    refs = set()
    for lab, base in BASES.items():
        for f in glob.glob(os.path.join(base, skill, "**", "SKILL.md"), recursive=True):
            b = open(f,"rb").read().decode("utf-8","replace")
            for m in re.finditer(r"(?:scripts|references|templates|assets)/([A-Za-z0-9_\-\.]+)", b):
                p = os.path.join(os.path.dirname(f), m.group(0).replace("/", os.sep))
                if not os.path.exists(p): refs.add(m.group(0))
    if not refs: continue
    print("  %-30s 缺: %s" % (skill[:30], ", ".join(sorted(refs))[:88]))
    for r in sorted(refs):
        base_name = r.split("/")[-1]
        # 在全盘技能库 / git 里找同名文件
        hit = []
        for lab, base in BASES.items():
            for g in glob.glob(os.path.join(base, "**", base_name), recursive=True):
                hit.append("%s:%s" % (lab, os.path.relpath(g, base)))
        gs = ""
        r2 = subprocess.run(["git","-C",ROOT,"log","--all","--diff-filter=D","--name-only","--","*%s*"%base_name],
                            capture_output=True, timeout=40)
        if r2.stdout.strip():
            gs = " git曾有: " + r2.stdout.decode("utf-8","replace").strip().split("\n")[0][:48]
        print("       %-42s %s%s" % (r[:42], ("找到: " + "; ".join(hit[:2])) if hit else "★全盘无", gs))

print()
print("="*94); print("### C. 能力覆盖缺口（按今日实际失手推导，而非凭感觉）"); print("="*94)
GAP = [
 ("公文/报告排版", "gongwen-docx-cn / gongwen-report-cn", "有"),
 ("普通 md→docx", "docx-md-bridge", "有★但我今天没用"),
 ("PPT", "ppt-deck-builder-pro / ppt-visual-editor / powerpoint-pptx", "有"),
 ("信息图/海报", "article-to-infographic / china-poster-studio / infographic", "有"),
 ("收益管理", "hotel-revenue-management", "有（但缺 RMS 系统/自动化）"),
 ("OCR/文档解析", "无（我今天手搓 rapidocr 流程）", "★缺"),
 ("编码/文件完整性修复", "无（我今天手搓 fix_mixed_encoding）", "★缺"),
 ("断言/自检/回归", "无（我今天手搓 selfcheck）", "★缺"),
 ("自动化编排", "evolver / gstack-openclaw-*", "有（但未纳入调用逻辑）"),
 ("网页抓取", "ultimate-search / crawl4ai / playwright-mcp / apify-mcp / firecrawl", "有（firecrawl 待配 Key）"),
 ("本地搜索/语义", "openviking / local_semantic_search / memory-recall", "有"),
 ("成本治理", "cost-governor", "有（无 description 不可路由）"),
]
for cap, impl, st in GAP:
    print("  %-16s %-52s %s" % (cap, impl[:52], st))
