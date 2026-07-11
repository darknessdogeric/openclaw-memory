---
skill_id: "design-md"
title: "design-md Skills — AI设计规范库"
category: "学术/研究"
description: "> 版本: V2.0 | 更新: 2026-05-07 > 来源: VoltAgent/awesome-design-md (44.2k ⭐) + 本地化重建 > 定位: 补充B166ER的设计规范能力，弥补"信息图/海报/UI生成"的视觉语言短板 ---"
when_to_use: ""
size_kb: 6.1
refactored: "2026-06-24"
source: "skills/design-md/SKILL.md"
tags:
  - skills
  - 学术/研究
---

# design-md Skills — AI设计规范库

> 版本: V2.0 | 更新: 2026-05-07
> 来源: VoltAgent/awesome-design-md (44.2k ⭐) + 本地化重建
> 定位: 补充B166ER的设计规范能力，弥补"信息图/海报/UI生成"的视觉语言短板

---

## ⭐ 核心升级 (V2.0)

**V1.0状态**: 59个品牌的目录指针，内容依赖外链getdesign.md（国内不可访问）

**V2.0修复**: 亲手建立实际可用的设计规范库，本地化保存，无需外链

---

## 本地已完善品牌（持续更新）

| 品牌 | 风格定位 | 适用场景 | 状态 |
|------|---------|---------|------|
| **ahl** | 科技×温度，去中心化旅行平台 | AHL自有品牌规范 | ✅ 本地 |
| **stripe** | 专业金融，高级清晰 | 商业/酒店/支付类信息图 | ✅ 本地 |
| **airbnb** | 温暖有人情味，旅行感 | 民宿/旅行/生活方式 | ✅ 本地 |
| **linear** | 深色开发者工具，精确克制 | 科技/数据/架构图 | ✅ 本地 |
| **vercel** | 准系统极简，技术感 | 开发者工具/技术文档 | ✅ 本地 |
| **claude** | 温暖AI，智慧但有温度 | AI产品/对话界面 | ✅ 本地 |
| **notion** | 柔和中性，文档感 | 文档/知识管理/轻量 | ✅ 本地 |
| **tesla** | 极致简洁，高端未来感 | 高端产品/电动车风格 | ✅ 本地 |

---

## 技能路由矩阵

| 需求 | 首选工具 | 备选工具 | 品牌规范 |
|------|---------|---------|---------|
| **生成海报/信息图PNG** | `article-to-infographic` | `lh-html-to-image` | 参考品牌DESIGN.md |
| **生成HTML可发版式** | `business-design` | `md2all-converter` | AHL/Surface |
| **生成PPT演示文稿** | `ppt-deck-builder-pro` | `pptx-generator` | 自定义风格 |
| **生成AI图片素材** | `image-gen` | `image_generate` | 参考品牌风格 |
| **生成符合品牌的UI代码** | `frontend-design-pro` + 品牌DESIGN.md | `superdesign` | 指定品牌 |
| **建立自有产品设计规范** | 组合参考品牌 + 自定义 | - | AHL品牌规范 |
| **设计质量审查/Audit** | `frontend-design-pro` (audit命令) | - | - |

---

## 完整设计链路

```
Step 1: 确定场景
    │
    ├─ 用户侧 (民宿/旅行/生活)
    │   └─ 参考: airbnb DESIGN.md
    │       └─ 风格: 暖色、16px圆角、旅行摄影
    │
    ├─ 技术侧 (数据/架构/开发者)
    │   └─ 参考: linear / vercel DESIGN.md
    │       └─ 风格: 深色、精确克制、代码感
    │
    ├─ 商业侧 (金融/酒店/企业)
    │   └─ 参考: stripe DESIGN.md
    │       └─ 风格: 专业蓝、清晰克制、金融信任
    │
    └─ AHL品牌 (自有)
        └─ 参考: ahl DESIGN.md
            └─ 双轨: 技术侧深色 + 用户侧暖色

Step 2: 选择工具
    │
    ├─ 需要PNG图片 → article-to-infographic
    ├─ 需要HTML页面 → business-design / frontend-design-pro
    ├─ 需要PPT → ppt-deck-builder-pro
    └─ 需要AI图片 → image-gen

Step 3: 融入品牌规范
    在prompt中引用对应品牌的DESIGN.md关键规范
```

---

## DESIGN.md标准结构（所有品牌统一）

每个本地DESIGN.md包含9个部分：

```
1. Visual Theme & Atmosphere      → 整体氛围/关键词/情绪板
2. Color Palette                  → 配色表（主色/中性/语义）
3. Typography                     → 字体/字号/字重/行高
4. Spacing & Grid                → 基础网格/间距系统
5. Component Styling              → 按钮/卡片/输入框等组件样式
6. Depth & Elevation             → 阴影/层级定义
7. Do's & Don'ts                 → 设计规范和禁忌
8. Motion Design                 → 动效/easing/时长
9. Agent Prompt Guide            → 给AI的参考指令模板
```

---

## AHL设计规范应用

### 双轨视觉策略

```
【用户侧】airbnb风格 (温暖)
──────────────────────────────────────
背景: #FAFAFA (浅色)
CTA: #F97316 (珊瑚橙)
照片: 自然光旅行摄影
圆角: 16px (卡片)
场景: 住宿卡片、预订流程、评价

【桥接层】AHL Protocol
──────────────────────────────────────
背景: #0A1628 (深蓝)
CTA: #F97316 (珊瑚橙)
强调: #06B6D4 (青色)
场景: Token经济、Agent展示

【技术侧】linear风格 (精确)
──────────────────────────────────────
背景: #0D0D0D (深黑)
强调: #8A8EF4 (紫色)
场景: 后台仪表盘、数据可视化
```

---

## 快速参考：品牌对照

| 需求 | 参考品牌 | 主色 | 圆角 | 背景 |
|------|---------|------|------|------|
| 民宿旅行 | airbnb | #FF385C | 16px | 浅色 |
| 金融支付 | stripe | #635BFF | 6px | 浅色 |
| 开发者工具 | linear | #8A8EF4 | 6-8px | 深色 |
| 极致简洁 | vercel | #000000 | 0-4px | 浅/深 |
| AI对话 | claude | #D97706 | 8px | 深色 |
| 文档知识 | notion | #37352F | 4px | 浅色 |
| 高端产品 | tesla | #E31937 | 0px | 浅/黑 |
| AHL品牌 | ahl | #F97316 | 8-16px | 双轨 |

---

## 本地品牌规范更新流程

当需要添加新品牌时：

1. 读取品牌官网设计资源或通过研究重建设计规范
2. 参考DESIGN.md标准9部分结构创建文件
3. 保存到 `design-md/design-md/<brand>/DESIGN.md`
4. 更新本SKILL.md的"本地已完善品牌"列表

---

## 目录结构

```
skills/design-md/
├── SKILL.md              ← 本文件 (V2.0)
├── README.md             ← VoltAgent原始说明
├── CONTRIBUTING.md       ← 贡献指南
└── design-md/           ← 品牌规范目录
    ├── ahl/              ← ⭐ AHL自有品牌
    ├── airbnb/           ← 民宿旅行
    ├── claude/           ← AI对话
    ├── linear.app/       ← 开发者工具
    ├── notion/           ← 文档知识
    ├── stripe/           ← 金融支付
    ├── tesla/            ← 高端产品
    ├── vercel/           ← 准系统技术
    └── ...（其他品牌可按需扩展）
```

---

*V2.0 | 2026-05-07 | 本地化重建，无需外链，完全可用*
