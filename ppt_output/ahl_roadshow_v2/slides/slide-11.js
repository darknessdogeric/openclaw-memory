// slide-11.js - 市场规模与机会
const pptxgen = require("pptxgenjs");
const slideConfig = { type: 'content', index: 11, title: '市场规模与机会' };

function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: theme.accent } });

  slide.addText("市场规模与机会", {
    x: 0.4, y: 0.3, w: 9, h: 0.7,
    fontSize: 30, fontFace: "Microsoft YaHei",
    color: theme.primary, bold: true
  });
  slide.addText("存量市场 + AI赋能 = 千亿级蓝海", {
    x: 0.4, y: 0.95, w: 9, h: 0.4,
    fontSize: 13, fontFace: "Microsoft YaHei",
    color: theme.gold
  });

  const stats = [
    { num: "1.2万亿", label: "中国酒店市场规模", color: theme.accent },
    { num: "2300万间", label: "存量客房", color: theme.light },
    { num: "10万+", label: "单体酒店", color: theme.gold },
    { num: "47%", label: "OTA获客成本3年涨幅", color: theme.orange },
  ];

  const cardW = 2.1;
  const cardH = 2.3;
  const gap = 0.3;
  const startX = 0.4;

  stats.forEach((s, i) => {
    const x = startX + i * (cardW + gap);
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: x, y: 1.55, w: cardW, h: cardH,
      fill: { color: theme.dark }, rectRadius: 0.1
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: x, y: 1.55, w: cardW, h: 0.08,
      fill: { color: s.color }
    });
    slide.addText(s.num, {
      x: x + 0.1, y: 1.75, w: cardW - 0.2, h: 1.1,
      fontSize: 28, fontFace: "Arial",
      color: s.color, bold: true, align: "center", valign: "middle"
    });
    slide.addText(s.label, {
      x: x + 0.1, y: 2.9, w: cardW - 0.2, h: 0.8,
      fontSize: 12, fontFace: "Microsoft YaHei",
      color: theme.secondary, align: "center"
    });
  });

  // 底部洞察
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.4, y: 4.1, w: 9.2, h: 1.1,
    fill: { color: theme.dark }, rectRadius: 0.1
  });

  const insights = [
    { label: "目标市场", value: "10万+单体酒店" },
    { label: "年均IT预算", value: "3-10万/家" },
    { label: "潜在市场规模", value: "30-100亿/年" },
  ];

  const iw = 2.9;
  const iy = 4.2;
  insights.forEach((ins, i) => {
    const ix = 0.55 + i * (iw + 0.2);
    slide.addText(ins.label, {
      x: ix, y: iy, w: iw, h: 0.35,
      fontSize: 11, fontFace: "Microsoft YaHei",
      color: theme.secondary, align: "center"
    });
    slide.addText(ins.value, {
      x: ix, y: iy + 0.35, w: iw, h: 0.5,
      fontSize: 18, fontFace: "Microsoft YaHei",
      color: theme.accent, bold: true, align: "center"
    });
  });

  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fill: { color: theme.accent } });
  slide.addText("11", { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fontSize: 11, fontFace: "Arial", color: "FFFFFF", bold: true, align: "center", valign: "middle" });

  return slide;
}

module.exports = { createSlide, slideConfig };
