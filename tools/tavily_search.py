#!/usr/bin/env python3
"""
Tavily Search 工具
使用主人提供的 API Key: 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
免费额度: 1000次/月
"""

import os
import sys
import json

# 主人的 API Key
TAVILY_API_KEY = "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"

def search(query, max_results=5, search_depth="basic"):
    """
    使用 Tavily API 进行搜索
    
    Args:
        query: 搜索查询
        max_results: 返回结果数量 (默认5)
        search_depth: basic 或 comprehensive
    """
    try:
        from tavily import TavilyClient
        
        client = TavilyClient(api_key=TAVILY_API_KEY)
        
        response = client.search(
            query=query,
            max_results=max_results,
            search_depth=search_depth,
            include_answer=True,
            include_images=False
        )
        
        return response
        
    except ImportError:
        # 如果没有安装tavily包，使用requests直接调用API
        import requests
        
        url = "https://api.tavily.com/search"
        
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "max_results": max_results,
            "search_depth": search_depth,
            "include_answer": True,
            "include_images": False
        }
        
        response = requests.post(url, json=payload)
        return response.json()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tavily_search.py <query>")
        sys.exit(1)
    
    query = sys.argv[1]
    results = search(query)
    
    print(json.dumps(results, ensure_ascii=False, indent=2))
