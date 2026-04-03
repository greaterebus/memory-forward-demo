#!/usr/bin/env python3
"""
mark_qa_complete.py

Records QA sign-off for a completed job and advances the job status to DELIVERY.

Usage:
    python mark_qa_complete.py --job-id <JOB_ID> --tech-id <YOUR_EMPLOYEE_ID>

Example:
    python mark_qa_complete.py --job-id MF240315 --tech-id TECH04
"""

import argparse
import datetime
import json
import os
import sys

JOBS_ROOT = r"\\mfshare\jobs"
REGISTRY_PATH = r"\\mfshare\job_registry.json"


def update_registry(job_id: str, tech_id: str) -> None:
    with open(REGISTRY_PATH) as f:
        registry = json.load(f)

    found = False
    for job in registry:
        if job["job_id"] == job_id:
            if job["status"] not in ("QA", "PROCESSING", "SCANNING"):
                print(
                    f"WARNING: Job status is '{job['status']}' — expected QA/PROCESSING/SCANNING. "
                    "Proceeding anyway.",
                    file=sys.stderr,
                )
            job["status"] = "DELIVERY"
            job["qa_approved_by"] = tech_id
            job["qa_approved_at"] = datetime.datetime.now().isoformat()
            found = True
            break

    if not found:
        print(f"ERROR: Job ID '{job_id}' not found.", file=sys.stderr)
        sys.exit(1)

    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2)


def append_job_log(job_id: str, tech_id: str) -> None:
    log_path = os.path.join(JOBS_ROOT, job_id, f"{job_id}_job_log.txt")
    with open(log_path, "a") as f:
        f.write(
            f"\n[{datetime.datetime.now().isoformat()}] QA APPROVED by {tech_id}\n"
            f"  Status advanced to: DELIVERY\n"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Mark a job as QA approved.")
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--tech-id", required=True, help="Your employee/technician ID")
    args = parser.parse_args()

    print(f"Recording QA approval for job {args.job_id} by {args.tech_id} ...")
    update_registry(args.job_id, args.tech_id)
    append_job_log(args.job_id, args.tech_id)

    print(f"  Status set to DELIVERY.")
    print(f"Next step: run  package_and_upload.py --job-id {args.job_id}")


if __name__ == "__main__":
    main()
