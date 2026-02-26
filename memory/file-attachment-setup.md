# 文件接收配置指南

## 当前状态

**WebChat 渠道**: ✅ 已连接
**文件接收**: 需要确认配置

---

## OpenClaw 文件接收能力

### 支持文件的渠道

| 渠道 | 文件类型 | 大小限制 | 配置需求 |
|------|---------|---------|---------|
| **WebChat** | PDF, DOCX, TXT, 图片等 | ~10MB | `webchat.attachments.enabled` |
| Telegram | 所有类型 | 20MB | 原生支持 |
| Discord | 所有类型 | 25MB | 原生支持 |
| Slack | 所有类型 | 1GB | 原生支持 |

### WebChat 文件上传配置

需要在 `openclaw.json` 配置文件中启用：

```json
{
  "channels": {
    "webchat": {
      "enabled": true,
      "attachments": {
        "enabled": true,
        "maxSize": "10MB",
        "allowedTypes": ["pdf", "docx", "txt", "md", "jpg", "png"]
      }
    }
  }
}
```

---

## 快速测试

**请尝试以下操作**：

1. 在当前 WebChat 对话界面，应该能看到 **附件/文件上传按钮** (通常是一个回形针图标 📎)
2. 点击按钮，选择任意文件上传
3. 如果我能收到文件，我会回复确认

---

## 如果无法上传

请运行以下命令检查和启用：

```bash
# 检查当前配置
openclaw config get channels.webchat

# 启用文件附件（如需要）
openclaw config patch --json '{"channels":{"webchat":{"attachments":{"enabled":true}}}}'

# 重启 gateway
openclaw gateway restart
```

---

## 文件处理流程

一旦你发送文件给我：

```
你上传文件 → WebChat → OpenClaw Gateway → 我接收 → 我处理 → 我回复
```

**我能处理的文件类型**：
- 📄 **文档**: PDF, DOCX, DOC, TXT, MD
- 📊 **表格**: CSV, XLSX, XLS
- 📝 **代码文件**: JS, PY, JSON, XML, HTML, CSS 等
- 🖼️ **图片**: JPG, PNG, GIF (可通过 vision 模型分析)

**处理示例**：
- 上传商业计划书 PDF → 我提取内容并分析
- 上传 Excel 数据表 → 我分析数据并提供洞察
- 上传代码文件 → 我 review 代码并提出改进建议
- 上传图片 → 我通过 vision 模型识别内容

---

## 现在请测试

**直接在当前对话窗口点击文件上传按钮，发送任意文件给我**。我会确认是否接收成功。

如果界面没有文件上传按钮，或者上传失败，请告诉我具体报错信息，我会帮你排查。
