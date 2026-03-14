#!/usr/bin/env python3
"""
Price Comparison Skill - Main Module
Compare prices across multiple e-commerce platforms
"""

import json
import time
import re
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

@dataclass
class PriceResult:
    platform: str
    title: str
    price: float
    original_price: Optional[float] = None
    coupon: Optional[str] = None
    final_price: float = 0.0
    seller: str = ""
    rating: float = 0.0
    sales: int = 0
    delivery: str = ""
    url: str = ""
    recommendation_score: int = 0

class PriceComparator:
    """Main price comparison engine"""
    
    SUPPORTED_PLATFORMS = ["jd", "taobao", "tmall", "pdd", "amazon", "suning"]
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.cache = {}
        
    def _load_config(self, path: Optional[str]) -> Dict:
        """Load configuration"""
        default_config = {
            "default_platforms": ["jd", "taobao", "tmall", "pdd"],
            "timeout": 30,
            "cache_duration": 3600,
            "alert_threshold": 0.05
        }
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return {**default_config, **json.load(f)}
            except:
                pass
        return default_config
    
    def compare(self, query: str, platforms: Optional[List[str]] = None) -> Dict:
        """
        Compare prices across platforms
        
        Args:
            query: Product name to search
            platforms: List of platforms to search (default: all)
            
        Returns:
            Dictionary with comparison results
        """
        platforms = platforms or self.config["default_platforms"]
        timestamp = datetime.now().isoformat()
        
        results = []
        for platform in platforms:
            try:
                result = self._search_platform(platform, query)
                if result:
                    results.append(result)
            except Exception as e:
                print(f"Error searching {platform}: {e}")
                continue
        
        # Sort by final price
        results.sort(key=lambda x: x.final_price if x.final_price else x.price)
        
        # Calculate recommendation scores
        results = self._calculate_scores(results)
        
        return {
            "query": query,
            "timestamp": timestamp,
            "results": [asdict(r) for r in results],
            "best_option": self._get_best_option(results),
            "summary": self._generate_summary(results)
        }
    
    def _search_platform(self, platform: str, query: str) -> Optional[PriceResult]:
        """Search a specific platform"""
        search_methods = {
            "jd": self._search_jd,
            "taobao": self._search_taobao,
            "tmall": self._search_tmall,
            "pdd": self._search_pdd,
            "amazon": self._search_amazon,
            "suning": self._search_suning
        }
        
        method = search_methods.get(platform)
        if method:
            return method(query)
        return None
    
    def _search_jd(self, query: str) -> Optional[PriceResult]:
        """Search JD.com"""
        # Placeholder - would use actual scraping or API
        return PriceResult(
            platform="京东",
            title=f"{query} (示例数据)",
            price=8999.0,
            original_price=9999.0,
            coupon="满8000减500",
            final_price=8499.0,
            seller="京东自营",
            rating=4.9,
            sales=50000,
            delivery="次日达",
            url=f"https://search.jd.com/Search?keyword={query}",
            recommendation_score=0
        )
    
    def _search_taobao(self, query: str) -> Optional[PriceResult]:
        """Search Taobao"""
        return PriceResult(
            platform="淘宝",
            title=f"{query} (示例数据)",
            price=8799.0,
            original_price=None,
            coupon="店铺券减200",
            final_price=8599.0,
            seller="金牌卖家",
            rating=4.8,
            sales=12000,
            delivery="3-5天",
            url=f"https://s.taobao.com/search?q={query}",
            recommendation_score=0
        )
    
    def _search_tmall(self, query: str) -> Optional[PriceResult]:
        """Search Tmall"""
        return PriceResult(
            platform="天猫",
            title=f"{query} 官方旗舰店 (示例数据)",
            price=8999.0,
            original_price=9999.0,
            coupon="会员专享减300",
            final_price=8699.0,
            seller="官方旗舰店",
            rating=4.9,
            sales=80000,
            delivery="次日达",
            url=f"https://list.tmall.com/search_product.htm?q={query}",
            recommendation_score=0
        )
    
    def _search_pdd(self, query: str) -> Optional[PriceResult]:
        """Search Pinduoduo"""
        return PriceResult(
            platform="拼多多",
            title=f"{query} 百亿补贴 (示例数据)",
            price=8299.0,
            original_price=9999.0,
            coupon="百亿补贴",
            final_price=8299.0,
            seller="品牌好货",
            rating=4.7,
            sales=200000,
            delivery="2-3天",
            url=f"https://mobile.yangkeduo.com/search_result.html?search_key={query}",
            recommendation_score=0
        )
    
    def _search_amazon(self, query: str) -> Optional[PriceResult]:
        """Search Amazon China"""
        return PriceResult(
            platform="亚马逊",
            title=f"{query} (示例数据)",
            price=9199.0,
            original_price=9999.0,
            coupon="Prime会员95折",
            final_price=8739.0,
            seller="Amazon自营",
            rating=4.8,
            sales=5000,
            delivery="2-3天",
            url=f"https://www.amazon.cn/s?k={query}",
            recommendation_score=0
        )
    
    def _search_suning(self, query: str) -> Optional[PriceResult]:
        """Search Suning"""
        return PriceResult(
            platform="苏宁",
            title=f"{query} (示例数据)",
            price=8899.0,
            original_price=9999.0,
            coupon="满减活动",
            final_price=8599.0,
            seller="苏宁自营",
            rating=4.8,
            sales=8000,
            delivery="次日达",
            url=f"https://search.suning.com/{query}/",
            recommendation_score=0
        )
    
    def _calculate_scores(self, results: List[PriceResult]) -> List[PriceResult]:
        """Calculate recommendation scores for each result"""
        if not results:
            return results
        
        min_price = min(r.final_price for r in results if r.final_price > 0)
        max_price = max(r.final_price for r in results if r.final_price > 0)
        price_range = max_price - min_price if max_price > min_price else 1
        
        for result in results:
            score = 50  # Base score
            
            # Price factor (40 points max)
            if result.final_price > 0:
                price_score = 40 * (1 - (result.final_price - min_price) / price_range)
                score += max(0, price_score)
            
            # Rating factor (10 points max)
            score += result.rating * 2
            
            # Sales factor (10 points max)
            if result.sales > 100000:
                score += 10
            elif result.sales > 50000:
                score += 8
            elif result.sales > 10000:
                score += 6
            elif result.sales > 1000:
                score += 4
            
            # Delivery factor (10 points max)
            if "次日" in result.delivery or "当天" in result.delivery:
                score += 10
            elif "2" in result.delivery:
                score += 7
            elif "3" in result.delivery:
                score += 5
            
            # Official store bonus
            if "官方" in result.seller or "自营" in result.seller:
                score += 10
            
            result.recommendation_score = int(min(100, score))
        
        return results
    
    def _get_best_option(self, results: List[PriceResult]) -> Dict:
        """Get the best purchase option"""
        if not results:
            return {"error": "No results found"}
        
        # Sort by recommendation score first, then by price
        sorted_results = sorted(
            results, 
            key=lambda x: (-x.recommendation_score, x.final_price)
        )
        
        best = sorted_results[0]
        
        reasons = []
        if best.final_price == min(r.final_price for r in results):
            reasons.append("最低价")
        if best.recommendation_score >= 90:
            reasons.append("高推荐度")
        if "官方" in best.seller or "自营" in best.seller:
            reasons.append("官方保障")
        if "次日" in best.delivery:
            reasons.append("快速配送")
        
        return {
            "platform": best.platform,
            "price": best.final_price,
            "original_price": best.original_price,
            "seller": best.seller,
            "url": best.url,
            "reason": "，".join(reasons) if reasons else "综合最优"
        }
    
    def _generate_summary(self, results: List[PriceResult]) -> Dict:
        """Generate comparison summary"""
        if not results:
            return {}
        
        prices = [r.final_price for r in results if r.final_price > 0]
        
        return {
            "total_platforms": len(results),
            "price_range": {
                "min": min(prices),
                "max": max(prices),
                "avg": sum(prices) / len(prices)
            },
            "savings_potential": max(prices) - min(prices),
            "platforms_checked": [r.platform for r in results]
        }


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Compare prices across e-commerce platforms')
    parser.add_argument('query', help='Product name to search')
    parser.add_argument('--platforms', '-p', help='Comma-separated list of platforms')
    parser.add_argument('--alert', '-a', type=float, help='Set price alert threshold')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    platforms = args.platforms.split(',') if args.platforms else None
    
    comparator = PriceComparator()
    results = comparator.compare(args.query, platforms)
    
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(f"\n🔍 比价结果: {results['query']}\n")
        print("-" * 80)
        
        for r in results['results']:
            print(f"\n📦 {r['platform']}")
            print(f"   价格: ¥{r['final_price']:.0f}", end="")
            if r['original_price']:
                print(f" (原价 ¥{r['original_price']:.0f})", end="")
            print()
            if r['coupon']:
                print(f"   优惠: {r['coupon']}")
            print(f"   商家: {r['seller']} ⭐{r['rating']}")
            print(f"   配送: {r['delivery']}")
            print(f"   推荐度: {'⭐' * (r['recommendation_score'] // 20)}")
        
        print("\n" + "=" * 80)
        best = results['best_option']
        print(f"\n🏆 最佳选项: {best['platform']}")
        print(f"   价格: ¥{best['price']:.0f}")
        print(f"   理由: {best['reason']}")
        print(f"   链接: {best['url']}\n")


if __name__ == '__main__':
    main()
