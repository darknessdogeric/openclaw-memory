# 9 图均匀铺满范式 v2.0(基于金轩十文 9 图验证)

> **固化时间**:2026-10-06
> **范式来源**:金轩十文解读 9 图(v11 验证)
> **核心问题**:内容挤上半部分,下半空白
> **核心解决**:**整个画布 1440px 用 grid 4 行固定分配,seg-body 用 space-evenly 让内容段均匀分布**

---

## 一、4 区段严格分配(Grid 固定行高)

```css
.canvas {
  width:1080px; height:1440px;
  padding: 40px 56px 30px;
  display: grid;
  grid-template-rows: 70px 150px 1fr 170px;
  gap: 14px;
}
```

| 区段 | 高度 | 作用 |
|------|------|------|
| Zone 1 Header | 70px | tag + 页码 |
| Zone 2 Title | 150px | line1 (46px) + line2 (26px) + divider |
| Zone 3 Body | **1fr**(撑满) | 主内容,3-4 段均匀分布 |
| Zone 4 Footer | 170px | B 标 + 大字绿色锚点 summary |

**关键**:Zone 3 用 `1fr` 让内容**撑满剩余空间**,而不是固定高度(否则内容塞不下)。

---

## 二、Zone 3 内部"内容均匀铺满"关键

```css
.seg-body {
  background:rgba(255,255,255,0.04);
  border:1px solid rgba(212,167,116,0.20);
  border-radius:10px;
  padding:18px 20px;
  display:flex; flex-direction:column;
  justify-content: space-evenly;  /* 关键:让子段上下左右等距 */
  overflow:hidden;
}
```

`space-evenly` 是 Eric 反复要求的"上下左右等距"的**精确实现** —— 内容段自动均匀分布到整个 seg-body 区域。

---

## 三、每个内容段结构(2 段或 4 段)

每个内容段(`.seg`)的结构:
```
<div>
  <div class="seg-title-text">{标题}</div>
  {内容:表格 / KPI / 时间线 / 解读}
</div>
```

**每张卡放 2-4 个 seg**,数量根据内容多少定。

---

## 四、Footer 大字锚点(画面重心)

```css
.footer-summary {
  color:#9AE8B4; font-size:26px; font-weight:900;
  padding:12px 24px;
  background:linear-gradient(135deg, rgba(154,232,180,0.15), rgba(74,111,165,0.10));
  border:1.5px solid rgba(154,232,180,0.40);
  border-radius:10px;
  text-align:center;
}
```

**为什么需要**:即使 seg-body 内容不多,footer 大字锚点也能**填充画面底部**,避免下半空白。

---

## 五、不要再犯的错

- ❌ **不要用 flex:1 给 seg-body 让它撑满然后用 gap 让内容堆顶部** —— 必须用 justify-content: space-evenly
- ❌ **不要用 position:absolute 定位各区段** —— 容易产生区段错位
- ❌ **不要让 footer-summary 字号小于 24px** —— 它是画面锚点,必须够大
- ✅ **正确做法**:grid-template-rows 严格分配 4 行 + seg-body 用 space-evenly

---

## 六、范式核心代码(可直接复用)

```python
CSS = """
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body { width:1080px; height:1440px; overflow:hidden; ... }
  .canvas {
    width:1080px; height:1440px; padding: 40px 56px 30px;
    display: grid; grid-template-rows: 70px 150px 1fr 170px; gap: 14px;
  }
  .seg-body {
    display:flex; flex-direction:column; justify-content: space-evenly;
    padding:18px 20px;
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(212,167,116,0.20);
    border-radius:10px; overflow:hidden;
  }
  .footer-summary {
    color:#9AE8B4; font-size:26px; font-weight:900;
    background:linear-gradient(135deg, rgba(154,232,180,0.15), rgba(74,111,165,0.10));
    border:1.5px solid rgba(154,232,180,0.40);
    border-radius:10px; padding:12px 24px; text-align:center;
  }
"""

def card(tag, idx, total, l1, l2, body_html, footer_summary):
    return f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=1080,height=1440"><style>{CSS}</style></head>
<body><div class="bg"></div><div class="glow"></div>
<div class="canvas">
  <div class="seg-header"><span class="tag">{tag}</span><span class="page-num">{idx}/{total}</span></div>
  <div class="seg-title"><div class="line1">{l1}</div><div class="line2">{l2}</div></div>
  <div class="seg-body">{body_html}</div>
  <div class="seg-footer"><div class="footer-line">...</div><div class="footer-summary">{footer_summary}</div></div>
</div></body></html>'''
```

---

## 七、版本

- v1.0(2026-10-06 上午):基于前 10 版混乱迭代,4-zone Grid 基础范式
- **v2.0(2026-10-06 10:31):grid-template-rows 严格 4 行 + space-evenly 均匀分布 + footer 大字锚点**

**v2.0 是真验证后的版本**,从 v11(金轩十文 9 图)落地。
