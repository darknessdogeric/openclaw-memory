# Nano-PDF Examples

Real-world examples organized by use case. Copy and adapt these commands.

---

## Fixing Text and Typos

```bash
# Fix a single typo
nano-pdf edit report.pdf 3 "Fix the typo 'recieve' to 'receive'"

# Fix multiple typos across pages
nano-pdf edit deck.pdf \
  3 "Fix the typo 'recieve' to 'receive'" \
  7 "Change 'Q4 2024' to 'Q1 2025'" \
  12 "Fix 'accomodate' to 'accommodate'"

# Update a date
nano-pdf edit slides.pdf 1 "Update the date from 'January 2025' to 'February 2026'"
```

---

## Updating Charts and Data

```bash
# Change a value in a chart
nano-pdf edit report.pdf 12 "Update the revenue chart to show Q3 at $2.5M instead of $2.1M"

# Change chart type
nano-pdf edit deck.pdf 8 "Change the pie chart to a horizontal bar chart with the same data"

# Add data to a chart
nano-pdf edit report.pdf 5 "Add a 2025 data point showing 15% growth to the line chart"

# Use Google Search for current data
nano-pdf edit deck.pdf 5 "Update the market share data to latest available figures"
```

---

## Visual Design and Branding

```bash
# Change colors
nano-pdf edit slides.pdf 1 "Make the header background dark blue (#1a365d) and text white"

# Update branding across multiple pages
nano-pdf edit pitch.pdf \
  1 "Change the tagline to 'Building the Future'" \
  2 "Update all section headings to dark blue" \
  5 "Replace the old logo with text 'NewCorp' in the same position" \
  --style-refs "1" --output branded_pitch.pdf

# Change layout
nano-pdf edit deck.pdf 4 "Move the image to the left side and text to the right"

# Add visual elements
nano-pdf edit presentation.pdf 8 "Add a subtle grid pattern to the background"
```

---

## Adding New Slides

```bash
# Add a title slide at the very beginning
nano-pdf add deck.pdf 0 "Title slide: 'Annual Review 2025' with subtitle 'Building the Future'"

# Add an agenda slide after the title
nano-pdf add deck.pdf 1 "Agenda slide with items: Overview, Financial Results, Product Roadmap, Q4 Outlook"

# Add a summary/takeaway slide after page 10
nano-pdf add deck.pdf 10 "Summary slide with key takeaways as bullet points"

# Add a slide that references existing content
nano-pdf add quarterly.pdf 5 "Comparison table showing Q1 vs Q2 metrics from the previous pages"

# Add a slide without Google Search
nano-pdf add deck.pdf 3 "Blank section divider with just the word 'STRATEGY' centered" \
  --disable-google-search
```

---

## Batch Processing

```bash
# Comprehensive deck update
nano-pdf edit quarterly_report.pdf \
  1 "Update the date to Q1 2026" \
  3 "Fix the typo in the subtitle" \
  5 "Update the revenue figure from $12M to $14.2M" \
  8 "Change the chart colors to blue and teal" \
  12 "Add 'Confidential' watermark in light gray" \
  --use-context --output q1_2026_report.pdf

# Multi-page style update with references
nano-pdf edit slides.pdf \
  2 "Match the header style to the style reference pages" \
  4 "Match the header style to the style reference pages" \
  6 "Match the header style to the style reference pages" \
  --style-refs "1"
```

---

## Working with Different PDF Types

### Pitch Decks
```bash
nano-pdf edit pitch.pdf 1 \
  "Change the tagline in the logo to 'Cringe posts from work colleagues' and update the date"
```

### Financial Reports
```bash
nano-pdf edit financials.pdf 8 \
  "Update the revenue waterfall chart: Q1=$3.2M, Q2=$3.8M, Q3=$4.1M, Q4=$4.5M" \
  --use-context
```

### Academic Papers
```bash
nano-pdf edit paper.pdf 1 "Update the author affiliation from 'MIT' to 'Stanford University'"
```

### Marketing Materials
```bash
nano-pdf edit brochure.pdf \
  1 "Change the headline to 'Summer Sale — Up to 50% Off'" \
  2 "Update the phone number to (555) 123-4567" \
  --resolution "4K" --output summer_brochure.pdf
```

---

## Quality Control Patterns

```bash
# Quick draft first, then high-quality final
nano-pdf edit deck.pdf 5 "Add a comparison table" --resolution "1K" --output draft.pdf
# Review draft.pdf, then if happy:
nano-pdf edit deck.pdf 5 "Add a comparison table" --resolution "4K" --output final.pdf

# Use context for consistency when editing many pages
nano-pdf edit deck.pdf \
  1 "Update branding" \
  2 "Update branding" \
  3 "Update branding" \
  --use-context --style-refs "1"
```
