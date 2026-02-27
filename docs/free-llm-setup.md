# Free LLM API 配置指南

> 配置日期: 2026-02-14  
> 来源: https://github.com/cheahjs/free-llm-api-resources

---

## 已配置的免费模型

### 1. OpenRouter (推荐)
**特点**: 无需注册即可使用免费模型，限制 20 req/min, 50 req/day

| 模型别名 | 模型ID | 特点 |
|---------|--------|------|
| `Kimi-Free` | moonshotai/kimi-k2:free | 长上下文 256K，中文强 |
| `Llama-Free` | meta-llama/llama-3.3-70b-instruct:free | Meta最新，通用能力强 |
| `Qwen-Coder` | qwen/qwen3-coder:free | 代码能力强 |
| `DeepSeek-R1` | deepseek/deepseek-r1-0528:free | 推理模型，数学逻辑强 |

**API Key**: 需要在 https://openrouter.ai/keys 注册获取

---

### 2. Google AI Studio
**特点**: Gemini 系列，需要 Google 账号，有地区限制

| 模型别名 | 模型ID | 特点 |
|---------|--------|------|
| `Gemini-Flash` | gemini-2.5-flash | 100万上下文，速度极快 |
| `Gemma-27B` | gemma-3-27b-it | Google开源，本地可部署 |

**API Key**: https://aistudio.google.com/app/apikey

---

### 3. Cerebras
**特点**: 速度极快，限制 30 req/min, 14400 req/day

| 模型别名 | 模型ID | 特点 |
|---------|--------|------|
| `Cerebras-Llama` | llama-3.3-70b | 推理速度最快 |
| `Cerebras-Qwen` | qwen-3-32b | 中文优化 |

**API Key**: https://cloud.cerebras.ai/

---

### 4. GitHub Models
**特点**: 需要 GitHub 账号，速率限制较低

| 模型别名 | 模型ID | 特点 |
|---------|--------|------|
| `GPT4o-Mini` | gpt-4o-mini | OpenAI小模型，成本低 |

**API Key**: https://github.com/settings/tokens

---

## 快速切换模型

### 方法1: 命令行切换
```bash
# 查看可用模型
openclaw models list

# 切换模型
openclaw session model Kimi-Free
openclaw session model Llama-Free
openclaw session model DeepSeek-R1
```

### 方法2: 对话中切换
```
/model Kimi-Free
/model Gemini-Flash
/model Cerebras-Llama
```

### 方法3: 临时指定
```
使用 DeepSeek-R1 分析这个问题...
```

---

## API Key 配置

### 设置环境变量 (推荐)
在 `~/.bashrc` 或 `~/.zshrc` 中添加:

```bash
# OpenRouter (必须)
export OPENROUTER_API_KEY="your-key-here"

# Google AI Studio (可选)
export GOOGLE_AI_STUDIO_API_KEY="your-key-here"

# Cerebras (可选)
export CEREBRAS_API_KEY="your-key-here"

# GitHub Models (可选)
export GITHUB_TOKEN="your-token-here"
```

### Windows PowerShell
```powershell
[Environment]::SetEnvironmentVariable("OPENROUTER_API_KEY", "your-key", "User")
```

---

## 模型选择建议

| 场景 | 推荐模型 | 原因 |
|------|---------|------|
| 日常对话 | `Kimi-Free` | 中文好，上下文长 |
| 代码编写 | `Qwen-Coder` | 专门优化代码 |
| 复杂推理 | `DeepSeek-R1` | 推理模型，思维链 |
| 长文档分析 | `Gemini-Flash` | 100万上下文 |
| 速度优先 | `Cerebras-Llama` | 推理速度最快 |
| 英文内容 | `Llama-Free` | Meta原版，英文强 |

---

## 注意事项

1. **速率限制**: 免费模型有请求频率限制，超额会报错
2. **稳定性**: 免费服务可能不稳定，建议配置多个备选
3. **隐私**: 部分服务(OpenRouter)可能会记录数据用于改进
4. **地区限制**: Google AI Studio 在某些地区不可用

---

## 故障排查

### 模型切换失败
检查 API Key 是否设置:
```bash
echo $OPENROUTER_API_KEY
```

### 请求被限制
切换备用模型:
```
/model Cerebras-Llama
```

### 模型无响应
检查网络连接，或尝试重启 gateway:
```bash
openclaw gateway restart
```
