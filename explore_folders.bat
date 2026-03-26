@echo off
chcp 65001 >nul
cd /d F:\
echo === F: DRIVE STRUCTURE ===
dir /ad /b
echo.
echo === CHECKING KEY FOLDERS ===
for %%a in (管理项目 运营文件 中酒拓展 中旅酒店相关内容 主要经营数据 自我革命 襄阳共享国际文件 个人事项报告 新媒体 述职报告) do (
    if exist "%%a" (
        echo [EXISTS] %%a
        dir /a-d /o-s "%%a" 2>nul | findstr /v "^$"
    ) else (
        echo [NOT FOUND] %%a
    )
    echo.
)
