---
name: design-studio
description: >-
  建筑设计/室内设计/平面设计概念图与渲染图生成。覆盖建筑外观、室内空间、平面图、
  立面图、三视图、户型图、Logo/VI、海报、Mood Board、设计简报。参数驱动，输入
  项目类型+风格+规模即可生成全套前期设计文件。触发词：建筑设计、室内设计、平面设计、
  平面图、立面图、三视图、户型图、效果图、概念图、渲染图、酒店设计、民宿设计、
  设计简报、mood board、情绪板、品牌VI、logo设计。
---

# Design Studio — 建筑设计/室内设计/平面设计

项目前期概念图+渲染图阶段。参数驱动，一键生成全套设计文件。

## 核心能力

| 输出类型 | 格式 | 引擎 |
|---------|------|------|
| 建筑外观渲染 | PNG 16:9 | Minimax image-01 |
| 室内空间渲染 | PNG 16:9 | Minimax image-01 |
| **平面图 (Floor Plan)** | PNG 1:1 | Minimax + 在线工具 |
| **立面图 (Elevation)** | PNG 9:16 | Minimax |
| **三视图 (Orthographic)** | PNG set | Minimax ×3 |
| 设计简报 | MD → PDF | engine.py |
| Mood Board | HTML → PNG | engine.py |
| Logo/VI | PNG 1:1 | Minimax |
| 户型需求文档 | MD | engine.py |

## 参数驱动工作流

用户提供参数，系统自动生成全套输出：

```
项目类型: 酒店/民宿/医养/度假村/办公楼/住宅
风格: 现代/新中式/侘寂/工业/北欧/奢华/生物亲和
规模: 房间数+面积
地点: 城市+地理特征
```

### 工作流

1. 接收参数 → 2. 加载对应提示词库 → 3. 并行生成多张概念图 → 4. 生成设计简报 → 5. 生成Mood Board → 6. 输出汇总

## 提示词库

完整专业提示词库（按需加载）：
- `references/architecture-prompts.md` — 建筑外观 60+条
- `references/interior-prompts.md` — 室内空间 40+条
- `references/floorplan-prompts.md` — 平面图/立面图/三视图 30+条
- `references/graphic-prompts.md` — 平面设计/VI 20+条

## 快速调用

```bash
# 完整项目包
python design-studio/engine.py full "医养酒店" 大理 "150间" --style 生物亲和

# 单项
python design-studio/engine.py architecture "精品酒店" --style 新中式 --mood 黄昏
python design-studio/engine.py interior "酒店大堂" --style 奢华
python design-studio/engine.py floorplan "主卧,次卧,客厅,厨房" 120 现代
python design-studio/engine.py brief "医养酒店" 大理 "150间"
python design-studio/engine.py moodboard "项目名称"
```

## 平面图生成

两种方式：
1. **AI渲染**: 用 Minimax + 平面图专用提示词直接生成概念平面图
2. **在线工具**: 生成参数化需求文档 → 用户复制到 Homestyler/Planner5D 获取精确户型

平面图提示词模式：
```
architectural floor plan, top-down view, [N] bedrooms, [N] bathrooms,
open-plan living and kitchen, total area [X] sqm, [style] design,
clean professional architectural drawing style, dimensioned,
white background with black linework, 1:100 scale appearance
```

## 立面图生成

```
architectural elevation drawing, [direction] elevation,
[building description], [style] architecture,
orthographic projection, professional architectural drafting style,
white background, precise linework with material annotations,
human scale figure for reference
```

## 三视图生成

依次生成 Front/Side/Top 三张：
1. 正立面 (Front Elevation): 主入口视角
2. 侧立面 (Side Elevation): 剖面关系
3. 俯视图 (Top/Plan View): 屋顶+总平关系

## 输出文件

所有输出保存在 `design-studio/output/`：
- `render_*.png` — 概念渲染图
- `brief_*.md` — 设计简报
- `moodboard_*.html` — 情绪板
- `floorplan_*.md` — 户型需求
- `project_*.md` — 项目汇总
