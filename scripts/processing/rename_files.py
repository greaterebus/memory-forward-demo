#!/usr/bin/env python3
"""
rename_files.py

Renames files in a job's processed/ folder to the Memory Forward naming convention:
    <JOB_ID>_<MEDIA_TYPE>_<SEQUENCE>.<EXT>

Usage:
    python rename_files.py --job-id <JOB_ID> [--media-type <CODE>] [--dry-run]

    --media-type  Limit renaming to one media type (PH, NG, SL, VH, FM).
                  Omit to rename everything.

Example:
    python rename_files.py --job-id MF240315
    python rename_files.py --job-id MF240315 --media-type PH --dry-run
"""

import argparse
import os
import re
import sys

JOBS_ROOT = r"\\mfshare\jobs"

SUBFOLDER_TO_CODE = {
    "photos": "PH",
    "negatives": "NG",
    "slides": "SL",
    "video": "VH",
}

VALID_CODES = {"PH", "NG", "SL", "VH", "FM", "OT"}


def already_named(filename: str, job_id: str) -> bool:
    """Return True if the file already follows the naming convention."""
    pattern = re.compile(rf"^{re.escape(job_id)}_[A-Z]{{2}}_\d{{4}}")
    return bool(pattern.match(filename))


def rename_folder(job_id: str, folder_path: str, media_code: str, dry_run: bool) -> int:
    files = sorted(
        f for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
        and not f.startswith(".")
        and not already_named(f, job_id)
    )

    renamed = 0
    for seq, fname in enumerate(files, start=1):
        ext = os.path.splitext(fname)[1].lower()
        new_name = f"{job_id}_{media_code}_{seq:04d}{ext}"
        src = os.path.join(folder_path, fname)
        dst = os.path.join(folder_path, new_name)

        if os.path.exists(dst):
            print(f"  SKIP (destination exists): {new_name}", file=sys.stderr)
            continue

        if dry_run:
            print(f"  [DRY RUN] {fname} → {new_name}")
        else:
            os.rename(src, dst)
            print(f"  Renamed: {fname} → {new_name}")
        renamed += 1

    return renamed


def main() -> None:
    parser = argparse.ArgumentParser(description="Rename processed files to naming convention.")
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--media-type", default=None, choices=list(VALID_CODES))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    processed_root = os.path.join(JOBS_ROOT, args.job_id, "processed")
    if not os.path.isdir(processed_root):
        print(f"ERROR: processed/ folder not found for job {args.job_id}", file=sys.stderr)
        sys.exit(1)

    total_renamed = 0

    for subfolder, code in SUBFOLDER_TO_CODE.items():
        if args.media_type and code != args.media_type:
            continue

        folder_path = os.path.join(processed_root, subfolder)
        if not os.path.isdir(folder_path):
            continue

        print(f"\nRenaming {subfolder}/ ({code}) ...")
        count = rename_folder(args.job_id, folder_path, code, args.dry_run)
        print(f"  {count} file(s) renamed.")
        total_renamed += count

    print(f"\nTotal renamed: {total_renamed}")


if __name__ == "__main__":
    main()
