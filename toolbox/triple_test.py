import sys
sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace\toolbox')
from crawl4ai_wrapper import crawl_llm_ready

# Test 1
print('[Test 1] example.com')
r1 = crawl_llm_ready('https://example.com')
print(f'  Success: {r1.success}, MD len: {len(r1.markdown)}, Elapsed: {r1.elapsed:.1f}s')
if r1.error:
    print(f'  Error: {r1.error[:200]}')

# Test 2
print('[Test 2] github.com/unclecode/crawl4ai')
r2 = crawl_llm_ready('https://github.com/unclecode/crawl4ai')
print(f'  Success: {r2.success}, MD len: {len(r2.markdown)}, Elapsed: {r2.elapsed:.1f}s')
if r2.error:
    print(f'  Error: {r2.error[:200]}')

# Test 3
print('[Test 3] python.org')
r3 = crawl_llm_ready('https://www.python.org/')
print(f'  Success: {r3.success}, MD len: {len(r3.markdown)}, Elapsed: {r3.elapsed:.1f}s')
if r3.error:
    print(f'  Error: {r3.error[:200]}')