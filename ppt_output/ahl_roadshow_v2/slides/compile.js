// compile.js - AHL商业计划书 V2.0 PPTX编译脚本
const pptxgen = require('pptxgenjs');
const path = require('path');

const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.title = 'AHL去中心化旅行平台 商业计划书';
pres.author = 'AHL Team';
pres.subject = 'AI驱动的酒店去中心化旅行平台';

// Pure Tech Blue 配色方案 - AI科技感
const theme = {
  primary:   "FFFFFF",   // 白色主文字
  secondary: "90E0EF",   // 浅蓝次要文字
  accent:    "00B4D8",   // 青色强调
  light:     "0077B6",   // 蓝色装饰
  bg:        "03045E",    // 深蓝背景
  dark:      "023047",   // 更深的蓝
  gold:      "FFD60A",   // 金色高亮
  orange:    "FF6B35",   // 橙色点缀
};

// 共17页幻灯片
const totalSlides = 17;
for (let i = 1; i <= totalSlides; i++) {
  const num = String(i).padStart(2, '0');
  const slidePath = path.join(__dirname, `slide-${num}.js`);
  try {
    const slideModule = require(slidePath);
    slideModule.createSlide(pres, theme);
    console.log(`  Slide ${num} added`);
  } catch (e) {
    console.error(`  ERROR slide-${num}: ${e.message}`);
  }
}

const outPath = path.join(__dirname, 'output', 'AHL_商业计划书_V2.0.pptx');
pres.writeFile({ fileName: outPath })
  .then(() => console.log(`\nSaved: ${outPath}`))
  .catch(e => console.error('Write error:', e));
