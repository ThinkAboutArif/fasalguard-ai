# FasalGuard AI — Phase-by-Phase AI Prompts

> **How to use this file:**  
> Each section below contains the exact prompt to give to your AI assistant at the start of that phase. Copy the entire prompt including the lines above and below it. Start a new chat if your current one is getting too long — just paste the new phase prompt and attach FasalGuard_PRD.md and PROGRESS_LOG.md.

---

## How to Start Any New Chat Session

Paste this at the very beginning of every new chat:

```
I am working on a project called FasalGuard AI — an AI crop pest detection system. 
I am attaching two files:
1. FasalGuard_PRD.md — the full project plan and architecture
2. PROGRESS_LOG.md — what has been done so far and what is next

Please read both files carefully before saying anything. Then tell me:
- What phase we are currently on
- What the next step is
- Which machine I should be on (LAPTOP or GPU SYSTEM)

Wait for me to confirm I am ready before giving any instructions.
Remember: I am a first-time ML student. Explain everything step by step. 
Do not move to the next step until I confirm the current one is working.
```

---

## PHASE 0 PROMPT — Environment Setup [LAPTOP]

```
I am starting Phase 0 of FasalGuard AI: Environment Setup.
I am on my LAPTOP. It runs Windows [tell the AI if you use Mac or Linux instead].
I have never set up a Python project before.

Here is what Phase 0 requires (from the PRD):
- Install Python 3.10
- Create the project folder structure
- Set up a virtual environment
- Install laptop libraries
- Set up Git and GitHub
- Create the fasalguard-ai repository
- Make the first commit

Rules you must follow:
1. One step at a time. Do not give me Step 2 until I confirm Step 1 is done.
2. Give click-by-click instructions — tell me which website to open, which button to click, what to type.
3. After each step, ask me to paste the output or confirm it worked before continuing.
4. If I get an error, stop and help me fix it before moving on.
5. After each completed step, tell me exactly what to write in PROGRESS_LOG.md.

Start with checking if Python is already installed. Give me the exact command to run.
```

---

## PHASE 1 PROMPT — Dataset Download & Organisation [LAPTOP]

```
I am starting Phase 1 of FasalGuard AI: Dataset Download and Organisation.
I am on my LAPTOP.
Phase 0 is complete (environment and GitHub are set up).

I need to download these datasets:
1. PlantVillage from Kaggle
2. Three datasets from Roboflow Universe (wheat rust, aphid, cotton leaf curl)

Then I need to run a script to rename and organise all images into the correct 
folder structure for training.

The 10 classes I am targeting are listed in FasalGuard_PRD.md under "Target Classes".

Rules you must follow:
1. One step at a time. One dataset at a time.
2. Click-by-click instructions — tell me exactly which website, which button, what to download.
3. For Roboflow: tell me exactly what to search, which dataset to pick, and which export 
   format to choose (it must be YOLOv8 format).
4. After each download, tell me how to verify the files are correct before moving on.
5. Write the harmonise_data.py script for me. Explain every line with a comment.
6. After the script runs, tell me how to count the images per class to verify.
7. Update PROGRESS_LOG.md — tell me exactly what to fill in after each dataset.

Start with checking if I have a Kaggle account. Ask me.
```

---

## PHASE 2 PROMPT — Data Cleaning [LAPTOP]

```
I am starting Phase 2 of FasalGuard AI: Data Cleaning.
I am on my LAPTOP.
Phases 0 and 1 are complete. All images are in data/processed/ organised by class.

I need you to write me 3 Python scripts:
1. clean_data.py — removes corrupt, blurry, and too-small images automatically
2. check_balance.py — counts images per class and shows a bar chart
3. (if needed) augment_data.py — increases image count for underrepresented classes

Rules you must follow:
1. Write one script at a time. Explain every single line with a comment above it.
2. Before I run any script, tell me exactly what it will do and what output I should expect.
3. After I run each script, ask me to paste the output so you can verify it worked.
4. If any class has fewer than 200 images after cleaning, automatically write the 
   augmentation script and tell me to run it.
5. Never delete original files — scripts should move bad images to a 'rejected/' folder, 
   not permanently delete them.
6. After all cleaning is done, tell me exactly what to fill in PROGRESS_LOG.md.

Start by asking me to run check_balance.py first so we can see the current state 
before cleaning anything.
```

