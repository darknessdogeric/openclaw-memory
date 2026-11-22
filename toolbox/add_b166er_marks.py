"""Add B166ER mark to every slide of 4 PPT files"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pathlib import Path
import copy

# ===== Configuration =====
PPT_DIR = Path(r"C:\Users\ericz\Desktop\产业发展部人事\培训资料")

# All 4 PPT files
PPT_FILES = [
    "【Edit】PPT_ 实战案例：成功+失败.pptx",
    "【Edit】PPT_ 酒店行业速查表 · 核心概念.pptx",
    "【Edit】PPT_ 酒店行业专业培训手册.pptx",
    "【Edit】PPT_ 深度专题三：5 大国际酒店集团品牌矩阵.pptx",
]

# B标 position (bottom-right corner) - same on every slide
B_MARK_LEFT   = Emu(10_900_000)   # ~11.91" from left
B_MARK_TOP    = Emu(6_640_000)    # ~7.26" from top (about 0.24" from bottom)
B_MARK_WIDTH  = Emu(1_100_000)    # ~1.20" wide
B_MARK_HEIGHT = Emu(180_000)     # ~0.20" tall

# Colors (B166ER brand red dot)
RED_COLOR  = RGBColor(0xD6, 0x28, 0x28)  # B166ER red
GRAY_COLOR = RGBColor(0x9A, 0x9A, 0x9A)  # gray for text


def add_b166er_mark(slide, slide_width, slide_height, idx):
    """Add a small B166ER brand mark to a slide."""
    # Adjust position to bottom-right with margin
    margin_right = Emu(80_000)   # ~0.09" from right
    margin_bottom = Emu(50_000)  # ~0.05" from bottom

    # Position: bottom-right corner
    left   = slide_width  - B_MARK_WIDTH  - margin_right
    top    = slide_height - B_MARK_HEIGHT - margin_bottom
    width  = B_MARK_WIDTH
    height = B_MARK_HEIGHT

    # Create text box
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = False
    tf.margin_left = Emu(0)
    tf.margin_right = Emu(0)
    tf.margin_top = Emu(0)
    tf.margin_bottom = Emu(0)

    # First paragraph: red dot + space + B166ER text
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT

    # Run 1: red dot
    r1 = p.add_run()
    r1.text = "●"
    r1.font.name = "Microsoft YaHei"
    r1.font.size = Pt(12)
    r1.font.bold = True
    r1.font.color.rgb = RED_COLOR

    # Run 2: space + "B166ER"
    r2 = p.add_run()
    r2.text = " B166ER"
    r2.font.name = "Microsoft YaHei"
    r2.font.size = Pt(10)
    r2.font.bold = True
    r2.font.color.rgb = GRAY_COLOR

    return tb


def process_ppt(path: Path):
    """Process a single PPT file: add B166ER mark to every slide."""
    print(f"\n{'='*60}")
    print(f"处理: {path.name}")
    print(f"路径: {path}")
    print(f"大小: {path.stat().st_size:,} bytes")
    print(f"{'='*60}")

    prs = Presentation(str(path))
    slide_w, slide_h = prs.slide_width, prs.slide_height
    print(f"幻灯片数: {len(prs.slides)}")
    print(f"页面尺寸: {Emu(slide_w).inches:.2f}\" x {Emu(slide_h).inches:.2f}\"")

    # Add B标 to every slide
    for i, slide in enumerate(prs.slides, 1):
        # Check if slide already has B166ER mark
        has_b = False
        for shape in slide.shapes:
            if shape.has_text_frame and 'B166ER' in shape.text_frame.text:
                has_b = True
                break

        # Add B标 (even if exists - so it's consistent across all slides)
        add_b166er_mark(slide, slide_w, slide_h, i)
        marker = "(已有B标，新加底部版)" if has_b else "(新增)"
        print(f"  Slide {i:2d}: [OK] {marker}")

    # Save (overwrite original - Eric explicitly said the PPTs themselves)
    prs.save(str(path))
    print(f"[OK] 保存: {path}")


def main():
    print("\n" + "="*60)
    print("B166ER 品牌标识批量添加工具")
    print("="*60)

    for fname in PPT_FILES:
        fpath = PPT_DIR / fname
        if not fpath.exists():
            print(f"⚠️ 文件不存在: {fpath}")
            continue
        process_ppt(fpath)

    print("\n" + "="*60)
    print("[OK] 全部完成")
    print("="*60)


if __name__ == "__main__":
    main()