---
skill_id: "ppt-deep-generator"
title: "PPT深度生成器 (ppt-deep-generator)"
category: "PPT/演示"
description: "## 概述 高级PPT智能生成系统，支持深度排版、丰富背景、图形化数据展示。"
when_to_use: ""
size_kb: 1.4
refactored: "2026-06-24"
source: "skills/ppt-deep-generator/SKILL.md"
tags:
  - skills
  - PPT/演示
---

# PPT深度生成器 (ppt-deep-generator)

## 概述

高级PPT智能生成系统，支持深度排版、丰富背景、图形化数据展示。

## 核心系统

### 1. 背景系统 (BackgroundSystem)
- 纯色背景
- 渐变背景
- 网格图案
- 对角线纹理
- 强调色条

### 2. 排版系统 (TypographySystem)
- 主标题 (超大字号)
- 章节标签
- 段落标题
- 正文
- 标签/分类
- 大数字强调
- 项目符号列表

### 3. 图形元素 (GraphicElements)
- 卡片组件
- 统计卡片
- 对比框
- 时间线项目
- 进度条
- 头像/头像框

## 颜色系统

```
主色:
- primary: #111111 (纯黑)
- accent: #FFCC00 (亮黄)
- accent_red: #FF3333 (警示红)

背景:
- bg_white: #FFFFFF
- bg_gray: #F5F5F5
- bg_dark: #1A1A1A

功能色:
- success: #10B981
- warning: #F59E0B
- danger: #EF4444
- info: #3B82F6
```

## 模板风格

### NotebookLM/Swiss风格
- 网格系统布局
- 黄黑配色
- 超大Typography
- 极简留白
- 数据可视化

### 生成器

| 文件 | 功能 |
|------|------|
| notebooklm_gen.py | NotebookLM风格基础版 |
| advanced_gen.py | 深度排版增强版 |

## 使用方法

```bash
# 生成NotebookLM风格
python notebooklm_gen.py

# 生成高级版
python advanced_gen.py
```

## 输出

- PPTX格式文件
- 11页完整结构
- 专业设计可编辑
