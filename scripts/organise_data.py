# organise_data.py
# Copies images from raw PlantVillage folders into processed/
# with clean class names. Keeps raw data untouched.

import os
import shutil
from pathlib import Path

# ============================================================
# STEP 1: Define paths
# ============================================================

RAW_DIR = Path(r"C:\Users\dhhdb\Desktop\fasalguard\data\raw\plantvillage")
PROCESSED_DIR = Path(r"C:\Users\dhhdb\Desktop\fasalguard\data\processed")

# ============================================================
# STEP 2: Mapping of ugly folder names → clean class names
# ============================================================

CLASS_MAP = {
    "Apple___Apple_scab": "apple_scab",
    "Apple___Black_rot": "apple_black_rot",
    "Apple___Cedar_apple_rust": "apple_cedar_rust",
    "Apple___healthy": "apple_healthy",
    "Blueberry___healthy": "blueberry_healthy",
    "Cherry_(including_sour)___healthy": "cherry_healthy",
    "Cherry_(including_sour)___Powdery_mildew": "cherry_powdery_mildew",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": "maize_cercospora",
    "Corn_(maize)___Common_rust_": "maize_common_rust",
    "Corn_(maize)___healthy": "maize_healthy",
    "Corn_(maize)___Northern_Leaf_Blight": "maize_northern_blight",
    "Grape___Black_rot": "grape_black_rot",
    "Grape___Esca_(Black_Measles)": "grape_esca",
    "Grape___healthy": "grape_healthy",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": "grape_leaf_blight",
    "Orange___Haunglongbing_(Citrus_greening)": "orange_citrus_greening",
    "Peach___Bacterial_spot": "peach_bacterial_spot",
    "Peach___healthy": "peach_healthy",
    "Pepper,_bell___Bacterial_spot": "pepper_bacterial_spot",
    "Pepper,_bell___healthy": "pepper_healthy",
    "Potato___Early_blight": "potato_early_blight",
    "Potato___healthy": "potato_healthy",
    "Potato___Late_blight": "potato_late_blight",
    "Raspberry___healthy": "raspberry_healthy",
    "Soybean___healthy": "soybean_healthy",
    "Squash___Powdery_mildew": "squash_powdery_mildew",
    "Strawberry___healthy": "strawberry_healthy",
    "Strawberry___Leaf_scorch": "strawberry_leaf_scorch",
    "Tomato___Bacterial_spot": "tomato_bacterial_spot",
    "Tomato___Early_blight": "tomato_early_blight",
    "Tomato___healthy": "tomato_healthy",
    "Tomato___Late_blight": "tomato_late_blight",
    "Tomato___Leaf_Mold": "tomato_leaf_mold",
    "Tomato___Septoria_leaf_spot": "tomato_septoria",
    "Tomato___Spider_mites Two-spotted_spider_mite": "tomato_spider_mite",
    "Tomato___Target_Spot": "tomato_target_spot",
    "Tomato___Tomato_mosaic_virus": "tomato_mosaic_virus",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "tomato_yellow_leaf_curl",
}

# ============================================================
# STEP 3: Create processed directory
# ============================================================

print("=" * 60)
print("FasalGuard AI — Organise Data Script")
print("=" * 60)
print(f"\nRaw data source: {RAW_DIR}")
print(f"Processed destination: {PROCESSED_DIR}\n")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
print("✓ Created processed directory\n")

# ============================================================
# STEP 4: Copy images from each raw folder to processed
# ============================================================

total_images = 0
class_counts = {}

for raw_folder_name, clean_name in CLASS_MAP.items():
    raw_folder_path = RAW_DIR / raw_folder_name
    clean_folder_path = PROCESSED_DIR / clean_name
    
    if not raw_folder_path.exists():
        print(f"⚠️  WARNING: Folder not found — {raw_folder_name}")
        continue
    
    clean_folder_path.mkdir(parents=True, exist_ok=True)
    
    # Look for image files
    image_extensions = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')
    image_files = [f for f in raw_folder_path.iterdir() if f.suffix in image_extensions]
    
    copied = 0
    for img_file in image_files:
        dest = clean_folder_path / img_file.name
        shutil.copy2(img_file, dest)
        copied += 1
    
    class_counts[clean_name] = copied
    total_images += copied
    print(f"✓ {clean_name:35s} — {copied:5d} images")

# ============================================================
# STEP 5: Print summary
# ============================================================

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Total classes processed: {len(class_counts)}")
print(f"Total images copied: {total_images:,}")
print(f"Output folder: {PROCESSED_DIR}")
print("\nImage counts per class:")
print("-" * 50)

for name in sorted(class_counts.keys()):
    count = class_counts[name]
    status = "✓ OK" if count >= 200 else "⚠️ LOW"
    print(f"  {name:35s} {count:6d} {status}")

print("=" * 60)