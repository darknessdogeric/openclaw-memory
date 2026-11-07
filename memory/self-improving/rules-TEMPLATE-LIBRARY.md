# B166ER 模板库总索引 V2 (R36)
**更新时间**: 2026-07-16 20:15
**触发**: Eric "全面梳理好你的模版库。我们之前做过很多模版。不光是这一个。"
**范围**: 遍历 workspace 所有 HTML/Python 产出 + Desktop 所有发布版本 → 11 大范式

---

## 🎨 11 大视觉范式（按 Eric 偏好强度排序）

### V0 · B166ER 主标识（B 标 / Logo 体系）⭐⭐⭐⭐⭐
| 项 | 值 |
|----|---|
| 配色 | 黑底金字 + 米色 ERIC 标志 |
| 元素 | 左上 E 圆标 + ERIC × B166ER + 右下 B166ER EST. 标 + 红方块 |
| 适用 | 几乎所有产出品 |
| Eric 评价 | ⭐⭐⭐⭐⭐ 必带标志（强 IP 资产）|

### V1 · B166ER 海报范式（深空金色）⭐⭐⭐
| 项 | 值 |
|----|---|
| 配色 | 深空 #0a0e1a → #141b2d + 金 #d4af37 + 朱红 |
| 字体 | PingFang SC / 思源宋体 |
| 元素 | 径向高光 + 网格背景 + 四角金色 L 角标 |
| 适用 | 朋友圈信息图、长图海报 |
| 脚本 | `toolbox/xhs_slides.py` |
| 案例 | 智驾小蓝灯 V1（2026-07-16）|
| Eric 评价 | ❌ 第一版被否（"模版不行"）|

### V2 · 玉帝视角（深底朱红金）⭐⭐⭐
| 项 | 值 |
|----|---|
| 配色 | 深空 #080b1e + 朱红 #d02030 + 真金 #d4af5f + 雾蓝 |
| 字体 | 黑体 / 楷体 / 思源宋体 |
| 元素 | 四角金色 L + 顶部红条 + 玉帝视角版式 |
| 适用 | 9 张小红书深度叙事 |
| 脚本 | `toolbox/gen_2026_summer_xhs_9.py` |
| 案例 | 2026 暑期酒店 9 图 V2 |
| Eric 评价 | ✅ 行业解读系列 |

### V3 · Swiss Modern 基础版（燕麦白黑白红）⭐⭐⭐
| 项 | 值 |
|----|---|
| 配色 | 燕麦白 #f4f1ec + 黑白灰 + 朱红 #d62828 + 暗蓝 #003049 |
| 字体 | Inter / Noto Sans SC + IBM Plex Mono |
| 元素 | 网格背景线 + 顶部 56px 黑线 + flex 自适应 |
| 适用 | 6 张/9 张通用版 |
| 脚本 | `toolbox/gen_xhs_6grid_hotel.py` / `toolbox/gen_2026_summer_xhs_v3.py` |
| 案例 | 暑期 V3.1 / 十五五 6 图 |
| Eric 评价 | ✅ 工作笔记风 |

