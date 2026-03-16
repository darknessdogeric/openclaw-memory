# Agent Reach 配置向导

> 配置时间: 2026年3月15日  
> 目标: Twitter/X, 小红书, 抖音, Reddit, LinkedIn

---

## 📋 环境检查

### ✅ 已安装
- Node.js v24.13.0
- npm 11.6.2
- Chrome浏览器

### ❌ 未安装
- Docker - 小红书MCP需要（可选，可用替代方案）

---

## 🐦 第一步: Twitter/X 配置

### 1.1 安装 Cookie-Editor 插件

1. 打开Chrome浏览器
2. 访问: https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm
3. 点击 "添加至 Chrome"
4. 确认安装

### 1.2 登录Twitter/X

**⚠️ 重要: 建议使用小号，不要用主账号！**

1. 访问 https://twitter.com 或 https://x.com
2. 使用小号登录
3. 确保登录状态正常（能看到时间线）

### 1.3 导出Cookie

1. 在Twitter页面点击Cookie-Editor图标（地址栏右侧拼图图标）
2. 点击 "Export" 按钮
3. 选择格式: **JSON**
4. 点击复制按钮或全选复制

### 1.4 配置Agent Reach

**方法A: 命令行配置（推荐）**

```bash
# 先创建配置目录
mkdir -p %USERPROFILE%\.agent-reach

# 使用agent-reach命令配置
agent-reach configure twitter-cookies "粘贴你的JSON Cookie"
```

**方法B: 手动配置文件**

创建文件 `%USERPROFILE%\.agent-reach\config.yaml`:

```yaml
twitter:
  enabled: true
  cookies: |
    粘贴你的JSON Cookie内容
```

### 1.5 安装 xreach CLI

```bash
# 安装Twitter访问工具
npm install -g xreach-cli

# 验证安装
xreach --version
```

### 1.6 验证配置

```bash
# 测试读取推文
xreach tweet https://twitter.com/elonmusk/status/1234567890

# 测试搜索
xreach search "大理民宿" --limit 10
```

---

## 📕 第二步: 小红书 配置

由于Docker未安装，提供两种替代方案：

### 方案A: Python直接调用 (推荐)

```bash
# 安装Python库
pip install xiaohongshu-api

# 或使用requests直接调用
pip install requests
```

创建测试脚本 `test_xhs.py`:

```python
import requests
import json

# 需要配置Cookie
COOKIES = """粘贴你的小红书Cookie"""

cookies_dict = json.loads(COOKIES)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://www.xiaohongshu.com/',
}

# 读取笔记详情
def get_note_detail(note_id):
    url = f'https://www.xiaohongshu.com/explore/{note_id}'
    response = requests.get(url, headers=headers, cookies=cookies_dict)
    return response.text

# 搜索笔记
def search_notes(keyword):
    search_url = 'https://www.xiaohongshu.com/api/sns/web/v1/search/notes'
    # ... 实现搜索逻辑
    pass

if __name__ == '__main__':
    # 测试
    result = get_note_detail('笔记ID')
    print(result[:500])
```

### 方案B: 安装Docker后使用MCP

如需完整功能，可安装Docker Desktop:
https://www.docker.com/products/docker-desktop

安装后配置:
```bash
# 设置Cookie环境变量
set XHS_COOKIES=你的Cookie JSON

# 启动MCP服务
docker run -i --rm -e XHS_COOKIES=%XHS_COOKIES% xpzouying/xiaohongshu-mcp
```

---

## 🎵 第三步: 抖音 配置

### 3.1 安装抖音MCP服务

```bash
# 安装抖音MCP
npm install -g douyin-mcp-server

# 验证安装
douyin-mcp-server --version
```

### 3.2 配置Cookie

1. 访问 https://www.douyin.com
2. 使用Cookie-Editor导出Cookie (JSON格式)
3. 保存Cookie到配置文件

### 3.3 配置Agent Reach

编辑 `%USERPROFILE%\.agent-reach\config.yaml`:

```yaml
douyin:
  enabled: true
  cookies: |
    粘贴你的抖音Cookie
```

---

## 🔍 第四步: 全网搜索配置 (Exa MCP)

Exa提供免费的AI语义搜索，无需API Key。

### 4.1 安装 mcporter

```bash
# 安装MCP工具
npm install -g mcporter

# 验证安装
mcporter --version
```

### 4.2 配置Exa搜索

编辑 `%USERPROFILE%\.agent-reach\config.yaml`:

```yaml
mcp_servers:
  exa:
    enabled: true
    command: npx
    args:
      - -y
      - exa-mcp-server
```

### 4.3 验证搜索

