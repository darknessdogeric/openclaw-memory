#!/usr/bin/env python3
import argparse
import json
import os
import pathlib
import re
import sys
import urllib.request

TAVILY_URL = "https://api.tavily.com/search"
TAVILY_KEY = "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"

def tavily_search(query, max_results, include_answer, search_depth):
    payload = {
        "api_key": TAVILY_KEY,
        "query": query,
        "max_results": max_results,
        "search_depth": search_depth,
        "include_answer": bool(include_answer),
        "include_images": False,
        "include_raw_content": False,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        TAVILY_URL,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8", errors="replace")
    obj = json.loads(body)
    return {
        "query": query,
        "answer": obj.get("answer"),
        "results": [{"title": r.get("title"), "url": r.get("url"), "content": r.get("content")} for r in (obj.get("results") or [])[:max_results]],
    }

def to_markdown(obj):
    lines = []
    if obj.get("answer"):
        lines.append(obj["answer"].strip())
        lines.append("")
    for i, r in enumerate(obj.get("results", []) or [], 1):
        title = (r.get("title") or "").strip() or r.get("url") or "(no title)"
        url = r.get("url") or ""
        snippet = (r.get("content") or "").strip()
        lines.append(f"{i}. {title}")
        if url:
            lines.append(f"   {url}")
        if snippet:
            lines.append(f"   - {snippet}")
    return "\n".join(lines).strip()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--max-results", type=int, default=5)
    ap.add_argument("--include-answer", action="store_true")
    ap.add_argument("--search-depth", default="basic", choices=["basic", "advanced"])
    ap.add_argument("--format", default="md", choices=["raw", "md"])
    args = ap.parse_args()

    res = tavily_search(args.query, max(1, min(args.max_results, 10)), args.include_answer, args.search_depth)

    if args.format == "md":
        print(to_markdown(res))
    else:
        print(json.dumps(res, ensure_ascii=False, indent=2))
