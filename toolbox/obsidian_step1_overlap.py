#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 1: 找桌面 vs vault 的同名/同名类似文件,识别重叠
输出: overlap_report.json + overlap_summary.md
"""
import json
import hashlib
from pathlib import Path
from datetime import datetime

DESK = Path(r"C:\Users\ericz\Desktop")
VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")

# 关键的桌面目录(放这里的 .md 可能与 vault 重叠)
KEY_DIRS = [
    "张实项目总控",
    "新媒体产品线",
    "小红书产品线",
    "AHL源代码",
    "AHL专利申请文件",
    "专利",
    "专利补正",
    "软著申请材料-AHL",
    "安逸集团_入职物料_20260707",
    "知局_完整版_v1.0",
    "AHL-BP-2026",
    "自我革命",
    "工作文档",
]

def md5(p: Path):
    h = hashlib.md5()
    try:
        with p.open('rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def scan():
    report = {
        "generated_at": datetime.now().isoformat(),
        "vault_md_total": sum(1 for _ in VAULT.rglob("*.md")),
        "desktop_md_total": 0,
        "by_dir": {},
        "overlaps_exact": [],
        "overlaps_name_only": [],
        "desktop_unique": {},
    }

    # 1) 取 vault 全部 .md: {name: [(path, md5), ...]}
    vault_index = {}
    for p in VAULT.rglob("*.md"):
        n = p.name
        h = md5(p)
        if h:
            vault_index.setdefault(n, []).append({"path": str(p), "md5": h, "size": p.stat().st_size})

    # 2) 扫每个桌面目录
    for d in KEY_DIRS:
        dp = DESK / d
        if not dp.exists(): continue
        md_files = list(dp.rglob("*.md"))
        report["desktop_md_total"] += len(md_files)
        report["by_dir"][d] = {
            "md_count": len(md_files),
            "files": []
        }
        for m in md_files:
            # 相对桌面路径
            rel = str(m.relative_to(DESK)).replace("\\", "/")
            h = md5(m)
            entry = {
                "rel": rel,
                "name": m.name,
                "md5": h,
                "size": m.stat().st_size,
                "in_vault": m.name in vault_index,
                "vault_match": []
            }
            if m.name in vault_index:
                # 检查 md5 是否完全相同
                for vp in vault_index[m.name]:
                    entry["vault_match"].append({
                        "path": vp["path"].replace(str(VAULT), "[VAULT]"),
                        "md5": vp["md5"],
                        "same_md5": vp["md5"] == h
                    })
                if any(vm["same_md5"] for vm in entry["vault_match"]):
                    report["overlaps_exact"].append({
                        "desktop": rel,
                        "name": m.name,
                        "vault_paths": [vm["path"] for vm in entry["vault_match"] if vm["same_md5"]],
                    })
                else:
                    report["overlaps_name_only"].append({
                        "desktop": rel,
                        "name": m.name,
                        "vault_paths": [vm["path"] for vm in entry["vault_match"]],
                    })
            else:
                report["desktop_unique"].setdefault(d, []).append(rel)
            report["by_dir"][d]["files"].append(entry)

    # 写报告
    out = Path(r"D:\B166ER-OpenClaw\workspace\toolbox\overlap_report.json")
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"报告写入: {out}")
    print(f"\n=== 摘要 ===")
    print(f"Vault .md 总数: {report['vault_md_total']}")
    print(f"桌面扫到的 .md: {report['desktop_md_total']}")
    print(f"**完全相同**(md5 一致): {len(report['overlaps_exact'])}")
    print(f"同名但不同内容: {len(report['overlaps_name_only'])}")
    print(f"\n各桌面目录的 .md 计数:")
    for d, info in report["by_dir"].items():
        u = len(report["desktop_unique"].get(d, []))
        print(f"  {d:<30} total={info['md_count']:4d}  unique={u:4d}")

if __name__ == "__main__":
    scan()
