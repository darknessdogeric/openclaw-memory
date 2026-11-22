# anyi_reports — 安逸集团文档生成标准工具箱

> **建立**：2026-10-02（Eric 要求系统解决工具可用性）
> **原则**：**接到文档任务先来这里，不要手拼 XML / 不要手写渲染脚本**

## 模块

| 模块 | 用途 | 依赖 |
|---|---|---|
| **docx_gongwen.py** | Word 公文生成（GB/T 9704-2012 标准）| python-docx 1.2.0 |
| **html_to_png.py** | HTML → PNG/PDF 渲染（海报/信息图）| playwright 1.58.0 |

## 快速上手

### Word 公文

```python
import sys
sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace\toolbox')
from anyi_reports.docx_gongwen import GongwenDoc

d = GongwenDoc(title='安逸集团XXX方案', author='张实（Eric）', date='2026-10-02')
d.h1('一、背景')
d.body('正文段落...')          # 自动首行缩进 2 字符 + 仿宋 16pt + 行距 28pt
d.h2('（一）子项')
d.table(headers=['列1','列2'], rows=[['a','b']], caption='表1 示例')
d.signature('安逸酒店集团产业发展部')
d.save(r'C:\Users\ericz\Desktop\out.docx')
```

### HTML → PNG

```python
import sys
sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace\toolbox')
from anyi_reports.html_to_png import render_html, render_batch

render_html('poster.html', 'poster.png', width=1080, height=1440)   # 2x 高清
render_batch([
    ('p1.html', 'p1.png', 1080, 1080),
    ('p2.html', 'p2.png', 1080, 1440),
])
```

CLI：
```bash
python toolbox/anyi_reports/html_to_png.py in.html out.png 1080 1440
```

## GB/T 9704 标准参数（内置，勿改）

| 项 | 值 |
|---|---|
| 页 | A4 21×29.7cm |
| 边距 | 上37mm 下35mm 左28mm 右26mm |
| 正文 | 仿宋_GB2312 三号(16pt) 固定行距28pt 首行缩进2字符 |
| 一级标题 | 黑体 三号(16pt) |
| 二级标题 | 黑体 三号(16pt) |
| 标题 | 方正小标宋简体 二号(22pt) |
| 表格 | 三线表（顶/底1.5pt，表头下0.75pt，无竖线）|
| 页码 | 宋体 四号(14pt) -X- 格式 |

## 相关范式（优先复用）

| 资产 | 路径 |
|---|---|
| 海报模板系统 v3 | `poster_templates/v3/` |
| 海报模板系统 v1（5套）| `poster_templates/` |
| 环境能力清单 | `toolbox/CAPABILITIES.md` |

---
*B166ER · 2026-10-02*
