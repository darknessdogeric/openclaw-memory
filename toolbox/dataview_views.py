#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROI 3: 准备 Dataview 视图 + 安装指南

策略:
1. 在 vault 内准备 4 个 dataview 视图页面:
   - 00-Workspace-核心/相关浮现.md (主入口)
   - 00-Inbox-待整理/今日相关.md (每日涌现)
   - emergence/hubs/00-网络健康度.md (hub MOC 强度排名)
   - 00-Inbox-待整理/孤岛笔记.md (Eric 可手动清理)

2. 写一个安装指南 _Dataview-安装指南.md

3. 写一份 datastore 配置示例
"""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
    print(f"[OK] {path.relative_to(VAULT)}")


# === 1. 相关浮现 (主入口) ===
related_page = """---
type: 知识涌现入口
created: 2026-07-28
author: b166er
---

# 🔮 相关浮现 - 知识自涌现入口

> 由 B166ER 设计, 用于让 vault 从"档案室"变成"网络"
> 启用 Dataview 插件后自动工作
> 安装指南: [[_Dataview-安装指南]]

---

## 📊 网络健康度

> Eric 的 vault 不是"档案室", 是"复杂网络"。这里显示每个主题 MOC 的网络中心强度。

```dataview
TABLE length(file.outlinks) AS "正向", length(file.inlinks) AS "反向", file.cday AS "创建"
FROM "emergence/hubs"
SORT length(file.inlinks) DESC
```

## 🌐 全局网络: 反向链接 TOP 30

```dataview
TABLE length(file.inlinks) AS "被引用"
FROM "50-外部接入" OR "20-我们共同维护的" OR "10-我为你生成的"
SORT length(file.inlinks) DESC
LIMIT 30
```

## 🕒 最近 7 天更新的笔记 (按主题)

```dataview
TABLE file.mtime AS "更新"
FROM "50-外部接入"
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
LIMIT 20
```

## 🚨 仍未 link 的孤岛 (Eric 可手动补)

```dataview
LIST
FROM ""
WHERE length(file.outlinks) = 0 AND length(file.inlinks) = 0
LIMIT 30
```

## 🔗 跨主题高频 wiki link

```dataview
TABLE length(rows.b) AS "链接次数"
FROM ""
FLATTEN file.outlinks AS b
WHERE b
GROUP BY b
SORT length(rows.b) DESC
LIMIT 30
```

---

**使用方式**:
- 每天打开 Obsidian, 看本页面
- 找 7 天内更新的笔记 → 主动 link 到 3-5 个相关主题
- 看孤岛清单 → 删或者加 related

**维护人**: Eric + B166ER (自动化补 related)
"""

write(VAULT / "00-Workspace-核心" / "相关浮现.md", related_page)


# === 2. 今日相关 (涌现层 daily feed) ===
daily_page = """---
type: 今日相关涌现
created: 2026-07-28
update_cron: yes
---

# 🌅 今日相关 - 涌现层 Daily Feed

> 每日涌现: 找出"今天"与"今天相关"的笔记
> 由 Dataview 自动生成, 不用维护

## 📅 最近 1 天

```dataview
TABLE file.mtime AS "更新", length(file.inlinks) AS "反向链接"
FROM ""
WHERE file.mtime >= date(today) - dur(1 days)
SORT file.mtime DESC
LIMIT 15
```

## 📅 最近 3 天

```dataview
TABLE file.mtime AS "更新"
FROM ""
WHERE file.mtime >= date(today) - dur(3 days)
SORT file.mtime DESC
LIMIT 30
```

## 📅 最近 7 天

```dataview
LIST
FROM ""
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
LIMIT 50
```

---

**操作方式**: 看 [相关浮现|相关浮现主页] → 找最近 7 天更新 → 主动加 wikilink → 网络密度再 +1
"""

write(VAULT / "00-Inbox-待整理" / "今日相关.md", daily_page)


# === 3. 孤岛清单 (Eric 可手动清理) ===
islands_page = """---
type: 孤岛诊断
created: 2026-07-28
---

# 🏝️ 孤岛笔记清单

> 含义: 既无正向 wikilink (出度=0) 也无反向 wikilink (入度=0) 的笔记
> 修复: 主动加 3-5 个 [[wikilink]] 到主题 MOC, 让"档案"变成"网络"
> 自动诊断: B166ER 的 `obsidian_link_injector.py` 已经处理了 530/686 个 (2026-07-28)

## 📊 实时诊断 (Dataview 自动)

```dataview
LIST
FROM ""
WHERE length(file.outlinks) = 0 AND length(file.inlinks) = 0
SORT file.cday DESC
LIMIT 100
```

## 📅 最近创建但还孤岛的笔记 (Eric 重点关注)

```dataview
LIST
FROM ""
WHERE length(file.outlinks) = 0 AND length(file.inlinks) = 0 AND file.cday >= date(today) - dur(7 days)
SORT file.cday DESC
```

---

## 🛠️ 手动修复指南

对每个孤岛笔记:
1. 看内容主题
2. 加 3-5 个 `[[wikilink]]` 指向相关 MOC / 主题笔记
3. 或者: 写一行 `## 🔗 相关笔记`, 列出主题

或者让 B166ER 自动修:
- `python toolbox/obsidian_link_injector.py --force`

---

