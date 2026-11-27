"""平面设计类 skill 批量审查 (复用 skill-vetter 协议)"""
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

NODE = r"D:\Program Files\nodejs\node.exe"
CLI = r"C:\Users\ericz\AppData\Roaming\npm\node_modules\clawhub\bin\clawdhub.js"
TMP = r"D:\B166ER-openclaw\workspace\memory\_vet_tmp"


def run(args):
    r = subprocess.run([NODE, CLI] + args, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    out = r.stdout or ""
    return "\n".join(l for l in out.splitlines()
                     if "所在位置" not in l and "CategoryInfo" not in l
                     and "FullyQualifiedErrorId" not in l and "node.exe" not in l
                     and not l.startswith("  + ") and l.strip() != "")


RED = [
    (r"curl\s|wget\s|urllib\.request|requests\.(get|post|put)\(", "网络请求"),
    (r"http[s]?://(?!github\.com|docs\.python\.org|pypi\.org|www\.w3\.org|fonts\.googleapis|fonts\.gstatic)", "外部URL"),
    (r"os\.environ|getenv\(|api[_-]?key|API_KEY|secret|password", "读凭据"),
    (r"\.ssh|\.aws|\.git-credentials|id_rsa", "敏感目录"),
    (r"MEMORY\.md|USER\.md|SOUL\.md|IDENTITY\.md", "读Agent身份"),
    (r"base64|b64decode", "编码解码"),
    (r"\beval\(|\bexec\(|__import__\(", "动态执行"),
    (r"subprocess|os\.system|shell=True", "执行命令"),
    (r"shutil\.rmtree|os\.remove|os\.unlink", "删文件"),
    (r"chmod|sudo|runas", "提权"),
    (r"cookies|Authorization:\s*Bearer", "会话凭证"),
    (r"socket\.|listen\(|bind\(|0\.0\.0\.0", "开端口"),
    (r"pip\s+install|npm\s+install|apt-get", "装包"),
]

CANDS = ["brand-identity-design", "color-palette-advisor", "poster-design-studio", "fontpick"]

for slug in CANDS:
    print("=" * 74)
    print(f"【{slug}】")
    print("=" * 74)
    meta = run(["inspect", slug])
    for line in meta.splitlines():
        if any(k in line for k in ["Owner:", "Latest:", "License:", "Created:",
                                   "Updated:", "Security:", "Warnings:", "Checked:",
                                   "Summary:", "Selected:"]):
            print("  " + line)
    files_meta = run(["inspect", slug, "--files"])
    filelist = [l.strip() for l in files_meta.splitlines()
                if l.strip() and not any(k in l for k in
                   ["Owner:", "Latest:", "License:", "Created:", "Updated:", "Security:",
                    "Warnings:", "Checked:", "Summary:", "Selected", "Changelog", "- "])]
    print(f"\n  文件:")
    for fl in filelist[:15]:
        print("    " + fl)

    slug_dir = os.path.join(TMP, slug)
    os.makedirs(slug_dir, exist_ok=True)
    total_hits = 0
    for row in filelist[:12]:
        parts = row.split()
        if not parts:
            continue
        fn = parts[0]
        if not fn or fn.endswith(":"):
            continue
        content = run(["inspect", slug, "--file", fn])
        dest = os.path.join(slug_dir, fn)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(content)
        hits = []
        for pat, label in RED:
            for m in re.finditer(pat, content, re.IGNORECASE):
                ln = content[:m.start()].count("\n") + 1
                lines = content.splitlines()
                sn = lines[ln - 1].strip()[:100] if ln <= len(lines) else ""
                hits.append((label, ln, sn))
        if hits:
            total_hits += len(hits)
            print(f"\n    {fn} ({len(content)}B):")
            for label, ln, sn in hits[:8]:
                print(f"       [{label}] L{ln}: {sn}")
    print(f"\n  >>> 红旗命中合计: {total_hits}")
    print()
