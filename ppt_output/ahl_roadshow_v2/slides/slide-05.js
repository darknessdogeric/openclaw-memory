// slide-05.js - 章节页：解决方案
const pptxgen = require("pptxgenjs");
const slideConfig = { type: 'section', index: 5, title: '02 解决方案' };

function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.dark };

  slide.addText("02", {
    x: 0.5, y: 1.5, w: 3, h: 2,
    fontSize: 120, fontFace: "Arial",
    color: theme.accent, bold: true, align: "left", valign: "middle"
  });
  slide.addShape(pres.shapes.RECTANGLE, { x: 3.3, y: 1.8, w: 0.06, h: 2.2, fill: { color: theme.gold } });
  slide.addText("解决方案", {
    x: 3.6, y: 1.9, w: 6, h: 1,
    fontSize: 48, fontFace: "Microsoft YaHei",
    color: theme.primary, bold: true, valign: "middle"
  });
  slide.addText("AHL一站式AI平台——从被动接单到主动狩猎", {
    x: 3.6, y: 2.9, w: 6, h: 0.6,
    fontSize: 18, fontFace: "Microsoft YaHei",
    color: theme.secondary, valign: "middle"
  });

  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fill: { color: theme.accent } });
  slide.addText("5", { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fontSize: 12, fontFace: "Arial", color: "FFFFFF", bold: true, align: "center", valign: "middle" });

  return slide;
}

module.exports = { createSlide, slideConfig };
