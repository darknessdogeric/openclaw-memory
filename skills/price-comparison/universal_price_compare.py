#!/usr/bin/env python3
"""
Universal Price Comparison - 全网比价统一接口 (Phase 3)
整合多个电商平台的比价功能
支持: 京东、淘宝、天猫、拼多多
特性: 代理池、验证码处理、智能重试
"""

import asyncio
import json
import time
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

# 导入各平台抓取器
from jd_scraper import JDPriceComparison

# 淘宝抓取器
try:
    from taobao_scraper import TaobaoPriceComparison
    TAOBAO_AVAILABLE = True
except ImportError:
    TAOBAO_AVAILABLE = False

# 拼多多抓取器
try:
    from pdd_scraper import PDDPriceComparison
    PDD_AVAILABLE = True
except ImportError:
    PDD_AVAILABLE = False

# 代理池
try:
    from proxy_pool import ProxyPool, ProxyMiddleware
    PROXY_AVAILABLE = True
except ImportError:
    PROXY_AVAILABLE = False


@dataclass
class PriceResult:
    """统一价格结果结构"""
    platform: str
    sku_id: str
    title: str
    price: float
    original_price: Optional[float]
    discount: str
    shop_name: str
    shop_type: str
    rating: float
    comment_count: int
    delivery: str
    url: str
    recommendation_score: int = 0


