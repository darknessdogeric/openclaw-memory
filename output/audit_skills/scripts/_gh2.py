# -*- coding: utf-8 -*-
import io, sys, os, re, glob, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
import requests
H = {"User-Agent":"openclaw-audit","Accept":"application/vnd.github+json"}

print("="*94); print("### A. agent-reach（AGENTS.md 称『17平台路由表已就位』）—— 实测在不在/能不能用"); print("="*94)
ar = os.path.join(HOME, ".agents", "skills", "agent-reach")
print("  路径:", ar, "| 存在:", os.path.isdir(ar))
if os.path.isdir(ar):
    for f in sorted(glob.glob(os.path.join(ar, "**","*"), recursive=True))[:14]:
        if os.path.isfile(f): print("     %8d B  %s" % (os.path.getsize(f), os.path.relpath(f, ar)))
    sk = os.path.join(ar, "SKILL.md")
    if os.path.exists(sk):
        t = open(sk, encoding="utf-8", errors="replace").read()
        plats = sorted(set(re.findall(r"\b(twitter|reddit|youtube|instagram|tiktok|linkedin|xiaoHongShu|zhihu|weibo|wechat|douyin|bilibili|x|telegram|discord|medium|substack|hackernews|indiehackers|producthunt)\b", t.lower())))
        print("   SKILL.md %d B ｜ 提及平台: %s" % (len(t), ", ".join(plats) if plats else "未识别"))
        m = re.search(r"^description:\s*(.+)$", t, re.M)
        print("   description:", m.group(1)[:100] if m else "无")

print()
print("="*94); print("### B. clawhub 官方注册表 69 个技能全表（挑可补缺口的）"); print("="*94)
t = requests.get("https://api.github.com/repos/openclaw/clawhub/git/trees/main?recursive=1", headers=H, timeout=60)
paths = [x["path"] for x in t.json().get("tree",[]) if x["path"].endswith("SKILL.md")]
names = sorted(p.split("/")[-2] for p in paths)
print("  共 %d 个: %s" % (len(names), ", ".join(names)))
KW = ["ocr","pdf","doc","assert","regress","test","lint","encod","valid","audit","review","cost","budget"]
hit = [n for n in names if any(k in n.lower() for k in KW)]
print()
print("  ★ 与本方缺口/强需求相关候选 %d: %s" % (len(hit), ", ".join(hit)))

print()
print("="*94); print("### C. 缺口三件套在 GitHub 上有无可直接用的现成件"); print("="*94)
for cap, q in [("OCR/文档解析", "clawskills.sh OCR skill PDF extract"),
                ("断言/自检/回归", "clawhub skill test assertion agent"),
                ("编码/文件完整性", "skill agent file encoding integrity check")]:
    try:
        r = requests.get("https://api.github.com/search/repositories", params={"q":q,"per_page":3,"sort":"stars"}, headers=H, timeout=30)
        print("  【%s】" % cap)
        for it in r.json().get("items",[])[:3]:
            print("     %-46s ★%-6s %s" % (it["full_name"][:46], it["stargazers_count"], (it.get("description") or "")[:52]))
    except Exception as e:
        print("  【%s】失败 %s" % (cap, str(e)[:60]))
