#!/usr/bin/env python3
"""
Amazon FBA Profit Calculator
亚马逊利润计算器

Usage:
python profit_calculator.py

or import:
from profit_calculator import calculate_profit
result = calculate_profit(...)
"""

import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')

from typing import Optional

def format_currency(amount: float, symbol: str = "$") -> str:
    """Format currency"""
    if symbol == "¥":
        return f"RMB {amount:.2f}"
    return f"USD {symbol}{amount:.2f}"

def calculate_fba_fees(product_cost_rmb: float, weight_grams: float, 
                       length_cm: float, width_cm: float, height_cm: float,
                       selling_price_usd: float, exchange_rate: float = 7.2) -> dict:
    """
    计算FBA费用和利润
    
    参数:
    - product_cost_rmb: 产品成本(人民币)
    - weight_grams: 重量(克)
    - length_cm: 长度(cm)
    - width_cm: 宽度(cm)
    - height_cm: 高度(cm)
    - selling_price_usd: 售价(美元)
    - exchange_rate: 汇率(默认7.2)
    
    返回: 费用明细字典
    """
    
    # 基础换算
    product_cost_usd = product_cost_rmb / exchange_rate
    weight_kg = weight_grams / 1000
    
    # 体积重(立方厘米转磅)
    # 166 cubic inches = 1 lb
    volume_cubic_cm = length_cm * width_cm * height_cm
    volume_cubic_inches = volume_cubic_cm / 16.387
    volumetric_weight_lb = volume_cubic_inches / 166
    
    # 实际重量(磅)
    actual_weight_lb = weight_kg * 2.205
    
    # 计费重量(取较大值)
    billable_weight_lb = max(volumetric_weight_lb, actual_weight_lb)
    
    # FBA配送费(标准尺寸，参考2024年)
    # 小号标准: $3.22, 大号标准: $5.00
    if billable_weight_lb <= 0.5:
        fba_fulfillment_fee = 3.22
    elif billable_weight_lb <= 1:
        fba_fulfillment_fee = 3.40
    elif billable_weight_lb <= 2:
        fba_fulfillment_fee = 4.50
    elif billable_weight_lb <= 3:
        fba_fulfillment_fee = 5.00
    else:
        fba_fulfillment_fee = 5.00 + (billable_weight_lb - 3) * 0.38
    
    # 平台佣金(15%)
    referral_fee = selling_price_usd * 0.15
    
    # 头程物流(海运，约$0.6/磅)
    shipping_to_amazon_lb = 0.6
    shipping_cost = billable_weight_lb * shipping_to_amazon_lb * 1.1  # 加10%包装
    
    # 关税估算(假设10%)
    duty_rate = 0.10
    duty_fee = product_cost_usd * duty_rate
    
    # 广告预留(售价的10%)
    ad_reserve = selling_price_usd * 0.10
    
    # 总成本
    total_cost = (product_cost_usd + 
                  shipping_cost + 
                  duty_fee + 
                  referral_fee + 
                  fba_fulfillment_fee + 
                  ad_reserve)
    
    # 利润
    revenue = selling_price_usd * 0.85  # 扣除佣金后的实际收入
    profit = revenue - product_cost_usd - shipping_cost - duty_fee - fba_fulfillment_fee - ad_reserve
    
    # 毛利率
    gross_margin = (profit / selling_price_usd) * 100 if selling_price_usd > 0 else 0
    
    return {
        "selling_price": selling_price_usd,
        "product_cost_usd": product_cost_usd,
        "product_cost_rmb": product_cost_rmb,
        "weight_lb": billable_weight_lb,
        "shipping_cost": shipping_cost,
        "duty_fee": duty_fee,
        "referral_fee": referral_fee,
        "fba_fulfillment_fee": fba_fulfillment_fee,
        "ad_reserve": ad_reserve,
        "total_cost": total_cost,
        "profit": profit,
        "gross_margin": gross_margin,
        "exchange_rate": exchange_rate
    }

