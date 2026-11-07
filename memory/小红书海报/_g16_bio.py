# -*- coding: utf-8 -*-
import os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _g16_lib import CSS

EXTRA = """
.graph{position:relative}
.graph>svg{position:absolute;inset:0;width:100%;height:100%;z-index:0;pointer-events:none;overflow:visible}
.graph .layer{position:relative;z-index:2}
.nrow{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.gap{height:88px}
.node{position:relative;background:#ffffff;border:1.5px solid rgba(28,25,23,.16);border-radius:8px;padding:18px 15px;text-align:center}
.node .nk{font-size:12.5px;font-weight:900;letter-spacing:1.6px;margin-bottom:7px}
.node .nt{font-size:19px;font-weight:800;color:#1c1917;line-height:1.3}
.node .ns{font-size:15px;color:#6b6259;line-height:1.45;margin-top:5px}
.nroot{max-width:540px;margin:0 auto;background:#1c1917;border-color:#1c1917}
.nroot .nt{color:#fff;font-size:22px}
.nroot .ns{color:#c9c1b6}
.nroot .nk{color:#d8a06a}
.nmech{border-color:rgba(160,95,38,.42);background:#fdfaf4;padding:20px 11px}
.nmech .nk{color:#a05f26}
.nmech .nt{font-size:17.5px}
.ncore{max-width:600px;margin:0 auto;border-color:#a05f26;border-width:2px;background:#fdfaf4}
.ncore .nk{color:#a05f26}
.ncore .nt{font-size:21px}
.ntrig{max-width:640px;margin:0 auto;background:#a05f26;border-color:#a05f26}
.ntrig .nt{color:#fff;font-size:20px}
.ntrig .ns{color:#f2e4d4}
.ntrig .nk{color:#f7dcc0}
.nout{text-align:left;padding:19px 16px}
.nout .nt{font-size:18.5px;text-align:left}
.nout .ns{font-size:15.5px;text-align:left;margin-top:7px;line-height:1.5}
.nout .nt b{color:#a05f26}
.case{margin-top:10px;background:#ffffff;border:1.5px solid rgba(160,95,38,.45);border-radius:8px;padding:23px 22px}
.case .ct{font-size:19px;font-weight:800;color:#1c1917;margin-bottom:14px}
.case .ct .cbt{font-size:12.5px;font-weight:900;color:#fff;background:#a05f26;padding:3px 9px;border-radius:4px;letter-spacing:1.2px;margin-left:9px;vertical-align:2px}
.u25{display:flex;gap:24px;align-items:flex-start}
.u25 .udraw{flex:0 0 318px}
.u25 .utext{flex:1;font-size:17.5px;color:#57534e;line-height:1.6}
.u25 .utext b{color:#1c1917}
.u25 .utext .w{color:#a05f26;font-weight:700}
.scaf{background:#ffffff;border:1px solid rgba(28,25,23,.13);border-radius:7px;padding:23px 24px}
.slab{background:#1c1917;color:#fff;border-radius:6px;text-align:center;padding:13px 10px;font-size:22px;font-weight:900;letter-spacing:2px}
.sposts{display:flex;gap:30px;justify-content:center}
.spost{flex:1;background:linear-gradient(180deg,#a05f26,#7f4619);border-radius:0 0 5px 5px;height:58px;display:flex;align-items:center;justify-content:center;font-size:17px;color:#fff;font-weight:800;letter-spacing:4px}
.swarn{font-size:18px;color:#57534e;margin-top:12px;line-height:1.55;border-top:1px dashed rgba(28,25,23,.2);padding-top:12px}
.swarn b{color:#a05f26;font-weight:700}
"""

OUT = r"C:\Users\ericz\Desktop\小红书_生物层面的危险_9x16_2026-11-01"
os.makedirs(OUT, exist_ok=True)

ROOT = """
<div class="node nroot" data-node="root">
  <div class="nk">根 因</div>
  <div class="nt">漫长的稀缺与竞争环境</div>
  <div class="ns">生存压力 · 地位竞争 · 资源不确定</div>
</div>
"""

