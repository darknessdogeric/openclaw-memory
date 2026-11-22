import sys, zipfile, os, io, glob
from xml.etree import ElementTree as ET

NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

def docx_text(path):
    try:
        with zipfile.ZipFile(path) as z:
            xml = z.read('word/document.xml')
    except Exception as e:
        return f"[ERR] {e}"
    root = ET.fromstring(xml)
    out = []
    body = root.find(NS + 'body')
    if body is None:
        return "[ERR] no body"
    def walk(el):
        for child in el:
            tag = child.tag
            if tag == NS + 'p':
                buf = ''.join(t.text or '' for t in child.iter(NS + 't')).strip()
                if buf:
                    out.append(buf)
            elif tag == NS + 'tbl':
                out.append('[TABLE]')
                for tr in child.findall(NS + 'tr'):
                    cells = []
                    for tc in tr.findall(NS + 'tc'):
                        ct = ''.join(t.text or '' for t in tc.iter(NS + 't')).strip()
                        cells.append(ct.replace('\n', ' '))
                    out.append(' | '.join(cells))
                out.append('[/TABLE]')
            else:
                walk(child)
    walk(body)
    return '\n'.join(out)

if __name__ == '__main__':
    outdir = sys.argv[1]
    files = sys.argv[2:]
    os.makedirs(outdir, exist_ok=True)
    log = []
    for f in files:
        name = os.path.splitext(os.path.basename(f))[0]
        txt = docx_text(f)
        dest = os.path.join(outdir, name + '.txt')
        with open(dest, 'w', encoding='utf-8') as fh:
            fh.write(f"SOURCE: {f}\n{'='*80}\n{txt}")
        log.append(f"{dest}  chars={len(txt)}")
    print('\n'.join(log))