# Kimi PPT / 图片生成能力 · 逆向分析 (2026-10-21)

> **触发**: Eric "你可以逆向 KIMI 的 PPT 和图片生成能力么？"
> **方法**: 抓公开帮助文档 (kimi.com/help/ppt/ppt-overview, kimi.com/help/ppt, kimi.com/features/slides) + Tavily 查官方 API
> **边界**: 只读公开页面与官方文档；不抓私有接口、不绕鉴权/付费/风控
> **结论**: **能逆向"方法"，不必逆向"接口"**——Kimi PPT 的每一层我们都有对应零件，且视觉层我们明显更强

---

## 一、Kimi PPT 管线规格（逆向出的核心）

官方原文要点：
> "Kimi PPT 是 Kimi 推出的智能演示文稿生成工具，由 **K3 大模型**驱动，能够自动优化排版与设计……只需输入**一句话主题、粘贴一段文字，或上传一份文档**，Kimi PPT 就能根据内容类型选择最合适的视觉叙事方式，在**数分钟内**自动生成结构清晰、设计专业的完整演示文稿。当前 PPT 支持 PDF、Word 和上传的 PPT 对比。"

### 4 步管线（复原）

```
输入（3 种）
├─ 一句话主题
├─ 粘贴一段文字
└─ 上传文档 (PDF / Word / Excel / Markdown / PPT)
      ↓
① AI 深度研究 + 内容生成
   └─ 联网搜索 + 长文本整理 → 主题调研 + 数据整合 + 内容撰写
   └─ 关键: 引用的文献与数据均经真实信息源核验 ("有据可循")
      ↓
② 内容生成 (K3)
   └─ 自动研究 → 撰写 → 结构化 → 完整大纲 + 逐页文案
      ↓
③ 智能视觉设计
   └─ 自动匹配 主题配色 / 字体 / 图标 / 图表样式
   └─ 同步优化视觉呈现, 支持多种风格和模板
      ↓
④ 输出
   └─ 在线预览 → 可视化编辑 (点击改) → 下载可编辑 PPTX
   └─ 每月一定免费额度
```

### Kimi 官方对比表（传统 PPT vs Kimi PPT）

| 维度 | 传统 PPT | Kimi PPT |
|------|---------|----------|
| 创作方式 | 手动排版、逐页设计 | 一句话生成完整大纲+内容+设计 |
| 耗时 | 数小时至数天 | **几分钟**生成初稿 |
| 内容生成 | 需自己撰写文案 | AI 自动研究、撰写、结构化 |
| 视觉设计 | 依赖模板或设计能力 | AI 自动匹配配色、排版、图表 |

### Kimi 官方场景提示词（说明它的输入契约）

| 场景 | 提示词原文 |
|------|-----------|
| 工作汇报 | "我把这季度门店销售数据转成word文档转成10页PPT，商业风格，突出增长趋势" |
| 行业研究 | "生成一份2025年中国新能源车市场分析PPT，包含竞争格局、技术路线、政策背景" |
| 课程课件 | "我做一份从AGENT入门到进阶的PPT，适合非技术背景的产品经理，15页左右" |
| 产品发布 | "为一次AI写作工具产品发布会制作演示PPT，包含痛点、解决方案、核心功能、定价" |
| 提案融资 | "我把这份商业计划书PDF转成融资路演PPT，突出市场规模和团队优势" |
| 长文转化 | "我有一篇十万字的研究报告，帮我提炼成20页图文并茂的汇报PPT" |

**注意**: 提示词里**显式指定了页数、风格、目标听众、必含章节**——这是它的输入 schema，不是自由发挥。

---

## 二、Kimi 图片生成能力：**它没有**

- 官方 API 侧主推 **Vision（图像理解）**，不是生成
- 第三方对比明确写：**"Vision output is text-only: cannot generate or edit images, only interpret them"**
- 它的图片能力来自**上游模型**（GPT Image / Gemini 之类），Kimi 自己不做生成

**结论**: 图片生成这块**不需要逆向 Kimi**——我们本机已有：
| 我们的 | 能力 | 体积 |
|--------|------|------|
| `minimax-multimodal-toolkit` | 图像/视频/语音/音乐生成 + FFmpeg | 196 KB / 97 hits |
| `image-gen` | 图像生成 | 13 KB / 48 hits |
| `nano-banana-pdf` | Google nano-banana 图像编辑 | 24 KB |
| `image_generate` 工具 | 已验证可用（刚出深空主视觉） | — |
| `image-watermark-edit` | 水印/签名增删（PIL+OpenCV） | — |

---

## 三、Kimi 官方 API（可直接用，非逆向）

