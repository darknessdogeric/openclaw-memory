# 2026-03-06 技能安装记录

## 今日完成安装的技能（从GitHub克隆）

### ✅ Ontology（本体论知识图谱）
- **来源**: https://github.com/hiveminderbot/ontology
- **位置**: `skills/ontology/`
- **状态**: ✅ 已安装并测试
- **功能**: 结构化知识图谱，实体关系管理
- **已创建**: Person(张实) + Project(AHL) + Relation(owns)

### ✅ Skill-Creator（技能创建工具）
- **来源**: https://github.com/nkchivas/openclaw-skill-skill-creator
- **位置**: `skills/skill-creator/`
- **状态**: ✅ 已克隆
- **功能**: 自动生成OpenClaw技能结构

### ✅ Ultimate-Search（终极搜索）
- **来源**: https://github.com/ckckck/UltimateSearchSkill
- **位置**: `skills/ultimate-search/`
- **状态**: ✅ 已克隆
- **功能**: Grok + Tavily双引擎搜索，FireCrawl降级
- **依赖**: Docker部署，需配置Grok Token和Tavily Key

### ✅ Firecrawl-Skill（网页爬取）
- **来源**: https://github.com/capt-marbles/firecrawl
- **位置**: `skills/firecrawl-skill/`
- **状态**: ✅ 已克隆
- **功能**: Firecrawl API网页爬取，支持markdown/screenshot/extract
- **依赖**: `pip install firecrawl`, `FIRECRAWL_API_KEY`

### ✅ Crawl4AI（AI网页爬取）
- **来源**: https://github.com/unclecode/crawl4ai
- **位置**: `skills/crawl4ai/`
- **状态**: ✅ 已克隆（大型项目，11413个对象）
- **功能**: AI驱动的网页爬取和数据提取

### ✅ Playwright-MCP（浏览器自动化）
- **来源**: https://github.com/microsoft/playwright-mcp
- **位置**: `skills/playwright-mcp/`
- **状态**: ✅ 已克隆
- **功能**: Microsoft Playwright浏览器自动化MCP服务器

### ✅ Apify-MCP（Apify平台集成）
- **来源**: https://github.com/apify/actors-mcp-server
- **位置**: `skills/apify-mcp/`
- **状态**: ✅ 已克隆
- **功能**: Apify actors MCP服务器

---

## 待配置技能（需要API Key/环境）

| 技能 | 需要配置 | 优先级 |
|------|---------|--------|
| firecrawl-skill | FIRECRAWL_API_KEY | ⭐⭐⭐ |
| ultimate-search | Grok Token + Tavily Key + Docker | ⭐⭐ |
| apify-mcp | Apify账号 | ⭐⭐ |
| playwright-mcp | Playwright浏览器 | ⭐⭐ |
| crawl4ai | 依赖安装 | ⭐⭐ |

---

## 仍需安装的技能（搜索中未找到/未安装）

- [ ] superpowers - 48k+星标技能集
- [ ] planning-with-files - 文件规划技能
- [ ] ui-ux-promax - UI/UX设计技能
- [ ] decodo-scraper - Decodo抓取

---

### ✅ Nano PDF（PDF自然语言编辑）
- **来源**: https://github.com/nkchivas/openclaw-skill-nano-pdf
- **位置**: `skills/nano-pdf/`
- **状态**: ✅ 已克隆
- **功能**: 使用自然语言指令编辑PDF
- **依赖**: `uv install nano-pdf`
- **使用示例**:
  ```bash
  nano-pdf edit deck.pdf 1 "Change the title to 'Q3 Results'"
  ```

---

### ✅ Proactive Agent（主动式智能体）
- **来源**: https://github.com/nkchivas/openclaw-skill-proactive-agent
- **位置**: `skills/proactive-agent/`
- **状态**: ✅ 已克隆
- **版本**: v3.0.0 by Hal Labs
- **功能**: 
  - **WAL Protocol** - 预写日志保护关键信息
  - **Working Buffer** - 60%上下文后自动记录
  - **Compaction Recovery** - 上下文截断后恢复
  - **安全加固** - 技能审查、上下文防泄露
  - **自我改进** - ADL/VFM安全进化协议
  - **主动惊喜** - 主动创造用户未要求的价值

---

## 明日行动计划

1. 配置 firecrawl-skill（获取API Key）
2. 测试 ultimate-search（部署Docker）
3. 继续搜索剩余4个技能
4. 安装并测试所有爬虫技能
