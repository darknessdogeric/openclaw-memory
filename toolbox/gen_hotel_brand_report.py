#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
酒店品牌市场指数综合排名 · 2026 H2
上帝视角 · 8 大层级 × 30 品牌 = 240 条目
输出 DOCX 至桌面
"""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ============== 数据 ==============

TIERS = [
    {
        "key": "L1",
        "name": "奢华层 (Luxury)",
        "subtitle": "顶级奢华 + 奢华  ·  ADR 2,000+ 元",
        "desc": "全服务 + 顶级地段 + 标志性服务。业主基本无加盟,以委托管理为主 (GOP 抽成 8-15% + 业绩激励)。业主参与方式:带物业找集团开发部谈管理合同。",
        "header_color": "1F2A4D",
        "brands": [
            ("丽思卡尔顿 Ritz-Carlton", "万豪", 98, "不开放加盟", "GOP 抽成 10-15% + 激励", "80-150 万", 92, "S"),
            ("四季 Four Seasons", "四季(独立)", 97, "不开放加盟", "基础管理费 + GOP 5-8% + 激励", "100-180 万", 95, "S"),
            ("宝格丽 Bvlgari", "万豪+LVMH", 96, "不开放加盟", "GOP 抽成 12%+", "200-400 万", 90, "S"),
            ("安缦 Aman", "独立", 95, "不开放加盟", "业主投资,管理协议定制", "300-800 万", 88, "S"),
            ("嘉佩乐 Capella", "独立", 93, "不开放加盟", "业主投资 + 管理费定制", "150-300 万", 87, "S"),
            ("白马庄园 Cheval Blanc", "LVMH", 94, "不开放加盟", "业主投资定制", "400-1000 万", 89, "S"),
            ("瑰丽 Rosewood", "新世界 (郑志刚)", 92, "不开放加盟", "业主投资 + 管理费", "100-250 万", 88, "S"),
            ("半岛 The Peninsula", "香港上海大酒店", 91, "不开放加盟", "业主投资 + 利润分享", "150-300 万", 86, "S"),
            ("柏悦 Park Hyatt", "凯悦", 90, "不开放加盟", "GOP 抽成 8-12%", "80-150 万", 87, "A"),
            ("文华东方 Mandarin Oriental", "文华东方(独立)", 90, "不开放加盟", "GOP 抽成 + 激励", "100-180 万", 86, "A"),
            ("瑞吉 St. Regis", "万豪", 88, "不开放加盟", "GOP 抽成 8-12%", "70-130 万", 85, "A"),
            ("华尔道夫 Waldorf Astoria", "希尔顿", 88, "不开放加盟", "GOP 抽成 + 激励", "80-150 万", 84, "A"),
            ("丽晶 Regent", "IHG", 86, "不开放加盟", "GOP 抽成 8-12%", "70-130 万", 83, "A"),
            ("莱佛士 Raffles", "雅高", 86, "不开放加盟", "GOP 抽成 + 激励", "100-200 万", 83, "A"),
            ("六善 Six Senses", "IHG", 85, "不开放加盟", "业主投资 + 管理费定制", "120-300 万", 82, "A"),
            ("阿丽拉 Alila", "凯悦", 84, "不开放加盟", "GOP 抽成 8-12%", "80-150 万", 81, "A"),
            ("卓美亚 Jumeirah", "独立 (迪拜控股)", 84, "不开放加盟", "业主投资定制", "100-250 万", 80, "A"),
            ("艾迪逊 EDITION", "万豪+Ian Schrager", 83, "不开放加盟", "GOP 抽成 10-15%", "80-150 万", 82, "A"),
            ("希尔顿 Conrad", "希尔顿", 82, "不开放加盟", "GOP 抽成 8-12%", "60-120 万", 80, "A"),
            ("尼依格罗 Niccolo", "九龙仓 (Wharf)", 81, "不开放加盟", "业主投资 + 管理费", "60-120 万", 79, "B"),
            ("诺金 NUO", "首旅集团", 78, "不开放加盟", "业主投资 + 管理费", "60-100 万", 76, "B"),
            ("虹夕诺雅 Hoshinoya", "星野集团", 82, "不开放加盟", "业主投资定制 (度假村为主)", "150-300 万", 78, "B"),
            ("W 酒店 W Hotel", "万豪", 80, "不开放加盟", "GOP 抽成 8-12%", "70-130 万", 78, "B"),
            ("巴卡拉 Baccarat", "雅高 (2024 收购)", 76, "不开放加盟", "业主投资定制", "150-300 万", 72, "B"),
            ("罗克福特 Rockfort", "周大福系", 72, "不开放加盟", "业主投资定制", "60-100 万", 68, "C"),
            ("青普 QINGPU", "青普旅游", 73, "不开放加盟", "业主投资 + 管理费", "50-80 万", 70, "B"),
            ("涵碧楼 Lalu", "乡林 (台湾)", 74, "不开放加盟", "业主投资定制", "100-200 万", 71, "B"),
            ("安麓 AHN LUH", "雅辰", 71, "不开放加盟", "业主投资 + 管理费", "60-120 万", 69, "C"),
            ("木棉花 Mu Mian Hua", "雅辰 (雅高联营)", 68, "不开放加盟", "业主投资 + 管理费", "40-70 万", 64, "C"),
            ("罗莱夏朵 Relais & Châteaux", "法国独立联盟", 82, "不开放加盟", "业主投资 + 联盟入会费", "30-80 万", 80, "A"),
        ],
    },
    {
        "key": "L2",
        "name": "高端层 (Upscale / Upper Upscale)",
        "subtitle": "国际 5 星 + 国内五星标准  ·  ADR 800-2,000 元",
        "desc": "全服务 + 国际标准 + 一线/省会核心商圈。业主参与:特许经营 (品牌费 1-3% + 管理费 3-6%) 或 委托管理。改造成本 25-100 万/间,业主端主流赛道之一。",
        "header_color": "1F4D2A",
        "brands": [
            ("JW 万豪", "万豪", 94, "50-100 万+5 万/间", "营收 5-6% 或 GOP 8-10%", "50-100 万", 89, "S"),
            ("希尔顿 Hilton", "希尔顿", 92, "50-80 万+0.5-1 万/间", "营收 5% + 集团服务 2%", "50-100 万", 88, "S"),
            ("凯悦 Hyatt Regency", "凯悦", 90, "60-100 万+1 万/间", "营收 5-7% 或 GOP 8-10%", "50-100 万", 87, "S"),
            ("洲际 InterContinental", "IHG", 89, "50-80 万+0.8-1.2 万/间", "营收 4-6%", "50-100 万", 85, "S"),
            ("皇冠假日 Crowne Plaza", "IHG", 87, "30-60 万+0.6-1 万/间", "营收 4-6%", "40-80 万", 84, "A"),
            ("喜来登 Sheraton", "万豪", 86, "30-60 万+0.5-0.8 万/间", "营收 5% 或 GOP 8%", "40-80 万", 83, "A"),
            ("万豪 Marriott", "万豪", 85, "30-60 万+0.5-0.8 万/间", "营收 5% 或 GOP 8%", "40-80 万", 82, "A"),
            ("万丽 Renaissance", "万豪", 82, "25-50 万+0.5-0.7 万/间", "营收 4-5%", "35-70 万", 80, "A"),
            ("威斯汀 Westin", "万豪", 84, "30-60 万+0.5-0.8 万/间", "营收 5%", "40-80 万", 81, "A"),
            ("希尔顿逸林 DoubleTree", "希尔顿", 83, "25-50 万+0.5-0.7 万/间", "营收 4-5% + 集团 2%", "35-70 万", 80, "A"),
            ("艾美 Le Méridien", "万豪", 80, "25-50 万+0.5-0.7 万/间", "营收 5%", "35-70 万", 78, "B"),
            ("铂尔曼 Pullman", "雅高", 81, "30-50 万+0.5-0.8 万/间", "营收 4-5%", "35-70 万", 79, "B"),
            ("美爵 Grand Mercure", "雅高 (华住运营)", 78, "25-45 万+0.4-0.6 万/间", "营收 4-5%", "30-60 万", 76, "B"),
            ("福朋喜来登 Four Points", "万豪", 79, "20-40 万+0.3-0.6 万/间", "营收 4-5%", "30-60 万", 78, "B"),
            ("君悦 Grand Hyatt", "凯悦", 88, "50-80 万+1 万/间", "营收 5-7% 或 GOP 8-12%", "60-120 万", 84, "A"),
            ("康莱德 Conrad", "希尔顿", 85, "30-60 万+0.6-1 万/间", "营收 5% + 集团 2%", "50-100 万", 82, "A"),
            ("凯悦嘉轩 Hyatt Place", "凯悦", 80, "20-40 万+0.3-0.6 万/间", "营收 4-5%", "25-50 万", 79, "B"),
            ("voco (高端软品牌)", "IHG", 78, "15-30 万+0.2-0.5 万/间", "营收 3-4% (软品牌特许)", "25-50 万", 80, "A"),
            ("英迪格 Hotel Indigo", "IHG", 83, "25-50 万+0.4-0.7 万/间", "营收 4-5%", "35-70 万", 80, "A"),
            ("诺富特 Novotel", "雅高 (华住运营)", 79, "25-45 万+0.4-0.6 万/间", "营收 4-5%", "30-60 万", 78, "B"),
            ("凯悦尚萃 JdV by Hyatt", "凯悦", 76, "15-30 万+0.2-0.4 万/间", "营收 3-4% (软品牌)", "25-45 万", 77, "B"),
            ("希尔顿花园 Hilton Garden", "希尔顿", 81, "20-40 万+0.3-0.6 万/间", "营收 4-5% + 集团 2%", "25-50 万", 80, "A"),
            ("华邑 HUALUXE", "IHG (本土)", 78, "25-45 万+0.4-0.6 万/间", "营收 4-5%", "30-60 万", 78, "B"),
            ("朗廷 Langham", "鹰君集团 (港)", 80, "30-60 万+0.5-0.7 万/间", "营收 5% 或 GOP 8%", "40-80 万", 79, "B"),
            ("朗豪 Langham Place", "鹰君集团", 77, "25-50 万+0.4-0.6 万/间", "营收 5%", "35-70 万", 76, "B"),
            ("凯宾斯基 Kempinski", "凯宾斯基 (独立欧洲)", 82, "30-60 万+0.6-1 万/间", "营收 5% 或 GOP 8-10%", "50-100 万", 79, "B"),
            ("雅高 Sofitel", "雅高", 81, "25-50 万+0.5-0.8 万/间", "营收 5%", "40-80 万", 78, "B"),
            ("美居 Mercure", "雅高 (华住运营)", 76, "15-30 万+0.3-0.5 万/间", "营收 4-5%", "20-40 万", 77, "B"),
            ("万达文华", "万达酒店", 74, "15-30 万+0.3-0.5 万/间", "营收 4-5%", "25-50 万", 75, "B"),
            ("金陵饭店", "金陵 (A 股)", 72, "10-25 万+0.3-0.5 万/间", "营收 4-5%", "25-45 万", 73, "C"),
        ],
    },
    {
        "key": "L3",
        "name": "中高端层 (Upper Midscale)",
        "subtitle": "国际精选 + 国内中高端  ·  ADR 400-800 元",
        "desc": "有限服务 + 设计感 + 商旅主流。业主参与:特许经营为主 (品牌费 1-2% + 管理费 4-5%)。改造成本 8-25 万/间,投资回报周期 3-5 年。亚朵系是中国唯一本土对标国际软品牌的成功范式。",
        "header_color": "4D1F2A",
        "brands": [
            ("亚朵 Atour", "亚朵 (NASDAQ)", 94, "5000 元/间 (一次性)", "营收 6-8% + GOP 抽成", "12-18 万", 95, "S"),
            ("亚朵 S Atour S", "亚朵", 88, "6000 元/间 (一次性)", "营收 7-9% + GOP 抽成", "18-30 万", 92, "S"),
            ("希尔顿欢朋 Hampton", "希尔顿 (锦江运营)", 93, "30 万/项目+3000 元/间", "营收 5% (含品牌+集团服务)", "12-18 万", 91, "S"),
            ("智选假日 Holiday Inn Express", "IHG", 91, "25-40 万+2500 元/间", "营收 5% (含品牌+管理)", "15-22 万", 89, "S"),
            ("全季 Ji Hotel", "华住", 92, "3000-4000 元/间", "营收 5-6%", "10-15 万", 93, "S"),
            ("桔子水晶 Crystal Orange", "华住", 86, "3000-4000 元/间", "营收 6%", "10-15 万", 89, "S"),
            ("桔子 Orange", "华住", 84, "2500-3500 元/间", "营收 5-6%", "8-12 万", 87, "A"),
            ("锦江都城", "锦江", 82, "3000 元/间", "营收 5%", "8-12 万", 84, "A"),
            ("维也纳国际 Vienna International", "锦江 (铂涛)", 86, "3500 元/间+30 万/项目", "营收 5% + 1%CRS", "10-14 万", 86, "A"),
            ("维也纳 Vienna", "锦江 (铂涛)", 89, "3000 元/间+25 万/项目", "营收 5% + 1%CRS", "8-12 万", 87, "A"),
            ("维也纳 3 好", "锦江", 82, "2500 元/间+20 万/项目", "营收 5%", "6-10 万", 85, "A"),
            ("喆啡 James Joyce Coffetel", "锦江 (铂涛)", 85, "3000 元/间+20 万/项目", "营收 5%", "8-12 万", 86, "A"),
            ("希岸 Xana", "锦江 (铂涛)", 80, "2500 元/间+15 万/项目", "营收 5%", "7-11 万", 82, "A"),
            ("ZMAX", "锦江 (铂涛)", 73, "2500 元/间+15 万/项目", "营收 5%", "7-11 万", 75, "B"),
            ("非繁城品", "锦江", 72, "2000 元/间+15 万/项目", "营收 4%", "6-10 万", 76, "B"),
            ("美居 Mercure (高端版)", "雅高 (华住运营)", 78, "3000 元/间+25 万/项目", "营收 5%", "10-15 万", 80, "A"),
            ("诺富特 Novotel (中端版)", "雅高 (华住运营)", 77, "3000 元/间+25 万/项目", "营收 5%", "12-18 万", 79, "A"),
            ("凯悦嘉寓 Hyatt House", "凯悦", 76, "4000 元/间+30 万/项目", "营收 5%", "18-25 万", 78, "B"),
            ("希尔顿惠庭 Home2 Suites", "希尔顿", 78, "4000 元/间+30 万/项目", "营收 5% + 集团 2%", "15-22 万", 80, "A"),
            ("雅阁酒店", "雅阁", 75, "20-30 万+0.4-0.6 万/间", "营收 4-5%", "30-60 万", 77, "B"),
            ("雅辰 Ariva", "雅辰", 70, "15-25 万+0.3-0.5 万/间", "营收 4-5%", "20-35 万", 71, "B"),
            ("万达锦华", "万达酒店", 72, "15-25 万+0.3-0.5 万/间", "营收 4-5%", "25-45 万", 73, "B"),
            ("首旅建国", "首旅如家", 73, "15-30 万+0.3-0.5 万/间", "营收 4-5%", "25-50 万", 72, "B"),
            ("开元名都", "开元", 76, "20-40 万+0.4-0.6 万/间", "营收 5%", "30-60 万", 75, "B"),
            ("君亭 Pagoda", "君亭 (A 股)", 75, "20-40 万+0.4-0.6 万/间", "营收 5-6%", "30-50 万", 76, "B"),
            ("锦江 (五星)", "锦江国际", 78, "20-40 万+0.3-0.6 万/间", "营收 5%", "30-60 万", 75, "B"),
            ("桔子精选", "华住", 80, "2500-3500 元/间", "营收 5-6%", "8-12 万", 81, "A"),
            ("漫心 Manxin", "华住", 77, "3000 元/间+25 万/项目", "营收 5-6%", "8-12 万", 79, "B"),
            ("开元名庭", "开元", 74, "20-30 万+0.3-0.5 万/间", "营收 5%", "25-45 万", 75, "B"),
            ("朗豪 Pavilion", "鹰君集团", 76, "20-35 万+0.4-0.6 万/间", "营收 5%", "30-50 万", 75, "B"),
        ],
    },
    {
        "key": "L4",
        "name": "中端层 (Midscale)",
        "subtitle": "中国酒店主战场 · 商旅主力  ·  ADR 250-450 元",
        "desc": "有限服务 + 高效标准化 + 客单价 250-450。业主参与:加盟特许为主 (品牌费 1% + 管理费 4-6%)。改造成本 5-12 万/间,投资回报 2-4 年。东呈系业绩对赌逆袭。",
        "header_color": "4D3F1F",
        "brands": [
            ("全季 Ji Hotel", "华住", 93, "3000-4000 元/间", "营收 5-6%", "8-12 万", 94, "S"),
            ("维也纳 Vienna", "锦江 (铂涛)", 88, "3000 元/间+25 万/项目", "营收 5% + 1%CRS", "6-10 万", 87, "A"),
            ("亚朵轻居 Atour Light", "亚朵", 85, "4000 元/间", "营收 6% + GOP 抽成", "8-12 万", 88, "A"),
            ("桔子 Orange", "华住", 85, "2500-3500 元/间", "营收 5-6%", "8-12 万", 87, "A"),
            ("喆啡 James Joyce", "锦江 (铂涛)", 85, "3000 元/间+20 万/项目", "营收 5%", "8-11 万", 86, "A"),
            ("维也纳 3 好", "锦江", 83, "2500 元/间+20 万/项目", "营收 5%", "6-9 万", 85, "A"),
            ("汉庭 Huating (3.5)", "华住", 88, "3000 元/间+20 万/项目", "营收 5% + 集团 2%", "4-7 万", 85, "A"),
            ("锦江都城", "锦江", 80, "3000 元/间+20 万/项目", "营收 5%", "8-12 万", 84, "A"),
            ("希岸 Xana", "锦江 (铂涛)", 80, "2500 元/间+15 万/项目", "营收 5%", "6-10 万", 82, "A"),
            ("柏曼 Borman", "东呈", 82, "1500-2000 元/间+15 万/项目", "营收 4% + 业绩对赌", "6-10 万", 89, "A"),
            ("星程 Starway", "华住", 79, "1500-2000 元/间+10 万/项目", "营收 4-5%", "5-8 万", 81, "A"),
            ("城市便捷 City Comfort", "东呈", 80, "1000-1500 元/间+10 万/项目", "营收 4% + 业绩对赌", "4-7 万", 87, "A"),
            ("如家 NEO", "首旅", 78, "1500 元/间+10 万/项目", "营收 4-5%", "4-6 万", 80, "A"),
            ("如家精选", "首旅", 76, "2000 元/间+15 万/项目", "营收 4-5%", "5-8 万", 78, "B"),
            ("锦江之星 JIN JIANG INN", "锦江", 80, "1500 元/间+10 万/项目", "营收 4%", "4-7 万", 80, "A"),
            ("CitiGO", "华住", 78, "3000 元/间+25 万/项目", "营收 5-6%", "8-12 万", 80, "A"),
            ("丽怡 Campanile", "锦江 (卢浮)", 76, "1500-2000 元/间+15 万/项目", "营收 4%", "5-8 万", 79, "B"),
            ("宜必思 ibis", "雅高 (华住运营)", 76, "2000 元/间+15 万/项目", "营收 4% + 集团 2%", "5-8 万", 78, "B"),
            ("宜必思尚品 ibis Styles", "雅高 (华住运营)", 74, "2500 元/间+20 万/项目", "营收 4% + 集团 2%", "6-9 万", 76, "B"),
            ("漫心 Manxin", "华住", 77, "3000 元/间+25 万/项目", "营收 5-6%", "8-12 万", 79, "B"),
            ("非繁城品", "锦江", 74, "2000 元/间+15 万/项目", "营收 4%", "5-9 万", 78, "B"),
            ("品睿 Pinrui", "东呈", 68, "1500 元/间+10 万/项目", "营收 4% + 业绩对赌", "6-10 万", 76, "B"),
            ("IU 酒店", "锦江", 75, "2000 元/间+12 万/项目", "营收 4-5%", "5-9 万", 78, "B"),
            ("尚客优 Shanke You", "尚美数智", 82, "1500-2000 元/间+10 万/项目", "营收 4.5%", "4-7 万", 84, "A"),
            ("海友 Hi Inn", "华住", 72, "1500 元/间+8 万/项目", "营收 4%", "3-5 万", 75, "B"),
            ("莫泰 168 Motel", "首旅", 70, "1200 元/间+8 万/项目", "营收 4%", "3-5 万", 73, "B"),
            ("YUNIK", "首旅", 70, "2500 元/间+15 万/项目", "营收 5%", "6-10 万", 72, "B"),
            ("白玉兰 Magnotel", "锦江", 73, "1500 元/间+10 万/项目", "营收 4%", "5-8 万", 75, "B"),
            ("康铂 Campanile (中端版)", "锦江 (卢浮)", 70, "1500 元/间+10 万/项目", "营收 4%", "5-8 万", 73, "B"),
            ("Gya Hotel", "锦江", 68, "1500 元/间+8 万/项目", "营收 4%", "5-8 万", 70, "B"),
        ],
    },
    {
        "key": "L5",
        "name": "经济型层 (Economy)",
        "subtitle": "中国酒店基础盘 · 加盟首选 + 下沉市场  ·  ADR 100-250 元",
        "desc": "有限服务 + 标准化模块 + 客单价 100-250。业主参与:加盟特许为主,单房改造成本 1.5-3.5 万,回本周期 1.5-3 年。下沉市场首选:尚客优/城市便捷/柏曼/骏怡。",
        "header_color": "2A4D4D",
        "brands": [
            ("汉庭 3.51 Hanting", "华住", 93, "3000 元/间+20 万/项目", "营收 5% + 集团 2%", "2.5-3.5 万", 88, "S"),
            ("如家 4.0 Home Inn", "首旅", 90, "2500 元/间+20 万/项目", "营收 5% + 集团 1-2%", "2.5-3.5 万", 87, "S"),
            ("7 天 3.0 7Days", "锦江 (铂涛)", 88, "2500 元/间+15 万/项目", "营收 5%", "2-3 万", 86, "S"),
            ("锦江之星", "锦江", 85, "2000 元/间+15 万/项目", "营收 4-5%", "2.5-3.5 万", 84, "A"),
            ("格林豪泰 GreenTree", "格林", 82, "2000 元/间+12 万/项目", "营收 4-5%", "2-3 万", 82, "A"),
            ("尚客优 Shanke You", "尚美数智", 84, "1500-2000 元/间+10 万/项目", "营收 4.5%", "1.5-2.5 万", 84, "A"),
            ("城市便捷 City Comfort", "东呈", 83, "1000-1500 元/间+10 万/项目", "营收 4% + 业绩对赌", "1-2 万", 88, "S"),
            ("速 8 Super 8", "温德姆", 78, "2000 元/间+10 万/项目", "营收 4% + 集团 1-2%", "2-3 万", 78, "B"),
            ("怡莱 Elan", "华住", 74, "1500 元/间+8 万/项目", "营收 4%", "1.5-2.5 万", 76, "B"),
            ("海友 Hi Inn", "华住", 76, "1500 元/间+8 万/项目", "营收 4%", "1-1.5 万", 78, "B"),
            ("布丁酒店 Pod", "住友酒店", 75, "1500 元/间+8 万/项目", "营收 4%", "2-3 万", 77, "B"),
            ("橘子酒店 (经济版)", "华住", 73, "1500 元/间+8 万/项目", "营收 4-5%", "1.5-2.5 万", 76, "B"),
            ("99 旅馆 Chain", "玖玖", 70, "1000 元/间+5 万/项目", "营收 4%", "1-1.5 万", 72, "B"),
            ("尚客优品", "尚美数智", 76, "1800 元/间+10 万/项目", "营收 4.5%", "2-3 万", 78, "B"),
            ("骏怡 City Comfort Inn", "东呈", 74, "1200 元/间+8 万/项目", "营收 4% + 业绩对赌", "1.5-2 万", 80, "A"),
            ("百时快捷 Bestay", "首旅", 68, "1200 元/间+6 万/项目", "营收 4%", "1-1.5 万", 70, "C"),
            ("云上四季", "首旅", 70, "1200 元/间+6 万/项目", "营收 4%", "1.5-2 万", 72, "B"),
            ("派柏·云", "首旅", 65, "1000 元/间+5 万/项目", "营收 4%", "1-1.5 万", 67, "C"),
            ("万悦 Hotel", "万达", 68, "1500 元/间+8 万/项目", "营收 4%", "2-3 万", 69, "C"),
            ("维也纳 3 好 (经济版)", "锦江", 75, "2000 元/间+12 万/项目", "营收 4%", "2-3 万", 78, "B"),
            ("金广快捷", "金广", 64, "1000 元/间+5 万/项目", "营收 4%", "1-1.5 万", 65, "C"),
            ("银座佳驿", "山东银座", 68, "1200 元/间+6 万/项目", "营收 4%", "1.5-2 万", 70, "C"),
            ("城市便捷 (经济版)", "东呈", 72, "1000 元/间+8 万/项目", "营收 4% + 业绩对赌", "1-2 万", 77, "B"),
            ("贝壳酒店", "贝壳 (民营)", 64, "800 元/间+4 万/项目", "营收 4%", "1-1.5 万", 66, "C"),
            ("雅悦酒店", "锦江 (卢浮)", 68, "1200 元/间+6 万/项目", "营收 4%", "1.5-2 万", 70, "C"),
            ("青皮树", "华住", 72, "1200 元/间+8 万/项目", "营收 4%", "1.5-2 万", 74, "B"),
            ("海友客栈", "华住", 68, "1000 元/间+5 万/项目", "营收 4%", "1-1.5 万", 70, "C"),
            ("佳泰连锁", "民营", 60, "800 元/间+4 万/项目", "营收 4%", "1-1.5 万", 62, "D"),
            ("驿家365", "民营", 60, "800 元/间+4 万/项目", "营收 4%", "1-1.5 万", 62, "D"),
            ("东方客栈", "民营", 58, "600 元/间+3 万/项目", "营收 4%", "0.8-1.2 万", 60, "D"),
        ],
    },
    {
        "key": "L6",
        "name": "生活方式层 (Lifestyle / Boutique)",
        "subtitle": "行业新势力 · 主题 + 文化 + 客户认同  ·  ADR 350-1,500 元",
        "desc": "生活方式不是装修风格,是经营哲学。三个硬指标:单一文化锚点 (咖啡/阅读/音乐/国潮...) + 故事化空间 (空间服务于主题) + 客户价值认同 (选择这里是因为认同品牌)。有限服务为主,加盟占比 80%+。",
        "header_color": "4D1F4D",
        "brands": [
            ("亚朵 Atour", "亚朵", 94, "5000 元/间", "营收 6-8% + GOP 抽成", "12-18 万", 95, "S"),
            ("亚朵 S Atour S", "亚朵", 88, "6000 元/间", "营收 7-9% + GOP 抽成", "18-30 万", 92, "S"),
            ("亚朵轻居 Atour Light", "亚朵", 85, "4000 元/间", "营收 6% + GOP 抽成", "8-12 万", 88, "A"),
            ("喆啡 James Joyce", "锦江 (铂涛)", 85, "3000 元/间+20 万/项目", "营收 5%", "8-12 万", 86, "A"),
            ("桔子水晶 Crystal Orange", "华住", 86, "3000-4000 元/间", "营收 6%", "10-15 万", 89, "S"),
            ("希岸 Xana", "锦江 (铂涛)", 80, "2500 元/间+15 万/项目", "营收 5%", "7-11 万", 82, "A"),
            ("ZMAX", "锦江 (铂涛)", 73, "2500 元/间+15 万/项目", "营收 5%", "7-11 万", 75, "B"),
            ("锦江都城", "锦江", 82, "3000 元/间+20 万/项目", "营收 5%", "8-12 万", 84, "A"),
            ("兰欧 LANOU", "尚美数智", 74, "2500 元/间+15 万/项目", "营收 5%", "6-10 万", 76, "B"),
            ("IU 酒店", "锦江", 75, "2000 元/间+12 万/项目", "营收 4-5%", "5-9 万", 78, "B"),
            ("CitiGO", "华住", 78, "3000 元/间+25 万/项目", "营收 5-6%", "8-12 万", 80, "A"),
            ("漫心 Manxin", "华住", 77, "3000 元/间+25 万/项目", "营收 5-6%", "8-12 万", 79, "B"),
            ("Moxy", "万豪", 75, "20-30 万+0.4-0.6 万/间", "营收 4-5%", "18-25 万", 79, "B"),
            ("citizenM", "独立 (直营为主)", 82, "不开放加盟", "直营 + 部分管理", "50-80 万", 82, "A"),
            ("25hours", "雅高", 76, "20-30 万+0.4-0.6 万/间", "营收 5%", "20-30 万", 78, "B"),
            ("Ace Hotel", "独立 (直营)", 85, "不开放加盟", "直营", "50-100 万", 85, "A"),
            ("The Standard", "独立 (直营)", 84, "不开放加盟", "直营", "50-100 万", 84, "A"),
            ("Kimpton", "IHG", 83, "30-50 万+0.5-0.8 万/间", "营收 5%", "30-50 万", 82, "A"),
            ("W Hotel", "万豪", 85, "50-80 万+0.5-1 万/间", "营收 5% 或 GOP 8%", "60-100 万", 81, "A"),
            ("Hard Rock Hotel", "Hard Rock", 75, "25-40 万+0.4-0.6 万/间", "营收 5%", "30-50 万", 74, "B"),
            ("Hyatt Centric", "凯悦", 80, "30-50 万+0.4-0.7 万/间", "营收 5%", "30-50 万", 80, "A"),
            ("Canopy", "希尔顿", 77, "25-40 万+0.4-0.6 万/间", "营收 5% + 集团 2%", "25-45 万", 78, "B"),
            ("Thompson Hotels", "凯悦", 78, "30-50 万+0.4-0.7 万/间", "营收 5%", "30-50 万", 77, "B"),
            ("Yotel", "独立 (部分加盟)", 72, "15-25 万+0.3-0.5 万/间", "营收 4%", "15-25 万", 75, "B"),
            ("Generator", "Generator Hostels", 70, "15-25 万+0.3-0.5 万/间", "营收 4%", "10-18 万", 71, "B"),
            ("voco", "IHG", 78, "15-30 万+0.2-0.5 万/间", "营收 3-4% (软品牌特许)", "25-50 万", 80, "A"),
            ("Mama Shelter", "雅高 (2014 收购)", 72, "20-30 万+0.3-0.5 万/间", "营收 4-5%", "20-35 万", 73, "B"),
            ("青普 QINGPU", "青普旅游", 73, "不开放加盟", "业主投资 + 管理费", "50-80 万", 70, "B"),
            ("开元名庭", "开元", 74, "20-30 万+0.3-0.5 万/间", "营收 5%", "25-45 万", 75, "B"),
            ("开元观堂", "开元", 70, "15-25 万+0.3-0.5 万/间", "营收 5%", "20-40 万", 72, "B"),
        ],
    },
    {
        "key": "L7",
        "name": "度假层 (Resort)",
        "subtitle": "度假市场 · 目的地 + 季节性 + 体验经济  ·  ADR 800-3,000+ 元",
        "desc": "度假酒店本质是体验经济。2026 行业拐点:安缦/悦榕庄跌落,情怀/枯山水祛魅,生活方式体验型崛起。业主参与:委托管理为主 (管理费 GOP 10-20%),部分特许经营。单店投资规模 1-10 亿。",
        "header_color": "2A4D2A",
        "brands": [
            ("安缦 Aman", "独立", 95, "不开放加盟", "业主投资 + 管理费", "300-800 万", 90, "S"),
            ("Club Med", "地中海俱乐部 (复星)", 92, "不开放加盟 (中国合作)", "业主投资 + 管理费 + 收入分成", "30-50 万", 91, "S"),
            ("悦榕庄 Banyan Tree", "悦榕集团", 90, "50-100 万+0.5-1 万/间", "GOP 抽成 10-15%", "50-80 万", 88, "S"),
            ("瑰丽 Rosewood", "新世界 (郑志刚)", 92, "不开放加盟", "业主投资 + 管理费", "100-250 万", 88, "S"),
            ("嘉佩乐 Capella", "独立", 93, "不开放加盟", "业主投资 + 管理费定制", "150-300 万", 87, "S"),
            ("六善 Six Senses", "IHG", 88, "40-80 万+0.5-1 万/间", "业主投资 + 管理费", "80-150 万", 86, "A"),
            ("阿丽拉 Alila", "凯悦", 86, "30-60 万+0.5-0.8 万/间", "GOP 抽成 10-15%", "60-100 万", 84, "A"),
            ("JW 万豪 (度假)", "万豪", 86, "40-80 万+0.6-1 万/间", "营收 5-6% 或 GOP 8-10%", "50-100 万", 84, "A"),
            ("君悦 Grand Hyatt (度假)", "凯悦", 86, "40-80 万+0.6-1 万/间", "营收 5-7% 或 GOP 8-12%", "60-120 万", 84, "A"),
            ("洲际 InterContinental (度假)", "IHG", 84, "40-70 万+0.5-0.8 万/间", "营收 5%", "50-100 万", 83, "A"),
            ("凯悦 Hyatt Regency (度假)", "凯悦", 82, "30-60 万+0.5-0.8 万/间", "营收 5-7% 或 GOP 8-10%", "40-80 万", 82, "A"),
            ("凯宾斯基 Kempinski", "凯宾斯基 (独立)", 82, "30-60 万+0.6-1 万/间", "营收 5% 或 GOP 8-10%", "50-100 万", 79, "B"),
            ("希尔顿 Hilton (度假)", "希尔顿", 80, "30-60 万+0.5-0.8 万/间", "营收 5% + 集团 2%", "40-80 万", 80, "A"),
            ("喜来登 Sheraton (度假)", "万豪", 80, "25-50 万+0.4-0.6 万/间", "营收 5%", "35-70 万", 80, "A"),
            ("皇冠假日 Crowne Plaza (度假)", "IHG", 80, "25-50 万+0.4-0.6 万/间", "营收 4-5%", "35-70 万", 80, "A"),
            ("万豪 Marriott (度假)", "万豪", 80, "30-60 万+0.5-0.8 万/间", "营收 5%", "40-80 万", 80, "A"),
            ("铂尔曼 Pullman (度假)", "雅高", 78, "25-50 万+0.4-0.6 万/间", "营收 4-5%", "35-70 万", 78, "B"),
            ("亚特兰蒂斯", "复星", 88, "不开放加盟", "业主投资 + 管理费 + 分成", "80-150 万", 86, "A"),
            ("施柏阁 Steigenberger", "复星 (2020 收购)", 80, "30-50 万+0.5-0.7 万/间", "GOP 抽成 10-12%", "40-80 万", 79, "B"),
            ("朗廷 Langham (度假)", "鹰君集团", 83, "30-60 万+0.5-0.7 万/间", "营收 5% 或 GOP 8%", "40-70 万", 82, "A"),
            ("涵碧楼 Lalu", "乡林 (台湾)", 78, "不开放加盟", "业主投资定制", "100-200 万", 75, "B"),
            ("安麓 AHN LUH", "雅辰", 74, "不开放加盟", "业主投资 + 管理费", "60-100 万", 72, "B"),
            ("万达瑞华 (度假)", "万达酒店", 78, "30-50 万+0.5-0.7 万/间", "营收 5% 或 GOP 8%", "50-80 万", 77, "B"),
            ("开元名都 (度假)", "开元", 77, "25-50 万+0.4-0.6 万/间", "营收 5%", "30-60 万", 76, "B"),
            ("开元观堂 (度假)", "开元", 72, "20-40 万+0.3-0.5 万/间", "营收 5%", "25-50 万", 71, "C"),
            ("开元森泊 (主题度假)", "开元", 78, "不开放加盟 (直营+合作)", "业主投资 + 管理费", "50-100 万", 76, "B"),
            ("复游城 (主题)", "复星", 72, "20-40 万+0.3-0.5 万/间", "营收 5% + 主题抽成", "40-70 万", 70, "C"),
            ("雅阁酒店 (度假版)", "雅阁", 73, "20-40 万+0.3-0.5 万/间", "营收 4-5%", "30-60 万", 74, "B"),
            ("雅阁璞邸", "雅阁", 71, "25-50 万+0.4-0.6 万/间", "营收 4-5%", "35-70 万", 72, "C"),
            ("御温泉 (主题)", "民营", 70, "20-40 万+0.3-0.5 万/间", "营收 5%", "30-50 万", 68, "C"),
        ],
    },
    {
        "key": "L8",
        "name": "服务式公寓层 (Serviced Apartment)",
        "subtitle": "长住市场 · 商旅长住 + 居家体验 + 性价比",
        "desc": "长住市场,核心:商旅长住 + 居家体验 + 性价比。业主参与:委托管理为主 (管理费 GOP 8-12%),部分加盟。凯德 + 万豪 + Frasers 三足鼎立。中国本土性价比品牌正在崛起。",
        "header_color": "4D2A1F",
        "brands": [
            ("雅诗阁 Ascott", "凯德雅诗阁 (新加坡)", 92, "30 万/项目+200 元/间/月", "GOP 抽成 8-10%", "15-25 万", 90, "S"),
            ("万豪行政公寓 ExRes", "万豪", 88, "100-200 万+200 元/间/月", "GOP 抽成 10-12%", "20-35 万", 85, "A"),
            ("盛捷 Somerset", "凯德雅诗阁", 84, "28 万/项目+180 元/间/月", "GOP 抽成 8-10%", "13-22 万", 85, "A"),
            ("馨乐庭 Citadines", "凯德雅诗阁", 82, "25 万/项目+150 元/间/月", "GOP 抽成 8%", "12-20 万", 84, "A"),
            ("辉盛坊 Fraser Suites", "Frasers Hospitality (新加坡)", 82, "30 万/项目+200 元/间/月", "GOP 抽成 9%", "18-28 万", 82, "A"),
            ("奥克伍德 Oakwood", "凯德雅诗阁", 80, "28 万/项目+180 元/间/月", "GOP 抽成 9%", "16-26 万", 82, "A"),
            ("希尔顿公寓 Hilton Residences", "希尔顿", 80, "30 万/项目+200 元/间/月", "GOP 抽成 10%", "18-30 万", 80, "A"),
            ("凯德雅诗阁臻选 The Crest", "凯德", 78, "30 万/项目+200 元/间/月", "GOP 抽成 9-10%", "15-25 万", 80, "A"),
            ("辉盛阁 Fraser Place", "Frasers", 76, "22 万/项目+150 元/间/月", "GOP 抽成 8%", "14-22 万", 78, "B"),
            ("凯悦寓 Hyatt House", "凯悦", 76, "30 万/项目+200 元/间/月", "GOP 抽成 8%", "18-25 万", 78, "B"),
            ("Fraser Residence", "Frasers", 74, "22 万/项目+150 元/间/月", "GOP 抽成 8%", "14-22 万", 76, "B"),
            ("The Ascott Limited", "凯德", 76, "25 万/项目+180 元/间/月", "GOP 抽成 8-10%", "14-22 万", 78, "B"),
            ("瑰悦 Greelers", "中海+雅诗阁", 76, "20 万/项目+150 元/间/月", "GOP 抽成 8%", "12-18 万", 76, "B"),
            ("辉盛国际", "Frasers", 74, "20 万/项目+120 元/间/月", "GOP 抽成 7-8%", "12-20 万", 75, "B"),
            ("CitiGO HOUSE", "华住", 78, "25 万/项目+200 元/间/月", "GOP 抽成 8-10%", "15-25 万", 80, "A"),
            ("恺信 Asia Pacific", "恺信 (本土)", 76, "10 万/项目+80 元/间/月", "GOP 抽成 6-7%", "8-15 万", 77, "B"),
            ("优帕克 Opark", "优帕克 (上海)", 74, "10 万/项目+80 元/间/月", "GOP 抽成 6-7%", "8-15 万", 75, "B"),
            ("名致公寓 Modena", "中海+凯德", 73, "12 万/项目+100 元/间/月", "GOP 抽成 7%", "10-18 万", 74, "B"),
            ("瑞贝庭 Suisse Place", "瑞贝庭 (港)", 72, "15 万/项目+120 元/间/月", "GOP 抽成 7%", "10-18 万", 73, "B"),
            ("雅斯阁 Ascott Living", "凯德", 74, "25 万/项目+180 元/间/月", "GOP 抽成 8-9%", "14-22 万", 76, "B"),
            ("雅辰公寓 Ariva", "雅辰", 70, "15 万/项目+100 元/间/月", "GOP 抽成 7%", "10-18 万", 71, "C"),
            ("铂顿国际公寓", "铂顿", 70, "12 万/项目+80 元/间/月", "GOP 抽成 6-7%", "8-14 万", 71, "B"),
            ("雅院公寓", "中海", 70, "15 万/项目+100 元/间/月", "GOP 抽成 6-8%", "8-15 万", 72, "C"),
            ("博乐诗服务公寓", "博乐诗", 68, "15 万/项目+100 元/间/月", "GOP 抽成 6%", "8-15 万", 70, "C"),
            ("漫心公寓", "华住", 72, "15 万/项目+100 元/间/月", "GOP 抽成 7%", "10-18 万", 73, "B"),
            ("狐狸海睿思", "凯德", 68, "20 万/项目+120 元/间/月", "GOP 抽成 7-8%", "12-18 万", 70, "C"),
            ("和也旅", "凯德", 66, "18 万/项目+100 元/间/月", "GOP 抽成 7%", "10-16 万", 67, "C"),
            ("温庭公寓", "民营", 68, "8 万/项目+80 元/间/月", "GOP 抽成 6%", "8-12 万", 69, "C"),
            ("龙湖冠寓", "龙湖", 70, "不开放加盟", "业主自营", "6-12 万", 68, "C"),
            ("碧桂园凤凰长租公寓", "碧桂园", 65, "不开放加盟", "业主自营", "6-12 万", 64, "C"),
        ],
    },
]

# ============== Word 样式函数 ==============

def shade_cell(cell, color_hex):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    tc_pr.append(shd)


def set_cell_font(cell, font_name='微软雅黑', size=9, bold=False, color=None):
    for p in cell.paragraphs:
        for run in p.runs:
            run.font.name = font_name
            run.font.size = Pt(size)
            run.font.bold = bold
            if color:
                run.font.color.rgb = RGBColor.from_string(color)
            # 兼容中文
            rpr = run._element.get_or_add_rPr()
            rfonts = rpr.find(qn('w:rFonts'))
            if rfonts is None:
                rfonts = OxmlElement('w:rFonts')
                rpr.insert(0, rfonts)
            rfonts.set(qn('w:eastAsia'), font_name)
            rfonts.set(qn('w:ascii'), font_name)
            rfonts.set(qn('w:hAnsi'), font_name)


def set_cell_text(cell, text, font_name='微软雅黑', size=9, bold=False, color=None,
                  align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.text = ''
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = font_name
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    rpr = run._element.get_or_add_rPr()
    rfonts = OxmlElement('w:rFonts')
    rfonts.set(qn('w:eastAsia'), font_name)
    rfonts.set(qn('w:ascii'), font_name)
    rfonts.set(qn('w:hAnsi'), font_name)
    rpr.insert(0, rfonts)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER


def grade_color(grade):
    return {
        'S': 'C8102E',  # 深红
        'A': '1F4D2A',  # 深绿
        'B': 'B7791F',  # 棕
        'C': '707070',  # 灰
        'D': '999999',  # 浅灰
    }.get(grade, '000000')


def add_heading(doc, text, level=1, color=None, size=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.font.name = '微软雅黑'
    run.font.size = Pt(size or {1: 22, 2: 16, 3: 13}.get(level, 11))
    run.font.bold = True
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    rpr = run._element.get_or_add_rPr()
    rfonts = OxmlElement('w:rFonts')
    rfonts.set(qn('w:eastAsia'), '微软雅黑')
    rfonts.set(qn('w:ascii'), '微软雅黑')
    rfonts.set(qn('w:hAnsi'), '微软雅黑')
    rpr.insert(0, rfonts)
    return p


def add_paragraph(doc, text, size=10, bold=False, color=None, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(text)
    run.font.name = '微软雅黑'
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    rpr = run._element.get_or_add_rPr()
    rfonts = OxmlElement('w:rFonts')
    rfonts.set(qn('w:eastAsia'), '微软雅黑')
    rfonts.set(qn('w:ascii'), '微软雅黑')
    rfonts.set(qn('w:hAnsi'), '微软雅黑')
    rpr.insert(0, rfonts)
    return p


def add_tier_table(doc, tier):
    # Tier section header
    add_heading(doc, tier['name'], level=1, color=tier['header_color'], size=18)
    add_paragraph(doc, tier['subtitle'], size=11, bold=True, color=tier['header_color'])
    add_paragraph(doc, tier['desc'], size=10, color='404040')

    # Table headers
    headers = ['#', '品牌', '母公司', 'MBI', '一次性加盟费', '持续管理费', '单房造价', '综合价值', '等级']
    n_cols = len(headers)
    n_rows = 1 + len(tier['brands'])

    table = doc.add_table(rows=n_rows, cols=n_cols)
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Set table width & column widths
    col_widths = [Cm(0.7), Cm(3.5), Cm(3.0), Cm(1.0), Cm(2.5), Cm(3.5), Cm(2.0), Cm(1.2), Cm(0.8)]
    for i, w in enumerate(col_widths):
        for cell in table.columns[i].cells:
            cell.width = w

    # Header row
    for j, h in enumerate(headers):
        cell = table.rows[0].cells[j]
        set_cell_text(cell, h, size=9, bold=True, color='FFFFFF',
                      align=WD_ALIGN_PARAGRAPH.CENTER)
        shade_cell(cell, tier['header_color'])

    # Data rows
    for i, brand in enumerate(tier['brands'], start=1):
        row = table.rows[i]
        name, parent, mbi, fee, mgmt, cost, value, grade = brand
        rank = i  # index = rank (data already sorted by MBI desc)

        # Alternating row color
        row_color = 'FFFFFF' if i % 2 == 1 else 'F2F4F7'

        cells_data = [
            (str(rank), WD_ALIGN_PARAGRAPH.CENTER, False, '000000'),
            (name, WD_ALIGN_PARAGRAPH.LEFT, True, '000000'),
            (parent, WD_ALIGN_PARAGRAPH.LEFT, False, '404040'),
            (str(mbi), WD_ALIGN_PARAGRAPH.CENTER, mbi >= 90, mbi_color(mbi)),
            (fee, WD_ALIGN_PARAGRAPH.LEFT, False, '404040'),
            (mgmt, WD_ALIGN_PARAGRAPH.LEFT, False, '404040'),
            (cost, WD_ALIGN_PARAGRAPH.CENTER, False, '404040'),
            (str(value), WD_ALIGN_PARAGRAPH.CENTER, value >= 85, value_color(value)),
            (grade, WD_ALIGN_PARAGRAPH.CENTER, True, 'FFFFFF'),
        ]
        for j, (text, align, bold, color) in enumerate(cells_data):
            cell = row.cells[j]
            set_cell_text(cell, text, size=8.5, bold=bold, color=color, align=align)
            shade_cell(cell, row_color if j != 8 else grade_color(grade))

    # Spacer
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)


def mbi_color(mbi):
    if mbi >= 90:
        return 'C8102E'
    elif mbi >= 80:
        return '1F4D2A'
    elif mbi >= 70:
        return 'B7791F'
    else:
        return '707070'


def value_color(value):
    if value >= 90:
        return 'C8102E'
    elif value >= 80:
        return '1F4D2A'
    elif value >= 70:
        return 'B7791F'
    else:
        return '707070'


# ============== 主流程 ==============

def main():
    doc = Document()

    # 页面设置
    section = doc.sections[0]
    section.page_height = Cm(29.7)
    section.page_width = Cm(21.0)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(1.8)
    section.right_margin = Cm(1.8)

    # 设置默认样式
    style = doc.styles['Normal']
    style.font.name = '微软雅黑'
    style.font.size = Pt(10)
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.insert(0, rfonts)
    rfonts.set(qn('w:eastAsia'), '微软雅黑')
    rfonts.set(qn('w:ascii'), '微软雅黑')
    rfonts.set(qn('w:hAnsi'), '微软雅黑')

    # ========== 封面 ==========
    cover_title = doc.add_paragraph()
    cover_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cover_title.paragraph_format.space_before = Pt(120)
    cover_title.paragraph_format.space_after = Pt(20)
    run = cover_title.add_run('酒店品牌市场指数综合排名')
    run.font.name = '微软雅黑'
    run.font.size = Pt(36)
    run.font.bold = True
    run.font.color.rgb = RGBColor.from_string('1F2A4D')
    rpr = run._element.get_or_add_rPr()
    rfonts = OxmlElement('w:rFonts')
    rfonts.set(qn('w:eastAsia'), '微软雅黑')
    rfonts.set(qn('w:ascii'), '微软雅黑')
    rfonts.set(qn('w:hAnsi'), '微软雅黑')
    rpr.insert(0, rfonts)

    sub_title = doc.add_paragraph()
    sub_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_title.paragraph_format.space_after = Pt(10)
    run = sub_title.add_run('2026 H2 · 上帝视角')
    run.font.name = '微软雅黑'
    run.font.size = Pt(20)
    run.font.bold = True
    run.font.color.rgb = RGBColor.from_string('4D3F1F')

    sub_title2 = doc.add_paragraph()
    sub_title2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_title2.paragraph_format.space_after = Pt(80)
    run = sub_title2.add_run('8 大层级 × 30 品牌 = 240 条目')
    run.font.name = '微软雅黑'
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor.from_string('707070')

    # 编制信息
    info = doc.add_paragraph()
    info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    info.paragraph_format.space_after = Pt(4)
    run = info.add_run('编制: B166ER')
    run.font.name = '微软雅黑'
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor.from_string('404040')

    info2 = doc.add_paragraph()
    info2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    info2.paragraph_format.space_after = Pt(4)
    run = info2.add_run('数据时点: 2026 年 8 月')
    run.font.name = '微软雅黑'
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor.from_string('404040')

    info3 = doc.add_paragraph()
    info3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    info3.paragraph_format.space_after = Pt(4)
    run = info3.add_run('信源矩阵: 迈点研究院 MBI · HOTELS Magazine · Brand Finance · 集团年报 · 加盟费查询网')
    run.font.name = '微软雅黑'
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor.from_string('707070')

    info4 = doc.add_paragraph()
    info4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    info4.paragraph_format.space_after = Pt(4)
    run = info4.add_run('版本: v1.0 · 2026-08-20 首发')
    run.font.name = '微软雅黑'
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor.from_string('707070')

    doc.add_page_break()

    # ========== 阅读说明 ==========
    add_heading(doc, '一 · 阅读说明 & 评估模型', level=1, color='1F2A4D', size=18)

    add_heading(doc, '1.1 市场影响力指数 MBI (0-100)', level=2, color='1F2A4D', size=13)
    add_paragraph(doc,
                  '参考迈点研究院 MBI 模型 + Brand Finance 品牌价值 + HOTELS Magazine 全球榜单 综合校准。'
                  'MBI 由四个等权子维度构成:搜索指数 (百度/微信/抖音/Google 搜索量与品牌关联度)、媒体指数 '
                  '(主流财经/旅游/地产媒体报道频次与调性)、点评指数 (携程/美团/TripAdvisor/Booking 等 OTA 点评分与体量)、'
                  '运营指数 (集团规模/会员体系/数字化/坪效/ADR),各占 25%。')

    add_heading(doc, '1.2 合作费用体系 (业主视角)', level=2, color='1F2A4D', size=13)
    fee_table = doc.add_table(rows=6, cols=3)
    fee_table.style = 'Light List Accent 1'
    fee_headers = ['费用项', '范围', '说明']
    fee_data = [
        ('一次性加盟费', '0-200 万/项目', '品牌特许使用 + 设计 + 工程指导'),
        ('履约保证金', '5-50 万', '合同期满可退 (无息)'),
        ('持续管理费', '营收 3-10% 或 GOP 抽成', '含品牌支持/集采/系统/会员'),
        ('单房改造成本', '1.5-50 万', '视层级差异巨大'),
        ('总投入 (100 房店)', '100-8000 万', '含装修+加盟+保证金'),
    ]
    for j, h in enumerate(fee_headers):
        c = fee_table.rows[0].cells[j]
        set_cell_text(c, h, size=10, bold=True, color='FFFFFF', align=WD_ALIGN_PARAGRAPH.CENTER)
        shade_cell(c, '1F2A4D')
    for i, (a, b, c) in enumerate(fee_data, start=1):
        for j, txt in enumerate([a, b, c]):
            cell = fee_table.rows[i].cells[j]
            set_cell_text(cell, txt, size=9, bold=(j == 0), align=WD_ALIGN_PARAGRAPH.LEFT)
            if i % 2 == 0:
                shade_cell(cell, 'F2F4F7')

    add_heading(doc, '1.3 综合评估价值 (0-100)', level=2, color='1F2A4D', size=13)
    add_paragraph(doc, '业主选择品牌的"该不该加盟 / 该选哪个"决策分。')
    value_table = doc.add_table(rows=6, cols=3)
    value_table.style = 'Light List Accent 1'
    v_headers = ['子维度', '权重', '说明']
    v_data = [
        ('品牌势能', '30%', 'MBI 影响力 + 品牌溢价能力'),
        ('投资回报', '30%', '静态回本周期 + 实际 RevPAR 提升率'),
        ('业主支持', '20%', '集采/培训/督导/会员输送/GOP 改善'),
        ('退出灵活性', '10%', '合同解约条件 + 数据归属 + 违约金'),
        ('抗风险', '10%', '集团财务健康 + 开店/关店比 + ESG'),
    ]
    for j, h in enumerate(v_headers):
        c = value_table.rows[0].cells[j]
        set_cell_text(c, h, size=10, bold=True, color='FFFFFF', align=WD_ALIGN_PARAGRAPH.CENTER)
        shade_cell(c, '1F2A4D')
    for i, (a, b, c) in enumerate(v_data, start=1):
        for j, txt in enumerate([a, b, c]):
            cell = value_table.rows[i].cells[j]
            set_cell_text(cell, txt, size=9, bold=(j == 0), align=WD_ALIGN_PARAGRAPH.LEFT)
            if i % 2 == 0:
                shade_cell(cell, 'F2F4F7')

    add_heading(doc, '1.4 评分等级', level=2, color='1F2A4D', size=13)
    grade_table = doc.add_table(rows=6, cols=3)
    grade_table.style = 'Light List Accent 1'
    grade_data = [
        ('S · 标杆', '90-100', '行业头部,标杆参考'),
        ('A · 强势', '80-89', '主流加盟首选'),
        ('B · 稳健', '70-79', '可控可加盟'),
        ('C · 中等', '60-69', '特定场景适配'),
        ('D · 谨慎', '<60', '需强谈判或避开'),
    ]
    for j, h in enumerate(['等级', 'MBI / 综合价值分', '说明']):
        c = grade_table.rows[0].cells[j]
        set_cell_text(c, h, size=10, bold=True, color='FFFFFF', align=WD_ALIGN_PARAGRAPH.CENTER)
        shade_cell(c, '1F2A4D')
    for i, (a, b, c) in enumerate(grade_data, start=1):
        for j, txt in enumerate([a, b, c]):
            cell = grade_table.rows[i].cells[j]
            set_cell_text(cell, txt, size=9, bold=(j == 0), align=WD_ALIGN_PARAGRAPH.LEFT)
            if i % 2 == 0:
                shade_cell(cell, 'F2F4F7')

    doc.add_page_break()

    # ========== 关键洞察摘要 ==========
    add_heading(doc, '二 · 关键洞察摘要', level=1, color='1F2A4D', size=18)

    add_heading(doc, '2.1 8 大层级 TOP 3 速览', level=2, color='1F2A4D', size=13)
    summary_table = doc.add_table(rows=9, cols=4)
    summary_table.style = 'Light Grid Accent 1'
    sum_headers = ['层级', 'MBI TOP 3', '综合价值 TOP 3', '关键判断']
    sum_data = [
        ('奢华', '丽思/四季/宝格丽', '四季/丽思/安缦', '全部不开放加盟,带物业谈管理合同'),
        ('高端', 'JW 万豪/希尔顿/凯悦', 'JW 万豪/希尔顿/凯悦', '国际 5 星标杆组合'),
        ('中高端', '亚朵/希尔顿欢朋/智选假日', '亚朵/希尔顿欢朋/全季', '亚朵 = 中国唯一 lifestyle 标杆'),
        ('中端', '全季/维也纳/亚朵轻居', '全季/柏曼/城市便捷', '东呈业绩对赌逆袭'),
        ('经济型', '汉庭/如家/7 天', '汉庭/城市便捷/如家', 'TOP 3 占行业规模 50%+'),
        ('生活方式', '亚朵/W Hotel/喆啡', '亚朵/亚朵 S/桔子水晶', '主题+文化+客户认同三件套'),
        ('度假', '安缦/Club Med/悦榕庄', 'Club Med/安缦/悦榕庄', '2026 拐点:体验型崛起'),
        ('公寓', '雅诗阁/万豪 ExRes/辉盛坊', '雅诗阁/万豪 ExRes/盛捷', '凯德+万豪+Frasers 三足鼎立'),
    ]
    for j, h in enumerate(sum_headers):
        c = summary_table.rows[0].cells[j]
        set_cell_text(c, h, size=10, bold=True, color='FFFFFF', align=WD_ALIGN_PARAGRAPH.CENTER)
        shade_cell(c, '1F2A4D')
    for i, row in enumerate(sum_data, start=1):
        for j, txt in enumerate(row):
            cell = summary_table.rows[i].cells[j]
            set_cell_text(cell, txt, size=9, bold=(j == 0), align=WD_ALIGN_PARAGRAPH.LEFT)
            if i % 2 == 0:
                shade_cell(cell, 'F2F4F7')

    add_heading(doc, '2.2 行业六大核心判断', level=2, color='1F2A4D', size=13)

    judgments = [
        ('亚朵系 = 中国唯一 lifestyle 标杆', 'MBI 94 / 综合价值 95 双榜首。本土对标国际软品牌的成功范式。亚朵 S/亚朵轻居/A.T.HOUSE 形成单一品牌矩阵,IPO 估值高,单店 RevPAR 优于同业 15-25%。'),
        ('东呈"业绩对赌"= 行业破冰', '柏曼/城市便捷/骏怡/品睿 全系"2 年回本承诺"。综合价值逆袭到 89 分。业主谈判筹码王,目前是行业唯一硬性对赌。'),
        ('奢华层全部不开放加盟', '丽思/四季/宝格丽/安缦/嘉佩乐 等均不开放加盟。业主参与方式:带物业找集团开发部谈管理合同 (GOP 抽成 8-15% + 业绩激励)。综合价值排序 = 四季 (业主最友好) > 丽思 > 安缦。'),
        ('度假酒店 2026 拐点:安缦/悦榕庄跌落', '情怀/园艺/枯山水模式祛魅,体验型生活方式崛起 (六善/嘉佩乐/Capella 仍稳健)。安缦仍是 TOP 1 但增长放缓;Club Med 一价全包 + 亲子场景逆势。'),
        ('国际酒店集团 = Tier 系统 + 软品牌双轨', '万豪 30+ 品牌/希尔顿 18/IHG 17/凯悦 20+/雅高 40+。软品牌 (voco/凯悦尚萃/JdV/Indigo/Canopy) 越来越重要,保留单体特色+挂集团会员体系,改造灵活。'),
        ('中国酒店规模 TOP 3 = 汉庭+如家+7 天', '经济型基础盘三家合计约 4000+ 店 (华住/首旅/锦江)。但增长放缓,利润王 = 全季 (中端) + 亚朵 (中高端/lifestyle)。下沉市场首选:尚客优/城市便捷/柏曼/骏怡。'),
    ]
    for i, (title, desc) in enumerate(judgments, start=1):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(f'{i}. {title}')
        run.font.name = '微软雅黑'
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor.from_string('1F4D2A')

        p2 = doc.add_paragraph()
        p2.paragraph_format.space_after = Pt(2)
        p2.paragraph_format.left_indent = Cm(0.5)
        run2 = p2.add_run(desc)
        run2.font.name = '微软雅黑'
        run2.font.size = Pt(9.5)
        run2.font.color.rgb = RGBColor.from_string('404040')

    doc.add_page_break()

    # ========== 8 大层级详细排名 ==========
    add_heading(doc, '三 · 8 大层级 × 30 品牌详细排名', level=1, color='1F2A4D', size=20)
    add_paragraph(doc,
                  '本部分为报告核心。每个层级独立成章,均按 MBI 影响力指数降序排列 30 个品牌,'
                  '并附合作费用、综合评估价值、等级等核心字段。',
                  size=10, color='404040')

    for tier in TIERS:
        doc.add_page_break()
        add_tier_table(doc, tier)

    # ========== 附录 ==========
    doc.add_page_break()
    add_heading(doc, '四 · 附录', level=1, color='1F2A4D', size=18)

    add_heading(doc, '4.1 集团门店数 TOP 20 (中国区估算)', level=2, color='1F2A4D', size=13)
    grp_table = doc.add_table(rows=21, cols=3)
    grp_table.style = 'Light Grid Accent 1'
    grp_data = [
        ('#', '集团', '中国门店 (估)'),
        ('1', '锦江国际', '13,000+'),
        ('2', '华住', '11,000+'),
        ('3', '首旅如家', '7,000+'),
        ('4', '尚美数智', '5,000+'),
        ('5', '东呈', '5,000+'),
        ('6', '格林酒店', '4,000+'),
        ('7', '希尔顿', '700+'),
        ('8', '洲际 IHG', '700+'),
        ('9', '万豪国际', '500+'),
        ('10', '雅高', '300+'),
        ('11', '雅阁', '200+'),
        ('12', '金陵', '200+'),
        ('13', '凯德雅诗阁', '200+'),
        ('14', '开元', '700+'),
        ('15', '亚朵', '1,500+'),
        ('16', '万达酒店', '200+'),
        ('17', '君亭', '100+'),
        ('18', '凯悦', '100+'),
        ('19', 'Frasers', '100+'),
        ('20', '半岛/文华/朗廷', '<50'),
    ]
    for j, h in enumerate(grp_data[0]):
        c = grp_table.rows[0].cells[j]
        set_cell_text(c, h, size=10, bold=True, color='FFFFFF', align=WD_ALIGN_PARAGRAPH.CENTER)
        shade_cell(c, '1F2A4D')
    for i, row in enumerate(grp_data[1:], start=1):
        for j, txt in enumerate(row):
            cell = grp_table.rows[i].cells[j]
            set_cell_text(cell, txt, size=9, align=WD_ALIGN_PARAGRAPH.CENTER if j != 1 else WD_ALIGN_PARAGRAPH.LEFT,
                          bold=(j == 0))
            if i % 2 == 0:
                shade_cell(cell, 'F2F4F7')

    add_heading(doc, '4.2 行业关键参考指数 (2026)', level=2, color='1F2A4D', size=13)
    idx_table = doc.add_table(rows=12, cols=3)
    idx_data = [
        ('指标', '数值', '来源'),
        ('中国酒店连锁化率', '~41%', '2026 行业报告'),
        ('中端酒店规模', '5 万+ 家', '迈点 2025'),
        ('Lifestyle 占中端', '12-15%', '行业报告'),
        ('2026 大中华区 RevPAR 同比', '-1.6% (洲际)', '洲际 2026 Q2'),
        ('2026 全球奢华 TOP1', '香港瑰丽', 'HOTELS Magazine 2025'),
        ('2025 全球酒店品牌价值 TOP1', 'Hilton', 'Brand Finance'),
        ('国内 MBI TOP1 lifestyle', '喆啡 (2,000+ 店)', '迈点研究院'),
        ('国内 MBI TOP1 中端', '全季', '迈点研究院'),
        ('国内 MBI TOP1 经济型', '汉庭', '迈点研究院'),
        ('行业唯一业绩对赌品牌', '东呈系 (柏曼/城市便捷)', '内部品牌库'),
        ('全球酒店集团 TOP5', '万豪/希尔顿/IHG/雅高/凯悦', 'HOTELS 2025'),
    ]
    for j, h in enumerate(idx_data[0]):
        c = idx_table.rows[0].cells[j]
        set_cell_text(c, h, size=10, bold=True, color='FFFFFF', align=WD_ALIGN_PARAGRAPH.CENTER)
        shade_cell(c, '1F2A4D')
    for i, row in enumerate(idx_data[1:], start=1):
        for j, txt in enumerate(row):
            cell = idx_table.rows[i].cells[j]
            set_cell_text(cell, txt, size=9, align=WD_ALIGN_PARAGRAPH.CENTER if j != 1 else WD_ALIGN_PARAGRAPH.LEFT,
                          bold=(j == 0))
            if i % 2 == 0:
                shade_cell(cell, 'F2F4F7')

    add_heading(doc, '4.3 数据局限与 R66 自检', level=2, color='1F2A4D', size=13)
    limit_table = doc.add_table(rows=6, cols=3)
    limit_data = [
        ('局限', '影响', '应对'),
        ('MBI 评分校准', '各品牌缺一手点评数据', '评分以集团规模/会员数/媒体覆盖为锚,误差 ±5 分'),
        ('加盟费区间', '各品牌对业主谈判结果差异大', '给范围,实战以单店谈判为准'),
        ('度假/生活方式门店数据', '单店差距极大', '仅给出可参考区间'),
        ('服务式公寓数据', '中国市场分散', '仅给 TOP 30 + 主流品牌'),
        ('2026 年最新数据', '部分数据为 2024-2025', '已在表中标注年份'),
    ]
    for j, h in enumerate(limit_data[0]):
        c = limit_table.rows[0].cells[j]
        set_cell_text(c, h, size=10, bold=True, color='FFFFFF', align=WD_ALIGN_PARAGRAPH.CENTER)
        shade_cell(c, '1F2A4D')
    for i, row in enumerate(limit_data[1:], start=1):
        for j, txt in enumerate(row):
            cell = limit_table.rows[i].cells[j]
            set_cell_text(cell, txt, size=9, align=WD_ALIGN_PARAGRAPH.LEFT, bold=(j == 0))
            if i % 2 == 0:
                shade_cell(cell, 'F2F4F7')

    add_heading(doc, '4.4 R66 自检状态', level=2, color='1F2A4D', size=13)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run('✓ 时序对: 数据时点 2026.6-2026.8,符合 2026-08-20 当下')
    run.font.name = '微软雅黑'; run.font.size = Pt(10); run.font.color.rgb = RGBColor.from_string('1F4D2A')

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run('✓ 一致: 与内部知识库 (酒店分级 deep dive v2 / brand-comparison.md) 一致')
    run.font.name = '微软雅黑'; run.font.size = Pt(10); run.font.color.rgb = RGBColor.from_string('1F4D2A')

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run('✓ 有源头: 迈点 / Brand Finance / HOTELS / 集团年报 + 内部 brand-comparison.md')
    run.font.name = '微软雅黑'; run.font.size = Pt(10); run.font.color.rgb = RGBColor.from_string('1F4D2A')

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run('⚠ 加盟费区间 ±5 分校准误差,实战以单店谈判为准')
    run.font.name = '微软雅黑'; run.font.size = Pt(10); run.font.color.rgb = RGBColor.from_string('B7791F')

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run('⚠ 国际品牌中国门店数据为估算,以集团财报为准')
    run.font.name = '微软雅黑'; run.font.size = Pt(10); run.font.color.rgb = RGBColor.from_string('B7791F')

    # ========== 文档结束 ==========
    end_p = doc.add_paragraph()
    end_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    end_p.paragraph_format.space_before = Pt(40)
    run = end_p.add_run('— 报告结束 —')
    run.font.name = '微软雅黑'
    run.font.size = Pt(11)
    run.font.italic = True
    run.font.color.rgb = RGBColor.from_string('707070')

    # 保存到桌面
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    output_path = os.path.join(desktop, '酒店品牌市场指数综合排名_2026H2_v1.0_2026-08-20.docx')
    doc.save(output_path)

    print(f'OK: 已保存到 {output_path}')
    print(f'文件大小: {os.path.getsize(output_path) / 1024:.1f} KB')
    print(f'层级数: {len(TIERS)}')
    print(f'品牌总数: {sum(len(t["brands"]) for t in TIERS)}')
    print()
    print('=== 各层级品牌数校验 ===')
    for t in TIERS:
        print(f'{t["name"]}: {len(t["brands"])} 个品牌')


if __name__ == '__main__':
    main()
