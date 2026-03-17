# AHL Document Generator CLI

基于CLI-Anything方法论构建的AHL项目文档生成工具。

## 功能
- 快速生成AHL项目各类文档（BP、路演材料、申报书）
- 基于模板自动填充内容
- 支持多格式输出（Markdown、PDF、Word）

## 安装
```bash
cd ahl-doc-generator/agent-harness
pip install -e .
```

## 使用
```bash
# 生成商业计划书
ahl-doc bp --template v3 --output ./output/

# 生成路演PPT
ahl-doc pitch --type investor --output ./output/

# 生成政府申报书
ahl-doc gov --region dali --output ./output/
```

## 命令结构
```
ahl-doc
├── bp          # 商业计划书生成
├── pitch       # 路演材料生成
├── gov         # 政府申报书生成
├── sop         # SOP文档生成
└── template    # 模板管理
```
