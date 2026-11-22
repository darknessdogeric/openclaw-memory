#!/usr/bin/env python3
"""
comprehensive_health_check.py v2.0 - 无缝适配版
==============================================

核心理念 (Eric 2026-09-04 00:30 "无缝适配"):
- ❌ 不猜测路径 (信源矩阵 → 实际在 04_信源体系)
- ✅ 内容驱动的发现 (Content-based discovery)
- ✅ 多命名容错 (Fuzzy directory matching)
- ✅ 自适应扫描 (Adaptive scanning)

检查项 (8 大维度, 全部基于内容自动发现):
1. SOUL.md (人格层)
2. MEMORY.md (快速入口层)
3. USER.md (Eric 偏好层)
4. IDENTITY.md
5. AGENTS.md
6. anyi-ops-kb (业务事实层, 按内容分类)
7. memory (历史 daily notes)
8. toolbox/*.py
9. 信源矩阵 (内容驱动发现)
10. SKILL 库 (skill_workshop 内容)
11. 安逸集团知识库
12. OpenClaw 备份链

每项检查: 存在/编码/R66/时间戳/大小/关键段
"""
from __future__ import annotations
import sys
import io
import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

# Force UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

WORKSPACE = Path(__file__).resolve().parent.parent
R66_BANNED = ("350亿", "本奥米尔", "Benoemir")
TRACE_MARKERS = (
    "R66", "修订", "修复", "清理", "删除", "硬编码", "含", "留痕", "违规",
    "重生成", "扫描", "→", "虚构", "修正", "已清理", "同类", "L1", "L2", "L3",
)


def safe_read(path: Path) -> str:
    """Try multiple encodings, return content"""
    try:
        raw = path.read_bytes()
    except Exception:
        return ""
    for enc in ["utf-8", "gbk", "gb18030"]:
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="ignore")


def r66_count(content: str) -> tuple[int, list[str]]:
    """Count active R66 violations (excluding 留痕 logs)"""
    hits = []
    for term in R66_BANNED:
        for line in content.split("\n"):
            if term in line:
                if not any(m in line for m in TRACE_MARKERS):
                    hits.append(f"{term}: {line.strip()[:80]}")
                    break
    return len(hits), hits[:5]


def check_file(label: str, path: Path, key_sections: Optional[list] = None) -> dict:
    """Check a single file"""
    out = {"label": label, "path": str(path), "exists": False}
    if not path.exists():
        out["status"] = "NOT_FOUND"
        return out
    out["exists"] = True
    out["size_kb"] = round(path.stat().st_size / 1024, 1)
    out["mtime"] = datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds")

    content = safe_read(path)
    out["r66_violations"] = r66_count(content)[0]

    if key_sections:
        out["key_sections"] = {}
        for sec in key_sections:
            out["key_sections"][sec] = "yes" if sec in content else "NO"

    out["status"] = "OK" if out["r66_violations"] == 0 else "FAIL"
    return out


