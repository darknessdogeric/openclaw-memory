#!/usr/bin/env python3
"""
Price Cache Manager - 价格缓存管理系统
基于Redis的价格缓存和历史记录
"""

import json
import hashlib
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import redis


@dataclass
class PriceHistory:
    """价格历史记录"""
    timestamp: str
    price: float
    platform: str
    shop_name: str


@dataclass
class CachedPrice:
    """缓存的价格数据"""
    keyword: str
    platform: str
    sku_id: str
    title: str
    price: float
    original_price: Optional[float]
    shop_name: str
    url: str
    cached_at: str
    expires_at: str
    query_count: int = 1


class PriceCacheManager:
    """价格缓存管理器"""
    
    DEFAULT_TTL = 3600  # 默认缓存1小时
    HISTORY_TTL = 7 * 24 * 3600  # 历史记录保留7天
    
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        """
        初始化缓存管理器
        
        Args:
            host: Redis主机
            port: Redis端口
            db: Redis数据库
        """
        try:
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                db=db,
                decode_responses=True,
                socket_connect_timeout=5
            )
            self.redis_client.ping()
            self.enabled = True
            print("✅ Redis连接成功")
        except Exception as e:
            print(f"⚠️ Redis连接失败: {e}")
            print("   将使用内存缓存（重启后丢失）")
            self.enabled = False
            self.memory_cache = {}
    
    def _generate_cache_key(self, keyword: str, platform: str) -> str:
        """生成缓存key"""
        key_str = f"{platform}:{keyword.lower().strip()}"
        return f"price:{hashlib.md5(key_str.encode()).hexdigest()}"
    
    def _generate_history_key(self, sku_id: str, platform: str) -> str:
        """生成历史记录key"""
        return f"history:{platform}:{sku_id}"
    
    def get_cached_price(self, keyword: str, platform: str) -> Optional[Dict]:
        """
        获取缓存的价格
        
        Args:
            keyword: 商品关键词
            platform: 平台
            
        Returns:
            缓存数据或None
        """
        cache_key = self._generate_cache_key(keyword, platform)
        
        if self.enabled:
            try:
                data = self.redis_client.get(cache_key)
                if data:
                    cached = json.loads(data)
                    # 检查是否过期
                    expires = datetime.fromisoformat(cached['expires_at'])
                    if datetime.now() < expires:
                        # 增加查询计数
                        cached['query_count'] = cached.get('query_count', 0) + 1
                        self.redis_client.setex(
                            cache_key,
                            self.DEFAULT_TTL,
                            json.dumps(cached)
                        )
                        return cached
                    else:
                        # 已过期，删除
                        self.redis_client.delete(cache_key)
            except Exception as e:
                print(f"读取缓存失败: {e}")
        else:
            # 内存缓存
            if cache_key in self.memory_cache:
                cached = self.memory_cache[cache_key]
                expires = datetime.fromisoformat(cached['expires_at'])
                if datetime.now() < expires:
                    cached['query_count'] = cached.get('query_count', 0) + 1
                    return cached
                else:
                    del self.memory_cache[cache_key]
        
        return None
    
    def cache_price(self, 
                   keyword: str,
                   platform: str,
                   product_data: Dict,
                   ttl: int = None):
        """
        缓存价格数据
        
        Args:
            keyword: 商品关键词
            platform: 平台
            product_data: 商品数据
            ttl: 过期时间（秒）
        """
        ttl = ttl or self.DEFAULT_TTL
        cache_key = self._generate_cache_key(keyword, platform)
        
        cached = CachedPrice(
            keyword=keyword,
            platform=platform,
            sku_id=product_data.get('sku_id', product_data.get('goods_id', '')),
            title=product_data.get('title', ''),
            price=product_data.get('price', 0),
            original_price=product_data.get('original_price'),
            shop_name=product_data.get('shop_name', ''),
            url=product_data.get('url', ''),
            cached_at=datetime.now().isoformat(),
            expires_at=(datetime.now() + timedelta(seconds=ttl)).isoformat()
        )
        
        data = asdict(cached)
        
        if self.enabled:
            try:
                self.redis_client.setex(
                    cache_key,
                    ttl,
                    json.dumps(data)
                )
            except Exception as e:
                print(f"写入缓存失败: {e}")
        else:
            self.memory_cache[cache_key] = data
        
        # 同时记录价格历史
        self._record_price_history(cached)
    
    def _record_price_history(self, cached: CachedPrice):
        """记录价格历史"""
        if not cached.sku_id:
            return
        
        history_key = self._generate_history_key(cached.sku_id, cached.platform)
        
        history_entry = PriceHistory(
            timestamp=datetime.now().isoformat(),
            price=cached.price,
            platform=cached.platform,
            shop_name=cached.shop_name
        )
        
        data = asdict(history_entry)
        
        if self.enabled:
            try:
                # 使用列表存储历史记录
                self.redis_client.lpush(history_key, json.dumps(data))
                # 设置过期时间
                self.redis_client.expire(history_key, self.HISTORY_TTL)
                # 只保留最近100条
                self.redis_client.ltrim(history_key, 0, 99)
            except Exception as e:
                print(f"记录历史失败: {e}")
    
    def get_price_history(self, sku_id: str, platform: str, days: int = 7) -> List[Dict]:
        """
        获取价格历史
        
        Args:
            sku_id: 商品ID
            platform: 平台
            days: 查询天数
            
        Returns:
            历史价格列表
        """
        history_key = self._generate_history_key(sku_id, platform)
        
        if self.enabled:
            try:
                data_list = self.redis_client.lrange(history_key, 0, -1)
                history = [json.loads(d) for d in data_list]
                
                # 过滤时间范围
                cutoff = datetime.now() - timedelta(days=days)
                history = [
                    h for h in history 
                    if datetime.fromisoformat(h['timestamp']) > cutoff
                ]
                
                return sorted(history, key=lambda x: x['timestamp'])
            except Exception as e:
                print(f"读取历史失败: {e}")
                return []
        
        return []
    
    def get_price_trend(self, sku_id: str, platform: str) -> Dict:
        """
        获取价格趋势分析
        
        Args:
            sku_id: 商品ID
            platform: 平台
            
        Returns:
            趋势分析数据
        """
        history = self.get_price_history(sku_id, platform, days=30)
        
        if not history:
            return {
                'has_data': False,
                'message': '暂无历史数据'
            }
        
        prices = [h['price'] for h in history]
        
        # 计算趋势
        if len(prices) >= 2:
            first_price = prices[-1]  # 最早的价格
            last_price = prices[0]    # 最新的价格
            change = last_price - first_price
            change_pct = (change / first_price) * 100 if first_price > 0 else 0
            
            trend = 'up' if change > 0 else 'down' if change < 0 else 'stable'
        else:
            trend = 'unknown'
            change = 0
            change_pct = 0
        
        return {
            'has_data': True,
            'trend': trend,
            'current_price': prices[0],
            'lowest_price': min(prices),
            'highest_price': max(prices),
            'average_price': sum(prices) / len(prices),
            'price_change': change,
            'price_change_pct': change_pct,
            'data_points': len(prices),
            'history': history[:10]  # 最近10条
        }
    
    def clear_expired(self):
        """清理过期缓存"""
        # Redis自动过期，无需手动清理
        if not self.enabled:
            # 清理内存缓存中的过期项
            now = datetime.now()
            expired_keys = []
            for key, data in self.memory_cache.items():
                expires = datetime.fromisoformat(data['expires_at'])
                if now > expires:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self.memory_cache[key]
            
            print(f"清理了 {len(expired_keys)} 个过期缓存")
    
    def get_cache_stats(self) -> Dict:
        """获取缓存统计"""
        if self.enabled:
            try:
                info = self.redis_client.info()
                return {
                    'enabled': True,
                    'used_memory': info.get('used_memory_human', 'N/A'),
                    'total_keys': self.redis_client.dbsize(),
                    'connected_clients': info.get('connected_clients', 0)
                }
            except:
                return {'enabled': True, 'error': '无法获取统计'}
        else:
            return {
                'enabled': False,
                'memory_items': len(self.memory_cache)
            }
    
    def close(self):
        """关闭连接"""
        if self.enabled and self.redis_client:
            self.redis_client.close()


