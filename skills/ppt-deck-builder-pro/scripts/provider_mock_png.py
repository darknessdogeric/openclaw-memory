#!/usr/bin/env python3
"""
Offline mock provider for pipeline verification.

It ignores the prompt and returns a tiny PNG via base64 so the deck workflow
can be validated without any external API.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


MOCK_PNG_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO7Z8tQAAAAASUVORK5CYII="
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-file", required=True, help="Path to the JSON request file")
    args = parser.parse_args()

    request = json.loads(Path(args.request_file).read_text(encoding="utf-8"))
    result = {
        "status": "SUCCESS",
        "provider": "mock_png",
        "model": "offline-test",
        "taskId": f"mock-{request.get('slide_number', 0)}",
        "image_base64": MOCK_PNG_BASE64,
    }
    json.dump(result, sys.stdout, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
