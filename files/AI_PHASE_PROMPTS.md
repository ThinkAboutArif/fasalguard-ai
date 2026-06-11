# FasalGuard AI — Phase-by-Phase AI Prompts

> **How to use this file:**
> Each section contains the exact prompt to paste into a new AI chat for that phase.
> Always attach BOTH `FasalGuard_PRD.md` AND `PROGRESS_LOG.md` when starting any chat.
> Copy the full prompt including all the lines inside the code block.

---

## HOW TO START ANY NEW CHAT SESSION

Paste this at the very beginning of every new chat, then attach both files:

```
I am working on a project called FasalGuard AI — an AI-powered crop disease detection web app.
I am attaching two files:
1. FasalGuard_PRD.md — full project plan, architecture, all code references
2. PROGRESS_LOG.md — exact record of what is done and what is next

Please read BOTH files fully before saying anything.
Then tell me:
- Which phase we are currently on
- What the very next step is
- Which machine I should be on (LAPTOP or GPU SYSTEM)

Do not start any instructions until I confirm I am ready.

My setup:
- Laptop: Windows, CPU only, virtual environment called fasalguard_env
- Project folder: C:\Users\dhhdb\Desktop\fasalguard\
- GitHub: https://github.com/ThinkAboutArif/fasalguard-ai.git
- School GPU system: NVIDIA GPU (model unknown), used for training only

Rules you must follow for this entire conversation:
1. One step at a time. Never give the next step until I confirm the current one works.
2. Click-by-click instructions — tell me which folder to open, which command to run, what to look for.
3. Put every command in a code block and explain what it does before I run it.
4. After every step ask me to paste the output or confirm it worked.
5. If I report an error, stop and fix it before anything else.
6. After each completed phase, give me the exact git commit command to run.
7. After each completed step, tell me exactly what to update in PROGRESS_LOG.md.
8. Never assume a library is installed — always check first.
```

---

## PHASE 1 PROMPT — Dataset Organisation [LAPTOP]

```
I am continuing FasalGuard AI. I am on my LAPTOP.

Phase 0 is complete. Phase 1 is in progress.

What is done so far in Phase 1:
- PlantVillage dataset downloaded and extracted
- Location: C:\Users\dhhdb\Desktop\fasalguard\data\raw\plantvillage\
- All 38 folders are confirmed present

What still needs to be done in Phase 1:
1. Write and run organise_data.py — this should copy images from each of the 38
   raw PlantVillage folders into data\processed\ using our clean class names
   (the mapping of original folder names to clean class names is in FasalGuard_PRD.md
   under "All 38 Classes")
2. Write and run check_balance.py — show image count per class as a bar chart
3. Record all image counts in PROGRESS_LOG.md
4. Git commit when done

Rules:
1. One script at a time. Write organise_data.py first.
2. Explain every single line of the script with a comment.
3. Before I run it, tell me exactly what it will do and what the output should look like.
4. After it runs, tell me how to verify it worked correctly.
5. Do not write check_balance.py until organise_data.py is confirmed working.
6. After both scripts work, tell me the exact git commit command to run.
7. Tell me exactly what to fill in PROGRESS_LOG.md after each script.

Start by showing me the complete organise_data.py script.
The script must:
- Read from: C:\Users\dhhdb\Desktop\fasalguard\data\raw\plantvillage\
- Write to: C:\Users\dhhdb\Desktop\fasalguard\data\processed\
- Create one subfolder per class using our clean names (e.g. tomato_early_blight)
- Copy (not move) images so the raw data stays untouched
- Print progress so I can see it working
- At the end, print the count of images copied per class
```

---

## PHASE 2 PROMPT — Data Cleaning [LAPTOP]

```
I am continuing FasalGuard AI. I am on my LAPTOP.
Phases 0 and 1 are complete. Starting Phase 2: Data Cleaning.

Data is organised in: C:\Users\dhhdb\Desktop\fasalguard\data\processed\
There are 38 class folders.

I need 3 scripts written one at a time:
1. clean_data.py — automatically removes bad images (corrupt, too small, blurry)
2. check_balance.py — counts images per class and shows a bar chart  
3. augment_data.py — only needed if any class has fewer than 200 images after cleaning

Rules:
1. Write clean_data.py first. Do not write the others until this one works.
2. Explain every line with a comment.
3. The script must MOVE bad images to a data\rejected\ folder — never permanently delete.
   This way if something goes wrong we still have the originals.
4. Print a summary at the end: how many images were moved out per class and why.
5. After clean_data.py works, write check_balance.py.
6. After check_balance.py runs, show me the counts.
   If any class is under 200 images, immediately write augment_data.py for those classes.
7. After all cleaning is done, tell me the exact git commit command.
8. Tell me exactly what to fill in PROGRESS_LOG.md after each script.

Thresholds to use in clean_data.py:
- Minimum image size: 100 x 100 pixels (remove anything smaller)
- Blur threshold: Laplacian variance below 50 (remove if blurrier than this)
- Corrupt check: try to open with PIL, if it fails the image is corrupt — remove it

Start by showing me the complete clean_data.py script.
```

