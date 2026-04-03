# Scanning Best Practices

Consistent, high-quality scans are the core of what we deliver. Follow these guidelines for every
order.

---

## General Rules

- Always wear **anti-static gloves** when handling negatives, slides, or original prints
- Clean the scanner glass before every new order with a lint-free cloth
- Never use household glass cleaner — use only the approved optical cleaning solution
- Keep food and drinks away from all scanning equipment
- If a scan looks wrong, **stop and ask** — never guess

---

## Printed Photos

### Settings
- **Resolution:** 600 DPI (minimum); 1200 DPI for photos smaller than 3×3 inches
- **Color mode:** 48-bit color (24-bit acceptable for black & white originals)
- **File format:** TIFF for raw scans, JPEG (quality 95) for delivery copies

### Procedure
1. Wipe each photo gently with a soft brush to remove loose dust before placing on the glass
2. Lay photos face-down, aligned to the corner guides
3. For auto-feeder batches, do not exceed 30 photos at a time
4. Preview the scan and check for skew — correct if more than 1 degree off
5. Name files immediately after scanning using the [naming convention](../standards/file-naming-conventions.md)

### Common Issues
| Problem | Cause | Fix |
|---------|-------|-----|
| Faded colors | Old photo paper | Flag for color restoration in processing notes |
| Newton rings | Photo touching glass too tightly | Place a thin transparency sheet underneath |
| Blurry scan | Dirty glass | Clean glass, rescan |

---

## 35mm Negatives

### Settings
- **Resolution:** 2400 DPI (standard); 4800 DPI for enlargements requested by customer
- **Color mode:** 48-bit color; 16-bit grayscale for B&W negatives
- **File format:** TIFF

### Procedure
1. Identify negative format (color, B&W, slide) and load the correct holder
2. Load strips of 6 frames at a time — do not force curled negatives
3. Use the Epson Scan "Film" mode with negative inversion enabled
4. Preview the full strip before committing to the final scan
5. For severely curled negatives, place in the humidification cabinet for 30 minutes first (ask a
   senior technician before doing this)

---

## 35mm Slides

### Settings
- **Resolution:** 2400 DPI
- **Color mode:** 48-bit color
- **File format:** TIFF

### Procedure
1. Remove slides from mounts carefully; scan in the slide holder (not loose on the glass)
2. Dust slides with compressed air before loading
3. Scan batches of 4 at a time
4. Mark any cracked or broken mounts on the inventory sheet

---

## VHS / Beta Tapes

### Equipment Setup
- Rewind all tapes fully before playback
- Use the cleaning tape before processing every 10th order or if playback looks degraded
- Connect the VCR output to the Elgato HD60 S+ capture card via composite (yellow/red/white)
- Use OBS Studio with the `MemFwd_VHS_Capture` profile

### Procedure
1. Label the tape with the job ID on a removable sticker before putting it in the deck
2. Start OBS recording, then press Play on the VCR
3. Monitor the first 30 seconds for tracking issues — adjust the VCR tracking dial if needed
4. Let the tape play to the end; do not pause or stop unless the tape is clearly blank
5. Stop OBS recording and verify the file was saved to the correct raw folder

### Common Issues
| Problem | Cause | Fix |
|---------|-------|-----|
| Snowy/static image | Dirty heads | Run cleaning tape |
| Wavy horizontal lines | Tracking problem | Adjust VCR tracking dial |
| No audio | Wrong cable | Check composite audio connectors |
| Tape eats | Old/stretched tape | Do NOT force — alert senior tech |

---

## 8mm / Super 8 Film

> All 8mm and Super 8 work must be performed by a senior technician or under direct supervision.

### Procedure
1. Inspect the reel for mold, brittleness, or vinegar syndrome before loading
   - Mold: white fuzzy spots → quarantine and alert Operations Lead immediately
   - Vinegar smell: acetic acid degradation → scan immediately, do not store
2. Load the reel onto the Wolverine Pro film scanner
3. Select the correct film type in the Wolverine software (8mm vs. Super 8)
4. Run a test capture of the first 30 seconds and review before full scan
5. Raw output goes to `\\mfshare\jobs\<JOB_ID>\raw\video\`
