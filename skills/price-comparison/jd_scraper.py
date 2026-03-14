#!/usr/bin/env python3
"""
JD Scraper - 京东专用抓取器
Phase 1: 基础HTTP抓取 + 简单反爬
"""

import requests
import json
import re
import time
import random
from urllib.parse import quote
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class JDProduct:
    """京东商品数据结构"""
    sku_id: str
    title: str
    price: float
    original_price: Optional[float]
    discount: str
    shop_name: str
    shop_type: str  # 自营/旗舰店/专营店
    rating: float
    comment_count: int
    delivery: str
    url: str
    image: str

class JDScraper:
    """京东抓取器"""
    
    BASE_URL = "https://search.jd.com/Search"
    PRICE_API = "https://p.3.cn/prices/mgets"
    
    def __init__(self, use_proxy: bool = False):
        self.session = requests.Session()
        self.use_proxy = use_proxy
        self.proxy_pool = []
        self._init_session()
    
    def _init_session(self):
        """初始化会话，设置基础请求头"""
        self.session.headers.update({
            'User-Agent': self._get_random_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
        
        # 访问首页获取基础Cookie
        try:
            self.session.get('https://www.jd.com', timeout=10)
            time.sleep(random.uniform(1, 2))
        except:
            pass
    
    def _get_random_ua(self) -> str:
        """获取随机User-Agent"""
        ua_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'
        ]
        return random.choice(ua_list)
    
    def _get_proxy(self) -> Optional[Dict]:
        """获取代理（预留接口）"""
        if self.use_proxy and self.proxy_pool:
            return random.choice(self.proxy_pool)
        return None
    
    def _random_delay(self, min_sec: float = 1.5, max_sec: float = 3.5):
        """随机延迟，模拟人类行为"""
        delay = random.uniform(min_sec, max_sec)
        # 添加正态分布随机性
        delay += random.gauss(0, 0.5)
        delay = max(min_sec, min(max_sec, delay))
        time.sleep(delay)
    
    def search(self, keyword: str, page: int = 1) -> List[JDProduct]:
        """
        搜索商品
        
        Args:
            keyword: 搜索关键词
            page: 页码（每页约30个商品）
            
        Returns:
            商品列表
        """
        params = {
            'keyword': keyword,
            'enc': 'utf-8',
            'page': (page - 1) * 2 + 1,  # 京东页码规则: 1, 3, 5...
            's': (page - 1) * 30,
            'click': '0'
        }
        
        try:
            # 随机延迟
            self._random_delay()
            
            # 发送请求
            response = self.session.get(
                self.BASE_URL,
                params=params,
                proxies=self._get_proxy(),
                timeout=15
            )
            response.raise_for_status()
            
            # 解析商品列表
            products = self._parse_search_page(response.text)
            
            # 获取实时价格
            if products:
                products = self._enrich_prices(products)
            
            return products
            
        except requests.RequestException as e:
            print(f"搜索请求失败: {e}")
            return []
        except Exception as e:
            print(f"解析失败: {e}")
            return []
    
    def _parse_search_page(self, html: str) -> List[JDProduct]:
        """解析搜索页面HTML"""
        products = []
        
        # 京东商品列表选择器
        # 商品信息在 gl-item 或 gl-i-wrap 中
        import re
        
        # 提取商品数据
        # 京东商品数据通常在 pageData 或直接在HTML中
        
        # 方法1: 尝试提取 pageData
        page_data_match = re.search(r'window\.pageData\s*=\s*({.*?});', html, re.DOTALL)
        if page_data_match:
            try:
                page_data = json.loads(page_data_match.group(1))
                # 从pageData提取商品
                # 注意：京东的pageData结构经常变化
            except:
                pass
        
        # 方法2: 正则提取商品信息
        # SKU ID
        sku_pattern = r'data-sku="(\d+)"'
        skus = re.findall(sku_pattern, html)
        
        # 商品标题
        title_pattern = r'<em>([^<]+)</em>'
        titles = re.findall(title_pattern, html)
        
        # 店铺信息
        shop_pattern = r'<a[^>]*title="([^"]+)"[^>]*>\s*<i class="iconfont icon-shop">'
        shops = re.findall(shop_pattern, html)
        
        # 简化处理：提取前N个SKU
        for i, sku in enumerate(skus[:10]):
            title = titles[i] if i < len(titles) else "未知商品"
            shop = shops[i] if i < len(shops) else "未知店铺"
            
            # 判断店铺类型
            shop_type = "自营" if "自营" in shop or "京东" in shop else "第三方"
            
            product = JDProduct(
                sku_id=sku,
                title=title.strip(),
                price=0.0,  # 稍后通过API获取
                original_price=None,
                discount="",
                shop_name=shop.strip(),
                shop_type=shop_type,
                rating=0.0,
                comment_count=0,
                delivery="",
                url=f"https://item.jd.com/{sku}.html",
                image=""
            )
            products.append(product)
        
        return products
    
    def _enrich_prices(self, products: List[JDProduct]) -> List[JDProduct]:
        """通过京东价格API获取实时价格"""
        if not products:
            return products
        
        sku_ids = [p.sku_id for p in products]
        
        # 京东价格API: 支持批量查询
        # 格式: https://p.3.cn/prices/mgets?skuIds=J_100012043978,J_100016133988
        sku_param = ','.join([f'J_{sku}' for sku in sku_ids])
        
        try:
            price_response = self.session.get(
                self.PRICE_API,
                params={'skuIds': sku_param},
                timeout=10
            )
            price_data = price_response.json()
            
            # 构建价格映射
            price_map = {}
            for item in price_data:
                sku = item.get('id', '').replace('J_', '')
                price_map[sku] = {
                    'price': float(item.get('p', 0)),
                    'original_price': float(item.get('m', 0)) if item.get('m') else None,
                    'op_price': float(item.get('op', 0)) if item.get('op') else None
                }
            
            # 更新商品价格
            for product in products:
                if product.sku_id in price_map:
                    price_info = price_map[product.sku_id]
                    product.price = price_info['price']
                    product.original_price = price_info['original_price'] or price_info['op_price']
                    
                    # 计算折扣
                    if product.original_price and product.original_price > product.price:
                        discount_pct = (1 - product.price / product.original_price) * 100
                        product.discount = f"{discount_pct:.0f}% off"
            
        except Exception as e:
            print(f"获取价格失败: {e}")
        
        return products
    
    def get_product_detail(self, sku_id: str) -> Optional[Dict]:
        """
        获取商品详情
        
        Args:
            sku_id: 商品SKU ID
            
        Returns:
            商品详情字典
        """
        url = f"https://item.jd.com/{sku_id}.html"
        
        try:
            self._random_delay(2, 4)
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            # 解析详情页
            html = response.text
            
            # 提取商品名称
            name_match = re.search(r'<div class="sku-name">([^<]+)</div>', html)
            name = name_match.group(1).strip() if name_match else ""
            
            # 提取价格
            price_match = re.search(r'price:\s*"([\d.]+)"', html)
            price = float(price_match.group(1)) if price_match else 0
            
            # 提取评价数
            comment_match = re.search(r'comment-count[^>]*>(\d+)', html)
            comment_count = int(comment_match.group(1)) if comment_match else 0
            
            return {
                'sku_id': sku_id,
                'name': name,
                'price': price,
                'comment_count': comment_count,
                'url': url
            }
            
        except Exception as e:
            print(f"获取详情失败: {e}")
            return None


class JDPriceComparison:
    """京东价格比较器"""
    
    def __init__(self):
        self.scraper = JDScraper()
    
    def compare(self, keyword: str, top_n: int = 5) -> Dict:
        """
        比价并返回最优选项
        
        Args:
            keyword: 商品关键词
            top_n: 返回前N个结果
            
        Returns:
            比价结果字典
        """
        print(f"🔍 正在京东搜索: {keyword}...")
        
        products = self.scraper.search(keyword, page=1)
        
        if not products:
            return {
                'success': False,
                'error': '未找到商品',
                'results': []
            }
        
        # 按价格排序
        products.sort(key=lambda x: x.price)
        
        # 取前N个
        top_products = products[:top_n]
        
        # 找出最优选项
        best = self._find_best_option(top_products)
        
        return {
            'success': True,
            'keyword': keyword,
            'platform': '京东',
            'total_found': len(products),
            'results': [self._product_to_dict(p) for p in top_products],
            'best_option': best,
            'price_range': {
                'min': min(p.price for p in top_products),
                'max': max(p.price for p in top_products)
            }
        }
    
    def _find_best_option(self, products: List[JDProduct]) -> Dict:
        """找出最佳购买选项"""
        if not products:
            return {}
        
        # 评分标准：价格(40%) + 店铺类型(30%) + 评价数(30%)
        scored_products = []
        
        min_price = min(p.price for p in products)
        max_price = max(p.price for p in products)
        price_range = max_price - min_price if max_price > min_price else 1
        
        for p in products:
            score = 0
            
            # 价格分 (40分)
            if price_range > 0:
                price_score = 40 * (1 - (p.price - min_price) / price_range)
                score += price_score
            
            # 店铺类型分 (30分)
            if p.shop_type == "自营":
                score += 30
            elif "旗舰" in p.shop_name:
                score += 25
            else:
                score += 15
            
            # 评价数分 (30分)
            if p.comment_count > 100000:
                score += 30
            elif p.comment_count > 50000:
                score += 25
            elif p.comment_count > 10000:
                score += 20
            elif p.comment_count > 1000:
                score += 15
            else:
                score += 10
            
            scored_products.append((p, score))
        
        # 按分数排序
        scored_products.sort(key=lambda x: x[1], reverse=True)
        best_product, best_score = scored_products[0]
        
        return {
            'sku_id': best_product.sku_id,
            'title': best_product.title,
            'platform': '京东',
            'price': best_product.price,
            'original_price': best_product.original_price,
            'shop_name': best_product.shop_name,
            'shop_type': best_product.shop_type,
            'url': best_product.url,
            'score': int(best_score),
            'reason': self._get_reason(best_product, best_score)
        }
    
    def _get_reason(self, product: JDProduct, score: float) -> str:
        """生成推荐理由"""
        reasons = []
        
        if product.shop_type == "自营":
            reasons.append("京东自营")
        
        if product.original_price and product.original_price > product.price:
            discount = (1 - product.price / product.original_price) * 100
            if discount > 10:
                reasons.append(f"优惠{discount:.0f}%")
        
        if product.comment_count > 50000:
            reasons.append("热销商品")
        
        if score > 80:
            reasons.append("高推荐度")
        
        return "，".join(reasons) if reasons else "综合最优"
    
    def _product_to_dict(self, product: JDProduct) -> Dict:
        """转换商品为字典"""
        return {
            'sku_id': product.sku_id,
            'title': product.title,
            'price': product.price,
            'original_price': product.original_price,
            'discount': product.discount,
            'shop_name': product.shop_name,
            'shop_type': product.shop_type,
            'comment_count': product.comment_count,
            'url': product.url
        }


def main():
    """测试入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python jd_scraper.py '商品名称'")
        print("示例: python jd_scraper.py 'iPhone 16 Pro'")
        return
    
    keyword = sys.argv[1]
    
    comparator = JDPriceComparison()
    result = comparator.compare(keyword)
    
    if result['success']:
        print(f"\n{'='*60}")
        print(f"🔍 比价结果: {result['keyword']}")
        print(f"{'='*60}\n")
        
        for i, p in enumerate(result['results'], 1):
            print(f"{i}. {p['title'][:40]}...")
            print(f"   💰 ¥{p['price']:.0f}", end="")
            if p['original_price']:
                print(f" (原价 ¥{p['original_price']:.0f})", end="")
            print()
            print(f"   🏪 {p['shop_name']} ({p['shop_type']})")
            if p['discount']:
                print(f"   🏷️ {p['discount']}")
            print(f"   🔗 {p['url']}\n")
        
        best = result['best_option']
        print(f"{'='*60}")
        print(f"🏆 最佳选项")
        print(f"{'='*60}")
        print(f"商品: {best['title'][:50]}")
        print(f"价格: ¥{best['price']:.0f}")
        print(f"店铺: {best['shop_name']}")
        print(f"理由: {best['reason']}")
        print(f"链接: {best['url']}")
        print(f"{'='*60}\n")
    else:
        print(f"❌ {result['error']}")


if __name__ == '__main__':
    main()
