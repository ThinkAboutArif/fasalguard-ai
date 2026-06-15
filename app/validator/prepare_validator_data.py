"""
prepare_validator_data.py
Run this on LAPTOP.
Creates data/validator/ folder with leaf vs not_leaf images for training.
"""

import os
import random
import shutil
from pathlib import Path

# ── CONFIG ────────────────────────────────────────────────────────────────────
LEAF_SOURCE      = r"C:\Users\dhhdb\Desktop\fasalguard\data\processed"
NOT_LEAF_SOURCE  = r"C:\Users\dhhdb\Desktop\fasalguard\data\imagenette2-160\imagenette2-160"
OUTPUT_DIR       = r"C:\Users\dhhdb\Desktop\fasalguard\data\validator"

TOTAL_LEAF     = 4000   # total leaf images (split 80/20)
TOTAL_NOT_LEAF = 4000   # total not-leaf images (split 80/20)
TRAIN_SPLIT    = 0.80
SEED           = 42
# ──────────────────────────────────────────────────────────────────────────────

random.seed(SEED)

SPLITS = {
    "train": {"leaf": int(TOTAL_LEAF * TRAIN_SPLIT),
              "not_leaf": int(TOTAL_NOT_LEAF * TRAIN_SPLIT)},
    "val":   {"leaf": TOTAL_LEAF - int(TOTAL_LEAF * TRAIN_SPLIT),
              "not_leaf": TOTAL_NOT_LEAF - int(TOTAL_NOT_LEAF * TRAIN_SPLIT)},
}

def collect_images(folder, extensions=(".jpg", ".jpeg", ".png")):
    """Walk a folder and return all image paths."""
    paths = []
    for root, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith(extensions):
                paths.append(os.path.join(root, f))
    return paths

def copy_sample(sources, dest_folder, count, label):
    """Randomly sample `count` images from sources and copy to dest_folder."""
    os.makedirs(dest_folder, exist_ok=True)
    sample = random.sample(sources, min(count, len(sources)))
    for i, src in enumerate(sample):
        ext = Path(src).suffix
        dst = os.path.join(dest_folder, f"{label}_{i:05d}{ext}")
        shutil.copy2(src, dst)
    print(f"  Copied {len(sample)} images to {dest_folder}")
    return len(sample)

print("Collecting leaf images from PlantVillage...")
all_leaf = collect_images(LEAF_SOURCE)
print(f"  Found {len(all_leaf)} leaf images")

print("Collecting not-leaf images from imagenette2-160...")
all_not_leaf = collect_images(NOT_LEAF_SOURCE)
print(f"  Found {len(all_not_leaf)} not-leaf images")

random.shuffle(all_leaf)
random.shuffle(all_not_leaf)

leaf_train     = all_leaf[:SPLITS["train"]["leaf"]]
leaf_val       = all_leaf[SPLITS["train"]["leaf"]:SPLITS["train"]["leaf"] + SPLITS["val"]["leaf"]]
not_leaf_train = all_not_leaf[:SPLITS["train"]["not_leaf"]]
not_leaf_val   = all_not_leaf[SPLITS["train"]["not_leaf"]:SPLITS["train"]["not_leaf"] + SPLITS["val"]["not_leaf"]]

print("\nCopying files...")
copy_sample(leaf_train,     os.path.join(OUTPUT_DIR, "train", "leaf"),     len(leaf_train),     "leaf")
copy_sample(leaf_val,       os.path.join(OUTPUT_DIR, "val",   "leaf"),     len(leaf_val),       "leaf")
copy_sample(not_leaf_train, os.path.join(OUTPUT_DIR, "train", "not_leaf"), len(not_leaf_train), "not_leaf")
copy_sample(not_leaf_val,   os.path.join(OUTPUT_DIR, "val",   "not_leaf"), len(not_leaf_val),   "not_leaf")

print("\nDone! Validator dataset ready.")
print(f"  Train: {len(leaf_train)} leaf + {len(not_leaf_train)} not_leaf")
print(f"  Val:   {len(leaf_val)} leaf + {len(not_leaf_val)} not_leaf")