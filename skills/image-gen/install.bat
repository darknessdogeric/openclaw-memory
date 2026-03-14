@echo off
chcp 65001 >nul
echo ==========================================
echo    ImageGen Skill - 安装脚本
echo    AI图像生成技能
echo ==========================================
echo.

echo [1/3] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python
    pause
    exit /b 1
)
echo [✓] Python 已安装
echo.

echo [2/3] 安装依赖...
pip install requests -q
echo [✓] 依赖安装完成
echo.

echo [3/3] 安装 image-gen 命令...
set "TARGET_DIR=C:\Users\Administrator\.openclaw\tools\image-gen"
set "SYSTEM_DIR=C:\Windows\System32"

mkdir "%TARGET_DIR%" 2>nul
copy /Y "%~dp0image_gen.py" "%TARGET_DIR%\image_gen.py" >nul

echo @echo off > "%SYSTEM_DIR%\image-gen.bat"
echo set PYTHONIOENCODING=utf-8 >> "%SYSTEM_DIR%\image-gen.bat"
echo python "%TARGET_DIR%\image_gen.py" %%* >> "%SYSTEM_DIR%\image-gen.bat"

echo [✓] 命令安装完成
echo.

echo ==========================================
echo    安装完成！
echo ==========================================
echo.
echo 使用方法:
echo   image-gen "你的图像描述"
echo   image-gen "现代酒店大堂" -p pollinations
echo   image-gen "海景客房" -s 1024x1024
echo.
echo 提示:
echo   - 默认使用免费的Pollinations服务
echo   - 图像保存到桌面的 AI_Generated_Images 文件夹
echo   - 首次使用无需配置API Key
echo.
pause
