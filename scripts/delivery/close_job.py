#!/usr/bin/env python3
"""
close_job.py

Marks a job as fully complete after originals have been shipped back to the customer.
Archives the job folder to cold storage and removes it from the active jobs drive.

Usage:
    python close_job.py --job-id <JOB_ID> [--tracking <RETURN_TRACKING_NUMBER>]

Example:
    python close_job.py --job-id MF240315 --tracking 9400111899223397614678
"""

import argparse
import datetime
import json
import os
import shutil
import sys

REGISTRY_PATH = r"\\mfshare\job_registry.json"
JOBS_ROOT = r"\\mfshare\jobs"
ARCHIVE_ROOT = r"\\mfarchive\completed_jobs"


def update_registry(job_id: str, tracking: str | None) -> None:
    with open(REGISTRY_PATH) as f:
        registry = json.load(f)

    for job in registry:
        if job["job_id"] == job_id:
            job["status"] = "COMPLETE"
            job["closed_at"] = datetime.datetime.now().isoformat()
            if tracking:
                job["return_tracking"] = tracking
            break

    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2)


def archive_job_folder(job_id: str, dry_run: bool) -> None:
    src = os.path.join(JOBS_ROOT, job_id)
    dst = os.path.join(ARCHIVE_ROOT, job_id)

    if dry_run:
        print(f"  [DRY RUN] Would move {src} → {dst}")
        return

    if not os.path.isdir(src):
        print(f"  WARNING: Job folder not found at {src} — skipping archive.", file=sys.stderr)
        return

    os.makedirs(ARCHIVE_ROOT, exist_ok=True)
    shutil.move(src, dst)
    print(f"  Job folder archived to: {dst}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Close a completed job.")
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--tracking", default=None, help="Return shipment tracking number")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print(f"\nClosing job {args.job_id} ...")

    if not args.dry_run:
        update_registry(args.job_id, args.tracking)
        print("  Registry updated → status: COMPLETE")

    archive_job_folder(args.job_id, args.dry_run)

    print(f"\nJob {args.job_id} is fully closed.")
    if args.tracking:
        print(f"Return tracking: {args.tracking}")


if __name__ == "__main__":
    main()
