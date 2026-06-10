# FasalGuard AI — Complete Project PRD
**Project:** AI-Powered Pest & Disease Detection for KPK Crops, Pakistan  
**Version:** 2.0 (Clean Start)  
**Last Updated:** See PROGRESS_LOG.md  
**Student:** CECOS University, Peshawar — Fourth Semester  
**Deadline:** Monday

---

## AI ASSISTANT RULES (Read Before Every Session)

You are a patient, expert software engineering mentor guiding a first-time machine learning student through building FasalGuard AI from scratch. Follow these rules without exception:

### Core Rules
1. **Zero experience assumed.** Explain every term, every command, every concept as if the student has never seen it before.
2. **One step at a time.** Never give Step 2 until Step 1 is fully confirmed working with zero errors.
3. **Verify before moving.** After every step, ask the student to confirm the output or paste any error messages before proceeding.
4. **Click-by-click instructions.** Don't say "install Python." Say: open your browser, go to python.org, click the yellow Download button, run the installer, check the box that says Add to PATH, click Install Now.
5. **Error-first mindset.** If the student reports an error, stop everything and fix it before any new steps.
6. **Explain why.** Before any major step, explain in one sentence WHY we are doing it.
7. **Check the progress log.** At the start of every session, read PROGRESS_LOG.md to know exactly what is done and what is next.
8. **Update the progress log.** After every completed step, write the update to PROGRESS_LOG.md before moving on.
9. **Never assume tools are installed.** Always verify with a check command first.
10. **Laptop vs GPU system split.** Steps marked [LAPTOP] are done on the student's personal laptop (CPU only). Steps marked [GPU SYSTEM] are done at school on the GPU machine. Never mix them up.

### Communication Rules
- Use simple English, no jargon without explanation
- When giving terminal commands, put them in a code block and explain every part of the command
- If something can go wrong, warn the student before they run it
- Celebrate small wins — this student is learning fast under time pressure

---

## Project Summary

FasalGuard AI is a web application where a farmer uploads a photo of their crop and receives:
- The name of the pest or disease detected
- Where it is on the image (bounding box)
- How severe the infection is (Low / Medium / High)
- A treatment recommendation in English

### Crops Covered
Wheat · Maize · Cotton · Tomato

### Target Classes (10 — Focused Scope for Deadline)
| ID | Class Name | Type | Main Dataset |
|---|---|---|---|
| 0 | healthy | Healthy | PlantVillage |
| 1 | tomato_early_blight | Disease | PlantVillage |
| 2 | tomato_late_blight | Disease | PlantVillage |
| 3 | tomato_yellow_leaf_curl_virus | Disease | PlantVillage |
| 4 | maize_common_rust | Disease | PlantVillage |
| 5 | maize_northern_blight | Disease | PlantVillage |
| 6 | wheat_rust_yellow | Disease | Roboflow |
| 7 | aphid | Pest | IP102 / Roboflow |
| 8 | spider_mite | Disease | PlantVillage |
| 9 | cotton_leaf_curl_virus | Disease | Roboflow |

---

## System Architecture

```
User uploads crop photo (browser)
           │
           ▼
    Flask Web Server
           │
           ▼
    YOLOv8s Model
    (detects WHERE + WHAT)
           │
           ▼
    Severity Calculator
    (counts detections, calculates area)
           │
           ▼
    Treatment Lookup
    (Python dictionary — no database needed)
           │
           ▼
    JSON Response → Browser displays result
```

### Why Only YOLOv8 (Not Two Models)
The original plan used YOLOv8 + EfficientNet together. For this deadline we use YOLOv8 only because:
- It does detection AND classification in one model
- Simpler to train and debug
- Still achieves 85–92% accuracy on focused classes
- Half the training time

---

## Tech Stack

| Component | Technology | Why |
|---|---|---|
| AI Model | YOLOv8s (Ultralytics) | Best speed/accuracy balance, free |
| Training Framework | PyTorch + CUDA | Industry standard, GPU support |
| Web Backend | Flask (Python) | Simple, beginner-friendly |
| Web Frontend | HTML + CSS + JavaScript | No framework needed |
| Dataset Management | Roboflow (free account) | Visual interface, auto-converts labels |
| Model Export | ONNX format | Runs on CPU without GPU |

---

## Hardware Split

### [LAPTOP] — Student's Personal Laptop (CPU Only)
Do these tasks here:
- Download datasets
- Run data cleaning scripts
- Organize folder structure
- Set up GitHub repository
- Build the Flask web application
- Test the final model after training

### [GPU SYSTEM] — School Computer (NVIDIA GPU)
Do only this here:
- Install PyTorch with CUDA
- Run model training
- Export trained model weights (.pt file)
- Transfer weights back to laptop via USB or Google Drive

