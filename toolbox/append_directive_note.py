"""Append concept update note to hotel-sources-directive.md"""
from pathlib import Path

note = """


---

# ⚠️ 概念更新（2026-08-02 Eric 纠正）

本文档的"28 信源"概念已**过时**。

## 真实信源矩阵（2026-08-02 盘点）

| 子系统 | 来源 | 数量 |
|---|---|---|
| 酒店行业 28 信源 | `toolbox/hotel_sources.py` | 28（核心子集） |
| TrendRadar RSS | `trendradar/config/config.yaml` | 40 配置 / **31 启用** |
| TrendRadar 平台热搜 | 同上 | **11 平台** |
| 趋势关键词库 | `trendradar/config/frequency_words.txt` | **~1355 关键词** |
| **合计主动信源** | | **~103 个** |

**Eric 估的 68-81 ≈ 实际 103**（扩展后含国际 + 平台 + 关键词四维）。

## 4 大覆盖领域（frequency_words.txt 标注）

1. **酒店/旅游**：国内 + 国外关键词全覆盖
2. **宏观/金融**：Fed / ECB / FOMC / Treasury / 货币 / 大宗商品
3. **AI/科技**：AGI / Foundation Model / 芯片 / 政策 / 估值 / 投资
4. **地缘/世界局势**：大国博弈 / 半导体 / 能源 / 货币 / 制裁 / 区域冲突

## 行动

- 详见 `memory/2026-08-02-source-matrix-expansion.md`
- 已更新 `toolbox/hotel_sources.py` line 36（标注"广义矩阵子集"）
- 本文档保留为"v6 海报基线"，新矩阵以 2026-08-02 文件为准
"""

target = Path(r'D:\B166ER-OpenClaw\workspace\memory\2026-07-21-hotel-sources-directive.md')
existing = target.read_text(encoding='utf-8')
target.write_text(existing + note, encoding='utf-8')
print(f'OK: appended {len(note)} chars to {target.name}')