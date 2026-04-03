#!/usr/bin/env python3
"""
register_order.py

Registers a new incoming customer order when a package arrives at the facility.
Creates the job folder structure on the shared drive and prints a job ID label.

Usage:
    python register_order.py --box-id <TRACKING_NUMBER> [--customer-id <CID>]

Example:
    python register_order.py --box-id 1Z999AA10123456784
"""

import argparse
import datetime
import json
import os
import random
import string
import sys

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
JOBS_ROOT = r"\\mfshare\jobs"
JOB_LOG_FILE = r"\\mfshare\job_registry.json"
JOB_ID_PREFIX = "MF"

RAW_SUBFOLDERS = ["photos", "negatives", "slides", "video"]
PROCESSED_SUBFOLDERS = ["photos", "negatives", "slides", "video", "previews"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def generate_job_id() -> str:
    """Generate a unique 8-character job ID, e.g. MF240315."""
    date_part = datetime.date.today().strftime("%y%m%d")
    rand_part = "".join(random.choices(string.digits, k=2))
    return f"{JOB_ID_PREFIX}{date_part}{rand_part}"


def create_job_folders(job_id: str) -> str:
    """Create the standard folder tree for a new job. Returns the root path."""
    job_root = os.path.join(JOBS_ROOT, job_id)

    folders = (
        [os.path.join(job_root, "raw", sub) for sub in RAW_SUBFOLDERS]
        + [os.path.join(job_root, "processed", sub) for sub in PROCESSED_SUBFOLDERS]
        + [os.path.join(job_root, "delivery")]
    )

    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    return job_root


def register_in_log(job_id: str, tracking_number: str, customer_id: str | None) -> None:
    """Append this job to the central registry JSON file."""
    registry = []
    if os.path.exists(JOB_LOG_FILE):
        with open(JOB_LOG_FILE, "r") as f:
            registry = json.load(f)

    registry.append(
        {
            "job_id": job_id,
            "tracking_number": tracking_number,
            "customer_id": customer_id,
            "status": "RECEIVED",
            "received_at": datetime.datetime.now().isoformat(),
            "technician": None,
        }
    )

    with open(JOB_LOG_FILE, "w") as f:
        json.dump(registry, f, indent=2)


def print_label(job_id: str, tracking_number: str) -> None:
    """Simulate sending a print job to the label printer."""
    print("=" * 40)
    print("         MEMORY FORWARD")
    print(f"  Job ID: {job_id}")
    print(f"  Tracking: {tracking_number}")
    print(f"  Received: {datetime.date.today().isoformat()}")
    print("  Status: RECEIVED")
    print("=" * 40)
    print("[Label sent to printer]")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Register a new incoming order.")
    parser.add_argument("--box-id", required=True, help="Carrier tracking number on the box")
    parser.add_argument("--customer-id", default=None, help="Optional customer account ID")
    args = parser.parse_args()

    job_id = generate_job_id()
    print(f"Creating job {job_id} for tracking number {args.box_id} ...")

    try:
        job_root = create_job_folders(job_id)
        print(f"  Folder created: {job_root}")
    except OSError as e:
        print(f"ERROR: Could not create job folder: {e}", file=sys.stderr)
        sys.exit(1)

    register_in_log(job_id, args.box_id, args.customer_id)
    print(f"  Registered in job log.")

    print_label(job_id, args.box_id)
    print(f"\nDone. Place box in 'Awaiting Inventory' shelf with label attached.")


if __name__ == "__main__":
    main()
