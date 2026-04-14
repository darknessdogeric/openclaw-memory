# design-md Skills — AI设计规范库

> 版本: V1.0
> 创建: 2026-04-14
> 来源: VoltAgent/awesome-design-md (44.2k ⭐)
> 定位: 补充B166ER的设计规范能力，弥补"信息图/海报/UI生成"的视觉语言短板

---

## 核心定位

**voltagent/awesome-design-md** 是一个设计规范库，把50+个知名产品的视觉系统提取成DESIGN.md文件。

**这个skill的价值：**
- 设计规范 → 不是生成图片，是给AI编码agent看的"视觉语言说明书"
- 让AI生成的UI/HTML符合某个品牌的视觉规范
- 配合article-to-infographic使用：后者生成图片，前者生成代码级规范

---

## 技能路由

| 需求 | 工具 |
|------|------|
| 生成海报/信息图PNG | `article-to-infographic` skill |
| 生成符合品牌规范的HTML/UI代码 | `design-md` skill |
| 生成完整的产品页面 | `design-md` + `article-to-infographic` 组合 |
| 建立自有产品的设计规范 | 提取参考品牌规范 → 定制DESIGN.md |

---

## 使用方法

### Step 1: 确定要参考的品牌设计规范

已收录的59个品牌（按类别）：

**AI/LLM平台**
Claude / Cohere / ElevenLabs / Minimax / Mistral AI / Ollama / OpenCode AI / Replicate / RunwayML / Together AI / VoltAgent / xAI

**开发者工具/IDE**
Cursor / Expo / Linear.app / Lovable / Raycast / Superhuman / Vercel / Warp / Zapier

**后端/数据库/DevOps**
Cal.com / ClickHouse / HashiCorp / IBM / MongoDB / Neon / PlanetScale / Sentry

**金融/支付**
Coinbase / Revolut / Stripe / Wise

**电商/零售**
Airbnb / Figma / Pinterest / Sanity / Webflow

**汽车/硬件**
BMW / Ferrari / Lamborghini / NVIDIA / Renault / Tesla / Uber

**创意/媒体**
Apple / Framer / Intercom / Miro / Notion / Spotify

**设计工具**
Clay / Figma / Framer / Loom / Mintlify / Semrush

### Step 2: 获取DESIGN.md

通过 `https://getdesign.md/<brand>/design-md` 获取对应品牌的DESIGN.md规范文件。

例如：
```
https://getdesign.md/stripe/design-md
https://getdesign.md/vercel/design-md
https://getdesign.md/airbnb/design-md
https://getdesign.md/minimax/design-md
```

### Step 3: 将DESIGN.md融入创作流程

**方式A：作为article-to-infographic的参考**
在prompt中引用DESIGN.md的核心规范：
```
参考Stripe的DESIGN.md规范：
- 配色：Deep blue #635BFF + soft gray
- 字体：System UI, large headings
- 组件：Buttons with subtle shadows, card-style inputs
- 间距：8px base grid

基于以上规范，为AHL生成一张手机海报...
```

**方式B：直接生成HTML代码**
将DESIGN.md内容作为system prompt的一部分，让AI直接生成符合该规范的HTML/CSS代码。

**方式C：创建自定义设计规范**
读取多个品牌的DESIGN.md → 提取共同的设计模式 → 根据需求组合 → 创建AHL自有DESIGN.md

---

## DESIGN.md的标准结构（VoltAgent规范）

每个DESIGN.md包含9个部分：

```
1. Visual Theme & Atmosphere
   - 整体氛围描述（如"cool-toned, high-contrast, minimal geeky"）

2. Color Palette & Roles
   - 配色及语义化名称
   - 例如: background-primary / accent-color-hover

3. Typography Rules
   - 字体/字号/字重/行高/字间距

4. Spacing & Layout
   - 基础网格（4px或8px）
   - 间距token
   - 容器宽度/断点

5. Component Stylings
   - 基础组件样式和交互状态
   - Buttons / Cards / Inputs / Navigation等

6. Depth & Elevation
   - 阴影定义和层级

7. Do's & Don'ts
   - 设计规范和禁忌

8. Responsive Behavior
   - 断点和自适应规则

9. Agent Prompt Guide
   - 给AI coding agent的示例prompt
```

---

## 核心使用场景

### 场景1：AHL需要生成某个酒店集团的界面
1. 确定目标品牌（如：Accor/IHG/万豪）
2. 获取其DESIGN.md（如有）
3. 用article-to-infographic生成符合该品牌视觉的海报
4. 如需HTML代码，直接将DESIGN.md规范作为prompt一部分

### 场景2：建立AHL自有设计规范
1. 选择最接近目标的参考品牌（推荐：Stripe / Linear / Vercel）
2. 读取其DESIGN.md全部内容
3. 结合AHL品牌特征（科技感/旅行/中文）调整
4. 输出AHL自有DESIGN.md文件

### 场景3：竞品分析时快速了解对手视觉语言
1. 获取竞品对应品牌的DESIGN.md
2. 分析其色彩/字体/布局/组件选择
3. 用于竞争策略分析

### 场景4：为Eric的创作提供视觉参考
当Eric要求"做成像XXX那样的风格"时：
1. 查找该品牌的DESIGN.md
2. 在创作prompt中引用关键规范
3. article-to-infographic据此生成匹配风格的作品

---

## 目录结构

```
skills/design-md/
├── SKILL.md              ← 本文件
├── README.md             ← VoltAgent原始说明
├── CONTRIBUTING.md       ← 贡献指南
└── design-md/            ← 品牌规范目录（59个品牌）
    ├── airbnb/
    ├── apple/
    ├── claude/
    ├── cursor/
    ├── figma/
    ├── linear.app/
    ├── minimax/          ← ⭐ 对B166ER最有参考价值（AI品牌）
    ├── notion/
    ├── opencode.ai/
    ├── Rever/
    ├── stripe/           ← ⭐ 金融/商业类最佳参考
    ├── supabase/
    ├── vercel/           ← ⭐ 科技/开发者类最佳参考
    └── ...（共59个）
```

---

## 与其他技能的集成

### design-md × article-to-infographic
```
design-md提供"设计规范"
         ↓
article-to-infographic生成"设计结果"
         ↓
输出：符合品牌规范的PNG/HTML海报
```

### design-md × design-md-generator（自建流程）
```
读取多个品牌DESIGN.md
         ↓
提取共性+个性
         ↓
生成AHL自有DESIGN.md
         ↓
用于未来所有AI生成项目
```

---

## 快速参考

**推荐B166ER优先掌握的5个品牌规范：**

| 品牌 | 视觉特点 | 适用场景 |
|------|---------|---------|
| Stripe | 高级金融感，蓝色+灰，清晰专业 | 商业/酒店/金融类信息图 |
| Vercel | 开发者科技感，深色+白，准系统风格 | 科技/AI/架构图 |
| Airbnb | 温暖亲切，珊瑚色+大地色，有温度 | 民宿/旅行/生活方式 |
| Linear | 深色海军蓝+青色，现代精确 | 工具型/数据型界面 |
| Notion | 柔和中性，灰度+绿，简洁克制 | 文档/知识/轻量感 |

---

## 注意事项

1. **DESIGN.md是Markdown格式**，直接可读可引用
2. **国内访问getdesign.md可能有网络限制**，如遇问题可尝试代理或直接读取本地design-md目录下的参考文件
3. **DESIGN.md不能替代Figma/设计稿**，它是AI友好的规范文档，不是完整设计系统
4. **品牌规范仅供学习参考**，如涉及商用需注意商标版权
