# 4-Zone 信息图排版范式 v1.0(金轩十文 9 图验证)

> **固化时间**:2026-10-06
> **范式来源**:金轩十文解读 9 图卡(从 3 版迭代而来)
> **核心问题**:每张卡 block 内部内容撑不满,导致页面"挤顶部、底部空"

---

## 一、4 区段绝对定位范式

```
[0-50px]    padding-top
[50-80px]   Header (tag + 页码,30px 高)
[140-310px] Title 区 (170px:line1 + line2 + divider)
[330-1280px] Body 区 (950px,2 个 block,各 ~465px,20px gap)
[1280-1430px] Footer 区 (120px:B 标 + summary)
[1430-1440px] padding-bottom
```

用 absolute 定位,**不用 grid-template-rows**(避免 1fr 不撑开的陷阱)。

## 二、Block 内部三段式结构

每个 block 必须塞满 ~465px,结构是:
```
1. block-title (40px,标题)
2. 第一数据组件 (KPI 行/表格/解读,~150-180px)
3. 第二数据组件 (KPI 行/解读/表格,~80-120px)
4. conclusion 结论条 (50px,绿色背景,一句话总结)
```

**关键**:每张卡的每个 block 都必须有 conclusion 条,这是"撑满内容"的关键。

## 三、CSS 关键范式

```css
/* Body 区,2 个 block 等分 */
.z-body { position:absolute; top:330px; bottom:160px; left:60px; right:60px;
  display:flex; flex-direction:column; gap:20px; overflow:hidden; }
.block { flex:1; min-height:0;
  background:rgba(255,255,255,0.04); border:1px solid rgba(212,167,116,0.20);
  border-radius:10px; padding:18px 22px;
  display:grid; grid-template-rows: auto 1fr auto; gap:10px; }

/* 结论条(关键,撑满 block 内容) */
.conclusion { color:#9AE8B4; font-size:20px; font-weight:700; line-height:1.5;
  padding:10px 14px; background:rgba(154,232,180,0.08);
  border-left:3px solid #9AE8B4; border-radius:4px; }
```

## 四、不要再犯的错

- ❌ `flex:1` block + `justify-content:center` 内容居中 → 内容堆中部,block 上下空白
- ❌ `justify-content:space-between` block → 内容散到两端,中间空白
- ❌ `grid-auto-rows:1fr` block → 内容不撑满,block 内部留白
- ✅ **正确做法**:block 用 grid 三段式 + 第二个数据组件 + conclusion 条

## 五、可用工具函数(Python 模板)

```python
def card(tag, idx, total, l1, l2, body_html, footer_summary):
    return f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=1080,height=1440">
<style>{CSS}</style></head>
<body>
<div class="bg"></div><div class="glow"></div>
<div class="z-header"><div class="tag">{tag}</div><div class="page-num">{idx}/{total}</div></div>
<div class="z-title"><div class="line1">{l1}</div><div class="line2">{l2}</div><div class="divider"></div></div>
<div class="z-body">{body_html}</div>
<div class="z-footer">
  <div class="footer-line"><div class="b-mark">B166ER<span>出品 · 2026.10.06</span></div>
  <div class="b-right">金轩十文解读 · 酒店文旅AI</div></div>
  <div class="footer-summary">{footer_summary}</div></div>
</body></html>'''
```

## 六、组件清单

| 组件 | 高度参考 | 用途 |
|------|---------|------|
| `.kpi-row` (4 个 kpi) | ~80px | 数据高密度 |
| `.kpi` | 内部高 60px | 单个数据点 |
| `table` 5-6 行 | ~150-180px | 矩阵 / 对应关系 |
| `.compare` 3 列 | ~120-150px | 对比关系 |
| `.timeline` 3 行 | ~100-120px | 时间序列 |
| `.matrix` 6 行 | ~180px | 多维评分 |
| `.conclusion` | 50px | 撑满 + 一句话总结 |
| `.block-content` | 30-50px | 段落文字 |

**block 内容最少 = 标题 + 1 数据组件 + 结论 = ~270px,撑满 465px 还差 ~200px**,
**所以每张卡的每个 block 至少要 标题 + 2 数据组件 + 结论 = ~400px,撑满 ✓**

## 七、诊断方法

```python
# 检查 Zone 3 覆盖率
img = np.array(Image.open(png).convert('L'))
row_var = img.std(axis=1)
has_content = row_var > 5
coverage = has_content[330:1280].sum() / 950 * 100
# 目标:coverage > 60%,最大空白 < 80px
```

## 八、版本

- v1.0(2026-10-06):从金轩十文 9 图 5 版迭代而来,固化标准范式
