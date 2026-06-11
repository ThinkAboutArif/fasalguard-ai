# FasalGuard AI — Complete Project PRD
**Project:** AI-Powered Crop Disease & Pest Detection  
**Version:** 3.0 — Classification + Grad-CAM  
**GitHub:** https://github.com/ThinkAboutArif/fasalguard-ai.git  
**Student:** CECOS University, Peshawar — Fourth Semester  
**Deadline:** Monday  
**Last Updated:** See PROGRESS_LOG.md

---

## AI ASSISTANT RULES (Read Before Every Session)

You are a patient, expert software engineering mentor guiding a first-time machine learning student. Follow these rules without exception:

### Core Rules
1. **Zero experience assumed.** Explain every term, every command, every concept as if the student has never seen it before.
2. **One step at a time.** Never give Step 2 until Step 1 is fully confirmed working with zero errors.
3. **Verify before moving.** After every step, ask the student to confirm output or paste error messages before proceeding.
4. **Click-by-click instructions.** Never say "install X." Say exactly which website, which button, which option to choose.
5. **Error-first mindset.** If the student reports an error, stop everything and fix it before any new steps.
6. **Explain why.** Before any major step, explain in one sentence WHY we are doing it.
7. **Check the progress log.** At the start of every session, read PROGRESS_LOG.md to know exactly what is done and what is next.
8. **Update the progress log.** After every completed step, tell the student exactly what to write in PROGRESS_LOG.md before moving on.
9. **GitHub commits.** After completing each full phase, tell the student to commit to GitHub. Give the exact commit message to use.
10. **Never assume tools are installed.** Always verify with a check command first.
11. **Laptop vs GPU system split.** Steps marked [LAPTOP] are done on the student's personal laptop (CPU only, Windows). Steps marked [GPU SYSTEM] are done at school on the GPU machine.

### Communication Rules
- Simple English only. No jargon without explanation.
- Put every terminal command in a code block and explain every part of it.
- Warn the student before anything that could go wrong.
- After each phase, remind the student to commit to GitHub with the exact command and message.

---

## Project Summary

FasalGuard AI is a web application where a user uploads a photo of a crop leaf and receives:
- Whether the crop is **healthy or infected**
- If infected: the **exact disease/pest name**
- A **confidence percentage** (how sure the model is)
- A **Grad-CAM heatmap** overlay showing which part of the leaf the model focused on
- A **severity estimate** (Low / Medium / High) based on confidence score
- A **treatment recommendation** (what to do, what chemical to use, how to prevent)

### Architecture Change from v2.0
**Removed:** YOLOv8 object detection (required bounding box labels — PlantVillage has none)  
**Replaced with:** EfficientNet-B0 image classification + Grad-CAM visualisation  
**Reason:** PlantVillage is a classification dataset. Classification models hit 93–97% accuracy on it. Detection models would fail without labels.

---

## System Architecture

```
User uploads crop leaf photo (browser)
              │
              ▼
       Flask Web Server
              │
              ▼
   EfficientNet-B0 Classifier
   (pretrained on ImageNet,
    fine-tuned on PlantVillage)
              │
         Predicts class
              │
      ┌───────┴────────┐
      ▼                ▼
 Grad-CAM           Severity
 Heatmap            Calculator
 Generator          (based on
 (shows where       confidence %)
 model looked)
      │                │
      └───────┬────────┘
              ▼
      Treatment Lookup
      (Python dictionary)
              │
              ▼
    Result page shown to user
```

---

## Tech Stack

| Component | Technology | Why |
|---|---|---|
| AI Model | EfficientNet-B0 (PyTorch) | 93-97% accuracy on PlantVillage, fast, small |
| Heatmap | Grad-CAM (pytorch-grad-cam library) | Shows which area model focused on, no labels needed |
| Training | PyTorch + torchvision | Industry standard |
| Web Backend | Flask (Python) | Simple, beginner-friendly |
| Web Frontend | HTML + CSS + JavaScript | No framework, works offline |
| Model Export | TorchScript (.pt) or ONNX | Runs on CPU laptop |

---

## Hardware Split

