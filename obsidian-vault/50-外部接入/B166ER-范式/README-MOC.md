# B166ER 新媒体模板库 MOC

> 整合时间: 2026-07-12 22:45
> Eric 反馈: "你现在这个方法不行。全面扫描一遍以后再做调用和规范。"
> 目的: 任何新会话/新聊天 都自动加载此 MOC 作为视觉产出的标准

---

## 🚨 触发规则（每次新会话必读）

**任何视觉产出**（小红书详情图 / 海报 / PPT / 信息图）→ **必读此 MOC** → 复用模板 → 替换内容 → 渲染。

---

## 📐 范式总览（3 大固定）

### V3 Brutalist（已固定）
- **路径**: `revenue-v3-template/` + `overseas-v3-template/`
- **比例**: 1080 × 1440 (3:4)
- **配色**: 燕麦白 #F5F1EA + 砖红 #B6442A + 黑 #1A1410 + 金 #C9A87C
- **9 段结构**: cover/painpoints/value/audience/chapters/templates/quotes/delivery/cta
- **10 段结构**: cover/painpoints/value/audience/chapters/channels/cases/delivery/cta/trust
- **适用**: 决策类/总经理/采购总监/供应链（权威稳重）

### V6 美联储（已固定）
- **路径**: `supply-chain-gen-scripts/gen_v6_fed.py`
- **比例**: 1080 × 1440 (3:4)
- **配色**: 深蓝 #1E3A5F + 金 #D4A574 + 米白 #F5F1EA + 黑
- **特点**: 货币视觉锤（¥99 金色块）+ 数据墙（13/10/5/24）+ 严格左上右下 B 标
- **适用**: 价格突出/数字驱动/专业权威

### B166ER 海报（暗黑霓虹）
- **路径**: `B166ER-海报-template.html` + `B166ER-架构图-template.html`
- **比例**: 1080 × 1920 (9:16)
- **配色**: 暗黑底 #050810 + 主题色 c0-c52 + Noto Sans SC
- **适用**: 架构图/概念图/长海报

---

## 🎨 B 标严格用法（铁律 R30）

