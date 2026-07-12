# OpenViking Token 压缩工作流

## 核心理念

用 **语义检索** 替代 **全量加载**，按需获取上下文。

## 工作流设计

### 1. 记忆分层结构

```
/user/eric/
  /preferences/     # 用户偏好、沟通风格
  /projects/        # 项目关键信息 (HAL、酒店等)
  /knowledge/      # 知识库摘要
  /tasks/           # 当前任务状态
```

### 2. 会话启动策略

| 场景 | 策略 |
|------|------|
| 日常对话 | 只加载 preferences + 当前任务 |
| 项目讨论 | 搜索相关项目记忆 |
| 新主题 | 按需加载知识库摘要 |

### 3. Token 压缩流程

```
用户提问 → 判断意图 → 搜索相关记忆 → 补充必要文件 → 回答
```

**不**: 加载所有文件到上下文
**而是**: 只加载搜索结果 + 关键引用

### 4. 会话结束策略

- 自动提取关键决策
- 更新相关记忆
- 标记待处理任务

## MCP 工具使用

```python
# 搜索相关上下文
search(query="用户当前项目", path="/user/eric/projects", limit=3)

# 添加记忆
add_memory(
  content="用户偏好简洁直接的沟通风格",
  path="/user/eric/preferences",
  tags=["communication", "style"]
)
```

## 启动检查

每次重要会话开始时，检查 OpenViking 可用性。
