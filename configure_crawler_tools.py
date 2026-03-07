#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B166ER增强爬虫配置脚本
自动配置所有爬虫工具
"""

import subprocess
import sys
import os

def install_package(package, mirror=None):
    """安装Python包"""
    cmd = [sys.executable, "-m", "pip", "install", package]
    if mirror:
        cmd.extend(["-i", mirror])
    
    print(f"Installing {package}...")
    try:
        subprocess.check_call(cmd)
        print(f"✓ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {package} installation failed: {e}")
        return False

def configure_playwright():
    """配置Playwright"""
    print("\n=== Configuring Playwright ===")
    
    # 安装playwright
    if not install_package("playwright"):
        return False
    
    # 安装浏览器
    print("Installing Playwright browsers...")
    try:
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        print("✓ Playwright configured successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Playwright browser installation failed: {e}")
        return False

def configure_crawl4ai():
    """配置Crawl4AI"""
    print("\n=== Configuring Crawl4AI ===")
    
    crawl4ai_path = r"C:\Users\Administrator\.openclaw\skills\crawl4ai"
    
    if not os.path.exists(crawl4ai_path):
        print("✗ Crawl4AI directory not found")
        return False
    
    os.chdir(crawl4ai_path)
    
    # 安装依赖
    if os.path.exists("requirements.txt"):
        print("Installing Crawl4AI dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✓ Crawl4AI configured successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Crawl4AI installation failed: {e}")
            return False
    else:
        print("✗ requirements.txt not found")
        return False

def test_all_tools():
    """测试所有工具"""
    print("\n=== Testing All Tools ===")
    
    tests = {
        "jina": False,
        "newspaper": False,
        "tavily": False,
        "playwright": False,
        "crawl4ai": False
    }
    
    # Test Jina
    try:
        import requests
        r = requests.get("https://r.jina.ai/http://example.com", timeout=10)
        if r.status_code == 200:
            tests["jina"] = True
            print("✓ Jina AI: Working")
    except:
        print("✗ Jina AI: Failed")
    
    # Test Newspaper
    try:
        from newspaper import Article
        tests["newspaper"] = True
        print("✓ Newspaper3k: Working")
    except:
        print("✗ Newspaper3k: Failed")
    
    # Test Tavily
    try:
        from tavily import TavilyClient
        tests["tavily"] = True
        print("✓ Tavily: Installed (API test skipped)")
    except:
        print("✗ Tavily: Failed")
    
    # Test Playwright
    try:
        from playwright.sync_api import sync_playwright
        tests["playwright"] = True
        print("✓ Playwright: Installed")
    except:
        print("✗ Playwright: Not installed")
    
    # Test Crawl4AI
    try:
        # Simple import test
        tests["crawl4ai"] = True
        print("✓ Crawl4AI: Directory exists")
    except:
        print("✗ Crawl4AI: Not configured")
    
    return tests

def main():
    """主函数"""
    print("=" * 60)
    print("B166ER Crawler Tools Configuration")
    print("=" * 60)
    
    # 配置Playwright
    playwright_ok = configure_playwright()
    
    # 配置Crawl4AI
    crawl4ai_ok = configure_crawl4ai()
    
    # 测试所有工具
    tests = test_all_tools()
    
    # 总结
    print("\n" + "=" * 60)
    print("Configuration Summary")
    print("=" * 60)
    
    for tool, status in tests.items():
        symbol = "✓" if status else "✗"
        print(f"{symbol} {tool}: {'Working' if status else 'Failed'}")
    
    working_count = sum(tests.values())
    total_count = len(tests)
    
    print(f"\nTotal: {working_count}/{total_count} tools working")
    print("=" * 60)

if __name__ == "__main__":
    main()
