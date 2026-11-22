# DeepSeek API 配置指南

## 步骤1：获取 DeepSeek API Key

1. 访问 https://platform.deepseek.com/
2. 注册或登录账户
3. 进入 API 密钥管理页面
4. 创建新的 API Key
5. 复制 API Key（格式通常为 sk-xxxxxxxx）

## 步骤2：配置环境变量

### 方式1：创建 .env 文件（推荐）

在 `ai-homestay-system/backend/` 目录下创建 `.env` 文件：

```
DEEPSEEK_API_KEY=sk-your_actual_api_key_here
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_API_BASE=https://api.deepseek.com/v1
DEEPSEEK_MAX_TOKENS=500
DEEPSEEK_TEMPERATURE=0.7
FLASK_ENV=development
```

### 方式2：设置系统环境变量

**Windows 用户：**

1. 打开 "系统属性" -> "环境变量"
2. 点击 "新建" 添加用户变量
3. 变量名：`DEEPSEEK_API_KEY`
4. 变量值：`sk-your_actual_api_key_here`
5. 点击确定并重启 Python 应用

**或在 CMD 中临时设置：**

```bash
set DEEPSEEK_API_KEY=sk-your_actual_api_key_here
python main.py
```

## 步骤3：验证配置

运行诊断脚本：

```bash
cd D:\文旅agent\文旅项目2\ai-homestay-system\backend
python test_deepseek.py
```

## 常见问题

**Q: 如何获取 DeepSeek API Key？**
A: 访问 https://platform.deepseek.com/ 注册账户并创建 API Key

**Q: API Key 格式是什么？**
A: 通常以 `sk-` 开头，后跟一长串字符

**Q: 如何测试 API 是否正常工作？**
A: 运行 `python test_deepseek.py` 进行测试

**Q: 如果 API 调用失败怎么办？**
A: 系统会自动使用本地模拟回答作为备用方案


---

## 🔗 相关笔记

- [[AHL 平台 MOC]]
- [[AI-Agent MOC]]

*该区块由 B166ER 自动注入 (2026-07-28) — 关键词匹配*
