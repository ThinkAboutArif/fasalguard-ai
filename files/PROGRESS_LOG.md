# FasalGuard AI — Progress Log

> **AI Assistant Instructions:**  
> Read this file at the start of every session. It tells you exactly what has been completed, what failed, and what to do next. After completing any step, update the relevant section immediately. Never skip updating this log.

---

## Project Status Overview

| Phase | Name | Status | Machine |
|---|---|---|---|
| Phase 0 | Environment Setup | ⬜ NOT STARTED | LAPTOP |
| Phase 1 | Dataset Download & Organisation | ⬜ NOT STARTED | LAPTOP |
| Phase 2 | Data Cleaning | ⬜ NOT STARTED | LAPTOP |
| Phase 3 | Data Verification | ⬜ NOT STARTED | LAPTOP |
| Phase 4 | Model Training | ⬜ NOT STARTED | GPU SYSTEM |
| Phase 5 | Model Export & Transfer | ⬜ NOT STARTED | GPU SYSTEM → LAPTOP |
| Phase 6 | Flask Web App | ⬜ NOT STARTED | LAPTOP |
| Phase 7 | Integration & Testing | ⬜ NOT STARTED | LAPTOP |
| Phase 8 | GitHub & Final Commit | ⬜ NOT STARTED | LAPTOP |

**Status Key:** ⬜ Not Started | 🔄 In Progress | ✅ Complete | ❌ Blocked

---

## Current Session

**Date:** ___________  
**Machine:** ___________  
**Working On:** ___________  
**Resume Point:** ___________

---

## Phase 0: Environment Setup [LAPTOP]

**Status:** ⬜ NOT STARTED

### Steps Checklist
- [ ] Python 3.10 installed and verified (`python --version` shows 3.10.x)
- [ ] pip verified (`pip --version`)
- [ ] Project folder created at: ___________
- [ ] Virtual environment created (`fasalguard_env`)
- [ ] Virtual environment activated
- [ ] requirements_laptop.txt created
- [ ] All laptop libraries installed with no errors
- [ ] Git installed and verified (`git --version`)
- [ ] GitHub account ready (username: ___________)
- [ ] Repository created: `fasalguard-ai`
- [ ] Local repo initialised and connected to GitHub
- [ ] Initial commit pushed

### Notes / Errors Encountered
```
(record any errors and how they were fixed here)
```

---

## Phase 1: Dataset Download & Organisation [LAPTOP]

**Status:** ⬜ NOT STARTED

### Steps Checklist

#### PlantVillage Dataset
- [ ] Kaggle account created / logged in
- [ ] Kaggle API token downloaded (kaggle.json)
- [ ] PlantVillage dataset downloaded (URL: https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset)
- [ ] Extracted to: `data/raw/plantvillage/`
- [ ] Verified folder count inside: ___________ folders
- [ ] Identified correct class folders:
  - [ ] Tomato___Early_blight → found, image count: ___
  - [ ] Tomato___Late_blight → found, image count: ___
  - [ ] Tomato___Tomato_Yellow_Leaf_Curl_Virus → found, image count: ___
  - [ ] Tomato___Spider_mites Two-spotted_spider_mite → found, image count: ___
  - [ ] Corn_(maize)___Common_rust_ → found, image count: ___
  - [ ] Corn_(maize)___Northern_Leaf_Blight → found, image count: ___
  - [ ] Tomato___healthy → found, image count: ___
  - [ ] Corn_(maize)___healthy → found, image count: ___

#### Roboflow Datasets
- [ ] Roboflow account created at roboflow.com
- [ ] Wheat rust dataset found and downloaded (YOLO format)
  - Dataset name used: ___________
  - Image count: ___________
- [ ] Aphid dataset found and downloaded (YOLO format)
  - Dataset name used: ___________
  - Image count: ___________
- [ ] Cotton leaf curl dataset found and downloaded (YOLO format)
  - Dataset name used: ___________
  - Image count: ___________
- [ ] All Roboflow datasets extracted to `data/raw/roboflow_*/`

#### Folder Organisation
- [ ] `harmonise_data.py` script written
- [ ] Script run successfully — all images copied to `data/processed/` with correct class names
- [ ] Verified all 10 class folders exist in `data/processed/`

### Class Image Counts After Organisation
| Class | Count | Enough? (need 200+) |
|---|---|---|
| healthy | ___ | ___ |
| tomato_early_blight | ___ | ___ |
| tomato_late_blight | ___ | ___ |
| tomato_yellow_leaf_curl_virus | ___ | ___ |
| maize_common_rust | ___ | ___ |
| maize_northern_blight | ___ | ___ |
| wheat_rust_yellow | ___ | ___ |
| aphid | ___ | ___ |
| spider_mite | ___ | ___ |
| cotton_leaf_curl_virus | ___ | ___ |

### Notes / Errors Encountered
```
(record any errors and how they were fixed here)
```

---

## Phase 2: Data Cleaning [LAPTOP]

**Status:** ⬜ NOT STARTED

### Steps Checklist
- [ ] `scripts/clean_data.py` written
- [ ] Corrupt image removal run — removed: ___ images
- [ ] Small image removal run (under 100x100px) — removed: ___ images
- [ ] Blurry image removal run — removed: ___ images
- [ ] Duplicate removal run — removed: ___ images
- [ ] `scripts/check_balance.py` run — chart generated
- [ ] Class balance reviewed — any classes under 200 images? List: ___________
- [ ] Augmentation run for underrepresented classes (if needed)
- [ ] Final image counts recorded (see table below)

