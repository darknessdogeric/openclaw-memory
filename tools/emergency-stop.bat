@echo off
chcp 65001 >nul
title B166ER 紧急停止工具
color 0C

echo.
echo  ██████╗ ███████╗███████╗██████╗     ███████╗████████╗ ██████╗ ██████╗ 
echo  ██╔══██╗██╔════╝██╔════╝██╔══██╗    ██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
echo  ██████╔╝█████╗  █████╗  ██████╔╝    ███████╗   ██║   ██║   ██║██████╔╝
echo  ██╔══██╗██╔══╝  ██╔══╝  ██╔══██╗    ╚════██║   ██║   ██║   ██║██╔═══╝ 
echo  ██████╔╝███████╗███████╗██║  ██║    ███████║   ██║   ╚██████╔╝██║     
echo  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝    ╚══════╝   ╚═╝    ╚═════╝ ╚═╝     
echo.
echo  ════════════════════════════════════════════════════════════════════
echo   正在扫描并停止 B166ER/OpenClaw 相关进程...
echo  ════════════════════════════════════════════════════════════════════
echo.

:: 查找并终止 OpenClaw 相关进程
tasklist /FI "IMAGENAME eq openclaw.exe" 2>nul | find /I "openclaw.exe" >nul
if %errorlevel% equ 0 (
    echo  [!] 发现 OpenClaw 进程，正在终止...
    taskkill /F /IM openclaw.exe /T 2>nul
    if %errorlevel% equ 0 (
        echo  [✓] OpenClaw 已成功停止
    ) else (
        echo  [✗] 无法终止 OpenClaw，可能需要管理员权限
    )
) else (
    echo  [i] 未发现 OpenClaw 进程在运行
)

:: 查找 Node.js 进程（OpenClaw 可能以 node 运行）
tasklist /FI "IMAGENAME eq node.exe" 2>nul | find /I "node.exe" >nul
if %errorlevel% equ 0 (
    echo.
    echo  [!] 发现 Node.js 进程
    echo      如果 OpenClaw 以 Node 方式运行，请输入 Y 终止
echo.
    choice /C YN /M "  是否终止 Node.js 进程" /N
    if %errorlevel% equ 1 (
        taskkill /F /IM node.exe /T 2>nul
        echo  [✓] Node.js 进程已终止
    ) else (
        echo  [i] 跳过 Node.js 进程
    )
)

:: 查找 Python 进程（可能正在运行任务）
tasklist /FI "IMAGENAME eq python.exe" 2>nul | find /I "python.exe" >nul
if %errorlevel% equ 0 (
    echo.
    echo  [!] 发现 Python 进程（可能是正在运行的任务）
    choice /C YN /M "  是否终止 Python 进程" /N
    if %errorlevel% equ 1 (
        taskkill /F /IM python.exe /T 2>nul
        echo  [✓] Python 进程已终止
    ) else (
        echo  [i] 跳过 Python 进程
    )
)

echo.
echo  ════════════════════════════════════════════════════════════════════
echo   扫描完成
echo  ════════════════════════════════════════════════════════════════════
echo.
echo   提示：此工具只能强制终止进程，无法优雅地保存进行中的工作。
echo        建议优先使用 Web 界面中的停止按钮。
echo.

pause
