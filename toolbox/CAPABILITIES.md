# B166ER 环境能力清单 (CAPABILITIES)

> **建立**：2026-10-02（Eric 要求"系统解决工具可用性问题"）
> **位置**：`toolbox/CAPABILITIES.md`
> **用途**：**接到任何文档/图片生成任务前，先读本文件**。禁止假设"没有工具"。

---

## 一、执行环境（2026-10-02 实测）

| 组件 | 状态 | 版本/路径 |
|---|---|---|
| **exec** | ✅ 可用 | OpenClaw exec 工具（一直在，别再说没有） |
| **Python** | ✅ | 3.14.3 · `C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe` |
| **pip** | ✅ | 同目录 `Scripts\pip.exe` |
| **Node** | ✅ | v24.18.0 |
| **.NET SDK** | ✅ | **8.0.425**（`C:\Program Files\dotnet\dotnet.exe`） |
| **npx** | ✅ | 可用 |

## 二、Python 文档/图像库（全部已装）

| 库 | 版本 | 用途 |
|---|---|---|
| **python-docx** | **1.2.0** | ⭐ **Word 生成/编辑/格式化**（不用再手拼 XML！） |
| **python-pptx** | **1.0.2** | ⭐ PowerPoint 生成/编辑 |
| **openpyxl** | **3.1.5** | ⭐ Excel 生成/编辑 |
| **Pillow** | **12.3.0** | 图像处理/水印/合成 |
| **lxml** | **6.1.3** | XML 处理 |
| **Markdown** | **3.10.2** | Markdown → HTML |
| **markdown_pdf** | **1.13.2** | Markdown → PDF |
| **markdownify** | **1.2.2** | HTML → Markdown |
| **playwright** | **1.58.0** | ⭐ 无头浏览器（HTML→PNG/PDF） |
| **playwright-stealth** | 2.0.2 | 反检测 |
| **invisible-playwright** | 0.2.0 | 隐身模式 |

## 三、浏览器/渲染引擎

| 引擎 | 状态 | 路径 |
|---|---|---|
| **Playwright Chromium** | ✅ 已装 | `C:\Users\ericz\AppData\Local\ms-playwright\chromium-1208\chrome-win64\chrome.exe` |
| **Edge headless** | ✅ 可用 | `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe` |
| **Playwright CLI** | ✅ | npx playwright 1.59.1 |

## 四、缺失项

| 组件 | 状态 | 影响 | 解决方案 |
|---|---|---|---|
| **.NET SDK 8.0.425** | ✅ **已装**（2026-10-02）| `minimax-docx` 技能的 C# 原生路径（OpenXML SDK）**已可用** | 已构建 `MiniMaxAIDocx.Cli`（0 错误）|

---

## 五、标准调用路径（★ 硬规则 ★）

### A. Word 文档（.docx）

**禁止**手拼 XML。**必须**用 `python-docx`：

```python
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
# 设置页面（GB/T 9704 示例）
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)   # A4
sec.top_margin, sec.bottom_margin = Cm(3.7), Cm(3.5)
sec.left_margin, sec.right_margin = Cm(2.8), Cm(2.6)

# 中文正文（仿宋_GB2312 三号=16pt）
p = doc.add_paragraph()
run = p.add_run('正文内容')
run.font.size = Pt(16)
run.font.name = 'Times New Roman'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '仿宋_GB2312')
p.paragraph_format.first_line_indent = Pt(32)   # 2 字符
p.paragraph_format.line_spacing = Pt(28)        # 固定 28pt

doc.save(r'C:\path\to\out.docx')
```

**现成封装**：`toolbox/anyi_reports/docx_gongwen.py`（安逸集团公文模版，GB/T 9704）

### B. HTML → PNG（海报/信息图）

**禁止**手写 Node/Edge 脚本。**必须**用 `playwright`：

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':1080,'height':1440}, device_scale_factor=2)
    pg.goto(f'file:///{html_path}')
    pg.wait_for_timeout(1500)
    pg.screenshot(path=png_path, clip={'x':0,'y':0,'width':1080,'height':1440})
    b.close()
