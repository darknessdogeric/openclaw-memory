"""B166ER 酒店行业信源矩阵
=====================================
Eric 给我的核心指令（2026-07-21 23:25）：
> "这些信源是给你的，不光是 AHL。你自己本身需要具备这些信源全维度"

这是 B166ER 的"行业大脑"——28 个权威信源，覆盖酒店行业的全维度。
不仅服务 AHL 项目，也是 B166ER 作为 Eric 助理的标配行业能力。

== 信源矩阵（28 个，按类型分组）==

【T1 - 国际权威】     STR Global, CTHA
【T2 - 国内全样本/官方】酒店之家, 国家统计, 文旅部
【T3 - 协会权威】     CHA, CTA, CCFA, CCA, 世界中餐业联合会
【T4 - 权威咨询】     浩华 HTL, 厚海数据, PwC, Deloitte, EY, KPMG
【T5 - 头部财报】     华住, 锦江, 亚朵, 首旅, 万豪, 希尔顿 等 20 家
【T6 - 券商研报】     中金, 中信, 光大, 东方, 招商 等
【T7 - 代理行】       仲量联行, 戴德梁行, 第一太平, CBRE, 高力, 世邦魏理
【T8 - 交通部】       民航, 铁路
【T9 - OTA 平台】     携程, 美团, 去哪儿, 飞猪, 同程, 途家, 木鸟
【T10 - 转让数据】    指点网
【T11 - 行业研究】    浩华景气, 迈点, 品橙, 北二外
【T12 - 用户调研】    腾讯智慧文旅
"""
import os
import sys
import json
import asyncio
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime

sys.path.insert(0, r"D:\B166ER-OpenClaw\workspace\toolbox")


# ============================================================
# 酒店行业 28 信源字典（广义信源矩阵的子集）
# 注：广义信源矩阵 = hotel_sources.py 28 酒店信源 + TrendRadar 31 RSS + 11 平台热搜 = ~103 个主动信源 + ~1355 关键词
# 详情见 memory/2026-08-02-source-matrix-expansion.md
# ============================================================

