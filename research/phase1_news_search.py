#!/usr/bin/env python3
"""
2026年Q1中国酒店行业研究报告 - 阶段1：新闻搜集
使用Tavily API进行多主题搜索
"""

import os
import json
from datetime import datetime
from tavily import TavilyClient

# 获取API key
tavily_api_key = os.getenv('TAVILY_API_KEY')
if not tavily_api_key:
    print("错误: TAVILY_API_KEY 环境变量未设置")
    exit(1)

client = TavilyClient(api_key=tavily_api_key)

# 定义搜索主题
search_topics = [
    {
        "category": "酒店管理",
        "query": "2026年Q1中国酒店管理新闻 酒店集团 品牌管理"
    },
    {
        "category": "酒店投资",
        "query": "2026年Q1中国酒店投资 酒店并购 酒店交易 酒店融资"
    },
    {
        "category": "酒店运营",
        "query": "2026年Q1中国酒店运营 酒店业绩 酒店入住率 RevPAR"
    },
    {
        "category": "酒店科技",
        "query": "2026年Q1酒店科技 智慧酒店 AI酒店 数字化转型 酒店智能化"
    },
    {
        "category": "行业整体",
        "query": "2026年Q1中国酒店行业新闻 酒店市场 酒店业发展 酒店趋势"
    }
]

# 存储所有结果
all_results = {}
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

print(f"开始执行阶段1新闻搜集任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

for topic in search_topics:
    category = topic["category"]
    query = topic["query"]
    
    print(f"\n正在搜索: {category}...")
    print(f"查询词: {query}")
    
    try:
        result = client.search(
            query=query,
            search_depth='advanced',
            include_answer=True,
            max_results=10,
            time_range='month'  # 最近一个月，确保时效性
        )
        
        all_results[category] = {
            "query": query,
            "answer": result.get('answer', ''),
            "results": []
        }
        
        # 处理搜索结果
        for r in result.get('results', []):
            all_results[category]["results"].append({
                "title": r.get('title', ''),
                "url": r.get('url', ''),
                "content": r.get('content', '')[:500] + "..." if len(r.get('content', '')) > 500 else r.get('content', ''),
                "score": r.get('score', 0),
                "published_date": r.get('published_date', '未知')
            })
        
        print(f"  ✓ 找到 {len(all_results[category]['results'])} 条结果")
        
    except Exception as e:
        print(f"  ✗ 搜索失败: {str(e)}")
        all_results[category] = {
            "query": query,
            "error": str(e),
            "results": []
        }

# 保存结果到文件
output_dir = os.path.expanduser("~/.openclaw/workspace/research/hotel_industry_q1_2026")
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, f"phase1_news_collection_{timestamp}.json")
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({
        "metadata": {
            "phase": "阶段1：新闻搜集",
            "timestamp": timestamp,
            "search_topics": len(search_topics),
            "total_results": sum(len(v.get('results', [])) for v in all_results.values())
        },
        "data": all_results
    }, f, ensure_ascii=False, indent=2)

# 同时生成Markdown摘要报告
md_file = os.path.join(output_dir, f"phase1_news_collection_{timestamp}.md")
with open(md_file, 'w', encoding='utf-8') as f:
    f.write("# 2026年Q1中国酒店行业研究报告 - 阶段1：新闻搜集\n\n")
    f.write(f"**搜集时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write("---\n\n")
    
    for category, data in all_results.items():
        f.write(f"## {category}\n\n")
        f.write(f"**搜索词**: {data.get('query', '')}\n\n")
        
        if 'answer' in data and data['answer']:
            f.write(f"**AI摘要**: {data['answer']}\n\n")
        
        if 'error' in data:
            f.write(f"**错误**: {data['error']}\n\n")
        
        f.write("### 搜索结果\n\n")
        for i, r in enumerate(data.get('results', []), 1):
            f.write(f"{i}. **{r.get('title', '无标题')}**\n")
            f.write(f"   - URL: {r.get('url', '')}\n")
            f.write(f"   - 发布时间: {r.get('published_date', '未知')}\n")
            f.write(f"   - 相关性评分: {r.get('score', 0):.2f}\n")
            f.write(f"   - 摘要: {r.get('content', '')[:200]}...\n\n")
        
        f.write("---\n\n")

print("\n" + "=" * 80)
print(f"阶段1完成！")
print(f"JSON数据: {output_file}")
print(f"Markdown报告: {md_file}")
print(f"总计搜集: {sum(len(v.get('results', [])) for v in all_results.values())} 条结果")
