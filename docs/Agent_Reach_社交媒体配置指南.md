# Agent Reach - Twitter/小红书/抖音 配置指南

> **配置时间**: 2026年2月27日  
> **目标平台**: Twitter/X, 小红书, 抖音  
> **安全提示**: 建议使用小号Cookie，不要用主账号

---

## 📋 配置前准备

### 必需工具检查

请确认以下工具已安装：

```bash
# 检查Docker (用于小红书)
docker --version

# 检查Node.js/npm (用于抖音)
node --version
npm --version

# 检查Chrome浏览器 (用于提取Cookie)
# 确保已登录Twitter/小红书/抖音
```

**安装状态**:
- [ ] Docker - 如需使用小红书MCP
- [ ] Node.js - 如需使用抖音MCP
- [x] Chrome浏览器 - 用于Cookie提取

---

## 🐦 1. Twitter/X 配置

### 步骤1: 登录Twitter
1. 打开Chrome浏览器
2. 访问 https://twitter.com 或 https://x.com
3. **使用小号登录** (不要用主账号！)
4. 确保登录状态正常

### 步骤2: 安装Cookie-Editor插件
1. 打开Chrome应用商店
2. 搜索 "Cookie-Editor"
3. 安装插件: https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm

### 步骤3: 导出Cookie
1. 在Twitter页面点击Cookie-Editor图标
2. 点击 "Export" 按钮
3. 选择格式: **JSON**
4. 复制导出的JSON内容

### 步骤4: 配置Agent Reach

**方法一: 命令行配置**
```bash
agent-reach configure twitter-cookies '粘贴你的JSON Cookie'
```

**方法二: 手动编辑配置文件**
1. 打开文件: `C:\Users\Administrator\.agent-reach\config.yaml`
2. 找到 `twitter_cookies` 部分
3. 粘贴Cookie JSON
4. 保存文件

### 步骤5: 验证配置
```bash
# 测试读取推文
xreach tweet https://twitter.com/username/status/1234567890 --json

# 测试搜索
xreach search "大理民宿" --json
```

---

## 📕 2. 小红书 配置

### 方式A: Docker MCP服务 (推荐)

#### 前提条件
- 安装Docker: https://www.docker.com/products/docker-desktop

#### 步骤1: 登录小红书
1. Chrome访问 https://www.xiaohongshu.com
2. **使用小号登录**
3. 确保登录状态正常

#### 步骤2: 导出Cookie
1. 使用Cookie-Editor插件
2. 导出JSON格式Cookie
3. 保存为环境变量或配置文件

#### 步骤3: 启动MCP服务
```bash
# 设置Cookie环境变量
set XHS_COOKIES=你的Cookie JSON字符串

# 启动Docker容器
docker run -i --rm -e XHS_COOKIES=%XHS_COOKIES% xpzouying/xiaohongshu-mcp
```

#### 步骤4: 配置Agent Reach
编辑 `config.yaml`:
```yaml
mcp_servers:
  xiaohongshu:
    enabled: true
    command: docker
    args:
      - run
      - -i
      - --rm
      - -e
      - XHS_COOKIES=${XHS_COOKIES}
      - xpzouying/xiaohongshu-mcp
    env:
      XHS_COOKIES: "粘贴你的Cookie"
```

#### 步骤5: 验证
```bash
# 读取笔记
mcporter call 'xiaohongshu.get_feed_detail(feed_id: "笔记ID")'

# 搜索
mcporter call 'xiaohongshu.search_feeds(keyword: "大理民宿")'
```

### 方式B: Python直接调用 (无需Docker)

如果Docker不可用，可以使用Python库:
```bash
pip install xiaohongshu-api
```

然后编写Python脚本调用。

---

## 🎵 3. 抖音 配置

### 步骤1: 安装抖音MCP服务
```bash
npm install -g douyin-mcp-server
```

