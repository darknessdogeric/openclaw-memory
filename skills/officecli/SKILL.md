---
name: officecli
description: OfficeCLI 单文件二进制 Office 文档读写：无需安装 Office 即可创建/读取/修改 docx、xlsx、pptx。触发：Office 文档读写、docx/xlsx/pptx 生成、免装 Office 环境。
---

# OfficeCLI — AI Agent Office Document Skill

> **Tool**: iOfficeAI/OfficeCLI v1.0.135  
> **Repo**: https://github.com/iOfficeAI/OfficeCLI  
> **Binary**: `D:\OfficeCLI-test\officecli.exe` (33MB, single file, no Office install)  
> **Wrapper**: `toolbox/officecli_skill.py`  
> **Installed**: 2026-07-13 | **Integrated**: 2026-07-14  
> **B166ER SKILL v1.0**

---

## What It Does

A single-binary CLI tool for AI agents to **create, read, modify**:
- `.pptx` (PowerPoint)
- `.docx` (Word)
- `.xlsx` (Excel)

No Microsoft Office or LibreOffice required. Built-in HTML rendering engine for visual feedback.

**Core value for B166ER**: Replace brittle `python-pptx` scripting with declarative slide creation. The agent can issue natural commands like "add a text shape to slide 3" without worrying about XML namespaces.

---

## Installation

```powershell
irm https://raw.githubusercontent.com/iOfficeAI/OfficeCLI/main/install.ps1 | iex
```

Binary is at `D:\OfficeCLI-test\officecli.exe`. Added to PATH (user scope).

---

## Commands That Work

| Command | Status | Notes |
|---------|:------:|-------|
| `create` | ✅ | Creates .pptx/.docx/.xlsx |
| `add` | ✅ | Adds slides, shapes, text, tables |
| `set` | ✅ | Modifies existing shapes |
| `remove` | ✅ | Removes slides or shapes |
| `save` | ✅ | Flushes to disk |
| `close` | ✅ | Closes resident session |
| `view html` | ✅ | HTML preview — **Chinese renders correctly** |
| `view png` | ⚠️ | PNG preview — sometimes garbled for Chinese |
| `view outline` | ❌ | Chinese garbled (UTF-16 LE conversion bug) |
| `raw` | ❌ | Chinese garbled (same bug) |

---

## Known Bug: Chinese Encoding

**Problem**: `view outline` and `raw` commands corrupt Chinese characters when reading back from .pptx files.

**Root cause**: OfficeCLI writes correct UTF-8 XML inside the .pptx zip archive, but its read-back path uses UTF-16 LE encoding that mishandles multi-byte Chinese characters.

**Impact**: TEXT EXTRACTION only. The actual file content is correct.

**Workaround** (used by B166ER wrapper):
```python
from pptx import Presentation
prs = Presentation("file.pptx")
for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame:
            print(shape.text_frame.text)  # ← correct Chinese
```

---

## B166ER Wrapper: `toolbox/officecli_skill.py`

### Quick Start

```python
from toolbox.officecli_skill import create_pptx, add_pptx_slide, add_pptx_text, verify_pptx, build_pptx

# High-level: build a deck from a slide spec
slides = [
    {"title": "封面标题", "subtitle": "副标题", "background": "0A0E27"},
    {"title": "第二页", "shapes": [
        {"text": "要点1", "x": "2cm", "y": "5cm", "size": 20, "bold": True}
    ]},
]
result = build_pptx("output.pptx", slides, verify=True)
print(result["ok"], result["verify"]["slide_count"])

# Low-level: step by step
create_pptx("test.pptx")
add_pptx_slide("test.pptx", title="Hello World")
add_pptx_text("test.pptx", 1, "中文内容", x="2cm", y="5cm")
save_pptx("test.pptx")
close_pptx("test.pptx")

# Verify (bypasses encoding bug)
verify_pptx("test.pptx")
```

### CLI Usage
```bash
python toolbox/officecli_skill.py --version
python toolbox/officecli_skill.py --verify file.pptx
python toolbox/officecli_skill.py --create new.pptx
```

---

## Real-World Test: D-day 等待期情报协议 v1.0

**Output**: `D:\OfficeCLI-test\b166er_outputs\dday_intel_protocol_v1.pptx`

**Result**: 5 slides, 48 text shapes, 0 errors, Chinese verified via python-pptx.

```python
from toolbox.officecli_skill import build_pptx

slides = [
    {"title": "D-day 等待期情报协议", "background": "0A0E27", ...},
    {"title": "时间窗口 T+1 ~ T+12", ...},
    {"title": "三方信号监控清单", ...},
    {"title": "7 个决策触发器", ...},
    {"title": "行动 SOP · 每晚 22:00 自检", ...},
]
build_pptx("output.pptx", slides, verify=True)
# → Build OK: True, 53 steps, 0 errors
```

---

## Comparison: officecli vs python-pptx

| Feature | officecli | python-pptx |
|---------|:---------:|:-----------:|
| Install | 33MB binary | pip + lxml dependencies |
| Chinese text | ✅ (creation) | ✅ |
| Read-back Chinese | ❌ (bug in view/raw) | ✅ |
| Declarative API | ✅ | ❌ (imperative XML-level) |
| HTML preview | ✅ | ❌ |
| Speed (simple deck) | ~15s | ~5s |
| Agent-friendly | ✅ (single binary) | ⚠️ (Python env required) |

**Verdict**: Use officecli for AGENT-DRIVEN creation (declarative, single binary). Use python-pptx for VERIFICATION (Read-back reliability). The `officecli_skill.py` wrapper does both.

---

## Integration into B166ER Workflows

### PPT Generation Pipeline
```
B166ER generates slide spec (JSON/MD)
    ↓
officecli_skill.build_pptx()
    ↓
officecli creates .pptx (declarative, fast)
    ↓
python-pptx verifies Chinese content
    ↓
watermark_tool.protect_output() (R12)
    ↓
→ Deliverable .pptx
```

### Known Integration Points
- AHL pitch decks (ppt-deck-builder-pro → officecli for rapid iteration)
- Hotel reports (Word → officecli .docx generation)
- Revenue dashboards (Excel → officecli .xlsx)
- B166ER 新媒体海报 (future: .pptx → PDF → image)

### Attention
- **R12 水印**: All visual outputs must go through `watermark_tool.protect_output()` after officecli creation
- **R29 主题**: Use B166ER V3 Brutalist theme (background: `#0A0E27`, accent: `#C8102E`) for B166ER-branded decks

---

## Upstream Watch

- **Repo**: https://github.com/iOfficeAI/OfficeCLI
- **Current**: v1.0.135 (2026-07-10)
- **Watch for**: Chinese encoding fix in `view`/`raw` commands
- **Backup binary**: `D:\OfficeCLI-test\officecli.exe.bak` (keep snapshot before each upgrade)
