// slide-17.js - 结语 + 联系方式
const pptxgen = require("pptxgenjs");
const slideConfig = { type: 'closing', index: 17, title: '开启酒店业的智能新纪元' };

function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  // 顶部金色装饰条
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.08, fill: { color: theme.gold } });
  // 底部金色装饰条
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 7.5-0.08, w: 10, h: 0.08, fill: { color: theme.gold } });

  // 左侧装饰块
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 2.5, w: 0.12, h: 2.5, fill: { color: theme.gold } });

  // 主标题
  slide.addText("开启酒店业的智能新纪元", {
    x: 0.5, y: 2.0, w: 9, h: 1.2,
    fontSize: 48, fontFace: "Microsoft YaHei",
    color: theme.primary, bold: true, align: "center"
  });

  // 副标题/核心理念
  slide.addText("让AI成为酒店最好的员工", {
    x: 0.5, y: 3.2, w: 9, h: 0.6,
    fontSize: 22, fontFace: "Microsoft YaHei",
    color: theme.accent, align: "center"
  });

  // 分隔线
  slide.addShape(pres.shapes.LINE, {
    x: 3.5, y: 3.95, w: 3, h: 0,
    line: { color: theme.gold, width: 2 }
  });

  // 联系方式
  slide.addText("合作联系", {
    x: 0.5, y: 4.2, w: 9, h: 0.45,
    fontSize: 14, fontFace: "Microsoft YaHei",
    color: theme.secondary, align: "center"
  });

  const contacts = [
    { label: "邮箱", value: "ericzhangshi@163.com" },
    { label: "电话", value: "17760348653" },
    { label: "微信", value: "17760348653（同号）" },
  ];

  const cw = 3.0;
  const cy = 4.7;
  contacts.forEach((c, i) => {
    const cx = 0.5 + i * cw;
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: cx, y: cy, w: cw - 0.2, h: 0.55,
      fill: { color: theme.dark }, rectRadius: 0.08
    });
    slide.addText(c.label + "：" + c.value, {
      x: cx, y: cy, w: cw - 0.2, h: 0.55,
      fontSize: 12, fontFace: "Microsoft YaHei",
      color: theme.primary, align: "center", valign: "middle"
    });
  });

  // 右下角 AHL标签
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 8.0, y: 6.7, w: 1.7, h: 0.5,
    fill: { color: theme.gold, transparency: 20 },
    rectRadius: 0.1
  });
  slide.addText("AHL · AI Hotel Language", {
    x: 8.0, y: 6.7, w: 1.7, h: 0.5,
    fontSize: 9, fontFace: "Arial",
    color: theme.gold, align: "center", valign: "middle"
  });

  // 感谢语
  slide.addText("感谢关注", {
    x: 0.4, y: 5.5, w: 2, h: 0.5,
    fontSize: 28, fontFace: "Microsoft YaHei",
    color: theme.dark
  });

  return slide;
}

module.exports = { createSlide, slideConfig };
