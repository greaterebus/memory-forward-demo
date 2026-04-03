---
layout: default
title: Quality Standards
parent: Standards
nav_order: 2
---

# Quality Standards

Every file we deliver must meet these minimum standards. When in doubt, rescan — a slightly
longer turnaround is always better than delivering a poor-quality archive to a customer.

---

## Photo & Negative Scans

### Resolution Requirements

| Original Size | Minimum DPI | Target DPI |
|---------------|-------------|------------|
| ≥ 4×6 inches | 600 DPI | 600 DPI |
| 3×3 – 4×6 inches | 600 DPI | 1200 DPI |
| < 3×3 inches (wallet, etc.) | 1200 DPI | 2400 DPI |
| 35mm negative | 2400 DPI | 4800 DPI |
| 35mm slide | 2400 DPI | 2400 DPI |
| Medium format negative | 1200 DPI | 2400 DPI |

### Image Quality Checklist

- [ ] Image is in focus (not blurry due to scanner error)
- [ ] No visible dust spots larger than 3px at delivery resolution
- [ ] No Newton rings
- [ ] Color balance is neutral (no unexpected color cast from equipment)
- [ ] Image is cropped to the edges of the original (no black borders > 5px)
- [ ] Rotation is correct (subject appears upright)
- [ ] No scan lines or banding artifacts

### Color Restoration Notes

We do **not** automatically apply color restoration or enhancement beyond:
- Dust/scratch reduction via Epson Digital ICE
- Auto-levels (disabled by default — only enabled if customer requested it)

If a customer requests "restoration," flag the order for our manual restoration queue — do not
attempt this with automation tools.

---

## Video Captures

### Technical Specifications

| Setting | VHS/Beta | 8mm / Super 8 |
|---------|----------|---------------|
| Resolution | 720×480 (NTSC) | 1440×1080 upscaled |
| Frame rate | 29.97 fps | 18 fps (Standard 8) / 24 fps (Super 8) |
| Video codec | H.264 | H.264 |
| Audio codec | AAC 192kbps | AAC 192kbps (if audio present) |
| Container | MP4 | MP4 |

### Video Quality Checklist

- [ ] No dropped frames in the first and last 30 seconds
- [ ] Audio is present and at a reasonable level (not clipping, not silent unless tape had none)
- [ ] No OBS recording artifacts (frozen frames, black frames)
- [ ] File plays back completely in VLC without errors
- [ ] Duration matches the expected tape length (±30 seconds)

---

## Delivery Archive

- [ ] All processed files are present (count matches inventory)
- [ ] Folder structure follows the [naming convention](file-naming-conventions.md)
- [ ] No `.DS_Store`, `Thumbs.db`, or other system junk files included
- [ ] Archive ZIP opens without errors
- [ ] Total file size was logged in the job record

---

## Rejection Criteria

Return an item for rework if **any** of the following are true:

- A scan is visibly blurry (not due to the original photo being blurry)
- More than 5% of files in a batch have dust artifacts
- A video capture has more than 2 seconds of dropped/frozen frames
- Any file is corrupt or zero bytes
- File names do not follow the naming convention
