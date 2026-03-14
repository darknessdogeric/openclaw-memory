@echo off
chcp 65001 >nul
echo ==========================================
echo    Summarize Skill - 安装脚本
echo    文本摘要技能
echo ==========================================
echo.

echo [1/2] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python
    pause
    exit /b 1
)
echo [✓] Python 已安装
echo.

echo [2/2] 安装依赖...
pip install jieba -q
echo [✓] 依赖安装完成
echo.

echo ==========================================
echo    安装完成！
echo ==========================================
echo.
echo 使用方法:
echo   summarize "你的长文本" -t text
echo   summarize article.md -t text -o summary.json
echo   summarize paper.txt -t paper
echo   summarize chat.txt -t chat
echo.
pause
