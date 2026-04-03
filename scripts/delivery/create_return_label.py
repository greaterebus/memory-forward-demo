#!/usr/bin/env python3
"""
create_return_label.py

Generates a prepaid return shipping label for a customer's original media.
Uses the EasyPost API to create a USPS Priority Mail label.

Requires:
    pip install easypost

Usage:
    python create_return_label.py --job-id <JOB_ID>

Example:
    python create_return_label.py --job-id MF240315
"""

import argparse
import datetime
import json
import os
import sys

REGISTRY_PATH = r"\\mfshare\job_registry.json"
JOBS_ROOT = r"\\mfshare\jobs"
LABELS_DIR = r"\\mfshare\return_labels"

# Memory Forward return address
MF_ADDRESS = {
    "name": "Memory Forward",
    "street1": "4821 Archival Way",
    "city": "Portland",
    "state": "OR",
    "zip": "97201",
    "country": "US",
    "phone": "503-555-0192",
}

EASYPOST_API_KEY = os.environ.get("EASYPOST_API_KEY", "")


def load_job(job_id: str) -> dict:
    with open(REGISTRY_PATH) as f:
        registry = json.load(f)
    for job in registry:
        if job["job_id"] == job_id:
            return job
    print(f"ERROR: Job '{job_id}' not found.", file=sys.stderr)
    sys.exit(1)


def create_label(job: dict, dry_run: bool) -> str:
    """Create a return shipping label. Returns path to saved PDF."""
    job_id = job["job_id"]
    customer_address = job.get("return_address", {})

    if not customer_address:
        print("ERROR: No return address on file for this job.", file=sys.stderr)
        print("  Add 'return_address' to the job record and retry.", file=sys.stderr)
        sys.exit(1)

    label_path = os.path.join(LABELS_DIR, f"{job_id}_return_label.pdf")

    if dry_run:
        print(f"  [DRY RUN] Would create USPS Priority label:")
        print(f"    From: {MF_ADDRESS['name']}, {MF_ADDRESS['city']}, {MF_ADDRESS['state']}")
        print(f"    To:   {customer_address.get('name')}, {customer_address.get('city')}, {customer_address.get('state')}")
        print(f"    Output: {label_path}")
        return label_path

    # --- Real implementation with EasyPost ---
    # import easypost
    # easypost.api_key = EASYPOST_API_KEY
    #
    # shipment = easypost.Shipment.create(
    #     to_address=customer_address,
    #     from_address=MF_ADDRESS,
    #     parcel={"weight": job.get("estimated_weight_oz", 32)},
    # )
    # rate = shipment.lowest_rate(carriers=["USPS"], services=["Priority"])
    # shipment.buy(rate=rate)
    #
    # label_url = shipment.postage_label.label_url
    # # Download PDF ...
    # ---

    # Stub for demo
    os.makedirs(LABELS_DIR, exist_ok=True)
    with open(label_path, "wb") as f:
        f.write(b"%PDF-1.4 (demo label placeholder)")

    print(f"  Label created: {label_path}")
    return label_path


def update_registry(job_id: str, label_path: str) -> None:
    with open(REGISTRY_PATH) as f:
        registry = json.load(f)
    for job in registry:
        if job["job_id"] == job_id:
            job["return_label_path"] = label_path
            job["return_label_created_at"] = datetime.datetime.now().isoformat()
    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a prepaid return shipping label.")
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print(f"\nCreating return label for job {args.job_id} ...")
    job = load_job(args.job_id)
    label_path = create_label(job, args.dry_run)

    if not args.dry_run:
        update_registry(args.job_id, label_path)

    print(f"\nDone. Print the label and attach it to the return package.")
    print(f"Drop at the outgoing mail station before 3 PM for same-day pickup.")


if __name__ == "__main__":
    main()