def find_content_based(label: str, search_dirs: list[Path], content_keywords: list[str],
                       min_score: int = 3, key_sections: Optional[list] = None,
                       filename_match: Optional[list[str]] = None) -> dict:
    """
    无缝适配版 v2.1: 文件名优先 (filename = 人为意图, content = 偶然)
    1. 扫描所有 .md 文件
    2. 如果有任何文件匹配 filename_match → 优先选该文件 (权重无限)
    3. 否则 fallback 到 content scoring
    4. 这样避免"培训手册"这种大体量高关键词密度的错误匹配
    """
    out = {"label": label, "search_dirs": [str(d) for d in search_dirs], "status": "NOT_FOUND"}
    candidates = []
    filename_patterns = filename_match or content_keywords

    # Phase 1: 文件名优先 (任意匹配 → 胜出)
    filename_winner = None
    filename_winner_score = 0

    for d in search_dirs:
        if not d.exists():
            continue
        for f in d.rglob("*.md"):
            try:
                fname = f.name
                filename_hits = sum(fname.count(p) for p in filename_patterns)
                if filename_hits > 0 and filename_hits > filename_winner_score:
                    content = safe_read(f)
                    filename_winner = (filename_hits, f, content)
                    filename_winner_score = filename_hits
            except Exception:
                continue

    if filename_winner:
        filename_hits, best_file, best_content = filename_winner
        # Still compute content score for reporting
        content_score = sum(best_content.count(kw) for kw in content_keywords)
        # Filename winner wins by default
        out["best_file"] = str(best_file) if not str(best_file).startswith(str(WORKSPACE)) else str(best_file.relative_to(WORKSPACE))
        out["best_score"] = filename_hits * 100 + content_score
        out["content_score"] = content_score
        out["filename_score"] = filename_hits
        out["total_candidates"] = 1
        out["size_kb"] = round(best_file.stat().st_size / 1024, 1)
        out["mtime"] = datetime.fromtimestamp(best_file.stat().st_mtime).isoformat(timespec="seconds")
        out["selection_method"] = "filename_match"
        out["r66_violations"] = r66_count(best_content)[0]
        if key_sections:
            out["key_sections"] = {}
            for sec in key_sections:
                out["key_sections"][sec] = "yes" if sec in best_content else "NO"
        out["status"] = "OK" if out["r66_violations"] == 0 else "FAIL"
        return out

    # Phase 2: Fallback - content-based scoring
    for d in search_dirs:
        if not d.exists():
            continue
        for f in d.rglob("*.md"):
            try:
                content = safe_read(f)
                fname = f.name
                content_score = sum(content.count(kw) for kw in content_keywords)
                filename_score = sum(fname.count(p) for p in filename_patterns)
                total_score = content_score + filename_score * 10
                if total_score >= min_score:
                    candidates.append((total_score, content_score, filename_score, f, content))
            except Exception:
                continue

    if not candidates:
        return out

    candidates.sort(key=lambda x: (-x[0], -x[2]))
    best_score, best_content_score, best_filename_score, best_file, best_content = candidates[0]

    out["best_file"] = str(best_file) if not str(best_file).startswith(str(WORKSPACE)) else str(best_file.relative_to(WORKSPACE))
    out["best_score"] = best_score
    out["content_score"] = best_content_score
    out["filename_score"] = best_filename_score
    out["total_candidates"] = len(candidates)
    out["size_kb"] = round(best_file.stat().st_size / 1024, 1)
    out["mtime"] = datetime.fromtimestamp(best_file.stat().st_mtime).isoformat(timespec="seconds")
    out["selection_method"] = "content_score"

    out["r66_violations"] = r66_count(best_content)[0]

    if key_sections:
        out["key_sections"] = {}
        for sec in key_sections:
            out["key_sections"][sec] = "yes" if sec in best_content else "NO"

    out["status"] = "OK" if out["r66_violations"] == 0 else "FAIL"
    return out


def scan_dir_content(label: str, dir_path: Path, content_keywords: list[str],
                     min_score: int = 3, file_pattern: str = "*.md") -> dict:
    """Scan a directory for content matching keywords"""
    out = {"label": label, "path": str(dir_path), "exists": dir_path.exists()}
    if not dir_path.exists():
        out["status"] = "NOT_FOUND"
        return out

    files = list(dir_path.rglob(file_pattern))
    out["total_files"] = len(files)
    out["total_size_mb"] = round(sum(f.stat().st_size for f in files) / (1024 * 1024), 2)

    # Find files matching content
    matching_files = []
    for f in files:
        content = safe_read(f)
        score = sum(content.count(kw) for kw in content_keywords)
        if score >= min_score:
            matching_files.append(f)
    out["matching_files"] = len(matching_files)
    out["matching_sample"] = [str(f.relative_to(dir_path)) for f in matching_files[:5]]

    # Recent files
    if files:
        files_sorted = sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)
        out["latest_5"] = [
            {
                "path": str(f.relative_to(dir_path)),
                "size_kb": round(f.stat().st_size / 1024, 1),
                "mtime": datetime.fromtimestamp(f.stat().st_mtime).isoformat(timespec="seconds"),
            }
            for f in files_sorted[:5]
        ]

    # R66 across all matching files
    total_r66 = 0
    for f in matching_files:
        content = safe_read(f)
        cnt, _ = r66_count(content)
        total_r66 += cnt
    out["r66_violations"] = total_r66

    out["status"] = "OK" if total_r66 == 0 else "FAIL"
    return out


