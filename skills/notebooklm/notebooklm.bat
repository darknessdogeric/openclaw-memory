@echo off
chcp 65001 >nul
echo ==========================================
echo    NotebookLM - 智能文档分析工具
echo ==========================================
echo.

if "%~1"=="" (
    echo 使用方法:
    echo   notebooklm create "笔记本名称" [--description "描述"]
    echo   notebooklm add ^<笔记本ID^> ^<文件1^> [文件2] ...
    echo   notebooklm summary ^<笔记本ID^> [--style narrative/bullet/executive]
    echo   notebooklm ask ^<笔记本ID^> "问题"
    echo   notebooklm list
    echo.
    echo 示例:
    echo   notebooklm create "项目研究"
    echo   notebooklm add abc123 paper.pdf notes.md
    echo   notebooklm summary abc123 --style bullet
    echo   notebooklm ask abc123 "主要结论是什么？"
    pause
    exit /b 1
)

cd /d "%~dp0"
python notebooklm.py %*
