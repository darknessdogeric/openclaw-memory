# -*- coding: utf-8 -*-
"""
scrap_tools.py v2 - scrapling爬虫工具箱增强版
解决JS渲染等待 + 搜索结果地理定位问题
"""

import sys
import os
import asyncio
import time
from urllib.parse import quote, urlparse
from scrapling import Fetcher, DynamicFetcher

# ============================================================
# 阶段一：基础增强
# ============================================================

def fetch_static(url, output_file=None):
    """抓取静态页面"""
    f = Fetcher()
    response = f.get(url)
    text = response.get_all_text()
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as fw:
            fw.write(text)
    print(f'[{response.status}] OK: {url} -> {len(text)} chars')
    return text


async def fetch_dynamic_async(url, output_file=None):
    """异步抓取JS渲染页面"""
    f = DynamicFetcher()
    response = await f.fetch(url)
    text = response.get_all_text()
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as fw:
            fw.write(text)
    print(f'[{response.status}] OK: {url} -> {len(text)} chars')
    return text


def fetch_dynamic(url, output_file=None):
    """同步封装"""
    return asyncio.run(fetch_dynamic_async(url, output_file))


# ============================================================
# 阶段二：搜索增强 - 解决地理定位问题
# ============================================================

def search_web_enhanced(query, engine='baidu', output_file=None, 
                        wait_time=5000, use_proxy=False):
    """
    增强版全网搜索
    - 更长的JS渲染等待时间
    - 强制地理位置设置
    - 失败重试机制
    """
    from playwright.sync_api import sync_playwright
    from urllib.parse import quote
    
    query_enc = quote(query)
    
    engines = {
        'baidu': ('https://www.baidu.com/s?wd={q}', 'zh-CN,zh;q=0.9'),
        'google': ('https://www.google.com/search?q={q}&gl=cn&hl=zh-CN', 'zh-CN,zh;q=0.9,en;q=0.8'),
        'bing': ('https://www.bing.com/search?q={q}&mkt=zh-CN', 'zh-CN,zh;q=0.9'),
    }
    
    if engine not in engines:
        engine = 'baidu'
    
    url_template, accept_lang = engines[engine]
    url = url_template.format(q=query_enc)
    
    # 搜索结果缓存目录
    cache_dir = 'C:/Users/ericz/.openclaw/workspace/search_cache'
    os.makedirs(cache_dir, exist_ok=True)
    
    # 默认输出文件
    if not output_file:
        safe_query = query.replace(' ', '_')[:30]
        output_file = os.path.join(cache_dir, f'{engine}_{safe_query}.html')
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--lang=zh-CN',
            ]
        )
        
        context = browser.new_context(
            permissions=['geolocation'],
            geolocation={'latitude': 29.5647, 'longitude': 106.5507},
            locale='zh-CN',
            extra_http_headers={
                'Accept-Language': accept_lang,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }
        )
        page = context.new_page()
        
        # 语言和地理已在context设置
        pass
        
        try:
            print(f'  [search] 访问: {url[:80]}...')
            page.goto(url, timeout=25000, wait_until='domcontentloaded')
            
            # 延长等待时间，让JS完全渲染
            print(f'  [wait] 等待 {wait_time}ms 让JS渲染...')
            
            # 方案1：等待搜索结果元素出现
            try:
                page.wait_for_selector('li.b_algo, div.b_algo, #b_results', 
                                       timeout=wait_time)
                print(f'  [found] 搜索结果元素已出现')
            except Exception as e:
                print(f'  [wait fallback] 继续等待...{e}')
                page.wait_for_timeout(wait_time - 3000)
            
            # 尝试关闭可能弹出的验证对话框
            try:
                page.keyboard.press('Escape')
                page.wait_for_timeout(500)
            except:
                pass
            
            # 滚动页面触发懒加载
            try:
                page.evaluate('window.scrollTo(0, document.body.scrollHeight / 2)')
                page.wait_for_timeout(1000)
                page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                page.wait_for_timeout(1000)
            except:
                pass
            
            text = page.content()
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            print(f'  [OK] -> {len(text)} chars -> {output_file}')
            
        except Exception as e:
            print(f'  [ERROR] {e}')
            # 失败重试一次
            print(f'  [retry] 等待2秒后重试...')
            time.sleep(2)
            try:
                page = context.new_page()
                page.goto(url, timeout=30000, wait_until='domcontentloaded')
                page.wait_for_timeout(wait_time + 2000)
                text = page.content()
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f'  [retry OK] -> {len(text)} chars')
            except Exception as e2:
                print(f'  [retry FAIL] {e2}')
                text = None
        
        browser.close()
        return text


# ============================================================
# 阶段三：搜索结果解析增强
# ============================================================

