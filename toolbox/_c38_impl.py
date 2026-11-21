# -*- coding: utf-8 -*-
"""
_c38_impl.py —— B 标旧形态扫描（补齐 C37 的两个漏洞）

漏洞（2026-11-21 实测，均由我自己踩出来）：
  漏洞1 扫描根只有 memory/toolbox/anyi-ops-kb/skills
        -> outputs/ 与 obsidian-vault/ 两个活件目录从未被扫过，旧形态长期漏网
  漏洞2 正则用 \\s* 跨行匹配
        -> 匹配可吞掉两词之间整段文档；且校验函数若复用同一正则归一化，会把"删除"一起归一化 -> 假绿
        -> 本实现两侧只允许 [空格/制表/不换行空格]，绝不跨行；扫描与校验用同一套安全正则

范围：工作区全部活件目录（排除 .git/node_modules/.backups 归档/anyi 他人工作树/
      brand_rename_2026-11-21 整改工作区/_archive）
例外：AGENTS.md（规则文档须引用被禁形态作举例）与 anyi/（他人 agent 工作树）不判 FAIL
"""
import os
import re

# 安全正则：分隔符两侧只允许水平空白，绝不跨行
_PAD = r"[ \t\u00a0]*"
_SEP = r"[\u00d7\u2715Xx\uFF38\u00b7]"
OLD1 = re.compile(r"ERIC" + _PAD + _SEP + _PAD + r"B166ER")
OLD2 = re.compile(r"B166ER" + _PAD + _SEP + _PAD + r"ERIC")

EXTS = (".md", ".txt", ".html", ".htm", ".css", ".js", ".json", ".py", ".csv")
SKIP_DIRS = {"node_modules", ".git", "__pycache__", "site-packages", ".venv", "venv",
             ".chroma_db", ".edge-screenshot", ".tmp", ".backups", "_archive",
             "brand_rename_2026-11-21"}
# 顶层排除：归档区 / 他人 agent 工作树 / 整改工作区
SKIP_TOP = {"anyi", "output", ".scratch"}
# 规则文档：正文须引用被禁形态作举例，不判 FAIL
EXEMPT_FILES = {"AGENTS.md"}


def _scan(root):
    bad = []
    for base, dirs, files in os.walk(root):
        rel = os.path.relpath(base, root)
        top = rel.split(os.sep)[0] if rel != "." else ""
        if top in SKIP_TOP:
            dirs[:] = []
            continue
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for f in files:
            if os.path.splitext(f)[1].lower() not in EXTS:
                continue
            if f in EXEMPT_FILES:
                continue
            p = os.path.join(base, f)
            try:
                if os.path.getsize(p) > 8_000_000:
                    continue
                with open(p, encoding="utf-8", errors="replace") as fh:
                    tx = fh.read()
            except Exception:
                continue
            n = 0
            for ln in tx.split("\n"):          # 逐行判定，杜绝跨行吞内容
                if OLD1.search(ln) or OLD2.search(ln):
                    n += 1
            if n:
                bad.append(os.path.relpath(p, root).replace("\\", "/") + ":" + str(n))
    return bad


def check(root):
    bad = []
    for top in ("memory", "toolbox", "anyi-ops-kb", "skills", "outputs", "obsidian-vault"):
        rt = os.path.join(root, top)
        if os.path.isdir(rt):
            bad.extend(_scan(rt))
    if bad:
        return False, ("旧 B 标形态残留 " + str(len(bad)) + " 处（outputs/ 与 obsidian-vault/ 已纳入扫描）: "
                       + "; ".join(bad[:3])), bad[:3]
    return True, "B 标统一 ERIC & B166ER ｜ 6 根扫描（旧形态 0 残留，不跨行判定）", []


if __name__ == "__main__":
    import sys
    ok, msg, det = check(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(msg)
    for d in det:
        print("  - " + str(d))
    sys.exit(0 if ok else 1)
