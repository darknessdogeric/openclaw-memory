// slide-08.js - 技术架构
const pptxgen = require("pptxgenjs");
const slideConfig = { type: 'content', index: 8, title: '技术架构' };

function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: theme.accent } });

  slide.addText("技术架构", {
    x: 0.4, y: 0.3, w: 9, h: 0.7,
    fontSize: 30, fontFace: "Microsoft YaHei",
    color: theme.primary, bold: true
  });
  slide.addText("大模型 + LangGraph工作流 + 双AGENT编排 + 可插拔SKILL体系", {
    x: 0.4, y: 0.95, w: 9, h: 0.4,
    fontSize: 13, fontFace: "Microsoft YaHei",
    color: theme.secondary
  });

  const layers = [
    { layer: "交互层", items: "Web · APP · 微信 · 飞书 · 短信", color: theme.gold },
    { layer: "协议层", items: "AHL自然语言协议 · 向量匹配引擎 · 隐私计算", color: theme.accent },
    { layer: "AGENT层", items: "C端AI管家 · B端AI运营官 · 协调AGENT", color: theme.light },
    { layer: "SKILL层", items: "80+可插拔场景技能 · 餐饮 · 收益 · 销售 · 运营", color: theme.accent },
    { layer: "数据层", items: "酒店知识库 · 用户画像 · 行为轨迹 · 知识图谱", color: theme.gold },
  ];

  const layerH = 1.0;
  const startY = 1.5;

  layers.forEach((l, i) => {
    const y = startY + i * (layerH + 0.08);
    // 左侧标签条
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 0.4, y: y, w: 1.8, h: layerH,
      fill: { color: l.color, transparency: 20 },
      rectRadius: 0.06
    });
    slide.addText(l.layer, {
      x: 0.4, y: y, w: 1.8, h: layerH,
      fontSize: 14, fontFace: "Microsoft YaHei",
      color: l.color, bold: true, align: "center", valign: "middle"
    });
    // 右侧内容
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 2.3, y: y, w: 7.3, h: layerH,
      fill: { color: theme.dark }, rectRadius: 0.06
    });
    slide.addText(l.items, {
      x: 2.5, y: y, w: 7, h: layerH,
      fontSize: 14, fontFace: "Microsoft YaHei",
      color: theme.primary, valign: "middle"
    });
    // 连接箭头
    if (i < layers.length - 1) {
      slide.addText("▼", {
        x: 1.1, y: y + layerH - 0.05, w: 0.5, h: 0.25,
        fontSize: 10, fontFace: "Arial",
        color: theme.secondary, align: "center"
      });
    }
  });

  slide.addShape(pres.shapes.OVAL, { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fill: { color: theme.accent } });
  slide.addText("8", { x: 9.3, y: 5.1, w: 0.4, h: 0.4, fontSize: 12, fontFace: "Arial", color: "FFFFFF", bold: true, align: "center", valign: "middle" });

  return slide;
}

module.exports = { createSlide, slideConfig };
