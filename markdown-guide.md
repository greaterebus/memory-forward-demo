# Markdown Syntax Guide

Markdown is a lightweight formatting language used throughout Memory Forward's documentation,
templates, and job notes. It renders as formatted text in most editors and platforms while
remaining readable as plain text.

---

## Headings

Use `#` signs to create headings. More `#` signs = smaller heading.

```markdown
# Heading 1 — page title
## Heading 2 — major section
### Heading 3 — subsection
#### Heading 4 — minor subsection
```

---

## Text Formatting

| Effect | Syntax | Result |
|--------|--------|--------|
| Bold | `**text**` | **text** |
| Italic | `*text*` | *text* |
| Bold + italic | `***text***` | ***text*** |
| Strikethrough | `~~text~~` | ~~text~~ |
| Inline code | `` `text` `` | `text` |

---

## Lists

### Unordered lists

Use `-`, `*`, or `+` as bullets. Indent two spaces to nest.

```markdown
- Item one
- Item two
  - Nested item
  - Another nested item
- Item three
```

### Ordered lists

Use numbers followed by a period. The actual numbers don't matter — Markdown will render them
in sequence.

```markdown
1. First step
2. Second step
3. Third step
```

### Task / checklist lists

```markdown
- [x] Completed item
- [ ] Incomplete item
```

---

## Links

```markdown
[Link text](https://example.com)
```

For internal document references:

```markdown
[File Naming Conventions](file-naming-conventions.md)
```

---

## Images

```markdown
![Alt text](path/to/image.jpg)
```

Alt text is displayed if the image fails to load and is important for accessibility.

---

## Code Blocks

For multi-line code, wrap with triple backticks. Add a language name for syntax highlighting.

````markdown
```bash
python scripts/processing/rename_files.py --job-id MF240315
```
````

Common language tags: `bash`, `python`, `json`, `csv`, `markdown`, `text`

---

## Tables

```markdown
| Column A | Column B | Column C |
|----------|----------|----------|
| Row 1    | Value    | Value    |
| Row 2    | Value    | Value    |
```

Colons in the separator row control alignment:

```markdown
| Left     | Center   | Right    |
|:---------|:--------:|---------:|
| text     | text     | text     |
```

---

## Blockquotes

Use `>` for quoted or highlighted text:

```markdown
> This is a blockquote. Good for callouts, warnings, or customer notes.
```

---

## Horizontal Rules

Three dashes on their own line create a divider:

```markdown
---
```

---

## Line Breaks and Paragraphs

- A blank line between text creates a new paragraph.
- A single newline within a paragraph is ignored — the text wraps together.
- To force a line break within a paragraph, end the line with two spaces.

---

## Escaping Special Characters

To display a character that Markdown would otherwise interpret (like `*` or `#`), prefix it
with a backslash:

```markdown
\*not italic\*
\# not a heading
```

---

## Tips for Memory Forward Documents

- Use `##` sections to organize job notes — makes them scannable at a glance.
- Use task lists (`- [ ]`) in checklists like the [job checklist template](../../templates/job-checklist.md).
- Keep tables for structured data like media counts or scan settings.
- Prefer fenced code blocks (triple backtick) over indented code — it's clearer.
