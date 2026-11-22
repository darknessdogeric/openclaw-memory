# 卡片生成范式纪律 · 长期生效

> **固化时间**:2026-10-06 12:29 GMT+8
> **来源**:综合 nexu-io/card-xiaohongshu(Apache-2.0, 8.3K stars) + Eric 反复反馈 + 金轩十文 9 图 11 版迭代实战
> **状态**:**以后 Eric 让作图(小红书、PPT、信息图、海报),一律走 `toolbox/templates/xhs_card_generator.py` 范式,不再重新写 CSS**

---

## 一、5 条硬纪律(每次出图前对照)

### 1. 画布用 grid 4 行固定分配

```css
.canvas {
  width:1080px; height:1440px;
  padding: 40px 56px 30px;
  display: grid;
  grid-template-rows: 70px 150px 1fr 170px;
  gap: 14px;
}
```

**禁止**用 `position:absolute` 定位各区段(11 版踩过的坑)。

### 2. seg-body 用 `justify-content: space-evenly`

```css
.seg-body {
  background:rgba(255,255,255,0.04);
  border:1px solid rgba(212,167,116,0.20);
  border-radius:10px;
  padding:18px 20px;
  display:flex; flex-direction:column;
  justify-content: space-evenly;  /* 让内容上下左右等距 */
}
```

**禁止**用 `flex:1 + gap`(内容堆顶部,不撑开)。

### 3. 字号锁定(经验证可读 + 不重叠)

| 元素 | 字号 |
|------|------|
| 正文 seg-text | **22px** |
| 表格 td | **17px** |
| 表格 th | **16px** |
| KPI 数字 | **24px** |
| KPI 标签 | **15px** |
| seg-title-text | **22px** |
| comparison p | **16px** |
| conclusion | **20px** |
| footer-summary | **26px** |

### 4. footer-summary 用绿色背景框 + 26px 字号

```css
.footer-summary {
  color:#9AE8B4; font-size:26px; font-weight:900;
  background:linear-gradient(135deg, rgba(154,232,180,0.15), rgba(74,111,165,0.10));
  border:1.5px solid rgba(154,232,180,0.40);
  border-radius:10px;
  padding:12px 24px;
}
```

**作用**:画面视觉锚点,避免底部大块空白。

### 5. Playwright 启动参数(避免 dashboard 闪退)

```python
browser = p.chromium.launch(
    args=['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage',
          '--disable-software-rasterizer', '--disable-extensions'])
```

**禁止**加 `single-process` 或 `no-zygote`(会导致后续 context 失败)。

**每个图用独立 context + 渲染完立即关**,避免内存积累。

---

## 二、范式模块位置

`toolbox/templates/xhs_card_generator.py` —— **可直接 import 使用**

```python
from xhs_card_generator import render_n_cards, seg, kpi, table, timeline, compare, matrix

cards = [
    ('封面', '标题 1', '副标题 1', seg('段 1', '内容'), '锚点 1'),
    # ...
]
render_n_cards(cards, './output')
```

---

## 三、不要再踩的坑(从 11 版迭代总结)

1. ❌ **flex:1 + content-top**(我之前 8 版都栽这个)→ 内容堆顶部
2. ❌ **position:absolute 定位各区段** → 区段错位重叠
3. ❌ **grid-template-rows 用 1fr 不分配固定值** → 1fr 不撑开
4. ❌ **flex:1 + justify-content:center** → 内容在 block 中部居中,上下空白
5. ❌ **Playwright 用 single-process** → 第二个 context 立即挂
6. ❌ **杀 chrome 进程** → dashboard 闪退
7. ❌ **grid-template-rows: auto auto auto** → 不会填满,只占内容高度
8. ❌ **emoji 当图标 + 大标题 + 大空白**(反面教材,nexu-io 范式明确禁止)
9. ❌ **纯黑文字 + 蓝紫科技渐变**(廉价 AI 卡)
10. ❌ **每次重新写 CSS**(本次固化目的)

---

## 四、KIMI/豆包为什么不出这些问题

第三方 KIMI/豆包有**强模板系统**:
- 生成前**必读设计系统**(`card-design/SKILL.md`)
- 配色从**调色板文件**选一套锁定的,**整套卡片全程用它**
- 渲染后跑 **`card_audit.py` 硬门禁**脚本,确保不违规
- 一行 HTML 都不允许自己造颜色/字体

我们的范式**没有外部验证步骤**,所以容易退化。Eric 让我做的"内化范式",核心就是这个。

---

## 五、使用流程

1. Eric 让作图
2. **直接调用 `toolbox/templates/xhs_card_generator.py`**(不写新 CSS)
3. 内容用 `seg()` / `kpi()` / `table()` / `timeline()` / `compare()` / `matrix()` 辅助函数
4. 渲染输出 PNG

**禁止行为**:Eric 让作图时**不调范式直接写代码**。

---

## 六、版本

- v1.0(2026-10-06 12:30):综合 KIMI/豆包标准范式 + 金轩十文 9 图实战
