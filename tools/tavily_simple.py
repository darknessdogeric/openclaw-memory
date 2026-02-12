#!/usr/bin/env python3
"""
Tavily Search 工具 - 轻量版 (无需安装tavily包)
使用主人提供的 API Key
"""

import os
import sys
import json
import urllib.request
import urllib.error
import ssl

# 主人的 API Key
TAVILY_API_KEY = "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"

def search(query, max_results=5, search_depth="basic"):
    """
    使用 Tavily API 进行搜索
    """
    url = "https://api.tavily.com/search"
    
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": max_results,
        "search_depth": search_depth,
        "include_answer": True,
        "include_images": False
    }
    
    data = json.dumps(payload).encode('utf-8')
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
    }
    
    try:
        # 创建 SSL 上下文
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        
        with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
            
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP Error {e.code}: {e.reason}", "details": e.read().decode('utf-8')}
    except urllib.error.URLError as e:
        return {"error": f"URL Error: {str(e.reason)}", "hint": "检查网络连接或代理设置"}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tavily_simple.py <query>")
        sys.exit(1)
    
    query = sys.argv[1]
    print(f"Searching: {query}\n")
    
    results = search(query)
    
    # 格式化输出
    if "error" in results:
        print(f"[!] Error: {results['error']}")
        if "details" in results:
            print(f"Details: {results['details']}")
    else:
        print(f"[OK] Search completed!")
        print(f"Query: {results.get('query', 'N/A')}")
        print(f"Results count: {len(results.get('results', []))}")
        
        if results.get('answer'):
            print(f"\n[Answer]:\n{results['answer']}\n")
        
        print("=" * 60)
        for i, r in enumerate(results.get('results', [])[:3], 1):
            print(f"\n{i}. {r.get('title', 'No title')}")
            print(f"   URL: {r.get('url', 'N/A')}")
            print(f"   {r.get('content', 'No content')[:200]}...")
