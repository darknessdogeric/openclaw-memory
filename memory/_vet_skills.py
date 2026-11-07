"""skill-vetter 协议: 抓取候选 skill 全部源码, 扫描红旗模式"""
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TMP = r"D:\B166ER-openclaw\workspace\memory\_vet_tmp"
os.makedirs(TMP, exist_ok=True)

CANDIDATES = {
    "interior-fullplan": ["SKILL.md", "generate_fullplan.py", "skill.json", "skill-card.md"],
    "cad-batch-processing": ["SKILL.md", "batch_export.py", "batch_modify.py",
                             "cad_utils.py", "generate_dwg.py", "skill-card.md"],
    "cad-agent": ["SKILL.md"],
    "openscad-automation": ["SKILL.md"],
}

# skill-vetter 红旗清单
RED_FLAGS = [
    (r"curl\s|wget\s|urllib\.request|requests\.(get|post|put)\(", "网络请求"),
    (r"http[s]?://(?!github\.com|docs\.python\.org|pypi\.org|www\.w3\.org)", "外部 URL"),
    (r"os\.environ|getenv\(|api[_-]?key|API_KEY|token|secret|password", "读取凭据/密钥"),
    (r"\.ssh|\.aws|\.config|\.npmrc|id_rsa|\.git-credentials", "访问敏感目录"),
    (r"MEMORY\.md|USER\.md|SOUL\.md|IDENTITY\.md", "读取 Agent 身份文件"),
    (r"base64|b64decode|codecs\.decode", "编码解码"),
    (r"\beval\(|\bexec\(|__import__\(|importlib", "动态执行"),
    (r"subprocess|os\.system|popen|shell=True", "执行系统命令"),
    (r"shutil\.rmtree|os\.remove|os\.unlink|rm -rf|Remove-Item", "删除文件"),
    (r"chmod|chown|sudo|runas", "提权"),
    (r"cookies|session_id|Authorization:\s*Bearer", "访问会话凭证"),
    (r"socket\.|listen\(|bind\(|0\.0\.0\.0|localhost:\d+", "开端口/监听"),
    (r"pip\s+install|npm\s+install|apt-get|conda install", "静默装包"),
    (r"\.ssh|\.git/config|registry.*token", "凭据文件"),
]

NODE = r"D:\Program Files\nodejs\node.exe"
CLI = r"C:\Users\ericz\AppData\Roaming\npm\node_modules\clawhub\bin\clawdhub.js"

results = {}
for slug, files in CANDIDATES.items():
    print("=" * 76)
    print(f"审查对象: {slug}")
    print("=" * 76)
    slug_dir = os.path.join(TMP, slug)
    os.makedirs(slug_dir, exist_ok=True)
    findings = []
    for fn in files:
        r = subprocess.run([NODE, CLI, "inspect", slug, "--file", fn],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        out = r.stdout or ""
        # 去掉 CLI 噪音行
        lines = [l for l in out.splitlines()
                 if "所在位置" not in l and "CategoryInfo" not in l
                 and "FullyQualifiedErrorId" not in l and "node.exe" not in l
                 and not l.startswith("  + ")]
        content = "\n".join(lines)
        with open(os.path.join(slug_dir, fn), "w", encoding="utf-8") as f:
            f.write(content)
        hits = []
        for pat, label in RED_FLAGS:
            for m in re.finditer(pat, content, re.IGNORECASE):
                ln = content[:m.start()].count("\n") + 1
                snippet = content.splitlines()[ln-1].strip()[:110]
                hits.append((label, ln, snippet))
        print(f"\n  {fn}  ({len(content)} bytes)")
        if hits:
            for label, ln, sn in hits[:12]:
                print(f"     [{label}] L{ln}: {sn}")
        else:
            print("     ✅ 无红旗命中")
        findings.extend((fn, h) for h in hits)
    results[slug] = findings
    print()

# 汇总
print("=" * 76)
print("红旗汇总")
print("=" * 76)
for slug, fs in results.items():
    if not fs:
        print(f"  {slug}: ✅ 干净")
    else:
        print(f"  {slug}: ⚠️ {len(fs)} 处命中")
        labels = {}
        for fn, (label, ln, sn) in fs:
            labels.setdefault(label, []).append(f"{fn}:L{ln}")
        for label, places in labels.items():
            print(f"      {label}: {', '.join(places[:6])}")
print(f"\n临时目录: {TMP}")