HOTEL_SOURCES = {
    # === Tier 1: 国际权威 + 行业第一协会 ===
    "STR": {
        "name": "STR Global",
        "name_zh": "STR 全球",
        "category": "国际权威",
        "url": "https://str.com",
        "china_url": "https://str.com/region/greater-china",
        "publish_frequency": "月报+季报",
        "key_reports": ["China Hotel Review Monthly", "Asia Pacific Hotel Review"],
        "value": "全球+亚太+中国独立酒店样本 · 行业金标准",
        "credibility": "★★★★★",
    },
    "CTHA": {
        "name": "China Tourist Hotel Association",
        "name_zh": "中国旅游饭店业协会",
        "category": "行业协会",
        "url": "http://www.ctha.com.cn",
        "publish_frequency": "季度景气+年报",
        "key_reports": ["中国酒店业发展报告", "季度景气指数"],
        "value": "行业第一协会 · 政策风向标",
        "credibility": "★★★★★",
    },

    # === Tier 2: 国内全样本 + 官方数据 ===
    "HotelsHome": {
        "name": "酒店之家",
        "name_zh": "酒店之家",
        "category": "国内全样本",
        "url": "https://www.jiudianzhijia.com",
        "publish_frequency": "月度",
        "key_reports": ["月度报告", "新开业数据", "连锁化率"],
        "value": "36-37万家 · 1850万间客房全样本",
        "credibility": "★★★★★",
    },
    "NBS": {
        "name": "National Bureau of Statistics",
        "name_zh": "国家统计局",
        "category": "官方数据",
        "url": "https://www.stats.gov.cn",
        "publish_frequency": "月度+季度+年度",
        "key_reports": ["GDP", "CPI", "消费数据", "住宿业统计"],
        "value": "宏观基准 · GDP/CPI/消费倾向",
        "credibility": "★★★★★",
    },
    "MoCT": {
        "name": "Ministry of Culture and Tourism",
        "name_zh": "文化和旅游部",
        "category": "官方数据",
        "url": "https://www.mct.gov.cn",
        "publish_frequency": "季度+年度+节假日",
        "key_reports": ["国内旅游统计", "入境游数据", "节假日数据"],
        "value": "出游人次+收入+入境 · 政策动向",
        "credibility": "★★★★★",
    },

    # === Tier 3: 协会权威 ===
    "CHA": {
        "name": "China Hotel Association",
        "name_zh": "中国饭店协会",
        "category": "行业协会",
        "url": "http://www.chinahotel.org.cn",
        "publish_frequency": "年度+季度",
        "key_reports": ["中国饭店业年度报告", "酒店品牌榜"],
        "value": "第二大协会 · 品牌指数权威",
        "credibility": "★★★★",
    },
    "CTA": {
        "name": "China Tourism Academy",
        "name_zh": "中国旅游研究院",
        "category": "行业协会",
        "url": "https://www.ctaweb.org.cn",
        "publish_frequency": "季度+年度",
        "key_reports": ["中国旅游经济运行报告", "季度报告", "节假日报告"],
        "value": "文旅部直属 · 最权威旅游/酒店统计",
        "credibility": "★★★★★",
    },
    "CCFA": {
        "name": "China Chain Store & Franchise Association",
        "name_zh": "中国连锁经营协会",
        "category": "行业协会",
        "url": "https://www.ccfa.org.cn",
        "publish_frequency": "年度",
        "key_reports": ["中国连锁经营年鉴", "连锁TOP100", "酒店连锁榜"],
        "value": "连锁酒店 TOP100 · 餐饮连锁",
        "credibility": "★★★★",
    },
    "CCA": {
        "name": "China Cuisine Association",
        "name_zh": "中国烹饪协会",
        "category": "行业协会",
        "url": "http://www.ccas.com.cn",
        "publish_frequency": "年度",
        "key_reports": ["餐饮行业统计", "酒店餐饮报告"],
        "value": "餐饮数据 · 酒店餐饮关联",
        "credibility": "★★★",
    },
    "WCF": {
        "name": "World Chinese Cuisine Federation",
        "name_zh": "世界中餐业联合会",
        "category": "行业协会",
        "url": "https://www.worldchinesecuisine.org",
        "publish_frequency": "不定期",
        "key_reports": ["国际中餐行业报告"],
        "value": "国际中餐 · 出海相关",
        "credibility": "★★",
    },

    # === Tier 4: 权威咨询（酒店行业最老牌） ===
    "Horwath": {
        "name": "Horwath HTL (China)",
        "name_zh": "浩华管理顾问",
        "category": "权威咨询",
        "url": "https://www.horwathhtl.com",
        "china_url": "https://www.horwathhtl.com/zh",
        "publish_frequency": "季度景气+年度白皮书",
        "key_reports": ["中国酒店业市场景气调查报告", "年度白皮书"],
        "value": "1985入华 · 酒店咨询老牌 · 季度景气指数",
        "credibility": "★★★★★",
    },
    "HotelleMatrix": {
        "name": "Hotelle Matrix (浩华旗下)",
        "name_zh": "厚海数据",
        "category": "数据平台",
        "url": "https://www.hotellematrixdata.com",
        "publish_frequency": "月度",
        "key_reports": ["RevPAR/OCC/ADR 月度数据", "城市级数据"],
        "value": "浩华旗下 · 月度真实行业数据",
        "credibility": "★★★★★",
    },
    "PwC": {
        "name": "PricewaterhouseCoopers (China)",
        "name_zh": "普华永道",
        "category": "四大咨询",
        "url": "https://www.pwc.com/cn",
        "publish_frequency": "年度报告",
        "key_reports": ["中国酒店业展望", "中国消费者洞察报告"],
        "value": "宏观+行业洞察 · 国际视角",
        "credibility": "★★★★",
    },
    "Deloitte": {
        "name": "Deloitte (China)",
        "name_zh": "德勤",
        "category": "四大咨询",
        "url": "https://www.deloitte.com/cn",
        "publish_frequency": "年度+季度",
        "key_reports": ["中国酒店业展望", "中国零售消费洞察"],
        "value": "行业洞察 · 财务/战略咨询",
        "credibility": "★★★★",
    },
    "EY": {
        "name": "Ernst & Young (China)",
        "name_zh": "安永",
        "category": "四大咨询",
        "url": "https://www.ey.com/cn",
        "publish_frequency": "年度",
        "key_reports": ["中国酒店市场展望", "消费者指数报告"],
        "value": "行业洞察 · 审计+咨询",
        "credibility": "★★★★",
    },
    "KPMG": {
        "name": "KPMG (China)",
        "name_zh": "毕马威",
        "category": "四大咨询",
        "url": "https://kpmg.com/cn",
        "publish_frequency": "年度+季度",
        "key_reports": ["中国酒店业前景展望", "消费者洞察报告"],
        "value": "行业前景 · 审计+咨询",
        "credibility": "★★★★",
    },

    # === Tier 5: 头部财报（10+10 = 20 家上市公司） ===
    "HuaZhu": {
        "name": "Huazhu Group (1179.HK / HTHT)",
        "name_zh": "华住集团",
        "category": "头部财报",
        "url": "https://www.huazhu.com",
        "ir_url": "https://ir.huazhu.com",
        "publish_frequency": "季度+年度",
        "key_reports": ["Q1/Q2/Q3/Q4 财报", "H1/H2 半年报"],
        "value": "国内最大连锁 · 中端+经济型",
        "credibility": "★★★★★",
    },
    "JinJiang": {
        "name": "Jin Jiang Hotels (600754.SH)",
        "name_zh": "锦江酒店",
        "category": "头部财报",
        "url": "https://www.jinjianghotels.com",
        "publish_frequency": "季度+年度",
        "value": "国内第一大酒店集团 · 17391 已签约",
        "credibility": "★★★★★",
    },
    "Atour": {
        "name": "Atour Lifestyle (ATAT.US)",
        "name_zh": "亚朵集团",
        "category": "头部财报",
        "url": "https://www.atourhotel.com",
        "ir_url": "https://ir.atourhotel.com",
        "value": "中高端+零售 · 利润涨67%",
        "credibility": "★★★★★",
    },
    "BTH": {
        "name": "BTG Homeinns (600258.SH)",
        "name_zh": "首旅酒店",
        "category": "头部财报",
        "url": "https://www.bthhotels.com",
        "value": "第三大集团 · 如家+中高端",
        "credibility": "★★★★★",
    },
    "JunTang": {
        "name": "JunTang Hotels (301073.SZ)",
        "name_zh": "君亭酒店",
        "category": "头部财报",
        "url": "https://www.juntinghotels.com",
        "value": "中高端 · 小而美",
        "credibility": "★★★★",
    },
    "Dossen": {
        "name": "Dossen (东呈集团)",
        "name_zh": "东呈集团",
        "category": "头部财报",
        "url": "https://www.dossen.com",
        "value": "中端连锁 · 华南龙头",
        "credibility": "★★★★",
    },
    "GreenTree": {
        "name": "GreenTree Inns (NASDAQ: GHG)",
        "name_zh": "格林酒店",
        "category": "头部财报",
        "value": "经济型连锁 · 美股上市",
        "credibility": "★★★★",
    },
    "Marriott": {
        "name": "Marriott International (MAR)",
        "name_zh": "万豪国际",
        "category": "外资财报",
        "url": "https://www.marriott.com",
        "ir_url": "https://marriott.gcs-web.com",
        "value": "全球第一 · 大中华区Q1 RevPAR+6%",
        "credibility": "★★★★★",
    },
    "Hilton": {
        "name": "Hilton Worldwide (HLT)",
        "name_zh": "希尔顿",
        "category": "外资财报",
        "url": "https://www.hilton.com",
        "ir_url": "https://ir.hilton.com",
        "value": "全球第二 · 2026 Q1 营收+8.98%",
        "credibility": "★★★★★",
    },
    "IHG": {
        "name": "InterContinental Hotels (IHG)",
        "name_zh": "洲际酒店",
        "category": "外资财报",
        "url": "https://www.ihg.com",
        "value": "全球第三 · 在建34.3万间客房",
        "credibility": "★★★★★",
    },
    "Hyatt": {
        "name": "Hyatt Hotels (H)",
        "name_zh": "凯悦酒店",
        "category": "外资财报",
        "url": "https://www.hyatt.com",
        "value": "全球奢华+高端",
        "credibility": "★★★★★",
    },
    "Wyndham": {
        "name": "Wyndham Hotels (WH)",
        "name_zh": "温德姆",
        "category": "外资财报",
        "url": "https://www.wyndhamhotels.com",
        "value": "全球最大特许经营",
        "credibility": "★★★★★",
    },
    "Accor": {
        "name": "Accor (AC.PA)",
        "name_zh": "雅高",
        "category": "外资财报",
        "url": "https://group.accor.com",
        "value": "全球奢华+生活方式",
        "credibility": "★★★★★",
    },
    "ShangriLa": {
        "name": "Shangri-La Asia (0069.HK)",
        "name_zh": "香格里拉",
        "category": "外资财报",
        "url": "https://www.shangri-la.com",
        "value": "亚太奢华 · 港股",
        "credibility": "★★★★",
    },
    "FourSeasons": {
        "name": "Four Seasons Hotels",
        "name_zh": "四季酒店",
        "category": "外资财报",
        "url": "https://www.fourseasons.com",
        "value": "全球奢华标杆",
        "credibility": "★★★★",
    },
    "BanyanTree": {
        "name": "Banyan Tree Holdings",
        "name_zh": "悦榕集团",
        "category": "外资财报",
        "url": "https://www.banyantree.com",
        "value": "亚太奢华度假",
        "credibility": "★★★★",
    },
    "Ascott": {
        "name": "The Ascott (CapitaLand)",
        "name_zh": "雅诗阁",
        "category": "外资财报",
        "url": "https://www.discoverasr.com/en/discover-asr/our-businesses/the-ascott-limited",
        "value": "亚太服务公寓",
        "credibility": "★★★★",
    },
    "JinJiangCap": {
        "name": "Jin Jiang Capital",
        "name_zh": "锦江资本",
        "category": "外资财报",
        "url": "https://www.jinjiangcapital.com",
        "value": "锦江系资本平台",
        "credibility": "★★★",
    },

    # === Tier 6: 券商研报 ===
    "CICC": {
        "name": "CICC (中金)",
        "name_zh": "中金公司",
        "category": "券商研报",
        "url": "https://www.cicc.com",
        "value": "《中国酒店业的向下扩容与向上突破》· 一线券商",
        "credibility": "★★★★★",
    },
    "CITIC": {
        "name": "CITIC Securities (中信证券)",
        "name_zh": "中信证券",
        "category": "券商研报",
        "url": "https://www.cs.com.cn",
        "value": "行业景气+目标价跟踪",
        "credibility": "★★★★★",
    },
    "EBSec": {
        "name": "Everbright Securities (光大证券)",
        "name_zh": "光大证券",
        "category": "券商研报",
        "url": "https://www.ebscn.com",
        "value": "周期复苏与结构红利共振研报",
        "credibility": "★★★★★",
    },
    "OrientSec": {
        "name": "Orient Securities (东方证券)",
        "name_zh": "东方证券",
        "category": "券商研报",
        "url": "https://www.dfzq.com.cn",
        "value": "行业景气+周期判断",
        "credibility": "★★★★★",
    },
    "CMSChina": {
        "name": "China Merchants Securities (招商证券)",
        "name_zh": "招商证券",
        "category": "券商研报",
        "url": "https://www.cmschina.com.cn",
        "value": "行业景气+周期判断",
        "credibility": "★★★★★",
    },
    "CaitongSec": {
        "name": "Caitong Securities (财通证券)",
        "name_zh": "财通证券",
        "category": "券商研报",
        "url": "https://www.ctsec.com",
        "value": "酒店行业周度数据跟踪· 出品方",
        "credibility": "★★★★",
    },

    # === Tier 7: 代理行 ===
    "JLL": {
        "name": "JLL Hotels (仲量联行)",
        "name_zh": "仲量联行",
        "category": "代理行",
        "url": "https://www.jll.com.cn",
        "publish_frequency": "季度+年报+白皮书",
        "key_reports": ["酒店运营商信心指数", "中国REITs白皮书"],
        "value": "投资交易+信心指数· 2026 GOP -1~-2%",
        "credibility": "★★★★★",
    },
    "CushWake": {
        "name": "Cushman & Wakefield (戴德梁行)",
        "name_zh": "戴德梁行",
        "category": "代理行",
        "url": "https://www.cushmanwakefield.com",
        "value": "投资交易+酒店业市场报告",
        "credibility": "★★★★★",
    },
    "Savills": {
        "name": "Savills (第一太平戴维斯)",
        "name_zh": "第一太平戴维斯",
        "category": "代理行",
        "url": "https://www.savills.com",
        "value": "亚太酒店投资+市场报告",
        "credibility": "★★★★★",
    },
    "CBRE": {
        "name": "CBRE Hotels",
        "name_zh": "世邦魏理仕",
        "category": "代理行",
        "url": "https://www.cbre.com",
        "value": "全球酒店投资+商业地产",
        "credibility": "★★★★★",
    },
    "Colliers": {
        "name": "Colliers (高力国际)",
        "name_zh": "高力国际",
        "category": "代理行",
        "url": "https://www.colliers.com",
        "value": "亚太酒店投资",
        "credibility": "★★★★",
    },
    "KnightFrank": {
        "name": "Knight Frank",
        "name_zh": "莱坊",
        "category": "代理行",
        "url": "https://www.knightfrank.com",
        "value": "高端酒店投资",
        "credibility": "★★★★",
    },

    # === Tier 8: 交通部数据 ===
    "CAAC": {
        "name": "CAAC (民航局)",
        "name_zh": "中国民航局",
        "category": "交通部",
        "url": "http://www.caac.gov.cn",
        "publish_frequency": "月度",
        "value": "民航客流 · 需求侧前置指标",
        "credibility": "★★★★★",
    },
    "CRC": {
        "name": "China Railway (国铁集团)",
        "name_zh": "国家铁路集团",
        "category": "交通部",
        "url": "http://www.china-railway.com.cn",
        "publish_frequency": "月度",
        "value": "铁路客流 · 商旅基础",
        "credibility": "★★★★★",
    },

    # === Tier 9: OTA 平台 ===
    "Ctrip": {
        "name": "Ctrip (携程)",
        "name_zh": "携程",
        "category": "OTA",
        "url": "https://www.trip.com",
        "value": "订单+价格+搜索热度 · 国内最大 OTA",
        "credibility": "★★★★★",
    },
    "Meituan": {
        "name": "Meituan (美团)",
        "name_zh": "美团",
        "category": "OTA",
        "url": "https://www.meituan.com",
        "value": "本地生活+酒店预订",
        "credibility": "★★★★★",
    },
    "Qunar": {
        "name": "Qunar (去哪儿)",
        "name_zh": "去哪儿",
        "category": "OTA",
        "url": "https://www.qunar.com",
        "value": "机票+酒店预订 · 暑期预测发布",
        "credibility": "★★★★★",
    },
    "Fliggy": {
        "name": "Fliggy (飞猪)",
        "name_zh": "飞猪",
        "category": "OTA",
        "url": "https://www.fliggy.com",
        "value": "阿里旗下 · 年轻客群",
        "credibility": "★★★★★",
    },
    "TongCheng": {
        "name": "Tongcheng Travel (同程旅行)",
        "name_zh": "同程旅行",
        "category": "OTA 补充",
        "url": "https://www.ly.com",
        "value": "下沉市场+暑期预测",
        "credibility": "★★★★",
    },
    "Tujia": {
        "name": "Tujia (途家)",
        "name_zh": "途家",
        "category": "OTA 补充",
        "url": "https://www.tujia.com",
        "value": "民宿+短租",
        "credibility": "★★★★",
    },
    "Muniao": {
        "name": "Muniao (木鸟民宿)",
        "name_zh": "木鸟民宿",
        "category": "OTA 补充",
        "url": "https://www.muniao.com",
        "value": "民宿补充",
        "credibility": "★★★",
    },

    # === Tier 10: 转让数据 ===
    "ZhiDian": {
        "name": "Zhidian (指点网)",
        "name_zh": "指点网",
        "category": "转让数据",
        "url": "https://www.jiudianrong.com",
        "value": "酒店转让挂牌量+成交周期",
        "credibility": "★★★★",
    },

    # === Tier 11: 行业研究 ===
    "HorwathMMI": {
        "name": "Horwath HTL MMI (浩华景气指数)",
        "name_zh": "浩华景气指数",
        "category": "行业研究",
        "url": "https://www.horwathhtl.com",
        "value": "季度景气指数 · 经理人信心",
        "credibility": "★★★★★",
    },
    "MeiDian": {
        "name": "Meidian (迈点研究院)",
        "name_zh": "迈点研究院",
        "category": "行业研究",
        "url": "https://www.meadin.com",
        "value": "MBI 品牌指数+榜单",
        "credibility": "★★★★",
    },
    "PinOrange": {
        "name": "PinOrange Tourism (品橙旅游)",
        "name_zh": "品橙旅游",
        "category": "行业研究",
        "url": "http://www.pinchain.com",
        "value": "文旅行业研究",
        "credibility": "★★★",
    },
    "BJU": {
        "name": "Beijing Union University (北二外)",
        "name_zh": "北京第二外国语学院",
        "category": "行业研究",
        "url": "https://www.bisu.edu.cn",
        "value": "旅游酒店学术研究",
        "credibility": "★★★",
    },

    # === Tier 12: 用户调研 ===
    "TencentTI": {
        "name": "Tencent Smart Tourism (腾讯智慧文旅)",
        "name_zh": "腾讯智慧文旅",
        "category": "用户调研",
        "url": "https://cloud.tencent.com/product/tourism",
        "value": "客群画像·需求侧",
        "credibility": "★★★★",
    },
}

