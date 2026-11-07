"""自绘示意图 v3 — 改为宽扁比例 (980x250) + 大字号
根因: 上一版 SVG viewBox 980x420 (比 2.33) 塞进 988x138 的图区 (比 7.2),
      preserveAspectRatio=meet 只能按高度缩放 (0.34x), 标注文字全部变成小点。
修法: SVG 本身改宽扁 + 字号/线宽按 1:1 显示设计, 这样 150px 高时缩放 0.6, 字仍可读。
"""
import math


def _wrap(w, h, body):
    return (f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'xmlns="http://www.w3.org/2000/svg">' + body + '</svg>')


def solar_svg(w=980, h=250, fg="#E8E4DA", dim="#6E7A92", ac="#D4A74A"):
    """太阳系接力轨迹 (宽扁版)"""
    cx, cy = 92, 178
    orbs = [("水星", 34, 5, "#8C7A63", 236), ("金星", 62, 9, "#C9A227", 190),
            ("地球", 94, 10, "#3E6BA8", 146), ("火星", 128, 8, "#B4503E", 108),
            ("木星", 174, 26, "#C08552", 66), ("土星", 222, 22, "#D4B36A", 24)]
    P = []
    for name, r, pr, col, ang in orbs:
        ry = r * 0.42
        P.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{ry:.1f}" fill="none" '
                 f'stroke="{col}" stroke-width="2" opacity="0.38"/>')

    def pos(r, ang):
        a = math.radians(ang)
        return (cx + math.cos(a) * r, cy - math.sin(a) * r * 0.42)

    for name, r, pr, col, ang in orbs:
        x, y = pos(r, ang)
        P.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{pr}" fill="{col}" opacity="0.96"/>')

    P.append(f'<circle cx="{cx}" cy="{cy}" r="36" fill="#E8B84B" opacity="0.16"/>')
    P.append(f'<circle cx="{cx}" cy="{cy}" r="23" fill="#E8B84B"/>')

    ex, ey = pos(94, 146)
    jx, jy = pos(174, 66)
    sx, sy = pos(222, 24)
    P.append(f'<path d="M {ex:.0f} {ey:.0f} Q {cx+128} {cy-108} {jx:.0f} {jy:.0f} '
             f'L {sx:.0f} {sy:.0f}" fill="none" stroke="{ac}" stroke-width="5" '
             f'stroke-linecap="round"/>')
    P.append(f'<rect x="{ex-9:.0f}" y="{ey-9:.0f}" width="18" height="18" fill="{ac}"/>')
    P.append(f'<rect x="{sx-9:.0f}" y="{sy-9:.0f}" width="18" height="18" fill="{ac}"/>')

    p1 = (sx + 150, sy - 62)
    p2 = (p1[0] + 190, p1[1] - 40)
    P.append(f'<path d="M {sx:.0f} {sy:.0f} Q {p1[0]-50:.0f} {p1[1]+24:.0f} {p1[0]:.0f} {p1[1]:.0f} '
             f'L {p2[0]:.0f} {p2[1]:.0f}" fill="none" stroke="{fg}" stroke-width="4" '
             f'stroke-linecap="round" stroke-dasharray="15 12" opacity="0.92"/>')
    P.append(f'<circle cx="{p2[0]:.0f}" cy="{p2[1]:.0f}" r="12" fill="{fg}"/>')
    P.append(f'<circle cx="{p2[0]:.0f}" cy="{p2[1]:.0f}" r="26" fill="none" stroke="{fg}" '
             f'stroke-width="2.4" opacity="0.38"/>')

    for name, r, pr, col, ang in orbs:
        x, y = pos(r, ang)
        dy = -18 if pr < 12 else -34
        P.append(f'<text x="{x:.0f}" y="{y+dy:.0f}" fill="{col}" font-size="21" '
                 f'text-anchor="middle" font-family="Microsoft YaHei,sans-serif">{name}</text>')

    P.append(f'<g><rect x="{sx+26:.0f}" y="{sy-2:.0f}" width="17" height="17" fill="{ac}"/>'
             f'<text x="{sx+52:.0f}" y="{sy+13:.0f}" fill="{ac}" font-size="25" font-weight="700" '
             f'font-family="Microsoft YaHei,sans-serif">先驱者</text>'
             f'<text x="{sx+52:.0f}" y="{sy+36:.0f}" fill="{dim}" font-size="19" '
             f'font-family="Microsoft YaHei,sans-serif">推门者 · 已失联</text></g>')
    P.append(f'<g><circle cx="{p2[0]:.0f}" cy="{p2[1]:.0f}" r="11" fill="{fg}"/>'
             f'<text x="{p2[0]+22:.0f}" y="{p2[1]+7:.0f}" fill="{fg}" font-size="25" font-weight="700" '
             f'font-family="Microsoft YaHei,sans-serif">旅行者</text>'
             f'<text x="{p2[0]+22:.0f}" y="{p2[1]+30:.0f}" fill="{dim}" font-size="19" '
             f'font-family="Microsoft YaHei,sans-serif">仍在发信号</text></g>')
    return _wrap(w, h, "".join(P))


