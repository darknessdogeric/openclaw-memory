#!/bin/bash
# Price Comparison Skill - 全网比价工具

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ $# -eq 0 ]; then
    echo "=========================================="
    echo "   Price Comparison Skill - 全网比价工具"
    echo "=========================================="
    echo ""
    echo "使用方法:"
    echo "  price-compare \"商品名称\""
    echo "  price-compare \"iPhone 16 Pro\" --platforms jd,tmall,pdd"
    echo "  price-compare \"Sony WH-1000XM5\" --json"
    echo ""
    echo "支持平台: jd, taobao, tmall, pdd, amazon, suning"
    exit 1
fi

python3 "$SCRIPT_DIR/price_comparison.py" "$@"
