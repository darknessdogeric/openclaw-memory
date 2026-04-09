# Corrections Log

## 2026-04-08

**Issue**: Emoji in Python scripts (`print("🔧 ...")`) caused `UnicodeEncodeError: 'gbk' codec can't encode character` on Windows
**Context**: local_semantic_search.py crashed 3 times before fixing
**Lesson**: Never use emoji in any script output on Windows. Always use ASCII alternatives.
**Applied**: 3x → Promote to HOT rule

**Issue**: Spent 40+ minutes trying to fix Jina API rate limit instead of implementing the already-known local fallback
**Context**: User asked "不升级jina api的话有没有免费替代方案" - I knew about model2vec+ChromaDB but hesitated
**Lesson**: When API has a clear rate limit problem, implement the backup immediately without prolonged analysis
**Applied**: 1x → Track

**Issue**: KB version cleanup only done when user asked, not proactively
**Context**: 50 versioned KB files (361KB wasted) accumulated over weeks
**Lesson**: Proactively maintain knowledge base, don't wait to be asked
**Applied**: 1x → Track
