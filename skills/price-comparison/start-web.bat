@echo off
chcp 65001 >nul
echo ==========================================
echo    Price Comparison Web UI - 启动脚本
echo ==========================================
echo.

cd /d "%~dp0"

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请安装Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖
echo 检查依赖...
pip list | findstr Flask >nul
if errorlevel 1 (
    echo 安装依赖...
    pip install -r requirements.txt
)

echo.
echo 启动Web服务器...
echo 访问地址: http://localhost:5000
echo.

python web_ui.py

pause