def probe_svg(w=980, h=250, fg="#E8E4DA", dim="#6E7A92", ac="#D4A74A"):
    """先驱者号探测器剪影 (宽扁版)"""
    P = []
    cx, cy = 300, 150
    # 高增益天线 (六边碟侧视)
    P.append(f'<path d="M {cx-170} {cy-72} L {cx+10} {cy-72} L {cx+44} {cy-4} '
             f'L {cx-56} {cy-4} Z" fill="none" stroke="{fg}" stroke-width="4" '
             f'stroke-linejoin="round" opacity="0.94"/>')
    for i in range(4):
        t = i / 4
        x = cx - 170 + t * 180
        P.append(f'<line x1="{x:.0f}" y1="{cy-72}" x2="{cx-46+t*100:.0f}" y2="{cy-4}" '
                 f'stroke="{fg}" stroke-width="1.6" opacity="0.45"/>')
    P.append(f'<line x1="{cx-170}" y1="{cy-72}" x2="{cx+10}" y2="{cy-72}" stroke="{fg}" '
             f'stroke-width="4"/>')
    P.append(f'<line x1="{cx-60}" y1="{cy-72}" x2="{cx-16}" y2="{cy-104}" stroke="{fg}" stroke-width="2.6"/>')
    P.append(f'<circle cx="{cx-16}" cy="{cy-110}" r="9" fill="none" stroke="{fg}" stroke-width="2.6"/>')
    # 柱体
    P.append(f'<rect x="{cx+44}" y="{cy-30}" width="128" height="82" rx="7" fill="{ac}" opacity="0.20"/>')
    P.append(f'<rect x="{cx+44}" y="{cy-30}" width="128" height="82" rx="7" fill="none" '
             f'stroke="{ac}" stroke-width="3.4"/>')
    for i in range(1, 5):
        P.append(f'<line x1="{cx+44+i*25}" y1="{cy-30}" x2="{cx+44+i*25}" y2="{cy+52}" '
                 f'stroke="{ac}" stroke-width="1.2" opacity="0.55"/>')
    P.append(f'<line x1="{cx+10}" y1="{cy-4}" x2="{cx+58}" y2="{cy-30}" stroke="{fg}" stroke-width="2.6" opacity="0.82"/>')
    P.append(f'<line x1="{cx-8}" y1="{cy-4}" x2="{cx+44}" y2="{cy-30}" stroke="{fg}" stroke-width="2.6" opacity="0.82"/>')
    # 磁强计伸杆
    P.append(f'<line x1="{cx+172}" y1="{cy+8}" x2="{cx+560}" y2="{cy+24}" stroke="{fg}" stroke-width="3" opacity="0.92"/>')
    P.append(f'<line x1="{cx+540}" y1="{cy-2}" x2="{cx+540}" y2="{cy+50}" stroke="{ac}" stroke-width="3"/>')
    # V 形天线
    P.append(f'<line x1="{cx+110}" y1="{cy+52}" x2="{cx+250}" y2="{cy+118}" stroke="{fg}" stroke-width="2.6" opacity="0.88"/>')
    P.append(f'<line x1="{cx+84}" y1="{cy+52}" x2="{cx+250}" y2="{cy+118}" stroke="{fg}" stroke-width="2.6" opacity="0.88"/>')
    P.append(f'<rect x="{cx+240}" y="{cy+108}" width="30" height="22" fill="#B4503E" opacity="0.95"/>')
    # 铭牌
    P.append(f'<rect x="{cx+186}" y="{cy+14}" width="34" height="28" rx="3" fill="none" '
             f'stroke="{ac}" stroke-width="2.2" opacity="0.9"/>')
    P.append(f'<circle cx="{cx+203}" cy="{cy+28}" r="6" fill="none" stroke="{ac}" stroke-width="1.5" opacity="0.8"/>')

    def ann(x, y, tx, up=True):
        dy = -1 if up else 1
        return (f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+dy*16}" stroke="{dim}" stroke-width="1.6" opacity="0.85"/>'
                f'<text x="{x}" y="{y+dy*36}" fill="{dim}" font-size="21" text-anchor="middle" '
                f'font-family="Microsoft YaHei,sans-serif">{tx}</text>')
    P.append(ann(cx - 110, cy - 72, "高增益天线", True))
    P.append(ann(cx + 108, cy - 30, "镀金铝板", True))
    P.append(ann(cx + 540, cy + 26, "磁强计伸杆", False))
    P.append(ann(cx + 255, cy + 118, "V 形天线杆", False))
    return _wrap(w, h, "".join(P))


