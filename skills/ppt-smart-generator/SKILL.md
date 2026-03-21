# PPT智能生成器 (ppt-smart-generator)

## 触发条件

当用户要求以下操作时自动触发：
- "生成PPT" / "做PPT" / "帮我做个演示"
- "把文档做成PPT" / "Word转PPT"
- "智能PPT" / "AI生成PPT"
- "配图PPT" / "带图的PPT"
- "banana-slides" / "香蕉幻灯片"

## 核心能力

### 1. AI大纲规划
- 分析输入内容（Word/文档/主题）
- 自动提取关键信息点
- 生成结构化PPT大纲
- 推荐合适的内容布局

### 2. 智能配图生成
- 调用AI生图接口（Flux/DALL-E/Midjourney）
- 为每个关键页面生成配图
- 支持风格定制（商务/科技/插画/摄影）
- 批量生成，自动匹配

### 3. PPT组装
- 多种模板风格可选
- 自动排版布局
- 动画效果添加
- 输出PPTX/HTML双格式

## 工作流程

```
用户输入 → AI分析大纲 → 配图生成 → PPT组装 → 输出交付
```

## 使用方法

### 基本命令
```
生成PPT: "帮我做一个关于XX的PPT"
风格指定: "商务风格PPT" / "科技感PPT"
配图要求: "生成带配图的PPT" / "需要图片"
文档转换: "把这个Word做成PPT"
```

### 参数选项
- `-t, --template`: 模板风格 (corporate/premium/startup/tech/minimal)
- `-s, --style`: 配图风格 (realistic/illustration/tech/abstract)
- `-o, --output`: 输出文件名
- `-l, --language`: 语言 (cn/en)

## 技术实现

### 依赖
- python-pptx: PPT文件生成
- openai/dalle: 图片生成 (可选)
- 风格模板系统

### 核心模块
1. `outline_planner.py` - AI大纲规划
2. `image_generator.py` - 配图生成 (模拟)
3. `ppt_assembler.py` - PPT组装
4. `template_manager.py` - 模板管理

## 输出示例

生成的PPT包含：
- 封面页
- 目录页
- 内容页（带配图）
- 数据图表页
- 总结页
- 结尾页

## 配置

在 `config.yaml` 中设置：
```yaml
default_template: premium
default_style: realistic
output_dir: ppt_output
image_count: 10
```

## 更新日志

- 2026-03-21: 初始版本
  - AI大纲规划
  - 模拟配图生成
  - 多模板支持
