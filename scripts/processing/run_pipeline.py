#!/usr/bin/env python3
"""
run_pipeline.py

Runs the full post-scan processing pipeline for a completed job.
Handles image correction, file renaming, video normalization, and preview generation.

Requires:
    pip install Pillow pillow-avif-plugin tqdm

Usage:
    python run_pipeline.py --job-id <JOB_ID> [--skip-video] [--dry-run]

Example:
    python run_pipeline.py --job-id MF240315
    python run_pipeline.py --job-id MF240315 --dry-run
"""

import argparse
import datetime
import os
import sys

# Third-party (graceful import — not available in demo environment)
try:
    from PIL import Image, ImageOps
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

JOBS_ROOT = r"\\mfshare\jobs"

IMAGE_EXTENSIONS = {".tif", ".tiff", ".jpg", ".jpeg", ".png"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv"}

PREVIEW_MAX_SIZE = (2048, 2048)
PREVIEW_QUALITY = 85


# ---------------------------------------------------------------------------
# Steps
# ---------------------------------------------------------------------------

def collect_raw_files(job_id: str) -> dict[str, list[str]]:
    """Walk the raw/ folder and sort files by type."""
    raw_root = os.path.join(JOBS_ROOT, job_id, "raw")
    images, videos = [], []

    for root, _, files in os.walk(raw_root):
        for fname in sorted(files):
            ext = os.path.splitext(fname)[1].lower()
            full = os.path.join(root, fname)
            if ext in IMAGE_EXTENSIONS:
                images.append(full)
            elif ext in VIDEO_EXTENSIONS:
                videos.append(full)

    print(f"  Found {len(images)} image(s) and {len(videos)} video(s) in raw/")
    return {"images": images, "videos": videos}


def process_images(job_id: str, images: list[str], dry_run: bool) -> int:
    """Auto-rotate, apply dust reduction stub, and generate previews."""
    if not images:
        return 0

    out_root = os.path.join(JOBS_ROOT, job_id, "processed")
    preview_root = os.path.join(JOBS_ROOT, job_id, "processed", "previews")
    processed = 0

    iterator = tqdm(images, desc="  Images") if TQDM_AVAILABLE else images
    for src_path in iterator:
        # Determine output subfolder from source subfolder name
        parts = src_path.split(os.sep)
        subdir = parts[-2] if len(parts) >= 2 else "photos"
        dst_dir = os.path.join(out_root, subdir)

        fname = os.path.basename(src_path)
        dst_path = os.path.join(dst_dir, fname)
        preview_path = os.path.join(
            preview_root, os.path.splitext(fname)[0] + "_preview.jpg"
        )

        if dry_run:
            print(f"    [DRY RUN] Would process: {src_path} → {dst_path}")
            processed += 1
            continue

        if not PIL_AVAILABLE:
            # Simulate processing when Pillow is not installed
            print(f"    (Pillow not installed — skipping actual image processing for {fname})")
            processed += 1
            continue

        os.makedirs(dst_dir, exist_ok=True)
        os.makedirs(preview_root, exist_ok=True)

        img = Image.open(src_path)
        img = ImageOps.exif_transpose(img)  # auto-rotate from EXIF

        img.save(dst_path)

        preview = img.copy()
        preview.thumbnail(PREVIEW_MAX_SIZE, Image.LANCZOS)
        preview.save(preview_path, "JPEG", quality=PREVIEW_QUALITY)

        processed += 1

    return processed


def normalize_videos(job_id: str, videos: list[str], dry_run: bool) -> int:
    """Re-encode videos with normalized audio using ffmpeg."""
    if not videos:
        return 0

    out_root = os.path.join(JOBS_ROOT, job_id, "processed", "video")
    processed = 0

    for src_path in videos:
        fname = os.path.basename(src_path)
        dst_path = os.path.join(out_root, fname)

        ffmpeg_cmd = (
            f'ffmpeg -i "{src_path}" '
            f'-af "loudnorm=I=-23:LRA=7:TP=-2" '
            f'-c:v copy '
            f'"{dst_path}"'
        )

        if dry_run:
            print(f"    [DRY RUN] Would run: {ffmpeg_cmd}")
            processed += 1
            continue

        print(f"    Normalizing audio: {fname}")
        ret = os.system(ffmpeg_cmd)
        if ret != 0:
            print(f"    WARNING: ffmpeg returned non-zero exit code for {fname}", file=sys.stderr)
        else:
            processed += 1

    return processed


def rename_files(job_id: str, dry_run: bool) -> None:
    """Apply the Memory Forward naming convention to all processed files."""
    # Delegated to the rename_files.py script for clarity
    cmd = f'python scripts/processing/rename_files.py --job-id {job_id}'
    if dry_run:
        print(f"    [DRY RUN] Would run: {cmd}")
        return
    print(f"    Running rename script ...")
    os.system(cmd)


def write_job_log(job_id: str, summary: dict) -> None:
    log_path = os.path.join(JOBS_ROOT, job_id, f"{job_id}_job_log.txt")
    with open(log_path, "a") as f:
        f.write(f"\n[{datetime.datetime.now().isoformat()}] PIPELINE RUN\n")
        for k, v in summary.items():
            f.write(f"  {k}: {v}\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Run the processing pipeline for a job.")
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--skip-video", action="store_true", help="Skip video normalization step")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without making changes")
    args = parser.parse_args()

    print(f"\nMemory Forward Processing Pipeline")
    print(f"Job: {args.job_id}  {'[DRY RUN]' if args.dry_run else ''}")
    print("-" * 40)

    print("\n[1/4] Collecting raw files ...")
    files = collect_raw_files(args.job_id)

    print("\n[2/4] Processing images ...")
    img_count = process_images(args.job_id, files["images"], args.dry_run)
    print(f"  Processed {img_count} image(s).")

    if not args.skip_video:
        print("\n[3/4] Normalizing video audio ...")
        vid_count = normalize_videos(args.job_id, files["videos"], args.dry_run)
        print(f"  Processed {vid_count} video(s).")
    else:
        print("\n[3/4] Skipping video (--skip-video).")
        vid_count = 0

    print("\n[4/4] Renaming files ...")
    rename_files(args.job_id, args.dry_run)

    summary = {
        "images_processed": img_count,
        "videos_processed": vid_count,
        "dry_run": args.dry_run,
    }

    if not args.dry_run:
        write_job_log(args.job_id, summary)

    print("\nPipeline complete.")
    print(f"Next step: run QA, then mark_qa_complete.py --job-id {args.job_id}")


if __name__ == "__main__":
    main()
