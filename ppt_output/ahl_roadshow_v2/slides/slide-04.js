// slide-04.js - 酒店业的四低困境
const pptxgen = require("pptxgenjs");
const slideConfig = { type: 'content', index: 4, title: '酒店业的四低困境' };

function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  // 顶部装饰条
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: theme.accent } });

  // 标题
  slide.addText("酒店业的四低困境", {
    x: 0.4, y: 0.3, w: 9, h: 0.7,
    fontSize: 30, fontFace: "Microsoft YaHei",
    color: theme.primary, bold: true
  });

  // 小标题
  slide.addText("每个困境背后都是一个被忽视的数字化机会", {
    x: 0.4, y: 0.95, w: 9, h: 0.4,
    fontSize: 13, fontFace: "Microsoft YaHei",
    color: theme.secondary
  });

  const items = [
    { icon: "📉", title: "低议价", detail: "OTA佣金20%+\n净利润压缩至5%以下", color: theme.orange },
    { icon: "⏰", title: "低效率", detail: "销售日均拜访<3家\n信息滞后48小时", color: theme.accent },
    { icon: "🔄", title: "低复购", detail: "会员次留率<15%\n沉睡会员占60%", color: theme.light },
    { icon: "🧠", title: "低洞察", detail: "无法预测客户需求\n依赖经验做决策", color: theme.gold },
  ];

  const cardW = 2.1;
  const gap = 0.25;
  const startX = 0.4;

  items.forEach((item, i) => {
    const x = startX + i * (cardW + gap);
    // 卡片背景
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: x, y: 1.6, w: cardW, h: 3.2,
      fill: { color: theme.dark }, rectRadius: 0.12
    });
    // 顶部色条
    slide.addShape(pres.shapes.RECTANGLE, {
      x: x, y: 1.6, w: cardW, h: 0.1,
      fill: { color: item.color }
    });
    // 图标
    slide.addText(item.icon, {
      x: x, y: 1.85, w: cardW, h: 0.7,
      fontSize: 36, align: "center", valign: "middle"
    });
    // 标题
    slide.addText(item.title, {
      x: x + 0.15, y: 2.65, w: cardW - 0.3, h: 0.5,
      fontSize: 22, fontFace: "Microsoft YaHei",
      color: theme.primary, bold: true, align: "center"
    });
    // 分隔线
    slide.addShape(pres.shapes.LINE, {
      x: x + 0.4, y: 3.2, w: cardW - 0.8, h: 0,
      line: { color: item.color, width: 1.5 }
    });
    // 详细描述
    slide.addText(item.detail, {
      x: x + 0.15, y: 3.35, w: cardW - 0.3, h: 1.2,
      fontSize: 12, fontFace: "Microsoft YaHei",
      color: theme.secondary, align: "center", valign: "top"
    });
  });

  // 底部结论
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.4, y: 5.0, w: 9.2, h: 0.65,
    fill: { color: theme.accent, transparency: 15 },
    rectRadius: 0.08
  });
  slide.addText("核心问题：我们连自己的客户都没有完全掌握，何来运营提升？", {
    x: 0.5, y: 5.0, w: 9, h: 0.65,
    fontSize: 14, fontFace: "Microsoft YaHei",
    color: theme.primary, align: "center", valign: "middle"
  });

  // 页码
  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fill: { color: theme.accent } });
  slide.addText("4", { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fontSize: 12, fontFace: "Arial", color: "FFFFFF", bold: true, align: "center", valign: "middle" });

  return slide;
}

module.exports = { createSlide, slideConfig };