### [LAPTOP] — Windows, CPU only
- Virtual environment: `fasalguard_env` (already created, already activated)
- Project folder: `C:\Users\dhhdb\Desktop\fasalguard\`
- GitHub repo: https://github.com/ThinkAboutArif/fasalguard-ai.git (already set up, 2 commits made)
- Do here: data prep, cleaning, web app, testing

### [GPU SYSTEM] — School computer, NVIDIA GPU
- Do only here: model training
- Transfer method: USB drive or Google Drive

---

## Current Dataset Status

**Location:** `C:\Users\dhhdb\Desktop\fasalguard\data\raw\plantvillage\`  
**Status:** Downloaded and extracted. All 38 folders present.  
**Source:** PlantVillage dataset from Kaggle

### All 38 Classes (Full Dataset — Use All of Them)

| # | Original Folder Name | Our Class Name |
|---|---|---|
| 0 | Apple___Apple_scab | apple_scab |
| 1 | Apple___Black_rot | apple_black_rot |
| 2 | Apple___Cedar_apple_rust | apple_cedar_rust |
| 3 | Apple___healthy | apple_healthy |
| 4 | Blueberry___healthy | blueberry_healthy |
| 5 | Cherry_(including_sour)___healthy | cherry_healthy |
| 6 | Cherry_(including_sour)___Powdery_mildew | cherry_powdery_mildew |
| 7 | Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot | maize_cercospora |
| 8 | Corn_(maize)___Common_rust_ | maize_common_rust |
| 9 | Corn_(maize)___healthy | maize_healthy |
| 10 | Corn_(maize)___Northern_Leaf_Blight | maize_northern_blight |
| 11 | Grape___Black_rot | grape_black_rot |
| 12 | Grape___Esca_(Black_Measles) | grape_esca |
| 13 | Grape___healthy | grape_healthy |
| 14 | Grape___Leaf_blight_(Isariopsis_Leaf_Spot) | grape_leaf_blight |
| 15 | Orange___Haunglongbing_(Citrus_greening) | orange_citrus_greening |
| 16 | Peach___Bacterial_spot | peach_bacterial_spot |
| 17 | Peach___healthy | peach_healthy |
| 18 | Pepper,_bell___Bacterial_spot | pepper_bacterial_spot |
| 19 | Pepper,_bell___healthy | pepper_healthy |
| 20 | Potato___Early_blight | potato_early_blight |
| 21 | Potato___healthy | potato_healthy |
| 22 | Potato___Late_blight | potato_late_blight |
| 23 | Raspberry___healthy | raspberry_healthy |
| 24 | Soybean___healthy | soybean_healthy |
| 25 | Squash___Powdery_mildew | squash_powdery_mildew |
| 26 | Strawberry___healthy | strawberry_healthy |
| 27 | Strawberry___Leaf_scorch | strawberry_leaf_scorch |
| 28 | Tomato___Bacterial_spot | tomato_bacterial_spot |
| 29 | Tomato___Early_blight | tomato_early_blight |
| 30 | Tomato___healthy | tomato_healthy |
| 31 | Tomato___Late_blight | tomato_late_blight |
| 32 | Tomato___Leaf_Mold | tomato_leaf_mold |
| 33 | Tomato___Septoria_leaf_spot | tomato_septoria |
| 34 | Tomato___Spider_mites Two-spotted_spider_mite | tomato_spider_mite |
| 35 | Tomato___Target_Spot | tomato_target_spot |
| 36 | Tomato___Tomato_mosaic_virus | tomato_mosaic_virus |
| 37 | Tomato___Tomato_Yellow_Leaf_Curl_Virus | tomato_yellow_leaf_curl |

---

## Folder Structure (Final Target)

```
C:\Users\dhhdb\Desktop\fasalguard\
├── data\
│   ├── raw\
│   │   └── plantvillage\        ← already here, 38 folders
│   └── processed\               ← scripts will create this
│       ├── train\               ← 80% of images
│       ├── val\                 ← 10% of images
│       └── test\                ← 10% of images
│           (each split has 38 subfolders, one per class)
├── scripts\
│   ├── organise_data.py         ← renames folders, creates processed/
│   ├── clean_data.py            ← removes bad images
│   ├── check_balance.py         ← shows image count per class
│   └── split_data.py            ← creates train/val/test split
├── training\                    ← copy entire project to GPU system
│   ├── train.py
│   └── class_names.json
├── app\
│   ├── app.py                   ← Flask server
│   ├── model\
│   │   └── fasalguard_model.pt  ← trained model goes here after training
│   ├── templates\
│   │   ├── index.html
│   │   └── result.html
│   └── static\
│       └── style.css
├── requirements_laptop.txt
├── requirements_gpu.txt
├── README.md
└── .gitignore
```

---

## Severity Logic

Based on model confidence score (no bounding boxes needed):

| Confidence | Severity | Display Colour |
|---|---|---|
| Below 60% | Low — Early stage, monitor closely | 🟡 Yellow |
| 60% – 85% | Medium — Action recommended soon | 🟠 Orange |
| Above 85% | High — Immediate action required | 🔴 Red |
| Any "healthy" class | None | 🟢 Green |

---

## Treatment Dictionary (All 38 Classes)

```python
TREATMENTS = {
    # ── APPLE ──────────────────────────────────────────────
    "apple_scab": {
        "common_name": "Apple Scab",
        "action": "Remove and destroy infected leaves and fruit. Do not compost them.",
        "chemical": "Apply Captan 50WP at 2g per litre of water. Spray every 10 days during wet weather.",
        "prevention": "Plant scab-resistant apple varieties. Ensure good air circulation by pruning."
    },
    "apple_black_rot": {
        "common_name": "Apple Black Rot",
        "action": "Prune out all dead or infected branches. Remove mummified fruit from tree and ground.",
        "chemical": "Apply Thiophanate-methyl at 1.5g per litre. Begin at pink bud stage, repeat every 14 days.",
        "prevention": "Remove all fallen fruit and leaves. Avoid wounding trees during pruning."
    },
    "apple_cedar_rust": {
        "common_name": "Apple Cedar Rust",
        "action": "Remove galls from nearby cedar/juniper trees in late winter before spores release.",
        "chemical": "Apply Myclobutanil 20EW at 1ml per litre at pink bud stage. Repeat every 7–10 days.",
        "prevention": "Plant rust-resistant apple varieties. Remove cedar trees near apple orchards if possible."
    },
    "apple_healthy": {
        "common_name": "Healthy Apple",
        "action": "No action needed. Crop appears healthy.",
        "chemical": "None required.",
        "prevention": "Continue regular monitoring every 7 days. Maintain good orchard hygiene."
    },
    # ── BLUEBERRY ──────────────────────────────────────────
    "blueberry_healthy": {
        "common_name": "Healthy Blueberry",
        "action": "No action needed.",
        "chemical": "None required.",
        "prevention": "Monitor regularly. Maintain soil pH between 4.5 and 5.5 for healthy blueberries."
    },
    # ── CHERRY ─────────────────────────────────────────────
    "cherry_healthy": {
        "common_name": "Healthy Cherry",
        "action": "No action needed.",
        "chemical": "None required.",
        "prevention": "Monitor weekly. Prune for air circulation."
    },
    "cherry_powdery_mildew": {
        "common_name": "Cherry Powdery Mildew",
        "action": "Remove heavily infected shoots. Do not compost infected material.",
        "chemical": "Apply Sulphur 80WP at 2g per litre or Hexaconazole 5EC at 1ml per litre. Spray every 14 days.",
        "prevention": "Avoid overhead irrigation. Prune to improve air circulation. Avoid excessive nitrogen."
    },
    # ── MAIZE / CORN ───────────────────────────────────────
    "maize_cercospora": {
        "common_name": "Maize Gray Leaf Spot (Cercospora)",
        "action": "Apply fungicide at first sign of rectangular grey-tan lesions on lower leaves.",
        "chemical": "Apply Azoxystrobin 250SC at 1ml per litre. Spray at tasselling stage, repeat after 14 days.",
        "prevention": "Crop rotation. Plant resistant hybrids. Avoid excessive plant density."
    },
    "maize_common_rust": {
        "common_name": "Maize Common Rust",
        "action": "Apply fungicide when orange-brown pustules appear on both leaf surfaces.",
        "chemical": "Apply Propiconazole 25EC at 1ml per litre. Spray at 14-day intervals.",
        "prevention": "Plant rust-resistant maize varieties. Avoid late planting."
    },
    "maize_healthy": {
        "common_name": "Healthy Maize",
        "action": "No action needed.",
        "chemical": "None required.",
        "prevention": "Monitor weekly from emergence to silking stage."
    },
    "maize_northern_blight": {
        "common_name": "Maize Northern Leaf Blight",
        "action": "Apply fungicide when long cigar-shaped lesions appear on leaves.",
        "chemical": "Apply Mancozeb 75WP at 2.5g per litre. Spray every 14 days.",
        "prevention": "Crop rotation with non-host crops. Remove crop debris after harvest."
    },
    # ── GRAPE ──────────────────────────────────────────────
    "grape_black_rot": {
        "common_name": "Grape Black Rot",
        "action": "Remove all mummified berries and infected leaves immediately.",
        "chemical": "Apply Mancozeb 75WP at 2g per litre. Begin before bloom, spray every 10 days.",
        "prevention": "Prune for good air circulation. Remove all debris from previous season."
    },
    "grape_esca": {
        "common_name": "Grape Esca (Black Measles)",
        "action": "No chemical cure. Remove and destroy severely infected vines.",
        "chemical": "Protect pruning wounds with wound sealant paste immediately after cutting.",
        "prevention": "Prune during dry weather. Disinfect pruning tools between vines with 70% alcohol."
    },
    "grape_healthy": {
        "common_name": "Healthy Grape",
        "action": "No action needed.",
        "chemical": "None required.",
        "prevention": "Monitor weekly. Maintain training system for good air circulation."
    },
    "grape_leaf_blight": {
        "common_name": "Grape Leaf Blight",
        "action": "Remove infected leaves. Improve air circulation by canopy management.",
        "chemical": "Apply Copper oxychloride 50WP at 3g per litre. Spray every 14 days.",
        "prevention": "Avoid overhead irrigation. Ensure vineyard has good drainage."
    },
    # ── ORANGE ─────────────────────────────────────────────
    "orange_citrus_greening": {
        "common_name": "Citrus Greening (Huanglongbing)",
        "action": "No cure exists. Remove and destroy infected trees immediately to prevent spread.",
        "chemical": "Control Asian citrus psyllid vector with Imidacloprid 200SL at 0.5ml per litre.",
        "prevention": "Use certified disease-free planting material only. Install psyllid monitoring traps."
    },
    # ── PEACH ──────────────────────────────────────────────
    "peach_bacterial_spot": {
        "common_name": "Peach Bacterial Spot",
        "action": "Remove heavily spotted leaves and fruit. Avoid working in orchard when wet.",
        "chemical": "Apply copper-based bactericide (Copper hydroxide 77WP at 3g per litre). Spray every 7–10 days.",
        "prevention": "Plant resistant varieties. Avoid overhead irrigation. Prune for air circulation."
    },
    "peach_healthy": {
        "common_name": "Healthy Peach",
        "action": "No action needed.",
        "chemical": "None required.",
        "prevention": "Monitor weekly. Thin fruit early for better air circulation."
    },
    # ── PEPPER ─────────────────────────────────────────────
    "pepper_bacterial_spot": {
        "common_name": "Pepper Bacterial Spot",
        "action": "Remove infected plants if severe. Avoid handling plants when wet.",
        "chemical": "Apply Copper oxychloride 50WP at 2.5g per litre. Spray every 7 days.",
        "prevention": "Use certified disease-free seeds. Avoid overhead irrigation. Rotate crops."
    },
    "pepper_healthy": {
        "common_name": "Healthy Bell Pepper",
        "action": "No action needed.",
        "chemical": "None required.",
        "prevention": "Monitor weekly. Water at base of plant, not overhead."
    },
    # ── POTATO ─────────────────────────────────────────────
    "potato_early_blight": {
        "common_name": "Potato Early Blight",
        "action": "Remove infected lower leaves. Apply fungicide at first sign of dark concentric-ring spots.",
        "chemical": "Apply Mancozeb 75WP at 2.5g per litre. Spray every 7 days in humid conditions.",
        "prevention": "Crop rotation. Avoid excessive nitrogen. Plant certified seed potatoes."
    },
    "potato_healthy": {
        "common_name": "Healthy Potato",
        "action": "No action needed.",
        "chemical": "None required.",
        "prevention": "Monitor weekly. Hill up soil around stems to prevent greening."
    },
    "potato_late_blight": {
        "common_name": "Potato Late Blight",
        "action": "Urgent: Destroy infected plants immediately. This disease spreads extremely fast.",
        "chemical": "Apply Metalaxyl + Mancozeb (Ridomil Gold) at 2g per litre. Spray every 5–7 days.",
        "prevention": "Use certified blight-free seed. Avoid overhead irrigation. Destroy volunteer plants."
    },
    # ── RASPBERRY ──────────────────────────────────────────
    "raspberry_healthy": {
        "common_name": "Healthy Raspberry",
        "action": "No action needed.",
        "chemical": "None required.",
        "prevention": "Monitor weekly. Remove old canes after fruiting."
    },
    # ── SOYBEAN ────────────────────────────────────────────
    "soybean_healthy": {
        "common_name": "Healthy Soybean",
        "action": "No action needed.",
        "chemical": "None required.",
        "prevention": "Monitor weekly. Scout for pests from V3 growth stage onwards."
    },
    # ── SQUASH ─────────────────────────────────────────────
    "squash_powdery_mildew": {
        "common_name": "Squash Powdery Mildew",
        "action": "Remove heavily infected leaves. Increase air circulation around plants.",
        "chemical": "Apply Sulphur 80WP at 2g per litre or Potassium bicarbonate at 5g per litre.",
        "prevention": "Avoid overhead watering. Space plants widely. Choose resistant varieties."
    },
    # ── STRAWBERRY ─────────────────────────────────────────
    "strawberry_healthy": {
        "common_name": "Healthy Strawberry",
        "action": "No action needed.",
        "chemical": "None required.",
        "prevention": "Monitor weekly. Replace beds every 3 years to prevent disease buildup."
    },
    "strawberry_leaf_scorch": {
        "common_name": "Strawberry Leaf Scorch",
        "action": "Remove and destroy infected leaves. Do not overhead irrigate.",
        "chemical": "Apply Myclobutanil 20EW at 1ml per litre. Spray every 14 days.",
        "prevention": "Ensure good drainage. Avoid planting in same location as previous strawberry crop."
    },
    # ── TOMATO ─────────────────────────────────────────────
    "tomato_bacterial_spot": {
        "common_name": "Tomato Bacterial Spot",
        "action": "Remove infected leaves and fruit. Avoid working with plants when wet.",
        "chemical": "Apply Copper hydroxide 77WP at 3g per litre. Spray every 7 days.",
        "prevention": "Use certified disease-free seed. Avoid overhead irrigation. Rotate crops annually."
    },
    "tomato_early_blight": {
        "common_name": "Tomato Early Blight",
        "action": "Remove infected lower leaves immediately. Apply fungicide at first sign of dark bull's-eye spots.",
        "chemical": "Apply Mancozeb 75WP at 2.5g per litre of water. Spray every 7 days.",
        "prevention": "Avoid overhead watering. Ensure good air circulation between plants. Mulch soil."
    },
    "tomato_healthy": {
        "common_name": "Healthy Tomato",
        "action": "No action needed. Crop appears healthy.",
        "chemical": "None required.",
        "prevention": "Continue regular monitoring every 7 days. Water at base of plant."
    },
    "tomato_late_blight": {
        "common_name": "Tomato Late Blight",
        "action": "Urgent: Remove all infected plants immediately. This spreads to entire field within days.",
        "chemical": "Apply Metalaxyl + Mancozeb (Ridomil Gold) at 2g per litre. Spray every 5 days.",
        "prevention": "Use certified disease-free seeds. Avoid planting in wet or poorly drained areas."
    },
    "tomato_leaf_mold": {
        "common_name": "Tomato Leaf Mold",
        "action": "Increase ventilation. Remove infected leaves. Reduce humidity in greenhouse.",
        "chemical": "Apply Chlorothalonil 75WP at 2g per litre. Spray every 14 days.",
        "prevention": "Ensure good air circulation. Keep humidity below 85%. Use resistant varieties."
    },
    "tomato_septoria": {
        "common_name": "Tomato Septoria Leaf Spot",
        "action": "Remove infected lower leaves immediately when small spots with dark borders appear.",
        "chemical": "Apply Mancozeb 75WP at 2g per litre. Spray every 7–10 days.",
        "prevention": "Rotate crops. Avoid overhead irrigation. Remove plant debris at end of season."
    },
    "tomato_spider_mite": {
        "common_name": "Tomato Spider Mite (Two-Spotted)",
        "action": "Spray leaf undersides where mites cluster. Remove heavily infested leaves.",
        "chemical": "Apply Abamectin 1.8EC at 1ml per litre. Spray in evening, not in midday heat.",
        "prevention": "Maintain adequate soil moisture. Remove weeds around crop. Avoid dusty conditions."
    },
    "tomato_target_spot": {
        "common_name": "Tomato Target Spot",
        "action": "Remove infected leaves. Apply fungicide when concentric-ring spots first appear.",
        "chemical": "Apply Azoxystrobin 250SC at 1ml per litre. Spray every 14 days.",
        "prevention": "Crop rotation. Avoid overhead irrigation. Destroy crop debris after harvest."
    },
    "tomato_mosaic_virus": {
        "common_name": "Tomato Mosaic Virus",
        "action": "No chemical cure. Remove and destroy infected plants immediately.",
        "chemical": "No effective chemical treatment. Focus on prevention and vector control.",
        "prevention": "Wash hands before handling plants. Disinfect tools. Control aphid vectors with Dimethoate."
    },
    "tomato_yellow_leaf_curl": {
        "common_name": "Tomato Yellow Leaf Curl Virus",
        "action": "No chemical cure. Remove infected plants immediately to prevent spread via whitefly.",
        "chemical": "Control whitefly vectors with Imidacloprid 200SL at 0.5ml per litre.",
        "prevention": "Use virus-resistant tomato varieties. Install yellow sticky traps to catch whiteflies."
    },
}
```

---

## Training Configuration

### Model: EfficientNet-B0

```python
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from torch import nn

