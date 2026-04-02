// slide-14.js - 发展路线图
const pptxgen = require("pptxgenjs");
const slideConfig = { type: 'content', index: 14, title: '发展路线图' };

function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: theme.accent } });

  slide.addText("发展路线图", {
    x: 0.4, y: 0.3, w: 9, h: 0.7,
    fontSize: 30, fontFace: "Microsoft YaHei",
    color: theme.primary, bold: true
  });
  slide.addText("三阶段战略，36个月完成规模化与生态构建", {
    x: 0.4, y: 0.95, w: 9, h: 0.4,
    fontSize: 13, fontFace: "Microsoft YaHei",
    color: theme.secondary
  });

  const phases = [
    {
      phase: "Phase 1",
      timeline: "0-6个月",
      title: "种子期",
      goal: "MVP开发 + 种子用户验证",
      targets: ["签约50家试点酒店", "核心AGENT上线", "产品PMF验证", "种子轮融资到位"],
      color: theme.accent
    },
    {
      phase: "Phase 2",
      timeline: "6-18个月",
      title: "成长期",
      goal: "产品打磨 + 渠道铺设",
      targets: ["扩展至500家酒店", "SKILL扩至50+", "PMS渠道对接", "月收入破500万"],
      color: theme.light
    },
    {
      phase: "Phase 3",
      timeline: "18-36个月",
      title: "规模化",
      goal: "规模化 + 生态构建",
      targets: ["覆盖2000家酒店", "80+SKILL生态", "AHL协议行业标准", "启动A轮融资"],
      color: theme.gold
    },
  ];

  const cardW = 2.9;
  const cardH = 4.3;
  const gap = 0.3;
  const startX = 0.4;

  phases.forEach((p, i) => {
    const x = startX + i * (cardW + gap);
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: x, y: 1.5, w: cardW, h: cardH,
      fill: { color: theme.dark }, rectRadius: 0.1
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: x, y: 1.5, w: cardW, h: 0.08,
      fill: { color: p.color }
    });
    // Phase标签
    slide.addText(p.phase, {
      x: x + 0.1, y: 1.68, w: 1.2, h: 0.35,
      fontSize: 12, fontFace: "Arial",
      color: p.color, bold: true
    });
    // 时间
    slide.addText(p.timeline, {
      x: x + 1.3, y: 1.68, w: 1.4, h: 0.35,
      fontSize: 11, fontFace: "Arial",
      color: theme.secondary, align: "right"
    });
    // 标题
    slide.addText(p.title, {
      x: x + 0.15, y: 2.08, w: cardW - 0.3, h: 0.45,
      fontSize: 20, fontFace: "Microsoft YaHei",
      color: theme.primary, bold: true, align: "center"
    });
    // 目标
    slide.addText(p.goal, {
      x: x + 0.15, y: 2.55, w: cardW - 0.3, h: 0.4,
      fontSize: 11, fontFace: "Microsoft YaHei",
      color: p.color, align: "center"
    });
    // 分隔线
    slide.addShape(pres.shapes.LINE, {
      x: x + 0.4, y: 3.0, w: cardW - 0.8, h: 0,
      line: { color: p.color, width: 1 }
    });
    // 里程碑列表
    p.targets.forEach((t, j) => {
      slide.addText("◆ " + t, {
        x: x + 0.2, y: 3.1 + j * 0.45, w: cardW - 0.4, h: 0.42,
        fontSize: 11, fontFace: "Microsoft YaHei",
        color: theme.secondary, valign: "middle"
      });
    });

    // 箭头连接
    if (i < phases.length - 1) {
      slide.addText("→", {
        x: x + cardW, y: 3.5, w: gap, h: 0.5,
        fontSize: 20, fontFace: "Arial",
        color: p.color, align: "center", valign: "middle"
      });
    }
  });

  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fill: { color: theme.accent } });
  slide.addText("14", { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fontSize: 11, fontFace: "Arial", color: "FFFFFF", bold: true, align: "center", valign: "middle" });

  return slide;
}

module.exports = { createSlide, slideConfig };