---

## PHASE 3 PROMPT — Data Split & Verification [LAPTOP]

```
I am continuing FasalGuard AI. I am on my LAPTOP.
Phases 0, 1, and 2 are complete. Starting Phase 3: Data Split and Verification.

Clean data is in: C:\Users\dhhdb\Desktop\fasalguard\data\processed\
38 class folders, all with 200+ images.

I need to:
1. Run split_data.py — splits each class into train (80%), val (10%), test (10%)
   Result must be:
   data\processed\train\<classname>\
   data\processed\val\<classname>\
   data\processed\test\<classname>\
2. Create training\class_names.json — a JSON file listing all 38 class names
   in the exact numbered order from FasalGuard_PRD.md (0 = apple_scab, 1 = apple_black_rot, etc.)
3. Zip the entire data\processed\ folder for transfer to the GPU system
4. Git commit

Rules:
1. Write split_data.py first. Explain every line.
2. The split must be RANDOM but REPRODUCIBLE — use random seed 42.
3. After the split, print the count per folder (train/val/test) so I can verify.
4. Then create class_names.json — show me the exact file content before I create it.
5. Tell me the exact command to zip the data folder on Windows.
6. After everything is done, tell me exactly what to fill in PROGRESS_LOG.md.
7. Tell me the exact git commit command.

After this phase, I will transfer the zip to the school GPU system.
Remind me to save the zip to a USB drive or upload to Google Drive.
```

---

## PHASE 4 PROMPT — Model Training [GPU SYSTEM]

```
I am continuing FasalGuard AI. I am now on the SCHOOL GPU SYSTEM.
This is a Windows or Linux computer with an NVIDIA GPU.
I have never trained a machine learning model before.

Phases 0–3 are complete on my laptop. I have transferred the data zip to this machine.

I need to:
1. Verify the GPU is working
2. Install Python, PyTorch with CUDA, and required libraries
3. Extract the data zip
4. Write and run the training script (EfficientNet-B0 on 38 classes)
5. Monitor training and understand the output numbers
6. Save the best model weights

Rules:
1. Start by helping me check what GPU this system has. Give me the exact command.
2. One installation step at a time — verify each one before the next.
3. Explain what each number means during training (loss, accuracy, epoch).
4. If training crashes, ask me to paste the full error before anything else.
5. Tell me what good results look like (we need validation accuracy ≥ 85%).
6. If results are below 85%, tell me exactly what to change and how to retrain.
7. After training, tell me exactly where the best model file is saved.
8. Tell me exactly what to fill in PROGRESS_LOG.md.

Training model: EfficientNet-B0 (pretrained on ImageNet, fine-tuned on our 38 classes)
The full training configuration is in FasalGuard_PRD.md under "Training Configuration".

Start by asking me to run: nvidia-smi
Then paste the output and we will go from there.
```

---

## PHASE 5 PROMPT — Model Export & Transfer [GPU SYSTEM → LAPTOP]

```
I am continuing FasalGuard AI. I am on the SCHOOL GPU SYSTEM.
Training is complete. The best model is saved as best_model.pt.
Validation accuracy achieved: [FILL IN YOUR RESULT]

I need to:
1. Export the trained model to TorchScript format so it runs on CPU
2. Test the exported model with one image on this machine
3. Transfer two files to my laptop:
   - fasalguard_model.pt (the exported model)
   - class_names.json (the 38 class names in order)
4. Test inference on my laptop CPU to confirm it works

Rules:
1. Write the export script with comments on every line.
2. After export, show me how to do a quick test inference on this machine first.
3. Tell me the exact two files I need to copy and where they go on my laptop:
   - Model goes to: app\model\fasalguard_model.pt
   - Class names go to: app\model\class_names.json
4. After I transfer and test on laptop, tell me what a successful inference output looks like.
5. Tell me the CPU inference time I should expect (should be under 10 seconds).
6. Tell me exactly what to fill in PROGRESS_LOG.md.

Start by showing me the complete export script.
```

---

## PHASE 6 PROMPT — Flask Web App [LAPTOP]

```
I am continuing FasalGuard AI. I am back on my LAPTOP.
Phases 0–5 are complete. The trained model is at app\model\fasalguard_model.pt

I need to build the Flask web application. This is a Python web app with two pages:
Page 1 (index.html): Upload a crop leaf image
Page 2 (result.html): Show the prediction, Grad-CAM heatmap, severity, and treatment

The full design spec is in FasalGuard_PRD.md under "Web App Pages".
The treatment dictionary for all 38 classes is in FasalGuard_PRD.md under "Treatment Dictionary".

Rules:
1. Build one file at a time in this exact order:
   a. app\app.py (Flask routes only, no model yet — just to confirm Flask works)
   b. app\templates\index.html
   c. app\static\style.css
   d. app\templates\result.html
2. After each file, tell me how to test that specific file before moving to the next.
3. Show me the complete file content every time — no partial code.
4. Design must use dark green (#1a5c2e) as the main colour — agriculture theme.
5. No CSS frameworks like Bootstrap — plain CSS only.
6. After all 4 files are done and tested, give me the git commit command.
7. Tell me exactly what to fill in PROGRESS_LOG.md after each file.

Start with app\app.py. Show me the complete file.
```

