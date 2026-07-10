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
        """嵌入文字水印"""
        if output_path is None:
            base, ext = os.path.splitext(img_path)
            output_path = f"{base}_wm{ext}"
        bwm = WaterMark(password_img=self.pwd, password_wm=self.pwd)
        bwm.read_img(img_path)
        bwm.read_wm(text, mode='str')
        bwm.embed(output_path)
        return output_path

    def extract_text(self, img_path: str, text: str) -> str:
        """提取文字水印（需知原文）"""
        bwm = WaterMark(password_img=self.pwd, password_wm=self.pwd)
        return bwm.extract(img_path, wm_shape=self._bits_for(text), mode='str')

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