### 设计标准
- 圆 B (深棕 #2A1F14 → #3A2E22) + 金环 #C9A87C + 单字母 "B"
- 副文字: "ERIC × B166ER" (主) + "共研出品" (副)
- 字号比例: B = 55%, 主文 = 28%, 副文 = 22%

### 严格 2 位置（任何视觉）
- **左上** (top-left): 主体 B 标 + ERIC × B166ER + 共研出品
- **右下** (bottom-right): 简化 B 标 + 版本/日期
- **绝不**放左下 / 右上 / 底部正中

### 5 大场景（统一）
1. PPT 首页/末页 — 大 B 标 64-128px
2. 长图水印 — 中 B 标 32-48px
3. 公众号文章 — 小 B 标 16-24px
4. 头像 — 圆 B 32-256px
5. 文档/海报 — 中 B 标 48-64px

### 3 大铁律
- **不抢主体**: B 标永远 ≤ 主标题尺寸的 1/4
- **统一署名**: 所有材料都是 "ERIC × B166ER 共研出品"
- **不绑行业**: B 标本身不带酒店/旅游/AI 标签

---

## 💰 价格铁律

- **整套资料统一 ¥99**（不是 ¥2980 / ¥19800 / ¥5000+）
- 价格出现 ≤ 2 处（中部主价 + CTA）
- 价格块必须金色 + 深蓝/燕麦背景 = **货币视觉锤**

---

## ✅ 小红书合规铁律（R29）

### 绝对禁止字眼
- 微信 / 加微信 / 加我
- 扫码 / 扫一扫 / 二维码
- 支付宝 / 抖音 / 微博 / 其他平台
- 私域 / 引流
- 企业开票 / 1对 1 答疑（外部渠道）
- 任何"非小红书"的交易/联系/沟通方式

### 可用合规字眼
- 评论扣 1 / 扣 1 / 留言 1
- 私信 / 站内信
- 点击下方 / 购物车 / 小红书商城
- 主页 / 店铺
- 立即购买 / 限时优惠
- 收藏 / 关注

---

## 🔧 调用流程（标准 5 步）

### Step 1：选择范式
```
决策类/价格突出 → V6 美联储
权威稳重/采购 → V3 Brutalist
架构图/概念图 → B166ER 海报
```

### Step 2：复制模板
```bash
# V3 路径示例
cp revenue-v3-template/html/p01_cover.html my-new-product/cover.html

# V6 路径示例
cp supply-chain-gen-scripts/gen_v6_fed.py my-new-product/gen.py
```

### Step 3：替换内容
- HTML body 内容（保留 CSS）
- 或 Python 脚本中的 PAGES 字典

### Step 4：渲染（Edge headless）
```bash
msedge --headless --disable-gpu --hide-scrollbars \
  --screenshot=out.png --window-size=1080,1440 \
  file:///path/to/html.html
```

### Step 5：沉淀到 vault
- 复制成品到 `50-外部接入/{产品名}-成品/`
- 写 README.md 记录

---

## 📁 模板文件清单

```
D:/B166ER-OpenClaw/workspace/obsidian-vault/50-外部接入/B166ER-范式/

├── README-MOC.md                              ← 本文件
├── B标-标准用法指南.html                       ← B 标官方指南 (13KB)
├── brand-official.png                          ← B166ER 品牌标 PNG (846KB)

├── revenue-v3-template/                       ← 范式 1: 收益管理 V3 (9 张 3:4)
│   ├── html/  (9 个 p01-p09 html)
│   ├── rendered-wm/  (9 个 wm png)
│   └── rendered-raw/  (9 个 raw png)

├── overseas-v3-template/                      ← 范式 2: 海外客源 V3 (10 张 3:4)
│   └── html/  (10 个 p01-p10 html)

├── supply-chain-gen-scripts/                  ← 范式 3: 我做的供应链工程 V5/V6
│   ├── gen_v5_pillow.py
│   └── gen_v6_fed.py

├── B166ER-海报-template.html                  ← 海报模板 (16KB)
├── B166ER-架构图-template.html                ← 架构图模板 (20KB)
├── AHL-infographic-template.html              ← AHL 信息图 (16KB)
├── poster-v2.2-template.html                  ← 海报 v2.2 (30KB)
├── infographic-v2.2-template.html             ← 信息图 v2.2 (23KB)
├── ahl-poster-template.html                    ← AHL 海报 (23KB)
└── ahl-phone-poster-template.html              ← AHL 手机海报 (20KB)
```

---

## 📋 自检清单（输出前）

- [ ] 价格 ¥99 (不是其他)
- [ ] 居中紧凑排版（无大片留白）
- [ ] 字号够大（主标题 ≥ 150px，正文 ≥ 28px）
- [ ] B 标严格左上+右下
- [ ] 无微信/扫码/加我（合规）
- [ ] 价格 ≤ 2 处（货币锤）
- [ ] 9-10 张成套（每张独立信息）
- [ ] 沉淀到 obsidian-vault

---

## 🎯 调用示例

### 例 1：做新产品的详情图
1. Eric 说: "做 XX 产品的小红书详情图"
2. 我读此 MOC → 选 V3 或 V6
3. 复制对应模板
4. 替换内容 (9 段信息)
5. Edge 截图渲染
6. 沉淀到 vault

### 例 2：换聊天继续
1. 新会话开始
2. 系统注入本 MOC（自动）
3. 我立即知道所有范式 + B 标 + 合规
4. 不用从头问"有没有模板？"

---

## 📝 版本历史

- **v1.0 (2026-07-12)** — 首次整合 12 类模板 + 9 条规则 + 5 步流程
- Eric 反馈: "换一个聊天就又要重来那不行" → 本 MOC 解决