MECH = """
<div class="nrow">
  <div class="node nmech" data-node="m1"><div class="nk">生理</div><div class="nt">多巴胺<br>奖励回路</div></div>
  <div class="node nmech" data-node="m2"><div class="nk">生理</div><div class="nt">催产素<br>信任机制</div></div>
  <div class="node nmech" data-node="m3"><div class="nk">生理</div><div class="nt">皮质醇<br>压力反应</div></div>
  <div class="node nmech" data-node="m4"><div class="nk">社会</div><div class="nt">地位与<br>合作策略</div></div>
</div>
"""

CORE = """
<div class="node ncore" data-node="core">
  <div class="nk">被塑造的结果</div>
  <div class="nt">动机系统 · 社会行为 · 意义建构</div>
  <div class="ns">这不是设计，是选择的结果</div>
</div>
"""

TRIG = """
<div class="node ntrig" data-node="trig">
  <div class="nk">触 发 点</div>
  <div class="nt">当物质条件接近「极大满足」</div>
  <div class="ns">基本需求几乎无成本地被满足 · 生存焦虑大幅消退</div>
</div>
"""

OUTS = """
<div class="nrow">
  <div class="node nout" data-node="o1">
    <div class="nt"><b>1</b> · 动机塌陷</div>
    <div class="ns">努力、延迟满足、长期规划的进化价值下降。转向即时快感、低投入娱乐，或彻底退缩。</div>
  </div>
  <div class="node nout" data-node="o2">
    <div class="nt"><b>2</b> · 社会病理放大</div>
    <div class="ns">地位竞争不消失，只是转向更纯粹的零和符号竞争——身份、话语权、审美优越感。更尖锐，也更虚无。</div>
  </div>
  <div class="node nout" data-node="o3">
    <div class="nt"><b>3</b> · 繁殖与代际传递受挫</div>
    <div class="ns">生育意愿与育儿能力的崩溃。现实中中富裕、高福利社会的低生育率，是同一逻辑的现代表现。</div>
  </div>
  <div class="node nout" data-node="o4">
    <div class="nt"><b>4</b> · 意义真空</div>
    <div class="ns">必须自己生成「为什么活」的答案。精神资源不足，于是陷入焦虑、抑郁、成瘾或意识形态狂热。</div>
  </div>
</div>
"""

GRAPH = "".join([
 "<div class=graph id=graph>",
 "<div class=layer>" + ROOT + "</div>",
 "<div class=layer gap></div>",
 "<div class=layer>" + MECH + "</div>",
 "<div class=layer gap></div>",
 "<div class=layer>" + CORE + "</div>",
 "<div class=layer gap></div>",
 "<div class=layer>" + TRIG + "</div>",
 "<div class=layer gap></div>",
 "<div class=layer>" + OUTS + "</div>",
 "</div>",
])

