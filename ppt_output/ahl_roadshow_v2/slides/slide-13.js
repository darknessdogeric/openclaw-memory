// slide-13.js - 竞争格局
const pptxgen = require("pptxgenjs");
const slideConfig = { type: 'content', index: 13, title: '竞争格局' };

function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: theme.accent } });

  slide.addText("竞争格局", {
    x: 0.4, y: 0.3, w: 9, h: 0.7,
    fontSize: 30, fontFace: "Microsoft YaHei",
    color: theme.primary, bold: true
  });
  slide.addText("赋能所有酒店，AI原生，开放生态 — 差异化破局", {
    x: 0.4, y: 0.95, w: 9, h: 0.4,
    fontSize: 13, fontFace: "Microsoft YaHei",
    color: theme.secondary
  });

  // 表头
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.35, y: 1.5, w: 9.3, h: 0.55,
    fill: { color: theme.dark }, rectRadius: 0.06
  });
  ["竞争对手", "代表玩家", "核心痛点", "AHL优势"].forEach((h, i) => {
    const xs = [0.5, 3.0, 5.4, 7.5];
    const ws = [2.3, 2.2, 1.9, 2.0];
    slide.addText(h, {
      x: xs[i], y: 1.5, w: ws[i], h: 0.55,
      fontSize: 13, fontFace: "Microsoft YaHei",
      color: i === 3 ? theme.gold : theme.secondary,
      bold: true, valign: "middle"
    });
  });

  const players = [
    { type: "OTA巨头", names: "携程/美团/飞猪", weakness: "中心化平台\n佣金20%+\n不赋能酒店", advantage: "接入AHL协议\n降低获客成本\n共享AI能力" },
    { type: "酒店集团", names: "华住/锦江/首旅", weakness: "只服务自有品牌\n不对外开放\n技术能力弱", advantage: "赋能单体酒店\n数据互通\n生态共建" },
    { type: "传统SaaS", names: "石基/绿云/别样红", weakness: "功能固定\n无AI能力\n迭代慢", advantage: "AI原生架构\n80+SKILL热插拔\n持续进化" },
  ];

  const rowH = 1.3;
  const startY = 2.15;

  players.forEach((p, i) => {
    const y = startY + i * (rowH + 0.1);
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 0.35, y: y, w: 9.3, h: rowH,
      fill: { color: theme.dark }, rectRadius: 0.06
    });

    const xs = [0.5, 3.0, 5.4, 7.5];
    const ws = [2.3, 2.2, 1.9, 2.0];
    const vals = [p.type, p.names, p.weakness, p.advantage];

    vals.forEach((val, j) => {
      slide.addText(val, {
        x: xs[j], y: y + 0.1, w: ws[j], h: rowH - 0.2,
        fontSize: j === 3 ? 11 : 12,
        fontFace: "Microsoft YaHei",
        color: j === 3 ? theme.gold : (j === 2 ? theme.secondary : theme.primary),
        bold: j !== 2, valign: "middle"
      });
    });
  });

  // AHL highlight
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.35, y: 5.85 - 0.65, w: 9.3, h: 0.55,
    fill: { color: theme.gold, transparency: 80 },
    line: { color: theme.gold, width: 1.5 },
    rectRadius: 0.06
  });
  slide.addText("AHL —— 去中心化协议 + AI原生 + 开放生态 = 行业基础设施", {
    x: 0.5, y: 5.85 - 0.65, w: 9, h: 0.55,
    fontSize: 13, fontFace: "Microsoft YaHei",
    color: theme.gold, bold: true, align: "center", valign: "middle"
  });

  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fill: { color: theme.accent } });
  slide.addText("13", { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fontSize: 11, fontFace: "Arial", color: "FFFFFF", bold: true, align: "center", valign: "middle" });

  return slide;
}

module.exports = { createSlide, slideConfig };
