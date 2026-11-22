# cn-pdf-local 设计参考

## 核心原则

**所有处理在 Eric 工作空间本地完成，不向任何云端上传任何文件。**

即使安全审计通过外部技能，本地技能永远是数据敏感的 Eric 文档处理的首选。

## 设计要点

### 1. 自动检测数字 vs 扫描

```
前 3 页平均字符数 / 页
├─ ≥ 50 → digital (有文字层)
├─ < 50 → scanned (无文字层,需 OCR)
└─ 0    → empty
```

启发式简单但 99% 准确（中国公文 PDF 一般都是数字型）。

### 2. 阅读顺序启发式（PyMuPDF blocks）

```python
blocks = page.get_text('blocks')
blocks_sorted = sorted(blocks, key=lambda b: (round(b[1] / 30), b[0]))
```

按 Y 坐标分桶（30 像素容差）→ 同行按 X 排序。**对单栏文件 100% 准确**，多栏需更复杂处理。

### 3. prettify 规则

- 去页码（`第 X 页` / `Page X` / 单独成行的数字）
- 多空行合一（≥3 个 → 2 个）
- 行尾空格去除

### 4. 表格 Markdown 化

直接用 Markdown 表格语法（`| --- |` 表头），非 HTML。可被 `gongwen-docx-cn` / `docx-md-bridge` 直接消费转 Word。

### 5. Sidecar JSON 用途

- 元数据（创建者、创建时间、页数）
- 每页原始文本（grep 用）
- 表格数据（程序化处理用）
- 工具状态（哪些工具可用）

## 升级路径

| 升级 | 触发条件 | 工作量 |
|------|---------|--------|
| 接入本地 paddleocr 二进制 | 扫描 PDF OCR 精度不够 | 中 |
| 接入 `pymupdf4llm` | 多栏阅读顺序需提升 | 低 |
| 接入 `marker-pdf` | 需要公式 + 图表全栈 | 高 |
| 加云端可选层 | 用户同意特定场景使用 | 中 |
