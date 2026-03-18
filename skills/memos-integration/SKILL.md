---
name: memos-integration
description: MemOS 记忆操作系统集成 - 为 OpenClaw 提供长期记忆能力
version: 1.0.0
---

# MemOS 集成配置

## 项目信息
- **项目名称**: MemOS
- **GitHub**: https://github.com/MemTensor/MemOS
- **文档**: https://memos-docs.openmem.net/
- **Stars**: 7.4k
- **版本**: v2.0.9 (星尘 Stardust)

## 部署状态
- **代码位置**: `C:\Users\Administrator\.openclaw\workspace\MemOS`
- **部署方式**: 本地 Python 部署 (Windows)
- **配置文件**: `.env`
- **启动脚本**: `start_windows.bat`

## 核心功能
MemOS 是一个为 LLM 和 AI Agent 设计的记忆操作系统：

1. **统一记忆 API** - 添加、检索、编辑、删除记忆
2. **多模态记忆** - 支持文本、图片、工具调用记录
3. **MemCube 知识库** - 多知识库管理，支持隔离和共享
4. **记忆调度器** - 异步处理，毫秒级延迟
5. **记忆反馈** - 自然语言修正和补充记忆
6. **OpenClaw 插件** - 官方生命周期插件支持

## 部署方式

### 方式 1: Docker (推荐，但需安装 Docker Desktop)
```bash
cd docker
docker-compose up
```

### 方式 2: Windows 本地 Python 运行
```bash
# 1. 安装依赖 (已完成)
pip install -r docker/requirements.txt

# 2. 配置 .env 文件 (需填写 API Key)

# 3. 启动服务
start_windows.bat
```

### 方式 3: 云端服务 (无需部署)
- 注册: https://memos-dashboard.openmem.net/
- 获取 API Key 直接使用

## 配置说明

### API Key 配置
编辑 `.env` 文件，配置以下 API Key:
- `OPENAI_API_KEY` - Kimi/其他 LLM API Key
- `MEMRADER_API_KEY` - 记忆读取模型 API Key
- `MOS_EMBEDDER_API_KEY` - Embedding 模型 API Key

### 数据库配置
- **Neo4j**: 图数据库，存储记忆关系 (默认 bolt://localhost:7687)
- **Qdrant**: 向量数据库，存储记忆向量 (默认 localhost:6333)

### 模型配置
当前配置使用 Moonshot Kimi API:
- Chat 模型: moonshot/kimi-k2.5
- Embedding 模型: text-embedding-v3
- API Base: https://api.moonshot.cn/v1

## 使用示例

### 添加记忆
```python
import requests

data = {
    "user_id": "user-123",
    "mem_cube_id": "cube-456",
    "messages": [{"role": "user", "content": "我喜欢草莓"}],
    "async_mode": "sync"
}

response = requests.post("http://localhost:8000/product/add", json=data)
```

### 搜索记忆
```python
data = {
    "query": "我喜欢什么",
    "user_id": "user-123",
    "mem_cube_id": "cube-456"
}

response = requests.post("http://localhost:8000/product/search", json=data)
```

## OpenClaw 集成

MemOS 提供官方 OpenClaw 插件:
- **云端插件**: https://github.com/MemTensor/MemOS-Cloud-OpenClaw-Plugin
- **本地插件**: https://www.npmjs.com/package/@memtensor/memos-local-openclaw-plugin

插件功能:
- 自动在 Agent 启动前召回记忆
- 对话结束后自动保存到 MemOS
- 支持多 Agent 记忆共享

## 资源链接
- **论文**: https://arxiv.org/abs/2507.03724
- **示例**: https://github.com/MemTensor/MemOS/tree/main/examples
- **Discord**: https://discord.gg/Txbx3gebZR
- **微信**: 见 GitHub README

## 注意事项
1. Windows 部署需要手动安装 Neo4j 和 Qdrant，或使用 Docker
2. 首次启动需要配置正确的 API Key
3. 默认端口 8000，确保未被占用
4. 生产环境建议使用 Docker 部署

## 下一步行动
- [ ] 安装 Docker Desktop (推荐)
- [ ] 或安装 Neo4j + Qdrant 本地服务
- [ ] 配置 API Key
- [ ] 启动 MemOS 服务
- [ ] 安装 OpenClaw 插件
