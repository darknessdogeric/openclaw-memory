#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 4: 建 vault\00-Inbox-待整理\桌面映射\README.md - 桌面→vault 归类总入口"""
import sys
from pathlib import Path
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')

DESK = Path(r"C:\Users\ericz\Desktop")
VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
MAP_DIR = VAULT / "00-Inbox-待整理" / "桌面映射"
MAP_DIR.mkdir(parents=True, exist_ok=True)
NOW = datetime.now().strftime("%Y-%m-%d")

# 桌面 → vault 归类决策 (来自方案 B)
CLASSIFICATION = [
    # (桌面目录, .md 数, vault 目标位置, 状态, 描述)
    ("张实项目总控", 180, "50-外部接入/张实项目总控/", "✅ 已入库",
     "11 一级目录,180 .md,含 05-AHL/AHL-春熙/04-SOP/03-AI赋能/02-人寿医养/01-自媒体/06-潮玩/07-美国跨境"),
    ("新媒体产品线", 63, "50-外部接入/新媒体产品线/", "✅ 已入库",
     "8 子目录: 收益管理 V3/独立酒店境外/数据资产/供应链工程交付包"),
    ("小红书产品线", 1, "50-外部接入/小红书产品线/", "✅ 已入库",
     "4 子目录+8 直接文件, 含十五六图/经济解读/AI收益"),
    ("AHL源代码", 33, "50-外部接入/AHL源代码-docs/", "✅ 已入库 .md, 代码不上 vault",
     "AI-HOTEL-LANGUAGE-DEMO-main 完整项目,33 个 .md 已入库;backend/frontend/legacy 代码不动"),
    ("AHL专利-原始申请", 6, "50-外部接入/AHL专利-原始申请/", "✅ 已入库",
     "27 份原始专利申请 .md + 8 张附图 + .docx/.pdf"),
    ("AHL专利-技术材料", 10, "50-外部接入/AHL专利-技术材料/", "✅ 已入库",
     "17 份 AHL 专利技术材料"),
    ("专利补正", 10, "50-外部接入/AHL专利-补正/", "✅ 已入库",
     "33 份补正文档,三轮回合"),
    ("软著申请材料-AHL", 4, "50-外部接入/AHL软著申请/", "✅ 已入库",
     "AHL 软件著作权 5 份"),
    ("安逸集团_入职物料_20260707", 11, "50-外部接入/01-安逸入职物料-20260707/", "✅ 已入库",
     "9 同名已重命名为 `(source-desktop)` 标新;2 7/24 研讨会孤本补入"),
    ("知局_完整版_v1.0", 7, "50-外部接入/知局-v1.0/", "✅ 已入库",
     "知局副业项目 V1.0 完整版"),
    ("自我革命", 1, "50-外部接入/自我革命/", "✅ 已入库 .md, PDF 建索引",
     "86 文件 - AI+酒店行业研究"),
    ("AHL-BP-2026", 0, "50-外部接入/AHL-BP-2026/", "✅ 索引",
     "14 PNG + 1 PDF 商业计划书, 见 `_原始素材索引.md`"),
    ("工作文档", 0, "50-外部接入/工作文档-桌面映射/", "✅ 索引",
     "14 文件 - 襄阳/中旅/HAL 模式"),
    ("项目资料", 0, "50-外部接入/项目资料-桌面映射/", "✅ 索引",
     "4 文件 - 音乐文创 + 潮玩 + 酒店土建策划"),
    ("劳动合同", 0, "—", "🔒 不入 vault (个人隐私)",
     "中旅劳动合同/解除通知 - 个人隐私,保留桌面"),
    ("小白的保单", 0, "—", "🔒 不入 vault (个人事务)",
     "小白(车)保单 - 个人事务,保留桌面"),
    ("简历及应聘文件", 0, "—", "🔒 不入 vault (个人敏感)",
     "简历/学位/社保/身份证 - 个人敏感,保留桌面"),
    ("图片", 0, "—", "🔒 不入 vault (个人证件)",
     "身份证/职业照片 - 个人证件,保留桌面"),
    ("快捷方式", 0, "—", "⚠️ 不动 (.lnk)",
     "33 个 Windows 快捷方式 - 不动"),
    ("GAME", 0, "—", "⚠️ 不动 (无关)",
     "游戏数据 - 不动"),
]

