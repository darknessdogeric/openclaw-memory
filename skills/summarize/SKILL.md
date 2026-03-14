---
name: summarize
description: >
  通用文本摘要技能，支持文章、论文、视频字幕、聊天记录等多种内容类型的智能摘要。
  支持抽取式摘要和生成式摘要，自动提取关键词、关键点和行动项。
  使用场景：(1) 长文章快速摘要，(2) 学术论文结构化摘要，(3) 视频字幕内容摘要，
  (4) 会议纪要提取，(5) 聊天记录整理。
---

# Summarize Skill - 文本摘要技能

通用文本摘要工具，支持多种内容类型的智能摘要。

## 功能特性

- ✅ **多类型支持**: 文章、论文、视频字幕、聊天记录
- ✅ **抽取式摘要**: 基于 TF-IDF 提取关键句子
- ✅ **生成式摘要**: 压缩重组关键信息
- ✅ **关键词提取**: 自动提取核心关键词
- ✅ **结构化输出**: JSON 格式，易于处理

## 安装依赖

```bash
pip install jieba
```

## 使用方法

### 命令行

```bash
# 文本摘要
python summarize.py "这是一段需要摘要的长文本..." -t text

# 论文摘要
python summarize.py paper.txt -t paper

# 视频字幕摘要
python summarize.py subtitles.srt -t video

# 聊天记录摘要
python summarize.py chat.txt -t chat

# 保存到文件
python summarize.py article.md -o summary.json
```

### Python API

```python
from summarize import TextSummarizer, PaperSummarizer, VideoSummarizer, ChatSummarizer

# 通用文本摘要
text = "你的长文本内容..."
summarizer = TextSummarizer(text)
summary = summarizer.summarize_extractive(ratio=0.3)
print(summary)

# 论文摘要
paper_text = "论文全文..."
paper_sum = PaperSummarizer(paper_text)
result = paper_sum.summarize()
print(result['summary'])

# 视频字幕摘要
subtitle = "字幕内容..."
video_sum = VideoSummarizer(subtitle)
result = video_sum.summarize()
print(result['content_summary'])
print(result['key_points'])

# 聊天记录摘要
chat = "聊天记录..."
chat_sum = ChatSummarizer(chat)
result = chat_sum.summarize()
print(result['summary'])
print(result['actions'])  # 行动项
```

## 摘要类型

### 1. 文本摘要 (text)

通用文本摘要，适用于文章、博客、报告等。

```python
summarizer = TextSummarizer(text, "text")
result = {
    'extractive': summarizer.summarize_extractive(ratio=0.3),  # 30% 长度
    'abstractive': summarizer.summarize_abstractive(max_length=200)
}
```

### 2. 论文摘要 (paper)

学术论文结构化摘要，自动提取各章节要点。

```python
summarizer = PaperSummarizer(paper_text)
result = summarizer.summarize()
# 返回:
# {
#   'type': 'paper',
#   'sections': {
#     'abstract': '...',
#     'introduction': '...',
#     'methodology': '...',
#     'results': '...',
#     'conclusion': '...'
#   },
#   'summary': '结构化摘要文本'
# }
```

### 3. 视频摘要 (video)

视频字幕内容摘要，提取关键知识点。

```python
summarizer = VideoSummarizer(subtitle_text)
result = summarizer.summarize()
# 返回:
# {
#   'type': 'video',
#   'original_duration': '约 150 句字幕',
#   'content_summary': '内容概述...',
#   'key_points': ['关键点1', '关键点2', ...]
# }
```

### 4. 聊天摘要 (chat)

聊天记录整理，提取讨论主题和行动项。

```python
summarizer = ChatSummarizer(chat_text)
result = summarizer.summarize()
# 返回:
# {
#   'type': 'chat',
#   'participants': ['张三', '李四'],
#   'topics': ['讨论主题1', '讨论主题2'],
#   'actions': ['行动项1', '行动项2'],
#   'summary': '格式化摘要'
# }
```

## 自动类型检测

如果不指定类型，会自动检测：
- 包含 "abstract" 或 "摘要" → 论文
- 包含时间戳格式 (00:00:00) → 视频字幕
- 包含 "用户名:" 格式 → 聊天记录
- 其他 → 普通文本

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-t, --type` | 摘要类型 | auto |
| `-r, --ratio` | 摘要比例 (0.1-0.5) | 0.3 |
| `-o, --output` | 输出文件 | 无 |

## 示例场景

### 场景1: 整理会议记录

```bash
python summarize.py meeting_notes.txt -t chat -o meeting_summary.json
```

输出包含：
- 参与者列表
- 讨论主题
- 行动项清单

### 场景2: 论文快速阅读

```bash
python summarize.py research_paper.pdf.txt -t paper
```

输出包含：
- 摘要、方法、结果、结论
- 各章节要点

### 场景3: 视频内容笔记

```bash
python summarize.py video_subtitles.srt -t video
```

输出包含：
- 内容概述
- 关键知识点列表

### 场景4: 文章摘要

```bash
python summarize.py article.md -t text -r 0.2
```

生成原文 20% 长度的摘要。

## 输出格式

所有输出为 JSON 格式，包含：
- `type`: 摘要类型
- 类型特定字段
- 结构化摘要文本

## 注意事项

1. 中文文本建议使用 UTF-8 编码
2. 长文本（>10000字）可能需要较长时间
3. 关键词提取需要 jieba 库
4. 论文摘要建议提供完整文本以获得更好效果

## 扩展开发

可以继承基类创建自定义摘要器：

```python
from summarize import TextSummarizer

class LegalDocumentSummarizer(TextSummarizer):
    def summarize(self):
        # 自定义法律文档摘要逻辑
        pass
```

## 更新日志

- v1.0 (2026-03-09): 初始版本
  - 支持 4 种摘要类型
  - 抽取式和生成式摘要
  - 自动类型检测
  - JSON 结构化输出