class UniversalPriceComparator:
    """全网比价器 - Phase 3完整版"""
    
    SUPPORTED_PLATFORMS = ['jd', 'taobao', 'tmall', 'pdd']
    
    def __init__(self, 
                 platforms: Optional[List[str]] = None,
                 use_proxy: bool = False,
                 taobao_headless: bool = True):
        """
        初始化比价器
        
        Args:
            platforms: 要查询的平台列表
            use_proxy: 是否使用代理池
            taobao_headless: 淘宝是否使用无头浏览器
        """
        self.platforms = platforms or ['jd']
        self.use_proxy = use_proxy and PROXY_AVAILABLE
        self.taobao_headless = taobao_headless
        
        self.comparators = {}
        self.proxy_pool = None
        self.proxy_middleware = None
        
        self._init_proxy_pool()
        self._init_comparators()
    
    def _init_proxy_pool(self):
        """初始化代理池"""
        if self.use_proxy:
            try:
                self.proxy_pool = ProxyPool(min_pool_size=5)
                # 尝试加载代理
                self.proxy_pool.load_proxies(source='file', filepath='proxies.txt')
                self.proxy_middleware = ProxyMiddleware(self.proxy_pool)
                print(f"✅ 代理池初始化完成")
            except Exception as e:
                print(f"⚠️ 代理池初始化失败: {e}")
                self.use_proxy = False
    
    def _init_comparators(self):
        """初始化各平台比价器"""
        if 'jd' in self.platforms:
            self.comparators['jd'] = JDPriceComparison()
        
        if 'taobao' in self.platforms or 'tmall' in self.platforms:
            if TAOBAO_AVAILABLE:
                self.comparators['taobao'] = TaobaoPriceComparison(
                    headless=self.taobao_headless
                )
            else:
                print("⚠️ 淘宝抓取器未安装")
        
        if 'pdd' in self.platforms:
            if PDD_AVAILABLE:
                self.comparators['pdd'] = PDDPriceComparison()
            else:
                print("⚠️ 拼多多抓取器未安装")
    
    def compare(self, keyword: str, top_n: int = 3) -> Dict:
        """
        全网比价
        
        Args:
            keyword: 商品关键词
            top_n: 每个平台返回前N个结果
            
        Returns:
            统一比价结果
        """
        print(f"🚀 开始全网比价: {keyword}")
        print(f"📊 查询平台: {', '.join(self.platforms)}")
        if self.use_proxy:
            print(f"🌐 使用代理池: 是\n")
        else:
            print(f"🌐 使用代理池: 否\n")
        
        all_results = []
        platform_errors = {}
        
        # 京东查询（同步）
        if 'jd' in self.platforms and 'jd' in self.comparators:
            try:
                print(f"🔍 正在查询 京东...")
                results = self._query_jd(keyword, top_n)
                all_results.extend(results)
                print(f"✅ 京东 查询完成，找到 {len(results)} 个商品\n")
                
                if len(self.platforms) > 1:
                    time.sleep(2)
                    
            except Exception as e:
                print(f"❌ 京东 查询失败: {e}\n")
                platform_errors['jd'] = str(e)
        
        # 淘宝/天猫查询（异步）
        if ('taobao' in self.platforms or 'tmall' in self.platforms) and 'taobao' in self.comparators:
            try:
                print(f"🔍 正在查询 淘宝/天猫...")
                print("⏳ 正在启动浏览器...")
                
                taobao_results = asyncio.run(self._query_taobao(keyword, top_n))
                all_results.extend(taobao_results)
                print(f"✅ 淘宝/天猫 查询完成，找到 {len(taobao_results)} 个商品\n")
                
            except Exception as e:
                print(f"❌ 淘宝/天猫 查询失败: {e}\n")
                platform_errors['taobao'] = str(e)
        
        # 拼多多查询（同步）
        if 'pdd' in self.platforms and 'pdd' in self.comparators:
            try:
                print(f"🔍 正在查询 拼多多...")
                results = self._query_pdd(keyword, top_n)
                all_results.extend(results)
                print(f"✅ 拼多多 查询完成，找到 {len(results)} 个商品\n")
                
            except Exception as e:
                print(f"❌ 拼多多 查询失败: {e}\n")
                platform_errors['pdd'] = str(e)
        
        if not all_results:
            return {
                'success': False,
                'error': '所有平台查询失败',
                'platform_errors': platform_errors,
                'keyword': keyword,
                'results': []
            }
        
        # 排序和评分
        all_results.sort(key=lambda x: (-x.recommendation_score, x.price))
        
        # 找出最优选项
        best_option = self._find_best_option(all_results)
        
        # 按平台分组
        platform_groups = {}
        for r in all_results:
            if r.platform not in platform_groups:
                platform_groups[r.platform] = []
            platform_groups[r.platform].append(r)
        
        return {
            'success': True,
            'keyword': keyword,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_results': len(all_results),
            'platforms_queried': list(platform_groups.keys()),
            'platform_summary': {
                platform: len(items) for platform, items in platform_groups.items()
            },
            'results': [asdict(r) for r in all_results],
            'best_option': best_option,
            'price_analysis': self._analyze_prices(all_results),
            'proxy_used': self.use_proxy
        }
    
    def _query_jd(self, keyword: str, top_n: int) -> List[PriceResult]:
        """查询京东"""
        results = []
        jd_result = self.comparators['jd'].compare(keyword, top_n)
        
        if jd_result['success']:
            for item in jd_result['results']:
                result = PriceResult(
                    platform='京东',
                    sku_id=item['sku_id'],
                    title=item['title'],
                    price=item['price'],
                    original_price=item['original_price'],
                    discount=item['discount'],
                    shop_name=item['shop_name'],
                    shop_type=item['shop_type'],
                    rating=0.0,
                    comment_count=item['comment_count'],
                    delivery='京东配送' if item['shop_type'] == '自营' else '商家配送',
                    url=item['url']
                )
                results.append(result)
        
        return self._calculate_scores(results)
    
    async def _query_taobao(self, keyword: str, top_n: int) -> List[PriceResult]:
        """查询淘宝/天猫"""
        results = []
        taobao_result = await self.comparators['taobao'].compare(keyword, top_n)
        
        if taobao_result['success']:
            for item in taobao_result['results']:
                result = PriceResult(
                    platform=item.get('shop_type', '淘宝'),
                    sku_id=item['item_id'],
                    title=item['title'],
                    price=item['price'],
                    original_price=item.get('original_price'),
                    discount=item.get('discount', ''),
                    shop_name=item['shop_name'],
                    shop_type=item['shop_type'],
                    rating=0.0,
                    comment_count=0,
                    delivery='商家配送',
                    url=item['url']
                )
                results.append(result)
        
        return self._calculate_scores(results)
    
    def _query_pdd(self, keyword: str, top_n: int) -> List[PriceResult]:
        """查询拼多多"""
        results = []
        pdd_result = self.comparators['pdd'].compare(keyword, top_n)
        
        if pdd_result['success']:
            for item in pdd_result['results']:
                result = PriceResult(
                    platform='拼多多',
                    sku_id=item['goods_id'],
                    title=item['title'],
                    price=item['price'],
                    original_price=item['original_price'],
                    discount=item['discount'],
                    shop_name=item['shop_name'],
                    shop_type=item['shop_type'],
                    rating=item['rating'],
                    comment_count=0,
                    delivery='商家配送',
                    url=item['url']
                )
                results.append(result)
        
        return self._calculate_scores(results)
    
    def _calculate_scores(self, results: List[PriceResult]) -> List[PriceResult]:
        """计算推荐分数"""
        if not results:
            return results
        
        platform_min_prices = {}
        for r in results:
            if r.platform not in platform_min_prices:
                platform_min_prices[r.platform] = r.price
            else:
                platform_min_prices[r.platform] = min(platform_min_prices[r.platform], r.price)
        
        global_min = min(r.price for r in results)
        global_max = max(r.price for r in results)
        price_range = global_max - global_min if global_max > global_min else 1
        
        for r in results:
            score = 50
            
            # 价格分
            if price_range > 0:
                price_score = 35 * (1 - (r.price - global_min) / price_range)
                score += max(0, price_score)
            
            # 平台最低价奖励
            if r.price == platform_min_prices.get(r.platform, float('inf')):
                score += 15
            
            # 店铺类型分
            if r.shop_type == '自营' or '官方' in r.shop_name:
                score += 15
            elif '旗舰' in r.shop_name:
                score += 12
            elif '天猫' in r.platform:
                score += 10
            else:
                score += 8
            
            # 评价数分
            if r.comment_count > 100000:
                score += 10
            elif r.comment_count > 50000:
                score += 8
            elif r.comment_count > 10000:
                score += 6
            elif r.comment_count > 1000:
                score += 4
            
            # 配送分
            if '京东' in r.delivery or '次日' in r.delivery:
                score += 10
            elif '2' in r.delivery:
                score += 7
            
            # 折扣分
            if r.discount:
                score += 5
            
            r.recommendation_score = int(min(100, score))
        
        return results
    
    def _find_best_option(self, results: List[PriceResult]) -> Dict:
        """找出最佳选项"""
        if not results:
            return {}
        
        sorted_results = sorted(
            results,
            key=lambda x: (-x.recommendation_score, x.price)
        )
        
        best = sorted_results[0]
        
        reasons = []
        all_prices = [r.price for r in results]
        if best.price == min(all_prices):
            reasons.append(f"全网最低价")
        if best.recommendation_score >= 90:
            reasons.append("高推荐度")
        if best.shop_type == '自营' or '官方' in best.shop_name:
            reasons.append("官方保障")
        if '天猫' in best.platform or '旗舰' in best.shop_name:
            reasons.append("品质保障")
        if '拼多多' in best.platform:
            reasons.append("百亿补贴")
        if best.discount:
            reasons.append("有优惠")
        
        return {
            'platform': best.platform,
            'sku_id': best.sku_id,
            'title': best.title,
            'price': best.price,
            'original_price': best.original_price,
            'discount': best.discount,
            'shop_name': best.shop_name,
            'url': best.url,
            'recommendation_score': best.recommendation_score,
            'reason': '，'.join(reasons) if reasons else '综合最优'
        }
    
    def _analyze_prices(self, results: List[PriceResult]) -> Dict:
        """价格分析"""
        if not results:
            return {}
        
        prices = [r.price for r in results]
        
        platform_stats = {}
        for r in results:
            if r.platform not in platform_stats:
                platform_stats[r.platform] = []
            platform_stats[r.platform].append(r.price)
        
        platform_analysis = {}
        for platform, platform_prices in platform_stats.items():
            platform_analysis[platform] = {
                'min': min(platform_prices),
                'max': max(platform_prices),
                'avg': sum(platform_prices) / len(platform_prices),
                'count': len(platform_prices)
            }
        
        return {
            'global': {
                'min': min(prices),
                'max': max(prices),
                'avg': sum(prices) / len(prices),
                'median': sorted(prices)[len(prices) // 2]
            },
            'by_platform': platform_analysis,
            'savings_potential': max(prices) - min(prices),
            'savings_percentage': (1 - min(prices) / max(prices)) * 100 if max(prices) > 0 else 0
        }


def format_output(result: Dict) -> str:
    """格式化输出结果"""
    if not result['success']:
        lines = [f"❌ 比价失败: {result.get('error', '未知错误')}"]
        if result.get('platform_errors'):
            lines.append("\n各平台错误:")
            for platform, error in result['platform_errors'].items():
                lines.append(f"  {platform}: {error}")
        return "\n".join(lines)
    
    lines = []
    lines.append("\n" + "="*70)
    lines.append(f"🔍 全网比价结果: {result['keyword']}")
    lines.append(f"⏰ 查询时间: {result['timestamp']}")
    lines.append(f"📊 查询平台: {', '.join(result['platforms_queried'])}")
    if result.get('proxy_used'):
        lines.append("🌐 使用代理池")
    lines.append("="*70)
    
    current_platform = None
    for item in result['results']:
        if item['platform'] != current_platform:
            current_platform = item['platform']
            lines.append(f"\n📦 {current_platform}")
            lines.append("-"*70)
        
        lines.append(f"\n  {item['title'][:50]}...")
        price_line = f"  💰 ¥{item['price']:.0f}"
        if item['original_price']:
            price_line += f" (原价 ¥{item['original_price']:.0f})"
        if item['discount']:
            price_line += f" [{item['discount']}]"
        lines.append(price_line)
        
        lines.append(f"  🏪 {item['shop_name']} ({item['shop_type']})")
        lines.append(f"  🚚 {item['delivery']}")
        lines.append(f"  ⭐ 推荐度: {item['recommendation_score']}/100")
        lines.append(f"  🔗 {item['url']}")
    
    best = result['best_option']
    lines.append("\n" + "="*70)
    lines.append("🏆 最佳购买选项")
    lines.append("="*70)
    lines.append(f"平台: {best['platform']}")
    lines.append(f"商品: {best['title'][:60]}")
    lines.append(f"价格: ¥{best['price']:.0f}")
    if best['original_price']:
        lines.append(f"原价: ¥{best['original_price']:.0f}")
    lines.append(f"商家: {best['shop_name']}")
    lines.append(f"推荐: {best['reason']}")
    lines.append(f"评分: {best['recommendation_score']}/100")
    lines.append(f"链接: {best['url']}")
    
    analysis = result['price_analysis']
    if analysis:
        lines.append("\n" + "="*70)
        lines.append("📊 价格分析")
        lines.append("="*70)
        lines.append(f"全网最低价: ¥{analysis['global']['min']:.0f}")
        lines.append(f"全网最高价: ¥{analysis['global']['max']:.0f}")
        lines.append(f"平均价格: ¥{analysis['global']['avg']:.0f}")
        lines.append(f"可节省: ¥{analysis['savings_potential']:.0f} ({analysis['savings_percentage']:.1f}%)")
        
        lines.append("\n各平台对比:")
        for platform, stats in analysis['by_platform'].items():
            lines.append(f"  {platform}: ¥{stats['min']:.0f} - ¥{stats['max']:.0f} (平均 ¥{stats['avg']:.0f}, {stats['count']}个商品)")
    
    lines.append("="*70 + "\n")
    
    return "\n".join(lines)


def main():
    """主入口"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='全网比价工具 v3.0')
    parser.add_argument('keyword', help='商品名称')
    parser.add_argument('--platforms', '-p', default='jd,taobao,pdd',
                       help='查询平台，逗号分隔 (默认: jd,taobao,pdd)')
    parser.add_argument('--use-proxy', action='store_true',
                       help='使用代理池')
    parser.add_argument('--headless', action='store_true', default=True,
                       help='使用无头浏览器 (默认)')
    parser.add_argument('--no-headless', action='store_true',
                       help='显示浏览器窗口（调试用）')
    parser.add_argument('--json', '-j', action='store_true',
                       help='输出JSON格式')
    parser.add_argument('--top-n', '-n', type=int, default=3,
                       help='每个平台返回结果数 (默认: 3)')
    
    args = parser.parse_args()
    
    platforms = args.platforms.split(',')
    headless = not args.no_headless
    
    print(f"🚀 启动全网比价 v3.0...")
    print(f"📦 商品: {args.keyword}")
    print(f"🌐 平台: {', '.join(platforms)}")
    print(f"🌐 代理池: {'开启' if args.use_proxy else '关闭'}")
    print(f"👻 无头模式: {headless}\n")
    
    comparator = UniversalPriceComparator(
        platforms=platforms,
        use_proxy=args.use_proxy,
        taobao_headless=headless
    )
    
    result = comparator.compare(args.keyword, top_n=args.top_n)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_output(result))


if __name__ == '__main__':
    main()