### V3-Pro · Swiss Modern 高级定制版（出版物感）⭐⭐⭐⭐
| 项 | 值 |
|----|---|
| 配色 | 燕麦白 #f5f1e8 + 黑 + 朱红 #c8102e + 暗蓝 #0a3d62 + 金 #a07d3c |
| 字体 | Inter / Noto Sans SC + IBM Plex Mono |
| **升级元素** | 黑色 4 宫格数据块 / "MASTER PLAN · 01/7" 编号 / POL 2026 / TOP 02 / 玉帝视角终极解读 / 01-06 红色编号 + 网格 |
| 视觉骨架 | top 1px 黑色横线 + brand 左 / COVER 日期右<br>main: flex column space-between, kicker 红短横线, h1 90px + em 红色斜体<br>tag: 黑色 4 宫格, 大数字朱红<br>audience: 2 列网格 + 红色编号<br>bottom: source 左 + 红方块 ERIC 标 + 副标识右 |
| 适用 | 6 张 + 7 张详情页 + 多受众 + 行业全景 + 个人售卖引流 |
| 案例 | **2026 十五五酒店业 6 图 v1.0** + sovereign_p0X（`C:\Users\ericz\Desktop\小红书产品线\2026十五五酒店业6图-v1.0\`）|
| Eric 评价 | ⭐⭐⭐⭐⭐ 实际使用案例 |

### V4 · 麦肯锡 + 美联储 + 摩根（白底深蓝红）⭐⭐⭐⭐⭐
| 项 | 值 |
|----|---|
| 配色 | 纯白 #FFFFFF + 深蓝 #0A2540 + 麦肯锡红 #C8102E |
| 字体 | Helvetica Neue + 思源宋体副字（v1）/ Inter + Noto Sans SC + IBM Plex Mono + Cormorant Garamond（V3-Pro 同源早期版）|
| 边距 | 40-50px side / masthead 80px / footer 60px |
| 元素 | masthead（编辑体小标）+ 红色 accent bar + 黑色数据表 + 灰色 callout + 黑色 pull quote |
| 字号 | h1 88px / h2 56px / 正文 28px |
| 适用 | 7 张小红书研报式多图笔记 |
| 脚本 | `toolbox/xhs_mckinsey.py` + `xhs_render_only.py` + `xhs_pil_wm.py` |
| 早版 | `toolbox/mckinsey_p0X_v4.html`（V3-Pro 配色 + IBM Plex Mono + Cormorant Garamond 衬线）|
| 案例 | 智驾小蓝灯 7 张（2026-07-16）|
| Eric 评价 | ⭐⭐⭐⭐⭐ 4 轮迭代定稿 |

### V5 · 留白东方美学（意境/气韵）⭐
| 项 | 值 |
|----|---|
| 配色 | 大面积留白 + 单色点缀 |
| 字体 | 宋体 / 楷体 |
| 风格 | 东方意境，气韵优先 |
| 适用 | 强调情绪/品牌调性的内容 |
| 现状 | 散落在 `brand_standard_usage.html` |
| Eric 评价 | 待用 |

### V6 · 东方气韵实战版（米黄朱红黑）⭐⭐⭐⭐⭐ ← Eric 真正的主视觉
| 项 | 值 |
|----|---|
| 配色 | **米黄渐变 #f5e8c8 → #e8d4a8** + **朱红 #c8102e / #d62828** + **黑 #0a0a0a** + 金边 |
| 字体 | 思源黑体 + 思源宋体 + 楷体（中文标题）|
| 元素 | **ERIC × B166ER 黑色圆角 logo** + B166ER EST 标 + 红色高潮条 + 白底圆角数据卡 + 黑榜（暗背景 + 红色大数据）+ 底部 B166ER 红方块 |
| 视觉骨架 | 顶部黑色 ERIC logo + ERIC × B166ER<br>main: 居中标题（黑底或米底）<br>数据卡: 白底圆角 + 大数据 + 绿色增长/红色下降/黑色稳健<br>黑榜: 黑色背景 + 红色数字 + 城市/品牌列表<br>风险区: 浅红/浅黄背景警示框<br>bottom: 黑色 ERIC 标 |
| 适用 | **酒店预测报告 / 行业分析 / 东方美学内容** |
| 案例 | **Eric 审美基因图鉴 9x16** / **端午酒店预测 9x16**（T-2 终稿）/ **全国端午酒店预测 9x16** |
| 脚本 | ✅ `toolbox/gen_xhs_v6_dongfang.py`（2026-08-30 补建）|
| Eric 评价 | ⭐⭐⭐⭐⭐ 多次发布使用 |

### V7 · 极简宽屏 Hero（米白蓝点）⭐⭐⭐
| 项 | 值 |
|----|---|
| 配色 | 黑色顶部 + 米白底 + **蓝色点缀 #1e3a8a / #0066cc** + 红字高亮 |
| 字体 | 思源黑体 |
| 元素 | 顶部黑色品牌条 + "HOTEL INDUSTRY BRIEF" + "ISSUE 26-307" + 黑榜 + 蓝色"¥ 亿级"块 + 红色 ¥99 CTA |
| 适用 | **公众号 / 官网首页 hero / 长图宽屏（不是 3:4 也不是 9:16，是宽屏 1080:1229 等）** |
| 案例 | **酒店数据资产 hook 图**（`D:\Users\ericz\Desktop\data-asset-hook.png`）|
| Eric 评价 | ✅ 售卖引流（这是 ¥99 售卖品的主视觉）|

### AHL 系列（项目专属）⭐⭐
| 子版本 | 配色 | 用途 | 文件 |
|--------|------|------|------|
| **AHL 深空科技** | 深空 + 青蓝渐变 + 紫 + 金 + 红 + 绿（6 色彩虹）+ Noto Sans/Serif | AHL 海报 / 信息图 | `ahl-poster.html` `ahl-glass.html` `B166ER_海报.html` `B166ER_架构图.html` |
| **AHL Landing** | 深空 #0a0a0f + 青绿 #00d4aa + Outfit / Space Grotesk | AHL 官网 / 落地页 | `ahl-landing.html` `ahl-phone-poster.html` `ahl-phone-flat.html` |
| **AHL 渐变蓝** | 渐变蓝 #1a365d + 青绿 #319795 + 金 #ffd700 | AHL 早期信息图 | `AHL_Infographic.html` |
| **AHL 抖音脚本** | 深蓝 #0A2540 + 朱红 #DC2626 + 金 #D4A574 + 思源宋体 | 抖音视频脚本 + 诊断 | `AHL_Zhiju_*.html` |
| **AHL SVG Dark** | 深灰 #27272a + 白色文字 + emoji 图标 | SVG 架构图 | `AHL-4层架构图.html` `ahl-arch-diagram.html` `ahl-single-hotel-arch.html` |

### GitHub Dark 风（开发/技术圈专属）⭐⭐
| 项 | 值 |
|----|---|
| 配色 | 深空 #05080c / #0a0e14 + GitHub 经典 6 色（蓝 #58a6ff / 紫 #a371f7 / 橙 #f0883e / 绿 #3fb950 / 黄 #d29922 / 红 #f85149）+ JetBrains Mono / Fira Code |
| 元素 | radial gradient 高光 + 6 色层级 badge |
| 适用 | **技术向内容 / 开发者受众 / AI Agent / AHL 类项目** |
| 案例 | `poster-v2.2.html` / `infographic-v2.2.html` |
| Eric 评价 | ✅ 技术圈 |

### 五角星 Pentagram（5 维度对比）⭐
| 项 | 值 |
|----|---|
| 配色 | 米白 #fafaf8 + 5 色（橙 #cf6e2e / 蓝 #2e6bcf / 绿 #2e8b57 / 紫 #6b3fbf / 金 #bf9a2e / 红 #cf3e3e）+ 衬线字体 |
| 适用 | **5 维度/5 主题对比图** |
| 案例 | `infographic-pentagram.html` |
| Eric 评价 | 待用 |

### Mindmap 风（思维导图专用）⭐
| 项 | 值 |
|----|---|
| 配色 | 深空 #080c1f + 6 色（青 #00c8ff / 橙 #ff6b35 / 紫 #a78bfa / 绿 #4ade80 / 金 #fbbf24 / 粉 #f472b6）+ Inter |
| 适用 | **思维导图 / 框架图** |
| 案例 | `b166er-framework-mindmap.html` |
| Eric 评价 | ✅ |

### 数据报告蓝灰（蓝灰数据卡）⭐⭐
| 项 | 值 |
|----|---|
| 配色 | 深空 #1a2438 + 米白 #f5f3ed + 数据卡（白底圆角 + 大数据 + 绿增红降黑稳）|
| 元素 | 顶部 "DRAGON BOAT FESTIVAL · 2026" 英文小标 + 朱红数据卡边框 |
| 适用 | **数据报告型内容** |
| 案例 | **2026 年 6 月_上半年经济数据全方位解读**（17 张 jpeg）|
| Eric 评价 | ✅ "官方原文验证版"风格 |

---

## 📐 通用视觉规范（R26-R33）

| 规则 | 内容 |
|------|------|
| R26 | B 标严格用法（V0 标志，左上 + 右下）|
| R27 | 价格 ¥99 整套模板 |
| R28 | 小红书合规铁律 |
| R29 | 9-10 段标准结构 |
| R30 | 标准 5 步调用流程 |
| R31-R33 | 配套规则（话题、互动、CTA）|

**统一参考**：`obsidian-vault/50-外部接入/B166ER-范式/README-MOC.md`

---

## 🛠 技术栈清单

### 渲染引擎
| 工具 | 用途 | 备注 |
|------|------|------|
| **Edge headless** | V3 / V4 / V3-Pro HTML → PNG | `--force-device-scale-factor=2` Retina |
| **PIL 直接画图** | V1 / V2 海报 | 2160×3840 (2x retina)，适合深色 |
| **SVG** | AHL 架构图 | `ahl-4层架构图.html` 系列 |

### 水印方案
| 工具 | 用途 | 注意事项 |
|------|------|---------|
| **PIL 视觉水印** | 文字版式海报 | 快、不 hang |
| **blind_watermark 库** | 隐蔽水印 | ⚠️ 并发 hang，已被替换 |

### 字体
- 思源宋体 / Noto Serif CJK SC（标题、副字）
- 思源黑体 / Noto Sans SC（中文正文）
- Inter / Helvetica Neue（西文）
- IBM Plex Mono / JetBrains Mono（数据、英文小标）
- Cormorant Garamond（衬线英文 - V3-Pro/V4 早期版）
- Outfit / Space Grotesk（AHL 落地页）
- PingFang SC / Microsoft YaHei（中文 fallback）

---

## 🎯 模板选择决策树（完整版）

**Eric 说："做 XX 内容"**

```
1. 内容场景是？
   ├─ 朋友圈 (4:5 或 3:4)
   │   ├─ 长图（多张内容）  → V1 B166ER 海报 或 V6 东方气韵 ⭐
   │   ├─ 单图海报          → V6 东方气韵 ⭐
   │   └─ 预测/数据报告     → V6 东方气韵 ⭐ / V8 KIMI 数据版 ⭐⭐⭐⭐⭐
   │
   ├─ 小红书 (3:4, 6-9 张)
   │   ├─ 行业全景/玉帝视角  → V2 玉帝视角 9 张
   │   ├─ 通用受众/售卖引流  → V3 Swiss Modern 6/9 张
   │   ├─ 出版物感/详情页    → V3-Pro (6 张详情页 + 笔记页)
   │   ├─ 研报式/商业分析   → V4 麦肯锡 7-9 张 ⭐
   │   ├─ 数据报告型        → 数据报告蓝灰
   │   └─ 预测报告          → V6 东方气韵 ⭐ (Eric 主用)
   │
   ├─ 公众号 (长图 / 多图)
   │   ├─ 详情页 + 笔记页组合 → V3-Pro ⭐
   │   ├─ 宽屏 hero (售卖)    → V7 极简宽屏 ⭐ (¥99 售卖)
   │   └─ 数据分析长文       → V4 麦肯锡
   │
   ├─ 抖音视频脚本
   │   ├─ 出镜人 + 旁白     → 直接写脚本
   │   ├─ 纯旁白 + 画面     → 直接写脚本
   │   └─ AHL 项目           → AHL 抖音脚本深蓝朱红金
   │
   ├─ 技术向内容
   │   ├─ 架构图 / 思维导图  → AHL 深空科技 / Mindmap 风 / 五角星
   │   └─ 开发者受众        → GitHub Dark 风
   │
   └─ AHL 项目
       ├─ 海报 / 信息图      → AHL 深空科技
       ├─ 落地页 / 官网       → AHL Landing (青绿)
       └─ 抖音脚本          → AHL 抖音脚本深蓝朱红金
