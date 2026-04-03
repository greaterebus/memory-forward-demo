# Job Completion Checklist

> Complete this checklist during the QA step (Step 5) before any job is delivered.
> Save a filled-out copy to `\\mfshare\jobs\<JOB_ID>\<JOB_ID>_qa_checklist.md`.

---

## Job Info

| Field | Value |
|-------|-------|
| **Job ID** | |
| **QA Technician** | |
| **QA Date** | |
| **Total files delivered** | |

---

## 1. File Count Verification

- [ ] File count in `processed/` matches the inventory count from intake
- [ ] No zero-byte files present
- [ ] No duplicate files (same content, different names)

**Expected count:** ________  
**Actual count:** ________

---

## 2. File Naming

- [ ] All files follow the `<JOB_ID>_<TYPE>_<SEQ>.<EXT>` naming convention
- [ ] No spaces or special characters in filenames
- [ ] Sequence numbers are unique within each media type

---

## 3. Image Quality Sample

Sample at least 10% of image files (minimum 20). Check each sample against the table.

| # | Filename | In Focus | No Dust | No Color Cast | Correct Rotation | Pass/Fail |
|---|----------|----------|---------|---------------|-----------------|-----------|
| 1 | | ☐ | ☐ | ☐ | ☐ | |
| 2 | | ☐ | ☐ | ☐ | ☐ | |
| 3 | | ☐ | ☐ | ☐ | ☐ | |
| 4 | | ☐ | ☐ | ☐ | ☐ | |
| 5 | | ☐ | ☐ | ☐ | ☐ | |
| 6 | | ☐ | ☐ | ☐ | ☐ | |
| 7 | | ☐ | ☐ | ☐ | ☐ | |
| 8 | | ☐ | ☐ | ☐ | ☐ | |
| 9 | | ☐ | ☐ | ☐ | ☐ | |
| 10 | | ☐ | ☐ | ☐ | ☐ | |

_Add rows as needed for larger samples._

---

## 4. Video Quality Sample

Review the first and last 2 minutes of each video file.

| # | Filename | Plays Without Error | Audio Present | No Freeze Frames | Duration Correct | Pass/Fail |
|---|----------|---------------------|--------------|-----------------|-----------------|-----------|
| 1 | | ☐ | ☐ | ☐ | ☐ | |
| 2 | | ☐ | ☐ | ☐ | ☐ | |
| 3 | | ☐ | ☐ | ☐ | ☐ | |

---

## 5. Delivery Archive

- [ ] `delivery/<JOB_ID>_archive.zip` exists
- [ ] ZIP opens without errors
- [ ] Folder structure inside ZIP matches the standard layout
- [ ] No `.DS_Store`, `Thumbs.db`, or temporary files included
- [ ] Archive file size is reasonable (logged in job record)

---

## 6. Final Sign-Off

**Overall result:**
- [ ] PASS — job is approved for delivery
- [ ] FAIL — job requires rework (document issues below)

**Issues requiring rework:**

```
(describe any failures here, including which files or batches need to be redone)
```

**Rework assigned to:** ____________________________

---

**QA Technician Signature:** ____________________________  
**Date:** ____________________________
