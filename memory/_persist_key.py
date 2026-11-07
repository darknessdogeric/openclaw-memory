"""持久化真 Tavily key 到 .env (不走 shell 回显)"""
from pathlib import Path

# Eric 2026-10-19 20:50 给的真 key
KEY = "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"

env_path = Path(r"D:\B166ER-openclaw\config\.env")
env_path.parent.mkdir(parents=True, exist_ok=True)

# ASCII 编码 (避免 UTF-8 BOM)
env_path.write_bytes(f"TAVILY_API_KEY={KEY}\n".encode("ascii"))

# 验证
print(f"[OK] .env: {env_path}")
print(f"     size: {env_path.stat().st_size} bytes")
content = env_path.read_bytes()
key_part = content[15:-1]
print(f"     starts_with_TAVILY: {content.startswith(b'TAVILY_API_KEY=')}")
print(f"     key_len: {len(key_part)} (expected 51+)")
print(f"     key_prefix: {key_part[:11]}")