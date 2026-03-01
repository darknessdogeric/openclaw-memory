#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown to PDF Converter using FPDF2
"""

import re
import os
import sys
from pathlib import Path

# Check and install fpdf2 if needed
try:
    from fpdf import FPDF
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fpdf2"])
    from fpdf import FPDF

class MarkdownPDFConverter:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()
        
        # Add Unicode fonts
        try:
            # Try to use system fonts with Chinese support
            self.pdf.add_font('NotoSansCJK', '', 'C:\\Windows\\Fonts\\msyh.ttc', uni=True)
            self.pdf.add_font('NotoSansCJK', 'B', 'C:\\Windows\\Fonts\\msyhbd.ttc', uni=True)
            self.default_font = 'NotoSansCJK'
        except:
            # Fallback to built-in
            self.default_font = 'Arial'
        
    def parse_markdown(self, content):
        """Parse markdown content into structured elements"""
        elements = []
        lines = content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Code blocks
            if line.strip().startswith('```'):
                code_lines = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                elements.append(('code', '\n'.join(code_lines)))
                i += 1
                continue
            
            # Tables
            if '|' in line and i + 1 < len(lines) and '---' in lines[i + 1]:
                table_lines = [line]
                i += 1
                while i < len(lines) and '|' in lines[i]:
                    table_lines.append(lines[i])
                    i += 1
                elements.append(('table', table_lines))
                continue
            
            # Headers
            if line.startswith('# '):
                elements.append(('h1', line[2:]))
            elif line.startswith('## '):
                elements.append(('h2', line[3:]))
            elif line.startswith('### '):
                elements.append(('h3', line[4:]))
            elif line.startswith('#### '):
                elements.append(('h4', line[5:]))
            elif line.startswith('##### '):
                elements.append(('h5', line[6:]))
            # Lists
            elif line.strip().startswith('- ') or line.strip().startswith('* '):
                elements.append(('bullet', line.strip()[2:]))
            elif re.match(r'^\d+\.\s', line.strip()):
                elements.append(('number', re.sub(r'^\d+\.\s', '', line.strip())))
            # Blockquote
            elif line.strip().startswith('> '):
                elements.append(('quote', line.strip()[2:]))
            # Horizontal rule
            elif line.strip() == '---' or line.strip() == '***':
                elements.append(('hr', ''))
            # Empty line
            elif not line.strip():
                elements.append(('empty', ''))
            # Regular paragraph
            else:
                # Check if it's a continuation of previous paragraph
                if elements and elements[-1][0] == 'paragraph':
                    elements[-1] = ('paragraph', elements[-1][1] + ' ' + line.strip())
                else:
                    elements.append(('paragraph', line.strip()))
            
            i += 1
        
        return elements
    
    def render_elements(self, elements):
        """Render parsed elements to PDF"""
        for elem_type, content in elements:
            if elem_type == 'h1':
                self.pdf.set_font(self.default_font, 'B', 20)
                self.pdf.ln(5)
                self.pdf.cell(0, 12, content, ln=True)
                self.pdf.ln(3)
            
            elif elem_type == 'h2':
                self.pdf.set_font(self.default_font, 'B', 16)
                self.pdf.ln(5)
                self.pdf.cell(0, 10, content, ln=True)
                self.pdf.ln(2)
            
            elif elem_type == 'h3':
                self.pdf.set_font(self.default_font, 'B', 13)
                self.pdf.ln(4)
                self.pdf.cell(0, 8, content, ln=True)
                self.pdf.ln(1)
            
            elif elem_type == 'h4':
                self.pdf.set_font(self.default_font, 'B', 11)
                self.pdf.ln(3)
                self.pdf.cell(0, 7, content, ln=True)
            
            elif elem_type == 'h5':
                self.pdf.set_font(self.default_font, 'B', 10)
                self.pdf.cell(0, 6, content, ln=True)
            
            elif elem_type == 'paragraph':
                self.pdf.set_font(self.default_font, '', 10)
                # Handle bold and italic
                content = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', content)  # Remove markdown
                content = re.sub(r'\*\*(.+?)\*\*', r'\1', content)
                content = re.sub(r'\*(.+?)\*', r'\1', content)
                content = re.sub(r'`(.+?)`', r'\1', content)
                self.pdf.multi_cell(0, 6, content)
                self.pdf.ln(1)
            
            elif elem_type == 'bullet':
                self.pdf.set_font(self.default_font, '', 10)
                self.pdf.cell(5, 6, '', ln=0)  # indent
                self.pdf.cell(5, 6, chr(149), ln=0)  # bullet
                self.pdf.multi_cell(0, 6, ' ' + content)
            
            elif elem_type == 'number':
                self.pdf.set_font(self.default_font, '', 10)
                self.pdf.cell(5, 6, '', ln=0)
                self.pdf.multi_cell(0, 6, content)
            
            elif elem_type == 'quote':
                self.pdf.set_font(self.default_font, 'I', 10)
                self.pdf.set_fill_color(240, 240, 240)
                self.pdf.cell(5, 6, '', ln=0)
                self.pdf.multi_cell(0, 6, content, fill=True)
                self.pdf.ln(1)
            
            elif elem_type == 'code':
                self.pdf.set_font('Courier', '', 9)
                self.pdf.set_fill_color(245, 245, 245)
                self.pdf.multi_cell(0, 5, content, fill=True)
                self.pdf.ln(2)
            
            elif elem_type == 'table':
                self.render_table(content)
            
            elif elem_type == 'hr':
                self.pdf.line(10, self.pdf.get_y(), 200, self.pdf.get_y())
                self.pdf.ln(3)
            
            elif elem_type == 'empty':
                if self.pdf.get_y() < 270:  # Avoid page break on empty line
                    self.pdf.ln(2)
    
    def render_table(self, table_lines):
        """Render markdown table"""
        if len(table_lines) < 2:
            return
        
        # Parse header
        headers = [cell.strip() for cell in table_lines[0].split('|') if cell.strip()]
        
        # Skip separator line
        rows = []
        for line in table_lines[2:]:
            cells = [cell.strip() for cell in line.split('|') if cell.strip()]
            if cells:
                rows.append(cells)
        
        if not headers or not rows:
            return
        
        # Calculate column widths
        col_count = len(headers)
        page_width = 190  # A4 width minus margins
        col_width = page_width / col_count
        
        # Render table
        self.pdf.set_font(self.default_font, 'B', 9)
        
        # Header
        for header in headers:
            self.pdf.cell(col_width, 7, header[:20], border=1, ln=0)
        self.pdf.ln()
        
        # Rows
        self.pdf.set_font(self.default_font, '', 8)
        for row in rows:
            for cell in row:
                # Clean markdown from cell
                cell = re.sub(r'\*\*(.+?)\*\*', r'\1', cell)
                cell = re.sub(r'`(.+?)`', r'\1', cell)
                self.pdf.cell(col_width, 6, cell[:25], border=1, ln=0)
            self.pdf.ln()
        
        self.pdf.ln(3)
    
    def convert(self, input_path, output_path):
        """Convert markdown file to PDF"""
        print(f"Reading: {input_path}")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("Parsing markdown...")
        elements = self.parse_markdown(content)
        
        print(f"Rendering {len(elements)} elements...")
        self.render_elements(elements)
        
        print(f"Saving: {output_path}")
        self.pdf.output(output_path)
        
        print("Done!")
        return output_path


if __name__ == '__main__':
    input_file = r"C:\Users\Administrator\Desktop\张实项目总控\06-AHL-去中心化旅行平台\AHL通用产品方案_V3_专业版.md"
    output_file = r"C:\Users\Administrator\Desktop\张实项目总控\06-AHL-去中心化旅行平台\AHL通用产品方案_V3_专业版.pdf"
    
    converter = MarkdownPDFConverter()
    converter.convert(input_file, output_file)
