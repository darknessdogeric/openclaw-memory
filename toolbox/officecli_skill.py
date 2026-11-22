"""
officecli_skill.py — B166ER production wrapper for OfficeCLI v1.0.135
=====================================================================

Wraps iOfficeAI/OfficeCLI (single binary, no Office install) for use in B166ER workflows.

KNOWN ISSUES (v1.0.135, 2026-07-14):
- 'view outline', 'view html', 'raw' commands corrupt Chinese (UTF-8 → UTF-16-LE conversion bug)
- XML content INSIDE the .pptx/.docx/.xlsx is correct — read back via python-pptx/openpyxl/python-docx
- 'add', 'set', 'remove', 'create' commands work perfectly for Chinese

WORKAROUND: This wrapper uses officecli for write operations and python-pptx/openpyxl
for verification (since python-pptx reads the underlying XML, which is correct).

Author: B166ER for Eric Zhang
Date: 2026-07-14
Status: Production-ready for content creation; verification via python-pptx only.
"""

import os
import sys
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass, field


# ===== Config =====

OFFICECLI_BIN = os.environ.get("OFFICECLI_BIN", r"D:\OfficeCLI-test\officecli.exe")
OFFICECLI_DEFAULT_TIMEOUT = 60  # seconds per command


@dataclass
class OfficeCliResult:
    """Result of an officecli command."""
    ok: bool
    returncode: int
    stdout: str
    stderr: str
    cmd: List[str]
    error: Optional[str] = None


def _run(cmd: List[str], timeout: int = OFFICECLI_DEFAULT_TIMEOUT, cwd: Optional[str] = None) -> OfficeCliResult:
    """Run an officecli command with timeout and capture output."""
    if not Path(OFFICECLI_BIN).exists():
        return OfficeCliResult(
            ok=False, returncode=-1, stdout="", stderr="",
            cmd=cmd, error=f"officecli binary not found at {OFFICECLI_BIN}"
        )
    
    full_cmd = [OFFICECLI_BIN] + cmd
    try:
        # Use bytes mode to avoid Windows encoding issues with Chinese
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            timeout=timeout,
            cwd=cwd,
        )
        return OfficeCliResult(
            ok=(result.returncode == 0),
            returncode=result.returncode,
            stdout=result.stdout.decode('utf-8', errors='replace'),
            stderr=result.stderr.decode('utf-8', errors='replace'),
            cmd=full_cmd,
        )
    except subprocess.TimeoutExpired:
        return OfficeCliResult(
            ok=False, returncode=-1, stdout="", stderr="",
            cmd=full_cmd, error=f"timeout after {timeout}s"
        )
    except Exception as e:
        return OfficeCliResult(
            ok=False, returncode=-1, stdout="", stderr="",
            cmd=full_cmd, error=f"{type(e).__name__}: {e}"
        )


# ===== Helpers =====

def ensure_extension(path: str) -> str:
    """Ensure path has .pptx/.docx/.xlsx extension. Detect from existing or content."""
    if path.endswith(('.pptx', '.docx', '.xlsx')):
        return path
    raise ValueError(f"Path must end with .pptx/.docx/.xlsx: {path}")


def verify_pptx(path: str) -> Dict[str, Any]:
    """Verify .pptx file by reading XML directly via python-pptx.
    This bypasses the officecli view bug for Chinese."""
    try:
        from pptx import Presentation
    except ImportError:
        return {"ok": False, "error": "python-pptx not installed"}
    
    if not Path(path).exists():
        return {"ok": False, "error": f"file not found: {path}"}
    
    try:
        prs = Presentation(path)
        slides = []
        for i, slide in enumerate(prs.slides, 1):
            shapes = []
            for shape in slide.shapes:
                if shape.has_text_frame:
                    text = shape.text_frame.text
                    if text.strip():
                        shapes.append({"type": "text", "name": shape.name, "text": text})
                elif shape.has_table:
                    tbl = []
                    for row in shape.table.rows:
                        tbl.append([cell.text for cell in row.cells])
                    shapes.append({"type": "table", "name": shape.name, "data": tbl})
                else:
                    shapes.append({"type": shape.shape_type.__class__.__name__, "name": shape.name})
            slides.append({"index": i, "shapes": shapes})
        
        return {
            "ok": True,
            "path": path,
            "size_bytes": Path(path).stat().st_size,
            "slide_count": len(prs.slides),
            "slides": slides,
            "slide_width_emu": prs.slide_width,
            "slide_height_emu": prs.slide_height,
        }
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}


