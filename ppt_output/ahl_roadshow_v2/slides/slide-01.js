// slide-01.js - 封面
const pptxgen = require("pptxgenjs");
const slideConfig = { type: 'cover', index: 1, title: 'AHL去中心化旅行平台' };

function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  // 顶部装饰渐变条
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.08, fill: { color: theme.accent } });
  // 底部装饰渐变条
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 7.5-0.08, w: 10, h: 0.08, fill: { color: theme.accent } });

  // 左侧装饰块
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 2.5, w: 0.12, h: 2.5, fill: { color: theme.gold } });

  // 主标题
  slide.addText("AHL去中心化旅行平台", {
    x: 0.5, y: 2.3, w: 9, h: 1.2,
    fontSize: 54, fontFace: "Microsoft YaHei",
    color: theme.primary, bold: true, align: "center"
  });

  // 副标题
  slide.addText("AI驱动 × 协议直连 × 智能运营", {
    x: 0.5, y: 3.5, w: 9, h: 0.6,
    fontSize: 24, fontFace: "Microsoft YaHei",
    color: theme.accent, align: "center"
  });

  // 分隔线
  slide.addShape(pres.shapes.LINE, {
    x: 3, y: 4.3, w: 4, h: 0,
    line: { color: theme.light, width: 1.5 }
  });

  // 标语
  slide.addText("让每一家酒店都拥有AI时代的智能运营能力", {
    x: 0.5, y: 4.6, w: 9, h: 0.5,
    fontSize: 18, fontFace: "Microsoft YaHei",
    color: theme.secondary, align: "center"
  });

  // 右下角 - 融资路演标签
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 7.8, y: 6.7, w: 1.9, h: 0.5,
    fill: { color: theme.accent, transparency: 20 },
    rectRadius: 0.1
  });
  slide.addText("种子轮路演", {
    x: 7.8, y: 6.7, w: 1.9, h: 0.5,
    fontSize: 12, fontFace: "Microsoft YaHei",
    color: theme.primary, align: "center", valign: "middle"
  });

  return slide;
}

module.exports = { createSlide, slideConfig };
