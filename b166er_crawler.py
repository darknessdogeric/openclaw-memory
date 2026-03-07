#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B166ER统一爬虫接口
整合多个免费爬虫工具，智能选择最佳方案
"""

import requests
import json
import time
from typing import Dict, List, Tuple, Optional
from urllib.parse import urlparse

class B166ERCrawler:
    """
    B166ER统一爬虫接口
    智能选择最佳爬虫工具，自动降级处理
    """
    
    def __init__(self):
        self.tools_status = {
            'jina': True,           # ✅ 免费，无需配置
            'newspaper': True,      # ✅ 已安装
            'tavily': True,         # ✅ 已安装
            'duckduckgo': False,    # ❌ 安装失败
            'playwright': True,     # ✅ 已安装（浏览器下载中）
            'crawl4ai': False,      # ⏳ 待部署
        }
        
        # Tavily API Key (已配置)
        self.tavily_api_key = "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"
        
        # 请求统计
        self.stats = {
            'total_requests': 0,
            'success_count': 0,
            'fail_count': 0,
            'tool_usage': {}
        }
    
    def read_url(self, url: str, method: str = 'auto') -> Tuple[Optional[str], str]:
        """
        读取URL内容
        
        Args:
            url: 目标URL
            method: 使用方法 ('auto', 'jina', 'newspaper')
        
        Returns:
            (内容, 使用的工具/状态)
        """
        self.stats['total_requests'] += 1
        
        if method == 'auto':
            return self._smart_read(url)
        
        tool_map = {
            'jina': self._jina_read,
            'newspaper': self._newspaper_read
        }
        
        tool_func = tool_map.get(method)
        if tool_func:
            result, status = tool_func(url)
            self._update_stats(method, status == 'success')
            return result, status
        
        return None, f"Unknown method: {method}"
    
    def _smart_read(self, url: str) -> Tuple[Optional[str], str]:
        """智能选择最佳工具读取URL"""
        
        # 尝试1: Jina AI (最快，免费)
        if self.tools_status['jina']:
            result, status = self._jina_read(url)
            if status == 'success':
                self._update_stats('jina', True)
                return result, 'jina'
        
        # 尝试2: Newspaper3k (新闻专用)
        if self.tools_status['newspaper']:
            try:
                result, status = self._newspaper_read(url)
                if status == 'success':
                    self._update_stats('newspaper', True)
                    return result, 'newspaper'
            except:
                pass
        
        # 尝试3: Playwright (JS渲染)
        if self.tools_status['playwright']:
            try:
                result, status = self._playwright_read(url)
                if status == 'success':
                    self._update_stats('playwright', True)
                    return result, 'playwright'
            except:
                pass
        
        self.stats['fail_count'] += 1
        return None, "All methods failed"
    
    def _jina_read(self, url: str) -> Tuple[Optional[str], str]:
        """使用Jina AI Reader读取URL"""
        try:
            # 确保URL格式正确
            if not url.startswith('http'):
                url = 'http://' + url
            
            jina_url = f"https://r.jina.ai/http://{url.replace('http://', '').replace('https://', '')}"
            
            response = requests.get(jina_url, timeout=30)
            
            if response.status_code == 200:
                return response.text, 'success'
            else:
                return None, f"Jina AI HTTP {response.status_code}"
                
        except requests.Timeout:
            return None, "Jina AI Timeout"
        except Exception as e:
            return None, f"Jina AI Error: {str(e)}"
    
    def _newspaper_read(self, url: str) -> Tuple[Optional[Dict], str]:
        """使用Newspaper3k读取URL"""
        try:
            from newspaper import Article
            
            article = Article(url)
            article.download()
            article.parse()
            
            result = {
                'title': article.title,
                'text': article.text,
                'authors': article.authors,
                'publish_date': str(article.publish_date) if article.publish_date else None,
                'top_image': article.top_image,
                'url': url
            }
            
            return result, 'success'
            
        except Exception as e:
            return None, f"Newspaper Error: {str(e)}"
    
    def search(self, query: str, engine: str = 'auto', max_results: int = 10) -> Tuple[Optional[List], str]:
        """
        搜索查询
        
        Args:
            query: 搜索关键词
            engine: 搜索引擎 ('auto', 'tavily', 'duckduckgo')
            max_results: 最大结果数
        
        Returns:
            (结果列表, 使用的引擎/状态)
        """
        self.stats['total_requests'] += 1
        
        if engine == 'auto':
            return self._smart_search(query, max_results)
        
        tool_map = {
            'tavily': self._tavily_search,
            'duckduckgo': self._ddg_search
        }
        
        tool_func = tool_map.get(engine)
        if tool_func:
            result, status = tool_func(query, max_results)
            self._update_stats(engine, status == 'success')
            return result, status
        
        return None, f"Unknown engine: {engine}"
    
    def _smart_search(self, query: str, max_results: int = 10) -> Tuple[Optional[List], str]:
        """智能选择最佳搜索引擎"""
        
        # 尝试1: Tavily (质量高，有免费额度)
        if self.tools_status['tavily']:
            try:
                result, status = self._tavily_search(query, max_results)
                if status == 'success':
                    self._update_stats('tavily', True)
                    return result, 'tavily'
            except:
                pass
        
        # 尝试2: DuckDuckGo (完全免费)
        if self.tools_status['duckduckgo']:
            try:
                result, status = self._ddg_search(query, max_results)
                if status == 'success':
                    self._update_stats('duckduckgo', True)
                    return result, 'duckduckgo'
            except:
                pass
        
        self.stats['fail_count'] += 1
        return None, "All search engines failed"
    
    def _tavily_search(self, query: str, max_results: int = 10) -> Tuple[Optional[List], str]:
        """使用Tavily搜索"""
        try:
            from tavily import TavilyClient
            
            client = TavilyClient(api_key=self.tavily_api_key)
            result = client.search(query, max_results=max_results)
            
            # 格式化结果
            formatted_results = []
            for item in result.get('results', []):
                formatted_results.append({
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'content': item.get('content', ''),
                    'score': item.get('score', 0)
                })
            
            return formatted_results, 'success'
            
        except Exception as e:
            return None, f"Tavily Error: {str(e)}"
    
    def _ddg_search(self, query: str, max_results: int = 10) -> Tuple[Optional[List], str]:
        """使用DuckDuckGo搜索"""
        try:
            from duckduckgo_search import DDGS
            
            with DDGS() as ddgs:
                results = ddgs.text(query, max_results=max_results)
                formatted_results = []
                
                for r in results:
                    formatted_results.append({
                        'title': r.get('title', ''),
                        'url': r.get('href', ''),
                        'content': r.get('body', ''),
                        'score': None
                    })
                
                return formatted_results, 'success'
                
        except Exception as e:
            return None, f"DuckDuckGo Error: {str(e)}"
    
    def _playwright_read(self, url: str, wait_for: str = None, timeout: int = 30000) -> Tuple[Optional[str], str]:
        """使用Playwright读取URL (支持JS渲染)"""
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=timeout)
                
                # 等待页面加载
                if wait_for:
                    page.wait_for_selector(wait_for, timeout=10000)
                else:
                    page.wait_for_load_state('networkidle', timeout=10000)
                
                content = page.content()
                browser.close()
                
                return content, 'success'
                
        except Exception as e:
            return None, f"Playwright Error: {str(e)}"
    
    def _update_stats(self, tool: str, success: bool):
        """更新使用统计"""
        if tool not in self.stats['tool_usage']:
            self.stats['tool_usage'][tool] = {'success': 0, 'fail': 0}
        
        if success:
            self.stats['success_count'] += 1
            self.stats['tool_usage'][tool]['success'] += 1
        else:
            self.stats['fail_count'] += 1
            self.stats['tool_usage'][tool]['fail'] += 1
    
    def get_stats(self) -> Dict:
        """获取使用统计"""
        return {
            'total_requests': self.stats['total_requests'],
            'success_count': self.stats['success_count'],
            'fail_count': self.stats['fail_count'],
            'success_rate': f"{(self.stats['success_count'] / max(self.stats['total_requests'], 1) * 100):.1f}%",
            'tool_usage': self.stats['tool_usage']
        }
    
    def update_tool_status(self, tool: str, status: bool):
        """更新工具状态"""
        if tool in self.tools_status:
            self.tools_status[tool] = status
            print(f"Tool '{tool}' status updated: {status}")


# 使用示例和测试
if __name__ == '__main__':
    crawler = B166ERCrawler()
    
    print("=" * 60)
    print("B166ER Crawler Test")
    print("=" * 60)
    
    # 测试1: 读取URL
    print("\nTest 1: Read URL")
    print("-" * 40)
    url = "https://example.com"
    content, method = crawler.read_url(url)
    print(f"URL: {url}")
    print(f"Method: {method}")
    if content:
        print(f"Content length: {len(content)} chars")
        print(f"Preview: {content[:200]}...")
    else:
        print("Failed to read")
    
    # 测试2: 搜索
    print("\nTest 2: Search")
    print("-" * 40)
    query = "Python web scraping"
    results, engine = crawler.search(query, max_results=3)
    print(f"Query: {query}")
    print(f"Engine: {engine}")
    if results:
        print(f"Results: {len(results)}")
        for i, r in enumerate(results[:2]):
            print(f"  {i+1}. {r.get('title', 'N/A')}")
    else:
        print("Search failed")
    
    # 统计
    print("\nTest 3: Statistics")
    print("-" * 40)
    stats = crawler.get_stats()
    print(f"Total requests: {stats['total_requests']}")
    print(f"Success rate: {stats['success_rate']}")
    print(f"Tool usage: {stats['tool_usage']}")
    
    print("\n" + "=" * 60)
    print("Test completed")
    print("=" * 60)
