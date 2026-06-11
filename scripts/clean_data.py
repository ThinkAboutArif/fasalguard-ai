"""
clean_data.py
FasalGuard AI - Phase 2: Data Cleaning

WHY THIS SCRIPT EXISTS:
Before we train our AI model, we must remove bad images from our dataset.
Bad images = corrupt files, images that are too small to learn from,
or images that are too blurry to see the disease clearly.
If we train on bad images, the model will learn wrong patterns.

WHAT THIS SCRIPT DOES:
1. Scans every image in data/processed/ (all 38 class folders)
2. Checks each image for 3 problems:
   a) CORRUPT - can PIL open it? If not, move it out.
   b) TOO SMALL - is it under 100x100 pixels? If yes, move it out.
   c) TOO BLURRY - does Laplacian variance fall below 50? If yes, move it out.
3. Moves ALL rejected images to data/rejected/ (never deletes permanently)
4. Prints a summary table showing how many were removed per class and why.

HOW TO RUN:
   cd C:/Users/dhhdb/Desktop/fasalguard
   python scripts/clean_data.py

IMPORTANT: This script only MOVES files. It never deletes.
If something goes wrong, you can always copy them back from data/rejected/.
"""

# ============================================================================
# STEP 1: IMPORT LIBRARIES
# ============================================================================

# os - lets us work with folders and file paths (create folders, move files, list files)
import os

# shutil - provides "move file" and "copy file" functions that work across drives
import shutil

# PIL (Pillow) - Python Imaging Library. Lets us open images, check their size, convert formats.
from PIL import Image

# cv2 - OpenCV. A powerful computer vision library. We use it to detect blur.
import cv2

# numpy - handles arrays and numbers efficiently. OpenCV images are numpy arrays.
import numpy as np

# collections - provides Counter, a handy tool to count things automatically.
from collections import Counter

# ============================================================================
# STEP 2: DEFINE PATHS
# ============================================================================

# os.path.join() builds correct paths for Windows (uses backslashes) or Linux (uses slashes).
# We use it so the script works on any computer.

# BASE_DIR: The root folder of our entire project.
# __file__ is the path to THIS script file (clean_data.py).
# os.path.dirname(__file__) gets the folder containing this script -> scripts/
# os.path.dirname(scripts/) goes UP one level -> the project root folder.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SOURCE_DIR: Where our clean, organised images currently live.
# This was created in Phase 1 by organise_data.py.
SOURCE_DIR = os.path.join(BASE_DIR, "data", "processed")

# REJECTED_DIR: Where bad images will be MOVED (not deleted).
# We create subfolders inside here matching the class names so we know where each came from.
REJECTED_DIR = os.path.join(BASE_DIR, "data", "rejected")

# ============================================================================
# STEP 3: CREATE REJECTED FOLDER IF IT DOESN'T EXIST
# ============================================================================

# os.makedirs() creates a folder AND any parent folders that don't exist yet.
# exist_ok=True means: "If the folder already exists, don't crash - just keep going."
# This is safe to run multiple times.
os.makedirs(REJECTED_DIR, exist_ok=True)

# ============================================================================
# STEP 4: DEFINE THRESHOLDS (rules for what counts as "bad")
# ============================================================================

MIN_WIDTH = 100       # Minimum width in pixels. Anything narrower gets moved out.
MIN_HEIGHT = 100      # Minimum height in pixels. Anything shorter gets moved out.
BLUR_THRESHOLD = 50   # Laplacian variance below this = too blurry. Higher = stricter.

# ============================================================================
# STEP 5: HELPER FUNCTIONS
# ============================================================================

def is_corrupt(image_path):
    """
    Check if an image file is corrupt (cannot be opened).

    WHY: Sometimes downloaded datasets contain broken files, zero-byte files,
         or files with wrong extensions. PIL will crash trying to open these.

    HOW: We try to open the image with PIL.Image.open().
         If it succeeds, we also call .verify() which does a deeper check.
         If ANY error happens, we return True (it IS corrupt).

    Args:
        image_path: Full path to the image file (e.g., ".../tomato_healthy/img_001.jpg")

    Returns:
        True if the image is corrupt, False if it opens fine.
    """
    try:
        # Try to open the image file
        with Image.open(image_path) as img:
            # .verify() checks the file structure without loading pixel data (fast)
            img.verify()
        return False  # If we get here, the image is fine
    except Exception:
        # Exception catches ANY error (file not found, wrong format, truncated file, etc.)
        return True   # The image is corrupt


def is_too_small(image_path):
    """
    Check if an image is smaller than our minimum size.

    WHY: Very small images (like 50x50 pixels) don't have enough detail
         for the AI to learn what diseases look like. We need at least 100x100.

    HOW: Open the image with PIL, read its .size property (width, height).
         Compare against MIN_WIDTH and MIN_HEIGHT.

    Args:
        image_path: Full path to the image file.

    Returns:
        True if width < 100 OR height < 100, False otherwise.
    """
    try:
        with Image.open(image_path) as img:
            width, height = img.size  # .size returns a tuple: (width, height)
            # Return True if EITHER dimension is too small
            return width < MIN_WIDTH or height < MIN_HEIGHT
    except Exception:
        # If we can't even read the size, treat it as bad (too small + corrupt)
        return True


