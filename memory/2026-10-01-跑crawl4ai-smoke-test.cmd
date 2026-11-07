@echo === crawl4ai v0.9.4 smoke test ===
echo 1) 物理清理空 skill 目录（inventory 已标采纳）
rmdir /s /q "D:\B166ER-OpenClaw\workspace\skills\crawl4ai" 2>nul
rmdir /s /q "D:\B166ER-OpenClaw\workspace\skills\crawl4ai_local" 2>nul
rmdir /s /q "D:\B166ER-OpenClaw\workspace\skills\temp_crawl4ai" 2>nul

echo.
echo 2) 验证 wrapper + v0.9.4 兼容性（需先 pip install crawl4ai==0.9.4）
python -c "import crawl4ai; print('crawl4ai version:', getattr(crawl4ai, '__version__', 'unknown'))"

echo.
echo 3) 跑 wrapper smoke test
python "D:\B166ER-OpenClaw\workspace\toolbox\crawl4ai_wrapper.py" --test "https://www.iana.org/help/example-domains"

echo.
echo === 完成 ===
pause