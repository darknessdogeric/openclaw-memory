# -*- coding: utf-8 -*-
import io, sys, os, re, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
import requests
H = {"User-Agent":"openclaw-skill-audit","Accept":"application/vnd.github+json"}

def gh(q, per=5):
    try:
        r = requests.get("https://api.github.com/search/repositories", params={"q":q,"per_page":per,"sort":"stars"}, headers=H, timeout=30)
        if r.status_code != 200: return []
        return [(i["full_name"], i["stargazers_count"], (i.get("description") or "")[:66]) for i in r.json().get("items",[])]
    except Exception as e:
        return []

print("="*94); print("### A. 三个能力缺口 · GitHub 上有无现成"); print("="*94)
Q = [
 ("OCR / PDF 文档解析", "openclaw skills OCR pdf document parse"),
 ("编码修复 / 文件完整性", "openclaw skills encoding repair file integrity"),
 ("断言 / 自检 / 回归测试", "openclaw skills test assertion regression harness"),
]
for cap, q in Q:
    print()
    print("  【%s】" % cap)
    for full, st, de in gh(q, 4):
        print("     %-46s ★%-6s %s" % (full[:46], st, de))

print()
print("="*94); print("### B. 官方技能注册表 openclaw/clawhub —— 有哪些可装"); print("="*94)
for q in ["repo:openclaw/clawhub skills", "repo:VoltAgent/awesome-openclaw-skills"]:
    for full, st, de in gh(q, 3):
        print("   %-48s ★%-7s %s" % (full[:48], st, de))

print()
print("="*94); print("### C. awesome-openclaw-skills 里是否已有 OCR/测试/编码类技能"); print("="*94)
try:
    r = requests.get("https://api.github.com/repos/VoltAgent/awesome-openclaw-skills/contents/skills",
                     headers=H, timeout=30)
    if r.status_code == 200:
        items = r.json()
        names = [i["name"] for i in items]
        print("   官方 awesome 集合技能数: %d" % len(names))
        KW = ["ocr","pdf","doc","test","assert","lint","format","encod","valid","audit","regress"]
        hit = [n for n in names if any(k in n.lower() for k in KW)]
        print("   ★ 与本方缺口相关（ocr/pdf/test/assert/format/audit/valid/regress）: %d" % len(hit))
        print("   ", ", ".join(hit[:40]))
        print()
        print("   其余可用于补缺的具体候选:")
        for cand in hit[:16]:
            print("     - %s" % cand)
    else:
        print("   目录 API rc=%s（仓库结构可能不同，改用 tree 探测）" % r.status_code)
        r2 = requests.get("https://api.github.com/repos/VoltAgent/awesome-openclaw-skills/git/trees/main?recursive=1", headers=H, timeout=40)
        if r2.status_code == 200:
            paths = [x["path"] for x in r2.json().get("tree",[]) if x["path"].endswith("SKILL.md")]
            print("   全树 SKILL.md 数: %d" % len(paths))
            KW = ["ocr","pdf","doc","test","assert","lint","format","encod","valid","audit","regress","md2docx","docx"]
            hit = sorted({p.split("/")[-2] for p in paths if any(k in p.lower() for k in KW)})
            print("   ★ 相关候选 %d:" % len(hit))
            print("   ", ", ".join(hit[:44]))
except Exception as e:
    print("   GitHub 探测失败:", str(e)[:120])

print()
print("="*94); print("### D. clawhub CLI 复查（上次失败是否因缺参数）"); print("="*94)
CLI = os.path.join(HOME, "AppData", "Roaming", "npm", "openclaw.cmd")
for args in [["clawhub","list"], ["clawhub","search","ocr"], ["skills","list"]]:
    try:
        r = subprocess.run([CLI]+args, capture_output=True, timeout=60)
        out = (r.stdout.decode("utf-8","replace") or r.stderr.decode("utf-8","replace")).strip().replace("\n"," | ")
        print("   %-28s rc=%s  %s" % (" ".join(args), r.returncode, out[:150]))
    except Exception as e:
        print("   %-28s 失败 %s" % (" ".join(args), str(e)[:70]))