### 步骤2: 配置Agent Reach
编辑 `config.yaml`:
```yaml
mcp_servers:
  douyin:
    enabled: true
    command: npx
    args:
      - -y
      - douyin-mcp-server
```

### 步骤3: 验证
```bash
# 解析视频
mcporter call 'douyin.parse_douyin_video_info(share_link: "抖音分享链接")'
```

**注意**: 抖音MCP不需要Cookie，直接解析分享链接即可。

---

## 🔒 安全建议

### Cookie安全
1. **使用小号**: 绝对不要用主账号的Cookie
2. **定期更换**: 建议每月更换一次Cookie
3. **本地存储**: Cookie只保存在本地，不会上传
4. **文件权限**: 配置文件权限设置为仅当前用户可读写

### 封号风险
- Twitter/小红书可能检测到API调用行为
- 建议控制调用频率，不要频繁爬取
- 如账号被封，使用备用小号

---

## 🧪 快速测试脚本

创建测试文件 `test_social.py`:

```python
#!/usr/bin/env python3
"""测试社交媒体配置"""

import subprocess
import json

def test_twitter():
    """测试Twitter"""
    try:
        result = subprocess.run(
            ['xreach', 'search', 'AI', '--json'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✅ Twitter: 配置成功")
            return True
        else:
            print("❌ Twitter:", result.stderr)
            return False
    except Exception as e:
        print("❌ Twitter:", str(e))
        return False

def test_xiaohongshu():
    """测试小红书"""
    try:
        # 使用mcporter调用
        result = subprocess.run(
            ['mcporter', 'call', 'xiaohongshu.search_feeds(keyword: "旅行")'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✅ 小红书: 配置成功")
            return True
        else:
            print("❌ 小红书:", result.stderr)
            return False
    except Exception as e:
        print("❌ 小红书:", str(e))
        return False

def test_douyin():
    """测试抖音"""
    try:
        result = subprocess.run(
            ['mcporter', 'call', 'douyin.parse_douyin_video_info(share_link: "")'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✅ 抖音: 配置成功")
            return True
        else:
            print("❌ 抖音:", result.stderr)
            return False
    except Exception as e:
        print("❌ 抖音:", str(e))
        return False

if __name__ == '__main__':
    print("测试社交媒体配置...\n")
    test_twitter()
    test_xiaohongshu()
    test_douyin()
```

运行测试:
```bash
python test_social.py
```

---

## 📚 使用示例

### 监控竞品动态
```python
# 搜索Twitter上的竞品讨论
import subprocess

result = subprocess.run(
    ['xreach', 'search', '直客通 OR 订单来了 OR 飞猪', '--json'],
    capture_output=True,
    text=True
)
tweets = json.loads(result.stdout)
```

### 小红书内容研究
```python
# 搜索民宿相关内容
mcporter call 'xiaohongshu.search_feeds(keyword: "大理民宿推荐")'
```

### 抖音视频分析
```python
# 解析抖音视频
mcporter call 'douyin.parse_douyin_video_info(share_link: "https://v.douyin.com/xxxxx")'
```

---

## ⚠️ 常见问题

### Q: Cookie过期了怎么办?
A: 重新登录浏览器，用Cookie-Editor导出新的Cookie，更新配置文件。

### Q: Twitter提示"403 Forbidden"?
A: 可能是IP被封锁，尝试配置代理:
```bash
agent-reach configure proxy http://user:pass@host:port
```

### Q: 小红书Docker启动失败?
A: 检查Docker是否运行:
```bash
docker ps
```

### Q: 抖音解析失败?
A: 确保使用正确的分享链接格式 (v.douyin.com/xxxxx)。

---

## 📁 相关文件

- 配置文件: `C:\Users\Administrator\.agent-reach\config.yaml`
- 使用指南: `docs/Agent_Reach_使用指南.md`
- 测试脚本: `test_social.py` (待创建)

---

**配置完成时间**: 2026-02-27  
**B166ER 协助配置**
