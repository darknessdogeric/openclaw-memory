# -*- coding: utf-8 -*-
"""Stealth search - bypass anti-bot for search engines"""
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
import time
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def create_stealth_driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--disable-blink-features=AutomationControlled')
    opts.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    opts.add_experimental_option('excludeSwitches', ['enable-automation'])
    opts.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=opts)
    
    stealth(driver,
        languages=['zh-CN', 'zh', 'en-US', 'en'],
        vendor='Google Inc.',
        platform='Win32',
        webgl_vendor='Intel Inc.',
        renderer='Intel Iris OpenGL Engine',
        fix_hairline=True,
        hide_webdriver=True,
    )
    
    return driver

def search_baidu(query, max_results=10):
    """Search Baidu with stealth mode"""
    driver = create_stealth_driver()
    results = []
    
    try:
        # First verify we can load baidu
        driver.get('https://www.baidu.com')
        time.sleep(2)
        
        # Navigate to search
        search_url = f'https://www.baidu.com/s?wd={query}&rn={max_results}'
        driver.get(search_url)
        time.sleep(5)
        
        # Check if blocked
        page_text = driver.page_source
        if '百度安全验证' in page_text or 'security' in page_text.lower():
            print('[BLOCKED] Baidu security verification')
            return results
        
        # Parse results - Baidu uses class="result" or "c-container"
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(page_text, 'html.parser')
        
        # Try different selectors
        items = soup.select('div.result') or soup.select('div.c-container') or soup.select('h3.t > a')
        
        if not items:
            # Try to find any links
            for a in soup.find_all('a', href=True)[:max_results]:
                title = a.get_text(strip=True)
                href = a.get('href', '')
                if title and 'baidu.com' not in href and len(title) > 5:
                    results.append({'title': title, 'url': href})
        else:
            for item in items[:max_results]:
                a = item.find('a') if item.name != 'a' else item
                if a:
                    title = a.get_text(strip=True)
                    href = a.get('href', '')
                    if title:
                        results.append({'title': title, 'url': href})
        
        print(f'[OK] Found {len(results)} results from Baidu')
        for r in results[:5]:
            print(f'  - {r["title"][:60]}')
            print(f'    {r["url"][:80]}')
        
    except Exception as e:
        print(f'[ERROR] {e}')
    finally:
        driver.quit()
    
    return results

def search_sogou(query, max_results=10):
    """Search Sogou with stealth mode"""
    driver = create_stealth_driver()
    results = []
    
    try:
        search_url = f'https://www.sogou.com/web?query={query}&num={max_results}'
        driver.get(search_url)
        time.sleep(6)
        
        # Check if blocked
        page_text = driver.page_source
        if '验证码' in page_text:
            print('[BLOCKED] Sogou verification')
            return results
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(page_text, 'html.parser')
        
        items = soup.select('div.vrwrap') or soup.select('div.rb') or soup.select('h3.pt a')
        
        for item in items[:max_results]:
            a = item.find('a') if item.name != 'a' else item
            if a:
                title = a.get_text(strip=True)
                href = a.get('href', '')
                if title and len(title) > 5:
                    results.append({'title': title, 'url': href})
        
        print(f'[OK] Found {len(results)} results from Sogou')
        for r in results[:5]:
            print(f'  - {r["title"][:60]}')
            print(f'    {r["url"][:80]}')
        
    except Exception as e:
        print(f'[ERROR] {e}')
    finally:
        driver.quit()
    
    return results

if __name__ == '__main__':
    query = '新华酒店管理公司 两江假日集团'
    
    print(f'=== Searching: {query} ===\n')
    
    print('[BAIDU]')
    baidu_results = search_baidu(query)
    
    print('\n[SOGOU]')
    sogou_results = search_sogou(query)
    
    print(f'\n[Total] Baidu: {len(baidu_results)}, Sogou: {len(sogou_results)}')
