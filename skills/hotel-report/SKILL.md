# Hotel Report Generator Skill

> **Version**: 1.0.0  
> **Author**: B166ER  
> **Created**: 2026-03-18  
> **Status**: Active Development

## Overview

A comprehensive toolkit for generating professional hotel industry reports (monthly, quarterly, annual, and holiday-specific) following industry-standard formats from leading authorities like 迈点研究院 (Meadin), 环球旅讯 (TravelDaily), STR, and major OTAs.

## Features

### Report Types
- **Monthly Reports** (15-25 pages): Operational monitoring and trend tracking
- **Quarterly Reports** (30-50 pages): Performance evaluation and strategy adjustment
- **Annual Reports** (80-150 pages): Strategic review and annual planning
- **Holiday Reports** (20-40 pages): Special analysis and forecast review

### Core Capabilities
- Automated data collection from multiple authoritative sources
- Standardized report structure with 10 core chapters
- Professional data visualization and chart generation
- Multi-format output (Word, PDF, Excel, PowerPoint)
- Quality assurance checklists

## Installation

### Prerequisites
```bash
pip install scrapling python-docx pandas matplotlib openpyxl
```

### Setup
1. Copy this skill to your workspace:
```bash
cp -r skills/hotel-report ~/.openclaw/workspace/skills/
```

2. Configure data sources in `config/data_sources.yaml`

3. Set up API keys (if needed) in environment variables:
```bash
export STR_API_KEY="your_str_api_key"
export CTRIP_API_KEY="your_ctrip_api_key"
```

## Usage

### Quick Start

#### Generate a Monthly Report
```bash
python skills/hotel-report/main.py --type monthly --month 2026-02 --output report.docx
```

#### Generate a Holiday Report
```bash
python skills/hotel-report/main.py --type holiday --holiday "spring_festival" --year 2026 --output spring_festival_report.docx
```

#### Generate a Quarterly Report
```bash
python skills/hotel-report/main.py --type quarterly --quarter Q1-2026 --output q1_report.docx
```

### Python API

```python
from skills.hotel_report import HotelReportGenerator

# Initialize generator
generator = HotelReportGenerator()

# Generate monthly report
report = generator.generate_monthly_report(
    year=2026,
    month=2,
    include_chapters=[
        "executive_summary",
        "operational_performance",
        "regional_analysis",
        "trend_forecast"
    ]
)

# Save to file
report.save("2026-02-hotel-report.docx")
```

## Report Structure

### Standard 10-Chapter Format

```
1. Executive Summary
   - Key Findings (3-5 points)
   - KPI Dashboard
   - Trend Assessment
   - Strategic Recommendations

2. Macro Environment Analysis
   - Economic indicators
   - Policy environment
   - Social trends
   - Technology landscape

3. Industry Supply Analysis
   - Market inventory
   - New supply
   - Segment structure
   - Regional distribution
   - Brand competition

4. Market Demand Analysis
   - Overall demand scale
   - Customer segmentation
   - Booking channels
   - Consumer behavior

5. Operational Performance (Core)
   - OCC/ADR/RevPAR metrics
   - Segment performance
   - Regional performance
   - Efficiency analysis
   - Revenue management

6. Competitive Landscape
   - Group-level competition
   - Brand rankings
   - Regional dynamics
   - International players

7. Consumer Insights
   - Customer profiling
   - Preference analysis
   - Satisfaction metrics
   - Emerging trends

8. Channel & Marketing Analysis
   - OTA performance
   - Direct booking
   - New media marketing
   - ROI analysis

9. Investment & Development
   - Investment heat
   - New projects
   - Asset transactions
   - ROI analysis

10. Trend Forecast & Recommendations
    - Short-term trends (1-3 months)
    - Medium-term trends (3-12 months)
    - Long-term trends (1-3 years)
    - Strategic recommendations
```

## Data Sources

