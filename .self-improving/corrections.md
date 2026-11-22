# Corrections Log

## 2026-04-08

**Issue**: Emoji in Python scripts (`print("🔧 ...")`) caused `UnicodeEncodeError: 'gbk' codec can't encode character` on Windows
**Context**: local_semantic_search.py crashed 3 times before fixing
**Lesson**: Never use emoji in any script output on Windows. Always use ASCII alternatives.
**Applied**: 3x → Promote to HOT rule

**Issue**: Spent 40+ minutes trying to fix Jina API rate limit instead of implementing the already-known local fallback
**Context**: User asked "不升级jina api的话有没有免费替代方案" - I knew about model2vec+ChromaDB but hesitated
**Lesson**: When API has a clear rate limit problem, implement the backup immediately without prolonged analysis
**Applied**: 1x → Track

**Issue**: KB version cleanup only done when user asked, not proactively
**Context**: 50 versioned KB files (361KB wasted) accumulated over weeks
**Lesson**: Proactively maintain knowledge base, don't wait to be asked
**Applied**: 1x → Track

## 2026-11-17 · 误判本机无 Word/Office 引擎（已更正）

**错在哪**：要出公文 PDF，我只扫了 `C:\Program Files\Microsoft Office` 与 `C:\Program Files (x86)\Microsoft Office` 两个固定路径，没扫 `AppData`，也没查注册表，就断言"本机无 Word、无 LibreOffice"，并据此改用 Chromium 打印替代。Eric 直接驳回（"其他会话都生成了那么多文件了……没有word去装一个啊"）。

**真相**：**WPS Office 12.1.0.29690 已安装**在 `C:\Users\ericz\AppData\Local\Kingsoft\WPS Office`，且注册了 `Word.Application`（CLSID `{000209FF-0000-0000-C000-000000000046}`）与 `KWPS.Application`。`New-Object -ComObject Word.Application` 实测可启动（Version 12.0），可直接做 docx→PDF 高保真转换。真正的 Microsoft Word 未安装。

**代价**：多走了 Chromium 打印这条低保真弯路，并差点让公文标题字体被替换成手写体的方正舒体。

**规则（以后强制）**：
1. 探测 Windows 工具链，**必须同时查** ①注册表 `App Paths`（WINWORD/soffice/wps）②`HKCR` COM CLSID（Word.Application / KWPS.Application / wps.Application）③用户级安装目录（`AppData\Local\Kingsoft`、`AppData\Local\Programs`）④卸载清单 DisplayName。**判据优先用 `New-Object -ComObject Word.Application` 实测**，比找 exe 路径更硬更准。
2. **"没有就装一个"之前先确认是哪一种"没有"** —— WPS 的 Word COM 已覆盖 docx/pdf/xlsx 需求，装 LibreOffice/Office 属多余动作。
3. **做 PDF 交付前必须渲染首页看图质检**（pymupdf 渲染 PNG + view_image）：字体替换、标题折行、孤字、页码位置，只有看图才发现。
4. 公文类交付一律走 **Word/WPS 真引擎**导出 PDF，不接受浏览器打印替代（浏览器打印无字体子集嵌入、分页与 Word 不一致）。
5. WPS 的 Word COM **转换一份后可能自毁** → 每份文档重建 COM 实例；写含中文路径的 `.ps1` 必须 **UTF-8 with BOM**（PS 5.1 按 GBK 解析会报错）。

## 2026-11-17 · 公文版式手搓（已改为走自家排版器）

**错在哪**：出立项请示时**手搓**了一个 python-docx 生成器，只对齐了 AI-RMS 请示的表层（页边距、字号层级、缩进），没走我们自己的 `skills/gongwen-docx-cn`（GB/T 9704 + Eric 个人排版习惯，自带 `scripts/md2docx_gongwen.py`），也没走 `gongwen-report-cn` 的**请示类四段骨架**（一、事项／二、依据／三、方案与测算／四、请示事项）。结果：标题 20pt 宋体加粗（应为方正小标宋简体 22pt）、无固定 28 磅行距（用空行凑）、一级标题不加粗、自创十章结构、落款白名单没覆盖、金额写成中文数字。Eric 判定："扫描一下我们做了那么多公文范式，怎么还是这种。"

**代价**：返工一轮（重写正文结构、重排版式、改正数字用法），且中间还为"标题字体被替换成方正舒体"自作主张把标题改成宋体加粗 —— 那也偏离了范式（历史公文一律方正小标宋简体）。

**规则（以后强制）**：
1. **公文/报告/纪要/发言稿类文档，一律走 `skills/gongwen-docx-cn/scripts/md2docx_gongwen.py`**，输入 md 用纯文本（无 `#`、无行内 `**`、无 emoji、层级不跳级）。
2. **先定文种再写骨架**：请示＝主送机关＋四段骨架（一、事项／二、依据／三、方案与测算／四、请示事项）；汇报材料＝呈／拟／时间抬头＋五段骨架。骨架查 `gongwen-report-cn` 技能。
3. **动手前先扫描历史样本**：桌面 `给董事长的单独汇报/`、`重要文件/`、KB `07_战略与改革/` 的既有 docx 是范式真源，用 python-docx 抽字体/字号/行距/缩进/页边距做频次统计，再定版式。
4. **金额、比例、计数一律阿拉伯数字**（GB/T 9704 数字用法），公文里写"零点一五元""百分之十五"是外行。
5. **出稿后跑脚本化回读校验**（版式 + 字体 + 骨架序列 + Markdown 残留 + 关键内容），校验器留档可复跑；人工看版式必然漏项。
6. **不擅自偏离范式**：字体缺失是环境问题，按范式声明字体并如实报告渲染情况，不要私自换成"看起来更稳"的替代字体。
7. **默认不输出 PDF**，除非 Eric 明确要求。