---

## PHASE 7 PROMPT — Model Integration & Testing [LAPTOP]

```
I am continuing FasalGuard AI. I am on my LAPTOP.
The Flask web app is built and running at http://localhost:5000
The model is at app\model\fasalguard_model.pt
The class names are at app\model\class_names.json

I now need to connect the model to the web app so uploading an image gives a real prediction.

I need these functions added to app.py:
1. Model loading (runs once when Flask starts)
2. Image preprocessing (resize, normalise to match training transforms)
3. Inference function (runs image through EfficientNet-B0, returns class + confidence)
4. Grad-CAM heatmap generation (creates heatmap image showing where model looked)
5. Severity calculation (based on confidence score — logic in FasalGuard_PRD.md)
6. Treatment lookup (use the full dictionary from FasalGuard_PRD.md)

Rules:
1. Add one function at a time. Test each before adding the next.
2. Show me the complete updated app.py after each addition — not just the new part.
3. Use pytorch-grad-cam library for Grad-CAM (install it first, verify installation).
4. After full integration, give me the 10 test images to download from Google Images
   (listed in FasalGuard_PRD.md under "Presentation & Live Demo Plan").
5. Walk me through testing each image one by one.
6. If any prediction is wrong, help me diagnose why before moving on.
7. After all 10 tests pass, give me the git commit command.
8. Tell me exactly what to fill in PROGRESS_LOG.md after each function and each test.

Start by showing me the updated app.py with just the model loading function added first.
```

---

## PHASE 8 PROMPT — Final GitHub Commit [LAPTOP]

```
I am on the final phase of FasalGuard AI. I am on my LAPTOP.
Everything is working. I need to clean up and make the final submission commit.

I need to:
1. Verify .gitignore is correct — no datasets, model weights, or pycache getting committed
2. Write a professional README.md for the GitHub repo
3. Make the final commit and push everything
4. Do a final walkthrough check for the presentation

Rules:
1. Show me the .gitignore content first — I verify before any commit.
2. Write a complete README.md that includes:
   - Project title with a one-line description
   - What it does (3-4 sentences)
   - Screenshot placeholder section
   - Step-by-step setup and run instructions (so anyone can run it)
   - List of all 38 detectable diseases
   - Tech stack
   - My name: Arif, CECOS University Peshawar
3. After final push, give me a 10-point presentation checklist.
4. Mark all phases as Complete (✅) in PROGRESS_LOG.md.
5. Final commit message: "final: readme updated, project complete"

Start by showing me the .gitignore file content.
```

---

## EMERGENCY PROMPTS

### If You Get an Error at Any Step

```
I am stuck in Phase [NUMBER] of FasalGuard AI on my [LAPTOP / GPU SYSTEM].

I was trying to: [DESCRIBE WHAT YOU WERE DOING IN ONE SENTENCE]
The last command I ran was:
[PASTE COMMAND HERE]

The error I got is:
[PASTE FULL ERROR MESSAGE HERE]

Please help me fix this error. Do not move on to anything else until it is resolved.
```

---

### If Training Accuracy Is Below 85%

```
My FasalGuard AI training finished but accuracy is too low.

Results:
- Final Validation Accuracy: [VALUE]
- Best Validation Accuracy: [VALUE]
- Number of epochs trained: [VALUE]

My class counts after cleaning were:
[PASTE THE CLASS COUNTS FROM PROGRESS_LOG.md]

Please diagnose why accuracy is low and tell me:
1. The most likely cause
2. Exactly what to change (epochs, learning rate, batch size, or data issue)
3. The exact changes to make in train.py
4. Whether I need to go back and fix data first

Do not just say "try more epochs" — give me specific numbers and reasons.
```

---

### If the Grad-CAM Heatmap Is Not Showing

```
I am in Phase 7 of FasalGuard AI. The model inference is working correctly
but the Grad-CAM heatmap is not generating properly.

The error or problem is:
[DESCRIBE OR PASTE ERROR]

My model is EfficientNet-B0, saved as TorchScript.
The library I installed is pytorch-grad-cam.

Please help me fix the heatmap generation. Show me the corrected code.
```

---

### Starting a New Chat After a Long Session

```
My previous chat got too long. I am continuing FasalGuard AI from where I left off.

I am attaching:
1. FasalGuard_PRD.md — full project plan
2. PROGRESS_LOG.md — record of everything done so far

Please read both files. Then tell me:
- Which phase we are currently on
- The last completed step
- The very next step
- Which machine I should be on

Then continue from exactly where we left off. Do not repeat anything already done.
```
