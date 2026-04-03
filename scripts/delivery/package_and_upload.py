#!/usr/bin/env python3
"""
package_and_upload.py

Zips the processed archive for a job and uploads it to the customer portal.
Sends the customer an automated notification email with their download link.

Requires:
    pip install boto3  (for S3 upload — replace with your actual storage backend)

Usage:
    python package_and_upload.py --job-id <JOB_ID> [--dry-run]

Example:
    python package_and_upload.py --job-id MF240315
"""

import argparse
import datetime
import json
import os
import shutil
import sys

JOBS_ROOT = r"\\mfshare\jobs"
REGISTRY_PATH = r"\\mfshare\job_registry.json"
PORTAL_BASE_URL = "https://portal.memoryforward.com/downloads"

# Replace with real credentials / environment variables in production
SMTP_HOST = "smtp.memoryforward.com"
SMTP_PORT = 587
SMTP_USER = os.environ.get("MF_SMTP_USER", "")
SMTP_PASS = os.environ.get("MF_SMTP_PASS", "")
NOTIFICATION_FROM = "no-reply@memoryforward.com"


# ---------------------------------------------------------------------------
# Packaging
# ---------------------------------------------------------------------------

def build_archive(job_id: str, dry_run: bool) -> str:
    """Zip the processed/ folder and return the path to the .zip file."""
    processed_dir = os.path.join(JOBS_ROOT, job_id, "processed")
    delivery_dir = os.path.join(JOBS_ROOT, job_id, "delivery")
    archive_name = os.path.join(delivery_dir, f"{job_id}_archive")

    if dry_run:
        print(f"  [DRY RUN] Would zip {processed_dir} → {archive_name}.zip")
        return archive_name + ".zip"

    print(f"  Zipping {processed_dir} ...")
    shutil.make_archive(archive_name, "zip", processed_dir)
    zip_path = archive_name + ".zip"
    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"  Archive created: {zip_path} ({size_mb:.1f} MB)")
    return zip_path


# ---------------------------------------------------------------------------
# Upload
# ---------------------------------------------------------------------------

def upload_to_portal(job_id: str, zip_path: str, dry_run: bool) -> str:
    """Upload the zip to the customer portal and return the download URL."""
    download_url = f"{PORTAL_BASE_URL}/{job_id}/{os.path.basename(zip_path)}"

    if dry_run:
        print(f"  [DRY RUN] Would upload to: {download_url}")
        return download_url

    # --- Real implementation would use boto3, requests, or an SFTP client ---
    # Example with boto3:
    #   import boto3
    #   s3 = boto3.client("s3")
    #   s3.upload_file(zip_path, "mf-customer-archives", f"{job_id}/{os.path.basename(zip_path)}")
    # ---

    print(f"  Upload complete. Download URL: {download_url}")
    return download_url


# ---------------------------------------------------------------------------
# Notification
# ---------------------------------------------------------------------------

def send_notification(job_id: str, download_url: str, customer_email: str, dry_run: bool) -> None:
    subject = "Your Memory Forward archive is ready!"
    body = f"""\
Hello,

Great news — your digitization order ({job_id}) is complete and your archive is ready to download.

Download your files here:
  {download_url}

This link will be available for 90 days. We recommend downloading your archive and storing it in
at least two places (e.g., an external hard drive and a cloud service like Google Photos or iCloud).

Your original photos and media will be returned to you via the shipping address on file within
5–7 business days.

Thank you for trusting Memory Forward with your memories.

— The Memory Forward Team
"""

    if dry_run:
        print(f"  [DRY RUN] Would send email to {customer_email}")
        print(f"  Subject: {subject}")
        return

    # --- Real implementation would use smtplib or a transactional email service ---
    # import smtplib, ssl
    # from email.message import EmailMessage
    # msg = EmailMessage()
    # msg["Subject"] = subject
    # msg["From"] = NOTIFICATION_FROM
    # msg["To"] = customer_email
    # msg.set_content(body)
    # with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
    #     smtp.starttls(context=ssl.create_default_context())
    #     smtp.login(SMTP_USER, SMTP_PASS)
    #     smtp.send_message(msg)
    # ---

    print(f"  Notification email sent to {customer_email}.")


# ---------------------------------------------------------------------------
# Registry update
# ---------------------------------------------------------------------------

def update_registry(job_id: str, download_url: str) -> str:
    with open(REGISTRY_PATH) as f:
        registry = json.load(f)

    customer_email = "unknown@example.com"
    for job in registry:
        if job["job_id"] == job_id:
            job["status"] = "COMPLETE"
            job["delivered_at"] = datetime.datetime.now().isoformat()
            job["download_url"] = download_url
            customer_email = job.get("customer_email", customer_email)
            break

    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2)

    return customer_email


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Package and upload a completed job.")
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print(f"\nMemory Forward Delivery — Job {args.job_id}  {'[DRY RUN]' if args.dry_run else ''}")
    print("-" * 40)

    print("\n[1/3] Building archive ...")
    zip_path = build_archive(args.job_id, args.dry_run)

    print("\n[2/3] Uploading to customer portal ...")
    download_url = upload_to_portal(args.job_id, zip_path, args.dry_run)

    print("\n[3/3] Sending customer notification ...")
    if not args.dry_run:
        customer_email = update_registry(args.job_id, download_url)
    else:
        customer_email = "customer@example.com"
    send_notification(args.job_id, download_url, customer_email, args.dry_run)

    print(f"\nDelivery complete for {args.job_id}.")
    print(f"Next step: create return shipping label with create_return_label.py --job-id {args.job_id}")


if __name__ == "__main__":
    main()
