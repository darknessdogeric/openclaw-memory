# -*- coding: utf-8 -*-
"""Research: international-chain luxury hotel investment/operating model benchmarks."""
import io, sys, os, re, requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
KEY = "***"
OUT = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\bench_intl.txt"

QUERIES = [
    "luxury hotel management agreement fee structure base fee incentive fee FF&E reserve percentage",
    "luxury hotel GOP margin benchmark 2025 2026 STR luxury upper upscale operating margin",
    "luxury hotel revenue mix rooms F&B spa percentage of total revenue",
    "luxury hotel renovation reduce number of rooms increase ADR total revenue case study",
    "USALI hotel operating statement structure owner operator management fee reserve accounts",
    "luxury hotel per key renovation cost per room 2025 2026 high end full service",
    "luxury hotel staffing ratio employees per room benchmark full service five star",
    "Rosewood Regent Peninsula Mandarin Oriental management fee structure luxury brand economics",
]


def search(q, max_results=6):
    r = requests.post(
        "https://api.tavily.com/search",
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
        json={"query": q, "max_results": max_results, "include_answer": True, "search_depth": "advanced"},
        timeout=45,
    )
    r.raise_for_status()
    return r.json()


def getkey():
    src = open(r"D:\B166ER-openclaw\workspace\toolbox\tavily_search.py", encoding="utf-8").read()
    m = re.search(r"tvly-[A-Za-z0-9\-_]+", src)
    return m.group(0) if m else KEY


KEY = getkey()

with open(OUT, "w", encoding="utf-8") as f:
    for q in QUERIES:
        f.write(f"\n{'='*92}\n### QUERY: {q}\n{'='*92}\n")
        try:
            d = search(q)
        except Exception as e:
            f.write(f"[ERR] {type(e).__name__}: {e}\n")
            continue
        ans = d.get("answer", "")
        if ans:
            f.write(f"[ANSWER]\n{ans}\n\n")
        for it in d.get("results", []):
            f.write(f"[{it.get('score',0):.2f}] {it.get('title','')[:110]}\n")
            f.write(f"    URL: {it.get('url','')}\n")
            c = (it.get("content") or "").strip()
            if c:
                f.write(f"    {c[:1400]}\n")
            f.write("\n")
print("written", os.path.getsize(OUT))
