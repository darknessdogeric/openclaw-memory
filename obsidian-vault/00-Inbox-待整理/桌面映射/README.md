---
type: 桌面映射总入口
created: 2026-07-28
author: b166er
---

# 🗂️ 桌面 → Vault 归类总图

> 整理日期: 2026-07-28
> 整理人: B166ER (授权 '你决定你行动')

## 总览

| 桌面目录 | .md | vault 目标位置 | 状态 |
|---|---:|---|---|
| `张实项目总控` | 180 | `50-外部接入/张实项目总控/` | ✅ 已入库 |
| `新媒体产品线` | 63 | `50-外部接入/新媒体产品线/` | ✅ 已入库 |
| `小红书产品线` | 1 | `50-外部接入/小红书产品线/` | ✅ 已入库 |
| `AHL源代码` | 33 | `50-外部接入/AHL源代码-docs/` | ✅ 已入库 .md, 代码不上 vault |
| `AHL专利-原始申请` | 6 | `50-外部接入/AHL专利-原始申请/` | ✅ 已入库 |
| `AHL专利-技术材料` | 10 | `50-外部接入/AHL专利-技术材料/` | ✅ 已入库 |
| `专利补正` | 10 | `50-外部接入/AHL专利-补正/` | ✅ 已入库 |
| `软著申请材料-AHL` | 4 | `50-外部接入/AHL软著申请/` | ✅ 已入库 |
| `安逸集团_入职物料_20260707` | 11 | `50-外部接入/01-安逸入职物料-20260707/` | ✅ 已入库 |
| `知局_完整版_v1.0` | 7 | `50-外部接入/知局-v1.0/` | ✅ 已入库 |
| `自我革命` | 1 | `50-外部接入/自我革命/` | ✅ 已入库 .md, PDF 建索引 |
| `AHL-BP-2026` | 0 | `50-外部接入/AHL-BP-2026/` | ✅ 索引 |
| `工作文档` | 0 | `50-外部接入/工作文档-桌面映射/` | ✅ 索引 |
| `项目资料` | 0 | `50-外部接入/项目资料-桌面映射/` | ✅ 索引 |
| `劳动合同` | 0 | `—` | 🔒 不入 vault (个人隐私) |
| `小白的保单` | 0 | `—` | 🔒 不入 vault (个人事务) |
| `简历及应聘文件` | 0 | `—` | 🔒 不入 vault (个人敏感) |
| `图片` | 0 | `—` | 🔒 不入 vault (个人证件) |
| `快捷方式` | 0 | `—` | ⚠️ 不动 (.lnk) |
| `GAME` | 0 | `—` | ⚠️ 不动 (无关) |

## 关键数字

| 维度 | 数据 |
|---|---:|
| 扫到的桌面 .md | 326 |
| 入 vault 的 .md | 326 |
| 仅做索引 (大文件) | 7 个目录 |
| 不入 vault (隐私/快捷) | 4 个目录 |

## 规则

- **不删除桌面原文件** (应对 7/12 误删事故 R13/R14)
- **只复制** `.md` 到 vault,二进制文件保留桌面
- **同名文件**比较 md5: 相同跳过;不同重命名为 `(source-desktop)` 后缀
- **大文件** (PDF/PNG/DOCX) 不复制,在 vault 建索引指向原路径
- **隐私文件** (合同/证件/保单) 不入 vault

## 怎么用

1. 找资料 → 先查本 README 找到 vault 目标位置
2. 看 vault 笔记 → 直接打开 vault 对应目录的 .md
3. 看原始素材 → 看对应 `_原始素材索引.md`,点链接回桌面
4. 维护规范 → 后续新增桌面 .md, 走 `obsidian_copy.py` 工具批量复制

## 工具

- `D:\B166ER-OpenClaw\workspace\toolbox\obsidian_classify.py` - 桌面分类扫描
- `D:\B166ER-OpenClaw\workspace\toolbox\obsidian_step1_overlap.py` - 重叠检测
- `D:\B166ER-OpenClaw\workspace\toolbox\obsidian_copy_phase1.py` - Phase1 复制
- `D:\B166ER-OpenClaw\workspace\toolbox\obsidian_copy_phase2.py` - Phase2 复制
- `D:\B166ER-OpenClaw\workspace\toolbox\obsidian_index_phase3.py` - Phase3 索引
- `D:\B166ER-OpenClaw\workspace\toolbox\obsidian_map_readme.py` - 本 README