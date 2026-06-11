# FasalGuard AI — Progress Log

> **AI Assistant Instructions:**
> Read this file at the start of every session. It tells you exactly what has been completed, what failed, and what to do next. After completing any step, update the relevant section immediately. Never skip updating this log.

---

## Project Status Overview

| Phase | Name | Status | Machine |
|---|---|---|---|
| Phase 0 | Environment Setup | ✅ COMPLETE | LAPTOP |
| Phase 1 | Dataset Download & Organisation | 🔄 IN PROGRESS | LAPTOP |
| Phase 2 | Data Cleaning | ⬜ NOT STARTED | LAPTOP |
| Phase 3 | Data Verification & Split | ⬜ NOT STARTED | LAPTOP |
| Phase 4 | Model Training | ⬜ NOT STARTED | GPU SYSTEM |
| Phase 5 | Model Export & Transfer | ⬜ NOT STARTED | GPU SYSTEM → LAPTOP |
| Phase 6 | Flask Web App | ⬜ NOT STARTED | LAPTOP |
| Phase 7 | Model Integration & Testing | ⬜ NOT STARTED | LAPTOP |
| Phase 8 | GitHub Final Commit | ⬜ NOT STARTED | LAPTOP |

**Status Key:** ⬜ Not Started | 🔄 In Progress | ✅ Complete | ❌ Blocked

---

## What To Do Next (Read This First)

**Current phase:** Phase 1 — Dataset Organisation  
**Current machine:** LAPTOP  
**Next action:** Run `organise_data.py` to rename the 38 PlantVillage folders into clean class names and copy images into `data/processed/` — then run `check_balance.py` to see image counts per class.

---

## Phase 0: Environment Setup [LAPTOP] — ✅ COMPLETE

