#!/usr/bin/env python3
"""
log_inventory.py

Interactive CLI for recording the physical inventory of items in a customer's box.
Run this after opening the box and before any scanning begins.

Usage:
    python log_inventory.py --job-id <JOB_ID>

Example:
    python log_inventory.py --job-id MF240315
"""

import argparse
import datetime
import json
import os
import sys

JOBS_ROOT = r"\\mfshare\jobs"

MEDIA_TYPES = {
    "1": ("printed_photos", "Printed photos"),
    "2": ("negatives_35mm", "35mm negatives (strips/rolls)"),
    "3": ("slides_35mm", "35mm slides"),
    "4": ("vhs_tapes", "VHS / Beta tapes"),
    "5": ("film_8mm", "8mm / Super 8 reels"),
    "6": ("other", "Other (describe below)"),
}


def load_registry(job_id: str) -> dict:
    registry_path = r"\\mfshare\job_registry.json"
    if not os.path.exists(registry_path):
        print(f"ERROR: Job registry not found at {registry_path}", file=sys.stderr)
        sys.exit(1)

    with open(registry_path) as f:
        registry = json.load(f)

    for job in registry:
        if job["job_id"] == job_id:
            return job

    print(f"ERROR: Job ID '{job_id}' not found in registry.", file=sys.stderr)
    sys.exit(1)


def prompt_inventory() -> dict:
    print("\n--- Inventory Entry ---")
    print("Enter the count for each media type (press Enter to skip / enter 0):\n")

    inventory = {}
    for key, (field, label) in MEDIA_TYPES.items():
        raw = input(f"  [{key}] {label}: ").strip()
        if not raw:
            continue
        if field == "other":
            desc = input("      Description: ").strip()
            count = int(input("      Count: ").strip() or "0")
            inventory[field] = {"count": count, "description": desc}
        else:
            try:
                inventory[field] = int(raw)
            except ValueError:
                print(f"      (invalid input, skipping {label})")

    fragile = input("\nAny items flagged as damaged/fragile? (y/n): ").strip().lower()
    notes = ""
    if fragile == "y":
        notes = input("  Describe damaged/fragile items: ").strip()

    return {"items": inventory, "fragile_notes": notes}


def save_inventory(job_id: str, inventory: dict) -> None:
    inventory_path = os.path.join(JOBS_ROOT, job_id, f"{job_id}_inventory.json")
    payload = {
        "job_id": job_id,
        "logged_at": datetime.datetime.now().isoformat(),
        "inventory": inventory,
    }
    with open(inventory_path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\nInventory saved to: {inventory_path}")


def update_status(job_id: str) -> None:
    registry_path = r"\\mfshare\job_registry.json"
    with open(registry_path) as f:
        registry = json.load(f)
    for job in registry:
        if job["job_id"] == job_id:
            job["status"] = "INVENTORY"
    with open(registry_path, "w") as f:
        json.dump(registry, f, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Log inventory for an incoming order.")
    parser.add_argument("--job-id", required=True)
    args = parser.parse_args()

    job = load_registry(args.job_id)
    print(f"\nLogging inventory for Job {args.job_id}")
    print(f"  Tracking number : {job['tracking_number']}")
    print(f"  Customer ID     : {job.get('customer_id', 'N/A')}")
    print(f"  Received at     : {job['received_at']}")

    inventory = prompt_inventory()
    save_inventory(args.job_id, inventory)
    update_status(args.job_id)

    total = sum(
        v if isinstance(v, int) else v.get("count", 0)
        for v in inventory["items"].values()
    )
    print(f"\nTotal items logged: {total}")
    print("Job status updated to INVENTORY.")
    print("Move the box to the appropriate scanning station.")


if __name__ == "__main__":
    main()
