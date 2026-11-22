# 🔧 Dataview 插件安装指南 - B166ER 设计

> 适用: Eric 的 vault (D:\B166ER-OpenClaw\workspace\obsidian-vault)
> 由 B166ER 在 2026-07-28 准备, 让知识真正"自涌现"

---

## 📦 步骤 1: 下载插件

Dataview 官方 GitHub: <https://github.com/blacksmithgu/obsidian-dataview/releases>

下载 3 个文件到 `vault\.obsidian\plugins\dataview\`:

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
