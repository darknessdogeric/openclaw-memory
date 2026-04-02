// slide-03.js - 章节页：市场痛点
const pptxgen = require("pptxgenjs");
const slideConfig = { type: 'section', index: 3, title: '01 市场痛点' };

function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.dark };

  // 大号章节号
  slide.addText("01", {
    x: 0.5, y: 1.5, w: 3, h: 2,
    fontSize: 120, fontFace: "Arial",
    color: theme.accent, bold: true, align: "left", valign: "middle"
  });

  // 竖线装饰
  slide.addShape(pres.shapes.RECTANGLE, { x: 3.3, y: 1.8, w: 0.06, h: 2.2, fill: { color: theme.gold } });

  // 章节标题
  slide.addText("市场痛点", {
    x: 3.6, y: 1.9, w: 6, h: 1,
    fontSize: 48, fontFace: "Microsoft YaHei",
    color: theme.primary, bold: true, valign: "middle"
  });

  slide.addText("酒店业正在经历的四大结构性困境", {
    x: 3.6, y: 2.9, w: 6, h: 0.6,
    fontSize: 18, fontFace: "Microsoft YaHei",
    color: theme.secondary, valign: "middle"
  });

  // 右下角页码
  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fill: { color: theme.accent } });
  slide.addText("3", { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fontSize: 12, fontFace: "Arial", color: "FFFFFF", bold: true, align: "center", valign: "middle" });

  return slide;
}

module.exports = { createSlide, slideConfig };
