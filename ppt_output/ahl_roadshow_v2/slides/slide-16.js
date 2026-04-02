// slide-16.js - 融资计划
const pptxgen = require("pptxgenjs");
const slideConfig = { type: 'content', index: 16, title: '融资计划' };

function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: theme.accent } });

  slide.addText("融资计划", {
    x: 0.4, y: 0.3, w: 9, h: 0.7,
    fontSize: 30, fontFace: "Microsoft YaHei",
    color: theme.primary, bold: true
  });
  slide.addText("截止日期：2026年4月30日", {
    x: 0.4, y: 0.95, w: 9, h: 0.4,
    fontSize: 13, fontFace: "Microsoft YaHei",
    color: theme.orange
  });

  // 左：大数字
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.4, y: 1.5, w: 3.8, h: 3.8,
    fill: { color: theme.dark }, rectRadius: 0.1
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 1.5, w: 3.8, h: 0.08,
    fill: { color: theme.gold }
  });
  slide.addText("种子轮", {
    x: 0.5, y: 1.7, w: 3.6, h: 0.45,
    fontSize: 16, fontFace: "Microsoft YaHei",
    color: theme.gold, bold: true, align: "center"
  });
  slide.addText("500-800万", {
    x: 0.5, y: 2.2, w: 3.6, h: 1.0,
    fontSize: 36, fontFace: "Arial",
    color: theme.primary, bold: true, align: "center"
  });
  slide.addText("人民币", {
    x: 0.5, y: 3.15, w: 3.6, h: 0.4,
    fontSize: 14, fontFace: "Microsoft YaHei",
    color: theme.secondary, align: "center"
  });
  slide.addShape(pres.shapes.LINE, {
    x: 0.8, y: 3.6, w: 3.0, h: 0,
    line: { color: theme.gold, width: 1 }
  });
  slide.addText("出让股份：10-15%", {
    x: 0.5, y: 3.75, w: 3.6, h: 0.4,
    fontSize: 13, fontFace: "Microsoft YaHei",
    color: theme.secondary, align: "center"
  });
  slide.addText("估值：4000-6000万", {
    x: 0.5, y: 4.15, w: 3.6, h: 0.4,
    fontSize: 13, fontFace: "Microsoft YaHei",
    color: theme.secondary, align: "center"
  });
  slide.addText("截止：2026年4月30日", {
    x: 0.5, y: 4.6, w: 3.6, h: 0.5,
    fontSize: 15, fontFace: "Microsoft YaHei",
    color: theme.orange, bold: true, align: "center"
  });

  // 右：资金用途
  slide.addText("资金用途", {
    x: 4.5, y: 1.55, w: 5.2, h: 0.45,
    fontSize: 18, fontFace: "Microsoft YaHei",
    color: theme.primary, bold: true
  });

  const usages = [
    { item: "MVP开发", pct: "40%", amount: "200-320万", desc: "核心AGENT+SKILL开发", color: theme.accent },
    { item: "市场推广", pct: "30%", amount: "150-240万", desc: "种子用户+品牌建设", color: theme.light },
    { item: "团队扩张", pct: "20%", amount: "100-160万", desc: "技术+运营核心岗位", color: theme.gold },
    { item: "运营储备", pct: "10%", amount: "50-80万", desc: "日常行政+合规", color: theme.secondary },
  ];

  const barStartX = 4.5;
  const barW = 5.0;
  const barH = 0.72;
  const gap = 0.15;

  usages.forEach((u, i) => {
    const y = 2.1 + i * (barH + gap);
    // 标签
    slide.addText(u.item, {
      x: barStartX, y: y, w: 1.3, h: barH,
      fontSize: 12, fontFace: "Microsoft YaHei",
      color: theme.primary, bold: true, valign: "middle"
    });
    // 百分比
    slide.addText(u.pct, {
      x: barStartX + 1.35, y: y, w: 0.7, h: barH,
      fontSize: 18, fontFace: "Arial",
      color: u.color, bold: true, valign: "middle"
    });
    // 进度条背景
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: barStartX + 2.1, y: y + 0.22, w: barW - 2.2, h: 0.28,
      fill: { color: theme.dark }, rectRadius: 0.1
    });
    // 进度条填充
    const fillW = (barW - 2.2) * (parseFloat(u.pct) / 100);
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: barStartX + 2.1, y: y + 0.22, w: fillW, h: 0.28,
      fill: { color: u.color }, rectRadius: 0.1
    });
    // 金额+描述
    slide.addText(u.amount, {
      x: barStartX + 3.5, y: y, w: 1.3, h: barH,
      fontSize: 11, fontFace: "Arial",
      color: u.color, bold: true, valign: "middle"
    });
    slide.addText(u.desc, {
      x: barStartX + 4.3, y: y, w: 1.3, h: barH,
      fontSize: 10, fontFace: "Microsoft YaHei",
      color: theme.secondary, valign: "middle"
    });
  });

  // ROI
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 4.5, y: 5.0, w: 5.1, h: 0.6,
    fill: { color: theme.gold, transparency: 85 },
    line: { color: theme.gold, width: 1.5 },
    rectRadius: 0.08
  });
  slide.addText("单酒店ROI超过35倍 · 年增收350万 / 投入10万", {
    x: 4.5, y: 5.0, w: 5.1, h: 0.6,
    fontSize: 13, fontFace: "Microsoft YaHei",
    color: theme.gold, bold: true, align: "center", valign: "middle"
  });

  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fill: { color: theme.accent } });
  slide.addText("16", { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fontSize: 11, fontFace: "Arial", color: "FFFFFF", bold: true, align: "center", valign: "middle" });

  return slide;
}

module.exports = { createSlide, slideConfig };