---

## PHASE 3 PROMPT — Data Verification & Split [LAPTOP]

```
I am starting Phase 3 of FasalGuard AI: Data Verification and Train/Val/Test Split.
I am on my LAPTOP.
Phases 0, 1, and 2 are complete. Clean images are in data/processed/.

I need to:
1. Split data into train (80%), val (10%), test (10%) folders
2. Create the data.yaml file that tells YOLOv8 about our 10 classes
3. Verify everything looks correct before transferring to the GPU system
4. Zip the entire processed data folder for transfer

Rules you must follow:
1. Write the split_data.py script for me with comments on every line.
2. After the split, show me the exact count per folder so I can verify.
3. Write the data.yaml file for me — show me the exact content.
4. Tell me how to do a manual spot check — I will open 5 images per class myself 
   and confirm the labels match.
5. Tell me how to zip the folder (exact command).
6. Tell me what to fill in PROGRESS_LOG.md after each step.

Important: The bounding box labels (from Roboflow datasets) must be in the 
labels/ folder mirroring the images/ folder structure. Verify this is correct.

Start by asking me to show you the current folder structure 
(I will run: tree data/processed/ or dir data/processed/ and paste the output).
```

---

## PHASE 4 PROMPT — Model Training [GPU SYSTEM]

```
I am starting Phase 4 of FasalGuard AI: Model Training.
I am now on the SCHOOL GPU SYSTEM (not my laptop).
Phases 0-3 are complete on my laptop. I have a zip file of the cleaned dataset.

This computer has an NVIDIA GPU. I do not know the exact model.
I have never trained a machine learning model before.

I need to:
1. Verify the GPU is working
2. Install Python, PyTorch with CUDA, and Ultralytics YOLOv8
3. Extract my dataset zip
4. Create the training script
5. Run training and monitor it
6. Understand the results

Rules you must follow:
1. Start by helping me check what GPU this computer has (exact command).
2. One installation step at a time — verify each one before the next.
3. Before starting training, verify the data.yaml paths are correct for THIS computer.
4. Show me how to start training and what the output should look like.
5. Explain what the numbers mean during training (mAP, precision, recall, loss).
6. If training crashes, ask me to paste the error immediately.
7. Tell me what counts as a good result and what to do if results are bad.
8. After training, tell me where the best.pt file is saved.
9. Tell me exactly what to fill in PROGRESS_LOG.md.

Important: If GPU runs out of memory, reduce batch size from 16 to 8. 
Tell me how to do this.

Start by asking me to paste the output of: nvidia-smi
```

---

## PHASE 5 PROMPT — Model Export & Transfer [GPU SYSTEM → LAPTOP]

```
I am starting Phase 5 of FasalGuard AI: Model Export and Transfer.
I am on the SCHOOL GPU SYSTEM.
Training is complete. The best.pt file is saved in runs/train/fasalguard_v1/weights/

I need to:
1. Export the trained model from .pt format to ONNX format
   (ONNX runs on CPU — this is what my laptop will use)
2. Verify the ONNX export worked
3. Test inference with one image on the GPU system
4. Transfer the ONNX file to my laptop

Rules you must follow:
1. Write the export script for me with explanations.
2. After export, tell me how to verify the file is valid.
3. Give me a quick test script to run inference on one image — 
   tell me what the output should look like.
4. Tell me the best method to transfer the file 
   (USB drive, Google Drive, or email — ask me which I prefer).
5. After transfer, tell me how to verify it works on my laptop CPU.
6. Tell me what to fill in PROGRESS_LOG.md.

The ONNX file should end up at: app/model/best.onnx on my laptop.

Start by showing me the exact export command.
```

---

## PHASE 6 PROMPT — Flask Web App [LAPTOP]

