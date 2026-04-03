---
layout: default
title: File Naming Conventions
parent: Standards
nav_order: 1
---

# File Naming Conventions

All files produced by Memory Forward must follow these naming conventions. Consistent naming makes
orders searchable, prevents overwrites, and helps customers navigate their archives.

---

## Master Format

```
<JOB_ID>_<MEDIA_TYPE>_<SEQUENCE>_<DESCRIPTOR>.<EXT>
```

### Components

| Part | Description | Example |
|------|-------------|---------|
| `JOB_ID` | 8-character alphanumeric job identifier | `MF240315` |
| `MEDIA_TYPE` | Two-letter media code (see table below) | `PH` |
| `SEQUENCE` | 4-digit zero-padded sequence number | `0042` |
| `DESCRIPTOR` | Optional free-text label (lowercase, hyphens only) | `vacation-hawaii` |
| `EXT` | File extension (lowercase) | `tif` |

### Media Type Codes

| Code | Media |
|------|-------|
| `PH` | Printed photo |
| `NG` | Film negative |
| `SL` | 35mm slide |
| `VH` | VHS/Beta tape |
| `FM` | 8mm / Super 8 film |
| `OT` | Other / miscellaneous |

---

## Examples

| Situation | Filename |
|-----------|---------|
| 42nd photo scanned in job MF240315 | `MF240315_PH_0042.tif` |
| 7th negative strip with a descriptor | `MF240315_NG_0007_summer-1987.tif` |
| 1st VHS tape capture | `MF240315_VH_0001.mp4` |
| 3rd slide in a batch | `MF240315_SL_0003.tif` |
| Web-quality JPEG preview of the same slide | `MF240315_SL_0003_preview.jpg` |

---

## Folder Structure

Each job folder follows this layout:

```
MF240315/
├── raw/
│   ├── photos/
│   ├── negatives/
│   ├── slides/
│   └── video/
├── processed/
│   ├── photos/
│   ├── negatives/
│   ├── slides/
│   ├── video/
│   └── previews/
├── delivery/
│   └── MF240315_archive.zip
└── MF240315_job_log.txt
```

---

## Rules

1. **No spaces** in filenames — use hyphens (`-`) to separate words in descriptors
2. **Lowercase extensions** always — `tif` not `TIF`, `jpg` not `JPG`
3. **Never overwrite** an existing file — increment the sequence number instead
4. **No special characters** — only letters, numbers, hyphens, and underscores
5. Descriptors are **optional** but encouraged when the customer has labeled items
6. Sequence numbers restart at `0001` for each media type within a job

---

## Automated Renaming

The processing pipeline handles renaming automatically. You do not need to rename raw scan files
by hand — the pipeline reads the scanner's output and applies the convention.

If you need to rename files manually (e.g., after a pipeline failure), use the helper script:

```bash
python scripts/processing/rename_files.py --job-id <JOB_ID> --media-type PH
```
