#!/usr/bin/env python3
"""
Proxy Pool Manager - 代理池管理系统
自动管理、验证、轮换代理IP
"""

import requests
import asyncio
import aiohttp
import random
import time
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import threading


@dataclass
class Proxy:
    """代理数据结构"""
    ip: str
    port: int
    protocol: str  # http, https, socks5
    anonymity: str  # transparent, anonymous, elite
    country: str
    region: str
    source: str  # 代理来源
    response_time: float = 0.0
    success_count: int = 0
    fail_count: int = 0
    last_used: Optional[datetime] = None
    last_checked: Optional[datetime] = None
    is_active: bool = True
    is_banned: Dict[str, bool] = None  # 被哪些平台封禁
    
    def __post_init__(self):
        if self.is_banned is None:
            self.is_banned = {}
    
    @property
    def url(self) -> str:
        """获取代理URL"""
        return f"{self.protocol}://{self.ip}:{self.port}"
    
    @property
    def score(self) -> float:
        """计算代理评分"""
        if self.success_count + self.fail_count == 0:
            return 50.0
        
        success_rate = self.success_count / (self.success_count + self.fail_count)
        
        # 响应时间评分 (0-30分)
        if self.response_time < 1:
            speed_score = 30
        elif self.response_time < 3:
            speed_score = 20
        elif self.response_time < 5:
            speed_score = 10
        else:
            speed_score = 5
        
        # 匿名度评分 (0-20分)
        anonymity_scores = {
            'elite': 20,
            'anonymous': 15,
            'transparent': 5
        }
        anonymity_score = anonymity_scores.get(self.anonymity, 10)
        
        # 成功率评分 (0-50分)
        success_score = success_rate * 50
        
        return speed_score + anonymity_score + success_score
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'ip': self.ip,
            'port': self.port,
            'protocol': self.protocol,
            'anonymity': self.anonymity,
            'country': self.country,
            'region': self.region,
            'source': self.source,
            'response_time': self.response_time,
            'success_count': self.success_count,
            'fail_count': self.fail_count,
            'score': self.score,
            'is_active': self.is_active,
            'is_banned': self.is_banned
        }


class ProxyFetcher:
    """代理获取器 - 从各种来源获取代理"""
    
    def __init__(self):
        self.sources = {
            'free': [
                # 免费代理API（示例）
                'http://api.ipify.org?format=json',  # 获取本机IP
            ],
            'paid': []  # 付费代理API配置
        }
    
    def fetch_from_free_apis(self) -> List[Proxy]:
        """从免费API获取代理"""
        proxies = []
        
        # 这里可以集成多个免费代理API
        # 示例：爬取免费代理网站
        
        return proxies
    
    def fetch_from_paid_api(self, api_url: str, api_key: str) -> List[Proxy]:
        """从付费API获取代理"""
        proxies = []
        
        try:
            response = requests.get(
                api_url,
                headers={'Authorization': f'Bearer {api_key}'},
                timeout=30
            )
            data = response.json()
            
            # 解析不同格式的代理数据
            for item in data.get('data', []):
                proxy = Proxy(
                    ip=item.get('ip'),
                    port=item.get('port'),
                    protocol=item.get('protocol', 'http'),
                    anonymity=item.get('anonymity', 'anonymous'),
                    country=item.get('country', 'CN'),
                    region=item.get('region', ''),
                    source='paid_api'
                )
                proxies.append(proxy)
                
        except Exception as e:
            print(f"获取付费代理失败: {e}")
        
        return proxies
    
    def load_from_file(self, filepath: str) -> List[Proxy]:
        """从文件加载代理列表"""
        proxies = []
        
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    # 格式: ip:port 或 protocol://ip:port
                    proxy = self._parse_proxy_line(line)
                    if proxy:
                        proxies.append(proxy)
                        
        except FileNotFoundError:
            print(f"代理文件不存在: {filepath}")
        
        return proxies
    
    def _parse_proxy_line(self, line: str) -> Optional[Proxy]:
        """解析代理行"""
        try:
            if '://' in line:
                protocol, address = line.split('://')
                ip, port = address.split(':')
            else:
                ip, port = line.split(':')
                protocol = 'http'
            
            return Proxy(
                ip=ip,
                port=int(port),
                protocol=protocol,
                anonymity='anonymous',
                country='CN',
                region='',
                source='file'
            )
        except:
            return None


