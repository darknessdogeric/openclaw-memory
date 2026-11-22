#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""外部内容纳入 vault: 整台电脑相关知识库内容"""
import sys, io, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
EXTERNAL = VAULT / "50-外部接入"
EXTERNAL.mkdir(parents=True, exist_ok=True)

stats = {'anyi': 0, 'eric_obsidian': 0, 'weijing_sop': 0, 'skipped': 0}


def safe_copy_dir(src: Path, dst: Path, label: str, key: str, max_files: int = 10000):
    """安全复制整个目录"""
    if not src.exists():
        print(f"  ✗ {label}: NOT EXIST ({src})")
        return 0
    dst.mkdir(parents=True, exist_ok=True)
    count = 0
    skipped = 0
    for f in src.rglob("*"):
        if f.is_file():
            # 跳过 .obsidian 配置（避免覆盖 vault 配置）
            if '.obsidian' in f.parts:
                skipped += 1
                continue
            # 跳过太大的文件
            try:
                if f.stat().st_size > 50 * 1024 * 1024:  # 50MB
                    skipped += 1
                    continue
            except Exception:
                pass
            rel = f.relative_to(src)
            target = dst / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copy2(f, target)
                count += 1
            except Exception as e:
                print(f"    ERR {f.name}: {e}")
            if count >= max_files:
                break
    stats[key] = count
    stats['skipped'] += skipped
    print(f"  ✓ {label}: {count} 文件 (skipped {skipped})")
    return count


print("=" * 70)
print("外部内容纳入 vault (D-day 关键)")
print("=" * 70)

# 1. 安逸集团入职物料（9 个 .md + 9 个 .docx）
print("\n[1] 安逸集团_入职物料_20260707")
anyi_src = Path(r"C:\Users\ericz\Desktop\安逸集团_入职物料_20260707")
anyi_dst = EXTERNAL / "01-安逸入职物料-20260707"
safe_copy_dir(anyi_src, anyi_dst, "安逸入职物料", 'anyi', max_files=50)

# 2. Eric 自己的 Obsidian Vault
print("\n[2] Eric 自己的 Obsidian Vault")
eric_obs_src = Path(r"C:\Users\ericz\Documents\Obsidian Vault")
eric_obs_dst = EXTERNAL / "02-Eric-Obsidian-Vault"
safe_copy_dir(eric_obs_src, eric_obs_dst, "Eric Obsidian", 'eric_obsidian', max_files=200)

# 3. 维景 SOP&PP 2024（最大目录，几百个 SOP）
print("\n[3] D:\\酒店相关SOP 维景SOP&PP 2024")
weijing_src = Path(r"D:\酒店相关SOP")
weijing_dst = EXTERNAL / "03-维景SOP-PP-2024"
safe_copy_dir(weijing_src, weijing_dst, "维景SOP&PP", 'weijing_sop', max_files=5000)

# 4. 写 50-外部接入 的 README
print("\n[4] 写 50-外部接入/README")
readme = """---
author: b166er
audience: eric
status: active
type: external-import
created: 2026-07-12
---

# 🌐 50-外部接入

> 整台电脑（C:\\ + D:\\）所有可纳入 vault 的外部内容
> Eric 反馈 (2026-07-12): "整台电脑就不仅仅是 openclaw 了"

## 📂 当前内容

| 子目录 | 来源 | 价值 |
|--------|------|------|
| **01-安逸入职物料-20260707** | 桌面 | **D-day 关键**（9 文档）|
| **02-Eric-Obsidian-Vault** | Documents | Eric 自己的 Obsidian |
| **03-维景SOP-PP-2024** | D:\\酒店相关SOP | 几百个酒店 SOP |

## 🎯 重要性

- **01-安逸入职物料**: 7/13 党委会 → 7/22 入职的核心材料
  - 集团 AI 应用场景盘点
  - 安逸酒店 Agent 协议立项草案
  - AI 人才梯队建设方案
  - AI 项目投资回报测算模板
  - 1对1 班子沟通提纲
  - 产业发展部职责草案
  - 入职信息清单
  - 第一周行动计划
  - 配套表格模板
- **02-Eric-Obsidian-Vault**: Eric 之前自己用的 Obsidian vault 内容
- **03-维景SOP-PP-2024**: 维景酒店（Eric 之前工作地）完整 SOP 库
  - 安保部 P&P / SOP
  - 工程部 P&P / SOP
  - 房务部 P&P / SOP
  - 餐饮部 P&P / SOP
  - 销售部 / 人事部 / 财务部 等

## 🔗 关联

- [[../20-我们共同维护的/战略与节奏/03-安逸集团机会|D-day 应对]]
- [[../emergence/hubs/安逸集团-D-day MOC]]
- [[../emergence/INDEX|emergence 索引]]

---

*by B166ER · 2026-07-12 14:05 · 整台电脑全盘扫描结果*
"""
(EXTERNAL / "README.md").write_text(readme, encoding="utf-8")
print(f"  ✓ README.md")

# 5. 写 R24 vault 架构决策
rules_path = Path.home() / ".self-improving" / "rules.md"
r24 = """

## R24 - 1 vault + 6 分区架构 (2026-07-12)

**触发场景**: vault 架构决策
**Eric 反馈 (2026-07-12)**: "你决定，你统筹，你行动。整台电脑就不仅仅是 openclaw 了。"
**决策**: **1 个主 vault + 6 大分区**（不分裂成多个 vault 实体）

**理由**:
- 1. Eric 用 1 个 Obsidian 客户端 → 1 vault 比 4 vault 体验好
- 2. 通过文件夹颜色 + MOC 主题枢纽 = 主题隔离效果
- 3. 减少 Eric 切换成本
- 4. 跨主题双链天然支持（wikilink）
- 5. 内容规模 4758+ .md 适配 1 vault + 6 分区

**6 大分区**:
- 00-Workspace-核心/ (workspace 镜像)
- 10-我为你生成的/ (知识库主体)
- 20-我们共同维护的/ (战略/报告/项目)
- 30-你写给我的/ (反馈)
- 40-工具与模板/ (工具)
- 50-外部接入/ (整台电脑外部内容) ← 新增
- emergence/ (涌现层)

**未来扩展**:
- 如果 vault 增长到 10000+ .md，再考虑分裂为多个 vault
- 现在 1 vault 600-800 .md 性能完全 OK
- 分裂成本高（双链重写 + 跨 vault 引用）

**反对意见的回应**:
- 担心性能 → 800 .md 流畅渲染
- 担心混乱 → MOC 主题枢纽 + 分区清晰
- 担心切换 → Obsidian 内置 "工作区" 功能可一键盘切换分区
"""
if rules_path.exists():
    with open(rules_path, "a", encoding="utf-8") as f:
        f.write(r24)
    print(f"\n  ✓ R24 appended to rules.md")

# 6. 总结
print("\n" + "=" * 70)
print("外部纳入完成")
print("=" * 70)
for k, v in stats.items():
    print(f"  {k}: {v}")
total = sum(v for k, v in stats.items() if k != 'skipped')
print(f"  TOTAL 复制: {total} 文件")