---

## Phase Plan

### Phase 0: Environment Setup [LAPTOP]
Set up Python, install libraries, create project folder, set up GitHub.

### Phase 1: Dataset Download & Organisation [LAPTOP]
Download all datasets, rename to standard class names, organise into correct folder structure.

### Phase 2: Data Cleaning [LAPTOP]
Run automated scripts to remove duplicates, blurry images, corrupt files, and fix class balance.

### Phase 3: Data Verification [LAPTOP]
Visually confirm the data looks correct before sending to GPU system.

### Phase 4: Model Training [GPU SYSTEM]
Transfer cleaned data to school computer, install training environment, train YOLOv8s.

### Phase 5: Model Export & Transfer [GPU SYSTEM → LAPTOP]
Export trained model to ONNX format (runs on CPU), transfer to laptop.

### Phase 6: Flask Web App [LAPTOP]
Build the upload interface and prediction display page.

### Phase 7: Integration & Testing [LAPTOP]
Connect the model to the web app, test with real images, fix errors.

### Phase 8: GitHub & Final Commit [LAPTOP]
Clean up code, write README, final commit.

---

## Dataset Details

### Dataset 1: PlantVillage (Kaggle)
- **URL:** https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
- **Size:** ~2.5 GB
- **Format:** JPG images, organised in folders by class name
- **Classes we use:** Tomato Early Blight, Tomato Late Blight, Tomato Yellow Leaf Curl Virus, Tomato Spider Mite, Maize Common Rust, Maize Northern Blight, Healthy (from multiple crops)
- **Label format:** Classification only (no bounding boxes) — we will use Roboflow to add detection labels

### Dataset 2: Roboflow Universe (Pest Detection)
- **URL:** https://universe.roboflow.com
- **Search terms to use:** "wheat rust", "aphid crop", "cotton leaf curl", "crop pest detection"
- **Format:** Already has YOLO-format bounding box labels — use directly
- **Size:** Varies per dataset, usually 500–3000 images

### Dataset 3: IP102 (GitHub)
- **URL:** https://github.com/xpwu95/IP102
- **Size:** ~75,000 images, 102 classes
- **Classes we use:** aphid only (class folder)
- **Format:** Classification only — needs labels added via Roboflow

---

## Folder Structure (What it Must Look Like Before Training)

```
fasalguard/
├── data/
│   ├── raw/                    ← downloaded datasets go here (untouched)
│   │   ├── plantvillage/
│   │   ├── roboflow_wheat/
│   │   ├── roboflow_aphid/
│   │   └── ip102/
│   └── processed/              ← cleaned, renamed, ready for training
│       ├── images/
│       │   ├── train/
│       │   ├── val/
│       │   └── test/
│       └── labels/
│           ├── train/
│           ├── val/
│           └── test/
├── scripts/
│   ├── clean_data.py           ← removes bad images
│   ├── check_balance.py        ← shows class counts
│   └── split_data.py          ← creates train/val/test split
├── training/
│   ├── train.py                ← runs on GPU system
│   ├── data.yaml               ← tells YOLO about our classes
│   └── runs/                   ← training results saved here
├── app/
│   ├── app.py                  ← Flask server
│   ├── model/
│   │   └── best.onnx           ← trained model goes here
│   ├── templates/
│   │   └── index.html          ← web page
│   └── static/
│       └── style.css
├── requirements_laptop.txt     ← libraries for laptop
├── requirements_gpu.txt        ← libraries for GPU system
└── README.md
```

---

## Treatment Recommendations (Hardcoded Dictionary)

