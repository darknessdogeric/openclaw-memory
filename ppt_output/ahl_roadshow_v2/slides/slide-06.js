// slide-06.js - AHL一站式AI解决方案
const pptxgen = require("pptxgenjs");
const slideConfig = { type: 'content', index: 6, title: 'AHL一站式AI解决方案' };

function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: theme.accent } });

  slide.addText("AHL：一站式AI解决方案", {
    x: 0.4, y: 0.3, w: 9, h: 0.7,
    fontSize: 30, fontFace: "Microsoft YaHei",
    color: theme.primary, bold: true
  });
  slide.addText("三层架构，全面赋能酒店AI转型", {
    x: 0.4, y: 0.95, w: 9, h: 0.4,
    fontSize: 13, fontFace: "Microsoft YaHei",
    color: theme.secondary
  });

  // 三列卡片
  const cols = [
    {
      title: "C端AI管家",
      subtitle: "自然语言交互",
      points: ["7×24小时即时响应", "个性化需求预测", "行程全周期管理", "服务无缝闭环"],
      color: theme.accent
    },
    {
      title: "B端AI运营官",
      subtitle: "智能运营决策",
      points: ["智能获客雷达", "协议全生命周期", "RFP智能应答", "动态收益管理"],
      color: theme.light
    },
    {
      title: "AHL协议层",
      subtitle: "行业基础设施",
      points: ["自然语言协议标准", "隐私保护原生", "开放生态对接", "数据价值流转"],
      color: theme.gold
    }
  ];

  const cardW = 2.9;
  const gap = 0.25;
  const startX = 0.4;

  cols.forEach((col, i) => {
    const x = startX + i * (cardW + gap);
    // 卡片背景
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: x, y: 1.5, w: cardW, h: 4.0,
      fill: { color: theme.dark }, rectRadius: 0.1
    });
    // 顶部色条
    slide.addShape(pres.shapes.RECTANGLE, {
      x: x, y: 1.5, w: cardW, h: 0.08,
      fill: { color: col.color }
    });
    // 标题
    slide.addText(col.title, {
      x: x + 0.2, y: 1.7, w: cardW - 0.4, h: 0.55,
      fontSize: 20, fontFace: "Microsoft YaHei",
      color: theme.primary, bold: true, align: "center"
    });
    // 副标题
    slide.addText(col.subtitle, {
      x: x + 0.2, y: 2.2, w: cardW - 0.4, h: 0.35,
      fontSize: 12, fontFace: "Microsoft YaHei",
      color: col.color, align: "center"
    });
    // 分隔线
    slide.addShape(pres.shapes.LINE, {
      x: x + 0.4, y: 2.65, w: cardW - 0.8, h: 0,
      line: { color: col.color, width: 1 }
    });
    // 要点列表
    col.points.forEach((pt, j) => {
      slide.addText("▸ " + pt, {
        x: x + 0.25, y: 2.8 + j * 0.52, w: cardW - 0.5, h: 0.45,
        fontSize: 13, fontFace: "Microsoft YaHei",
        color: theme.secondary, valign: "middle"
      });
    });
  });

  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fill: { color: theme.accent } });
  slide.addText("6", { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fontSize: 12, fontFace: "Arial", color: "FFFFFF", bold: true, align: "center", valign: "middle" });

  return slide;
}

module.exports = { createSlide, slideConfig };