# Load pretrained EfficientNet-B0
model = models.efficientnet_b0(pretrained=True)

# Replace final layer for our 38 classes
num_classes = 38
model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)

# Training settings
EPOCHS = 20
BATCH_SIZE = 32        # reduce to 16 if GPU runs out of memory
LEARNING_RATE = 0.001
IMAGE_SIZE = 224       # EfficientNet standard input size
```

### Data Transforms

```python
train_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

val_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
```

### Expected Training Results
| Metric | Minimum | Good | Excellent |
|---|---|---|---|
| Validation Accuracy | 85% | 92% | 96%+ |
| Training Time (GPU) | ~20 min | — | — |
| Inference on CPU | < 3 seconds | — | — |

---

## Grad-CAM Implementation

Grad-CAM generates a heatmap showing which pixels in the image most influenced the model's decision. It requires no extra training — it's applied to the already-trained model at inference time.

```python
# Library: pip install grad-cam
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image

# Target layer for EfficientNet-B0
target_layers = [model.features[-1]]

cam = GradCAM(model=model, target_layers=target_layers)
grayscale_cam = cam(input_tensor=input_tensor)

# Overlay heatmap on original image
visualization = show_cam_on_image(rgb_img, grayscale_cam[0], use_rgb=True)
```

The heatmap uses a red-blue colour scale. Red areas = what the model focused on most.

---

## Web App Pages

### Page 1: Upload Page (index.html)
- Logo + title: "FasalGuard AI"
- Subtitle: "Upload a crop leaf image to detect diseases instantly"
- Large upload box (click to browse or drag and drop)
- Supported formats note: JPG, PNG, JPEG
- Analyse button
- Colour theme: dark green (#1a5c2e) + white + light green accents

### Page 2: Results Page (result.html)
Layout (two columns on desktop, stacked on mobile):

**Left column:**
- Uploaded original image
- Grad-CAM heatmap image below it with label "What the AI focused on"

**Right column:**
- Detected class name (large, bold)
- Confidence percentage with progress bar
- Severity badge (colour-coded: green/yellow/orange/red)
- "What to do" section
- "Chemical treatment" section
- "Prevention" section
- "Analyse Another Image" button

---

## Presentation & Live Demo Plan

### Before the Presentation (Prepare These)
Download and save these 10 test images to a USB or desktop folder named `demo_images/`:

| # | What to Search on Google Images | Expected Result |
|---|---|---|
| 1 | "tomato late blight leaf close up" | tomato_late_blight |
| 2 | "tomato healthy green leaf" | tomato_healthy |
| 3 | "maize common rust orange pustules" | maize_common_rust |
| 4 | "potato late blight dark spots" | potato_late_blight |
| 5 | "apple scab lesions leaf" | apple_scab |
| 6 | "tomato yellow leaf curl virus" | tomato_yellow_leaf_curl |
| 7 | "pepper bacterial spot leaf" | pepper_bacterial_spot |
| 8 | "grape black rot leaf" | grape_black_rot |
| 9 | "tomato spider mite damage" | tomato_spider_mite |
| 10 | "corn northern leaf blight" | maize_northern_blight |

**Important:** Use images from PlantVillage-style close-up shots (single leaf, white or plain background). The model was trained on these so it performs best on similar images.

### During the Presentation
**Step 1:** Open browser, go to http://localhost:5000  
**Step 2:** Start with image #2 (healthy tomato) — show the system correctly says "Healthy"  
**Step 3:** Upload image #1 (tomato late blight) — show detection, heatmap, severity, treatment  
**Step 4:** Upload image #3 (maize rust) — show it works across different crops  
**Step 5:** If time allows, take a photo of any plant leaf in the room with phone — upload it for a live test

### What to Say for Each Result
- Point to the heatmap: *"The red area shows exactly where the AI detected the infection"*
- Point to severity: *"Based on confidence level, it rates this as High severity"*
- Point to treatment: *"It gives the farmer specific chemical names and dosage — no agricultural knowledge needed"*

### Backup Plan if Something Breaks
- Have 3 screenshots of successful predictions saved as images
- If Flask crashes: `Ctrl+C` then `python app.py` again
- If model gives wrong answer: say *"This image style differs from training data — real-world robustness is a future improvement"*

---

## GitHub Commit Schedule

| After Completing | Commit Message |
|---|---|
| Phase 0 | `setup: project structure and virtual environment` |
| Phase 1 | `data: plantvillage dataset organised into processed folder` |
| Phase 2 | `data: cleaning scripts and verified class balance` |
| Phase 3 | `data: train/val/test split complete, class_names.json added` |
| Phase 6 | `app: flask web app pages and styling complete` |
| Phase 7 | `app: model integrated, grad-cam working, end-to-end tested` |
| Phase 8 | `final: readme updated, project complete` |

---

## requirements_laptop.txt

```
flask==3.0.0
torch                  # CPU version — installed separately, see Phase 0
torchvision            # CPU version — installed separately, see Phase 0
grad-cam==1.4.8
opencv-python==4.9.0.80
Pillow==10.2.0
numpy==1.26.4
```

## requirements_gpu.txt

```
torch                  # GPU version with CUDA — installed separately
torchvision            # GPU version with CUDA — installed separately
grad-cam==1.4.8
opencv-python==4.9.0.80
Pillow==10.2.0
numpy==1.26.4
tqdm==4.66.2
matplotlib==3.8.3
```

---

## Definition of Done

- [ ] Model trained with validation accuracy ≥ 85%
- [ ] Web app runs with `python app.py` on laptop
- [ ] Upload any PlantVillage-style leaf image → correct class predicted
- [ ] Grad-CAM heatmap displays on result page
- [ ] Severity and treatment show correctly for all 38 classes
- [ ] 10 demo images tested and passing
- [ ] All code committed to GitHub
- [ ] App can run fully offline during presentation
