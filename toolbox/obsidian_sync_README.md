# obsidian_sync.py — 工具说明

> **目的**: 把"桌面→Vault 统一归纳"沉淀为 1 个 CLI, Eric 一句话就能复用
> **作者**: B166ER
> **创建**: 2026-07-28
> **触发**: Eric 22:22 "你决定你行动"

---

## 命令

```bash
python toolbox/obsidian_sync.py scan        # 摸底, 生成 overlap_report.json
python toolbox/obsidian_sync.py sync        # 主入口: 复制 .md + 建索引
python toolbox/obsidian_sync.py archive     # 归档空 vault (幂等)
python toolbox/obsidian_sync.py health      # vault 健康检查
python toolbox/obsidian_sync.py rebuild     # 重建 vault_index
```

---

## 默认行为 (sync)

| 操作 | 行为 |
|------|------|
| 复制 .md 到 vault | `shutil.copy2` 保留 mtime |
| 同名异版 | 重命名为 `(source-desktop)` 后缀 |
| 完全相同 (md5) | 跳过, 不重写 |
| 二进制 (PDF/PNG/DOCX) | 不复制, 仅在 `_原始素材索引.md` 标出 |
| 桌面原文件 | **不删** (R13/R14 教训) |
| 隐私目录 (合同/证件/保单) | 跳过, 不入 vault |
| 快捷方式 (.lnk) | 跳过 |

---

## DIRECTORY_MAP (硬编码归类决策)

| 桌面目录 | vault 目标 | 说明 |
|----------|-----------|------|
| 张实项目总控 | 50-外部接入/张实项目总控 | 180 .md, 11 子目录 |
| 新媒体产品线 | 50-外部接入/新媒体产品线 | 63 .md, 8 子目录 |
| 小红书产品线 | 50-外部接入/小红书产品线 | 1 .md |
| AHL源代码 | 50-外部接入/AHL源代码-docs | 33 .md (代码不动) |
| AHL专利申请文件 | 50-外部接入/AHL专利-技术材料 | 10 .md |
| 专利 | 50-外部接入/AHL专利-原始申请 | 6 .md |
| 专利补正 | 50-外部接入/AHL专利-补正 | 10 .md |
| 软著申请材料-AHL | 50-外部接入/AHL软著申请 | 4 .md |
| 安逸集团_入职物料_20260707 | 50-外部接入/01-安逸入职物料-20260707 | 11 .md |
| 知局_完整版_v1.0 | 50-外部接入/知局-v1.0 | 7 .md |
| 自我革命 | 50-外部接入/自我革命 | 1 .md |

**INDEX_ONLY** (仅建索引不复制 .md):
- AHL-BP-2026, 工作文档, 项目资料

**SKIP** (隐私/快捷/无关):
- 劳动合同, 小白的保单, 简历及应聘文件, 图片, 快捷方式, GAME

---

## 怎么扩展

Eric 桌面新增一个文件夹? 修改 `DIRECTORY_MAP` 加一行即可。
桌面新增一类隐私文件夹? 加到 `SKIP_DIRS`。

---

## 安全约束 (R13/R14)

- 全程 **不删** 桌面任何文件
- 用 **Python** 而非 PowerShell (避免 7/12 编码坑)
- 同名异版 **保留桌面版** (加 `(source-desktop)` 后缀), vault 用更新版
- 每次执行前 **先 scan**, 让 Eric 看到重叠报告再决定 sync

---

## 验证 (2026-07-28 实测)

```
Scan  : Vault=1018 / Desktop=326 / 完全相同=317 / 同名异版=9
Sync  : copied=9 (安逸集团同名异版), renamed=9, 其余全 skipped
Health: 99.3% 索引覆盖
```

Idempotent ✅ — 重复执行 vault 数量稳定。