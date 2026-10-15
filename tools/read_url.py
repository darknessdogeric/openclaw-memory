"""
B166ER 原子工具: read_url
=========================
通用 HTTP GET 抓取。带超时、重试、错误处理。

契约: tools/schemas/read_url.schema.json
"""
import requests
import time
from typing import List, Optional, Dict, Any

DEFAULT_TIMEOUT = 15
MAX_RETRIES = 2
USER_AGENT = "B166ER/1.0"


def read_url(
    url: str,
    timeout: int = DEFAULT_TIMEOUT,
    retries: int = MAX_RETRIES,
    headers: Optional[Dict[str, str]] = None,
    verify_ssl: bool = True,
) -> Dict[str, Any]:
    """
    HTTP GET 抓取 URL 内容

    Args:
        url: 目标 URL
        timeout: 单次超时秒数
        retries: 失败重试次数 (excluding first attempt)
        headers: 自定义 headers
        verify_ssl: 是否验证 SSL 证书

    Returns:
        {
            "ok": bool,
            "status_code": int,
            "content": str | None,
            "content_length": int,
            "elapsed_ms": int,
            "url_final": str,  # after redirects
            "error": str | None,  # if not ok
        }
    """
    merged_headers = {"User-Agent": USER_AGENT}
    if headers:
        merged_headers.update(headers)

    last_error: Optional[str] = None
    for attempt in range(retries + 1):
        start = time.time()
        try:
            resp = requests.get(
                url,
                timeout=timeout,
                headers=merged_headers,
                verify=verify_ssl,
                allow_redirects=True,
            )
            elapsed_ms = int((time.time() - start) * 1000)
            return {
                "ok": 200 <= resp.status_code < 400,
                "status_code": resp.status_code,
                "content": resp.text if resp.status_code == 200 else None,
                "content_length": len(resp.text) if resp.text else 0,
                "elapsed_ms": elapsed_ms,
                "url_final": resp.url,
                "error": None if 200 <= resp.status_code < 400 else f"HTTP {resp.status_code}",
            }
        except requests.exceptions.Timeout as e:
            last_error = f"timeout after {timeout}s"
        except requests.exceptions.SSLError as e:
            last_error = f"ssl_error: {type(e).__name__}"
        except requests.exceptions.ConnectionError as e:
            last_error = f"connection_error: {type(e).__name__}"
        except Exception as e:
            last_error = f"{type(e).__name__}: {str(e)[:100]}"
        if attempt < retries:
            time.sleep(0.5 * (attempt + 1))  # backoff

    return {
        "ok": False,
        "status_code": 0,
        "content": None,
        "content_length": 0,
        "elapsed_ms": int((time.time() - start) * 1000) if 'start' in dir() else 0,
        "url_final": url,
        "error": last_error,
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        r = read_url(sys.argv[1])
        print(f"ok={r['ok']} status={r['status_code']} length={r['content_length']} error={r['error']}")
    else:
        print("usage: python read_url.py <url>")