class ProxyValidator:
    """代理验证器"""
    
    TEST_URLS = {
        'jd': 'https://www.jd.com',
        'taobao': 'https://www.taobao.com',
        'tmall': 'https://www.tmall.com',
        'common': 'http://httpbin.org/ip'
    }
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
    
    async def validate_proxy(self, proxy: Proxy, test_platform: str = 'common') -> Tuple[bool, float]:
        """
        验证代理是否可用
        
        Returns:
            (是否可用, 响应时间)
        """
        test_url = self.TEST_URLS.get(test_platform, self.TEST_URLS['common'])
        
        proxy_url = proxy.url
        proxies = {
            'http': proxy_url,
            'https': proxy_url
        }
        
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    test_url,
                    proxy=proxy_url,
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                    headers={'User-Agent': 'Mozilla/5.0'}
                ) as response:
                    elapsed = time.time() - start_time
                    
                    if response.status == 200:
                        return True, elapsed
                    else:
                        return False, elapsed
                        
        except Exception as e:
            elapsed = time.time() - start_time
            return False, elapsed
    
    async def validate_proxies(self, proxies: List[Proxy], test_platform: str = 'common') -> List[Proxy]:
        """批量验证代理"""
        tasks = []
        for proxy in proxies:
            task = self.validate_proxy(proxy, test_platform)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        valid_proxies = []
        for proxy, result in zip(proxies, results):
            if isinstance(result, Exception):
                proxy.is_active = False
                proxy.fail_count += 1
            else:
                is_valid, response_time = result
                proxy.response_time = response_time
                proxy.last_checked = datetime.now()
                
                if is_valid:
                    proxy.is_active = True
                    proxy.success_count += 1
                    valid_proxies.append(proxy)
                else:
                    proxy.is_active = False
                    proxy.fail_count += 1
        
        return valid_proxies


class ProxyPool:
    """代理池管理器"""
    
    def __init__(self, 
                 min_pool_size: int = 10,
                 max_pool_size: int = 100,
                 validation_interval: int = 300):
        """
        初始化代理池
        
        Args:
            min_pool_size: 最小代理数量
            max_pool_size: 最大代理数量
            validation_interval: 验证间隔（秒）
        """
        self.min_pool_size = min_pool_size
        self.max_pool_size = max_pool_size
        self.validation_interval = validation_interval
        
        self.proxies: List[Proxy] = []
        self.current_index = 0
        self.lock = threading.Lock()
        
        self.fetcher = ProxyFetcher()
        self.validator = ProxyValidator()
        
        # 平台特定代理池
        self.platform_pools: Dict[str, List[Proxy]] = {
            'jd': [],
            'taobao': [],
            'tmall': []
        }
    
    def load_proxies(self, source: str = 'file', **kwargs):
        """加载代理"""
        if source == 'file':
            filepath = kwargs.get('filepath', 'proxies.txt')
            new_proxies = self.fetcher.load_from_file(filepath)
        elif source == 'paid_api':
            api_url = kwargs.get('api_url')
            api_key = kwargs.get('api_key')
            new_proxies = self.fetcher.fetch_from_paid_api(api_url, api_key)
        else:
            new_proxies = []
        
        with self.lock:
            self.proxies.extend(new_proxies)
            print(f"加载了 {len(new_proxies)} 个代理")
    
    async def validate_all(self, test_platform: str = 'common'):
        """验证所有代理"""
        print(f"开始验证 {len(self.proxies)} 个代理...")
        
        valid_proxies = await self.validator.validate_proxies(
            self.proxies, 
            test_platform
        )
        
        with self.lock:
            self.proxies = valid_proxies
        
        print(f"验证完成，有效代理: {len(valid_proxies)}/{len(self.proxies)}")
        return valid_proxies
    
    def get_proxy(self, platform: str = 'common', strategy: str = 'random') -> Optional[Proxy]:
        """
        获取一个代理
        
        Args:
            platform: 目标平台
            strategy: 选择策略 (random, round_robin, best_score)
            
        Returns:
            Proxy对象或None
        """
        with self.lock:
            # 过滤可用代理
            available = [
                p for p in self.proxies 
                if p.is_active and not p.is_banned.get(platform, False)
            ]
            
            if not available:
                return None
            
            if strategy == 'random':
                return random.choice(available)
            
            elif strategy == 'round_robin':
                proxy = available[self.current_index % len(available)]
                self.current_index += 1
                return proxy
            
            elif strategy == 'best_score':
                return max(available, key=lambda p: p.score)
            
            else:
                return random.choice(available)
    
    def report_result(self, proxy: Proxy, platform: str, success: bool):
        """报告代理使用结果"""
        with self.lock:
            if success:
                proxy.success_count += 1
            else:
                proxy.fail_count += 1
                # 连续失败3次，标记为该平台不可用
                if proxy.fail_count >= 3:
                    proxy.is_banned[platform] = True
            
            proxy.last_used = datetime.now()
    
    def remove_proxy(self, proxy: Proxy):
        """移除代理"""
        with self.lock:
            if proxy in self.proxies:
                self.proxies.remove(proxy)
    
    def get_stats(self) -> Dict:
        """获取代理池统计"""
        with self.lock:
            total = len(self.proxies)
            active = len([p for p in self.proxies if p.is_active])
            banned_by_platform = {}
            
            for platform in ['jd', 'taobao', 'tmall']:
                banned_by_platform[platform] = len([
                    p for p in self.proxies 
                    if p.is_banned.get(platform, False)
                ])
            
            return {
                'total': total,
                'active': active,
                'inactive': total - active,
                'banned_by_platform': banned_by_platform,
                'avg_score': sum(p.score for p in self.proxies) / total if total > 0 else 0
            }
    
    def save_to_file(self, filepath: str = 'proxies_validated.txt'):
        """保存有效代理到文件"""
        with self.lock:
            valid_proxies = [p for p in self.proxies if p.is_active]
            
        with open(filepath, 'w') as f:
            for proxy in valid_proxies:
                f.write(f"{proxy.url}\n")
        
        print(f"已保存 {len(valid_proxies)} 个有效代理到 {filepath}")


