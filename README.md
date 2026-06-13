# FasalGuard AI

> AI-powered crop disease detection — upload a leaf photo, get instant diagnosis, severity rating, and treatment advice.

## What It Does

FasalGuard AI is a web application that helps farmers and agricultural students identify crop diseases from a single leaf photograph. Upload an image and the deep learning model (EfficientNet-B0) classifies it into one of 38 possible conditions across 14 crop types. The app returns the disease name, a confidence score, a severity estimate, a Grad-CAM heatmap showing where the AI focused, and a full treatment advisory including what action to take, chemical names and dosages, and prevention strategies.

## Screenshots

| Upload Page | Result Page |
|---|---|
| ![Upload](docs/screenshot_upload.png) | ![Result](docs/screenshot_result.png) |

## Tech Stack

| Component | Technology |
|---|---|
| Deep Learning Model | EfficientNet-B0 (PyTorch) |
| Heatmap Visualisation | Grad-CAM |
| Web Backend | Flask (Python) |
| Frontend | HTML5 + CSS3 |
| Dataset | PlantVillage (38 classes, 53,000+ images) |

## Setup & Run

### 1. Clone the Repository

```bash
git clone https://github.com/ThinkAboutArif/fasalguard-ai.git
cd fasalguard-ai
```

### 2. Create and Activate a Virtual Environment

**Windows:**
```bash
python -m venv fasalguard_env
fasalguard_env\Scripts\activate
```

**macOS / Linux:**
```bash
python -m venv fasalguard_env
source fasalguard_env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements_laptop.txt
```

### 4. Add the Trained Model

Place the following two files inside `app/model/`:

```
app/model/best_model.pt
app/model/class_names.json
```

### 5. Run the App

```bash
cd app
python app.py
```

### 6. Open in Browser

[http://localhost:5000](http://localhost:5000)

---

## 38 Detectable Conditions

### Apple (4)
Apple Scab · Apple Black Rot · Apple Cedar Rust · Healthy

### Blueberry (1)
Healthy

### Cherry (2)
Cherry Powdery Mildew · Healthy

### Maize / Corn (4)
Gray Leaf Spot · Common Rust · Northern Leaf Blight · Healthy

### Grape (4)
Black Rot · Esca (Black Measles) · Leaf Blight · Healthy

### Orange (1)
Citrus Greening (Huanglongbing)

### Peach (2)
Bacterial Spot · Healthy

### Pepper (2)
Bacterial Spot · Healthy

### Potato (3)
Early Blight · Late Blight · Healthy

### Raspberry (1)
Healthy

### Soybean (1)
Healthy

### Squash (1)
Powdery Mildew

### Strawberry (2)
Leaf Scorch · Healthy

### Tomato (10)
Bacterial Spot · Early Blight · Late Blight · Leaf Mold · Septoria Leaf Spot · Spider Mite · Target Spot · Mosaic Virus · Yellow Leaf Curl Virus · Healthy

---

## Model Performance

| Metric | Value |
|---|---|
| Validation Accuracy | 99.17% |
| Test Accuracy | 99.27% |
| Training Epochs | 5 |
| Dataset | PlantVillage (53,114 images) |
| Classes | 38 |

---

## Project Structure

```
fasalguard/
├── app/
│   ├── app.py
│   ├── model/
│   │   ├── best_model.pt
│   │   └── class_names.json
│   ├── templates/
│   │   ├── index.html
│   │   ├── result.html
│   │   └── about.html
│   └── static/
│       └── style.css
├── training/
│   ├── train.py
│   └── class_names.json
├── scripts/
│   ├── organise_data.py
│   ├── clean_data.py
│   ├── check_balance.py
│   └── split_data.py
├── requirements_laptop.txt
├── requirements_gpu.txt
└── README.md
```

---

## Author

**Arif**
Fourth Semester · CECOS University, Peshawar, Pakistan

## Acknowledgements

- [PlantVillage Dataset](https://github.com/spMohanty/PlantVillage-Dataset)
- [PyTorch](https://pytorch.org/)
- [Flask](https://flask.palletsprojects.com/)
- [pytorch-grad-cam](https://github.com/jacobgil/pytorch-grad-cam)