def print_result(result: dict):
    """打印结果"""
    print("\n" + "="*50)
    print("亚马逊FBA利润计算结果")
    print("="*50)
    print(f"\n【售价设置】")
    print(f"  建议售价:     {format_currency(result['selling_price'])}")
    
    print(f"\n【成本明细】")
    print(f"  产品成本:     {format_currency(result['product_cost_usd'])} ({format_currency(result['product_cost_rmb'], '¥')})")
    print(f"  头程物流:     {format_currency(result['shipping_cost'])}")
    print(f"  关税(10%):   {format_currency(result['duty_fee'])}")
    print(f"  平台佣金(15%): {format_currency(result['referral_fee'])}")
    print(f"  FBA配送费:   {format_currency(result['fba_fulfillment_fee'])}")
    print(f"  广告预留(10%): {format_currency(result['ad_reserve'])}")
    print(f"  ─────────────────")
    print(f"  总成本:       {format_currency(result['total_cost'])}")
    
    print(f"\n【利润分析】")
    print(f"  预估利润:     {format_currency(result['profit'])}")
    print(f"  毛利率:       {result['gross_margin']:.1f}%")
    
    # 建议
    print(f"\n【建议】")
    if result['gross_margin'] >= 40:
        print(f"  ✅ 毛利率{result['gross_margin']:.1f}%，利润空间良好")
    elif result['gross_margin'] >= 25:
        print(f"  ⚠️ 毛利率{result['gross_margin']:.1f}%，建议优化成本或提高售价")
    else:
        print(f"  ❌ 毛利率{result['gross_margin']:.1f}%，利润空间不足，建议:")
        print(f"     - 寻找更低成本供应商")
        print(f"     - 考虑体积更小的产品")
        print(f"     - 提高售价")
    
    print("="*50)

def interactive_input():
    """交互式输入"""
    print("\n" + "="*50)
    print("亚马逊FBA利润计算器")
    print("="*50)
    
    try:
        # 产品成本
        product_cost_rmb = float(input("\n请输入产品成本(人民币): ¥"))
        
        # 重量
        weight_grams = float(input("请输入产品重量(克): "))
        
        # 尺寸
        print("请输入产品尺寸(cm):")
        length = float(input("  长度: "))
        width = float(input("  宽度: "))
        height = float(input("  高度: "))
        
        # 售价
        selling_price = float(input("\n请输入建议售价(美元): $"))
        
        # 汇率
        exchange = input("请输入汇率(默认7.2，直接回车使用默认): ")
        if not exchange:
            exchange = 7.2
        else:
            exchange = float(exchange)
        
        # 计算
        result = calculate_fba_fees(
            product_cost_rmb=product_cost_rmb,
            weight_grams=weight_grams,
            length_cm=length,
            width_cm=width,
            height_cm=height,
            selling_price_usd=selling_price,
            exchange_rate=exchange
        )
        
        print_result(result)
        
    except ValueError:
        print("\n❌ 输入错误，请输入数字")
    except Exception as e:
        print(f"\n❌ 错误: {e}")

def example():
    """示例计算"""
    print("\n【示例计算】无线充电器")
    result = calculate_fba_fees(
        product_cost_rmb=45,      # ¥45成本
        weight_grams=180,         # 180克
        length_cm=12,             # 12cm
        width_cm=8,              # 8cm
        height_cm=3,             # 3cm
        selling_price_usd=25,     # $25售价
        exchange_rate=7.2
    )
    print_result(result)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--example":
        example()
    elif len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("""
亚马逊FBA利润计算器

使用方法:
  python profit_calculator.py          # 交互式输入
  python profit_calculator.py --example  # 运行示例
  python profit_calculator.py --help   # 显示帮助

功能:
  - 计算FBA配送费
  - 计算平台佣金
  - 计算头程物流和关税
  - 计算预估利润和毛利率
  - 提供优化建议
""")
    else:
        interactive_input()
