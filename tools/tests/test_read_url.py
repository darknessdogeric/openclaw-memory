"""
B166ER 工具测试: test_read_url
==============================
测试 read_url 工具的核心契约。

运行: cd workspace/tools && python -m pytest tests/ -v
或: python tests/test_read_url.py (不需 pytest)
"""
import sys
import os
from pathlib import Path

# 允许从 tools/ 直接 import
sys.path.insert(0, str(Path(__file__).parent.parent))

from read_url import read_url  # noqa: E402


def test_basic_success():
    """基础成功: HTTP 200 + 有内容"""
    r = read_url("https://api.github.com/repos/morluto/rea", timeout=15)
    assert r["ok"] is True, f"expected ok=True, got {r}"
    assert 200 <= r["status_code"] < 400
    assert r["content"] is not None
    assert r["content_length"] > 0
    assert r["error"] is None
    print(f"[PASS] test_basic_success: status={r['status_code']} length={r['content_length']}")


def test_404_handled():
    """404 不抛异常,返回 ok=False"""
    r = read_url("https://api.github.com/repos/morluto/this-does-not-exist-xyz", timeout=10)
    assert r["ok"] is False
    assert r["status_code"] == 404
    assert r["error"] is not None
    assert "404" in r["error"]
    print(f"[PASS] test_404_handled: error={r['error']}")


def test_timeout_handled():
    """超时返回 error 而不抛"""
    # 使用一个不存在的域名,模拟快速失败
    r = read_url("https://this-domain-definitely-does-not-exist-xyz123.invalid", timeout=3, retries=0)
    assert r["ok"] is False
    assert r["error"] is not None
    print(f"[PASS] test_timeout_handled: error={r['error']}")


def test_redirects_followed():
    """redirects 被跟踪,url_final 改变"""
    r = read_url("https://github.com/morluto/rea", timeout=15)
    assert r["ok"] is True
    # GitHub 经常 redirect,url_final 应该跟 url 不同
    assert r["url_final"] != "https://github.com/morluto/rea" or r["status_code"] == 200
    print(f"[PASS] test_redirects_followed: url_final={r['url_final'][:50]}...")


def test_custom_headers():
    """自定义 headers 工作"""
    r = read_url(
        "https://api.github.com/repos/morluto/rea",
        headers={"Accept": "application/vnd.github.v3+json"},
        timeout=15,
    )
    assert r["ok"] is True
    print(f"[PASS] test_custom_headers: status={r['status_code']}")


def main():
    """无 pytest 时的 fallback"""
    tests = [
        test_basic_success,
        test_404_handled,
        test_timeout_handled,
        test_redirects_followed,
        test_custom_headers,
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] {t.__name__}: {type(e).__name__}: {e}")
            failed += 1
    print(f"\n{'='*50}")
    print(f"passed={passed} failed={failed} total={passed+failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