# 统计
print(f"[INIT] 酒店行业信源矩阵: {len(HOTEL_SOURCES)} 个")
by_category = {}
for k, v in HOTEL_SOURCES.items():
    cat = v["category"]
    by_category[cat] = by_category.get(cat, 0) + 1
for cat, cnt in by_category.items():
    print(f"  · {cat}: {cnt}")


# ============================================================
# 抓取接口（基于 crawl4ai）
# ============================================================

@dataclass
class SourceResult:
    """单信源抓取结果"""
    source_id: str
    name: str
    name_zh: str
    category: str
    url: str
    success: bool
    markdown_length: int = 0
    extracted: Optional[Dict] = None
    error: str = ""
    elapsed: float = 0.0
    fetched_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class HotelSourceCrawler:
    """28 信源抓取器（基于 crawl4ai）"""

    def __init__(self):
        from crawl4ai_wrapper import get_wrapper
        self._wrapper = get_wrapper()

    def fetch(self,
              source_id: str,
              extraction_schema: Optional[Dict] = None,
              extraction_instruction: Optional[str] = None,
              timeout: int = 60) -> SourceResult:
        """抓取单个信源的最新报告"""
        if source_id not in HOTEL_SOURCES:
            return SourceResult(
                source_id=source_id,
                name="Unknown",
                name_zh="未知",
                category="unknown",
                url="",
                success=False,
                error=f"Unknown source_id: {source_id}",
            )

        info = HOTEL_SOURCES[source_id]
        import time
        start = time.time()

        try:
            result = self._wrapper.crawl_sync(
                info["url"],
                extraction_schema=extraction_schema,
                extraction_instruction=extraction_instruction,
                timeout=timeout,
            )
            elapsed = time.time() - start
            return SourceResult(
                source_id=source_id,
                name=info["name"],
                name_zh=info["name_zh"],
                category=info["category"],
                url=info["url"],
                success=result.success,
                markdown_length=len(result.markdown) if result.markdown else 0,
                extracted=result.extracted_json,
                error=result.error,
                elapsed=elapsed,
            )
        except Exception as e:
            elapsed = time.time() - start
            return SourceResult(
                source_id=source_id,
                name=info["name"],
                name_zh=info["name_zh"],
                category=info["category"],
                url=info["url"],
                success=False,
                error=f"{type(e).__name__}: {str(e)}",
                elapsed=elapsed,
            )

    def fetch_batch(self,
                    source_ids: List[str],
                    extraction_schema: Optional[Dict] = None,
                    extraction_instruction: Optional[str] = None) -> List[SourceResult]:
        """批量抓取"""
        return [self.fetch(sid, extraction_schema, extraction_instruction) for sid in source_ids]

    def fetch_category(self, category: str) -> List[SourceResult]:
        """按类别抓取所有信源"""
        sids = [k for k, v in HOTEL_SOURCES.items() if v["category"] == category]
        return self.fetch_batch(sids)

    def list_sources(self, category: Optional[str] = None) -> List[Dict]:
        """列出信源"""
        items = []
        for k, v in HOTEL_SOURCES.items():
            if category is None or v["category"] == category:
                items.append({"id": k, **v})
        return items