### Final Clean Dataset Counts
| Class | Before Cleaning | After Cleaning | Augmented To |
|---|---|---|---|
| healthy | ___ | ___ | ___ |
| tomato_early_blight | ___ | ___ | ___ |
| tomato_late_blight | ___ | ___ | ___ |
| tomato_yellow_leaf_curl_virus | ___ | ___ | ___ |
| maize_common_rust | ___ | ___ | ___ |
| maize_northern_blight | ___ | ___ | ___ |
| wheat_rust_yellow | ___ | ___ | ___ |
| aphid | ___ | ___ | ___ |
| spider_mite | ___ | ___ | ___ |
| cotton_leaf_curl_virus | ___ | ___ | ___ |
| **TOTAL** | ___ | ___ | ___ |

### Notes / Errors Encountered
```
(record any errors and how they were fixed here)
```

---

## Phase 3: Data Verification [LAPTOP]

**Status:** ⬜ NOT STARTED

### Steps Checklist
- [ ] `scripts/split_data.py` run — 80/10/10 split done
- [ ] Train folder image count: ___
- [ ] Val folder image count: ___
- [ ] Test folder image count: ___
- [ ] `data.yaml` file created and verified
- [ ] Spot check done — manually viewed 5 images per class, labels look correct: YES / NO
- [ ] Data folder zipped for transfer to GPU system
- [ ] Zip file size: ___ GB

### Notes / Errors Encountered
```
(record any errors and how they were fixed here)
```

---

## Phase 4: Model Training [GPU SYSTEM]

**Status:** ⬜ NOT STARTED

### Steps Checklist
- [ ] Logged in to GPU system at school
- [ ] Python 3.10 verified on GPU system
- [ ] PyTorch with CUDA installed — verified GPU is detected
- [ ] GPU name detected: ___________
- [ ] Ultralytics YOLOv8 installed
- [ ] Data zip transferred to GPU system
- [ ] Data extracted to correct folder
- [ ] `data.yaml` path verified — points to correct folders
- [ ] `training/train.py` script run
- [ ] Training started — first epoch completed without error
- [ ] Training completed — total epochs: ___
- [ ] Training time: ___
- [ ] Best weights saved at: `runs/train/fasalguard_v1/weights/best.pt`

### Training Results
| Metric | Value | Acceptable? |
|---|---|---|
| mAP50 | ___ | ___ |
| mAP50-95 | ___ | ___ |
| Precision | ___ | ___ |
| Recall | ___ | ___ |

**mAP50 ≥ 70%?** YES / NO  
**If NO:** Action taken: ___________

### Notes / Errors Encountered
```
(record any errors and how they were fixed here)
```

---

## Phase 5: Model Export & Transfer [GPU SYSTEM → LAPTOP]

**Status:** ⬜ NOT STARTED

### Steps Checklist
- [ ] Model exported to ONNX format (`best.onnx`)
- [ ] ONNX file size: ___ MB
- [ ] ONNX file transferred to laptop (method used: ___________)
- [ ] ONNX file placed at: `app/model/best.onnx`
- [ ] Test inference run on laptop with one image — works? YES / NO
- [ ] Inference time on laptop CPU: ___ seconds

### Notes / Errors Encountered
```
(record any errors and how they were fixed here)
```

---

## Phase 6: Flask Web App [LAPTOP]

**Status:** ⬜ NOT STARTED

### Steps Checklist
- [ ] `app/app.py` created
- [ ] `app/templates/index.html` created (upload page)
- [ ] `app/templates/result.html` created (results page)
- [ ] `app/static/style.css` created
- [ ] Flask app runs with `python app.py` — no errors
- [ ] Upload page loads at http://localhost:5000
- [ ] Can select and upload an image
- [ ] Results page displays (even before model connected)

### Notes / Errors Encountered
```
(record any errors and how they were fixed here)
```

---

## Phase 7: Integration & Testing [LAPTOP]

**Status:** ⬜ NOT STARTED

### Steps Checklist
- [ ] ONNX model loading code added to app.py
- [ ] Inference function written and tested
- [ ] Bounding box drawing on image working
- [ ] Severity calculation working
- [ ] Treatment lookup returning correct text
- [ ] End-to-end test: upload real tomato image → correct prediction
- [ ] End-to-end test: upload real wheat image → correct prediction
- [ ] End-to-end test: upload healthy leaf → "healthy" result
- [ ] Tested with a bad image (no crop) — app doesn't crash
- [ ] Inference time under 15 seconds on CPU: YES / NO

### Test Results
| Image Used | Expected Result | Actual Result | Correct? |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

### Notes / Errors Encountered
```
(record any errors and how they were fixed here)
```

---

## Phase 8: GitHub & Final Commit [LAPTOP]

**Status:** ⬜ NOT STARTED

### Steps Checklist
- [ ] .gitignore verified — no large files being tracked
- [ ] README.md written with: project description, how to run, screenshots
- [ ] All Python scripts committed
- [ ] Web app files committed
- [ ] data.yaml committed
- [ ] requirements files committed
- [ ] Final commit pushed to GitHub
- [ ] GitHub repo URL: ___________
- [ ] Repo is public and accessible

### Notes / Errors Encountered
```
(record any errors and how they were fixed here)
```

---

## Known Issues / Bugs

| Issue | Phase | Status | Fix Applied |
|---|---|---|---|
| | | | |

---

## Session History

| Date | Machine | Phases Worked On | Completed Steps | Notes |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |
