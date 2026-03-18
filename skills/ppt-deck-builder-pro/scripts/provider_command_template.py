#!/usr/bin/env python3
"""
Template for a custom image provider command.

Contract:
- accepts `--request-file <path>`
- reads the JSON request file
- prints one JSON result object to stdout

A successful result should include `status: SUCCESS` plus one of:
- image_url
- image_path
- image_base64
- image_data_uri
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-file", required=True, help="Path to the JSON request file")
    args = parser.parse_args()

    request = json.loads(Path(args.request_file).read_text(encoding="utf-8"))

    result = {
        "status": "FAILED",
        "provider": "custom_adapter_template",
        "reason": "Edit scripts/provider_command_template.py to call your image API and return SUCCESS.",
        "example_request_fields": {
            "slide_number": request.get("slide_number"),
            "resolution": request.get("resolution"),
            "aspectRatio": request.get("aspectRatio"),
        },
    }
    json.dump(result, sys.stdout, ensure_ascii=False)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
