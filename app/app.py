# app.py — FasalGuard AI Flask Web Server
# This file runs the web application on your laptop.
# It handles image uploads and displays prediction results.

# Import Flask and helper functions for building web apps
from flask import Flask, render_template, request, redirect, url_for, flash
# Import os for working with file paths
import os
# Import uuid for generating unique filenames so uploads don't overwrite each other
import uuid

# Create the Flask application instance
app = Flask(__name__)

# Secret key is used by Flask to keep session data secure.
# For now we use a simple string. In production this should be random and hidden.
app.secret_key = 'fasalguard-secret-key-2026'

# Define the folder where uploaded images will be stored temporarily
# __file__ is the path to this app.py file. os.path.dirname gets its folder (the 'app' folder).
# Then we join it with 'uploads' to get C:\Users\dhhdb\Desktop\fasalguard\app\uploads
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

# Create the uploads folder if it doesn't already exist
# exist_ok=True means no error if folder already exists
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
except FileExistsError:
    # If a FILE named 'uploads' exists (not a folder), we handle it gracefully
    pass

# Tell Flask where the upload folder is
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed image file extensions (only these formats can be uploaded)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Function to check if a filename has an allowed extension
def allowed_file(filename):
    # Split the filename at the last dot and check the extension (lowercase)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Route: Home page — shows the image upload form
# When you visit http://localhost:5000, this function runs
@app.route('/')
def index():
    # Render and return the index.html template (the upload page)
    return render_template('index.html')


# Route: Handle image upload and show result page
# This runs when the user clicks the "Analyse" button on the upload form
@app.route('/predict', methods=['POST'])
def predict():
    # Check if the request contains a file part named 'image'
    if 'image' not in request.files:
        # If no file was selected, show an error message
        flash('No image file selected.')
        return redirect(url_for('index'))

    # Get the uploaded file from the request
    file = request.files['image']

    # Check if the user actually selected a file (not just clicked submit)
    if file.filename == '':
        flash('No image file selected.')
        return redirect(url_for('index'))

    # Check if the file has a valid extension and is not empty
    if file and allowed_file(file.filename):
        # Create a unique filename so uploads never conflict
        # uuid.uuid4() generates a random unique ID like 'a1b2c3d4...'
        unique_filename = str(uuid.uuid4()) + '_' + file.filename
        # Build the full path where the file will be saved
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        # Save the uploaded file to disk
        file.save(filepath)

        # ============================================================
        # TEMPORARY: Dummy data for testing the result page layout
        # When the real model arrives, this section will be replaced
        # with actual model inference code.
        # ============================================================
        result = {
            'filename': unique_filename,          # Name of the saved file
            'original_image': filepath,           # Path to the uploaded image
            'predicted_class': 'tomato_late_blight',  # Dummy prediction
            'common_name': 'Tomato Late Blight',     # Human-readable name
            'confidence': 94.7,                      # Dummy confidence %
            'severity': 'High',                       # Dummy severity
            'severity_color': 'red',                  # Color for badge
            'action': 'Urgent: Remove all infected plants immediately. This spreads to entire field within days.',
            'chemical': 'Apply Metalaxyl + Mancozeb (Ridomil Gold) at 2g per litre. Spray every 5 days.',
            'prevention': 'Use certified disease-free seeds. Avoid planting in wet or poorly drained areas.',
            'heatmap_path': None  # No heatmap yet — will be added in Phase 7
        }

        # Render the result page and pass the result dictionary to the template
        return render_template('result.html', result=result)

    # If the file type is not allowed, show an error
    flash('Invalid file type. Please upload PNG, JPG, or JPEG.')
    return redirect(url_for('index'))


# Route: About page (optional, for presentation)
@app.route('/about')
def about():
    return render_template('about.html')


# This block only runs when you execute this file directly (not when imported)
if __name__ == '__main__':
    # Run the Flask development server
    # debug=True means it auto-reloads when you change code
    # host='0.0.0.0' makes it accessible on your local network (for phone testing)
    app.run(debug=True, host='0.0.0.0', port=5000)