// slide-07.js - AHL协议：行业基础设施
const pptxgen = require("pptxgenjs");
const slideConfig = { type: 'content', index: 7, title: 'AHL协议：行业基础设施' };

function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: theme.accent } });

  slide.addText("AHL协议：行业基础设施", {
    x: 0.4, y: 0.3, w: 9, h: 0.7,
    fontSize: 30, fontFace: "Microsoft YaHei",
    color: theme.primary, bold: true
  });
  slide.addText("AI Hotel Language —— 用LLM协议重构民宿/酒店交易结构", {
    x: 0.4, y: 0.95, w: 9, h: 0.4,
    fontSize: 13, fontFace: "Microsoft YaHei",
    color: theme.secondary
  });

  // 四大特性卡片 - 2x2网格
  const features = [
    { num: "01", title: "自然语言协议", desc: "酒店用自然语言描述服务\nC端用自然语言表达需求\nAI自动理解并匹配" },
    { num: "02", title: "智能匹配引擎", desc: "需求↔供给精准双向向量匹配\n基于23个维度的特异化数据\n实时动态调整" },
    { num: "03", title: "隐私保护原生", desc: "数据最小化原则\n用户自主控制数据授权\n隐私计算技术支撑" },
    { num: "04", title: "开放生态对接", desc: "任何PMS/CRS可无感接入\nOTA平台协议互联\n构建行业数据标准" },
  ];

  const cardW = 4.4;
  const cardH = 1.9;
  const gapX = 0.3;
  const gapY = 0.25;
  const startX = 0.35;
  const startY = 1.55;

  features.forEach((f, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = startX + col * (cardW + gapX);
    const y = startY + row * (cardH + gapY);

    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: x, y: y, w: cardW, h: cardH,
      fill: { color: theme.dark }, rectRadius: 0.08
    });
    // 序号
    slide.addText(f.num, {
      x: x + 0.15, y: y + 0.15, w: 0.5, h: 0.5,
      fontSize: 22, fontFace: "Arial",
      color: theme.accent, bold: true
    });
    // 标题
    slide.addText(f.title, {
      x: x + 0.65, y: y + 0.18, w: 3.5, h: 0.45,
      fontSize: 18, fontFace: "Microsoft YaHei",
      color: theme.primary, bold: true, valign: "middle"
    });
    // 描述
    slide.addText(f.desc, {
      x: x + 0.2, y: y + 0.7, w: cardW - 0.4, h: 1.1,
      fontSize: 11, fontFace: "Microsoft YaHei",
      color: theme.secondary, valign: "top"
    });
  });

  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fill: { color: theme.accent } });
  slide.addText("7", { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fontSize: 12, fontFace: "Arial", color: "FFFFFF", bold: true, align: "center", valign: "middle" });

  return slide;
}

module.exports = { createSlide, slideConfig };
