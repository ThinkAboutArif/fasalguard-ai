# app.py — FasalGuard AI Flask Web Server
# This file runs the web application on your laptop.
# It handles image uploads and displays prediction results.

# ============================================================
# STEP 1: IMPORTS
# ============================================================

# Import Flask and helper functions for building web apps
from flask import Flask, render_template, request, redirect, url_for, flash
# Import os for working with file paths
import os
# Import uuid for generating unique filenames so uploads don't overwrite each other
import uuid
# Import json for reading the class names file
import json

# --- PyTorch imports for model loading ---
# torch is the main PyTorch library for running neural networks
import torch
# nn (neural network) contains layers and loss functions
from torch import nn
# transforms for image preprocessing
from torchvision import transforms
# PIL for opening image files
from PIL import Image
# F for softmax function
import torch.nn.functional as F

# ============================================================
# STEP 2: FLASK APP SETUP
# ============================================================

# Create the Flask application instance
app = Flask(__name__)

# Secret key is used by Flask to keep session data secure.
app.secret_key = 'fasalguard-secret-key-2026'

# Define the folder where uploaded images will be stored temporarily
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

# Create the uploads folder if it doesn't already exist
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
except FileExistsError:
    pass

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed image file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Function to check if a filename has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ============================================================
# STEP 3: MODEL LOADING (runs ONCE when Flask starts)
# ============================================================

# --- Define paths to model files ---
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'fasalguard_model.pt')
CLASS_NAMES_PATH = os.path.join(BASE_DIR, 'model', 'class_names.json')

# --- Load class names from JSON ---
with open(CLASS_NAMES_PATH, 'r') as f:
    class_names = json.load(f)

NUM_CLASSES = len(class_names)

print(f"Loaded {NUM_CLASSES} class names from {CLASS_NAMES_PATH}")
print(f"First 5 classes: {class_names[:5]}")

# --- Load the TorchScript model ---
# TorchScript models are standalone — no architecture code needed
model = torch.jit.load(MODEL_PATH, map_location='cpu')
model.eval()

print(f"Model loaded successfully from {MODEL_PATH}")
print(f"Model is ready for inference on CPU.")

# --- Device configuration ---
device = torch.device('cpu')
model = model.to(device)

# --- Define image preprocessing (same as training) ---
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


# ============================================================
# STEP 4: TREATMENT DICTIONARY
# ============================================================

TREATMENTS = {
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
    "blueberry_healthy": {
        "common_name": "Healthy Blueberry",
        "action": "No action needed.",
        "chemical": "None required.",
        "prevention": "Monitor regularly. Maintain soil pH between 4.5 and 5.5 for healthy blueberries."
    },
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
    "orange_citrus_greening": {
        "common_name": "Citrus Greening (Huanglongbing)",
        "action": "No cure exists. Remove and destroy infected trees immediately to prevent spread.",
        "chemical": "Control Asian citrus psyllid vector with Imidacloprid 200SL at 0.5ml per litre.",
        "prevention": "Use certified disease-free planting material only. Install psyllid monitoring traps."
    },
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
    "raspberry_healthy": {
        "common_name": "Healthy Raspberry",
        "action": "No action needed.",
        "chemical": "None required.",
        "prevention": "Monitor weekly. Remove old canes after fruiting."
    },
    "soybean_healthy": {
        "common_name": "Healthy Soybean",
        "action": "No action needed.",
        "chemical": "None required.",
        "prevention": "Monitor weekly. Scout for pests from V3 growth stage onwards."
    },
    "squash_powdery_mildew": {
        "common_name": "Squash Powdery Mildew",
        "action": "Remove heavily infected leaves. Increase air circulation around plants.",
        "chemical": "Apply Sulphur 80WP at 2g per litre or Potassium bicarbonate at 5g per litre.",
        "prevention": "Avoid overhead watering. Space plants widely. Choose resistant varieties."
    },
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


# ============================================================
# STEP 5: ROUTES
# ============================================================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        flash('No image file selected.')
        return redirect(url_for('index'))

    file = request.files['image']

    if file.filename == '':
        flash('No image file selected.')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        unique_filename = str(uuid.uuid4()) + '_' + file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)

        # ============================================================
        # REAL INFERENCE
        # ============================================================

        # Load and preprocess the uploaded image
        image = Image.open(filepath).convert('RGB')
        input_tensor = transform(image).unsqueeze(0).to(device)

        # Run prediction
        with torch.no_grad():
            output = model(input_tensor)

        # Apply temperature scaling to fix overconfidence
        # Higher temperature = softer probabilities (more realistic confidence)
        temperature = 2.1
        scaled_output = output[0] / temperature

        # Convert to probabilities
        probabilities = F.softmax(scaled_output, dim=0)
        predicted_idx = torch.argmax(probabilities).item()
        confidence = probabilities[predicted_idx].item() * 100

        # Get predicted class name
        predicted_class = class_names[predicted_idx]

        # Determine severity
        if 'healthy' in predicted_class:
            severity = 'None'
            severity_color = 'green'
        elif confidence < 60:
            severity = 'Low'
            severity_color = 'yellow'
        elif confidence < 85:
            severity = 'Medium'
            severity_color = 'orange'
        else:
            severity = 'High'
            severity_color = 'red'

        # Look up treatment info
        treatment = TREATMENTS.get(predicted_class, {
            "common_name": predicted_class.replace('_', ' ').title(),
            "action": "No specific treatment information available.",
            "chemical": "Consult a local agricultural expert.",
            "prevention": "Monitor regularly and maintain good crop hygiene."
        })

                # Build result
        result = {
            'filename': unique_filename,
            'original_image': filepath,
            'predicted_class': predicted_class,
            'common_name': treatment['common_name'],
            'confidence': int(confidence) if confidence == int(confidence) else round(confidence, 1),
            'severity': severity,
            'severity_color': severity_color,
            'action': treatment['action'],
            'chemical': treatment['chemical'],
            'prevention': treatment['prevention'],
            'heatmap_path': None
        }

        return render_template('result.html', result=result)

    flash('Invalid file type. Please upload PNG, JPG, or JPEG.')
    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)