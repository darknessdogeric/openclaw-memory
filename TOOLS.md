# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — environment-specific config and tool status.

---

## 环境偏好

**终端**: Git Bash（非PowerShell）

---

## OpenViking - AI上下文数据库 ⚠️
**位置**: `C:\Users\ericz\.openviking\` | **服务器**: http://127.0.0.1:1933
**版本**: v0.2.9 (CLI: 0.2.6) | **Embedding**: Jina v4（限速，免费100次/分钟）
**功能**: 文件系统管理/分层上下文加载/语义搜索
**用法**: `ov status` / `ov find "query"` / `ov ls viking://resources/`
**问题**: Jina免费配额有限，高并发时被限速
**手动重启**: `Remove-Item -Force 'C:\Users\ericz\.openviking\data2\.openviking.pid'` → 运行`start_ov.bat`

### 本地语义搜索（免费无限制）✅ 新
**位置**: `workspace/local_semantic_search.py`
**Embedding**: model2vec `minishlab/potion-base-8M`（8MB，256维，CPU运行，完全免费）
**向量库**: Chromadb（本地持久化，`workspace/.chroma_db/`）
**用法**:
```
python local_semantic_search.py index   # 重建索引
python local_semantic_search.py count    # 统计文档数
python local_semantic_search.py search "查询内容"  # 语义搜索
python local_semantic_search.py full     # 完整重建
```
**已索引**: 141个memory文件（2026-04-08）
**优势**: 完全离线、无API限制、无配额问题

---

## PPT工具

### ppt-deck-builder-pro ✅
**位置**: `skills/ppt-deck-builder-pro/` | **版本**: 0.3.0
**模板**: 12种（含 startup_roadshow/corporate_pro/minimal_white/luxury_premium 等）
**用法**: 告诉B166ER场景 → 自动推荐模板 → 生成PPT
**快速生成**: `bash scripts/run_image_batch.sh plan.json output_dir`
**打包**: `bash scripts/package_image_deck.sh output_dir deck.pptx plan.json`

### md2all - Markdown转多格式 ✅
**位置**: `tools/md2all/` | **依赖**: python-docx, markdown, fpdf2, beautifulsoup4
**用法**: `python md2all.py 文档.md [pdf|docx|html]`

### md2ppt ✅
**位置**: `skills/md2ppt/md2ppt.py` | **依赖**: python-pptx, Pillow
**用法**: `python C:\Users\Administrator\.openclaw\skills\md2ppt\md2ppt.py`
**输出**: `C:\Users\Administrator\Desktop\项目说明书\`

---

## 网络工具

### scrap_tools.py - 爬虫工具箱 ✅
**位置**: `workspace/scrap_tools.py`
**用法**:
```
python scrap_tools.py fetch <url> [output]     # 静态页面
python scrap_tools.py dynamic <url> [output]  # JS页面
python scrap_tools.py search <query> [engine] # 搜索
python scrap_tools.py smart <query>            # 多引擎智能搜索
python scrap_tools.py parse <html> [engine]   # 解析结果
```
**已验证**: 静态页面(百度百科/新闻)、Playwright可用、scrapling可用
**注意**: 国内搜索有反爬（Baidu安全验证/Bing人机验证）→ 用直接URL抓取替代

### tavily_search.py - Tavily API搜索 ✅
**位置**: `workspace/tavily_search_v2.py`
**API Key**: `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``
**状态**: ✅ 已验证可用
**用法**:
```bash
python tavily_search_v2.py --query "关键词" --max-results 8 --include-answer --format md
```
**成功率**: 接近100%（绕过国内搜索引擎反爬限制）
**配额**: 1000次/月（免费版）
**对比**:
| 工具 | 成功率 | 速度 | 备注 |
|------|--------|------|------|
| Tavily API | ✅ 95%+ | 快 | 需API Key |
| scrapling | ✅ 静态页 | 快 | 百科/新闻 |
| 搜狗+selenium | ✅ 70% | 慢 | JS渲染页 |
| 百度/必应 | ❌ 反爬 | - | 触发验证 |

### agent-reach ✅
**版本**: 1.2.0 | **位置**: `C:\Python314\Lib\site-packages`
**功能**: 网页读取/YouTube-B站字幕/RSS解析/GitHub/Exa搜索/Twitter
**用法**:
```bash
curl https://r.jina.ai/http://example.com  # 网页
yt-dlp --dump-json "URL"                  # 视频信息
gh repo view owner/repo                    # GitHub
```

### Firecrawl Skill ✅
**位置**: `skills/firecrawl-skill/` | **状态**: 已克隆，待配API Key
**用法**: `export FIRECRAWL_API_KEY=fc-your-key` → `python3 fc.py markdown "url"`

### Ultimate Search ✅
**位置**: `skills/ultimate-search/` | **状态**: 已克隆，需Docker
**功能**: Grok + Tavily双引擎搜索

### Crawl4AI ✅
**位置**: `skills/crawl4ai/` | **功能**: AI网页爬取

### Playwright MCP ✅
**位置**: `skills/playwright-mcp/` | **功能**: 浏览器自动化

### Apify MCP ✅
**位置**: `skills/apify-mcp/` | **功能**: Apify actors MCP

---

## 增长工具

### Growth Mindset ✅
**位置**: `skills/growth-mindset/` | **版本**: 1.0.0
**用法**:
```bash
python reflection-tool.py reflect --task "任务" --completion 90 --quality 4
python reflection-tool.py summary
python reflection-tool.py suggest
```

### Ontology ✅
**位置**: `skills/ontology/` | **存储**: `memory/ontology/graph.jsonl`
**用法**: `create_entity()` / `create_relation()` / `query_entities()`

---

## 内容工具

### 提示词库
**AHL专用**: `D:\AHL-Database\07-AIGC提示词库\`
**源**: github.com/PlexPt/awesome-chatgpt-prompts-zh
**覆盖**: 小红书/抖音/朋友圈/邮件/公众号/OTA详情页

---

## API Keys

| 服务 | Key | 备注 |
|------|-----|------|
| Jina Embedding | `jina_1aa1bc0d...` | OpenViking向量 |
| Tavily | `tvly-dev-8KxnA8...` | 搜索API |
| RUNNINGHUB | (待配置) | PPT图片生成 |

---

## 运行环境

- **Node**: v24.14.0
- **Python**: 3.14 (C:\Users\ericz\AppData\Local\Programs\Python\Python314\)
- **工作区**: `C:\Users\ericz\.openclaw\workspace`
- **项目**: `C:\Users\ericz\Desktop\张实项目总控\`
- **Gateway**: 127.0.0.1:18789 | Web: http://127.0.0.1:18789/
