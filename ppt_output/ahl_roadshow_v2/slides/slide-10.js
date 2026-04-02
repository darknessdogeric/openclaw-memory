// slide-10.js - B端能力：AI运营官
const pptxgen = require("pptxgenjs");
const slideConfig = { type: 'content', index: 10, title: 'B端能力：AI运营官' };

function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: theme.accent } });

  slide.addText("B端能力：AI运营官", {
    x: 0.4, y: 0.3, w: 9, h: 0.7,
    fontSize: 30, fontFace: "Microsoft YaHei",
    color: theme.primary, bold: true
  });
  slide.addText("四大智能销售模块 × 25个可插拔SKILL · 从获客到复购全链路覆盖", {
    x: 0.4, y: 0.95, w: 9, h: 0.4,
    fontSize: 13, fontFace: "Microsoft YaHei",
    color: theme.secondary
  });

  const modules = [
    {
      icon: "🎯", title: "智能获客雷达", metrics: "30秒 vs 3-5天",
      desc: "地理围栏+AI挖掘\n3-5km内高价值客户自动识别",
      color: theme.accent
    },
    {
      icon: "🤝", title: "协议全生命周期", metrics: "续签率+20%",
      desc: "签-管-续签全流程\n沉睡唤醒自动化",
      color: theme.light
    },
    {
      icon: "📋", title: "RFP智能应答", metrics: "7天→1天",
      desc: "一键生成标书\n竞品对标+差异化策略",
      color: theme.gold
    },
    {
      icon: "📈", title: "动态收益管理", metrics: "RevPAR+15%",
      desc: "AI实时动态定价\n需求预测+库存优化",
      color: theme.orange
    },
  ];

  const cardW = 2.1;
  const cardH = 3.5;
  const gap = 0.3;
  const startX = 0.4;

  modules.forEach((m, i) => {
    const x = startX + i * (cardW + gap);
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: x, y: 1.5, w: cardW, h: cardH,
      fill: { color: theme.dark }, rectRadius: 0.1
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: x, y: 1.5, w: cardW, h: 0.08,
      fill: { color: m.color }
    });
    slide.addText(m.icon, {
      x: x, y: 1.7, w: cardW, h: 0.65,
      fontSize: 36, align: "center", valign: "middle"
    });
    slide.addText(m.title, {
      x: x + 0.1, y: 2.4, w: cardW - 0.2, h: 0.5,
      fontSize: 15, fontFace: "Microsoft YaHei",
      color: theme.primary, bold: true, align: "center"
    });
    // 指标
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: x + 0.15, y: 2.95, w: cardW - 0.3, h: 0.42,
      fill: { color: m.color, transparency: 20 },
      rectRadius: 0.06
    });
    slide.addText(m.metrics, {
      x: x + 0.15, y: 2.95, w: cardW - 0.3, h: 0.42,
      fontSize: 13, fontFace: "Arial",
      color: m.color, bold: true, align: "center", valign: "middle"
    });
    slide.addText(m.desc, {
      x: x + 0.15, y: 3.5, w: cardW - 0.3, h: 1.3,
      fontSize: 11, fontFace: "Microsoft YaHei",
      color: theme.secondary, align: "center"
    });
  });

  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fill: { color: theme.accent } });
  slide.addText("10", { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fontSize: 11, fontFace: "Arial", color: "FFFFFF", bold: true, align: "center", valign: "middle" });

  return slide;
}

module.exports = { createSlide, slideConfig };
