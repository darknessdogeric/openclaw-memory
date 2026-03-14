# Development Diary — audiobook-skill

## 2026-02-16 - Initial implementation (Fase 2)

### What was done
- Created audiobook-skill from scratch, porting modules from PDF-whisperer
- Ported: models.py, cleaner.py, chapters.py (unchanged from PDF-whisperer)
- Ported + adapted: extractor.py (added .txt support), assembler.py (apt-get instead of brew)
- Created new: tts_piper.py (replaces macOS `say` with piper TTS)
- Created new: audiobook.py (CLI with convert + list-voices subcommands)
- Created SKILL.md for OpenClaw agent integration
- Created Makefile with setup, test, deploy, prod targets
- 74 tests passing locally (all mocked, no piper dependency needed)
- Deployed to poe.omelas.net, models downloaded automatically
- End-to-end test passed: text file -> M4B with 2 chapters

### Decisions made
- Used `voice.synthesize_wav()` API (not `synthesize_stream_raw` which doesn't exist in piper)
- Speaker ID passed via `SynthesisConfig` object
- piper import is lazy (only when needed) so tests work without piper installed
- Backslash escaping in ffmetadata fixed (must escape `\` first)
- TEXT_PAGE_SIZE = 3000 chars for splitting plain text into "pages"

### Challenges/Learnings
- piper API is `synthesize(text)` -> AudioChunk iterator and `synthesize_wav(text, wav_file)` — not `synthesize_stream_raw`
- `_escape_ffmeta()` had a bug in original PDF-whisperer: backslash was escaped last, causing double-escaping

### Next steps
- Test with a real PDF on the server
- Test via Telegram (OpenClaw agent using SKILL.md)
- Consider adding progress reporting for long books