```

---

## 📊 模板使用统计（Eric 真实发布）

| 模板 | 发布案例 | Eric 评价 |
|------|---------|---------|
| **V6 东方气韵** ⭐ | **Eric 审美基因图鉴 / 端午酒店预测 T-2 终稿 / 全国端午预测** | **⭐⭐⭐⭐⭐ 主视觉** |
| **V8 KIMI 数据版** ⭐⭐⭐⭐⭐ | **2026 H1 经济数据 17 张** | **⭐⭐⭐⭐⭐ 生产主力** |
| V3-Pro | 2026 十五五酒店业 6 图 | ⭐⭐⭐⭐⭐ |
| V4 麦肯锡 | 智驾小蓝灯 7 张 | ⭐⭐⭐⭐⭐ |
| V2 玉帝视角 | 暑期酒店 9 图 V2 | ✅ |
| V3 Swiss Modern | 暑期 V3.1 | ✅ |
| V1 B166ER 海报 | 智驾小蓝灯 V1 | ❌ 被否 |
| V7 极简宽屏 | 酒店数据资产 hook | ✅ |
| 数据报告蓝灰 | 2026 H1 经济数据 17 张 | ✅ |
| AHL 系列 | 多版本 | ✅ |
| GitHub Dark | 技术向 | ✅ |
| Mindmap / Pentagram | 待用 | 待用 |

---

## 🚨 已知坑（避免重犯）

| 坑 | 解决方案 |
|----|---------|
| PowerShell `&&` 报错 | 用 `;` |
| blind_watermark hang | PIL 视觉水印 |
| f-string + re.search | `exec()` 真正求值 |
| Edge headless 僵尸 | 监控 PID |
| 页面顶部密集 | flex column + space-between |
| 字号偏小 | Eric 喜欢 V4 的 28px 正文 |

---

## 🚧 待补建脚本

| 缺失 | 优先级 | 说明 |
|------|--------|------|
| **V6 东方气韵脚本** | ⭐⭐⭐⭐⭐ | Eric 主视觉，必须建 |
| **V8 KIMI 数据版脚本** | ⭐⭐⭐⭐⭐ | **生产主力，必须建**（用 HTML 模拟 KIMI 视觉）|
| V7 极简宽屏脚本 | ⭐⭐⭐ | ¥99 售卖品用 |
| 数据报告蓝灰脚本 | ⭐⭐⭐ | 17 张系列需要 |
| 五角星 Pentagram 脚本 | ⭐⭐ | 待用 |
| Mindmap 脚本 | ⭐⭐ | 待用 |

---

## 🔗 相关规则

- R12: 所有视觉产出必须水印
- R26-R33: B166ER 海报范式
- R34: 小红书多图研报笔记工作流
- R35: 模板库索引（已升级到 R36）

---

**维护人**: B166ER
**最后更新**: 2026-07-16 20:15
**触发**: Eric "全面梳理好你的模版库。我们之前做过很多模版。不光是这一个。"
**下次评审**: 当 Eric 提出新模板需求、或现有范式遇到新失败时。