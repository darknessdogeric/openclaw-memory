r"""
安逸集团公文生成器 v2.0 (python-docx 版)
==========================================
**替代** 手拼 XML 的旧版本 (anyi_gongwen_docx.py v1.0)
**标准** GB/T 9704-2012 公文格式
**依赖** python-docx 1.2.0（已装）

用法:
    from anyi_reports.docx_gongwen import GongwenDoc

    doc = GongwenDoc(title='安逸集团新媒体矩阵方案',
                     author='张实（Eric）',
                     date='2026-10-02')
    doc.h1('一、战略定位')
    doc.body('这是正文段落，会自动首行缩进 2 字符。')
    doc.h2('（一）我们是谁')
    doc.bullet('列表项')
    doc.table(headers=['列1','列2'], rows=[['a','b'],['c','d']])
    doc.signature('安逸酒店集团产业发展部')
    doc.save(r'C:\Users\ericz\Desktop\out.docx')

GB/T 9704 参数（内置，勿改）:
- A4: 21×29.7cm
- 边距: 上37mm 下35mm 左28mm 右26mm
- 正文: 仿宋_GB2312 三号(16pt), 固定行距28pt, 首行缩进2字符
- 一级标题: 黑体 三号(16pt)
- 二级标题: 黑体 三号(16pt)
- 标题: 方正小标宋简体 二号(22pt)
- 页码: 宋体 四号(14pt), -X- 格式
"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Emu
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from pathlib import Path
import datetime

# ===== GB/T 9704 标准参数 =====
GB = {
    'page_w': Cm(21.0), 'page_h': Cm(29.7),
    'margin_top': Cm(3.7), 'margin_bottom': Cm(3.5),
    'margin_left': Cm(2.8), 'margin_right': Cm(2.6),
    'body_font': '仿宋_GB2312', 'body_size': Pt(16),
    'h_font': '黑体', 'h_size': Pt(16),
    'title_font': '方正小标宋简体', 'title_size': Pt(22),
    'line_spacing': Pt(28),
    'first_indent': Pt(32),   # 2 chars @16pt
    'page_num_font': '宋体', 'page_num_size': Pt(14),
}


class GongwenDoc:
    """安逸集团公文文档构建器"""

    def __init__(self, title='', author='张实（Eric）', date=None):
        self.doc = Document()
        self.title_text = title
        self.author = author
        self.date = date or datetime.date.today().isoformat()
        self._setup_page()
        if title:
            self._add_title(title)

    def _setup_page(self):
        sec = self.doc.sections[0]
        sec.page_width = GB['page_w']
        sec.page_height = GB['page_h']
        sec.top_margin = GB['margin_top']
        sec.bottom_margin = GB['margin_bottom']
        sec.left_margin = GB['margin_left']
        sec.right_margin = GB['margin_right']

    def _set_cn_font(self, run, font_name, size):
        """设置中文字体（含 eastAsia）"""
        run.font.size = size
        run.font.name = 'Times New Roman'
        rpr = run._element.get_or_add_rPr()
        rfonts = rpr.find(qn('w:rFonts'))
        if rfonts is None:
            rfonts = OxmlElement('w:rFonts')
            rpr.append(rfonts)
        rfonts.set(qn('w:eastAsia'), font_name)
        rfonts.set(qn('w:ascii'), font_name)
        rfonts.set(qn('w:hAnsi'), font_name)

    def _fixed_line(self, para):
        pf = para.paragraph_format
        pf.line_spacing = GB['line_spacing']
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY

    def _add_title(self, text):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        self._fixed_line(p)
        run = p.add_run(text)
        self._set_cn_font(run, GB['title_font'], GB['title_size'])
        run.bold = True
        return p

    def h1(self, text):
        """一级标题（黑体 三号）"""
        p = self.doc.add_paragraph()
        self._fixed_line(p)
        run = p.add_run(text)
        self._set_cn_font(run, GB['h_font'], GB['h_size'])
        run.bold = True
        # 大纲级别 0（供 TOC 用）
        self._set_outline(p, 0)
        return p

    def h2(self, text):
        """二级标题（黑体 三号）"""
        p = self.doc.add_paragraph()
        self._fixed_line(p)
        run = p.add_run(text)
        self._set_cn_font(run, GB['h_font'], GB['h_size'])
        run.bold = True
        self._set_outline(p, 1)
        return p

    def h3(self, text):
        """三级标题（黑体 三号）"""
        p = self.doc.add_paragraph()
        self._fixed_line(p)
        run = p.add_run(text)
        self._set_cn_font(run, GB['h_font'], GB['h_size'])
        run.bold = True
        self._set_outline(p, 2)
        return p

    def _set_outline(self, para, level):
        ppr = para._element.get_or_add_pPr()
        ol = OxmlElement('w:outlineLvl')
        ol.set(qn('w:val'), str(level))
        ppr.append(ol)

    def body(self, text, indent=True):
        """正文（仿宋 三号, 固定行距 28pt, 首行缩进2字符）"""
        p = self.doc.add_paragraph()
        self._fixed_line(p)
        if indent:
            p.paragraph_format.first_line_indent = GB['first_indent']
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = p.add_run(text)
        self._set_cn_font(run, GB['body_font'], GB['body_size'])
        return p

    def bullet(self, text):
        """列表项（用破折号前缀，不用符号）"""
        return self.body('— ' + text)

    def table(self, headers, rows, caption=None):
        """三线表（GB/T 9704 公文标准）"""
        if caption:
            cp = self.doc.add_paragraph()
            self._fixed_line(cp)
            cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = cp.add_run(caption)
            self._set_cn_font(r, GB['body_font'], Pt(14))
            r.bold = True

        t = self.doc.add_table(rows=1 + len(rows), cols=len(headers))
        t.alignment = WD_TABLE_ALIGNMENT.CENTER

        # 表头
        for i, h in enumerate(headers):
            cell = t.cell(0, i)
            cell.text = ''
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            self._fixed_line(p)
            r = p.add_run(str(h))
            self._set_cn_font(r, GB['body_font'], Pt(14))
            r.bold = True
        # 数据
        for ri, row in enumerate(rows, start=1):
            for ci, val in enumerate(row):
                cell = t.cell(ri, ci)
                cell.text = ''
                p = cell.paragraphs[0]
                self._fixed_line(p)
                r = p.add_run(str(val))
                self._set_cn_font(r, GB['body_font'], Pt(14))

        # 三线表边框（顶/底 1.5pt；表头下 0.75pt；无竖线）
        self._apply_three_line(t)
        return t

    def _apply_three_line(self, table):
        tbl = table._tbl
        tblPr = tbl.tblPr
        borders = OxmlElement('w:tblBorders')
        for edge, sz in [('top', 12), ('bottom', 12), ('left', 0), ('right', 0),
                         ('insideH', 0), ('insideV', 0)]:
            e = OxmlElement(f'w:{edge}')
            if sz == 0:
                e.set(qn('w:val'), 'none')
                e.set(qn('w:sz'), '0')
            else:
                e.set(qn('w:val'), 'single')
                e.set(qn('w:sz'), str(sz))
                e.set(qn('w:color'), '000000')
            borders.append(e)
        tblPr.append(borders)

        # 表头行下边框
        if len(table.rows) > 0:
            hdr = table.rows[0]
            for cell in hdr.cells:
                tcPr = cell._tc.get_or_add_tcPr()
                cb = OxmlElement('w:tcBorders')
                bottom = OxmlElement('w:bottom')
                bottom.set(qn('w:val'), 'single')
                bottom.set(qn('w:sz'), '6')
                bottom.set(qn('w:color'), '000000')
                cb.append(bottom)
                tcPr.append(cb)

    def signature(self, unit, date=None):
        """落款（单位 + 日期，右对齐）"""
        d = date or self.date
        p1 = self.doc.add_paragraph()
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        self._fixed_line(p1)
        r1 = p1.add_run(unit)
        self._set_cn_font(r1, GB['body_font'], GB['body_size'])
        p2 = self.doc.add_paragraph()
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        self._fixed_line(p2)
        r2 = p2.add_run(d)
        self._set_cn_font(r2, GB['body_font'], GB['body_size'])

    def save(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.doc.save(path)
        return Path(path).stat().st_size


# ===== 便捷函数：从 markdown-ish sections 一步生成 =====
def build_from_sections(title, sections, output_path, author='张实（Eric）', date=None):
    """
    sections: [(level, text)]
      level: 1=标题(不用于此处) 2=一级 3=二级 4=三级 0=正文
    """
    doc = GongwenDoc(title=title, author=author, date=date)
    for item in sections:
        level, text = item[0], item[1]
        extra = item[2] if len(item) > 2 else None
        if level == 0:
            doc.body(text)
        elif level == 2:
            doc.h1(text)
        elif level == 3:
            doc.h2(text)
        elif level == 4:
            doc.h3(text)
        elif level == 5 and extra:
            doc.table(headers=extra['headers'], rows=extra['rows'],
                      caption=extra.get('caption'))
    return doc.save(output_path)


if __name__ == '__main__':
    # 自测
    out = r'D:\B166ER-OpenClaw\workspace\toolbox\.tmp\test_gongwen_v2.docx'
    d = GongwenDoc(title='安逸集团公文生成器自测', author='张实（Eric）')
    d.h1('一、测试章节')
    d.body('这是正文段落，用于验证 GB/T 9704 公文格式：仿宋_GB2312 三号（16pt），固定行距 28 磅，首行缩进 2 字符。')
    d.h2('（一）表格测试')
    d.table(headers=['项目', '数值', '备注'],
            rows=[['营收', '6.5亿', '2025年'], ['利润', '-6843万', '2025年']],
            caption='表1 测试三线表')
    d.body('表格后正文。')
    d.signature('安逸酒店集团产业发展部', '2026年10月2日')
    size = d.save(out)
    print(f'[OK] {out}')
    print(f'  size: {size:,} bytes')
    print(f'  标准: GB/T 9704-2012')
    print(f'  依赖: python-docx 1.2.0')
