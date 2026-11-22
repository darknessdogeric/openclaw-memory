"""
Extract all images from the Anyi Chashan PPTX.

Strategy:
1. Dump every file under ppt/media/ to /toolbox/anyi_pptx_images/raw/  (full fidelity)
2. Walk each slide via python-pptx and find picture shapes; copy each referenced
   image to /toolbox/anyi_pptx_images/by_slide/slide{NN}_img{NN}.{ext}
3. Produce a manifest.csv mapping (file_name, slide_no, kind, ext, size_bytes)
4. Print a summary table at the end.
"""

import os, sys, csv, shutil, zipfile, io
from pathlib import Path
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

SRC = Path(r"C:\Users\ericz\Desktop\安逸茶山\250306安逸茶山康养休生谷项目汇报PPT(修)(3).pptx")
OUT = Path(r"D:\B166ER-OpenClaw\workspace\toolbox\anyi_pptx_images")
RAW = OUT / "raw"        # 全部 ppt/media 下的文件
BY_SLIDE = OUT / "by_slide"  # 按 slide 关联的有意义的图片
OUT.mkdir(parents=True, exist_ok=True)
RAW.mkdir(parents=True, exist_ok=True)
BY_SLIDE.mkdir(parents=True, exist_ok=True)

# ---------- Step 1: raw dump of ppt/media/ ----------
raw_files = []
with zipfile.ZipFile(SRC) as z:
    media_names = sorted([n for n in z.namelist() if n.startswith("ppt/media/") and n != "ppt/media/"])
    for name in media_names:
        base = Path(name).name
        if not base:
            continue
        target = RAW / base
        if not target.exists():
            with z.open(name) as src_f, open(target, "wb") as out_f:
                shutil.copyfileobj(src_f, out_f)
        raw_files.append(base)

print(f"[raw] dumped {len(raw_files)} media files → {RAW}")

# ---------- Step 2: per-slide picture shapes ----------
prs = Presentation(SRC)
manifest_rows = []
seen_blobs = {}  # sha1 -> output name so we don't write the same blob twice within a slide

def blob_hash(blob: bytes) -> str:
    import hashlib
    return hashlib.sha1(blob).hexdigest()[:12]

for s_idx, slide in enumerate(prs.slides, 1):
    pic_count = 0
    for shape in slide.shapes:
        is_pic = False
        try:
            is_pic = shape.shape_type == MSO_SHAPE_TYPE.PICTURE
        except Exception:
            pass
        # also catch placeholders that hold pictures
        if not is_pic and hasattr(shape, "image"):
            try:
                _ = shape.image  # will raise if not a picture
                is_pic = True
            except Exception:
                is_pic = False
        if not is_pic:
            continue

        try:
            img = shape.image
            blob = img.blob
            ext = img.ext  # jpeg/png/...
        except Exception:
            continue
        h = blob_hash(blob)
        # Skip already-saved-per-slide duplicates (e.g., repeated icon on same slide)
        key = f"s{s_idx}_{h}"
        if key in seen_blobs:
            manifest_rows.append([f"s{s_idx:02d}_{pic_count:02d}", s_idx, "picture", ext,
                                   len(blob), "(dedup, same blob on slide)"])
            continue
        seen_blobs[key] = True
        pic_count += 1
        out_name = f"s{s_idx:02d}_img{pic_count:02d}.{ext}"
        (BY_SLIDE / out_name).write_bytes(blob)
        manifest_rows.append([out_name, s_idx, "picture", ext, len(blob), ""])

print(f"[by_slide] wrote {sum(1 for r in manifest_rows if r[5] == '')} pictures → {BY_SLIDE}")

# ---------- Step 3: write manifest.csv ----------
manifest_path = OUT / "manifest.csv"
with open(manifest_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["file_name", "slide_no", "kind", "ext", "size_bytes", "note"])
    for r in manifest_rows:
        w.writerow(r)

# ---------- Summary ----------
print()
print("=" * 60)
print("EXTRACTION SUMMARY")
print("=" * 60)
print(f"PPTX source: {SRC.name}")
print(f"Total slides: {len(prs.slides)}")
print(f"Raw media files: {len(raw_files)}  (in /raw/)")
print(f"Picture shapes extracted: {sum(1 for r in manifest_rows if r[5] == '')}  (in /by_slide/)")
print(f"Duplicates skipped (same blob reused): {sum(1 for r in manifest_rows if r[5])}")
print(f"Manifest: {manifest_path}")
print()
print("Output tree:")
print(f"  {OUT}/")
print(f"  ├── raw/          ({len(raw_files)} files, all ppt/media/* original)")
print(f"  ├── by_slide/     (per-slide picture shapes, dedup)")
print(f"  └── manifest.csv")
print()

# per-slide count
from collections import Counter
c = Counter(r[1] for r in manifest_rows if r[5] == "")
print("Pictures per slide:")
for slide_no in sorted(c.keys()):
    print(f"  slide {slide_no:>2} : {c[slide_no]} image(s)")