```
I am starting Phase 6 of FasalGuard AI: Building the Flask Web Application.
I am on my LAPTOP.
The trained model (best.onnx) is in app/model/

I need to build a simple website where:
- Page 1: Upload a crop image (drag and drop or browse)
- Page 2: See the result with bounding box image, pest name, severity, and treatment

Tech: Flask (Python), plain HTML/CSS/JavaScript. No React, no complicated frameworks.

Rules you must follow:
1. Build one file at a time. Show me the complete file content.
2. After each file, tell me how to test that specific part before moving on.
3. The design should look clean and professional — use green as main colour 
   (agriculture theme).
4. Explain what each section of code does.
5. Do not use any CSS framework (no Bootstrap) — write plain CSS.
6. The app must work fully offline after setup.
7. Tell me what to fill in PROGRESS_LOG.md after each file.

Build in this order:
1. app.py (Flask server, no model yet — just routing)
2. index.html (upload page)
3. style.css (styling)
4. result.html (results page)

Start with app.py. Show me the complete file.
```

---

## PHASE 7 PROMPT — Model Integration & Testing [LAPTOP]

```
I am starting Phase 7 of FasalGuard AI: Model Integration and Testing.
I am on my LAPTOP.
The Flask web app is built and running. The model is at app/model/best.onnx.
The treatment dictionary is in FasalGuard_PRD.md.

I need to:
1. Add the ONNX model loading code to app.py
2. Write the inference function (run the image through the model)
3. Write the bounding box drawing function
4. Write the severity calculation function
5. Connect everything so uploading an image shows a real prediction

Rules you must follow:
1. Add one function at a time. Test each before adding the next.
2. Use OpenCV for image processing and drawing bounding boxes.
3. Use onnxruntime for running the ONNX model.
4. For each function, explain what goes in and what comes out.
5. Give me specific test images to download to test each class.
6. If the model gives wrong predictions, tell me how to diagnose why.
7. After integration, give me a testing checklist of 10 images to upload.
8. Tell me what to fill in PROGRESS_LOG.md after each successful test.

The severity logic should be:
- Low: 1 detection, confidence < 60%
- Medium: 1-2 detections, confidence 60-80%  
- High: 3+ detections OR confidence > 80%

Start by showing me the updated app.py with model loading added.
```

---

## PHASE 8 PROMPT — GitHub Final Commit [LAPTOP]

```
I am starting Phase 8 of FasalGuard AI: Final GitHub Commit and Cleanup.
I am on my LAPTOP.
The full system is working. I need to clean up and make the final submission commit.

I need to:
1. Verify .gitignore is correct (no large files, no model weights, no datasets)
2. Write a good README.md for the GitHub repo
3. Clean up any unnecessary files
4. Make the final commit with a good commit message
5. Push to GitHub and verify the repo looks good

Rules you must follow:
1. Show me the .gitignore file first — I will verify before any commit.
2. Write a complete README.md that includes:
   - Project title and description
   - What it does (with one screenshot placeholder)
   - How to install and run it (step by step)
   - The 10 classes it detects
   - Tech stack
   - My name and university
3. After the final push, tell me how to verify the repo is correct on GitHub.
4. Give me a final checklist of everything that should be working for the presentation.
5. Mark all phases as Complete in PROGRESS_LOG.md.

Start by showing me the final .gitignore content.
```

---

## EMERGENCY PROMPTS

### If You Get Stuck Mid-Phase

```
I am stuck in Phase [NUMBER] of FasalGuard AI. Here is the error I am getting:

[PASTE ERROR HERE]

I was trying to: [DESCRIBE WHAT YOU WERE DOING]
The last command I ran was: [PASTE COMMAND]

Please help me fix this error before we continue. 
Do not move on until this is resolved.
```

### If You Need to Start a New Chat (Long Session)

```
My previous chat got too long. I am continuing FasalGuard AI.
I am attaching:
1. FasalGuard_PRD.md — full project plan
2. PROGRESS_LOG.md — what is done and what is next

Read both files. Tell me:
- Current phase
- Last completed step  
- What the next step is
- Which machine I should be on

Then continue from where we left off.
```

### If Training Results Are Bad (mAP50 below 60%)

```
My FasalGuard AI training finished but the results are poor.
mAP50 is: [VALUE]
Precision: [VALUE]
Recall: [VALUE]

Here is my data.yaml:
[PASTE CONTENT]

Here are my class counts:
[PASTE CHECK_BALANCE OUTPUT]

Please diagnose why the results are low and tell me:
1. What is likely causing the poor results
2. What I should change
3. Whether I need more data or different training settings
4. The exact changes to make before retraining
```