# ===== PPTX (PowerPoint) =====

def create_pptx(path: str, blank: bool = True) -> OfficeCliResult:
    """Create a new .pptx file."""
    path = ensure_extension(path)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    return _run(["create", path])


def add_pptx_slide(
    path: str,
    title: Optional[str] = None,
    layout: str = "blank",
    properties: Optional[Dict[str, str]] = None,
) -> OfficeCliResult:
    """Add a new slide to a .pptx file.
    
    Args:
        path: Path to .pptx file
        title: Slide title (sets --prop title=...)
        layout: Slide layout (blank, title, content, etc.)
        properties: Additional properties as --prop key=value
    """
    cmd = ["add", path, "/", "--type", "slide"]
    props = dict(properties or {})
    if title:
        props["title"] = title
    if layout and layout != "blank":
        props["layout"] = layout
    for k, v in props.items():
        cmd.extend(["--prop", f"{k}={v}"])
    return _run(cmd)


def add_pptx_text(
    path: str,
    slide_idx: int,
    text: str,
    x: str = "2cm",
    y: str = "5cm",
    font: str = "Microsoft YaHei",
    size: int = 24,
    color: str = "000000",
    bold: bool = False,
    width: Optional[str] = None,
    height: Optional[str] = None,
) -> OfficeCliResult:
    """Add a text shape to a slide."""
    target = f"/slide[{slide_idx}]"
    cmd = ["add", path, target, "--type", "shape", "--prop", f"text={text}",
           "--prop", f"x={x}", "--prop", f"y={y}",
           "--prop", f"font={font}", "--prop", f"size={size}",
           "--prop", f"color={color}"]
    if bold:
        cmd.extend(["--prop", "bold=true"])
    if width:
        cmd.extend(["--prop", f"width={width}"])
    if height:
        cmd.extend(["--prop", f"height={height}"])
    return _run(cmd)


def set_pptx_property(path: str, slide_idx: int, shape_idx: int, **kwargs) -> OfficeCliResult:
    """Set properties on an existing shape."""
    target = f"/slide[{slide_idx}]/shape[{shape_idx}]"
    cmd = ["set", path, target]
    for k, v in kwargs.items():
        cmd.extend(["--prop", f"{k}={v}"])
    return _run(cmd)


def save_pptx(path: str) -> OfficeCliResult:
    """Flush resident session to disk."""
    return _run(["save", path])


def close_pptx(path: str) -> OfficeCliResult:
    """Close resident session for a .pptx file."""
    return _run(["close", path])


