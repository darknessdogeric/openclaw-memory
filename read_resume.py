import pdfplumber, sys
sys.stdout.reconfigure(encoding='utf-8')

for fname in [
    'C:/Users/ericz/Desktop/简历/Zhangshi.pdf',
    'C:/Users/ericz/Desktop/简历/张实的简历.pdf'
]:
    print(f'\n=== {fname.split("/")[-1]} ===')
    try:
        with pdfplumber.open(fname) as pdf:
            print(f'Pages: {len(pdf.pages)}')
            for i, page in enumerate(pdf.pages[:8]):
                text = page.extract_text()
                if text:
                    print(f'--- Page {i+1} ---')
                    print(text[:3000])
    except Exception as e:
        print(f'Error: {e}')
