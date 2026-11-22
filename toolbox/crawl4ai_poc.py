"""crawl4ai AHL PoC: Booking 价格抓取 + LLM extraction
对比 crawl4ai 与 booking_price_extractor（InvisiblePlaywright）的输出质量
"""
import json
import sys

sys.path.insert(0, r"D:\B166ER-OpenClaw\workspace\toolbox")

from crawl4ai_wrapper import crawl_booking_hotel, crawl_llm_ready, BOOKING_PRICE_SCHEMA, BOOKING_EXTRACTION_INSTRUCTION

# 测试 URL: Imperial Hotel Tokyo (已在 booking_price_extractor 中验证过)
URL = "https://www.booking.com/hotel/jp/imperial-tokyo.html"
CHECKIN = "2026-07-22"
CHECKOUT = "2026-07-23"
ADULTS = 2
CURRENCY = "JPY"

def main():
    print("=" * 70)
    print(f"AHL PoC: crawl4ai Booking 价格抓取")
    print(f"URL: {URL}")
    print(f"入住: {CHECKIN}, 退房: {CHECKOUT}, 成人: {ADULTS}, 货币: {CURRENCY}")
    print("=" * 70)

    # Step 1: 基础模式（只输出 Markdown，无 LLM）
    print("\n[Step 1] 基础模式: Markdown only (no LLM)")
    print("-" * 70)
    url_with_dates = f"{URL}?checkin={CHECKIN}&checkout={CHECKOUT}&group_adults={ADULTS}&selected_currency={CURRENCY}"
    result_basic = crawl_llm_ready(url_with_dates, wait_for="table.hprt-table, div.hotel-room-list, [data-testid='property-card']")
    print(f"Success: {result_basic.success}")
    print(f"Elapsed: {result_basic.elapsed:.2f}s")
    print(f"Markdown length: {len(result_basic.markdown)}")
    if result_basic.error:
        print(f"Error: {result_basic.error}")

    if result_basic.markdown:
        # 输出前 3000 字（价格信息应该在这里）
        print("\nMarkdown preview (first 3000 chars):")
        print("-" * 70)
        print(result_basic.markdown[:3000])

        # 保存完整 Markdown
        out_md = r"D:\B166ER-OpenClaw\workspace\toolbox\crawl4ai_poc_imperial.md"
        with open(out_md, "w", encoding="utf-8") as f:
            f.write(result_basic.markdown)
        print(f"\n[SAVED] Full Markdown → {out_md}")

    # Step 2: LLM 提取模式（如有 API key）
    print("\n" + "=" * 70)
    print("[Step 2] LLM 提取模式 (如配置了 OPENAI_API_KEY 或 DEEPSEEK_API_KEY)")
    print("-" * 70)
    has_llm_key = bool(__import__("os").getenv("OPENAI_API_KEY")) or bool(__import__("os").getenv("DEEPSEEK_API_KEY"))
    if not has_llm_key:
        print("[SKIP] 未配置 LLM API key，跳过 LLM 提取")
        print("       配置方法: set OPENAI_API_KEY=sk-... 或 set DEEPSEEK_API_KEY=sk-...")
    else:
        print("[INFO] 已有 LLM API key，开始 LLM 提取...")
        result_llm = crawl_booking_hotel(URL, CHECKIN, CHECKOUT, ADULTS, CURRENCY, use_llm=True)
        print(f"Success: {result_llm.success}")
        print(f"Elapsed: {result_llm.elapsed:.2f}s")
        if result_llm.extracted_json:
            print("\nExtracted JSON:")
            print(json.dumps(result_llm.extracted_json, indent=2, ensure_ascii=False))

    print("\n" + "=" * 70)
    print("[DONE] PoC 完成")
    print("=" * 70)

if __name__ == "__main__":
    main()