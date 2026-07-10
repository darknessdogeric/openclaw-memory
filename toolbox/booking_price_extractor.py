# -*- coding: utf-8 -*-
"""
AHL 跨境 OTA 数据抓取 - Booking.com 价格提取器
================================================================
- 解决 Booking 隐式"无日期不显示价格"问题
- 用 URL 参数预设 checkin/checkout/group_adults/selected_currency
- 抓取每个房型行（table.hprt-table）内的：
    * 房型名 (td.hprt-table-cell-roomtype)
    * 床型/人数
    * 取消政策
    * 早餐
    * 价格 (td.hprt-table-cell-price)
- 输出 JSON 格式，可直接入 AHL 数据底座
- 自带 retry 机制 (默认 2 次)
================================================================
用法：
    from booking_price_extractor import BookingPriceExtractor
    ex = BookingPriceExtractor()
    result = ex.fetch_prices(
        hotel_url="https://www.booking.com/hotel/jp/imperial-tokyo.html",
        checkin="2026-07-15",
        checkout="2026-07-16",
        adults=2,
        currency="JPY",
    )
"""
from __future__ import annotations
import re
import json
import time
from dataclasses import dataclass, field, asdict
from typing import Optional
from invisible_playwright import InvisiblePlaywright


@dataclass
class RoomRate:
    """单房型价格"""
    room_type: str = ""
    bed_type: str = ""
    sleeps: int = 0
    original_price: float = 0.0
    current_price: float = 0.0
    discount_pct: float = 0.0
    currency: str = "JPY"
    cancellation_policy: str = ""
    breakfast_included: bool = False
    pay_later: bool = False
    raw_text: str = ""


@dataclass
class HotelPriceResult:
    """酒店价格抓取结果"""
    url: str
    hotel_id: str = ""
    hotel_name: str = ""
    checkin: str = ""
    checkout: str = ""
    adults: int = 2
    nights: int = 1
    currency: str = "JPY"
    rooms: list = field(default_factory=list)
    min_price: float = 0.0
    max_price: float = 0.0
    avg_price: float = 0.0
    timestamp: str = ""
    error: str = ""


