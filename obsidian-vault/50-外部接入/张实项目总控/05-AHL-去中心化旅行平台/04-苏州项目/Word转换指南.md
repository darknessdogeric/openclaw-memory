# 苏州项目Markdown转Word操作指南

## 方案一：使用Pandoc一键转换（推荐）

### 步骤1：安装Pandoc
1. 访问 https://pandoc.org/installing.html
2. 下载Windows安装包
3. 双击安装，记住安装路径

### 步骤2：批量转换脚本
将以下代码保存为 `convert-to-word.bat` 文件，放在苏州项目文件夹中运行：

```batch
@echo off
chcp 65001
echo ==========================================
echo  苏州项目Markdown转Word转换工具
echo ==========================================
echo.

set PANDOC_PATH=C:\Program Files\Pandoc\pandoc.exe
set SOURCE_DIR=%~dp0

echo 正在转换文件...
echo.

"%PANDOC_PATH%" "%SOURCE_DIR%01-完整方案书.md" -o "%SOURCE_DIR%01-完整方案书.docx" --toc --toc-depth=2
echo ✓ 01-完整方案书.docx 转换完成

"%PANDOC_PATH%" "%SOURCE_DIR%02-PPT结构大纲.md" -o "%SOURCE_DIR%02-PPT结构大纲.docx"
echo ✓ 02-PPT结构大纲.docx 转换完成

"%PANDOC_PATH%" "%SOURCE_DIR%03-需求清单.md" -o "%SOURCE_DIR%03-需求清单.docx"
echo ✓ 03-需求清单.docx 转换完成

"%PANDOC_PATH%" "%SOURCE_DIR%04-TOKEN成本分析.md" -o "%SOURCE_DIR%04-TOKEN成本分析.docx"
echo ✓ 04-TOKEN成本分析.docx 转换完成

echo.
echo ==========================================
echo  所有文件转换完成！
echo ==========================================
pause
```

### 步骤3：运行转换
双击 `convert-to-word.bat` 文件即可自动生成4个Word文档。

---

## 方案二：使用Python脚本转换

### 步骤1：安装依赖
```bash
pip install python-docx markdown
```

### 步骤2：使用转换脚本
我已为你创建 `md-to-docx.py` 脚本（见下文），运行：
```bash
python md-to-docx.py
```

---

## 方案三：在线工具转换

如果不想安装软件，可使用在线转换工具：

1. **CloudConvert**: https://cloudconvert.com/md-to-docx
2. **Vertopal**: https://www.vertopal.com/convert/md-to-docx
3. **Pandoc Try**: https://pandoc.org/try/

**操作步骤**：
1. 打开网页
2. 上传 `.md` 文件
3. 选择输出格式为 `.docx`
4. 下载转换后的文件

---

## 方案四：直接复制到Word

最简单的方法：
1. 用记事本打开 `.md` 文件
2. 全选复制 (Ctrl+A, Ctrl+C)
3. 粘贴到Word (Ctrl+V)
4. 在Word中调整格式（标题、表格等）

**格式调整建议**：
- `# 标题` → Word"标题1"样式
- `## 标题` → Word"标题2"样式
- `| 表格 |` → 转换为Word表格
- `**粗体**` → 应用加粗

---

## 转换后文件清单

转换完成后，你将有以下文件：

| 原文件 | Word版本 | 说明 |
|--------|---------|------|
| 01-完整方案书.md | 01-完整方案书.docx | 10章商务提案，约30页 |
| 02-PPT结构大纲.md | 02-PPT结构大纲.docx | 18页PPT结构+设计建议 |
| 03-需求清单.md | 03-需求清单.docx | 14项需求+团队替代映射 |
| 04-TOKEN成本分析.md | 04-TOKEN成本分析.docx | 成本测算+收费方案 |

---

## 推荐操作

**最快方式**：
1. 安装Pandoc（一次性）
2. 运行 `convert-to-word.bat`
3. 30秒内完成全部转换

**如果无法安装软件**：
- 使用在线转换工具逐个转换
- 或直接复制到Word手动调整

---

**需要帮助？** 告诉我你遇到的具体问题，我协助解决。


---

## 🔗 相关笔记

- [[工具-系统 MOC]]

*该区块由 B166ER 自动注入 (2026-07-28) — 关键词匹配*
