// slide-02.js - 目录
const pptxgen = require("pptxgenjs");
const slideConfig = { type: 'toc', index: 2, title: '目录' };

function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  // 标题
  slide.addText("目录", {
    x: 0.5, y: 0.4, w: 9, h: 0.8,
    fontSize: 36, fontFace: "Microsoft YaHei",
    color: theme.primary, bold: true
  });

  // 页面装饰线
  slide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.1, w: 1.2, h: 0.05, fill: { color: theme.accent } });

  const sections = [
    { num: "01", title: "市场痛点", sub: "酒店业的四低困境" },
    { num: "02", title: "解决方案", sub: "AHL一站式AI平台" },
    { num: "03", title: "产品架构", sub: "协议层+双AGENT+SKILL" },
    { num: "04", title: "C端体验", sub: "AI管家全场景服务" },
    { num: "05", title: "B端能力", sub: "AI运营官四大模块" },
    { num: "06", title: "市场与竞争", sub: "千亿蓝海差异化破局" },
    { num: "07", title: "商业与融资", sub: "SaaS+佣金+增值" },
  ];

  const startY = 1.5;
  const rowH = 0.78;

  sections.forEach((s, i) => {
    const y = startY + i * rowH;
    // 序号
    slide.addText(s.num, {
      x: 0.5, y: y, w: 0.7, h: 0.55,
      fontSize: 28, fontFace: "Arial",
      color: theme.accent, bold: true, valign: "middle"
    });
    // 竖线分隔
    slide.addShape(pres.shapes.RECTANGLE, { x: 1.3, y: y + 0.1, w: 0.03, h: 0.35, fill: { color: theme.light } });
    // 标题
    slide.addText(s.title, {
      x: 1.5, y: y, w: 3, h: 0.55,
      fontSize: 22, fontFace: "Microsoft YaHei",
      color: theme.primary, bold: true, valign: "middle"
    });
    // 副标题
    slide.addText(s.sub, {
      x: 4.5, y: y, w: 5, h: 0.55,
      fontSize: 14, fontFace: "Microsoft YaHei",
      color: theme.secondary, valign: "middle"
    });
  });

  // 右下角页码
  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fill: { color: theme.accent } });
  slide.addText("2", { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fontSize: 12, fontFace: "Arial", color: "FFFFFF", bold: true, align: "center", valign: "middle" });

  return slide;
}

module.exports = { createSlide, slideConfig };