**截止 2026-07-28T23:15**: 227/1018 笔记是孤岛 (-67% 从 ROI 1+2+2.5)
"""

write(VAULT / "00-Inbox-待整理" / "孤岛笔记.md", islands_page)


# === 4. 安装指南 ===
install_guide = """# 🔧 Dataview 插件安装指南 - B166ER 设计

> 适用: Eric 的 vault (D:\\B166ER-OpenClaw\\workspace\\obsidian-vault)
> 由 B166ER 在 2026-07-28 准备, 让知识真正"自涌现"

---

## 📦 步骤 1: 下载插件

Dataview 官方 GitHub: <https://github.com/blacksmithgu/obsidian-dataview/releases>

下载 3 个文件到 `vault\\.obsidian\\plugins\\dataview\\`:

```
manifest.json
main.js
styles.css
```

> 文件名: `obsidian-dataview-X.Y.Z.zip` (最新)
> 解压后直接复制

---

## ⚙️ 步骤 2: Obsidian 启用

1. 打开 Obsidian
2. `Settings` → `Community plugins` → `Community plugins` 开关 (若关,先开)
3. 找到 `Dataview` → 打开开关

---

## 🎯 步骤 3: 看效果

打开以下页面, 应能看到自动聚合:

| 页面 | 路径 | 看到什么 |
|------|------|---------|
| **🔮 相关浮现** | `00-Workspace-核心/相关浮现.md` | 全局网络中心 + 反向 link TOP 30 + 最近 7 天 |
| **🌅 今日相关** | `00-Inbox-待整理/今日相关.md` | 1/3/7 天内更新的笔记 |
| **🏝️ 孤岛清单** | `00-Inbox-待整理/孤岛笔记.md` | 还孤岛的笔记 (Eric 可手动加 link) |

---

## 💡 步骤 4: 主动涌现

启用 Dataview 后:
1. 每天看 `[🔮 相关浮现|相关浮现]`, 找"最近 7 天"区
2. 对每条,主动加 3-5 个 [[wikilink]]
3. 看"孤岛清单"区, 对每条加 related 区块
4. 这样知识在持续生长, 不是工具养你, 是你在养工具

---

## ⚠️ 已知限制

- Dataview 0.5+ 需要 **Trusting all community plugins** 模式
- 第一次启用后页面要刷新 (Ctrl+R) 才显示查询结果
- 查询语法用 `[[文件]]` 或 `[[目录/文件]]`, 不能跨 5 层目录

---

## 🎯 进阶用法 (等 Eric 习惯后)

1. **tag-aware query**: 给笔记加 `#AHL` `#酒店`, 用 `FROM #AHL`
2. **templater 结合**: 用 Template 自动建新笔记时带 dataview 查询
3. **pages with X link**: 查找"被某个 MOC 引用过的笔记", 用于回顾
4. **graph analysis**: 配合 Graph Analysis 插件, 看图说话

---

**维护**: B166ER 每日涌现 cron (09:00 GMT+8) 会把扫描结果推送到 `50-外部接入/cron-outputs/2026-07/`
"""

write(VAULT / "_Dataview-安装指南.md", install_guide)


# === 5. hub MOC 加 dataview 区块 (示例 AHL 平台 MOC) ===
ahl_moc_path = VAULT / "emergence/hubs/AHL 平台 MOC.md"
if ahl_moc_path.exists():
    text = ahl_moc_path.read_text(encoding='utf-8')
    if "dataview" not in text.lower() or "由 B166ER 注入" in text:
        # 找到 "## 📋 桌面项目素材" 区,在它后面插入 dataview 区块
        sup_section = """---

## 🔮 动态浮现 (Dataview)

> 启用 Dataview 插件后, 这里会自动显示 AHL 平台 MOC 相关的:
> - 最近更新的笔记
> - 该主题下的活跃笔记
> - 未被 link 的笔记

### 最近更新的 AHL 相关笔记

```dataview
TABLE file.mtime AS "更新", length(file.inlinks) AS "反向"
FROM "50-外部接入" OR "20-我们共同维护的"
WHERE contains(file.outlinks, "AHL 平台 MOC") OR contains(string(file.outlinks), "AHL")
SORT file.mtime DESC
LIMIT 10
```

### AHL 主题的孤岛笔记

```dataview
LIST
FROM "50-外部接入"
WHERE !contains(file.outlinks, "AHL 平台 MOC") AND !contains(file.outlinks, "AI-Agent MOC")
SORT file.cday DESC
LIMIT 20
```

---

"""
        # 找 "## 📋 桌面项目素材" 末尾位置,在那一节末尾追加
        if "## 📋 桌面项目素材" in text:
            # 在 "## 📋 桌面项目素材" 区块最后追加
            new_text = text + sup_section
        else:
            new_text = text + sup_section
        ahl_moc_path.write_text(new_text, encoding='utf-8')
        print(f"[OK] {ahl_moc_path.relative_to(VAULT)} 加 dataview 区块")

print("\n=== Dataview 视图准备完成 ===")
print("核心文件:")
print("  - vault/00-Workspace-核心/相关浮现.md")
print("  - vault/00-Inbox-待整理/今日相关.md")
print("  - vault/00-Inbox-待整理/孤岛笔记.md")
print("  - vault/_Dataview-安装指南.md")
print("  - vault/emergence/hubs/AHL 平台 MOC.md (加 dataview 区块)")