def parse_search_results(html_file, engine='baidu', max_results=15):
    """解析搜索结果"""
    from bs4 import BeautifulSoup
    
    if not os.path.exists(html_file):
        print(f'[ERROR] 文件不存在: {html_file}')
        return []
    
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    
    if engine == 'baidu':
        # 百度结果：div.result 或 div.c-container
        for item in soup.select('div.result, div.c-container')[:max_results]:
            title_elem = item.select_one('h3 a, h2 a, a.t')
            if title_elem and title_elem.get('href'):
                results.append({
                    'title': title_elem.get_text(strip=True),
                    'url': title_elem.get('href', ''),
                    'snippet': '',
                })
    elif engine == 'google':
        # Google结果：div.g
        for item in soup.select('div.g')[:max_results]:
            title_elem = item.select_one('a[href]')
            if title_elem and 'url' in str(title_elem.get('href', '')):
                results.append({
                    'title': title_elem.get_text(strip=True),
                    'url': title_elem.get('href', ''),
                    'snippet': '',
                })
    elif engine == 'bing':
        # Bing结果：li.b_algo
        for item in soup.select('li.b_algo')[:max_results]:
            title_elem = item.select_one('h2 a')
            if title_elem:
                results.append({
                    'title': title_elem.get_text(strip=True),
                    'url': title_elem.get('href', ''),
                    'snippet': '',
                })
    
    return results


# ============================================================
# 阶段四：智能多引擎搜索
# ============================================================

def smart_search(query, engines=['baidu', 'bing', 'google'], 
                 output_dir='C:/Users/ericz/.openclaw/workspace/search_cache'):
    """
    智能多引擎搜索，自动重试+结果合并
    """
    os.makedirs(output_dir, exist_ok=True)
    all_results = []
    
    for engine in engines:
        print(f'\n[{engine.upper()}] 搜索中...')
        try:
            text = search_web_enhanced(
                query, 
                engine=engine, 
                wait_time=6000,  # 6秒JS渲染等待
                output_file=os.path.join(output_dir, f'{engine}_search.html')
            )
            
            if text and len(text) > 5000:
                results = parse_search_results(
                    os.path.join(output_dir, f'{engine}_search.html'),
                    engine=engine
                )
                print(f'  -> 找到 {len(results)} 条结果')
                all_results.extend(results)
            else:
                print(f'  -> 抓取内容过少，跳过解析')
                
        except Exception as e:
            print(f'  [ERROR] {engine}: {e}')
        
        # 每个引擎间隔2秒
        time.sleep(2)
    
    # 去重
    seen_urls = set()
    unique_results = []
    for r in all_results:
        if r['url'] not in seen_urls and len(r['url']) > 20:
            seen_urls.add(r['url'])
            unique_results.append(r)
    
    print(f'\n[总计] 去重后 {len(unique_results)} 条结果')
    return unique_results


# ============================================================
# 主入口
# ============================================================

if __name__ == '__main__':
    args = sys.argv[1:]
    
    if not args:
        print(__doc__)
        print("\n用法:")
        print("  python scrap_tools.py fetch <url> [output]        # 静态页面")
        print("  python scrap_tools.py dynamic <url> [output]     # JS页面")
        print("  python scrap_tools.py search <query> [engine]   # 搜索 (baidu/bing/google)")
        print("  python scrap_tools.py parse <html> [engine]       # 解析")
        print("  python scrap_tools.py smart <query>              # 多引擎智能搜索")
        sys.exit(0)
    
    mode = args[0]
    
    if mode == 'fetch':
        url = args[1] if len(args) > 1 else input('URL: ')
        out = args[2] if len(args) > 2 else None
        fetch_static(url, out)
    
    elif mode == 'dynamic':
        url = args[1] if len(args) > 1 else input('URL: ')
        out = args[2] if len(args) > 2 else None
        fetch_dynamic(url, out)
    
    elif mode == 'search':
        query = args[1] if len(args) > 1 else input('Query: ')
        engine = args[2] if len(args) > 2 else 'baidu'
        search_web_enhanced(query, engine=engine, wait_time=6000)
    
    elif mode == 'parse':
        html_file = args[1] if len(args) > 1 else input('HTML: ')
        engine = args[2] if len(args) > 2 else 'baidu'
        results = parse_search_results(html_file, engine=engine)
        print(f'\n{len(results)} 条结果:\n')
        for i, r in enumerate(results):
            print(f'{i+1}. {r["title"][:60]}')
            print(f'   {r["url"][:80]}')
    
    elif mode == 'smart':
        query = args[1] if len(args) > 1 else input('Query: ')
        results = smart_search(query)
        print('\n最终结果:')
        for i, r in enumerate(results[:20]):
            print(f'{i+1}. {r["title"][:60]}')
            print(f'   {r["url"][:80]}')
    
    else:
        print(f'未知模式: {mode}')
