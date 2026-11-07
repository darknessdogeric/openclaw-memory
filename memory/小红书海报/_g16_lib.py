# -*- coding: utf-8 -*-
"""9:16 (1080x1920) Clean & Minimal — 演化机制专题"""
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;background:radial-gradient(130% 70% at 50% 0%,#fdfbf6 0%,#f2eee3 100%);
 color:#1c1917;overflow:hidden;
 font-family:'Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif;position:relative}
.wrap{position:relative;z-index:2;width:100%;height:100%;padding:56px 78px 48px 48px;
 display:flex;flex-direction:column}
.head{flex:0 0 auto}
.kick{font-size:19px;color:#a05f26;letter-spacing:4px;font-weight:700;margin-bottom:14px}
h1{font-size:56px;font-weight:900;line-height:1.16;letter-spacing:-.6px;
 font-family:'Noto Serif SC','Songti SC',serif}
h1.sm{font-size:44px;line-height:1.22}
h1 .hl{color:#a05f26}
.sub{font-size:21px;color:#78716c;line-height:1.5;margin-top:14px}
.body{flex:1 1 auto;display:flex;flex-direction:column;justify-content:space-evenly;
 gap:14px;min-height:0;padding:18px 0}
.foot{flex:0 0 auto;border-top:1px solid rgba(28,25,23,.16);padding-top:16px;margin-top:12px}
.foot .q{font-size:25px;font-weight:800;line-height:1.45}
.foot .q b{color:#a05f26}
.foot .s{font-size:15px;color:#8a8074;margin-top:10px;line-height:1.55}
.card{background:#ffffff;border:1px solid rgba(28,25,23,.13);border-radius:7px;padding:18px 20px}
.card.acc{border-color:#a05f26;border-width:1.5px;background:#fdfaf4}
.card.soft{background:#f2efe6;border-color:rgba(28,25,23,.1)}
.card .t{font-size:21px;font-weight:800;color:#1c1917;margin-bottom:8px;display:flex;
 justify-content:space-between;align-items:baseline;gap:12px}
.card .t .tag{font-size:13px;font-weight:700;color:#8a8074;background:#f0ece2;
 padding:3px 9px;border-radius:4px;white-space:nowrap;letter-spacing:.5px}
.card.acc .t .tag{background:#a05f26;color:#fff}
.card .d{font-size:18px;color:#57534e;line-height:1.6}
.card .d b{color:#1c1917;font-weight:700}
.card.acc .d b{color:#a05f26}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.lead{font-size:21px;color:#4b4540;line-height:1.62}
.lead b{color:#a05f26;font-weight:700}
/* 燃料条 */
.gauge{background:#ffffff;border:1px solid rgba(28,25,23,.13);border-radius:7px;padding:18px 20px 16px}
.gauge .gt{font-size:20px;font-weight:800;color:#1c1917;margin-bottom:12px}
.gbar{display:flex;height:74px;border-radius:6px;overflow:hidden;border:1px solid rgba(28,25,23,.12)}
.gseg{flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;
 font-size:15px;line-height:1.4;letter-spacing:.3px}
.gseg.on{background:linear-gradient(100deg,#a05f26,#c07f42);color:#fff}
.gseg.on b{font-size:17px;font-weight:800}
.gseg.off{background:#f2efe6;color:#8a8074;
 background-image:repeating-linear-gradient(45deg,rgba(28,25,23,.055) 0 8px,transparent 8px 16px)}
.gseg.off b{font-size:17px;font-weight:800;color:#57534e}
.glab{font-size:15.5px;color:#6b6259;margin-top:11px;line-height:1.5}
.glab b{color:#a05f26}
/* 三步机制链 */
.chain{display:flex;align-items:stretch;gap:10px}
.cstep{flex:1;background:#ffffff;border:1px solid rgba(28,25,23,.13);border-radius:7px;
 padding:15px 14px;display:flex;flex-direction:column}
.cstep.acc{background:#fdfaf4;border-color:#a05f26;border-width:1.5px}
.cstep .cn{font-size:13px;font-weight:900;color:#a05f26;letter-spacing:1.5px;margin-bottom:8px}
.cstep .ch{font-size:19px;font-weight:800;color:#1c1917;line-height:1.32;margin-bottom:7px}
.cstep .cp{font-size:16px;color:#6b6259;line-height:1.5}
.cstep.acc .cp{color:#57534e}
.carrow{flex:0 0 26px;display:flex;align-items:center;justify-content:center;
 font-size:26px;color:#a05f26;font-weight:700}
/* 后果卡编号 */
.eff{display:flex;gap:11px;align-items:flex-start;margin-bottom:9px}
.eff .en{flex:0 0 30px;height:30px;border-radius:5px;background:#a05f26;color:#fff;
 font-size:16px;font-weight:900;display:flex;align-items:center;justify-content:center}
.eff .et{font-size:20px;font-weight:800;color:#1c1917;line-height:1.28}
.brand{position:absolute;top:12px;right:12px;z-index:9;width:54px;height:54px;border-radius:7px;
 background:#a05f26;display:flex;flex-direction:column;align-items:center;justify-content:center}
.brand .bn{font-size:21px;font-weight:900;color:#fff;line-height:1}
.brand .bl{font-size:6.5px;color:rgba(255,255,255,.9);letter-spacing:1.1px;margin-top:2px;line-height:1}
.wm{position:absolute;bottom:9px;left:48px;z-index:9;font-size:12px;color:#a89f92;
 letter-spacing:1.4px;font-family:'Courier New',monospace}
"""