```bash
# AI语义搜索
mcporter call 'exa.search(query: "最新的LLM框架对比", num_results: 5)'
```

---

## 📄 完整配置文件模板

创建 `%USERPROFILE%\.agent-reach\config.yaml`:

```yaml
# Agent Reach 配置文件
version: "1.0"

# Twitter/X 配置
twitter:
  enabled: true
  cookies: |
    {
      "auth_token": "你的token",
      "ct0": "你的ct0",
      ...
    }

# 小红书配置
xiaohongshu:
  enabled: false  # 设置为true启用
  cookies: |
    {
      "web_session": "你的session",
      ...
    }

# 抖音配置
douyin:
  enabled: false
  cookies: |
    {
      "sessionid": "你的sessionid",
      ...
    }

# MCP服务配置
mcp_servers:
  exa:
    enabled: true
    command: npx
    args:
      - -y
      - exa-mcp-server
  
  xiaohongshu:
    enabled: false
    command: docker
    args:
      - run
      - -i
      - --rm
      - -e
      - XHS_COOKIES=${XHS_COOKIES}
      - xpzouying/xiaohongshu-mcp

# 代理配置（服务器需要）
proxy:
  enabled: false
  http: http://proxy:port
  https: http://proxy:port
```

---

## 🧪 验证所有配置

创建验证脚本 `verify_agent_reach.py`:

```python
#!/usr/bin/env python3
"""验证Agent Reach配置状态"""

import subprocess
import sys
import yaml
import os

def check_command(cmd, name):
    """检查命令是否可用"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {name}: 可用")
            return True
        else:
            print(f"❌ {name}: 不可用")
            return False
    except Exception as e:
        print(f"❌ {name}: 错误 - {e}")
        return False

def check_config():
    """检查配置文件"""
    config_path = os.path.expanduser("~/.agent-reach/config.yaml")
    if os.path.exists(config_path):
        print(f"✅ 配置文件存在: {config_path}")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # 检查各平台配置
        platforms = ['twitter', 'xiaohongshu', 'douyin']
        for platform in platforms:
            if config.get(platform, {}).get('enabled', False):
                print(f"  ✅ {platform}: 已启用")
            else:
                print(f"  ⏳ {platform}: 未启用")
    else:
        print(f"❌ 配置文件不存在: {config_path}")

def main():
    print("=" * 50)
    print("Agent Reach 配置验证")
    print("=" * 50)
    
    # 检查核心工具
    print("\n📦 核心工具检查:")
    check_command("yt-dlp --version", "yt-dlp")
    check_command("gh --version", "gh CLI")
    check_command("xreach --version", "xreach")
    check_command("mcporter --version", "mcporter")
    
    # 检查Python库
    print("\n🐍 Python库检查:")
    try:
        import feedparser
        print("✅ feedparser: 已安装")
    except:
        print("❌ feedparser: 未安装")
    
    try:
        import requests
        print("✅ requests: 已安装")
    except:
        print("❌ requests: 未安装")
    
    # 检查配置
    print("\n⚙️ 配置检查:")
    check_config()
    
    print("\n" + "=" * 50)
    print("验证完成!")
    print("=" * 50)

if __name__ == "__main__":
    main()
```

运行验证:
```bash
python verify_agent_reach.py
```

---

## 📚 使用示例

配置完成后，可以这样使用:

```bash
# 读取Twitter推文
xreach tweet https://twitter.com/username/status/1234567890

# 搜索Twitter
xreach search "关键词" --limit 20

# AI语义搜索
mcporter call 'exa.search(query: "问题", num_results: 10)'

# 网页阅读
curl https://r.jina.ai/http://example.com

# YouTube字幕
yt-dlp --dump-json "https://youtube.com/watch?v=VIDEO_ID"
```

---

## ⚠️ 安全提醒

1. **使用小号**: 所有社交媒体配置建议使用小号，不要用主账号
2. **Cookie保密**: Cookie包含登录凭证，不要分享给他人
3. **定期更新**: Cookie会过期，需要定期重新导出
4. **本地存储**: Cookie只存储在本地，不会上传到云端

---

## 🆘 故障排除

### 问题: xreach 命令找不到
**解决**: 
```bash
npm install -g xreach-cli
```

### 问题: Cookie配置后仍无法访问
**解决**:
1. 检查Cookie是否完整（包含auth_token和ct0）
2. 确认账号未被限制
3. 尝试重新导出Cookie

### 问题: 中文字符显示乱码
**解决**:
```powershell
# Windows PowerShell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

---

**配置完成后，Agent Reach将拥有完整的互联网访问能力！**
