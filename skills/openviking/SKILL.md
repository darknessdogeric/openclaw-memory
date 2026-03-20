# OpenViking Skill

**OpenViking** 是字节跳动火山引擎开源的 AI Agent 上下文数据库，专为 OpenClaw 等 AI Agent 平台设计。

## 功能概述

OpenViking 通过"文件系统范式"统一管理 AI Agent 所需的上下文（记忆、资源、技能），实现：

- 🗂️ **文件系统管理范式** - 统一组织记忆、资源、技能
- 📊 **分层上下文加载** - L0/L1/L2 三级结构，按需加载，显著节省 Token
- 🔍 **目录递归检索** - 结合目录定位与语义搜索，实现精准上下文获取
- 👁️ **可视化检索轨迹** - 可观察的上下文检索过程
- 🔄 **自动会话管理** - 自动压缩提取长期记忆，Agent 越用越聪明

## 与 OpenClaw 集成效果

根据官方测试数据（LoCoMo10 长对话数据集）：

| 实验组 | 任务完成率 | 输入 Token 成本 |
|--------|-----------|----------------|
| OpenClaw (原生记忆) | 35.65% | 24,611,530 |
| OpenClaw + LanceDB | 44.55% | 51,574,530 |
| **OpenClaw + OpenViking** | **52.08%** | **4,264,396** |

**提升效果**：
- 相比原生记忆：任务完成率提升 **43%**，Token 成本降低 **91%**
- 相比 LanceDB：任务完成率提升 **17%**，Token 成本降低 **92%**

## 安装要求

- Python 3.10+
- Go 1.22+ (构建 AGFS 组件)
- GCC 9+ 或 Clang 11+ (构建核心扩展)
- 操作系统：Linux / macOS / Windows

## 安装方法

### 1. Python 包安装

```bash
pip install openviking --upgrade --force-reinstall
```

### 2. Rust CLI 安装（可选）

```bash
# 使用安装脚本
curl -fsSL https://raw.githubusercontent.com/volcengine/OpenViking/main/crates/ov_cli/install.sh | bash

# 或从源码构建
cargo install --git https://github.com/volcengine/OpenViking ov_cli
```

## 配置说明

### 模型配置

OpenViking 需要以下模型能力：

1. **VLM 模型** - 用于图像和内容理解
2. **Embedding 模型** - 用于向量化和语义检索

支持的 VLM 提供商：

| 提供商 | 说明 | 获取 API Key |
|--------|------|-------------|
| `volcengine` | 火山引擎豆包模型 | [火山引擎控制台](https://console.volcengine.com/ark/) |
| `openai` | OpenAI 官方 API | [OpenAI Platform](https://platform.openai.com) |
| `litellm` | 统一访问第三方模型 | [LiteLLM Providers](https://docs.litellm.ai/docs/providers) |

### 服务器配置文件

创建配置文件 `~/.openviking/ov.conf`：

```json
{
  "storage": {
    "workspace": "/home/your-name/openviking_workspace"
  },
  "log": {
    "level": "INFO",
    "output": "stdout"
  },
  "embedding": {
    "dense": {
      "api_base": "<api-endpoint>",
      "api_key": "<your-api-key>",
      "provider": "<provider-type>",
      "dimension": 1024,
      "model": "<model-name>"
    },
    "max_concurrent": 10
  },
  "vlm": {
    "api_base": "<api-endpoint>",
    "api_key": "<your-api-key>",
    "provider": "<provider-type>",
    "model": "<model-name>",
    "max_concurrent": 100
  }
}
```

### 环境变量设置

**Linux/macOS:**
```bash
export OPENVIKING_CONFIG_FILE=~/.openviking/ov.conf
```

**Windows PowerShell:**
```powershell
$env:OPENVIKING_CONFIG_FILE = "$HOME/.openviking/ov.conf"
```

**Windows CMD:**
```cmd
set "OPENVIKING_CONFIG_FILE=%USERPROFILE%\.openviking\ov.conf"
```

## 快速开始

### 1. 启动服务器

```bash
openviking-server

# 后台运行
nohup openviking-server > /data/log/openviking.log 2>&1 &
```

### 2. 使用 CLI

```bash
# 查看状态
ov status

# 添加资源
ov add-resource https://github.com/volcengine/OpenViking

# 列出资源
ov ls viking://resources/

# 查看目录树
ov tree viking://resources/volcengine -L 2

# 语义搜索
ov find "what is openviking"

# 内容搜索
ov grep "openviking" --uri viking://resources/volcengine/OpenViking/docs/zh
```

### 3. VikingBot 快速开始

VikingBot 是基于 OpenViking 构建的 AI Agent 框架：

```bash
# 安装 VikingBot
pip install "openviking[bot]"

# 启动带 Bot 的服务器
openviking-server --with-bot

# 交互式聊天
ov chat
```

## 核心概念

### 1. 文件系统管理范式

OpenViking 将上下文统一映射到虚拟文件系统，通过 `viking://` 协议访问：

```
viking://
├── resources/     # 资源：项目文档、代码库、网页等
├── user/          # 用户：个人偏好、习惯等
└── agent/         # Agent：技能、指令、任务记忆等
```

### 2. 分层上下文加载

- **L0 (摘要)** - 一句话总结，用于快速检索识别
- **L1 (概览)** - 核心信息和使用场景，Agent 规划阶段使用
- **L2 (详情)** - 完整原始数据，必要时深度阅读

### 3. 目录递归检索策略

1. **意图分析** - 生成多个检索条件
2. **初始定位** - 向量检索快速定位高分目录
3. **精细探索** - 在目录内进行二次检索
4. **递归深入** - 子目录递归重复检索
5. **结果聚合** - 返回最相关的上下文

## OpenClaw 插件

OpenViking 提供专门的 OpenClaw 上下文插件，位于：

```
examples/openclaw-plugin/
```

使用该插件可显著提升 OpenClaw 的上下文管理能力和任务完成率。

## 项目信息

- **官网**: https://www.openviking.ai
- **文档**: https://www.openviking.ai/docs
- **GitHub**: https://github.com/volcengine/OpenViking
- **许可证**: Apache-2.0
- **Star 数**: 16.4k+
- **最新版本**: v0.2.9

## 社区

- 💬 Discord: https://discord.com/invite/eHvx8E9XF3
- 🐦 X (Twitter): https://x.com/openvikingai
- 📱 飞书群 / 微信群：参见官方文档

## 本地路径

```
C:\Users\Administrator\.openclaw\workspace\skills\openviking\
```

## 使用建议

1. **生产环境部署**：建议使用火山引擎 ECS + veLinux 操作系统
2. **模型选择**：推荐火山引擎豆包模型或 OpenAI 模型
3. **存储配置**：确保工作目录有足够的存储空间
4. **监控日志**：定期检查日志输出，优化检索效果