def plaque_svg(w=980, h=270, plate="#D9B96A", edge="#A88B45", ink="#2A2318"):
    """先驱者号铭牌 (宽扁 2x2 象限)"""
    P = []
    P.append(f'<rect x="6" y="6" width="{w-12}" height="{h-12}" rx="8" fill="{plate}"/>')
    for i in range(230):
        x = 10 + i * 4.3
        P.append(f'<line x1="{x:.0f}" y1="8" x2="{x-20:.0f}" y2="{h-8}" '
                 f'stroke="{edge}" stroke-width="0.6" opacity="0.15"/>')
    P.append(f'<rect x="6" y="6" width="{w-12}" height="{h-12}" rx="8" fill="none" '
             f'stroke="{edge}" stroke-width="3.5"/>')
    MX = w / 2
    P.append(f'<line x1="{MX}" y1="22" x2="{MX}" y2="{h-22}" stroke="{edge}" stroke-width="1.8" opacity="0.55"/>')

    # 左上 氢原子
    hx, hy = 160, 86
    P.append(f'<circle cx="{hx}" cy="{hy}" r="14" fill="{ink}"/>')
    for rot in (0, 60, -60):
        P.append(f'<ellipse cx="{hx}" cy="{hy}" rx="56" ry="22" fill="none" stroke="{ink}" '
                 f'stroke-width="3" transform="rotate({rot} {hx} {hy})"/>')
    P.append(f'<circle cx="{hx+42}" cy="{hy+31}" r="6.5" fill="{ink}"/>')
    P.append(f'<text x="{hx}" y="152" fill="{ink}" font-size="20" text-anchor="middle" '
             f'font-family="Microsoft YaHei,sans-serif" opacity="0.88">氢原子 · 一切的起点</text>')

    # 右上 14 脉冲星
    pcx, pcy = 720, 84
    P.append(f'<circle cx="{pcx}" cy="{pcy}" r="7" fill="{ink}"/>')
    for i in range(14):
        a = math.radians(i * (360 / 14) - 8)
        L = 38 + (i % 4) * 9
        x2, y2 = pcx + math.cos(a) * L, pcy + math.sin(a) * L * 0.86
        P.append(f'<line x1="{pcx}" y1="{pcy}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{ink}" '
                 f'stroke-width="1.7" opacity="0.8"/>')
        P.append(f'<circle cx="{x2:.0f}" cy="{y2:.0f}" r="3.8" fill="{ink}"/>')
        P.append(f'<line x1="{x2-7:.0f}" y1="{y2:.0f}" x2="{x2+7:.0f}" y2="{y2:.0f}" '
                 f'stroke="{ink}" stroke-width="2.2"/>')
    P.append(f'<text x="{pcx}" y="152" fill="{ink}" font-size="20" text-anchor="middle" '
             f'font-family="Microsoft YaHei,sans-serif" opacity="0.88">14 颗脉冲星 · 指出你在哪</text>')

    # 左下 太阳系
    sx, sy = 140, 204
    for rr in (18, 32, 46, 62, 80, 98):
        P.append(f'<ellipse cx="{sx}" cy="{sy}" rx="{rr}" ry="{rr*0.36:.0f}" fill="none" '
                 f'stroke="{ink}" stroke-width="1.3" opacity="0.42"/>')
    P.append(f'<circle cx="{sx}" cy="{sy}" r="11" fill="{ink}"/>')
    P.append(f'<path d="M {sx+42} {sy-16} L {sx+72} {sy-28} L {sx+104} {sy-38}" '
             f'fill="none" stroke="{ink}" stroke-width="2.8" stroke-linecap="round"/>')
    P.append(f'<rect x="{sx+38}" y="{sy-21}" width="10" height="10" fill="{ink}"/>')
    P.append(f'<text x="{sx+52}" y="256" fill="{ink}" font-size="20" text-anchor="middle" '
             f'font-family="Microsoft YaHei,sans-serif" opacity="0.88">太阳系与出航轨迹</text>')

    # 右下 人类
    def man(x, y, s=1.0):
        g = [f'<g transform="translate({x},{y}) scale({s},{s})">']
        g.append(f'<circle cx="0" cy="-52" r="12" fill="none" stroke="{ink}" stroke-width="3.4"/>')
        g.append(f'<line x1="0" y1="-40" x2="0" y2="0" stroke="{ink}" stroke-width="3.4"/>')
        g.append(f'<line x1="0" y1="-32" x2="26" y2="-70" stroke="{ink}" stroke-width="3.4"/>')
        g.append(f'<line x1="0" y1="-32" x2="-21" y2="-10" stroke="{ink}" stroke-width="3.4"/>')
        g.append(f'<line x1="0" y1="0" x2="-15" y2="42" stroke="{ink}" stroke-width="3.4"/>')
        g.append(f'<line x1="0" y1="0" x2="16" y2="42" stroke="{ink}" stroke-width="3.4"/>')
        g.append('</g>')
        return "".join(g)

    def woman(x, y, s=0.92):
        g = [f'<g transform="translate({x},{y}) scale({s},{s})">']
        g.append(f'<circle cx="0" cy="-48" r="10" fill="none" stroke="{ink}" stroke-width="3.2"/>')
        g.append(f'<line x1="0" y1="-38" x2="0" y2="0" stroke="{ink}" stroke-width="3.2"/>')
        g.append(f'<line x1="0" y1="-30" x2="-26" y2="-18" stroke="{ink}" stroke-width="3.2"/>')
        g.append(f'<line x1="0" y1="-30" x2="24" y2="-16" stroke="{ink}" stroke-width="3.2"/>')
        g.append(f'<line x1="0" y1="0" x2="-12" y2="38" stroke="{ink}" stroke-width="3.2"/>')
        g.append(f'<line x1="0" y1="0" x2="13" y2="38" stroke="{ink}" stroke-width="3.2"/>')
        g.append('</g>')
        return "".join(g)

    P.append(man(690, 206))
    P.append(woman(748, 206))
    P.append(f'<text x="712" y="258" fill="{ink}" font-size="20" text-anchor="middle" '
             f'font-family="Microsoft YaHei,sans-serif" opacity="0.88">你好 · 也可以是再见</text>')
    return _wrap(w, h, "".join(P))


if __name__ == "__main__":
    for fn in (solar_svg, probe_svg, plaque_svg):
        print(fn.__name__, len(fn()))