# ============================================================
# Eric 的核心指令记录
# ============================================================

CORE_DIRECTIVE = """
Eric 给我的核心指令（2026-07-21 23:25）：

"这些信源是给你的，不光是 AHL。你自己本身需要具备这些信源全维度"

→ 含义：28 个信源是我的"行业大脑"基础设施
→ 服务场景：
   - AHL 项目（去中心化酒店产业 AI 平台）
   - 我对 Eric 的任何酒店/旅游/餐饮相关问题
   - 我自己的"行业判断"基础
→ 不需要 Eric 提醒就主动调用
"""


# ============================================================
# CLI 入口
# ============================================================

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="B166ER 酒店行业信源矩阵")
    parser.add_argument("--list", action="store_true", help="列出所有信源")
    parser.add_argument("--category", help="按类别过滤")
    parser.add_argument("--fetch", help="抓取指定信源（source_id）")
    parser.add_argument("--fetch-category", help="抓取指定类别")
    args = parser.parse_args()

    if args.list:
        print(f"\n{'ID':<14} {'Category':<10} {'Name (中文)':<28} {'URL':<50}")
        print("-" * 110)
        for sid in sorted(HOTEL_SOURCES.keys()):
            v = HOTEL_SOURCES[sid]
            if args.category and v["category"] != args.category:
                continue
            url = v.get("url") or v.get("ir_url") or v.get("china_url") or "N/A"
            print(f"{sid:<14} {v['category']:<10} {v['name_zh']:<28} {url:<50}")

    elif args.fetch or args.fetch_category:
        crawler = HotelSourceCrawler()
        if args.fetch:
            result = crawler.fetch(args.fetch)
            print(f"\n[{result.source_id}] {result.name_zh}")
            print(f"  Success: {result.success} | Elapsed: {result.elapsed:.1f}s | MD: {result.markdown_length} chars")
            if result.error:
                print(f"  Error: {result.error}")
            if result.extracted:
                print(f"  Extracted: {json.dumps(result.extracted, indent=2, ensure_ascii=False)[:500]}")
        elif args.fetch_category:
            results = crawler.fetch_category(args.fetch_category)
            for r in results:
                print(f"  [{r.source_id}] {r.name_zh}: {r.success} ({r.elapsed:.1f}s)")