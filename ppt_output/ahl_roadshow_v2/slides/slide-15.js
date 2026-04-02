// slide-15.js - 核心团队
const pptxgen = require("pptxgenjs");
const slideConfig = { type: 'content', index: 15, title: '核心团队' };

function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: theme.accent } });

  slide.addText("核心团队", {
    x: 0.4, y: 0.3, w: 9, h: 0.7,
    fontSize: 30, fontFace: "Microsoft YaHei",
    color: theme.primary, bold: true
  });
  slide.addText("行业老兵 + AI专家 + 连续创业者", {
    x: 0.4, y: 0.95, w: 9, h: 0.4,
    fontSize: 13, fontFace: "Microsoft YaHei",
    color: theme.secondary
  });

  const members = [
    {
      role: "创始人 / CEO",
      name: "张实",
      bg: "24年酒店行业老兵\n前四川远途酒店管理创始人\n重庆丽苑维景国际酒店副总\n襄阳共享维景酒店总经理",
      color: theme.accent
    },
    {
      role: "AI技术负责人",
      name: "[待招募]",
      bg: "大模型 / LLM架构专家\n有SaaS平台从0到1经验\n精通NLP / 推荐系统\n具备数据工程能力",
      color: theme.light
    },
    {
      role: "酒店运营顾问",
      name: "[待邀请]",
      bg: "头部酒店集团前高管\n深度行业资源\n具备连锁集团\n运营管理经验",
      color: theme.gold
    },
    {
      role: "AI助手",
      name: "B166ER",
      bg: "AHL项目的AI大脑\n全天候智能协同\n掌握酒店行业知识库\n持续进化学习",
      color: theme.orange
    },
  ];

  const cardW = 2.1;
  const cardH = 3.6;
  const gap = 0.3;
  const startX = 0.4;

  members.forEach((m, i) => {
    const x = startX + i * (cardW + gap);
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: x, y: 1.5, w: cardW, h: cardH,
      fill: { color: theme.dark }, rectRadius: 0.1
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: x, y: 1.5, w: cardW, h: 0.08,
      fill: { color: m.color }
    });
    // 头像占位圆
    slide.addShape(pres.shapes.OVAL, {
      x: x + (cardW - 0.8) / 2, y: 1.7, w: 0.8, h: 0.8,
      fill: { color: m.color, transparency: 30 }
    });
    slide.addText(m.name[0], {
      x: x + (cardW - 0.8) / 2, y: 1.7, w: 0.8, h: 0.8,
      fontSize: 24, fontFace: "Microsoft YaHei",
      color: m.color, bold: true, align: "center", valign: "middle"
    });
    // 姓名
    slide.addText(m.name, {
      x: x + 0.1, y: 2.58, w: cardW - 0.2, h: 0.45,
      fontSize: 16, fontFace: "Microsoft YaHei",
      color: theme.primary, bold: true, align: "center"
    });
    // 角色
    slide.addText(m.role, {
      x: x + 0.1, y: 3.0, w: cardW - 0.2, h: 0.35,
      fontSize: 11, fontFace: "Microsoft YaHei",
      color: m.color, align: "center"
    });
    // 分隔线
    slide.addShape(pres.shapes.LINE, {
      x: x + 0.3, y: 3.4, w: cardW - 0.6, h: 0,
      line: { color: m.color, width: 0.8 }
    });
    // 背景描述
    slide.addText(m.bg, {
      x: x + 0.12, y: 3.5, w: cardW - 0.24, h: 1.5,
      fontSize: 10, fontFace: "Microsoft YaHei",
      color: theme.secondary, align: "center"
    });
  });

  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fill: { color: theme.accent } });
  slide.addText("15", { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fontSize: 11, fontFace: "Arial", color: "FFFFFF", bold: true, align: "center", valign: "middle" });

  return slide;
}

module.exports = { createSlide, slideConfig };
