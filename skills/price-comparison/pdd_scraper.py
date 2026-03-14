#!/usr/bin/env python3
"""
PDD Scraper - 拼多多专用抓取器
使用App模拟或小程序接口
"""

import requests
import json
import re
import time
import random
import hashlib
from typing import List, Dict, Optional
from dataclasses import dataclass
from urllib.parse import quote


@dataclass
class PDDProduct:
    """拼多多商品数据结构"""
    goods_id: str
    title: str
    price: float
    original_price: float
    discount: str
    sales: str
    shop_name: str
    shop_type: str  # 旗舰店/专营店/普通店
    rating: float
    url: str
    image: str


class PDDScraper:
    """拼多多抓取器"""
    
    # 拼多多搜索API（需要逆向获取真实接口）
    SEARCH_URL = "https://mobile.yangkeduo.com/search_result.html"
    API_BASE = "https://api.pinduoduo.com"
    
    def __init__(self):
        self.session = requests.Session()
        self.device_id = self._generate_device_id()
        self.headers = self._get_headers()
        self._init_session()
    
    def _generate_device_id(self) -> str:
        """生成设备ID"""
        import uuid
        return hashlib.md5(uuid.uuid4().hex.encode()).hexdigest()[:16]
    
    def _get_headers(self) -> Dict:
        """获取拼多多请求头（模拟APP）"""
        return {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Origin': 'https://mobile.yangkeduo.com',
            'Referer': 'https://mobile.yangkeduo.com/',
            'Connection': 'keep-alive',
            'X-Requested-With': 'com.xunmeng.pinduoduo'
        }
    
    def _init_session(self):
        """初始化会话"""
        self.session.headers.update(self.headers)
        
        # 访问首页获取Cookie
        try:
            self.session.get('https://mobile.yangkeduo.com', timeout=10)
            time.sleep(random.uniform(1, 2))
        except:
            pass
    
    def _random_delay(self, min_sec: float = 1.5, max_sec: float = 3.5):
        """随机延迟"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)
    
    def search_web(self, keyword: str, page: int = 1) -> List[PDDProduct]:
        """
        通过网页版搜索（稳定性较好）
        
        Args:
            keyword: 搜索关键词
            page: 页码
            
        Returns:
            商品列表
        """
        params = {
            'search_key': keyword,
            'page': page,
            'sort': 'default',  # default, price_asc, price_desc, sales
            'requery': '0'
        }
        
        try:
            self._random_delay()
            
            response = self.session.get(
                self.SEARCH_URL,
                params=params,
                timeout=15
            )
            response.raise_for_status()
            
            # 解析HTML
            products = self._parse_web_search(response.text)
            
            return products
            
        except Exception as e:
            print(f"拼多多搜索失败: {e}")
            return []
    
    def _parse_web_search(self, html: str) -> List[PDDProduct]:
        """解析网页版搜索结果"""
        products = []
        
        try:
            # 拼多多商品数据通常在 window.rawData 中
            import re
            
            # 提取 rawData
            raw_data_match = re.search(r'window\.rawData\s*=\s*({.*?});', html, re.DOTALL)
            if raw_data_match:
                raw_data = json.loads(raw_data_match.group(1))
                
                # 解析商品列表
                items = raw_data.get('store', {}).get('data', {}).get('ssrListData', {}).get('list', [])
                
                for item in items:
                    try:
                        goods_id = str(item.get('goodsId', ''))
                        title = item.get('goodsName', '')
                        
                        # 价格转换（分 -> 元）
                        price = item.get('price', 0) / 100
                        original_price = item.get('marketPrice', 0) / 100
                        
                        # 销量
                        sales = item.get('salesTip', '0')
                        
                        # 店铺
                        shop_name = item.get('mallName', '未知店铺')
                        
                        # 店铺类型
                        mall_cps = item.get('mallCps', 0)
                        if mall_cps == 1:
                            shop_type = '旗舰店'
                        elif mall_cps == 2:
                            shop_type = '专营店'
                        else:
                            shop_type = '普通店'
                        
                        # 评分
                        rating = item.get('avgStar', 0)
                        
                        product = PDDProduct(
                            goods_id=goods_id,
                            title=title,
                            price=price,
                            original_price=original_price,
                            discount=self._calc_discount(price, original_price),
                            sales=sales,
                            shop_name=shop_name,
                            shop_type=shop_type,
                            rating=rating,
                            url=f"https://mobile.yangkeduo.com/goods.html?goods_id={goods_id}",
                            image=item.get('goodsImageUrl', '')
                        )
                        products.append(product)
                        
                    except Exception as e:
                        print(f"解析商品失败: {e}")
                        continue
            
        except Exception as e:
            print(f"解析搜索结果失败: {e}")
        
        return products
    
    def _calc_discount(self, price: float, original_price: float) -> str:
        """计算折扣"""
        if original_price > 0 and original_price > price:
            discount_pct = (1 - price / original_price) * 100
            return f"{discount_pct:.0f}% off"
        return ""
    
    def search_api(self, keyword: str, page: int = 1) -> List[PDDProduct]:
        """
        通过API搜索（需要逆向获取真实接口参数）
        
        注意：拼多多的API有严格的签名验证，需要逆向APP获取签名算法
        """
        # 这是一个示例，实际参数需要通过逆向获取
        params = {
            'opt_id': '0',
            'page': page,
            'size': '20',
            'key': keyword,
            'sort_type': '0',  # 0-综合, 1-销量, 2-价格升序, 3-价格降序
        }
        
        # 生成签名（需要逆向获取算法）
        # sign = self._generate_sign(params)
        # params['sign'] = sign
        
        try:
            # 实际API端点需要通过逆向获取
            # response = self.session.get(
            #     f"{self.API_BASE}/api/...",
            #     params=params,
            #     timeout=15
            # )
            pass
            
        except Exception as e:
            print(f"API搜索失败: {e}")
        
        return []
    
    def _generate_sign(self, params: Dict) -> str:
        """
        生成API签名（需要逆向获取算法）
        
        拼多多的签名算法通常包括：
        1. 参数排序
        2. 拼接字符串
        3. MD5/SHA1加密
        4. 添加时间戳和随机数
        """
        # 示例伪代码
        sorted_params = sorted(params.items())
        param_str = '&'.join([f"{k}={v}" for k, v in sorted_params])
        
        # 添加密钥（需要逆向获取）
        secret_key = "your_secret_key"
        sign_str = f"{param_str}{secret_key}"
        
        return hashlib.md5(sign_str.encode()).hexdigest()
    
    def get_goods_detail(self, goods_id: str) -> Optional[Dict]:
        """获取商品详情"""
        url = f"https://mobile.yangkeduo.com/goods.html?goods_id={goods_id}"
        
        try:
            self._random_delay(2, 4)
            response = self.session.get(url, timeout=15)
            
            # 解析详情页
            html = response.text
            
            # 提取商品信息
            raw_data_match = re.search(r'window\.rawData\s*=\s*({.*?});', html, re.DOTALL)
            if raw_data_match:
                raw_data = json.loads(raw_data_match.group(1))
                
                goods_data = raw_data.get('store', {}).get('goods', {})
                
                return {
                    'goods_id': goods_id,
                    'title': goods_data.get('goodsName', ''),
                    'price': goods_data.get('minOnSaleGroupPrice', 0) / 100,
                    'original_price': goods_data.get('minGroupPrice', 0) / 100,
                    'sales': goods_data.get('sales', 0),
                    'desc': goods_data.get('goodsDesc', ''),
                    'url': url
                }
            
        except Exception as e:
            print(f"获取详情失败: {e}")
        
        return None


class PDDPriceComparison:
    """拼多多比价器"""
    
    def __init__(self):
        self.scraper = PDDScraper()
    
    def compare(self, keyword: str, top_n: int = 3) -> Dict:
        """比价"""
        print(f"🔍 正在拼多多搜索: {keyword}...")
        
        # 使用网页版搜索
        products = self.scraper.search_web(keyword, page=1)
        
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
            'platform': '拼多多',
            'total_found': len(products),
            'results': [self._product_to_dict(p) for p in top_products],
            'best_option': best
        }
    
    def _find_best_option(self, products: List[PDDProduct]) -> Dict:
        """找出最佳选项"""
        if not products:
            return {}
        
        # 拼多多优先选择百亿补贴或旗舰店
        for p in products:
            if '旗舰' in p.shop_type:
                return {
                    'platform': '拼多多',
                    'goods_id': p.goods_id,
                    'title': p.title,
                    'price': p.price,
                    'shop_name': p.shop_name,
                    'url': p.url,
                    'reason': '旗舰店'
                }
        
        # 返回最低价
        cheapest = min(products, key=lambda x: x.price)
        return {
            'platform': '拼多多',
            'goods_id': cheapest.goods_id,
            'title': cheapest.title,
            'price': cheapest.price,
            'shop_name': cheapest.shop_name,
            'url': cheapest.url,
            'reason': '最低价'
        }
    
    def _product_to_dict(self, product: PDDProduct) -> Dict:
        """转换为字典"""
        return {
            'goods_id': product.goods_id,
            'title': product.title,
            'price': product.price,
            'original_price': product.original_price,
            'discount': product.discount,
            'sales': product.sales,
            'shop_name': product.shop_name,
            'shop_type': product.shop_type,
            'rating': product.rating,
            'url': product.url
        }


def main():
    """测试入口"""
    import sys
    
    keyword = sys.argv[1] if len(sys.argv) > 1 else "iPhone 16 Pro"
    
    comparator = PDDPriceComparison()
    result = comparator.compare(keyword)
    
    if result['success']:
        print(f"\n{'='*60}")
        print(f"🔍 拼多多比价结果: {result['keyword']}")
        print(f"{'='*60}\n")
        
        for i, p in enumerate(result['results'], 1):
            print(f"{i}. {p['title'][:40]}...")
            print(f"   💰 ¥{p['price']:.0f}", end="")
            if p['original_price'] > 0:
                print(f" (原价 ¥{p['original_price']:.0f})", end="")
            print()
            if p['discount']:
                print(f"   🏷️ {p['discount']}")
            print(f"   🏪 {p['shop_name']} ({p['shop_type']})")
            print(f"   📈 销量: {p['sales']}")
            print(f"   🔗 {p['url']}\n")
        
        best = result['best_option']
        print(f"{'='*60}")
        print(f"🏆 最佳选项")
        print(f"{'='*60}")
        print(f"平台: {best['platform']}")
        print(f"商品: {best['title'][:50]}")
        print(f"价格: ¥{best['price']:.0f}")
        print(f"店铺: {best['shop_name']}")
        print(f"理由: {best['reason']}")
        print(f"链接: {best['url']}")
    else:
        print(f"❌ {result['error']}")


if __name__ == '__main__':
    main()