```

**现成封装**：`toolbox/anyi_reports/html_to_png.py`

### C. Excel / PPT

- Excel：`openpyxl.load_workbook()` / `Workbook()`
- PPT：`pptx.Presentation()`

### D. PDF

- Markdown → PDF：`markdown_pdf` 或 `markdown` + playwright print-to-pdf
- 直接改 PDF：`pypdf`（若装）

---

## 六、现有范式资产（优先复用，勿重造）

| 资产 | 路径 | 用途 |
|---|---|---|
| **安逸公文生成器** | `toolbox/anyi_reports/docx_gongwen.py` | GB/T 9704 公文 docx |
| **HTML→PNG 渲染器** | `toolbox/anyi_reports/html_to_png.py` | 海报/信息图出 PNG |
| **海报模板系统 v3** | `poster_templates/v3/` | HTML+CSS 海报 → Playwright 出图 |
| **海报模板系统 v1** | `poster_templates/` (5 套) | 路演/产品/朋友圈/名片/酒店 |
| **minimax-docx 技能** | `skills/minimax-docx/` | C# OpenXML 全套（需 .NET）|
| **minimax-pdf 技能** | `skills/minimax-pdf/` | 高设计感 PDF |
| **minimax-xlsx 技能** | `skills/minimax-xlsx/` | Excel 生成 |
| **article-to-infographic** | `skills/article-to-infographic/` | 文章 → 信息图 |
| **lh-html-to-image** | `skills/lh-html-to-image/` | HTML→图 |
| **docx-inplace-edit** | `skills/docx-inplace-edit/` | 就地编辑 docx |
| **docx-md-bridge** | `skills/docx-md-bridge/` | docx ↔ markdown |
| **gongwen-docx-cn** | `skills/gongwen-docx-cn/` | 中文公文 docx |

---

## 七、任务前检查清单（硬规则）

接到"生成文档/图片"任务时，**先**执行：

1. **读本文件**（`toolbox/CAPABILITIES.md`）
2. **查现有范式**（`grep` 关键词在 `toolbox/`、`skills/`、`poster_templates/`）
3. **确认目标格式**（docx / pptx / xlsx / png / pdf）
4. **选对应标准路径**（§五）
5. **禁止**：手拼 XML / 手写渲染脚本 / 假设工具不存在

---

*B166ER · 2026-10-02 · 能力清单 v1.0*
*修正历史错误：2026-10-02 前误判本机缺 exec/python-docx/playwright，实际全有*

---

## 八、图片识别（OCR）— 2026-10-02 新增

| 组件 | 状态 |
|---|---|
| **Tesseract-OCR** | ✅ `C:\Program Files\Tesseract-OCR\tesseract.exe`（Program Files 不可写）|
| **用户级 tessdata** | ✅ `C:\Users\ericz\tessdata\`（chi_sim / chi_sim_vert / eng / osd）|
| **pytesseract** | ✅ 已装 |
| **封装模块** | `toolbox/anyi_reports/ocr_image.py` |

### 用法

```python
import sys; sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace\toolbox')
from anyi_reports.ocr_image import ocr_image, ocr_to_file, ocr_pdf

text = ocr_image('截图.png')                       # 中英混合（默认）
text = ocr_image('截图.png', lang='chi_sim')       # 纯中文
ocr_to_file('截图.png', 'out.txt')                 # 写文件
ocr_pdf('报告.pdf', 'out.txt')                     # PDF 逐页 OCR
```

**关键**：必须先 `os.environ['TESSDATA_PREFIX'] = r'C:\Users\ericz\tessdata'`（模块内已自动设置）

---

## 九、视觉模型（看图）— 2026-10-02 修复

| 项 | 状态 |
|---|---|
| **image fallbacks（修复前）** | ❌ 0 个（导致三家默认视觉模型全挂）|
| **image fallbacks（修复后）** | ✅ 3 个：`codex/gpt-5.5` · `kimi-code/kimi-for-coding` · `codex/gpt-5.4-mini` |
| **view_image 工具** | ✅ 已实测可用 |

### 管理命令

```bash
openclaw models image-fallbacks list              # 查看
openclaw models image-fallbacks add <model>       # 添加
openclaw models image-fallbacks remove <model>    # 移除
openclaw models image-fallbacks clear             # 清空
```

### Provider 状态（2026-10-02 12:20 更新）

| Provider | 状态 | 处理 |
|---|---|---|
| `deepseek:default` | ✅ 正常 | — |
| `minimax:cn` | ✅ auth 正常（VL 有 Token Plan 上限）| 视觉走 codex/kimi |
| `anthropic:models-json` | ✅ 无 cooldown（已重排为优先）| **免费已修** |
| `anthropic:default` | ⚠️ auth cooldown（key 失效）| 已降为次选；如需修复须重认证 |
| `moonshot:default` | ⚠️ billing disabled（10-02 00:40 已到期，应自动恢复）| 观察 |
| `minimax-portal` | ⚠️ 用 env MINIMAX_API_KEY（同 minimax:cn）| 观察 |

**免费修复（已做）**：
```bash
# 重排 anthropic profile 顺序（models-json 优先）
openclaw models auth order set --agent main --provider anthropic anthropic:models-json anthropic:default
```

**需花钱（Eric 决定，默认跳过）**：
- minimax Token Plan 升级/买积分
- moonshot 充值

> 视觉能力不受影响——已用 codex/kimi 顶上。
