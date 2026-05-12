# -*- coding: utf-8 -*-
"""
数据标准化Pipeline
将各平台的原始HTML文本转换为统一的OTAHotel数据结构
"""
from __future__ import annotations
import re
import json
from datetime import datetime
from typing import Optional
from .core import OTAHotel, OTAPrice, OTARoom, OTAReview, ScrapeStatus


class DataPipeline:
    """数据提取和标准化管道"""

    @staticmethod
    def extract_price(text: str, platform_config: dict = None) -> Optional[float]:
        """从文本中提取价格数字"""
        if not text:
            return None
        text_clean = text.strip().replace(" ", "").replace(",", "")
        # 优先匹配带货币符号或"起/元"的价格
        patterns = [
            r'[¥￥]\s*(\d+\.?\d*)',              # ¥688
            r'(\d+\.?\d*)\s*(?:元|块)\s*(?:起)?',  # 688元起
            r'(?:price|售价|价格)[:：]?\s*[¥￥]?\s*(\d+\.?\d*)',
            r'USD\s*(\d+\.?\d*)',
            r'\$\s*(\d+\.?\d*)',
            r'€\s*(\d+\.?\d*)',
            r'£\s*(\d+\.?\d*)',
        ]
        for pattern in patterns:
            m = re.search(pattern, text_clean, re.IGNORECASE)
            if m:
                val = float(m.group(1))
                if 10 <= val <= 100000:  # 合理价格范围
                    return val
        # 如果没有货币符号但行中包含"价"字
        if '价' in text_clean:
            nums = re.findall(r'(\d{3,}\.?\d*)', text_clean)  # 至少3位数
            for n in nums:
                val = float(n)
                if 10 <= val <= 100000:
                    return val
        return None

    @staticmethod
    def extract_score(text: str, scale: float = 5.0) -> Optional[float]:
        """提取评分并归一化到0-5"""
        if not text:
            return None
        nums = re.findall(r'(\d+\.?\d*)', text)
        if not nums:
            return None
        score = float(nums[0])
        # 归一化到0-5
        if scale == 10.0 and score > 5:
            score = score / 2.0
        return min(5.0, max(0.0, score))

    @staticmethod
    def extract_review_count(text: str) -> int:
        """提取评论数量"""
        if not text:
            return 0
        nums = re.findall(r'(\d+)', text.replace(",", "").replace(" ", ""))
        if not nums:
            return 0
        return int(nums[0])

    @staticmethod
    def parse_hotel_list(html_content: str, platform_id: str,
                         platform_config: dict) -> list[OTAHotel]:
        """解析酒店列表 - 自动检测结构化/文本格式"""
        if not html_content or len(html_content) < 50:
            return []
        if "===HOTEL_CARD===" in html_content:
            return DataPipeline._parse_structured(html_content, platform_id, platform_config)
        return DataPipeline._parse_text_heuristic(html_content, platform_id, platform_config)

    @staticmethod
    def _parse_structured(html_content: str, platform_id: str,
                          platform_config: dict) -> list[OTAHotel]:
        """解析CSS选择器提取的结构化卡片"""
        hotels = []
        cards = html_content.split("===HOTEL_CARD===")
        normalize = platform_config.get("normalize", {})
        score_scale = normalize.get("score_scale", 5.0)

        for card in cards:
            card = card.replace("===END_CARD===", "").strip()
            if not card or len(card) < 10:
                continue

            hotel = OTAHotel(platform=platform_id)
            lines = card.split("\n")

            for line in lines:
                line = line.strip()
                if not line or ":" not in line:
                    continue
                idx = line.index(":")
                field = line[:idx].strip()
                value = line[idx+1:].strip()
                if not value:
                    continue

                if field in ("name", "hotel_name"):
                    hotel.hotel_name = value
                elif field == "price":
                    price = DataPipeline.extract_price(value)
                    if price:
                        hotel.prices.append(OTAPrice(
                            lowest_price=price,
                            currency=normalize.get("currency", "CNY")))
                elif field in ("score", "hotel_score", "rating"):
                    # Booking: "Scored 9.09.0Wonderful85 reviews"
                    scored_m = re.search(r'(?:Scored|scored)\s*(\d+\.?\d*)', value)
                    if scored_m:
                        s = float(scored_m.group(1))
                        if score_scale >= 10.0: s = s / 2.0
                        if not hotel.review: hotel.review = OTAReview()
                        hotel.review.score = s
                    else:
                        s = DataPipeline.extract_score(value, score_scale)
                        if s is not None:
                            if not hotel.review: hotel.review = OTAReview()
                            hotel.review.score = s
                elif field in ("reviews", "hotel_reviews", "review_count"):
                    # Booking: "Scored 9.0Wonderful85 reviews" or "9.0Wonderful 85 reviews"
                    # Ctrip: "超棒1,165条点评"
                    rm = re.search(r'(\d[\d,]*)\s*(?:reviews|条点评|条评论|点评|评论)', value, re.I)
                    if not rm:
                        # Booking no-space: "Wonderful85 reviews"
                        rm = re.search(r'[A-Z][a-z]+(\d[\d,]*)\s*(?:reviews|条)', value, re.I)
                    if rm:
                        cnt = DataPipeline.extract_review_count(rm.group(1))
                        if not hotel.review: hotel.review = OTAReview()
                        hotel.review.review_count = cnt
                    else:
                        cnt = DataPipeline.extract_review_count(value)
                        if cnt > 0:
                            if not hotel.review: hotel.review = OTAReview()
                            hotel.review.review_count = cnt
                elif field in ("address", "hotel_address", "location"):
                    hotel.address = value
                elif field in ("stars", "star_rating"):
                    m = re.search(r'(\d)', value)
                    if m: hotel.star_rating = int(m.group(1))
                elif field == "hotel_id":
                    hotel.hotel_id = value

            if not hotel.hotel_name:
                for ln in lines:
                    ln = ln.strip()
                    if ln and len(ln) > 2 and len(ln) < 120 and ":" not in ln:
                        hotel.hotel_name = ln; break

            # 文本回退: 从原始卡片文本提取评分/评论 (携程: "超棒1,165条点评4.8")
            card_text = card
            if not (hotel.review and hotel.review.review_count):
                # 携程: "1,165条点评"
                ctm = re.search(r'(\d[\d,]*)\s*条(?:点评|评论)', card_text)
                if ctm:
                    cnt = DataPipeline.extract_review_count(ctm.group(1))
                    if not hotel.review: hotel.review = OTAReview()
                    hotel.review.review_count = cnt
            if not (hotel.review and hotel.review.score):
                # 携程: "4.8" after "超棒" or standalone decimal
                stm = re.search(r'(?:超棒|棒|好|很好|非常好)\s*(\d\.\d)', card_text)
                if stm:
                    if not hotel.review: hotel.review = OTAReview()
                    hotel.review.score = float(stm.group(1))

            if hotel.hotel_name:
                hotel.data_quality = DataPipeline._calc_quality(hotel)
                hotel.scraped_at = datetime.now().isoformat()
                hotels.append(hotel)
        return hotels

    @staticmethod
    def _parse_text_heuristic(html_content: str, platform_id: str,
                              platform_config: dict) -> list[OTAHotel]:
        """通用文本启发式解析 (无结构化标记时fallback)"""
        hotels = []
        config = platform_config
        normalize = config.get("normalize", {})
        score_scale = normalize.get("score_scale", 5.0)
        blocks = re.split(r'\n\s*\n|---{3,}', html_content)

        for block in blocks:
            if len(block) < 50:
                continue
            hotel = OTAHotel(platform=platform_id)
            lines = block.strip().split("\n")

            for line in lines:
                line = line.strip()
                if not line: continue
                if not hotel.hotel_name and len(line) > 3 and len(line) < 100:
                    if not re.match(r'^[¥￥\d\s.,]+$', line):
                        hotel.hotel_name = line; continue
                price = DataPipeline.extract_price(line)
                if price and price > 10:
                    if not hotel.prices:
                        hotel.prices.append(OTAPrice(lowest_price=price,
                                            currency=normalize.get("currency", "CNY")))
                    continue
                score = DataPipeline.extract_score(line, score_scale)
                if score is not None and score >= 1.0:
                    if not hotel.review: hotel.review = OTAReview(score=score)
                    continue
                count = DataPipeline.extract_review_count(line)
                if count > 0 and any(kw in line for kw in ["评论","条","review"]):
                    if not hotel.review: hotel.review = OTAReview()
                    hotel.review.review_count = count
                    continue
                if any(kw in line for kw in ["街","路","号","区"]) and not hotel.address:
                    hotel.address = line

            if hotel.hotel_name:
                hotel.data_quality = DataPipeline._calc_quality(hotel)
                hotel.scraped_at = datetime.now().isoformat()
                hotels.append(hotel)
        return hotels

    @staticmethod
    def parse_hotel_detail(html_content: str, platform_id: str,
                           platform_config: dict) -> Optional[OTAHotel]:
        """从详情页文本解析单个酒店"""
        if not html_content:
            return None

        config = platform_config
        selectors = config.get("selectors", {})
        normalize = config.get("normalize", {})

        hotel = OTAHotel(platform=platform_id)
        lines = html_content.strip().split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 酒店名 (较长且在前面)
            if not hotel.hotel_name and len(line) > 3 and len(line) < 120:
                if not re.match(r'^[¥￥\d\s.,]+$', line):
                    hotel.hotel_name = line

            # 价格
            price = DataPipeline.extract_price(line)
            if price and price > 10:
                if not hotel.prices:
                    hotel.prices.append(OTAPrice(lowest_price=price, currency=normalize.get("currency", "CNY")))

            # 评分
            score = DataPipeline.extract_score(line, normalize.get("score_scale", 5.0))
            if score is not None and score >= 1.0:
                if not hotel.review:
                    hotel.review = OTAReview()
                hotel.review.score = score

            # 评论数
            count = DataPipeline.extract_review_count(line)
            if count > 0 and any(kw in line for kw in ["评论", "条", "review", "点评"]):
                if not hotel.review:
                    hotel.review = OTAReview()
                hotel.review.review_count = count

            # 地址
            if not hotel.address and any(kw in line for kw in ["街", "路", "号", "区", "地址", "address"]):
                hotel.address = line

            # 星级
            if not hotel.star_rating:
                star_match = re.search(r'(\d)\s*星', line)
                if star_match:
                    hotel.star_rating = int(star_match.group(1))

        hotel.data_quality = DataPipeline._calc_quality(hotel)
        hotel.scraped_at = datetime.now().isoformat()
        return hotel if hotel.hotel_name else None

    @staticmethod
    def _calc_quality(hotel: OTAHotel) -> float:
        """计算数据完整度"""
        score = 0.0
        if hotel.hotel_name: score += 0.2
        if hotel.prices: score += 0.2
        if hotel.address: score += 0.15
        if hotel.review and hotel.review.score: score += 0.15
        if hotel.star_rating: score += 0.1
        if hotel.amenities: score += 0.1
        if hotel.image_urls: score += 0.1
        return min(1.0, score)

    @staticmethod
    def export_json(hotels: list[OTAHotel], filepath: str = None) -> str:
        """导出为JSON"""
        data = []
        for h in hotels:
            d = {
                "hotel_id": h.hotel_id,
                "hotel_name": h.hotel_name,
                "platform": h.platform,
                "address": h.address,
                "city": h.city,
                "district": h.district,
                "star_rating": h.star_rating,
                "hotel_type": h.hotel_type,
                "brand": h.brand,
                "prices": [{"lowest_price": p.lowest_price, "currency": p.currency} for p in h.prices] if h.prices else [],
                "review_score": h.review.score if h.review else None,
                "review_count": h.review.review_count if h.review else 0,
                "latitude": h.latitude,
                "longitude": h.longitude,
                "data_quality": h.data_quality,
                "scraped_at": h.scraped_at,
            }
            data.append(d)

        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json_str)
        return json_str

    @staticmethod
    def export_csv(hotels: list[OTAHotel], filepath: str = None) -> str:
        """导出为CSV"""
        import csv
        import io

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["平台", "酒店名称", "星级", "最低价", "评分", "评论数", "地址", "城市", "数据质量"])

        for h in hotels:
            writer.writerow([
                h.platform, h.hotel_name, h.star_rating or "",
                h.prices[0].lowest_price if h.prices else "",
                h.review.score if h.review else "",
                h.review.review_count if h.review else "",
                h.address, h.city,
                f"{h.data_quality:.0%}"
            ])

        csv_str = output.getvalue()
        if filepath:
            with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
                f.write(csv_str)
        return csv_str