CASE = """
<div class="case" data-node="u25">
  <div class="ct">案例 · Universe 25「鼠类乌托邦」实验<span class="cbt">JOHN BUNNELL · 1960s-70s</span></div>
  <div class="u25">
    <div class="udraw">
      <svg viewBox="0 0 318 200" width="318" height="200">
        <defs><marker id="a" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill="#a05f26"/></marker></defs>
        <rect x="1" y="1" width="316" height="198" rx="8" fill="#f7f3ea" stroke="rgba(160,95,38,.4)"/>
        <circle cx="24" cy="26" r="7" fill="#a05f26"/>
        <text x="40" y="31" font-size="14" fill="#57534e">食物与空间近乎无限供给</text>
        <g fill="#a05f26">
          <circle cx="28" cy="64" r="5.5"/><circle cx="50" cy="64" r="5.5"/><circle cx="72" cy="64" r="5.5"/>
          <circle cx="94" cy="64" r="5.5"/><circle cx="116" cy="64" r="5.5"/><circle cx="138" cy="64" r="5.5"/>
          <circle cx="160" cy="64" r="5.5"/><circle cx="182" cy="64" r="5.5"/>
        </g>
        <text x="200" y="69" font-size="13" fill="#6b6259">丰足期</text>
        <path d="M28 82 L28 94" stroke="#a05f26" stroke-width="2" marker-end="url(#a)"/>
        <text x="40" y="95" font-size="13.5" fill="#a05f26" font-weight="700">鼠群自我组织、繁殖扩张</text>
        <g fill="#b9834c">
          <circle cx="28" cy="122" r="5.5"/><circle cx="50" cy="122" r="5.5"/><circle cx="72" cy="122" r="5.5"/>
        </g>
        <text x="90" y="127" font-size="13" fill="#6b6259">生育意愿下滑</text>
        <path d="M28 140 L28 152" stroke="#a05f26" stroke-width="2" marker-end="url(#a)"/>
        <text x="40" y="153" font-size="13.5" fill="#a05f26" font-weight="700">仅存少数「美丽鼠群」</text>
        <circle cx="28" cy="176" r="5.5" fill="#8a4e1e"/>
        <text x="40" y="181" font-size="13" fill="#6b6259">行为结构崩坏</text>
      </svg>
    </div>
    <div class="utext">
      <b>实验设置</b>：给鼠群近乎无限的食宿与空间，撤去一切外部约束。<br>
      <b>观察结果</b>：鼠群先自我组织、扩张繁殖，随后<b>生育意愿与育儿能力崩溃</b>，
      最终只剩一小群行为结构崩坏的「美丽鼠群」。<br>
      <b>为什么是它</b>：Universe 25 是「稀缺一旦解除，行为秩序会怎样崩解」最直接的实验室样本，
      也是第 3 个后果（繁殖与代际传递受挫）最干净的对应物。<br>
      <span class="w">注意</span>：该实验的解读边界学界仍有争议，此处仅作原文引述。
    </div>
  </div>
</div>
"""

SCAF = """
<div class="scaf">
  <div class="slab">人类行为秩序</div>
  <div class="sposts">
    <div class="spost">稀 缺</div>
    <div class="spost">稀 缺</div>
    <div class="spost">稀 缺</div>
  </div>
  <div class="swarn">彻底抽掉这根脚手架，系统<b>不一定会自动升维</b>，更可能先经历<b>失稳甚至坍塌</b>。</div>
</div>
"""
BODY = GRAPH + CASE + SCAF

FOOT_Q = "换句话说，<b>稀缺是残酷的</b>，但它也是人类行为秩序的重要脚手架。"
FOOT_S = "基因并非被设计成适应匮乏，而是在匮乏中被筛选——把环境中的优势带进下一代的，是生存与繁殖的相对成功率。稀缺一旦消失，脚手架随之消失，而结构不会自动升级。"

def page(kicker, title, sub, body, q, s):
    h = []
    h.append("<div class=wrap><div class=head>")
    h.append("<div class=kick>" + kicker + "</div>")
    h.append("<h1>" + title + "</h1>")
    h.append("<div class=sub>" + sub + "</div>")
    h.append("</div><div class=body>" + body + "</div>")
    h.append("<div class=foot><div class=q>" + q + "</div><div class=s>" + s + "</div></div></div>")
    h.append("<div class=brand><div class=bn>B</div><div class=bl>B166ER</div></div>")
    h.append("<div class=wm>EVOLUTION / 01 &middot; 2026-11-01</div>")
    return ("<!DOCTYPE html><html lang=zh-CN><head><meta charset=utf-8><title>" + kicker +
            "</title><style>" + CSS + EXTRA + "</style></head><body>" + "".join(h) + "</body></html>")

if __name__ == "__main__":
    html = page("EVOLUTION &middot; 演化机制",
                "生物层面的<span class=hl>危险</span>在哪里",
                "稀缺是脚手架 —— 抽掉它，系统不会自动升维",
                BODY, FOOT_Q, FOOT_S)
    open(os.path.join(OUT, "_bio.html"), "w", encoding="utf-8").write(html)
    print("html bytes:", len(html))
