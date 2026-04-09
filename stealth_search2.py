# -*- coding: utf-8 -*-
"""Stealth search - bypass anti-bot for search engines"""
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
import time
import sys
import io
from urllib.parse import parse_qs, urlparse
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def create_stealth_driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--disable-blink-features=AutomationControlled')
    opts.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    opts.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(options=opts)
    stealth(driver,
        languages=['zh-CN', 'zh', 'en-US', 'en'],
        vendor='Google Inc.', platform='Win32',
        webgl_vendor='Intel Inc.', renderer='Intel Iris OpenGL Engine',
        fix_hairline=True, hide_webdriver=True,
    )
    return driver

def get_real_url(redirect_url):
    """Convert sogou redirect URL to real URL"""
    if redirect_url.startswith('/link?'):
        try:
            params = parse_qs(urlparse(redirect_url).query)
            return params.get('url', [''])[0]
        except:
            return ''
    return redirect_url

def search_sogou(query, max_results=10):
    driver = create_stealth_driver()
    results = []
    
    try:
        search_url = f'https://www.sogou.com/web?query={query}&num={max_results}'
        driver.get(search_url)
        time.sleep(6)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Sogou result structure: div.vrwrap contains h3.pt > a
        for item in soup.select('div.vrwrap')[:max_results]:
            links = item.find_all('a')
            title = ''
            href = ''
            for a in links:
                t = a.get_text(strip=True)
                if t and len(t) > 10:
                    title = t
                    href = a.get('href', '')
                    break
            if title:
                real_url = get_real_url(href)
                results.append({'title': title, 'url': real_url})
        
        print(f'[SOGOU] Found {len(results)} results')
        for r in results:
            print(f'  {r["title"][:80]}')
            print(f'  -> {r["url"][:100]}')
            print()
        
    except Exception as e:
        print(f'[ERROR] {e}')
    finally:
        driver.quit()
    
    return results

def search_bing(query, max_results=10):
    driver = create_stealth_driver()
    results = []
    
    try:
        search_url = f'https://www.bing.com/search?q={query}&mkt=zh-CN'
        driver.get(search_url)
        time.sleep(8)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        for item in soup.select('li.b_algo')[:max_results]:
            a = item.select_one('h2 a')
            if a:
                title = a.get_text(strip=True)
                href = a.get('href', '')
                if title:
                    results.append({'title': title, 'url': href})
        
        print(f'[BING] Found {len(results)} results')
        for r in results:
            print(f'  {r["title"][:80]}')
            print(f'  -> {r["url"][:100]}')
            print()
            
    except Exception as e:
        print(f'[ERROR] {e}')
    finally:
        driver.quit()
    
    return results

if __name__ == '__main__':
    query = '新华酒店管理公司 两江假日集团 新华渝北酒店'
    
    print(f'=== Stealth Search: {query} ===\n')
    
    print('[SOGOU]')
    s_results = search_sogou(query)
    
    print('\n[BING]')
    b_results = search_bing(query)
    
    print(f'\nTotal: Sogou={len(s_results)}, Bing={len(b_results)}')
