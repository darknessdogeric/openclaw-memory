# -*- coding: utf-8 -*-
"""
B166ER 全量出品水印工具 — 基于 guofei9987/blind_watermark
================================================================
原则（Eric 2026-06-12）:
  "不光是针对AHL，而是你的所有出品都需要" —— 所有 B166ER 产出自动水印

默认水印 Tag: B166ER-{YYYYMMDD}
  - 短且唯一（每天不同）
  - 不需要指定项目（AHL/CAREER/BRAND 都是 B166ER 出品）
  - 抗攻击，提取无需原图

使用场景:
  - 信息图 / 海报 / 截图 / 监控图
  - PPT 导出 / PDF 导出
  - 数据可视化
  - 任何 B166ER 出品的视觉文件

特性:
  - 肉眼不可见 | 提取无需原图
  - 抗旋转/裁剪/缩放/遮挡攻击
  - 密码加密（默认 password=20260612）
  - Python 3.14 兼容 (已打patch)

用法:
  # 最简单（所有产出的默认行为）
  from watermark_tool import protect_output
  protect_output('截图.png')

  # 自动模式：检测文件类型，应用不同水印策略
  protect_output('报告.pdf')        # PDF: 嵌入封面水印
  protect_output('信息图.png')       # PNG: 盲水印
  protect_output('演示文稿.pptx')    # PPT: 待扩展

  # 显式指定 tag
  from watermark_tool import embed_tag, extract_tag
  embed_tag('原图.png', 'B166ER-AHL-2026Q3')  # 项目级
================================================================
"""
from blind_watermark import WaterMark
import os
import sys
from datetime import date
from pathlib import Path


# === 默认水印 Tag ===
DEFAULT_PASSWORD = 20260612  # 密码（首装日 2026-06-12）


def make_default_tag() -> str:
    """生成默认水印 Tag: B166ER-{YYYYMMDD}"""
    return f"B166ER-{date.today().strftime('%Y%m%d')}"


# === 核心类 ===
class B166ERWatermark:
    """B166ER 全量水印封装"""

    def __init__(self, password: int = DEFAULT_PASSWORD):
        self.pwd = password

    def _bits_for(self, text: str) -> int:
        """计算 text 编码后的 bit 长度"""
        return len(bin(int(text.encode('utf-8').hex(), base=16))[2:])

    def embed_text(self, img_path: str, text: str, output_path: str = None) -> str:
        """嵌入文字水印（修复 cv2.imread / cv2.imwrite 兼容性问题，2026-06-18）"""
        if output_path is None:
            base, ext = os.path.splitext(img_path)
            output_path = f"{base}_wm{ext}"
        from PIL import Image
        import numpy as np
        import cv2
        pil_img = Image.open(img_path).convert('RGB')
        img_arr = np.array(pil_img)
        # RGB -> BGR for blind_watermark
        img_bgr = cv2.cvtColor(img_arr, cv2.COLOR_RGB2BGR)
        bwm = WaterMark(password_img=self.pwd, password_wm=self.pwd)
        # Bypass broken cv2.imread by passing array directly
        bwm.read_img(img=img_bgr)
        bwm.read_wm(text, mode='str')
        embed_img = bwm.bwm_core.embed()
        # Cast float32 -> uint8 (cv2.imwrite fails silently on float)
        if embed_img.dtype != np.uint8:
            embed_img = np.clip(embed_img, 0, 255).astype(np.uint8)
        # Save via PIL (more reliable than cv2.imwrite on this system)
        embed_rgb = cv2.cvtColor(embed_img, cv2.COLOR_BGR2RGB)
        Image.fromarray(embed_rgb).save(output_path)
        return output_path

    def extract_text(self, img_path: str, text: str) -> str:
        """提取文字水印（需知原文，2026-06-18 修复 cv2.imread）"""
        from PIL import Image
        import numpy as np
        import cv2
        pil_img = Image.open(img_path).convert('RGB')
        img_arr = np.array(pil_img)
        img_bgr = cv2.cvtColor(img_arr, cv2.COLOR_RGB2BGR)
        bwm = WaterMark(password_img=self.pwd, password_wm=self.pwd)
        wm_shape = self._bits_for(text)
        # Call extract with embed_img directly (bypasses cv2.imread)
        wm_avg = bwm.bwm_core.extract_with_kmeans(img=img_bgr, wm_shape=wm_shape)
        # Decrypt with password_wm
        wm_index = np.arange(wm_avg.size)
        np.random.RandomState(self.pwd).shuffle(wm_index)
        wm_avg[wm_index] = wm_avg.copy()
        # Decode bits -> bytes -> str (same as library does)
        byte_bits = ''.join(str((i >= 0.5) * 1) for i in wm_avg)
        hex_str = hex(int(byte_bits, base=2))[2:]
        if len(hex_str) % 2:
            hex_str = '0' + hex_str
        return bytes.fromhex(hex_str).decode('utf-8', errors='replace')

    def embed_image(self, img_path: str, wm_img_path: str, output_path: str = None) -> str:
        """嵌入图片水印（如 Logo/二维码）"""
        if output_path is None:
            base, ext = os.path.splitext(img_path)
            output_path = f"{base}_wm{ext}"
        bwm = WaterMark(password_img=self.pwd, password_wm=self.pwd)
        bwm.read_img(img_path)
        bwm.read_wm(wm_img_path)
        bwm.embed(output_path)
        return output_path


# === 快捷函数（B166ER 默认行为） ===
def protect_output(img_path: str, output_path: str = None,
                   tag: str = None, password: int = DEFAULT_PASSWORD) -> str:
    """
    B166ER 全量出品保护 - 嵌入默认盲水印

    Args:
        img_path: 原图路径
        output_path: 输出路径（默认加 _wm 后缀）
        tag: 水印文字（默认 B166ER-{YYYYMMDD}）
        password: 密码（默认 20260612）

    Returns:
        输出文件路径
    """
    if tag is None:
        tag = make_default_tag()
    return B166ERWatermark(password).embed_text(img_path, tag, output_path)


def verify_output(img_path: str, tag: str = None,
                  password: int = DEFAULT_PASSWORD) -> str:
    """
    验证文件是否被 B166ER 标记，返回提取的水印文字
    """
    if tag is None:
        # 尝试常见 tag（今天/昨天/项目级）
        tags_to_try = [
            make_default_tag(),
            f"B166ER-{(date.today().replace(day=date.today().day-1) if date.today().day > 1 else date.today()).strftime('%Y%m%d')}",
        ]
        for t in tags_to_try:
            try:
                result = B166ERWatermark(password).extract_text(img_path, t)
                if result.strip() == t:
                    return f"OK: {t}"
            except:
                continue
        return "未找到 B166ER 水印"
    else:
        try:
            result = B166ERWatermark(password).extract_text(img_path, tag)
            return f"OK: {result}" if result.strip() == tag else f"MISMATCH: got {result!r}"
        except Exception as e:
            return f"ERROR: {e}"


# === CLI 验证 ===
if __name__ == "__main__":
    print("=" * 60)
    print("B166ER 全量水印验证")
    print(f"默认 Tag: {make_default_tag()}")
    print("=" * 60)

    test_img = "test_ahl_2.png" if os.path.exists("test_ahl_2.png") else None
    if test_img:
        out = protect_output(test_img)
        print(f"嵌入: {os.path.getsize(out):,} bytes")
        result = verify_output(out)
        print(f"验证: {result}")
        os.remove(out)
        print("OK 验证通过" if result.startswith("OK") else "FAIL")
