import os
import shutil
import random

# ── CONFIGURATION ─────────────────────────────────────────
# Path to your cleaned data folder (38 class folders inside)
BASE_DIR = r"C:\Users\dhhdb\Desktop\fasalguard\data\processed"

# Split ratios — these must add up to 1.0
TRAIN_RATIO = 0.8   # 80% for training
VAL_RATIO   = 0.1   # 10% for validation
TEST_RATIO  = 0.1   # 10% for testing

# Random seed — makes the shuffle IDENTICAL every time you run it
RANDOM_SEED = 42

# Image file extensions to look for
IMAGE_EXTS = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tif', '.tiff')

# ── SAFETY CHECK ──────────────────────────────────────────
# Stop if train/val/test folders already exist (script can only run once)
for split in ['train', 'val', 'test']:
    split_path = os.path.join(BASE_DIR, split)
    if os.path.exists(split_path):
        print(f"ERROR: {split_path} already exists.")
        print("This script can only be run once. Restore processed/ from backup if you need to re-run.")
        exit(1)

# ── STEP 1: FIND ALL CLASS FOLDERS ────────────────────────
all_items = os.listdir(BASE_DIR)
class_folders = []
for item in all_items:
    item_path = os.path.join(BASE_DIR, item)
    if os.path.isdir(item_path):
        class_folders.append(item)

class_folders.sort()  # alphabetical order
print(f"Found {len(class_folders)} class folders.")
print("-" * 60)

# ── STEP 2: CREATE TRAIN / VAL / TEST FOLDERS ─────────────
for split in ['train', 'val', 'test']:
    os.makedirs(os.path.join(BASE_DIR, split), exist_ok=True)

# ── STEP 3: SPLIT EACH CLASS ──────────────────────────────
random.seed(RANDOM_SEED)

total_train = 0
total_val   = 0
total_test  = 0

for class_name in class_folders:
    class_path = os.path.join(BASE_DIR, class_name)
    
    # Collect all image files in this class folder
    images = []
    for filename in os.listdir(class_path):
        if filename.lower().endswith(IMAGE_EXTS):
            images.append(filename)
    
    images.sort()
    n = len(images)
    
    if n == 0:
        print(f"WARNING: {class_name} has 0 images. Skipping.")
        continue
    
    # Shuffle with fixed seed — same result every time
    random.shuffle(images)
    
    # Calculate how many images go to each split
    n_train = int(n * TRAIN_RATIO)
    n_val   = int(n * VAL_RATIO)
    n_test  = n - n_train - n_val  # remainder goes to test (handles rounding)
    
    train_imgs = images[:n_train]
    val_imgs   = images[n_train : n_train + n_val]
    test_imgs  = images[n_train + n_val :]
    
    # Move images into their new split folders
    for split_name, split_imgs in [('train', train_imgs), ('val', val_imgs), ('test', test_imgs)]:
        split_class_path = os.path.join(BASE_DIR, split_name, class_name)
        os.makedirs(split_class_path, exist_ok=True)
        
        for img in split_imgs:
            src = os.path.join(class_path, img)
            dst = os.path.join(split_class_path, img)
            shutil.move(src, dst)  # move = instant rename on same drive, no extra space
    
    # Remove the now-empty original class folder
    remaining = os.listdir(class_path)
    if len(remaining) == 0:
        os.rmdir(class_path)
    else:
        print(f"WARNING: {class_name} still has {len(remaining)} non-image files. Folder not removed.")
    
    total_train += n_train
    total_val   += n_val
    total_test  += n_test
    
    print(f"{class_name:30s} | total: {n:4d} | train: {n_train:4d} | val: {n_val:4d} | test: {n_test:4d}")

# ── STEP 4: PRINT FINAL SUMMARY ───────────────────────────
print("=" * 60)
print(f"{'SPLIT':10s} | {'TOTAL IMAGES':15s}")
print("-" * 60)
print(f"{'train':10s} | {total_train:15d}")
print(f"{'val':10s} | {total_val:15d}")
print(f"{'test':10s} | {total_test:15d}")
print("=" * 60)
print(f"GRAND TOTAL: {total_train + total_val + total_test}")