@echo off
chcp 65001 >nul
echo ==========================================
echo    MD2ALL Converter - 安装脚本
echo    Markdown转PDF/Word/HTML全能转换器
echo ==========================================
echo.

echo [1/3] 检查Python安装...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [✓] Python已安装
python --version
echo.

echo [2/3] 安装Python依赖包...
echo 正在安装: python-docx, markdown, fpdf2, beautifulsoup4
pip install python-docx markdown fpdf2 beautifulsoup4 -q
if errorlevel 1 (
    echo [警告] 安装过程中出现问题，尝试强制重新安装...
    pip install python-docx markdown fpdf2 beautifulsoup4 --force-reinstall -q
)
echo [✓] 依赖包安装完成
echo.

echo [3/3] 验证安装...
python "%~dp0md2all.py" >nul 2>&1
if errorlevel 1 (
    echo [错误] 验证失败，请检查错误信息
    pause
    exit /b 1
)
echo [✓] 验证成功
echo.

echo ==========================================
echo    安装完成！
echo ==========================================
echo.
echo 使用方法:
echo   1. 将Markdown文件(.md)拖放到此窗口
echo   2. 或在命令行运行: python md2all.py 文件名.md
echo   3. 或在命令行运行: python md2all.py 文件名.md pdf
echo.
echo 支持格式:
echo   - pdf  : 转换为PDF文档
echo   - docx : 转换为Word文档
echo   - html : 转换为HTML网页
echo   - all  : 同时转换以上所有格式（默认）
echo.
pause
