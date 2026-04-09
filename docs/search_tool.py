# -*- coding: utf-8 -*-
"""
B166ER 全网搜索解决方案
使用Chrome浏览器 + 百度/Bing搜索，比web_search更稳定
"""
import subprocess
import sys
import json
import re
import time

def search_baidu(query, num_results=10):
    """使用chrome-devtools协议通过百度搜索"""
    try:
        import requests
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
        import requests

    # 使用百度搜索API（无需代理）
    encoded_query = requests.utils.quote(query)
    baidu_url = f"https://www.baidu.com/s?wd={encoded_query}&rn={num_results}"

    # 使用Jina Reader抓取百度搜索结果页
    jina_url = f"https://r.jina.ai/http://{baidu_url}"

    try:
        resp = requests.get(jina_url, timeout=15, headers={
            "Accept": "text/plain",
            "X-Engine": "B166ER-Search/1.0"
        })
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        return f"[Jina+百度搜索失败: {e}]"

def search_bing(query, num_results=10):
    """使用Bing搜索"""
    try:
        import requests
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
        import requests

    encoded_query = requests.utils.quote(query)
    bing_url = f"https://cn.bing.com/search?q={encoded_query}&count={num_results}"

    jina_url = f"https://r.jina.ai/http://{bing_url}"

    try:
        resp = requests.get(jina_url, timeout=15, headers={
            "Accept": "text/plain",
            "X-Engine": "B166ER-Search/1.0"
        })
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        return f"[Jina+Bing搜索失败: {e}]"

def parse_search_results(text, source="baidu"):
    """解析搜索结果文本，提取标题和URL"""
    results = []
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line or len(line) < 10:
            continue
        # 提取URL
        url_match = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', line)
        if url_match and len(line) > 20:
            url = url_match[0]
            # 清理URL
            url = re.sub(r'#[^/]*$', '', url)
            title = re.sub(r'https?://[^\s*]+', '', line).strip()
            title = re.sub(r'^\s*[-.\s*]+', '', title)
            if title and len(title) > 5:
                results.append({"title": title[:200], "url": url})

    # 去重
    seen = set()
    unique = []
    for r in results:
        if r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)

    return unique[:10]

def search(query, engine="baidu", num_results=10):
    """
    主搜索函数

    Args:
        query: 搜索关键词
        engine: "baidu" 或 "bing"
        num_results: 返回结果数量

    Returns:
        list: [{"title": "...", "url": "..."}, ...]
    """
    print(f"[B166ER Search] 使用{engine}搜索: {query}", flush=True)

    if engine == "baidu":
        raw = search_baidu(query, num_results)
    else:
        raw = search_bing(query, num_results)

    if raw.startswith("["):
        print(f"[B166ER Search] 搜索失败: {raw[:100]}")
        return []

    results = parse_search_results(raw, engine)
    print(f"[B166ER Search] 找到 {len(results)} 条结果", flush=True)
    return results

def fetch_page(url, max_chars=5000):
    """
    使用Jina Reader抓取网页内容

    Args:
        url: 目标URL
        max_chars: 最大字符数

    Returns:
        str: 页面文本内容
    """
    try:
        import requests
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
        import requests

    jina_url = f"https://r.jina.ai/http://{url}"
    try:
        resp = requests.get(jina_url, timeout=20, headers={
            "Accept": "text/plain",
            "X-Engine": "B166ER-Fetch/1.0",
            "X-Max-Length": str(max_chars)
        })
        resp.raise_for_status()
        return resp.text[:max_chars]
    except Exception as e:
        return f"[抓取失败: {e}]"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python search_tool.py <搜索关键词> [引擎:baidu|bing] [数量]")
        sys.exit(1)

    query = sys.argv[1]
    engine = sys.argv[2] if len(sys.argv) > 2 else "baidu"
    num = int(sys.argv[3]) if len(sys.argv) > 3 else 10

    results = search(query, engine, num)
    output = json.dumps(results, ensure_ascii=False, indent=2)
    # Windows GBK兼容
    try:
        print(output)
    except UnicodeEncodeError:
        print(output.encode('utf-8').decode('utf-8'))
