# -*- coding: utf-8 -*-
"""ctc_palette.py — 中国传统色配色速查（v1.0）

★ 数据源：references/ctc_colors.json（本书 71 色：47 传统色 + 24 节气色）
★ 色值口径：HEX/RGB/CMYK 为公开传统色通行值（郭浩《传统色》系），**非本书载值**；
  本书每色附自有 CMYK/RGB，载值待实体书/色卡校准（lib 中 pending_book_value=true）
用法:
    python ctc_palette.py list [族]
    python ctc_palette.py search 关键词
    python ctc_palette.py scene 场景关键词
    python ctc_palette.py term 节气名
"""
import io, os, sys, json

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, "..", "references", "ctc_colors.json")

# 场景 → 主 / 辅 / 点 三色（60% / 30% / 10%）+ 朝代 + 禁忌
SCENES = {
 "喜庆":   (["朱红", "大红"], ["琉璃黄", "杏黄"], ["玄色", "漆黑"], "明", "朱红+琉璃黄同屏时，明度差需 >30%，否则糊成一片"),
 "春节":   (["朱红", "大红"], ["琉璃黄"], ["玄色"], "明", "红金比例 7:3，金色只做点缀不超过 10%"),
 "中秋":   (["月白", "铅白"], ["玄色", "鸦青"], ["杏黄"], "明", "月白作底时，正文用玄色不用纯黑，避免死板"),
 "婚嫁":   (["胭脂红", "海棠红"], ["茜色"], ["月白"], "明", "海棠红与胭脂红明度接近，二选一不做主辅"),
 "高端中式": (["玄色", "紫檀"], ["墨色"], ["琉璃黄"], "清", "金只作点缀（<10%），否则变土豪金"),
 "禅意":   (["青莲", "鸦青"], ["荼白", "鸭卵青"], ["玄色"], "唐", "青莲与鸭卵青同属青，明度差需 >20%"),
 "文人":   (["竹青", "松花"], ["月白", "缃黄"], ["鸦青"], "宋", "不要用大红大绿直接压文人色"),
 "现代东方": (["群青", "黛蓝"], ["月白"], ["朱红"], "清", "东方感靠青系，不用描金加云纹那套"),
 "酒店大堂": (["紫檀", "玄色"], ["琉璃黄"], ["月白"], "明", "大面积极用暗色，金色留灯饰与标识"),
 "文创":   (["朱红", "青莲"], ["月白"], ["琉璃黄"], "明", "同一套色做不同 SKU 时只换明度不改色相"),
 "节气":   (["月白", "玄色"], ["鸦青"], ["杏黄"], "宋", "节气色须一节气一色，不混用"),
}
TERM_SEASON = {
 "春": (["柳绿", "松花", "青白"], "木·东·生发"),
 "夏": (["朱红", "海棠红", "碧色"], "火·南·热烈"),
 "秋": (["杏黄", "黄栌", "缃色"], "土·中·丰收"),
 "冬": (["玄色", "月白", "鸦青"], "水·北·收藏"),
}
WUXING = {"青": ("木", "东", "春", "生发"), "赤": ("火", "南", "夏", "热烈"),
          "黄": ("土", "中", "长夏", "中正"), "白": ("金", "西", "秋", "洁净"),
          "黑": ("水", "北", "冬", "玄远")}


def load():
    with open(LIB, encoding="utf-8") as f:
        return json.load(f)


def fmt(c):
    if not c or not c.get("hex") or not c.get("rgb") or not c.get("cmyk"):
        return "  （载值待校准：本书色值未取得 / 公开数据集未收录）"
    r = c["rgb"]; k = c["cmyk"]
    return "  HEX %s ｜ RGB(%d,%d,%d) ｜ CMYK(%d,%d,%d,%d)" % (
        c["hex"], r[0], r[1], r[2], k[0], k[1], k[2], k[3])


def show(lib, c, tag=""):
    print("  %-6s %s" % (c["name"], c["meaning"]))
    print("        " + fmt(c))
    if c.get("family") in WUXING:
        w = WUXING[c["family"]]
        print("        五行 %s ｜ 五方 %s ｜ 五季 %s ｜ 意象 %s" % w)
    if c.get("season"):
        print("        节气 %s" % c["season"])
    if tag:
        print("        %s" % tag)


def main():
    lib = load()
    cols = lib["colors"]
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    arg = sys.argv[2] if len(sys.argv) > 2 else ""

    if cmd == "list":
        if arg:
            rows = [c for c in cols if c["family"] == arg or arg in c["family"]]
            if not rows:
                print("无该族：%s" % arg)
                print("可用族：%s" % "、".join(sorted({c["family"] for c in cols})))
                return
            print("== %s（%d）==" % (arg, len(rows)))
            for c in rows:
                print("  %-8s %s" % (c["name"], (c["hex"] or "pending")))
            print()
            return
        fams = sorted({c["family"] for c in cols})
        for fam in fams:
            rows = [c for c in cols if c["family"] == fam]
            print("== %s（%d）==" % (fam, len(rows)))
            for c in rows:
                print("  %-8s %s" % (c["name"], (c["hex"] or "pending")))
            print()
    elif cmd == "search":
        rows = [c for c in cols if arg in c["name"] or arg in c["meaning"] or arg in c["family"]]
        print("命中 %d 条：" % len(rows))
        for c in rows:
            show(lib, c)
    elif cmd == "term":
        rows = [c for c in cols if c["name"] == arg]
        if not rows:
            print("未找到节气：%s" % arg)
            return
        c = rows[0]
        print("节气色：%s" % arg)
        show(lib, c, "★ 本书第八章每节气一页一色；载值待校准，下列公开通行值仅供占位")
        s = TERM_SEASON.get(c.get("season"))
        if s:
            print("  同季备选（推演，非本书载色）：%s" % "、".join(s[0]))
            print("  季节五行：%s" % s[1])
    elif cmd == "scene":
        key = None
        for k in SCENES:
            if k in arg:
                key = k
                break
        if not key:
            print("可用场景：%s" % "、".join(SCENES.keys()))
            return
        main_c, sub_c, acc_c, dyn, forbid = SCENES[key]
        print("场景：%s" % key)
        print("  朝代基调：%s" % dyn)
        for label, names in (("主色 60%", main_c), ("辅色 30%", sub_c), ("点缀 10%", acc_c)):
            for n in names:
                hit = [c for c in cols if c["name"] == n]
                if hit:
                    show(lib, hit[0], label)
        print("  禁忌/纪律：%s" % forbid)
        print("  配套通用方法：场景→类别→方案（见《拯救你的配色》内化），本表只给色名层")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
