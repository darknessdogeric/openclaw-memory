# PPT模板快速选择指南

## 🎯 一句话选择法

```
投资人路演 → startup_roadshow (渐变紫橙)
企业客户 → corporate_pro (专业深蓝)
董事会 → corporate_pro 或 dark_blue_business
数据报告 → data_viz_pro (数据可视化)
简洁演示 → minimal_white 或 light_consulting
科技产品 → gradient_modern (渐变现代)
中国风 → elegant_chinese (国风雅韵)
培训讲解 → whiteboard_handdrawn (白板手绘)
创意展示 → creative_playful (趣味创意)
高端奢华 → luxury_premium (黑金)
环保健康 → green_nature (自然清新)
```

---

## 📊 模板对比表

| 模板 | 背景色 | 主色调 | 风格 | 适用场景 |
|------|--------|--------|------|---------|
| startup_roadshow | 深色 | 紫→橙渐变 | 活力、动感 | 融资路演 |
| corporate_pro | 深蓝白 | 海军蓝 | 专业、商务 | 企业提案 |
| dark_blue_business | 深蓝 | 钴蓝 | 高端、商务 | 客户演示 |
| light_consulting | 白色 | 深灰 | 简洁、清晰 | 咨询报告 |
| minimal_white | 纯白 | 黑色 | 极简、设计 | 作品集 |
| gradient_modern | 深色 | 蓝紫粉渐变 | 科技、创新 | AI/科技 |
| elegant_chinese | 浅色 | 朱红/金/玉绿 | 国风、文化 | 文化演讲 |
| data_viz_pro | 浅色 | 蓝绿 | 专业、数据 | 分析报告 |
| creative_playful | 浅色 | 彩色 | 趣味、活力 | 教育/儿童 |
| luxury_premium | 黑色 | 黑金 | 高端、奢华 | VIP演示 |
| green_nature | 浅色 | 绿色 | 自然、环保 | 可持续品牌 |
| whiteboard_handdrawn | 白板 | 手绘 | 培训、讲解 | 教学演示 |

---

## 🔧 使用方法

### 方式1: 在plan文件中指定

```json
{
  "style_preset": "startup_roadshow",
  "slides": [...]
}
```

### 方式2: 命令行指定

```bash
bash scripts/run_full_deck.sh plan.json output_dir deck.pptx --preset startup_roadshow
```

### 方式3: 描述选择

告诉B166ER你的场景：
- "我要做融资路演" → 自动选择 `startup_roadshow`
- "给客户展示方案" → 自动选择 `corporate_pro`
- "产品发布会" → 自动选择 `gradient_modern`

---

## 💡 模板选择决策树

```
开始
  │
  ▼
是融资路演？ ──是──→ startup_roadshow
  │
  否
  ▼
是科技/AI产品？ ──是──→ gradient_modern
  │
  否
  ▼
需要大量数据？ ──是──→ data_viz_pro
  │
  否
  ▼
是培训/教学？ ──是──→ whiteboard_handdrawn
  │
  否
  ▼
是中国文化？ ──是──→ elegant_chinese
  │
  否
  ▼
需要高端奢华？ ──是──→ luxury_premium
  │
  否
  ▼
是环保/健康？ ──是──→ green_nature
  │
  否
  ▼
想要极简设计？ ──是──→ minimal_white
  │
  否
  ▼
默认 → corporate_pro 或 dark_blue_business
```

---

## 🎨 视觉示例关键词

每个模板对应的AI图像生成关键词：

### startup_roadshow
`startup pitch deck, venture capital style, gradient purple to orange, bold typography, dynamic energy, geometric shapes, floating particles, modern tech, innovative`

### corporate_pro
`corporate professional, enterprise style, navy blue theme, clean white space, structured business, board ready, formal presentation`

### gradient_modern
`modern gradient, blue purple pink gradient, glassmorphism, floating 3D elements, futuristic tech, innovative digital, colorful glow, dark theme`

### elegant_chinese
`Chinese traditional style, elegant Chinese, vermillion red, jade green, gold accents, ink wash texture, classical elegance, oriental style`

### luxury_premium
`luxury premium, black gold theme, elegant serif, exclusive feel, minimalist luxury, high-end brand, sophisticated`

---

**生成PPT时，告诉B166ER：**
1. 用途场景
2. 目标受众
3. 想要的风格（或让B166ER推荐）

B166ER会自动选择最合适的模板！