### What Was Done
- Python installed and working
- Project folder: `C:\Users\dhhdb\Desktop\fasalguard\`
- Virtual environment created and named: `fasalguard_env`
- Virtual environment is activated (prompt shows `(fasalguard_env)`)
- GitHub repository created: https://github.com/ThinkAboutArif/fasalguard-ai.git
- Local repo connected to GitHub
- 2 commits already pushed to GitHub

### Notes
- No errors encountered in Phase 0

---

## Phase 1: Dataset Download & Organisation [LAPTOP] — 🔄 IN PROGRESS

### What Was Done
- PlantVillage dataset downloaded from Kaggle
- Extracted to: `C:\Users\dhhdb\Desktop\fasalguard\data\raw\plantvillage\`
- All 38 class folders confirmed present

### 38 Folders Confirmed Present
```
Apple___Apple_scab
Apple___Black_rot
Apple___Cedar_apple_rust
Apple___healthy
Blueberry___healthy
Cherry_(including_sour)___healthy
Cherry_(including_sour)___Powdery_mildew
Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot
Corn_(maize)___Common_rust_
Corn_(maize)___healthy
Corn_(maize)___Northern_Leaf_Blight
Grape___Black_rot
Grape___Esca_(Black_Measles)
Grape___healthy
Grape___Leaf_blight_(Isariopsis_Leaf_Spot)
Orange___Haunglongbing_(Citrus_greening)
Peach___Bacterial_spot
Peach___healthy
Pepper,_bell___Bacterial_spot
Pepper,_bell___healthy
Potato___Early_blight
Potato___healthy
Potato___Late_blight
Raspberry___healthy
Soybean___healthy
Squash___Powdery_mildew
Strawberry___healthy
Strawberry___Leaf_scorch
Tomato___Bacterial_spot
Tomato___Early_blight
Tomato___healthy
Tomato___Late_blight
Tomato___Leaf_Mold
Tomato___Septoria_leaf_spot
Tomato___Spider_mites Two-spotted_spider_mite
Tomato___Target_Spot
Tomato___Tomato_mosaic_virus
Tomato___Tomato_Yellow_Leaf_Curl_Virus
```

### What Is Still Needed to Complete Phase 1
- [ ] `scripts/organise_data.py` written and run — copies+renames images to `data/processed/`
- [ ] `scripts/check_balance.py` written and run — shows image count per class
- [ ] All 38 class folders confirmed in `data/processed/`
- [ ] Image counts per class recorded in the table below
- [ ] GitHub commit: `data: plantvillage dataset organised into processed folder`

### Class Image Counts (Fill After organise_data.py Runs)
| Class Name | Image Count | Enough? (200+ needed) |
|---|---|---|
| apple_scab | ___ | ___ |
| apple_black_rot | ___ | ___ |
| apple_cedar_rust | ___ | ___ |
| apple_healthy | ___ | ___ |
| blueberry_healthy | ___ | ___ |
| cherry_healthy | ___ | ___ |
| cherry_powdery_mildew | ___ | ___ |
| maize_cercospora | ___ | ___ |
| maize_common_rust | ___ | ___ |
| maize_healthy | ___ | ___ |
| maize_northern_blight | ___ | ___ |
| grape_black_rot | ___ | ___ |
| grape_esca | ___ | ___ |
| grape_healthy | ___ | ___ |
| grape_leaf_blight | ___ | ___ |
| orange_citrus_greening | ___ | ___ |
| peach_bacterial_spot | ___ | ___ |
| peach_healthy | ___ | ___ |
| pepper_bacterial_spot | ___ | ___ |
| pepper_healthy | ___ | ___ |
| potato_early_blight | ___ | ___ |
| potato_healthy | ___ | ___ |
| potato_late_blight | ___ | ___ |
| raspberry_healthy | ___ | ___ |
| soybean_healthy | ___ | ___ |
| squash_powdery_mildew | ___ | ___ |
| strawberry_healthy | ___ | ___ |
| strawberry_leaf_scorch | ___ | ___ |
| tomato_bacterial_spot | ___ | ___ |
| tomato_early_blight | ___ | ___ |
| tomato_healthy | ___ | ___ |
| tomato_late_blight | ___ | ___ |
| tomato_leaf_mold | ___ | ___ |
| tomato_septoria | ___ | ___ |
| tomato_spider_mite | ___ | ___ |
| tomato_target_spot | ___ | ___ |
| tomato_mosaic_virus | ___ | ___ |
| tomato_yellow_leaf_curl | ___ | ___ |

### Notes / Errors Encountered
```
(record any errors and how they were fixed here)
```

---

## Phase 2: Data Cleaning [LAPTOP] — ⬜ NOT STARTED

### Steps Checklist
- [ ] `scripts/clean_data.py` written and run
  - Corrupt images removed: ___
  - Images under 100x100px removed: ___
  - Blurry images removed: ___
- [ ] `scripts/check_balance.py` run after cleaning — bar chart saved
- [ ] Any class under 200 images after cleaning? List: ___________
- [ ] If yes: augmentation script written and run for those classes
- [ ] Final counts recorded in table below
- [ ] GitHub commit: `data: cleaning scripts and verified class balance`

### Clean Dataset Counts (Fill After Cleaning)
| Class | Before | After Cleaning | Status |
|---|---|---|---|
| apple_scab | ___ | ___ | ___ |
| apple_black_rot | ___ | ___ | ___ |
| apple_cedar_rust | ___ | ___ | ___ |
| apple_healthy | ___ | ___ | ___ |
| blueberry_healthy | ___ | ___ | ___ |
| cherry_healthy | ___ | ___ | ___ |
| cherry_powdery_mildew | ___ | ___ | ___ |
| maize_cercospora | ___ | ___ | ___ |
| maize_common_rust | ___ | ___ | ___ |
| maize_healthy | ___ | ___ | ___ |
| maize_northern_blight | ___ | ___ | ___ |
| grape_black_rot | ___ | ___ | ___ |
| grape_esca | ___ | ___ | ___ |
| grape_healthy | ___ | ___ | ___ |
| grape_leaf_blight | ___ | ___ | ___ |
| orange_citrus_greening | ___ | ___ | ___ |
| peach_bacterial_spot | ___ | ___ | ___ |
| peach_healthy | ___ | ___ | ___ |
| pepper_bacterial_spot | ___ | ___ | ___ |
| pepper_healthy | ___ | ___ | ___ |
| potato_early_blight | ___ | ___ | ___ |
| potato_healthy | ___ | ___ | ___ |
| potato_late_blight | ___ | ___ | ___ |
| raspberry_healthy | ___ | ___ | ___ |
| soybean_healthy | ___ | ___ | ___ |
| squash_powdery_mildew | ___ | ___ | ___ |
| strawberry_healthy | ___ | ___ | ___ |
| strawberry_leaf_scorch | ___ | ___ | ___ |
| tomato_bacterial_spot | ___ | ___ | ___ |
| tomato_early_blight | ___ | ___ | ___ |
| tomato_healthy | ___ | ___ | ___ |
| tomato_late_blight | ___ | ___ | ___ |
| tomato_leaf_mold | ___ | ___ | ___ |
| tomato_septoria | ___ | ___ | ___ |
| tomato_spider_mite | ___ | ___ | ___ |
| tomato_target_spot | ___ | ___ | ___ |
| tomato_mosaic_virus | ___ | ___ | ___ |
| tomato_yellow_leaf_curl | ___ | ___ | ___ |
| **TOTAL** | ___ | ___ | ___ |

### Notes / Errors Encountered
```
(record any errors and how they were fixed here)
```

---

## Phase 3: Data Verification & Split [LAPTOP] — ⬜ NOT STARTED

### Steps Checklist
- [ ] `scripts/split_data.py` written and run — 80/10/10 split created
- [ ] Train image count: ___
- [ ] Val image count: ___
- [ ] Test image count: ___
- [ ] `training/class_names.json` created with all 38 class names in order
- [ ] Manual spot check: 5 random images per class reviewed visually — OK? YES / NO
- [ ] Data folder zipped for transfer to GPU system
- [ ] Zip file size: ___ GB
- [ ] GitHub commit: `data: train/val/test split complete, class_names.json added`

### Notes / Errors Encountered
```
(record any errors and how they were fixed here)
```

---

## Phase 4: Model Training [GPU SYSTEM] — ⬜ NOT STARTED

### Steps Checklist
- [ ] Logged in to GPU system at school
- [ ] GPU detected — name: ___________
- [ ] Python 3.10+ confirmed on GPU system
- [ ] PyTorch with CUDA installed — GPU confirmed working in PyTorch
- [ ] Data zip transferred to GPU system
- [ ] Data extracted, paths verified
- [ ] `training/train.py` written
- [ ] Training started — first epoch completed without error
- [ ] Training completed
  - Total epochs run: ___
  - Training time: ___
- [ ] Best model saved at: `training/runs/fasalguard_v1/best_model.pt`

### Training Results
| Metric | Value | Acceptable (≥85%)? |
|---|---|---|
| Final Validation Accuracy | ___ | ___ |
| Best Validation Accuracy | ___ | ___ |
| Final Training Loss | ___ | — |

**Accuracy ≥ 85%?** YES / NO  
**If NO — action taken:** ___________

### Notes / Errors Encountered
```
(record any errors and how they were fixed here)
```

---

## Phase 5: Model Export & Transfer [GPU SYSTEM → LAPTOP] — ⬜ NOT STARTED

### Steps Checklist
- [ ] Model exported to TorchScript format: `fasalguard_model.pt`
- [ ] `training/class_names.json` confirmed present alongside model
- [ ] Test inference on GPU system with one image — correct prediction? YES / NO
- [ ] Model file size: ___ MB
- [ ] Transfer method used: ___________
- [ ] Model placed on laptop at: `app/model/fasalguard_model.pt`
- [ ] `class_names.json` placed at: `app/model/class_names.json`
- [ ] Test inference on laptop CPU — works? YES / NO
- [ ] CPU inference time: ___ seconds

### Notes / Errors Encountered
```
(record any errors and how they were fixed here)
```

---

## Phase 6: Flask Web App [LAPTOP] — ⬜ NOT STARTED

### Steps Checklist
- [ ] `app/app.py` created — Flask routing only, no model yet
- [ ] Flask runs: `python app.py` — no errors
- [ ] `app/templates/index.html` created — upload page
- [ ] Upload page loads at http://localhost:5000
- [ ] `app/static/style.css` created — green agriculture theme
- [ ] `app/templates/result.html` created — results page
- [ ] Results page renders correctly with dummy data
- [ ] GitHub commit: `app: flask web app pages and styling complete`

### Notes / Errors Encountered
```
(record any errors and how they were fixed here)
```

---

## Phase 7: Model Integration & Testing [LAPTOP] — ⬜ NOT STARTED

### Steps Checklist
- [ ] Model loading code added to `app.py`
- [ ] Inference function written and tested
- [ ] Grad-CAM heatmap generation working
- [ ] Severity calculation working
- [ ] Treatment lookup returning correct text for all classes
- [ ] End-to-end test with 10 demo images (see table below)
- [ ] All 10 images give correct or sensible predictions
- [ ] Inference time under 10 seconds on CPU: YES / NO
- [ ] App does not crash on unexpected image: YES / NO
- [ ] GitHub commit: `app: model integrated, grad-cam working, end-to-end tested`

### Demo Image Test Results
| # | Image | Expected | Actual | Correct? |
|---|---|---|---|---|
| 1 | tomato late blight | tomato_late_blight | ___ | ___ |
| 2 | tomato healthy | tomato_healthy | ___ | ___ |
| 3 | maize common rust | maize_common_rust | ___ | ___ |
| 4 | potato late blight | potato_late_blight | ___ | ___ |
| 5 | apple scab | apple_scab | ___ | ___ |
| 6 | tomato yellow leaf curl | tomato_yellow_leaf_curl | ___ | ___ |
| 7 | pepper bacterial spot | pepper_bacterial_spot | ___ | ___ |
| 8 | grape black rot | grape_black_rot | ___ | ___ |
| 9 | tomato spider mite | tomato_spider_mite | ___ | ___ |
| 10 | maize northern blight | maize_northern_blight | ___ | ___ |

### Notes / Errors Encountered
```
(record any errors and how they were fixed here)
```

---

## Phase 8: GitHub Final Commit [LAPTOP] — ⬜ NOT STARTED

### Steps Checklist
- [ ] `.gitignore` verified — no datasets, no model weights, no pycache tracked
- [ ] `README.md` written with description, setup steps, class list, screenshots
- [ ] All scripts committed
- [ ] All app files committed
- [ ] Final commit pushed: `final: readme updated, project complete`
- [ ] GitHub repo verified public and accessible
- [ ] Repo URL confirmed: https://github.com/ThinkAboutArif/fasalguard-ai.git

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

| Date | Machine | Phase Worked On | Steps Completed | Notes |
|---|---|---|---|---|
| Wed | Laptop | 0 + Phase 1 start | Env setup, GitHub, PlantVillage download | 2 commits made |
