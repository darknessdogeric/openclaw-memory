# -*- coding: utf-8 -*-
import os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _g16_bio import page, BODY, FOOT_Q, FOOT_S, OUT

from playwright.sync_api import sync_playwright

html = page("EVOLUTION &middot; 演化机制",
            "生物层面的<span class=hl>危险</span>在哪里",
            "稀缺是脚手架 —— 抽掉它，系统不会自动升维",
            BODY, FOOT_Q, FOOT_S)

BUILD = """
() => {
  const g = document.getElementById("graph");
  const cs = document.querySelector(".case");
  if (cs) g.appendChild(cs);
  const nodes = {};
  document.querySelectorAll("[data-node]").forEach(el => {
    nodes[el.dataset.node] = el.getBoundingClientRect();
  });
  const gr = g.getBoundingClientRect();
  const E = [
    ["root","m1",0],["root","m2",0],["root","m3",0],["root","m4",0],
    ["m1","core",0],["m2","core",0],["m3","core",0],["m4","core",0],
    ["core","trig",0],
    ["trig","o1",0],["trig","o2",0],["trig","o3",0],["trig","o4",0],
    ["o3","u25",1]
  ];
  let p = "";
  E.forEach(e => {
    const ra = nodes[e[0]], rb = nodes[e[1]];
    if (!ra || !rb) return;
    const x1 = ra.left + ra.width/2 - gr.left;
    const y1 = ra.bottom - gr.top;
    let x2 = rb.left + rb.width/2 - gr.left;
    let y2 = rb.top - gr.top;
    if (e[1] === "core") {
      x2 = Math.min(Math.max(x2, rb.left - gr.left + 26), rb.right - gr.left - 26);
    }
    if (e[1] === "u25") { y2 = rb.top - gr.top - 5; }
    const dy = Math.max(16, (y2 - y1) * 0.45);
    const dash = e[2] ? " stroke-dasharray='6 4'" : "";
    p += "<path d='M " + x1 + " " + y1 + " C " + x1 + " " + (y1+dy) + " " + x2 + " " + (y2-dy) +
         " " + x2 + " " + y2 + "' fill='none' stroke='#a05f26' stroke-width='2' opacity='0.62'" +
         dash + " marker-end='url(#ah)'/>";
  });
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.innerHTML = "<defs><marker id='ah' markerWidth='8' markerHeight='8' refX='6' refY='3' orient='auto'>" +
                "<path d='M0,0 L7,3 L0,6 Z' fill='#a05f26'/></marker></defs>" + p;
  g.insertBefore(svg, g.firstChild);
  return Object.keys(nodes).length;
}
"""

CHECK = """
() => {
  const issues = [];
  const W = 1080, H = 1920;
  const R = (e) => e.getBoundingClientRect();
  const tx = (e) => (e.textContent || "").trim();
  document.querySelectorAll("*").forEach(el => {
    if (el.children.length === 0 && tx(el)) {
      if (el.scrollWidth > el.clientWidth + 2)
        issues.push("文字溢出: " + (el.className || el.tagName) + " :: " + tx(el).slice(0,22));
      if (el.clientHeight > 30 && el.scrollHeight > el.clientHeight + 2)
        issues.push("纵向溢出: " + (el.className || el.tagName) + " :: " + tx(el).slice(0,22));
    }
  });
  document.querySelectorAll(".wrap *").forEach(el => {
    const r = R(el);
    if (r.width === 0 && r.height === 0) return;
    if (r.right > W + 1 || r.bottom > H + 1 || r.left < -1)
      issues.push("出画布: " + (el.className || el.tagName) + " b=" + Math.round(r.bottom));
  });
  if (document.body.scrollHeight > H + 2) issues.push("body 纵向溢出 " + document.body.scrollHeight);
  if (document.body.scrollWidth > W + 2) issues.push("body 横向溢出 " + document.body.scrollWidth);
  const brand = document.querySelector(".brand");
  if (brand) {
    const b = R(brand);
    document.querySelectorAll(".wrap *").forEach(el => {
      if (!tx(el) || el.children.length || brand.contains(el)) return;
      const r = R(el);
      if (r.right > b.left && r.left < b.right && r.bottom > b.top && r.top < b.bottom)
        issues.push("B标压字: " + tx(el).slice(0,20));
    });
  }
  const wm = document.querySelector(".wm");
  const foot = document.querySelector(".foot");
  if (wm && foot) { if (R(wm).top < R(foot).bottom) issues.push("水印压foot"); }
  const bd = document.querySelector(".body");
  if (bd) {
    const kids = [...bd.children].map(k => R(k));
    if (kids.length > 2) {
      const gaps = [];
      for (let i = 1; i < kids.length; i++) gaps.push(kids[i].top - kids[i-1].bottom);
      const mn = Math.min.apply(null, gaps), mx = Math.max.apply(null, gaps);
      if (mx - mn > 48) issues.push("间距不均 极差 " + Math.round(mx-mn) + "px");
    }
    const bb = bd.getBoundingClientRect();
    const last = bd.lastElementChild.getBoundingClientRect();
    if (bb.bottom - last.bottom > 150) issues.push("下部空隙 " + Math.round(bb.bottom - last.bottom) + "px");
  }
  const svg = document.querySelector("#graph > svg");
  if (!svg) issues.push("SVG 连线层缺失");
  else if (svg.querySelectorAll("path[marker-end]").length < 14) issues.push("连线数不足 " + svg.querySelectorAll("path[marker-end]").length);
  return issues;
}
"""

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=2)
    pg.set_content(html, wait_until="domcontentloaded")
    pg.wait_for_timeout(400)
    n = pg.evaluate(BUILD)
    pg.wait_for_timeout(250)
    iss = pg.evaluate(CHECK)
    out = os.path.join(OUT, "生物层面的危险_9x16.png")
    pg.screenshot(path=out, full_page=False, omit_background=False, timeout=25000)
    pg.close()
    b.close()
print("nodes:", n, "|", ("OK  " if not iss else "WARN"), os.path.basename(out), os.path.getsize(out),
      ("" if not iss else "| " + " ; ".join(iss[:8])))