def build_pptx(path: str, slides: List[Dict[str, Any]], verify: bool = True) -> Dict[str, Any]:
    """High-level: build a PPTX deck from a slides spec.
    
    Each slide dict can have:
        - title: str (becomes title prop)
        - subtitle: str (added as text shape)
        - bullets: List[str] (each becomes a text shape)
        - background: hex color (e.g. "1A1A2E")
        - shapes: List[Dict] (custom shapes with text/x/y/font/size/color)
    """
    path = ensure_extension(path)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    
    log = {"steps": [], "errors": []}
    
    # Create
    r = create_pptx(path)
    log["steps"].append({"step": "create", "ok": r.ok, "stdout": r.stdout[:200]})
    if not r.ok:
        log["errors"].append(f"create failed: {r.error or r.stderr}")
        return {"ok": False, "log": log}
    
    # Add slides
    for i, slide in enumerate(slides, 1):
        props = {}
        if "title" in slide:
            props["title"] = slide["title"]
        if "background" in slide:
            props["background"] = slide["background"]
        
        r = add_pptx_slide(path, properties=props if props else None)
        log["steps"].append({"step": f"add_slide_{i}", "ok": r.ok, "stdout": r.stdout[:200]})
        if not r.ok:
            log["errors"].append(f"add_slide_{i} failed: {r.error or r.stderr}")
            continue
        
        # Add bullets as text shapes
        if "bullets" in slide:
            y_offset = 5
            for bullet in slide["bullets"]:
                r = add_pptx_text(path, i, bullet, x="2cm", y=f"{y_offset}cm", size=20)
                log["steps"].append({"step": f"add_text_{i}_{y_offset}", "ok": r.ok})
                y_offset += 1.5
                if y_offset > 20:  # safety
                    break
        
        # Add subtitle
        if "subtitle" in slide:
            r = add_pptx_text(path, i, slide["subtitle"], x="2cm", y="4cm", size=18, color="666666")
            log["steps"].append({"step": f"add_subtitle_{i}", "ok": r.ok})
        
        # Add custom shapes
        for j, shape in enumerate(slide.get("shapes", []), 1):
            r = add_pptx_text(
                path, i, shape["text"],
                x=shape.get("x", "2cm"),
                y=shape.get("y", f"{5 + j * 1.5}cm"),
                font=shape.get("font", "Microsoft YaHei"),
                size=shape.get("size", 20),
                color=shape.get("color", "000000"),
                bold=shape.get("bold", False),
            )
            log["steps"].append({"step": f"add_shape_{i}_{j}", "ok": r.ok})
    
    # Save and close
    r = save_pptx(path)
    log["steps"].append({"step": "save", "ok": r.ok})
    r = close_pptx(path)
    log["steps"].append({"step": "close", "ok": r.ok})
    
    result = {"ok": len(log["errors"]) == 0, "log": log, "path": path}
    
    # Verify if requested
    if verify:
        result["verify"] = verify_pptx(path)
        if not result["verify"]["ok"]:
            log["errors"].append(f"verify failed: {result['verify'].get('error')}")
            result["ok"] = False
    
    result["log"] = log
    return result


# ===== DOCX (Word) =====

def create_docx(path: str) -> OfficeCliResult:
    """Create a new .docx file."""
    path = ensure_extension(path)
    return _run(["create", path])


# ===== XLSX (Excel) =====

def create_xlsx(path: str) -> OfficeCliResult:
    """Create a new .xlsx file."""
    path = ensure_extension(path)
    return _run(["create", path])


# ===== CLI =====

def main():
    """CLI entry point for quick checks."""
    import argparse
    p = argparse.ArgumentParser(description="B166ER OfficeCLI Skill")
    p.add_argument("--version", action="store_true", help="Show officecli version")
    p.add_argument("--verify", metavar="PPTX", help="Verify a .pptx file")
    p.add_argument("--create", metavar="PPTX", help="Create a new pptx")
    p.add_argument("--add-slide", nargs=2, metavar=("PPTX", "TITLE"), help="Add a slide")
    args = p.parse_args()
    
    if args.version:
        r = _run(["--version"])
        print(f"officecli: {r.stdout.strip() or r.stderr.strip()}")
        print(f"binary: {OFFICECLI_BIN}")
        return
    
    if args.verify:
        result = verify_pptx(args.verify)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    
    if args.create:
        r = create_pptx(args.create)
        print(f"create {args.create}: rc={r.returncode}, ok={r.ok}")
        return
    
    if args.add_slide:
        path, title = args.add_slide
        r = add_pptx_slide(path, title=title)
        print(f"add_slide: rc={r.returncode}, ok={r.ok}")
        return
    
    p.print_help()


if __name__ == "__main__":
    main()