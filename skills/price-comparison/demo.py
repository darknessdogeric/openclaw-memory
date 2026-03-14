#!/usr/bin/env python3
"""
Price Comparison Demo - 比价功能演示
"""

from universal_price_compare import UniversalPriceComparator, format_output

def demo():
    """演示比价功能"""
    
    print("="*70)
    print("🛒 全网比价系统演示")
    print("="*70)
    print()
    
    # 测试商品列表
    test_products = [
        "iPhone 16 Pro 256GB",
        "Sony WH-1000XM5",
        "MacBook Air M3 16GB",
        "Nintendo Switch OLED"
    ]
    
    print("可测试的商品:")
    for i, product in enumerate(test_products, 1):
        print(f"  {i}. {product}")
    print()
    
    # 创建比价器
    comparator = UniversalPriceComparator(platforms=['jd'])
    
    # 演示第一个商品
    keyword = test_products[0]
    print(f"🔍 正在比价: {keyword}")
    print("-"*70)
    
    result = comparator.compare(keyword, top_n=3)
    
    if result['success']:
        print(format_output(result))
        
        # 保存结果到文件
        import json
        from datetime import datetime
        
        filename = f"price_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"💾 结果已保存到: {filename}")
    else:
        print(f"❌ 比价失败: {result.get('error')}")
    
    print()
    print("="*70)
    print("提示: 使用命令行运行: price-compare.bat '商品名称'")
    print("="*70)


if __name__ == '__main__':
    demo()
