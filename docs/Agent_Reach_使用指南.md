# Agent Reach 使用指南

> **安装时间**: 2026年2月27日  
> **版本**: 1.2.0  
> **来源**: https://github.com/Panniantong/Agent-Reach

---

## ✅ 安装状态

**核心包**: agent-reach 1.2.0 ✅ 已安装  
**位置**: C:\Python314\Lib\site-packages  
**依赖状态**:
- ✅ feedparser - RSS解析
- ✅ requests - HTTP请求
- ✅ pyyaml - YAML配置
- ✅ yt-dlp 2026.02.21 - 视频下载/字幕提取
- ✅ loguru - 日志
- ✅ rich - 终端美化

---

## 🌐 可用功能

### 无需配置 (装好即用)

| 功能 | 命令示例 | 说明 |
|------|----------|------|
| **网页阅读** | `curl https://r.jina.ai/http://example.com` | 任意网页转Markdown |
| **YouTube字幕** | `yt-dlp --dump-json "URL"` | 提取视频信息 |
| **YouTube下载** | `yt-dlp --write-sub --skip-download "URL"` | 下载字幕 |
| **RSS订阅** | Python feedparser库 | 解析RSS/Atom |
| **B站视频** | `yt-dlp "URL"` | 支持B站 |

### 需要配置

| 功能 | 配置方式 | 说明 |
|------|----------|------|
| **Twitter/X** | Cookie登录 | 读推文、搜索 |
| **小红书** | Docker MCP服务 | 阅读、搜索、发帖 |
| **抖音** | MCP服务 | 视频解析、无水印下载 |
| **Reddit** | 代理配置 | 搜索、读帖 |
| **GitHub** | gh CLI认证 | 私有仓库、Issue/PR |
| **LinkedIn** | MCP服务 | Profile、职位搜索 |
| **全网搜索** | Exa MCP | AI语义搜索 |

---

## 🚀 快速使用

### 1. 阅读任意网页

```bash
# 方法1: Jina Reader (推荐)
curl https://r.jina.ai/http://example.com

# 方法2: Python requests
python -c "import requests; print(requests.get('https://r.jina.ai/http://example.com').text)"
```

### 2. YouTube/B站视频字幕

```bash
# 提取视频信息
yt-dlp --dump-json "https://youtube.com/watch?v=VIDEO_ID"

# 提取字幕
yt-dlp --write-sub --skip-download "https://youtube.com/watch?v=VIDEO_ID"

# B站同样适用
yt-dlp --dump-json "https://bilibili.com/video/BVxxx"
```

### 3. RSS订阅

```python
import feedparser
feed = feedparser.parse('https://example.com/feed.xml')
for entry in feed.entries[:5]:
    print(entry.title, entry.link)
```

---

## 🔧 高级配置

### 配置Twitter/X

1. 安装Chrome插件: Cookie-Editor
2. 登录Twitter
3. 导出Cookie
4. 配置:
```bash
agent-reach configure twitter-cookies "your_cookies_json"
```

### 配置代理 (服务器需要)

```bash
agent-reach configure proxy http://user:pass@ip:port
```

---

## 💡 使用场景示例

### 场景1: 研究竞品
```bash
# 读取竞品网站
curl https://r.jina.ai/https://competitor.com

# 搜索相关讨论
# (需要配置Twitter/Reddit后)
```

### 场景2: 学习内容
```bash
# YouTube教程转文字
yt-dlp --write-sub --skip-download "https://youtube.com/watch?v=教程ID"

# B站技术视频
yt-dlp --write-sub --skip-download "https://bilibili.com/video/BVxxx"
```

### 场景3: 监控信息
```python
# RSS订阅行业资讯
import feedparser
feed = feedparser.parse('https://www.traveldaily.cn/rss')
```

---

## ⚠️ 注意事项

1. **Cookie安全**: Twitter/小红书等平台需要使用Cookie登录，建议用小号
2. **代理配置**: 服务器IP可能被Reddit等平台封锁，需要配置住宅代理
3. **本地 vs 服务器**: 本地电脑通常不需要代理，服务器需要
4. **封号风险**: 使用Cookie的平台存在被检测风险，注意使用频率

---

## 🔗 相关链接

- **GitHub**: https://github.com/Panniantong/Agent-Reach
- **Jina Reader**: https://github.com/jina-ai/reader
- **yt-dlp**: https://github.com/yt-dlp/yt-dlp

---

**安装完成时间**: 2026-02-27  
**B166ER 协助安装**
