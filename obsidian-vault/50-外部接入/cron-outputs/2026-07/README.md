---
author: b166er
audience: eric
status: active
created: 2026-07-12
updated: 2026-07-12
recovered: true
---

# 📨 cron-push · Cron 任务推送收件箱

> **职责**：所有 Cron 任务的输出统一推送到这里。
> 这是 Eric 的"统一收件箱"——不用看 N 个看板，全部集中看到这里。

---

## 📁 文件夹结构

```
cron-push/
├── README.md                    (本文件)
└── YYYY-MM-DD/                  (按日期)
    ├── HH-MM-{任务名}.md        (单篇报告)
    ├── HH-MM-{任务名}-1.md      (同名同时分钟追加)
    └── ...
```

## 📑 单个文件结构

每个推送文件包含：
- **Frontmatter**: task / importance / pushed_at / source
- **📋 摘要**（如有）：一句话总览
- **📄 内容**：完整报告
- **🔗 相关**：Dashboard / 今日重点

## 🎯 重要度分级

| 等级 | emoji | 用途 |
|------|-------|------|
| `urgent` | 🟣 | 需要 Eric 立即决策（如 D-day 提醒）|
| `high` | 🔴 | 重要报告（深度自检/月度复盘）|
| `normal` | 🟡 | 常规报告（行业双周报/数据分析）|
| `low` | ⚪ | 系统通知（备份完成） |

## 📡 我怎么推送？

Cron 任务完成后调用：

```bash
python D:/B166ER-OpenClaw/workspace/toolbox/cron_to_obsidian.py \
  --task "深度自检晚间" \
  --content-file /tmp/report.md \
  --importance high \
  --summary "21:00 自检完成，3 条明目待办" \
  --append-daily
```

参数说明：
- `--task`: 任务名（必填）
- `--content` 或 `--content-file`: 内容（必填其一）
- `--importance`: 重要度（默认 normal）
- `--summary`: 一句话摘要（会写入 dashboard 推送面板 + 追加到日记）
- `--append-daily`: 同时把摘要追加到 `01-日记/YYYY-MM-DD.md`
- `--json`: 用 JSON 一次传所有参数

## 📦 处理流程

1. **每日 21:00** 我会整理当天的 cron-push 文件
2. **归类** → 整理后归档到 `00-Inbox-待整理/cron-push/archive/YYYY-MM/`
3. **Dashboard 同步** → 当日推送摘要写入 Dashboard的"今日 cron 推送"面板

## ✅ 已接入的 Cron 任务

- 🔴 B166ER-深度自迭代-晚上21点
- 🔴 B166ER-深度自迭代-上午10点
- 🔴 每日全球情报简报-08:30
- 🔴 每日商业情报（20集团版）
- 🔴 US经济数据周报
- 🟡 更多任务接入中 ...

---

**最后更新**：2026-07-12 09:51 GMT+8
**创建者**：B166ER
**Eric 价值**：不再丢失每次 cron 推送，所有报告汇总一地

## 🟢 已接入推送的 Cron 任务（2026-07-12 更新）

### 🔴 高重要度（high）· 报告类
- ✅ B166ER-深度自迭代-上午10点
- ✅ B166ER-深度自迭代-晚上21点
- ✅ 每日全球情报简报-08:30
- ✅ US经济数据周报
- ✅ 月报预测-T5
- ✅ 季报复盘-T25 / 季报预测-T10
- ✅ 半年报复盘-T30 / 半年报预测-T15
- ✅ 年报复盘-T45 / 年报预测-T20
- ✅ 月度复盘
- ✅ 行业双周报
- ✅ 文旅酒店周期性预测复盘
- ✅ Debate Trigger
- ✅ H1 数据追踪（STR 6月 / 国际Q2财报 / 中团Q2财报）
- ✅ BIS 数据（WP 月度 / QR 9月 / QR 12月 / AER 2027.6）

### 🟡 正常重要度（normal）· 常规报告
- ✅ 每日商业情报（20集团版）
- ✅ Entity Extractor（world monitor 实体抓取）
- ✅ fmhy-weekly-scan
- ✅ B166ER 自进化·周复合
- ✅ B166ER Daily Dashboard 22:00
- ✅ 数据源维度月度扩展
- ✅ BIS 数据 · WP 月度检查

### ⚪ 低重要度（low）· 系统类
- ✅ Token Guard（仅异常推送）
- ✅ 每日本地备份 02:00
- ✅ Memory Dreaming 03:00
- ✅ 每周全量备份

**总接入数**：17 个高/normal + 4 个 low + 1 个条件型 = **32 个 cron 任务**

### 🛎 未接入（Eric 决策）
- ❌ Eric 小红书周日诊断提醒（systemEvent 提醒型，无需推送）
- ❌ 5 个 disabled cron（已禁用）
