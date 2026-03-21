# 微信公众号推送 Skill

## 简介

通过微信公众号 API 自动推送消息到粉丝。

## 前置条件

1. 拥有微信公众号（订阅号/服务号）
2. 获取 AppID 和 AppSecret
3. 配置 IP 白名单（服务器出口 IP）

## 配置

在 `~/.openclaw/workspace/skills/wechat-mp/config.yaml` 中配置：

```yaml
wechat_mp:
  app_id: "your_app_id"
  app_secret: "your_app_secret"
```

## 可用工具

### 发送文本消息

```
send_wechat_text --message "内容" --user_id "openid"
```

### 发送模板消息

```
send_wechat_template --template_id "模板ID" --data "{...}" --user_id "openid"
```

### 获取用户列表

```
get_wechat_users
```

## 使用示例

```
send_wechat_text --message "你的AI助手有新消息：项目 HAL 已更新"
```

## 注意事项

- 需要微信公众号后台配置 IP 白名单
- 每天群发次数有限制
- 模板消息需要预先在公众号后台创建