class BookingPriceExtractor:
    """Booking.com 价格抓取器"""

    def __init__(self, wait_ms: int = 15000, max_retries: int = 2):
        self.wait_ms = wait_ms
        self.max_retries = max_retries

    def _build_url(self, hotel_url, checkin, checkout, adults, currency):
        sep = "&" if "?" in hotel_url else "?"
        params = (
            f"checkin={checkin}&checkout={checkout}"
            f"&group_adults={adults}&group_children=0&no_rooms=1"
            f"&selected_currency={currency}"
        )
        return f"{hotel_url}{sep}{params}"

    def _calc_nights(self, checkin, checkout):
        from datetime import datetime
        try:
            d1 = datetime.strptime(checkin, "%Y-%m-%d")
            d2 = datetime.strptime(checkout, "%Y-%m-%d")
            return (d2 - d1).days
        except:
            return 1

    def fetch_prices(self, hotel_url, checkin, checkout, adults=2, currency="JPY"):
        url = self._build_url(hotel_url, checkin, checkout, adults, currency)
        result = HotelPriceResult(
            url=url,
            checkin=checkin,
            checkout=checkout,
            adults=adults,
            currency=currency,
            nights=self._calc_nights(checkin, checkout),
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
        )

        for attempt in range(self.max_retries + 1):
            try:
                self._fetch_once(result)
                if result.rooms or attempt == self.max_retries:
                    break
            except Exception as e:
                result.error = f"attempt {attempt+1}: {str(e)[:200]}"
                if attempt < self.max_retries:
                    time.sleep(2)
        return result

    def _fetch_once(self, result):
        url = result.url
        currency = result.currency
        with InvisiblePlaywright() as browser:
            page = browser.new_page()
            page.goto(url, timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(self.wait_ms)

            data = page.evaluate(r"""() => {
                const out = {hotel_name: '', hotel_id: '', rooms: []};
                const nameEl = document.querySelector('h2.hp__hotel-name, .hp__hotel-name, h1.hp__hotel-name');
                if (nameEl) out.hotel_name = nameEl.innerText.trim();
                const m = document.body.innerText.match(/hotel[\|/](\d+)/);
                if (m) out.hotel_id = m[1];
                const table = document.querySelector('table.hprt-table, #availability_table table');
                if (table) {
                    const trs = table.querySelectorAll('tbody tr');
                    let lastRoomType = '';
                    let lastBedType = '';
                    trs.forEach((tr, idx) => {
                        const room = {raw_text: tr.innerText.trim().substring(0, 500)};
                        const typeCell = tr.querySelector(
                            'td.hprt-table-cell-roomtype, .hprt-roomtype, .hprt-roomtype-icon-link, [data-testid*="room-type"]'
                        );
                        if (typeCell) {
                            const t = typeCell.innerText.trim();
                            if (t && t.length < 200) {
                                room.room_type = t;
                                lastRoomType = t;
                            }
                        } else {
                            room.room_type = lastRoomType;
                        }
                        const bedEl = tr.querySelector(
                            '.hprt-roomtype-bed, .hprt-bed-types, .hprt-room-facilities, [data-testid*="bed"]'
                        );
                        if (bedEl) {
                            room.bed_type = bedEl.innerText.trim().substring(0, 80);
                            lastBedType = room.bed_type;
                        } else {
                            room.bed_type = lastBedType;
                        }
                        const priceCell = tr.querySelector('td.hprt-table-cell-price, .hprt-price-block');
                        if (priceCell) {
                            const cellText = priceCell.innerText.trim();
                            room.price_cell_text = cellText.substring(0, 200);
                            const m = cellText.match(/[¥$€£]\s*[\d,]+/g);
                            if (m) room.prices = m;
                        }
                        const text = tr.innerText;
                        if (text.match(/free\s+cancellation/i)) room.cancellation_policy = "Free cancellation";
                        else if (text.match(/non.?refundable/i)) room.cancellation_policy = "Non-refundable";
                        if (text.match(/breakfast\s+included/i)) room.breakfast_included = true;
                        if (text.match(/pay\s+nothing\s+until|reserve\s+now,?\s+pay\s+later/i)) room.pay_later = true;
                        const d = text.match(/(\d+)\s*%\s*off/i);
                        if (d) room.discount_pct = parseInt(d[1]);
                        if ((room.prices && room.prices.length > 0) || room.room_type) {
                            out.rooms.push(room);
                        }
                    });
                } else {
                    document.querySelectorAll('.hprt-table-block, .hprt-block').forEach(row => {
                        const txt = row.innerText.trim();
                        if (txt.length > 30) {
                            const m = txt.match(/[¥$€£]\s*[\d,]+/g);
                            if (m) out.rooms.push({raw_text: txt.substring(0, 500), prices: m});
                        }
                    });
                }
                return out;
            }""")

            result.hotel_name = data.get("hotel_name", "")
            result.hotel_id = data.get("hotel_id", "")
            for r in data.get("rooms", []):
                room = self._build_room_rate(r, currency)
                if room:
                    result.rooms.append(room)

            prices = [r.current_price for r in result.rooms if r.current_price > 0]
            if prices:
                result.min_price = min(prices)
                result.max_price = max(prices)
                result.avg_price = round(sum(prices) / len(prices), 2)

            page.close()

    def _build_room_rate(self, raw, currency):
        if not raw or (not raw.get("room_type") and not raw.get("prices")):
            return None
        room = RoomRate(
            room_type=raw.get("room_type", "")[:100],
            bed_type=raw.get("bed_type", "")[:80],
            cancellation_policy=raw.get("cancellation_policy", ""),
            breakfast_included=raw.get("breakfast_included", False),
            pay_later=raw.get("pay_later", False),
            currency=currency,
            raw_text=raw.get("raw_text", "")[:300],
        )

        def to_num(s):
            if not s:
                return 0
            m = re.search(r"[\d,]+", s)
            if not m:
                return 0
            return int(m.group(0).replace(",", ""))

        prices = [to_num(p) for p in raw.get("prices", []) if p]
        original_prices = [to_num(p) for p in raw.get("original_prices", []) if p]
        prices = [p for p in prices if p > 0]
        original_prices = [p for p in original_prices if p > 0]
        if prices:
            room.current_price = min(prices)
        if original_prices:
            room.original_price = max(original_prices)
        elif len(prices) >= 2:
            room.original_price = max(prices)
        if raw.get("discount_pct"):
            room.discount_pct = raw["discount_pct"]
        elif room.original_price > room.current_price > 0:
            room.discount_pct = round((1 - room.current_price / room.original_price) * 100, 1)
        return room


# === CLI ===
if __name__ == "__main__":
    extractor = BookingPriceExtractor(wait_ms=12000)
    test_url = "https://www.booking.com/hotel/jp/imperial-tokyo.html"
    result = extractor.fetch_prices(
        hotel_url=test_url,
        checkin="2026-07-15",
        checkout="2026-07-16",
        adults=2,
        currency="JPY",
    )
    print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    print(f"\n[SUMMARY] rooms={len(result.rooms)} min=¥{result.min_price:,.0f} max=¥{result.max_price:,.0f} avg=¥{result.avg_price:,.0f}")
