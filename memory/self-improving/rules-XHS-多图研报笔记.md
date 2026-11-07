# 小红书多图研报笔记工作流 (R34)
**创建时间**: 2026-07-16 16:32
**触发**: Eric 从朋友圈信息图 → 抖音视频脚本 → 小红书多图笔记 4 次迭代定稿
**适用**: 任何"研报式分析 + 多图笔记"组合（小红书 / 公众号 / 微博九宫格）

---

## 核心模式 (If → Then)

**If** Eric 要求"小红书风格 / 多图笔记 / 7 张图 / 公众号长图"，
**Then** 直接调用下方 XHS 模板：

### 📐 设计规格

| 项 | 规格 |
|----|------|
| 画布 | **1080 × 1440** (3:4 标准) |
| 张数 | **7 张**（黄金节奏：封面 + 5 段内容 + 收口）|
| 风格 | **麦肯锡 + 美联储 + 摩根**：白底 + 深蓝 #0A2540 + 红 #C8102E |
| 字体 | 思源宋体 / Helvetica Neue / PingFang SC fallback |
| 顶部 masthead | "B166ER · 商业内参" + 日期 + ISSUE NO.001 (80px 高) |
| 底部 footer | SOURCE + 页码 (60px 高) |
| 内容区 | 上下 flex column + justify-content: space-between |

### 🎨 V4 字号体系（已验证）

| 元素 | 字号 |
|------|------|
| h1 标题 | 88px |
| h2 章节 | 56px |
| body-text 正文 | 28px |
| 表格 td | 23px |
| 列表 li | 28px |
| data-callout value | 78px |
| pull-quote | 36px |
| dark-callout body | 28px |

### 🗂 7 张叙事模板

| # | 角色 | 内容模板 |
|---|------|---------|
| 01 | 封面 | "EXECUTIVE BRIEFING" + 大字钩子（数字对比）+ 副标题斜体 + 3 项元数据表 |
| 02 | 现象 / 数据 | eyebrow "01 · THE PHENOMENON" + h2 + 一段引言 + 5 行硬数据表 + 红条批注 |
| 03 | 框架 / 公式 | eyebrow "02 · THE FRAMEWORK" + 巨型公式 + Pull Quote + Data Callout |
| 04 | 动机 / 拆解 | 表格化（# / 关键词 / 心理机制）+ 灰色 CONCLUSION 收口 |
| 05 | 反转 / 受众 | 三栏 audience grid + 黑色 KEY INSIGHT callout |
| 06 | 启示 / 启示 | 编号列表 (ol.editorial) + **黑色 UNDERLYING CAUSE 大 box** |
| 07 | 收口 / CTA | eyebrow "06 · THE TAKEAWAY" + 黑底 CORE LAW + 金句（删线对比）+ 灰色 FORWARD LOOK + DISCUSSION |

---

## 🛠 技术 SOP

### 渲染流程（避免 Edge headless hang）

```
1. 写 master CSS + 7 个 SLIDE_XX = f"""...""" 字符串到 toolbox/xhs_mckinsey.py
2. 写 toolbox/xhs_render_only.py → exec(master_file) 真正求值 f-string
3. Edge headless 渲染（每张 ~30-60s，timeout 45s）
4. 写 toolbox/xhs_pil_wm.py → PIL 视觉水印（不用 blind_watermark 库，会 hang）
```

### 必须避开的坑

1. **❌ blind_watermark 库** — 在大量 Python 并发下会 hang（曾浪费 20+ 分钟）
   - 改用 **PIL 视觉水印**（左上 B166ER 标签 + 右下 © 戳 + 中心浅色水印）
2. **❌ f-string 在 re.search 里** — 抓到的是字面源码（含 `{eyebrow(...)}`），渲染出来是 Python 代码
   - 改用 `exec()` 真正求值
3. **❌ PowerShell `&&` 链式** — PowerShell 不支持
   - 用分号 `;` 串行
4. **❌ Edge 进程僵尸** — 多个 headless 调用后会有 webview2 僵尸进程
   - 监控 PID CPU/RSS，必要时 `Stop-Process -Force`

### 一键命令

```bash
# 渲染 + 水印（用 ; 分隔，不是 &&）
python toolbox/xhs_render_only.py ; python toolbox/xhs_pil_wm.py
```

---

## 📊 Eric 反馈迭代轨迹（2026-07-16）

| 轮次 | Eric 反馈 | 我的响应 |
|------|---------|---------|
| 1 | "这个模版不行。换成麦肯锡+美联储+摩根的那种" | 重写为白底深蓝红三色体系 |
| 2 | "排版问题。正文字体太小，页面不均匀" | 字号 V1→V2（18→22px），加 spacer 节奏 |
| 3 | "6,7图的风格版式不一致" | 全部用统一 master CSS + flex space-between |
| 4 | "字体还应该继续放大。页面还是有很多空白区域" | 字号 V2→V3（22→26px），改用 flex 撑满 |
| 5 | "字体还可以再大一些。同时调整一下版面" | V3→V4（26→28px），render bug 修复，slide_06 加黑底大 box |

**关键经验**：Eric 对字号敏感度极高，每次评审都会要求"再大一些"。最终稿 V4 仍是"刚好够"。

---

## 📁 文件位置

- 渲染脚本：`D:\B166ER-OpenClaw\workspace\toolbox\xhs_mckinsey.py` (master + slide bodies)
- 渲染执行：`D:\B166ER-OpenClaw\workspace\toolbox\xhs_render_only.py`
- 水印脚本：`D:\B166ER-OpenClaw\workspace\toolbox\xhs_pil_wm.py`
- 输出目录：`D:\B166ER-OpenClaw\workspace\output\xhs_2026-07-16\`
- 发布内容（标题/正文/标签）：见 2026-07-16 对话记忆

---

## 🎯 复用触发条件

**符合以下任一**就调这个工作流：
- "做一组小红书图"
- "公众号长图 / 多图笔记"
- "7 张 / 9 张图的分析笔记"
- "研报风格的信息图"

**直接调**：`python toolbox/xhs_render_only.py ; python toolbox/xhs_pil_wm.py`，
然后改 `xhs_mckinsey.py` 里的 SLIDE_XX 内容即可。

---

## 🔗 相关规则

- R12: 所有视觉产出必须水印（盲水印或 PIL 视觉水印均可）
- R13: vault 大体量隔离（不直接适用于 XHS，但思路一致）
- R26-R33: B166ER 海报范式（小红书是范式的延伸应用）