class PriceMonitor:
    """价格监控器 - 监控价格变化并告警"""
    
    def __init__(self, cache_manager: PriceCacheManager):
        self.cache = cache_manager
    
    def check_price_drop(self, 
                        keyword: str, 
                        platform: str, 
                        current_price: float) -> Optional[Dict]:
        """
        检查是否降价
        
        Args:
            keyword: 商品关键词
            platform: 平台
            current_price: 当前价格
            
        Returns:
            降价信息或None
        """
        cached = self.cache.get_cached_price(keyword, platform)
        
        if cached and cached['price'] > current_price:
            drop_amount = cached['price'] - current_price
            drop_pct = (drop_amount / cached['price']) * 100
            
            return {
                'alert_type': 'price_drop',
                'keyword': keyword,
                'platform': platform,
                'old_price': cached['price'],
                'new_price': current_price,
                'drop_amount': drop_amount,
                'drop_percentage': drop_pct,
                'title': cached['title'],
                'url': cached['url']
            }
        
        return None
    
    def check_lowest_price(self,
                          sku_id: str,
                          platform: str,
                          current_price: float) -> Optional[Dict]:
        """
        检查是否历史最低价
        
        Args:
            sku_id: 商品ID
            platform: 平台
            current_price: 当前价格
            
        Returns:
            最低价提醒或None
        """
        trend = self.cache.get_price_trend(sku_id, platform)
        
        if trend['has_data'] and current_price <= trend['lowest_price']:
            return {
                'alert_type': 'lowest_price',
                'sku_id': sku_id,
                'platform': platform,
                'current_price': current_price,
                'previous_lowest': trend['lowest_price'],
                'message': '这是30天内的最低价格！'
            }
        
        return None
    
    def set_price_alert(self,
                       keyword: str,
                       platform: str,
                       target_price: float,
                       email: Optional[str] = None) -> bool:
        """
        设置价格提醒
        
        Args:
            keyword: 商品关键词
            platform: 平台
            target_price: 目标价格（低于此价格时提醒）
            email: 通知邮箱
            
        Returns:
            是否设置成功
        """
        alert_key = f"alert:{platform}:{hashlib.md5(keyword.encode()).hexdigest()}"
        
        alert_data = {
            'keyword': keyword,
            'platform': platform,
            'target_price': target_price,
            'email': email,
            'created_at': datetime.now().isoformat(),
            'active': True
        }
        
        if self.cache.enabled:
            try:
                self.cache.redis_client.set(
                    alert_key,
                    json.dumps(alert_data)
                )
                return True
            except Exception as e:
                print(f"设置提醒失败: {e}")
                return False
        
        return False
    
    def check_alerts(self, keyword: str, platform: str, current_price: float) -> List[Dict]:
        """检查触发的提醒"""
        triggered = []
        
        # 检查降价
        drop_alert = self.check_price_drop(keyword, platform, current_price)
        if drop_alert:
            triggered.append(drop_alert)
        
        return triggered


# 使用示例
def demo():
    """演示缓存功能"""
    
    # 创建缓存管理器
    cache = PriceCacheManager()
    
    # 模拟缓存数据
    product = {
        'sku_id': '12345',
        'title': 'iPhone 16 Pro',
        'price': 8999,
        'original_price': 9999,
        'shop_name': 'Apple旗舰店',
        'url': 'https://example.com/item/12345'
    }
    
    # 缓存价格
    cache.cache_price('iPhone 16 Pro', 'jd', product)
    print("✅ 价格已缓存")
    
    # 读取缓存
    cached = cache.get_cached_price('iPhone 16 Pro', 'jd')
    if cached:
        print(f"💾 缓存数据: {cached['title']} ¥{cached['price']}")
    
    # 获取统计
    stats = cache.get_cache_stats()
    print(f"📊 缓存统计: {stats}")
    
    cache.close()


if __name__ == '__main__':
    demo()
