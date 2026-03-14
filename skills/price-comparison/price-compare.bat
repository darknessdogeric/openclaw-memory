@echo off
chcp 65001 >nul
echo ==========================================
echo    Universal Price Comparison - 全网比价
echo ==========================================
echo.
echo 支持平台: 京东、淘宝、天猫
echo.
echo 使用方法:
echo   price-compare "商品名称"
echo   price-compare "iPhone 16 Pro 256GB" --platforms jd,taobao
echo   price-compare "Sony WH-1000XM5" --no-headless
echo   price-compare "MacBook Air" --json
echo.

if "%~1"=="" (
    echo 错误: 请提供商品名称
    pause
    exit /b 1
)

cd /d "%~dp0"
python "universal_price_compare.py" %*
