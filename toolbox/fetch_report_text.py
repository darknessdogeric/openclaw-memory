"""Fetch a meadin/traveldaily report page and dump readable text.

Usage: python fetch_report_text.py <url>
Reuses the same stealth-ish headers as data_collector.py (Cloudflare bypass).
"""
import re
import sys
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://www.google.com/",
}

TAG_RE = re.compile(r"<[^>]+>")
SCRIPT_RE = re.compile(r"<(script|style|noscript)[^>]*>.*?</\1>", re.S | re.I)
WS_RE = re.compile(r"[ \t\r\f\v]+")


def extract(html: str) -> str:
    html = SCRIPT_RE.sub(" ", html)
    text = TAG_RE.sub("\n", html)
    text = (text.replace("&nbsp;", " ").replace("&amp;", "&")
                .replace("&lt;", "<").replace("&gt;", ">")
                .replace("&quot;", '"').replace("&#39;", "'"))
    lines = [WS_RE.sub(" ", ln).strip() for ln in text.split("\n")]
    return "\n".join(ln for ln in lines if ln)


def main() -> int:
    url = sys.argv[1]
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=45) as resp:
        raw = resp.read()
    for enc in ("utf-8", "gbk", "gb18030"):
        try:
            html = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        html = raw.decode("utf-8", errors="replace")
    out = extract(html)
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 6000
    print(out[:limit])
    print(f"\n--- [chars={len(out)} shown={min(limit, len(out))}] ---")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())