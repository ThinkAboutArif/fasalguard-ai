# check_balance.py
# Creates a bar chart showing image count per class
# Helps us see if any classes need more data

import os
from pathlib import Path
import matplotlib.pyplot as plt

# ============================================================
# STEP 1: Define path to processed data
# ============================================================

PROCESSED_DIR = Path(r"C:\Users\dhhdb\Desktop\fasalguard\data\processed")

# ============================================================
# STEP 2: Count images in each class folder
# ============================================================

print("=" * 60)
print("FasalGuard AI — Check Class Balance")
print("=" * 60)

class_counts = {}
image_extensions = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')

# Go through each folder in processed/
for class_folder in sorted(PROCESSED_DIR.iterdir()):
    if class_folder.is_dir():
        # Count image files in this folder
        image_files = [f for f in class_folder.iterdir() if f.suffix in image_extensions]
        class_counts[class_folder.name] = len(image_files)

# ============================================================
# STEP 3: Print counts in a table
# ============================================================

print(f"\nTotal classes: {len(class_counts)}")
print(f"Total images: {sum(class_counts.values()):,}\n")
print("-" * 50)
print(f"{'Class Name':<35} {'Count':>8}")
print("-" * 50)

for name, count in sorted(class_counts.items()):
    status = "✓" if count >= 200 else "⚠️"
    print(f"{name:<35} {count:>8} {status}")

print("-" * 50)

# ============================================================
# STEP 4: Create a bar chart and save it
# ============================================================

# Sort by count (highest first) for better visualization
sorted_counts = dict(sorted(class_counts.items(), key=lambda x: x[1], reverse=True))

# Create the figure
plt.figure(figsize=(16, 10))
bars = plt.bar(range(len(sorted_counts)), list(sorted_counts.values()), color='green')

# Color bars: green for OK, orange for low
for i, (name, count) in enumerate(sorted_counts.items()):
    if count < 200:
        bars[i].set_color('orange')

# Add labels
plt.xticks(range(len(sorted_counts)), list(sorted_counts.keys()), rotation=90, ha='right')
plt.xlabel('Class Name', fontsize=12)
plt.ylabel('Number of Images', fontsize=12)
plt.title('FasalGuard AI — Image Count Per Class', fontsize=14, fontweight='bold')

# Add a horizontal line at 200 images
plt.axhline(y=200, color='red', linestyle='--', linewidth=1, label='Minimum threshold (200)')

plt.legend()
plt.tight_layout()

# Save the chart
chart_path = Path(r"C:\Users\dhhdb\Desktop\fasalguard\scripts\class_balance_chart.png")
plt.savefig(chart_path, dpi=150)
print(f"\n✓ Bar chart saved to: {chart_path}")

# Also show it (if you have a GUI)
plt.show()

print("\n" + "=" * 60)
print("Analysis complete!")
print("=" * 60)