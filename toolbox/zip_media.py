import zipfile, os
p = r"C:\Users\ericz\Desktop\大运营体系组织构架方案20261026（定稿）.docx"
dst = r"D:\B166ER-openclaw\workspace\toolbox\_extract_fazhan\dazun"
os.makedirs(dst, exist_ok=True)
z = zipfile.ZipFile(p)
for n in ["word/media/image1.jpeg", "word/media/image2.jpeg"]:
    data = z.read(n)
    fn = os.path.join(dst, os.path.basename(n))
    open(fn, "wb").write(data)
    print("saved", fn, len(data))
try:
    from PIL import Image
    for n in ["image1.jpeg", "image2.jpeg"]:
        f = os.path.join(dst, n)
        im = Image.open(f)
        print(n, "orig size:", im.size)
        w, h = im.size
        if w > 900:
            im2 = im.convert("RGB").resize((900, int(h*900/w)), Image.LANCZOS)
            o = os.path.join(dst, n.replace(".jpeg", "_small.png"))
            im2.save(o)
            print("  ->", o, im2.size)
except Exception as e:
    print("PIL:", e)
