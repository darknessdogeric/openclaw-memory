# Nano-PDF CLI Options Reference

## `nano-pdf edit`

Edit one or more existing pages in a PDF.

```
nano-pdf edit <file.pdf> <page> "<prompt>" [<page> "<prompt>" ...] [options]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `file.pdf` | Path to the input PDF file |
| `page` | 1-indexed page number to edit |
| `prompt` | Natural language description of the edit |

Multiple `page "prompt"` pairs can be provided. They are processed in parallel.

### Options

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--output` | string | `edited_<original>.pdf` | Output filename |
| `--resolution` | string | `4K` | Image resolution: `4K`, `2K`, or `1K`. Higher = better quality but slower and more expensive |
| `--style-refs` | string | Auto-selected | Comma-separated page numbers to use as style references (e.g., `"1,5"`) |
| `--use-context` | flag | Off | Include the full extracted text of the PDF as context for the model |
| `--no-use-context` | flag | — | Explicitly disable document context |
| `--disable-google-search` | flag | Search enabled | Prevent the model from using Google Search to find information |

---

## `nano-pdf add`

Insert a new AI-generated slide into the PDF.

```
nano-pdf add <file.pdf> <position> "<prompt>" [options]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `file.pdf` | Path to the input PDF file |
| `position` | Insert position: `0` = beginning, `N` = after page N |
| `prompt` | Natural language description of the new slide |

### Options

Same as `edit`, with one difference:

- `--use-context` is **enabled by default** for `add` (the model reads the full document to match style and content)
- Use `--no-use-context` to disable it

---

## Resolution Guide

| Setting | Pixels | Best For | Speed | Cost |
|---------|--------|----------|-------|------|
| `4K` | ~3840px | Final output, precise text, print-quality | Slowest | Highest |
| `2K` | ~2048px | Good balance of quality and speed | Medium | Medium |
| `1K` | ~1024px | Quick drafts, iteration, testing | Fastest | Lowest |

---

## Style References

When you use `--style-refs "1,3"`, the specified pages are sent alongside your target page so the model understands the visual language of the deck — fonts, colors, layout conventions, spacing.

Tips:
- Pick pages that best represent the design system (title slides, content slides)
- 2-3 style refs is usually sufficient
- More refs = more context for the model but also more tokens/cost
- If not specified, nano-pdf auto-selects reference pages

---

## Document Context

When `--use-context` is enabled, nano-pdf extracts the full text content of the PDF and includes it in the prompt. This helps the model:

- Understand the overall topic and narrative
- Maintain consistency across page edits
- Generate contextually relevant new slides

Use it when:
- Editing multiple pages that should be consistent
- Adding new slides that need to fit the narrative
- Making content-aware changes (e.g., "update to match the conclusion")

Skip it when:
- Making simple visual changes (color, layout)
- The PDF is very large (context can slow processing)
- You want the model to ignore existing content

---

## Google Search

By default, the model can use Google Search to look up current information before generating edits. This is useful for:

- "Update the market share data to latest figures"
- "Add current stock price for AAPL"
- "Include the latest quarterly results"

Use `--disable-google-search` when you want the model to only use provided context and not fetch external data.