def is_blurry(image_path):
    """
    Check if an image is too blurry using the Laplacian variance method.

    WHY: Blurry images hide the disease symptoms. The AI can't learn from a blur.
         We need sharp, clear leaf photos.

    HOW LAPLACIAN VARIANCE WORKS:
         1. Convert image to grayscale (colour doesn't matter for sharpness).
         2. Apply the Laplacian filter - this detects edges (sharp changes in brightness).
         3. Calculate the VARIANCE of the result.
            - Sharp image = lots of edges = high variance (above 50).
            - Blurry image = few edges = low variance (below 50).

    Args:
        image_path: Full path to the image file.

    Returns:
        True if Laplacian variance < 50 (too blurry), False otherwise.
    """
    try:
        # cv2.imread() loads the image as a numpy array of pixels.
        # cv2.IMREAD_COLOR means load as colour (3 channels: Blue, Green, Red).
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)

        # If cv2.imread() fails, it returns None (happens with some corrupt files)
        if img is None:
            return True

        # cv2.cvtColor converts the image from BGR (OpenCV's default) to GRAYSCALE.
        # Grayscale has 1 channel instead of 3, which is all we need for blur detection.
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # cv2.Laplacian applies the edge-detection filter.
        # cv2.CV_64F means use 64-bit floating point numbers for precision.
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)

        # np.var() calculates the variance (how spread out the numbers are).
        # High variance = lots of edges = sharp image.
        # Low variance = flat/smooth = blurry image.
        variance = np.var(laplacian)

        # Return True if the image is blurrier than our threshold
        return variance < BLUR_THRESHOLD

    except Exception:
        # If ANY error happens during blur check, treat image as bad
        return True


def move_to_rejected(image_path, class_name, reason):
    """
    Move a bad image from data/processed/ to data/rejected/.

    WHY: We NEVER delete images permanently. If the script makes a mistake,
         we can always move images back manually.

    HOW: 
         1. Create a subfolder inside rejected/ with the class name.
         2. Create a sub-subfolder with the reason (corrupt, too_small, blurry).
         3. Move the file there using shutil.move().

    Args:
        image_path: Full path to the original image.
        class_name: Name of the class folder (e.g., "tomato_healthy").
        reason: Why it was rejected ("corrupt", "too_small", or "blurry").

    Returns:
        The destination path where the file was moved.
    """
    # Build the destination folder path: rejected/tomato_healthy/corrupt/
    dest_folder = os.path.join(REJECTED_DIR, class_name, reason)

    # Create the folder (and any parent folders) if they don't exist
    os.makedirs(dest_folder, exist_ok=True)

    # os.path.basename() gets just the filename from the full path.
    # Example: "C:/.../tomato_healthy/img_001.jpg" -> "img_001.jpg"
    filename = os.path.basename(image_path)

    # Build the full destination path
    dest_path = os.path.join(dest_folder, filename)

    # shutil.move() moves the file from source to destination.
    # If source and destination are on the same drive, it's instant (just renames).
    # If different drives, it copies then deletes original.
    shutil.move(image_path, dest_path)

    return dest_path


# ============================================================================
# STEP 6: MAIN CLEANING LOOP
# ============================================================================