class ProxyMiddleware:
    """代理中间件 - 集成到抓取器"""
    
    def __init__(self, proxy_pool: ProxyPool):
        self.proxy_pool = proxy_pool
        self.max_retries = 3
    
    def request_with_proxy(self, url: str, platform: str, **kwargs) -> requests.Response:
        """
        使用代理发送请求，自动处理失败重试
        
        Args:
            url: 请求URL
            platform: 目标平台
            **kwargs: requests的其他参数
            
        Returns:
            Response对象
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            proxy = self.proxy_pool.get_proxy(platform, strategy='best_score')
            
            if not proxy:
                # 没有可用代理，直接请求
                return requests.get(url, **kwargs)
            
            try:
                proxies = {
                    'http': proxy.url,
                    'https': proxy.url
                }
                
                response = requests.get(
                    url,
                    proxies=proxies,
                    timeout=kwargs.get('timeout', 10),
                    **{k: v for k, v in kwargs.items() if k != 'timeout'}
                )
                
                # 报告成功
                self.proxy_pool.report_result(proxy, platform, True)
                return response
                
            except Exception as e:
                last_exception = e
                # 报告失败
                self.proxy_pool.report_result(proxy, platform, False)
                print(f"代理 {proxy.url} 请求失败，重试 {attempt + 1}/{self.max_retries}")
                time.sleep(1)
        
        # 所有重试都失败
        raise last_exception or Exception("所有代理都失败")


# 使用示例
def demo():
    """代理池使用演示"""
    
    # 创建代理池
    pool = ProxyPool(min_pool_size=5, max_pool_size=50)
    
    # 从文件加载代理
    pool.load_proxies(source='file', filepath='proxies.txt')
    
    # 验证代理
    asyncio.run(pool.validate_all())
    
    # 获取统计
    stats = pool.get_stats()
    print(f"\n代理池统计: {stats}")
    
    # 获取代理
    proxy = pool.get_proxy(platform='jd', strategy='best_score')
    if proxy:
        print(f"\n获取到代理: {proxy.url} (评分: {proxy.score:.1f})")
    
    # 保存有效代理
    pool.save_to_file()


if __name__ == '__main__':
    demo()
