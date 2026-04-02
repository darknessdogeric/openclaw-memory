// slide-12.js - 商业模式
const pptxgen = require("pptxgenjs");
const slideConfig = { type: 'content', index: 12, title: '商业模式' };

function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: theme.accent } });

  slide.addText("商业模式", {
    x: 0.4, y: 0.3, w: 9, h: 0.7,
    fontSize: 30, fontFace: "Microsoft YaHei",
    color: theme.primary, bold: true
  });
  slide.addText("SaaS订阅 + 交易佣金 + 增值服务三驾马车", {
    x: 0.4, y: 0.95, w: 9, h: 0.4,
    fontSize: 13, fontFace: "Microsoft YaHei",
    color: theme.secondary
  });

  const revenues = [
    {
      title: "SaaS订阅费",
      price: "3.98-9.98万/年",
      desc: "基础版3.98万/年（获客雷达+营销引擎）\n旗舰版9.98万/年（全模块）",
      color: theme.accent
    },
    {
      title: "交易佣金",
      price: "5%",
      desc: "协议客户订单\nOTA订单通道\n每次交易自动结算",
      color: theme.light
    },
    {
      title: "增值服务",
      price: "按模块",
      desc: "智能获客专项\nRFP应答包年\n营销自动化套餐\n定制化AI训练",
      color: theme.gold
    },
  ];

  const cardW = 2.9;
  const cardH = 3.3;
  const gap = 0.3;
  const startX = 0.4;

  revenues.forEach((r, i) => {
    const x = startX + i * (cardW + gap);
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: x, y: 1.5, w: cardW, h: cardH,
      fill: { color: theme.dark }, rectRadius: 0.1
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: x, y: 1.5, w: cardW, h: 0.08,
      fill: { color: r.color }
    });
    slide.addText(r.title, {
      x: x + 0.15, y: 1.7, w: cardW - 0.3, h: 0.5,
      fontSize: 18, fontFace: "Microsoft YaHei",
      color: theme.primary, bold: true, align: "center"
    });
    slide.addText(r.price, {
      x: x + 0.1, y: 2.25, w: cardW - 0.2, h: 0.7,
      fontSize: 22, fontFace: "Arial",
      color: r.color, bold: true, align: "center"
    });
    slide.addShape(pres.shapes.LINE, {
      x: x + 0.4, y: 3.05, w: cardW - 0.8, h: 0,
      line: { color: r.color, width: 1 }
    });
    slide.addText(r.desc, {
      x: x + 0.15, y: 3.15, w: cardW - 0.3, h: 1.5,
      fontSize: 11, fontFace: "Microsoft YaHei",
      color: theme.secondary, align: "center"
    });
  });

  // 目标
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.4, y: 5.0, w: 9.2, h: 0.65,
    fill: { color: theme.gold, transparency: 20 },
    rectRadius: 0.08
  });
  slide.addText("目标：首年签约1000家酒店 → 年GMV超5亿+", {
    x: 0.5, y: 5.0, w: 9, h: 0.65,
    fontSize: 16, fontFace: "Microsoft YaHei",
    color: theme.gold, bold: true, align: "center", valign: "middle"
  });

  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fill: { color: theme.accent } });
  slide.addText("12", { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fontSize: 11, fontFace: "Arial", color: "FFFFFF", bold: true, align: "center", valign: "middle" });

  return slide;
}

module.exports = { createSlide, slideConfig };