- 平台：`platform.kimi.com` / `platform.kimi.ai`
- 模型线：**Kimi K3.1 Pro / K3 / K2.6 / K2.5**（另有 moonshot-v1 系列）
- 价格（2026-09 第三方汇总）：`kimi-k3` 输入 $3 / 缓存命中 $0.30 / 输出 $15 per 1M，**上下文 1,048,576**
- 能力：`/chat/completions`、**Vision 视觉模型**、Web Search（$0.002/次）、URL Fetch（$0.002/次）、**Batch API（K2 线 6 折）**
- 兼容 OpenAI SDK（`base_url` 换 `https://api.moonshot.cn/v1`）

---

## 四、我们 vs Kimi：逐层对比

| 管线层 | Kimi | 我们（本机已有） | 谁强 |
|--------|------|----------------|------|
| ① 深度研究 | 联网搜索 + 长文整理 | **Tavily**（已装，已实测）+ **Scrapling 0.5**（已装，已实测）+ `scrapling-official` | 相当 |
| ② 内容生成 | K3 (1M ctx) | MiniMax-M3 / Kimi K3 API（可直接调）/ `x-research` / `last30days` / `autoresearch` | **Kimi 略强**（长上下文） |
| ③ 视觉设计 | "自动匹配配色/字体/图标/图表 + 多种风格和模板" | **open-design: 152 品牌 DESIGN.md + 116 渲染模板 + 13 craft 规则** + `design-md` + `color-palette-advisor` + `brandkit` + `creative-director` | **我们明显更强** |
| ④ 输出 | 在线预览 → 可视化编辑 → PPTX | `ppt-deck-builder-pro`(573KB) + `image-to-editable-ppt`(371KB) + `officecli` + `powerpoint-pptx` + `tiangong-wps-ppt-automation` + `super-ppt`(4 引擎) | 引擎更多，但**缺在线可视化编辑** |
| 图片生成 | ❌ 无 | ✅ 5 套 | **我们赢** |

### 我们唯一明确落后的一项

**在线可视化编辑（点击预览改）**——Kimi 生成后能点开预览、点哪里改哪里、在线改映射。
我们的 4 个引擎都是"生成→下载"链路，缺中间的可视化编辑层。

**这不是模型问题，是产品形态问题。** 补法有两条：
- 轻量：PPTX → HTML 预览（`lh-html-to-image` 反向 + `officecli` 读结构）→ 改 JSON → 重新导出
- 重量：自建中间层（PPTX ↔ 结构化 JSON ↔ Web 编辑器），工程量大

---

## 五、最优解：**用 Kimi 当发动机，不用 Kimi 当整车**

```
主题 / 长报告 / Word / PDF
      ↓
① 研究    → Tavily + Scrapling（我们的）
② 内容    → Kimi K3 API（1M 上下文读十万字报告，这是它最强的地方）
③ 视觉    → 152 品牌 DESIGN.md + 13 craft 规则（我们的，比它的"多风格模板"高一个量级）
④ 输出    → ppt-deck-builder-pro / officecli / WPS COM（我们的）
```

理由：
- Kimi 的护城河在 ①研究 + ②长文，**这两层我们自建要几个月**
- Kimi 的短板在 ③视觉——"支持多种风格和模板"= 通用化，没有专业设计系统
- 我们的 ③ 是**可累积资产**（每加一个品牌 DESIGN.md，能力永久提升），Kimi 每次生成都从零开始

---

## 六、下一步（待 Eric 决策）

1. **申请 Kimi API key**（platform.kimi.com）→ 接入 `②内容生成` 层，做一次 A/B 对比
2. **把 Kimi PPT 的输入契约写进我们的 PPT skill**：
   - 5 个显式参数：页数 / 风格 / 目标听众 / 必含章节 / 数据源
   - 我们的 `super-ppt` / `ppt-deck-builder-pro` 加同样的参数校验
3. **补在线可视化编辑**（我们唯一落后的项）——先做轻量版（PPTX↔HTML 预览）
4. **反向利用 Kimi PPT 的场景库**：它那 6 个场景提示词可以直接变成我们的 6 个 PPT 模板（工作汇报/行业研究/课程课件/产品发布/提案融资/长文转化）——**这批正好对应 Eric 的业务**（行业研究 + 提案融资 + 工作汇报）

## 七、相关文件

- 抓取脚本：`memory/_kimi_scrape2.py`（Playwright，等 React 渲染）
- 调研脚本：`memory/_kimi_research.py`（Tavily）
- 已有 skill：`ppt-deck-builder-pro` / `image-to-editable-ppt` / `super-ppt` / `officecli` / `minimax-multimodal-toolkit`
- 设计系统：`~/.open-design-skill/repo/`（152 DESIGN.md + 116 模板 + 13 craft + 169 skill）
