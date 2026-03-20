---
name: memos-cloud-integration
description: MemOS Cloud 记忆系统集成 - 为 OpenClaw 提供云端长期记忆能力
version: 1.0.0
---

# MemOS Cloud 集成配置

## 配置信息

- **API Key**: mpg-TwuyRqeYUEeZky2IVrRodWlNYqb4k6nl4Ure8b1F
- **Endpoint**: https://api.openmem.net
- **User ID**: ericzhangshi@163.com
- **MemCube ID**: default

## 功能开关

- **Auto Recall**: ✅ 启用 - 对话前自动召回相关记忆
- **Auto Save**: ✅ 启用 - 对话后自动保存记忆

## 配置文件位置

`C:\Users\Administrator\.openclaw\openclaw.json`

```json
"plugins": {
  "entries": {
    "memos-cloud": {
      "enabled": true,
      "config": {
        "apiKey": "mpg-TwuyRqeYUEeZky2IVrRodWlNYqb4k6nl4Ure8b1F",
        "endpoint": "https://api.openmem.net",
        "userId": "ericzhangshi@163.com",
        "memCubeId": "default",
        "autoRecall": true,
        "autoSave": true
      }
    }
  }
}
```

## 使用方式

### 1. 重启 OpenClaw

```powershell
openclaw gateway restart
```

### 2. 测试记忆功能

**测试 1 - 保存记忆:**
```
用户: 我喜欢草莓
```

**测试 2 - 召回记忆 (新会话):**
```
用户: 我喜欢什么？
AI: 根据之前的记忆，你喜欢草莓。
```

## API 直接调用

如果需要直接调用 MemOS Cloud API：

### 添加记忆
```bash
curl -X POST https://api.openmem.net/product/add \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer mpg-TwuyRqeYUEeZky2IVrRodWlNYqb4k6nl4Ure8b1F" \
  -d '{
    "user_id": "ericzhangshi@163.com",
    "mem_cube_id": "default",
    "messages": [{"role": "user", "content": "我喜欢草莓"}]
  }'
```

### 搜索记忆
```bash
curl -X POST https://api.openmem.net/product/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer mpg-TwuyRqeYUEeZky2IVrRodWlNYqb4k6nl4Ure8b1F" \
  -d '{
    "query": "我喜欢什么",
    "user_id": "ericzhangshi@163.com",
    "mem_cube_id": "default"
  }'
```

## 功能特性

1. **长期记忆** - 跨会话保持记忆
2. **语义搜索** - 智能召回相关记忆
3. **记忆图谱** - 记忆之间的关系存储
4. **记忆反馈** - 自然语言修正记忆
5. **多知识库** - 支持多个 MemCube

## 限制

- 免费版每月 1000 次 API 调用
- 超出后需要付费升级

## 资源链接

- **控制台**: https://memos-dashboard.openmem.net/
- **文档**: https://memos-docs.openmem.net/
- **GitHub**: https://github.com/MemTensor/MemOS

## 状态

- ✅ 配置完成
- ⏳ 等待 OpenClaw 重启后生效
