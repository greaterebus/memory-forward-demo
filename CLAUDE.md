# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

Memory Forward's internal knowledge base for a digitization business that restores physical media (printed photos, film negatives, slides, VHS/Beta tapes, 8mm film) and delivers organized digital archives to customers.

## Answering Questions

When the user asks a question, **always search `docs/` first** before looking elsewhere or searching the web. Questions are most likely about Memory Forward's business operations, and the answer is probably in:

- `docs/workflows/` — step-by-step job processes
- `docs/standards/` — file naming rules, quality benchmarks
- `docs/onboarding/` — new employee guides
- `templates/` — intake forms, job checklists

Only fall back to web search if the docs clearly don't cover the topic.

## Documentation Standards

All docs use GitHub-flavored Markdown. Pages under `docs/` use Jekyll frontmatter (`layout`, `title`, `parent`, `nav_order`). See [markdown-guide.md](markdown-guide.md) for the style reference.

## Contributing

Branch naming: `your-name/description-of-change`. PRs require a team lead review — do not merge your own PR.
