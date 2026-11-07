# -*- coding: utf-8 -*-
"""9图 v2 — Clean & Minimal 范式 (article-to-infographic style-presets)"""
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1440px;background:radial-gradient(130% 80% at 50% 0%,#fdfbf6 0%,#f2eee3 100%);color:#1c1917;overflow:hidden;
 font-family:'Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif;position:relative}
.wrap{position:relative;z-index:2;width:100%;height:100%;padding:52px 48px 44px;
 display:flex;flex-direction:column}
.head{flex:0 0 auto}
.kick{font-size:18px;color:#a05f26;letter-spacing:4px;font-weight:700;margin-bottom:12px}
h1{font-size:50px;font-weight:900;line-height:1.18;letter-spacing:-.5px;
 font-family:'Noto Serif SC','Songti SC',serif}
h1.sm{font-size:41px;line-height:1.22}
h1 .hl{color:#a05f26}
.sub{font-size:19px;color:#78716c;line-height:1.5;margin-top:12px}
.body{flex:1 1 auto;display:flex;flex-direction:column;justify-content:space-evenly;
 gap:12px;min-height:0;padding:14px 0}
.foot{flex:0 0 auto;border-top:1px solid rgba(28,25,23,.16);padding-top:14px;margin-top:10px}
.foot .q{font-size:22px;font-weight:800;line-height:1.45}
.foot .q b{color:#a05f26}
.foot .s{font-size:14px;color:#8a8074;margin-top:8px;line-height:1.5}
.card{background:#ffffff;border:1px solid rgba(28,25,23,.13);border-radius:6px;padding:16px 18px}
.card.acc{border-color:#a05f26;border-width:1.5px;background:#fdfaf4}
.card.soft{background:#f2efe6;border-color:rgba(28,25,23,.1)}
.card .t{font-size:20px;font-weight:800;color:#1c1917;margin-bottom:7px;display:flex;
 justify-content:space-between;align-items:baseline;gap:12px}
.card .t .tag{font-size:13px;font-weight:700;color:#8a8074;background:#f0ece2;
 padding:3px 9px;border-radius:4px;white-space:nowrap;letter-spacing:.5px}
.card.acc .t .tag{background:#a05f26;color:#fff}
.card .d{font-size:17px;color:#57534e;line-height:1.58}
.card .d b{color:#1c1917;font-weight:700}
.card.acc .d b{color:#a05f26}
.card .d i{font-style:normal;color:#8a8074;font-size:15.5px}
.card ul{list-style:none;padding:0;margin-top:6px}
.card li{font-size:16.5px;color:#57534e;line-height:1.5;padding:4px 0 4px 15px;
 position:relative;border-bottom:1px solid rgba(28,25,23,.07)}
.card li:last-child{border-bottom:none}
.card li::before{content:"";position:absolute;left:0;top:13px;width:6px;height:6px;
 border-radius:50%;background:#a05f26}
.card li b{color:#1c1917}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.row3{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.g3c{background:#ffffff;border:1px solid rgba(28,25,23,.13);border-radius:6px;padding:14px 13px}
.g3c.acc{background:#fdfaf4;border-color:#a05f26;border-width:1.5px}
.g3c .k{font-size:13px;color:#8a8074;letter-spacing:1px;margin-bottom:6px;font-weight:700}
.g3c .v{font-size:30px;font-weight:900;color:#1c1917;line-height:1.1;margin-bottom:6px}
.g3c.acc .v{color:#a05f26}
.g3c .d{font-size:14.5px;color:#6b6259;line-height:1.5}
.g3c.acc .d{color:#57534e}
.g3c .d b{color:#1c1917}
.kv{display:flex;justify-content:space-between;align-items:baseline;gap:14px;
 border-bottom:1px solid rgba(28,25,23,.1);padding:9px 0}
.kv:last-child{border-bottom:none}
.kv .k{font-size:17px;color:#57534e}
.kv .v{font-size:17px;font-weight:700;color:#1c1917;text-align:right}
.kv .v.a{color:#a05f26}
.tl{display:flex;flex-direction:column;gap:10px}
.tlrow{display:flex;gap:16px;align-items:flex-start}
.tlrow .yr{flex:0 0 104px;font-size:23px;font-weight:900;color:#a05f26;line-height:1.18}
.tlrow .tx{flex:1;border-left:2px solid rgba(160,95,38,.32);padding-left:16px}
.tlrow .tx .h{font-size:19px;font-weight:700;color:#1c1917;margin-bottom:3px}
.tlrow .tx .p{font-size:16px;color:#6b6259;line-height:1.5}
.tlrow .tx .p b{color:#1c1917}
.stack{display:flex;flex-direction:column;gap:8px}
.tier{display:flex;align-items:center;gap:14px;background:#ffffff;
 border:1px solid rgba(28,25,23,.13);border-radius:6px;padding:12px 15px}
.tier .no{flex:0 0 34px;height:34px;border-radius:5px;background:#a05f26;color:#fff;
 font-size:17px;font-weight:900;display:flex;align-items:center;justify-content:center}
.tier .tx{flex:1}
.tier .tx .h{font-size:19px;font-weight:800;color:#1c1917}
.tier .tx .p{font-size:15.5px;color:#6b6259;line-height:1.45;margin-top:2px}
.matrix{display:grid;grid-template-columns:150px 1fr;gap:7px 12px;align-items:center}
.matrix .mh{font-size:14px;font-weight:800;color:#8a8074;letter-spacing:.5px}
.matrix .mc{font-size:16.5px;color:#1c1917;background:#ffffff;border-radius:5px;
 border:1px solid rgba(28,25,23,.13);padding:9px 12px;line-height:1.35}
.matrix .mc.a{background:#fdfaf4;border-color:#a05f26;font-weight:600}
.matrix .mc.g{background:#f2efe6;color:#57534e}
.brand{position:absolute;top:12px;right:12px;z-index:9;width:54px;height:54px;border-radius:7px;
 background:#a05f26;display:flex;flex-direction:column;align-items:center;justify-content:center}
.brand .bn{font-size:21px;font-weight:900;color:#fff;line-height:1}
.brand .bl{font-size:6.5px;color:rgba(255,255,255,.9);letter-spacing:1.1px;margin-top:2px;line-height:1}
.wm{position:absolute;bottom:7px;left:48px;z-index:9;font-size:12px;color:#a89f92;
 letter-spacing:1.4px;font-family:'Courier New',monospace}
.toc{display:grid;grid-template-columns:1fr 1fr;gap:8px 18px}
.toc .it{display:flex;gap:10px;align-items:baseline;font-size:16px;color:#6b6259}
.toc .it .n{font-size:14px;font-weight:900;color:#a05f26;min-width:19px}
.toc .it.hl{color:#1c1917;font-weight:700}
.lead{font-size:20px;color:#57534e;line-height:1.6}
.lead b{color:#a05f26}
.bigline{display:flex;align-items:baseline;gap:12px}
.bigline .n{font-size:52px;font-weight:900;color:#a05f26;line-height:1}
.bigline .u{font-size:17px;color:#6b6259;line-height:1.45}
"""