def main():
    """
    The main function that runs the entire cleaning process.

    WHAT IT DOES:
    1. Lists all class folders in data/processed/
    2. For each class, scans every image file
    3. Runs the 3 checks (corrupt, too_small, blurry) in order
    4. Moves bad images to data/rejected/
    5. Prints a detailed summary
    """

    print("=" * 70)
    print("FASALGUARD AI - DATA CLEANING SCRIPT")
    print("=" * 70)
    print(f"\nSource folder: {SOURCE_DIR}")
    print(f"Rejected folder: {REJECTED_DIR}")
    print(f"\nThresholds:")
    print(f"  - Minimum size: {MIN_WIDTH}x{MIN_HEIGHT} pixels")
    print(f"  - Blur threshold: Laplacian variance < {BLUR_THRESHOLD}")
    print("=" * 70)

    # ------------------------------------------------------------------------
    # 6a. Find all class folders
    # ------------------------------------------------------------------------

    # os.listdir() returns a list of ALL items in a folder (files + folders).
    # We filter to keep only folders (directories) using os.path.isdir().
    class_folders = [
        name for name in os.listdir(SOURCE_DIR)
        if os.path.isdir(os.path.join(SOURCE_DIR, name))
    ]

    # Sort alphabetically so the output is easy to read
    class_folders.sort()

    print(f"\nFound {len(class_folders)} class folders to scan.\n")

    # ------------------------------------------------------------------------
    # 6b. Data structures to track what we find
    # ------------------------------------------------------------------------

    # total_counts: key = class name, value = number of images in that class
    total_counts = {}

    # rejected_counts: key = class name, value = dict of {reason: count}
    rejected_counts = {}

    # grand_totals: overall counts across ALL classes
    grand_totals = Counter()

    # ------------------------------------------------------------------------
    # 6c. Loop through each class folder
    # ------------------------------------------------------------------------

    for class_name in class_folders:
        # Build the full path to this class folder
        class_path = os.path.join(SOURCE_DIR, class_name)

        # Get a list of all files in this folder
        # os.listdir() returns everything; we filter for image files later
        all_files = os.listdir(class_path)

        # Filter to keep only likely image files.
        # We check the file extension (the part after the last dot).
        # .lower() makes it case-insensitive (.JPG and .jpg both work).
        image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp")
        image_files = [
            f for f in all_files
            if f.lower().endswith(image_extensions)
        ]

        total_images = len(image_files)
        total_counts[class_name] = total_images
        rejected_counts[class_name] = Counter()

        print(f"[{class_name}] Scanning {total_images} images...")

        # ----------------------------------------------------------------
        # 6d. Loop through each image in this class
        # ----------------------------------------------------------------

        for filename in image_files:
            # Build the full path to this image
            image_path = os.path.join(class_path, filename)

            # Skip if it's not actually a file (safety check)
            if not os.path.isfile(image_path):
                continue

            # ============================================================
            # CHECK 1: CORRUPT?
            # ============================================================
            if is_corrupt(image_path):
                # Move to rejected/<class>/corrupt/
                move_to_rejected(image_path, class_name, "corrupt")
                rejected_counts[class_name]["corrupt"] += 1
                grand_totals["corrupt"] += 1
                continue  # Skip the other checks - already moved

            # ============================================================
            # CHECK 2: TOO SMALL?
            # ============================================================
            if is_too_small(image_path):
                move_to_rejected(image_path, class_name, "too_small")
                rejected_counts[class_name]["too_small"] += 1
                grand_totals["too_small"] += 1
                continue  # Skip blur check - already moved

            # ============================================================
            # CHECK 3: TOO BLURRY?
            # ============================================================
            if is_blurry(image_path):
                move_to_rejected(image_path, class_name, "blurry")
                rejected_counts[class_name]["blurry"] += 1
                grand_totals["blurry"] += 1
                continue  # Image moved, go to next file

            # If we reach here, the image passed ALL checks. It stays put.

    # ------------------------------------------------------------------------
    # 6e. Calculate final counts (images that passed cleaning)
    # ------------------------------------------------------------------------

    print("\n" + "=" * 70)
    print("CLEANING COMPLETE - SUMMARY REPORT")
    print("=" * 70)

    # Calculate total rejected across all classes
    total_rejected = sum(grand_totals.values())
    total_scanned = sum(total_counts.values())
    total_kept = total_scanned - total_rejected

    print(f"\nOverall Statistics:")
    print(f"  - Total images scanned:     {total_scanned}")
    print(f"  - Total images kept:        {total_kept}")
    print(f"  - Total images rejected:    {total_rejected}")
    print(f"  - Rejection rate:            {total_rejected/total_scanned*100:.2f}%")

    print(f"\nRejection Breakdown:")
    print(f"  - Corrupt:   {grand_totals['corrupt']} images")
    print(f"  - Too small: {grand_totals['too_small']} images")
    print(f"  - Too blurry:{grand_totals['blurry']} images")

    # ------------------------------------------------------------------------
    # 6f. Print per-class summary table
    # ------------------------------------------------------------------------

    print("\n" + "-" * 70)
    print(f"{'Class Name':<35} {'Scanned':>8} {'Kept':>8} {'Rejected':>8} {'Corrupt':>8} {'Small':>8} {'Blurry':>8}")
    print("-" * 70)

    for class_name in class_folders:
        scanned = total_counts[class_name]
        rejected = sum(rejected_counts[class_name].values())
        kept = scanned - rejected
        corrupt = rejected_counts[class_name]["corrupt"]
        small = rejected_counts[class_name]["too_small"]
        blurry = rejected_counts[class_name]["blurry"]

        print(f"{class_name:<35} {scanned:>8} {kept:>8} {rejected:>8} {corrupt:>8} {small:>8} {blurry:>8}")

    print("-" * 70)
    print(f"{'TOTAL':<35} {total_scanned:>8} {total_kept:>8} {total_rejected:>8} {grand_totals['corrupt']:>8} {grand_totals['too_small']:>8} {grand_totals['blurry']:>8}")
    print("=" * 70)

    print("\nCleaning complete!")
    print(f"   Bad images moved to: {REJECTED_DIR}")
    print("   Good images remain in: data/processed/")
    print("\nNext step: Run check_balance.py to see image counts per class.")


# ============================================================================
# STEP 7: RUN THE SCRIPT
# ============================================================================

# This is a Python convention: only run main() if this file is executed directly.
# If someone imports this file as a module, main() won't run automatically.
# __name__ is "__main__" when you run: python clean_data.py
# __name__ is "clean_data" when you do: import clean_data
if __name__ == "__main__":
    main()