### Tier A (Official/Authoritative)
- **STR Global**: Industry-standard hotel performance data
- **National Bureau of Statistics**: Official economic data
- **Listed Company Reports**: 华住, 锦江, 首旅, 亚朵, 君亭

### Tier B (Industry/Platform)
- **迈点研究院 (Meadin)**: MBI brand index
- **环球旅讯 (TravelDaily)**: Industry news and analysis
- **小牛行研**: Market research data
- **OTA Platforms**: 携程, 美团, 飞猪, 去哪儿

### Tier C (Supplementary)
- Industry associations
- Research institutions
- Media reports

## Configuration

### data_sources.yaml
```yaml
sources:
  str:
    enabled: true
    api_endpoint: ${STR_API_ENDPOINT}
    api_key: ${STR_API_KEY}
    frequency: weekly
    
  meadin:
    enabled: true
    url: https://www.meadin.com/report/
    scraper: scrapling
    frequency: daily
    
  hangyan:
    enabled: true
    url: https://www.hangyan.co
    scraper: scrapling
    frequency: weekly
    
  traveldaily:
    enabled: true
    url: https://hub.traveldaily.cn
    scraper: scrapling
    frequency: daily
    
  ota:
    ctrip:
      enabled: true
      api_key: ${CTRIP_API_KEY}
    meituan:
      enabled: true
      api_key: ${MEITUAN_API_KEY}
    fliggy:
      enabled: true
      api_key: ${FLIGGY_API_KEY}
```

## Templates

Available templates in `templates/`:

- `monthly_template.md`: Monthly report template
- `quarterly_template.md`: Quarterly report template
- `annual_template.md`: Annual report template
- `holiday_template.md`: Holiday-specific report template

## Quality Checklist

### Content Completeness
- [ ] Cover page complete (title, date, version, organization)
- [ ] Executive summary includes key findings, KPIs, trends, recommendations
- [ ] All chapters logically connected, no omissions
- [ ] Data sources clearly cited
- [ ] Appendices complete (glossary, methodology, data tables)

### Data Accuracy
- [ ] All data has clear sources
- [ ] Calculations correct (YoY/MoM/percentage)
- [ ] Units consistent throughout
- [ ] Time periods aligned
- [ ] Cross-validation passed

### Format Standards
- [ ] Fonts and sizes follow specifications
- [ ] Chart numbering continuous
- [ ] Headers and footers correct
- [ ] Table of contents matches content
- [ ] Citations formatted consistently

## Examples

See `examples/` directory for sample reports:
- `monthly_example_2026_02.md`
- `holiday_spring_festival_2026.md`
- `quarterly_q1_2026.md`

## Roadmap

### Phase 1: Foundation (Current)
- [x] Report template system
- [x] Data collection framework
- [x] Basic report generation

### Phase 2: Enhancement (Next 2 weeks)
- [ ] Complete web scrapers for all sources
- [ ] Automated chart generation
- [ ] Multi-format output (PDF, PPT, Excel)

### Phase 3: Intelligence (Next month)
- [ ] AI-powered trend analysis
- [ ] Predictive modeling
- [ ] Automated insights generation

### Phase 4: Platform (Next quarter)
- [ ] Real-time data monitoring
- [ ] Custom report builder
- [ ] API service

## Contributing

To contribute to this skill:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - See LICENSE file for details

## Contact

For questions or support:
- Email: res@meadin.com (reference)
- GitHub Issues: Open an issue in the repository

## Acknowledgments

This skill draws inspiration and best practices from:
- 迈点研究院 (Meadin Research Institute)
- 环球旅讯 (TravelDaily)
- STR Global
- 浩华 (HVS)
- 彭润 (Horwath)
- 石基信息 (Shiji)
- 中国旅游饭店业协会
- 携程, 美团, 飞猪等OTA平台

---

**Note**: This skill is designed for professional hotel industry analysis. Ensure compliance with data source terms of service and copyright requirements when using collected data.
