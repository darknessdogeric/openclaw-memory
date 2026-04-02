// slide-09.js - C端体验：AI管家
const pptxgen = require("pptxgenjs");
const slideConfig = { type: 'content', index: 9, title: 'C端体验：AI管家' };

function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: theme.accent } });

  slide.addText("C端体验：AI管家", {
    x: 0.4, y: 0.3, w: 9, h: 0.7,
    fontSize: 30, fontFace: "Microsoft YaHei",
    color: theme.primary, bold: true
  });
  slide.addText("自然语言交互 · 个性化推荐 · 行程全周期管理", {
    x: 0.4, y: 0.95, w: 9, h: 0.4,
    fontSize: 13, fontFace: "Microsoft YaHei",
    color: theme.secondary
  });

  const scenarios = [
    {
      scene: "预订场景",
      q: "「下周要去成都，想住宽窄巷子附近，早点入住」",
      a: "已为您推荐3家酒店：成都锦里希尔顿（距宽窄巷800m）、成都院落民宿（景区内）、成都W酒店（距地铁200m）...",
      tag: "🏨 酒店推荐"
    },
    {
      scene: "入住场景",
      q: "「我到了，房间可以提前吗？」",
      a: "已协调前台：您的高级房已提前至14:00准备完毕，欢迎入住！如需行李托运服务，请回复1。",
      tag: "🔑 入住办理"
    },
    {
      scene: "服务场景",
      q: "「明天早起，帮我约个干洗」",
      a: "已为您预约明日8:00-9:00干洗服务，费用约68元，将从房间消费中扣除。是否需要加急服务（额外30元）？",
      tag: "👔 增值服务"
    }
  ];

  const cardH = 1.55;
  const startY = 1.5;
  const gap = 0.15;

  scenarios.forEach((s, i) => {
    const y = startY + i * (cardH + gap);
    // 卡片背景
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 0.35, y: y, w: 9.3, h: cardH,
      fill: { color: theme.dark }, rectRadius: 0.1
    });
    // 场景标签
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 0.5, y: y + 0.12, w: 1.5, h: 0.35,
      fill: { color: theme.accent }, rectRadius: 0.08
    });
    slide.addText(s.scene, {
      x: 0.5, y: y + 0.12, w: 1.5, h: 0.35,
      fontSize: 12, fontFace: "Microsoft YaHei",
      color: theme.primary, bold: true, align: "center", valign: "middle"
    });
    // 用户问
    slide.addText("用户：" + s.q, {
      x: 2.15, y: y + 0.1, w: 7.3, h: 0.5,
      fontSize: 12, fontFace: "Microsoft YaHei",
      color: theme.secondary
    });
    // AI回答
    slide.addText("AI：" + s.a, {
      x: 0.5, y: y + 0.65, w: 9, h: 0.75,
      fontSize: 11, fontFace: "Microsoft YaHei",
      color: theme.primary
    });
  });

  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fill: { color: theme.accent } });
  slide.addText("9", { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fontSize: 12, fontFace: "Arial", color: "FFFFFF", bold: true, align: "center", valign: "middle" });

  return slide;
}

module.exports = { createSlide, slideConfig };