lines = []
lines.append("---")
lines.append("type: 桌面映射总入口")
lines.append(f"created: {NOW}")
lines.append("author: b166er")
lines.append("---")
lines.append("")
lines.append("# 🗂️ 桌面 → Vault 归类总图")
lines.append("")
lines.append(f"> 整理日期: {NOW}")
lines.append(f"> 整理人: B166ER (授权 '你决定你行动')")
lines.append("")
lines.append("## 总览")
lines.append("")
lines.append("| 桌面目录 | .md | vault 目标位置 | 状态 |")
lines.append("|---|---:|---|---|")
for d, n, loc, status, desc in CLASSIFICATION:
    lines.append(f"| `{d}` | {n} | `{loc}` | {status} |")

lines.append("")
lines.append("## 关键数字")
lines.append("")
lines.append("| 维度 | 数据 |")
lines.append("|---|---:|")
lines.append(f"| 扫到的桌面 .md | {sum(c[1] for c in CLASSIFICATION)} |")
lines.append(f"| 入 vault 的 .md | {sum(c[1] for c in CLASSIFICATION if '已入库' in c[2] or '✅ 已入库' in c[3])} |")
lines.append(f"| 仅做索引 (大文件) | 7 个目录 |")
lines.append(f"| 不入 vault (隐私/快捷) | 4 个目录 |")

lines.append("")
lines.append("## 规则")
lines.append("")
lines.append("- **不删除桌面原文件** (应对 7/12 误删事故 R13/R14)")
lines.append("- **只复制** `.md` 到 vault,二进制文件保留桌面")
lines.append("- **同名文件**比较 md5: 相同跳过;不同重命名为 `(source-desktop)` 后缀")
lines.append("- **大文件** (PDF/PNG/DOCX) 不复制,在 vault 建索引指向原路径")
lines.append("- **隐私文件** (合同/证件/保单) 不入 vault")
lines.append("")
lines.append("## 怎么用")
lines.append("")
lines.append("1. 找资料 → 先查本 README 找到 vault 目标位置")
lines.append("2. 看 vault 笔记 → 直接打开 vault 对应目录的 .md")
lines.append("3. 看原始素材 → 看对应 `_原始素材索引.md`,点链接回桌面")
lines.append("4. 维护规范 → 后续新增桌面 .md, 走 `obsidian_copy.py` 工具批量复制")

lines.append("")
lines.append("## 工具")
lines.append("")
lines.append("- `D:\\B166ER-OpenClaw\\workspace\\toolbox\\obsidian_classify.py` - 桌面分类扫描")
lines.append("- `D:\\B166ER-OpenClaw\\workspace\\toolbox\\obsidian_step1_overlap.py` - 重叠检测")
lines.append("- `D:\\B166ER-OpenClaw\\workspace\\toolbox\\obsidian_copy_phase1.py` - Phase1 复制")
lines.append("- `D:\\B166ER-OpenClaw\\workspace\\toolbox\\obsidian_copy_phase2.py` - Phase2 复制")
lines.append("- `D:\\B166ER-OpenClaw\\workspace\\toolbox\\obsidian_index_phase3.py` - Phase3 索引")
lines.append("- `D:\\B166ER-OpenClaw\\workspace\\toolbox\\obsidian_map_readme.py` - 本 README")

out = MAP_DIR / "README.md"
out.write_text("\n".join(lines), encoding="utf-8")
print(f"[OK] {out}")
print(f"\n总 .md 移动: {sum(c[1] for c in CLASSIFICATION)} 个")