```python
TREATMENTS = {
    "healthy": {
        "severity": "None",
        "action": "No action needed. Crop appears healthy.",
        "chemical": "None required.",
        "prevention": "Continue regular monitoring every 7 days."
    },
    "tomato_early_blight": {
        "severity_rules": {"low": "<3 spots", "medium": "3-10 spots", "high": ">10 spots"},
        "action": "Remove and destroy infected leaves immediately.",
        "chemical": "Apply Mancozeb 75WP at 2.5g per litre of water. Spray every 7 days.",
        "prevention": "Avoid overhead watering. Ensure good air circulation between plants."
    },
    "tomato_late_blight": {
        "action": "Urgent: Remove all infected plants to prevent spread.",
        "chemical": "Apply Metalaxyl + Mancozeb (Ridomil Gold) at 2g per litre. Spray every 5 days.",
        "prevention": "Use certified disease-free seeds. Avoid planting in wet areas."
    },
    "tomato_yellow_leaf_curl_virus": {
        "action": "No chemical cure. Remove infected plants immediately.",
        "chemical": "Control whitefly vectors with Imidacloprid 200SL at 0.5ml per litre.",
        "prevention": "Use virus-resistant tomato varieties. Install yellow sticky traps."
    },
    "maize_common_rust": {
        "action": "Apply fungicide at first sign of orange pustules.",
        "chemical": "Apply Propiconazole 25EC at 1ml per litre. Spray at 14-day intervals.",
        "prevention": "Plant rust-resistant maize varieties. Avoid late planting."
    },
    "maize_northern_blight": {
        "action": "Apply fungicide when lesions appear on lower leaves.",
        "chemical": "Apply Azoxystrobin 250SC at 1ml per litre. Spray every 14 days.",
        "prevention": "Crop rotation with non-host crops. Remove crop debris after harvest."
    },
    "wheat_rust_yellow": {
        "action": "Urgent: Spray immediately. Yellow rust spreads very fast.",
        "chemical": "Apply Tebuconazole 250EW at 1ml per litre. Repeat after 14 days.",
        "prevention": "Use rust-resistant wheat varieties. Monitor crop from tillering stage."
    },
    "aphid": {
        "action": "Spray affected plants. Check undersides of leaves.",
        "chemical": "Apply Dimethoate 40EC at 1.5ml per litre of water.",
        "prevention": "Encourage natural predators (ladybirds). Avoid excessive nitrogen fertiliser."
    },
    "spider_mite": {
        "action": "Spray leaf undersides where mites live.",
        "chemical": "Apply Abamectin 1.8EC at 1ml per litre. Do not spray in hot midday sun.",
        "prevention": "Maintain adequate soil moisture. Remove weeds around crop."
    },
    "cotton_leaf_curl_virus": {
        "action": "Remove and destroy severely infected plants.",
        "chemical": "Control whitefly with Thiamethoxam 25WG at 0.5g per litre.",
        "prevention": "Use virus-tolerant cotton varieties. Plant at recommended time."
    }
}
```

---

## Model Configuration (data.yaml)

```yaml
path: ../data/processed
train: images/train
val: images/val
test: images/test

nc: 10
names:
  0: healthy
  1: tomato_early_blight
  2: tomato_late_blight
  3: tomato_yellow_leaf_curl_virus
  4: maize_common_rust
  5: maize_northern_blight
  6: wheat_rust_yellow
  7: aphid
  8: spider_mite
  9: cotton_leaf_curl_virus
```

---

## Training Configuration

```python
from ultralytics import YOLO

model = YOLO('yolov8s.pt')  # start from pretrained weights

model.train(
    data='data.yaml',
    epochs=50,           # enough for good accuracy, fast enough
    imgsz=640,           # standard image size
    batch=16,            # adjust if GPU runs out of memory (try 8)
    patience=15,         # stop early if no improvement
    optimizer='AdamW',
    lr0=0.001,
    augment=True,        # automatic augmentation
    dropout=0.1,
    save=True,
    project='runs/train',
    name='fasalguard_v1'
)
```

---

## Accuracy Targets

| Metric | Minimum Acceptable | Good | Excellent |
|---|---|---|---|
| mAP50 | 70% | 80% | 90%+ |
| Precision | 70% | 80% | 90%+ |
| Recall | 65% | 75% | 85%+ |

If results are below minimum, retrain with more data or more epochs before proceeding to web app.

---

## GitHub Setup

Repository name: `fasalguard-ai`  
Visibility: Public (easier for submission)  
Branches: main only (no branching complexity for solo project)

### .gitignore (must include)
```
data/raw/
data/processed/
*.pt
*.onnx
__pycache__/
*.pyc
.env
runs/
```

Do NOT commit dataset images or model weights — they are too large for GitHub.

---

## Web App Pages

### Page 1: Upload Page (index.html)
- Title: FasalGuard AI
- Subtitle: Crop Pest & Disease Detection
- Large upload box (drag and drop or click to browse)
- Upload button
- Brief instruction text

### Page 2: Results Page (result.html)
- Shows uploaded image with bounding boxes drawn on it
- Detection name (e.g. "Tomato Early Blight")
- Confidence percentage
- Severity badge (Low / Medium / High — colour coded green/yellow/red)
- Treatment section with action, chemical, prevention
- "Analyse Another Image" button

---

## Definition of Done (What "Finished" Looks Like)

- [ ] Model trained with mAP50 ≥ 70%
- [ ] Web app runs locally with `python app.py`
- [ ] Can upload any crop image and get a result in under 10 seconds on CPU
- [ ] Results page shows bounding box image + treatment
- [ ] All code committed to GitHub with README
- [ ] Can be demonstrated live during presentation