def main():
    results = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "version": "v2.0-seamless",
        "checks": [],
    }

    # 1. SOUL.md
    results["checks"].append(check_file(
        "SOUL.md (人格层)",
        WORKSPACE / "SOUL.md",
        ["V2.0", "V2.4", "认知分层架构", "群论", "博弈论", "审美"],
    ))

    # 2. MEMORY.md
    results["checks"].append(check_file(
        "MEMORY.md (快速入口层)",
        WORKSPACE / "MEMORY.md",
        ["安逸集团", "R66", "知识库"],
    ))

    # 3. USER.md
    results["checks"].append(check_file(
        "USER.md (Eric 偏好层)",
        WORKSPACE / "USER.md",
        ["Eric", "红绿灯"],
    ))

    # 4. IDENTITY.md
    results["checks"].append(check_file("IDENTITY.md", WORKSPACE / "IDENTITY.md"))

    # 5. AGENTS.md
    results["checks"].append(check_file(
        "AGENTS.md (启动指南)",
        WORKSPACE / "AGENTS.md",
        ["R66", "R67", "R291", "R292"],
    ))

    # 6. anyi-ops-kb (业务事实层)
    results["checks"].append(scan_dir_content(
        "anyi-ops-kb (业务事实层)",
        WORKSPACE / "anyi-ops-kb",
        content_keywords=["安逸", "锦江", "华住", "首旅", "亚朵", "酒店"],
        min_score=2,
    ))

    # 7. memory (历史 daily notes)
    results["checks"].append(scan_dir_content(
        "memory (历史 daily notes)",
        WORKSPACE / "memory",
        content_keywords=["daily", "日志", "迭代", "R60"],
        min_score=1,
    ))

    # 8. 信源矩阵 — CONTENT-BASED DISCOVERY (无缝适配核心)
    results["checks"].append(find_content_based(
        "信源矩阵 (内容驱动发现)",
        search_dirs=[WORKSPACE / "anyi-ops-kb", WORKSPACE / "memory" / "archive_hotel"],
        content_keywords=[
            "信源", "source", "STR", "Skift", "Phocuswright", "奥维", "迈点",
            "浩华", "STR Benchmark", "TrendRadar", "RSS", "平台热搜",
        ],
        min_score=4,
        filename_match=["全域信源体系", "信源体系建设方案", "全域信源", "全域信源矩阵"],
        key_sections=["信源", "领域", "数据等级"],
    ))

    # 9. SKILL 库 — 扫描所有 SKILL.md, 列出全部 + 计数 (不只是首个)
    skill_locations = [
        WORKSPACE / "toolbox" / "skills",
        Path(os.path.expanduser("~/AppData/Roaming/openclaw/skills")),
        Path(os.path.expanduser("~/.openclaw/skills")),
    ]
    all_skills = []
    for loc in skill_locations:
        if loc.exists():
            for skill_dir in loc.iterdir():
                if skill_dir.is_dir():
                    skill_md = skill_dir / "SKILL.md"
                    if skill_md.exists():
                        all_skills.append({
                            "name": skill_dir.name,
                            "path": str(skill_md),
                            "size_kb": round(skill_md.stat().st_size / 1024, 1),
                            "mtime": datetime.fromtimestamp(skill_md.stat().st_mtime).isoformat(timespec="seconds"),
                        })
    # 排序: 最近修改优先
    all_skills.sort(key=lambda x: x["mtime"], reverse=True)
    skill_check = {
        "label": "SKILL 库 (全部扫描)",
        "search_dirs": [str(l) for l in skill_locations],
        "total_skills": len(all_skills),
        "skills": all_skills[:20],  # 最近 20 个
        "status": "OK" if len(all_skills) > 0 else "EMPTY",
    }
    results["checks"].append(skill_check)

    # 10. 安逸集团总览 — 文件名优先 (filename = "00_安逸集团知识库总览.md")
    results["checks"].append(find_content_based(
        "安逸集团知识库总览",
        search_dirs=[WORKSPACE / "anyi-ops-kb"],
        content_keywords=["安逸集团", "基础认知"],
        min_score=10,
        filename_match=["安逸集团知识库总览", "安逸集团总览"],
        key_sections=["基础认知", "v2.0", "MOC"],
    ))

    # 11. toolbox/*.py
    toolbox_path = WORKSPACE / "toolbox"
    if toolbox_path.exists():
        py_files = list(toolbox_path.glob("*.py"))
        results["checks"].append({
            "label": "toolbox/*.py (脚本)",
            "total": len(py_files),
            "status": "OK" if len(py_files) > 0 else "EMPTY",
        })

    # 12. OpenClaw 备份链
    backup_files = []
    home = Path(os.path.expanduser("~/.openclaw/state"))
    if home.exists():
        for f in home.glob("*"):
            if "backup" in f.name or "migration" in f.name:
                backup_files.append({
                    "name": f.name,
                    "size_mb": round(f.stat().st_size / (1024 * 1024), 1),
                })
    results["checks"].append({
        "label": "OpenClaw 备份链",
        "files": backup_files,
        "status": "OK" if len(backup_files) >= 3 else "INCOMPLETE",
    })

    # 输出 JSON
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())