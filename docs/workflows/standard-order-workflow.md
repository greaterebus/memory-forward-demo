---
layout: default
title: Standard Order Workflow
parent: Workflows
nav_order: 1
---

# Standard Order Workflow

This document describes the end-to-end process for a Memory Forward digitization order — from the
moment a customer's box arrives to the moment their digital archive is delivered.

---

## Overview

```
[1] Intake → [2] Inventory → [3] Scanning/Capture → [4] Processing → [5] QA → [6] Delivery → [7] Return Originals
```

---

## Step 1 — Intake

When a customer's package arrives at the facility:

1. Sign for the package and bring it to the **Intake Station**
2. Run the intake script to register the order:
   ```bash
   python scripts/intake/register_order.py --box-id <TRACKING_NUMBER>
   ```
3. The script will create a new job folder at `\\mfshare\jobs\<JOB_ID>\`
4. Attach the printed **Job ID label** (printed automatically) to the physical box
5. Place the box in the **Awaiting Inventory** shelf

---

## Step 2 — Inventory

Open the box and catalog every item inside:

1. Fill out the [Customer Intake Form](../../templates/customer-intake-form.md) for each order
2. Count and log every item by type:
   - Printed photos (count)
   - Film negatives (count strips/rolls)
   - 35mm slides (count)
   - VHS/Beta tapes (count)
   - 8mm/Super 8 reels (count)
   - Other (describe)
3. Photograph the contents before removing anything
4. Enter counts into the job record:
   ```bash
   python scripts/intake/log_inventory.py --job-id <JOB_ID>
   ```
5. Flag any damaged or unusually fragile items with a **red tag**

---

## Step 3 — Scanning / Capture

Route each media type to the correct technician/station:

| Media Type | Equipment | Settings Profile |
|------------|-----------|-----------------|
| Printed photos (≤4×6) | Epson V850, auto-feeder | `profile_photo_standard` |
| Printed photos (>4×6) | Epson V850, flatbed | `profile_photo_large` |
| 35mm negatives | Epson V850, film holder | `profile_35mm_neg` |
| 35mm slides | Epson V850, slide holder | `profile_35mm_slide` |
| Medium/large format negatives | Epson V850, film holder | `profile_mf_neg` |
| VHS / Beta tapes | Elgato capture card + VCR | `profile_vhs` |
| 8mm / Super 8 reels | Wolverine film scanner | `profile_8mm` |

All scans must be saved to `\\mfshare\jobs\<JOB_ID>\raw\`.

See [Scanning Best Practices](scanning-best-practices.md) for detailed equipment guides.

---

## Step 4 — Processing

After raw capture is complete, run the processing pipeline:

```bash
python scripts/processing/run_pipeline.py --job-id <JOB_ID>
```

This script will:
- Auto-rotate images based on EXIF data
- Apply dust and scratch reduction (photos/negatives only)
- Normalize video audio levels
- Generate web-quality preview versions
- Rename all files according to [naming conventions](../standards/file-naming-conventions.md)
- Build the folder structure for delivery

Output goes to `\\mfshare\jobs\<JOB_ID>\processed\`.

---

## Step 5 — Quality Assurance

Every order must pass QA before delivery:

1. Open the [Job Completion Checklist](../../templates/job-checklist.md)
2. Review a random sample of at least 10% of files (minimum 20 files)
3. Check each sample against [Quality Standards](../standards/quality-standards.md)
4. If QA fails, return the job to the relevant step with a note explaining what needs to be redone
5. Sign off on the checklist and update the job status:
   ```bash
   python scripts/processing/mark_qa_complete.py --job-id <JOB_ID> --tech-id <YOUR_ID>
   ```

---

## Step 6 — Delivery

Once QA is approved:

```bash
python scripts/delivery/package_and_upload.py --job-id <JOB_ID>
```

This will:
- Zip the processed archive
- Upload to the customer's private portal folder
- Send the customer an automated email with their download link
- Log the delivery timestamp

For customers who requested a USB drive or DVD, see [Physical Delivery Process](physical-delivery.md).

---

## Step 7 — Return Originals

All original media is returned to the customer:

1. Re-package originals carefully in the original materials (or acid-free replacements if originals
   were damaged)
2. Run the return shipping script:
   ```bash
   python scripts/delivery/create_return_label.py --job-id <JOB_ID>
   ```
3. Drop the package at the outgoing mail station before 3 PM for same-day pickup
4. Mark the job as fully complete:
   ```bash
   python scripts/delivery/close_job.py --job-id <JOB_ID>
   ```

---

## Job Status Reference

| Status Code | Meaning |
|-------------|---------|
| `RECEIVED` | Box arrived, not yet inventoried |
| `INVENTORY` | Being catalogued |
| `SCANNING` | Active scanning/capture in progress |
| `PROCESSING` | Pipeline running |
| `QA` | Awaiting or in QA review |
| `QA_FAIL` | Returned for rework |
| `DELIVERY` | Upload/shipping in progress |
| `COMPLETE` | Delivered and originals returned |
