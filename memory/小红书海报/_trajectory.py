"""SVG 接力轨迹图 — 太阳系行星轨道 + 先驱者/旅行者路径
自绘而非 AI 生成: 需要信息精准 (轨道顺序/相对位置), AI 图会画错
"""
import math


def solar_svg(w=980, h=430):
    """太阳 + 4 颗行星轨道 + 先驱者/旅行者路径 (侧视剖面)"""
    cx, cy = 120, 215          # 太阳在左
    orbs = [
        # (名称, 轨道半径, 半径比例, 颜色)
        ("水星", 46, 3, "#8C7A63"),
        ("金星", 82, 6, "#C9A227"),
        ("地球", 122, 6.5, "#3E6BA8"),
        ("火星", 168, 5, "#B4503E"),
        ("木星", 240, 20, "#C08552"),
        ("土星", 330, 17, "#D4B36A"),
    ]
    P = []
    for name, r, pr, col in orbs:
        # 轨道椭圆 (略扁, 侧视透视)
        ry = r * 0.42
        P.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{ry:.1f}" fill="none" '
                 f'stroke="{col}" stroke-width="1.6" opacity="0.42"/>')
        # 行星位置: 沿轨道放在不同角度, 避免重叠
        P.append(f'<circle cx="{cx}" cy="{cy}" r="{pr}" fill="{col}" opacity="0.95"/>')

    # 太阳
    P.append(f'<circle cx="{cx}" cy="{cy}" r="24" fill="#E8B84B"/>')
    P.append(f'<circle cx="{cx}" cy="{cy}" r="38" fill="#E8B84B" opacity="0.18"/>')

    # 先驱者 10 号: 从地球出发行星, 再深木星 (实线 + 实心方点)
    # 简化: 一条从地球到木星再到土星外侧的折线
    P.append(f'<path d="M {cx+118} {cy-52} L {cx+196} {cy-78} L {cx+300} {cy-112}" '
             f'fill="none" stroke="#D4A74A" stroke-width="4" stroke-linecap="round" '
             f'stroke-dasharray="none" opacity="0.95"/>')
    P.append(f'<rect x="{cx+112}" y="{cy-58}" width="13" height="13" fill="#D4A74A" '
             f'transform="rotate(20 {cx+118} {cy-52})"/>')
    P.append(f'<rect x="{cx+294}" y="{cy-118}" width="13" height="13" fill="#D4A74A" '
             f'transform="rotate(-18 {cx+300} {cy-112})"/>')

    # 旅行者 1/2 号: 继续往外, 虚线
    P.append(f'<path d="M {cx+300} {cy-112} L {cx+430} {cy-140} L {cx+560} {cy-160} '
             f'L {cx+700} {cy-172}" fill="none" stroke="#E8E4DA" stroke-width="3" '
             f'stroke-linecap="round" stroke-dasharray="12 10" opacity="0.85"/>')
    P.append(f'<circle cx="{cx+700}" cy="{cy-172}" r="10" fill="#E8E4DA"/>')
    P.append(f'<circle cx="{cx+700}" cy="{cy-172}" r="20" fill="none" stroke="#E8E4DA" '
             f'stroke-width="2" opacity="0.4"/>')

    # 标注
    for name, r, pr, col in orbs:
        ry = r * 0.42
        P.append(f'<text x="{cx + r*0.72:.0f}" y="{cy - ry - 8:.0f}" fill="{col}" '
                 f'font-size="13" opacity="0.95" font-family="Microsoft YaHei,sans-serif">{name}</text>')

    P.append(f'<g><rect x="{cx+300}" y="{cy-152}" width="15" height="15" fill="#D4A74A"/>'
             f'<text x="{cx+322}" y="{cy-138}" fill="#D4A74A" font-size="16" font-weight="700" '
             f'font-family="Microsoft YaHei,sans-serif">先驱者</text>'
             f'<text x="{cx+322}" y="{cy-120}" fill="#8A8578" font-size="12" '
             f'font-family="Microsoft YaHei,sans-serif">推门者 · 已失联</text></g>')
    P.append(f'<g><circle cx="{cx+700}" cy="{cy-172}" r="9" fill="#E8E4DA"/>'
             f'<text x="{cx+716}" y="{cy-168}" fill="#E8E4DA" font-size="16" font-weight="700" '
             f'font-family="Microsoft YaHei,sans-serif">旅行者</text>'
             f'<text x="{cx+716}" y="{cy-150}" fill="#8A8578" font-size="12" '
             f'font-family="Microsoft YaHei,sans-serif">仍在发信号</text></g>')

    return (f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'xmlns="http://www.w3.org/2000/svg">' + "".join(P) + '</svg>')


if __name__ == "__main__":
    print(solar_svg()[:400])
    print("... len =", len(solar_svg()))
