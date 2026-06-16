const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, AlignmentType, BorderStyle, WidthType, ShadingType,
  PageNumber, LevelFormat, PageBreak, UnderlineType
} = require('docx');
const fs = require('fs');

// ─── HELPERS ────────────────────────────────────────────────────────────────

const BORDER = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const BORDERS = { top: BORDER, bottom: BORDER, left: BORDER, right: BORDER };
const NO_BORDER = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const NO_BORDERS = { top: NO_BORDER, bottom: NO_BORDER, left: NO_BORDER, right: NO_BORDER };

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun({ text, bold: true, size: 36, color: "1a5c2e", font: "Arial" })],
    spacing: { before: 480, after: 200 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "1a5c2e", space: 1 } }
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    children: [new TextRun({ text, bold: true, size: 28, color: "2e5c1a", font: "Arial" })],
    spacing: { before: 360, after: 160 }
  });
}

function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    children: [new TextRun({ text, bold: true, size: 24, color: "3a3a3a", font: "Arial" })],
    spacing: { before: 280, after: 120 }
  });
}

function para(runs, opts = {}) {
  if (typeof runs === 'string') {
    runs = [new TextRun({ text: runs, size: 22, font: "Arial" })];
  }
  return new Paragraph({
    children: runs,
    spacing: { before: 80, after: 120 },
    alignment: AlignmentType.JUSTIFIED,
    ...opts
  });
}

function run(text, opts = {}) {
  return new TextRun({ text, size: 22, font: "Arial", ...opts });
}

function bold(text) {
  return new TextRun({ text, bold: true, size: 22, font: "Arial" });
}

function italic(text) {
  return new TextRun({ text, italics: true, size: 22, font: "Arial" });
}

function boldItalic(text) {
  return new TextRun({ text, bold: true, italics: true, size: 22, font: "Arial" });
}

function highlight(text) {
  return new TextRun({ text, bold: true, color: "1a5c2e", size: 22, font: "Arial" });
}

function bullet(runs, level = 0) {
  if (typeof runs === 'string') runs = [run(runs)];
  return new Paragraph({
    numbering: { reference: "bullets", level },
    children: runs,
    spacing: { before: 60, after: 80 }
  });
}

function numbered(runs, level = 0) {
  if (typeof runs === 'string') runs = [run(runs)];
  return new Paragraph({
    numbering: { reference: "numbers", level },
    children: runs,
    spacing: { before: 60, after: 80 }
  });
}

function pageBreak() {
  return new Paragraph({ children: [new PageBreak()], spacing: { before: 0, after: 0 } });
}

function spacer() {
  return new Paragraph({ children: [run("")], spacing: { before: 60, after: 60 } });
}

function infoBox(label, content) {
  const labelCell = new TableCell({
    borders: BORDERS,
    width: { size: 2200, type: WidthType.DXA },
    shading: { fill: "d5e8d4", type: ShadingType.CLEAR },
    margins: { top: 100, bottom: 100, left: 140, right: 140 },
    children: [new Paragraph({ children: [bold(label)], spacing: { before: 0, after: 0 } })]
  });
  const contentCell = new TableCell({
    borders: BORDERS,
    width: { size: 7160, type: WidthType.DXA },
    margins: { top: 100, bottom: 100, left: 140, right: 140 },
    children: [new Paragraph({ children: [run(content)], spacing: { before: 0, after: 0 } })]
  });
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [2200, 7160],
    rows: [new TableRow({ children: [labelCell, contentCell] })],
    margins: { top: 80, bottom: 80 }
  });
}

function twoColTable(rows, header1, header2, col1W = 3120, col2W = 6240) {
  const headerRow = new TableRow({
    children: [
      new TableCell({
        borders: BORDERS,
        width: { size: col1W, type: WidthType.DXA },
        shading: { fill: "1a5c2e", type: ShadingType.CLEAR },
        margins: { top: 100, bottom: 100, left: 140, right: 140 },
        children: [new Paragraph({ children: [new TextRun({ text: header1, bold: true, color: "FFFFFF", size: 20, font: "Arial" })], spacing: { before: 0, after: 0 } })]
      }),
      new TableCell({
        borders: BORDERS,
        width: { size: col2W, type: WidthType.DXA },
        shading: { fill: "1a5c2e", type: ShadingType.CLEAR },
        margins: { top: 100, bottom: 100, left: 140, right: 140 },
        children: [new Paragraph({ children: [new TextRun({ text: header2, bold: true, color: "FFFFFF", size: 20, font: "Arial" })], spacing: { before: 0, after: 0 } })]
      })
    ]
  });
  const dataRows = rows.map((r, i) => new TableRow({
    children: [
      new TableCell({
        borders: BORDERS,
        width: { size: col1W, type: WidthType.DXA },
        shading: { fill: i % 2 === 0 ? "f4faf4" : "FFFFFF", type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 140, right: 140 },
        children: [new Paragraph({ children: [bold(r[0])], spacing: { before: 0, after: 0 } })]
      }),
      new TableCell({
        borders: BORDERS,
        width: { size: col2W, type: WidthType.DXA },
        shading: { fill: i % 2 === 0 ? "f4faf4" : "FFFFFF", type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 140, right: 140 },
        children: [new Paragraph({ children: [run(r[1])], spacing: { before: 0, after: 0 } })]
      })
    ]
  }));
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [col1W, col2W],
    rows: [headerRow, ...dataRows]
  });
}

function threeColTable(rows, h1t, h2t, h3t, w1 = 2600, w2 = 3380, w3 = 3380) {
  const headerRow = new TableRow({
    children: [h1t, h2t, h3t].map((h, i) => new TableCell({
      borders: BORDERS,
      width: { size: [w1, w2, w3][i], type: WidthType.DXA },
      shading: { fill: "1a5c2e", type: ShadingType.CLEAR },
      margins: { top: 100, bottom: 100, left: 140, right: 140 },
      children: [new Paragraph({ children: [new TextRun({ text: h, bold: true, color: "FFFFFF", size: 20, font: "Arial" })], spacing: { before: 0, after: 0 } })]
    }))
  });
  const dataRows = rows.map((r, i) => new TableRow({
    children: r.map((cell, j) => new TableCell({
      borders: BORDERS,
      width: { size: [w1, w2, w3][j], type: WidthType.DXA },
      shading: { fill: i % 2 === 0 ? "f4faf4" : "FFFFFF", type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 140, right: 140 },
      children: [new Paragraph({ children: [j === 0 ? bold(cell) : run(cell)], spacing: { before: 0, after: 0 } })]
    }))
  }));
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [w1, w2, w3],
    rows: [headerRow, ...dataRows]
  });
}

function vivaBox(question, answer) {
  const qRow = new TableRow({
    children: [
      new TableCell({
        borders: BORDERS,
        width: { size: 9360, type: WidthType.DXA },
        shading: { fill: "e8f4e8", type: ShadingType.CLEAR },
        margins: { top: 120, bottom: 80, left: 160, right: 160 },
        children: [new Paragraph({ children: [bold("Q: " + question)], spacing: { before: 0, after: 0 } })]
      })
    ]
  });
  const aRow = new TableRow({
    children: [
      new TableCell({
        borders: BORDERS,
        width: { size: 9360, type: WidthType.DXA },
        margins: { top: 80, bottom: 120, left: 160, right: 160 },
        children: [new Paragraph({ children: [run("A: " + answer)], spacing: { before: 0, after: 0 }, alignment: AlignmentType.JUSTIFIED })]
      })
    ]
  });
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    rows: [qRow, aRow],
    margins: { top: 160, bottom: 160 }
  });
}

// ─── TITLE PAGE ─────────────────────────────────────────────────────────────

const titlePage = [
  spacer(), spacer(), spacer(),
  new Paragraph({
    children: [new TextRun({ text: "FasalGuard AI", bold: true, size: 64, color: "1a5c2e", font: "Arial" })],
    alignment: AlignmentType.CENTER, spacing: { before: 0, after: 200 }
  }),
  new Paragraph({
    children: [new TextRun({ text: "Technical Documentation", bold: true, size: 40, color: "2e5c1a", font: "Arial" })],
    alignment: AlignmentType.CENTER, spacing: { before: 0, after: 160 }
  }),
  new Paragraph({
    children: [new TextRun({ text: "AI-Powered Crop Disease Detection System", size: 28, color: "555555", font: "Arial", italics: true })],
    alignment: AlignmentType.CENTER, spacing: { before: 0, after: 600 }
  }),
  new Paragraph({
    children: [new TextRun({ text: "Viva Preparation Guide", bold: true, size: 28, color: "1a5c2e", font: "Arial" })],
    alignment: AlignmentType.CENTER, spacing: { before: 0, after: 200 }
  }),
  spacer(), spacer(),
  new Paragraph({
    children: [new TextRun({ text: "CECOS University, Peshawar  |  Fourth Semester", size: 22, color: "666666", font: "Arial" })],
    alignment: AlignmentType.CENTER, spacing: { before: 0, after: 100 }
  }),
  new Paragraph({
    children: [new TextRun({ text: "GitHub: https://github.com/ThinkAboutArif/fasalguard-ai", size: 22, color: "1a5c2e", font: "Arial" })],
    alignment: AlignmentType.CENTER, spacing: { before: 0, after: 100 }
  }),
  pageBreak()
];

// ─── SECTION 1: PROJECT OVERVIEW ─────────────────────────────────────────────

const section1 = [
  h1("1. Project Overview"),

  h2("1.1 What Is FasalGuard AI?"),

  para([
    bold("FasalGuard AI"), run(" (\"Fasal\" is the Urdu word for \"crop\") is an artificial intelligence-powered web application that detects crop diseases and pest damage from a single photograph of a plant leaf. A farmer, agricultural extension worker, or student simply takes a photo of a leaf they are concerned about, uploads it to the web app, and within seconds the system tells them:"),
  ]),
  bullet("Whether the crop is healthy or infected"),
  bullet("If infected: the exact disease or pest name"),
  bullet("A confidence percentage showing how sure the AI model is about its prediction"),
  bullet("A Gradient-weighted Class Activation Mapping (Grad-CAM) heatmap — a colour-coded overlay showing exactly which part of the leaf the AI \"looked at\" to make its decision"),
  bullet("A severity rating (Low, Medium, or High) based on the confidence level"),
  bullet("A specific treatment recommendation including the chemical product name, correct dosage, and prevention advice"),
  spacer(),

  h2("1.2 What Problem Does It Solve?"),

  para([
    run("Agriculture in Pakistan and many developing regions faces a critical challenge: crop diseases and pests can destroy an entire season's harvest if not identified and treated early. The traditional solution — hiring an agricultural expert to physically visit a farm and diagnose the problem — is expensive, slow, and inaccessible to small-scale farmers in rural areas."),
  ]),
  para([
    run("FasalGuard AI addresses this by putting diagnostic power directly into the hands of the farmer. Because the app runs locally on a laptop (no internet connection required during use), it works even in areas with poor or no connectivity. The system can identify "),
    bold("38 different crop conditions"), run(" across 14 crop types — a level of coverage that would take a human expert years to master."),
  ]),

  h2("1.3 Who Is It For?"),
  bullet([bold("Farmers: "), run("Diagnose diseases immediately without waiting for an expert visit")]),
  bullet([bold("Agricultural Extension Workers: "), run("Use as a field tool to quickly identify and advise on diseases")]),
  bullet([bold("Students & Researchers: "), run("A reference tool for learning about crop pathology")]),
  bullet([bold("NGOs and Aid Organisations: "), run("Deploy as a no-cost disease screening tool in remote areas")]),

  h2("1.4 Architecture Overview"),
  para([
    run("The system is built on an important architectural decision: it uses "), bold("image classification"), run(", not object detection. This distinction is crucial and is a common viva question. Classification means the model looks at the whole image and decides which one category it belongs to. Object detection (the older approach considered for this project) means drawing bounding boxes around specific regions. Classification was chosen because the PlantVillage dataset — the training dataset used — only provides images labelled with a category name, not with bounding box coordinates. Classification is the right tool for this data."),
  ]),
  pageBreak()
];

// ─── SECTION 2: TECHNOLOGY STACK ─────────────────────────────────────────────

const section2 = [
  h1("2. Full Technology Stack"),

  para([run("Every tool and library used in this project is explained below — what it is, how it works, why it was chosen, and how it was used in FasalGuard AI.")]),

  h2("2.1 Python"),
  para([
    bold("Full name: "), run("Python Programming Language. "), bold("Category: "), run("General-purpose programming language."),
  ]),
  para([
    run("Python is a high-level programming language that prioritises human-readable code. Unlike languages like C++ or Java that require you to declare variable types and manage memory manually, Python handles these details for you. This makes it far faster to write, test, and modify code. Python is the standard language for machine learning and data science because virtually every major artificial intelligence library (PyTorch, TensorFlow, scikit-learn, NumPy) is written for Python first."),
  ]),
  para([
    bold("Why used here: "), run("Python was used for all data preparation scripts, the model training code, and the Flask web application. It was also used to write the data cleaning, organisation, and splitting scripts."),
  ]),

  h2("2.2 PyTorch"),
  para([
    bold("Full name: "), run("PyTorch (developed by Meta AI Research). "), bold("Category: "), run("Deep Learning Framework."),
  ]),
  para([
    run("PyTorch is an open-source deep learning framework that lets you build and train neural networks. Think of it like a construction toolkit: it gives you all the basic building blocks (layers, loss functions, optimisers) and you assemble them into an AI model. PyTorch works by creating computational graphs — mathematical structures that represent how data flows through the model — and then using a technique called "), bold("backpropagation"), run(" to adjust the model's internal numbers (called weights or parameters) to reduce prediction errors."),
  ]),
  para([
    run("PyTorch uses "), bold("tensors"), run(" as its core data structure. A tensor is simply a multi-dimensional array of numbers. For example, a single colour image of size 224x224 pixels is stored as a tensor of shape [3, 224, 224] — three colour channels (Red, Green, Blue), each 224 pixels tall and 224 pixels wide."),
  ]),
  para([
    bold("Why used here: "), run("PyTorch is the industry standard for research and model development. It was used to load the EfficientNet-B0 model, run training, save and load model files, and perform inference (prediction) inside the Flask app."),
  ]),

  h2("2.3 Torchvision"),
  para([
    bold("Full name: "), run("Torchvision (part of the PyTorch ecosystem). "), bold("Category: "), run("Computer Vision Library for PyTorch."),
  ]),
  para([
    run("Torchvision is a companion library to PyTorch that provides pre-built tools specifically for working with images. It includes: pre-trained model architectures (EfficientNet, ResNet, VGG, etc.), image dataset loaders (like ImageFolder that automatically reads folders of images), and image transformation functions (resize, crop, flip, normalise, etc.)."),
  ]),
  para([
    bold("Why used here: "), run("Torchvision provided the EfficientNet-B0 model pre-loaded with ImageNet weights (more on this in Section 6), the ImageFolder dataset class for loading the PlantVillage images, and all the image transformation functions used during both training and inference."),
  ]),

  h2("2.4 EfficientNet-B0"),
  para([
    bold("Full name: "), run("EfficientNet Baseline-0 (developed by Google Brain in 2019). "), bold("Category: "), run("Convolutional Neural Network Architecture."),
  ]),
  para([
    run("EfficientNet-B0 is an image classification neural network architecture. The key innovation of EfficientNet is a concept called "), bold("compound scaling"), run(" — it simultaneously scales the network's depth (number of layers), width (number of neurons per layer), and image resolution in a mathematically optimal ratio. Previous networks scaled only one of these dimensions at a time, leading to inefficiency. EfficientNet achieves higher accuracy with fewer parameters (internal numbers) than older architectures, meaning it runs faster and uses less memory while being equally accurate."),
  ]),
  para([
    run("EfficientNet-B0 is the smallest version in the EfficientNet family (B0 through B7), making it ideal for deployment on CPU-only laptops because its inference time (time to produce one prediction) is under 3 seconds even without a Graphics Processing Unit (GPU). Despite its small size, it achieves over 77% accuracy on ImageNet — one of the most challenging image classification benchmarks."),
  ]),
  para([
    bold("Why used here: "), run("EfficientNet-B0 achieves 93-97% accuracy on PlantVillage, runs fast enough on CPU for live demos, and is small enough (17 MB after conversion) to distribute easily. It was the right balance between accuracy, speed, and size."),
  ]),

  h2("2.5 Transfer Learning"),
  para([
    bold("Full name: "), run("Transfer Learning (a machine learning technique). "), bold("Category: "), run("Training Strategy / AI Technique."),
  ]),
  para([
    run("Transfer learning is one of the most important concepts in modern AI. Instead of training a model from scratch — which would require millions of images and weeks of computing time — you start with a model that has already been trained on a large, general dataset, and then adapt it for your specific task."),
  ]),
  para([
    run("In this project, EfficientNet-B0 was first pre-trained on "), bold("ImageNet"), run(" — a dataset of 1.4 million images across 1,000 everyday categories (cats, dogs, cars, buildings, etc.). During this training, the model learned fundamental visual features: how to detect edges, corners, textures, colour gradients, and eventually complex shapes like \"round objects\" or \"leaf-like patterns\". These foundational skills are stored in the model's weights."),
  ]),
  para([
    run("When we apply transfer learning, we load this pre-trained model and replace only the final "), bold("classification layer"), run(" — the layer that maps learned features to a category name. Originally, this layer had 1,000 outputs (one per ImageNet class). We replace it with a new layer that has 38 outputs (one per PlantVillage disease class). We then train only this new layer (or the entire network at a lower learning rate) on our PlantVillage data. The model does not start from zero — it already \"knows\" how to see. It just needs to learn a new way to interpret what it sees."),
  ]),
  para([
    bold("Analogy: "), run("Imagine a doctor who has spent years learning to read medical scans. Transfer learning is like asking that doctor to now also read a different but related type of scan — they do not need to re-learn what tissue looks like, they just need to learn the new specific patterns to look for."),
  ]),

  h2("2.6 Flask"),
  para([
    bold("Full name: "), run("Flask Web Framework (developed by Armin Ronacher). "), bold("Category: "), run("Python Web Framework."),
  ]),
  para([
    run("Flask is a lightweight web framework written in Python. A web framework provides the basic tools you need to build a website or web application: handling incoming requests from browsers, routing requests to the right code, generating HTML responses, and serving files. Flask is called a \"micro-framework\" because it provides only the essentials, without forcing you to use a specific database system or code structure."),
  ]),
  para([
    run("When you run "), bold("python app.py"), run(", Flask starts a local web server on your computer at the address http://localhost:5000. \"localhost\" means your own computer, and 5000 is the port number (like a door number for network traffic). When you open this address in a browser, Flask receives the request and responds with the HTML page for the upload form."),
  ]),
  para([
    bold("How routes work in Flask: "), run("A route is a mapping between a URL and a Python function. For example, @app.route('/') maps the homepage URL to the function that returns the upload page HTML. @app.route('/predict', methods=['POST']) maps the form submission URL to the function that runs the AI model. Flask handles all the networking complexity so we only need to write simple Python functions."),
  ]),
  para([
    bold("Why used here: "), run("Flask is the simplest Python web framework for beginners. It needed only about 100 lines of code to create a fully working web application. Django (the other popular Python web framework) would have required many more files and configuration steps for a project this size."),
  ]),

  h2("2.7 Grad-CAM"),
  para([
    bold("Full name: "), run("Gradient-weighted Class Activation Mapping (Grad-CAM), implemented via the pytorch-grad-cam library. "), bold("Category: "), run("Explainable Artificial Intelligence (XAI) Technique."),
  ]),
  para([
    run("Grad-CAM is a technique that makes AI decisions interpretable. Deep learning models are often called \"black boxes\" because, even though they produce accurate results, it is difficult to understand why they made a particular decision. Grad-CAM solves this by creating a heatmap — a colour-coded overlay on the original image — showing which regions of the image most influenced the model's prediction."),
  ]),
  para([
    run("Here is how Grad-CAM works technically, explained simply: When the model classifies an image, the information flows forward through many layers (this is called a "), bold("forward pass"), run("). Grad-CAM then asks: for the final predicted class (say, \"tomato_late_blight\"), how strongly did each spatial location in the last convolutional layer contribute? To find this out, it computes "), bold("gradients"), run(" — the rate of change of the prediction score with respect to the activations in a target convolutional layer. Locations with high gradient values were more important for the prediction. These values are then projected back onto the original image as a heatmap. Red areas mean \"the model looked here most\", blue areas mean \"these areas were less important\"."),
  ]),
  para([
    bold("Important detail about implementation: "), run("Grad-CAM requires access to the raw internal layers of the neural network. The original TorchScript format of the model (a compiled, faster format) hides these layers. This is why the project switched back to the raw PyTorch checkpoint format (best_model.pt) for the final app — to make Grad-CAM work correctly."),
  ]),
  para([
    bold("Target layer used: "), bold("model.features[-1]"), run(" — the last convolutional feature extraction block in EfficientNet-B0. This is standard practice: the last convolutional layer captures the highest-level features (disease patterns, texture anomalies) before the final classification decision."),
  ]),
  para([
    bold("Why used here: "), run("Grad-CAM transforms the project from a simple \"black box\" detector into a transparent, explainable system. When a farmer sees the heatmap highlighting the brown lesion on their tomato leaf, they trust the system because they can see that the AI looked at the right place."),
  ]),

  h2("2.8 OpenCV"),
  para([
    bold("Full name: "), run("Open Source Computer Vision Library (OpenCV). "), bold("Category: "), run("Computer Vision Library."),
  ]),
  para([
    run("OpenCV is one of the oldest and most powerful computer vision libraries in existence, originally developed by Intel in 1999. It provides thousands of functions for processing and analysing images: reading and writing image files, converting between colour spaces, detecting blur, resizing, applying filters, and much more."),
  ]),
  para([
    bold("How blur detection was used in this project: "), run("During the data cleaning phase (Phase 2), OpenCV's Laplacian operator was used to detect and remove blurry images. The Laplacian is a mathematical filter that detects edges. A sharp image has many strong edges (high variance of the Laplacian result). A blurry image has soft, undefined edges (low variance). By setting a threshold — images with Laplacian variance below 100 were considered blurry — the cleaning script automatically removed 1,191 poor-quality images from the dataset."),
  ]),
  para([
    bold("Why used here: "), run("OpenCV is the industry standard for image processing tasks. It was the natural choice for the blur detection step during data cleaning."),
  ]),

  h2("2.9 Pillow (PIL)"),
  para([
    bold("Full name: "), run("Pillow (Python Imaging Library fork). "), bold("Category: "), run("Image Processing Library for Python."),
  ]),
  para([
    run("Pillow is Python's standard library for opening, editing, and saving image files. It supports nearly every image format including JPEG, PNG, BMP, and TIFF. When a user uploads an image to the Flask app, Pillow opens the file, converts it to RGB colour format (ensuring consistent 3-channel format regardless of whether it was uploaded as RGBA or greyscale), and prepares it for the preprocessing pipeline."),
  ]),
  para([
    bold("Why used here: "), run("Pillow integrates seamlessly with PyTorch's torchvision transforms. When torchvision's transforms.ToTensor() is called on a Pillow image, it automatically converts it to a PyTorch tensor. Pillow was also used to check minimum image sizes (100x100 pixels) during data cleaning."),
  ]),

  h2("2.10 NumPy"),
  para([
    bold("Full name: "), run("NumPy (Numerical Python). "), bold("Category: "), run("Numerical Computing Library."),
  ]),
  para([
    run("NumPy is the foundational library for numerical computing in Python. It provides the ndarray (n-dimensional array) — a fast, memory-efficient data structure for storing and manipulating large arrays of numbers. PyTorch tensors and NumPy arrays are designed to work closely together and can often be converted between each other with no data copying. NumPy was used in the Grad-CAM pipeline — the heatmap is temporarily in NumPy array format before being overlaid on the original image."),
  ]),

  h2("2.11 HTML, CSS, and JavaScript (Frontend)"),
  para([
    bold("Full names: "), run("HyperText Markup Language (HTML), Cascading Style Sheets (CSS), JavaScript. "), bold("Category: "), run("Web Frontend Technologies."),
  ]),
  para([
    run("The web interface was built using raw HTML, CSS, and JavaScript with no external frameworks (no React, no Bootstrap). HTML defines the structure and content of the page — the upload box, the buttons, the result containers. CSS defines the visual styling — the dark green colour theme (#1a5c2e), the card layouts, the confidence progress bar, the severity badge colours. JavaScript handles interactive behaviour on the results page — displaying the uploaded image preview, the colour-coded severity badge, and triggering the analysis."),
  ]),
  para([
    bold("Design theme: "), run("The app uses a warm agricultural colour palette — dark green representing crops and nature, with orange and red for severity warnings. Scalable Vector Graphics (SVG) icons are used instead of emojis to ensure consistent rendering across all operating systems and browsers."),
  ]),

  h2("2.12 Git and GitHub"),
  para([
    bold("Full names: "), run("Git (Version Control System), GitHub (Cloud Hosting Platform for Git). "), bold("Category: "), run("Version Control and Collaboration."),
  ]),
  para([
    run("Git is a version control system that tracks every change made to code files. Every time you do a "), bold("git commit"), run(", Git saves a snapshot of the project at that moment in time. This means you can always go back to a previous working version if something breaks. GitHub is a website that hosts Git repositories online, making code accessible from any computer and providing backup."),
  ]),
  para([
    bold("Why used here: "), run("The project used Git throughout to track progress across 8 phases. The .gitignore file was configured to exclude large files: the dataset (data/), model weights (*.pt), and uploaded user images (app/uploads/). This kept the repository small and fast while all actual data was stored locally."),
  ]),

  h2("2.13 TorchScript"),
  para([
    bold("Full name: "), run("TorchScript (PyTorch's model serialisation format). "), bold("Category: "), run("Model Export Format."),
  ]),
  para([
    run("TorchScript is a way to save a trained PyTorch model in a self-contained, optimised format. When a model is converted to TorchScript using "), bold("torch.jit.trace()"), run(", the model architecture and weights are compiled together into a single .pt file. This file can be loaded and run without needing the original Python training code or class definitions."),
  ]),
  para([
    bold("Important project detail: "), run("The model was initially converted to TorchScript (shrinking from 49 MB to 17 MB by removing the training state like the optimiser). However, TorchScript hides the internal layers, which made Grad-CAM impossible. The final app switched back to loading the raw checkpoint (best_model.pt) with "), bold("torch.load()"), run(" and "), bold("load_state_dict()"), run(", which allows Grad-CAM to access internal layers at the cost of a slightly larger file."),
  ]),

  pageBreak()
];

// ─── SECTION 3: DATASET ───────────────────────────────────────────────────────

const section3 = [
  h1("3. Dataset and Data Collection"),

  h2("3.1 What Dataset Was Used?"),
  para([
    run("The project used the "), bold("PlantVillage Dataset"), run(", originally created by researchers at Pennsylvania State University and available freely through Kaggle. PlantVillage is one of the most widely used agricultural disease datasets in the world. It contains over 54,000 photographs of crop leaves, captured under controlled laboratory conditions — typically with the leaf placed against a plain white or grey background to isolate the leaf from distracting environmental factors."),
  ]),

  h2("3.2 Dataset Statistics"),
  threeColTable([
    ["Total raw images", "54,305", "Before cleaning"],
    ["Total after cleaning", "53,114", "After removing 1,191 blurry images"],
    ["Number of classes", "38", "Different crop/disease combinations"],
    ["Number of crop types", "14", "Apple, Blueberry, Cherry, Maize, Grape, Orange, Peach, Pepper, Potato, Raspberry, Soybean, Squash, Strawberry, Tomato"],
    ["Image format", "JPEG / JPG", "All images are colour photographs"],
    ["Image style", "Close-up, single leaf", "Controlled background (white or plain)"],
  ], "Property", "Value", "Notes", 2400, 3480, 3480),

  spacer(),
  h2("3.3 The 38 Class Categories"),
  para([run("The dataset covers 14 crop types with a mix of healthy and diseased classes. Some crops have multiple disease classes:")]),
  twoColTable([
    ["Apple (4 classes)", "Apple Scab, Black Rot, Cedar Rust, Healthy"],
    ["Blueberry (1 class)", "Healthy only"],
    ["Cherry (2 classes)", "Healthy, Powdery Mildew"],
    ["Maize/Corn (4 classes)", "Cercospora Leaf Spot, Common Rust, Northern Leaf Blight, Healthy"],
    ["Grape (4 classes)", "Black Rot, Esca (Black Measles), Leaf Blight, Healthy"],
    ["Orange (1 class)", "Citrus Greening (Huanglongbing)"],
    ["Peach (2 classes)", "Bacterial Spot, Healthy"],
    ["Pepper (2 classes)", "Bacterial Spot, Healthy"],
    ["Potato (3 classes)", "Early Blight, Late Blight, Healthy"],
    ["Raspberry (1 class)", "Healthy only"],
    ["Soybean (1 class)", "Healthy only"],
    ["Squash (1 class)", "Powdery Mildew"],
    ["Strawberry (2 classes)", "Leaf Scorch, Healthy"],
    ["Tomato (10 classes)", "Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mite, Target Spot, Mosaic Virus, Yellow Leaf Curl Virus, Healthy"],
  ], "Crop", "Classes"),

  spacer(),
  h2("3.4 Class Imbalance"),
  para([
    run("An important characteristic of the dataset is "), bold("class imbalance"), run(" — not all classes have the same number of images. For example, orange_citrus_greening has 5,507 images while potato_healthy has only 152 images. Class imbalance can cause problems during training: the model might become biased towards predicting the majority classes more often because it sees them more frequently. However, because all 38 classes had at least 152 images and the accuracy achieved was 99.17%, this imbalance did not significantly hurt performance in this project. The smallest class (potato_healthy with 152 images) was flagged as below the desired minimum of 200 images but was retained as-is."),
  ]),

  pageBreak()
];

// ─── SECTION 4: DATA PREPROCESSING ──────────────────────────────────────────

const section4 = [
  h1("4. Data Preprocessing Pipeline"),

  para([run("Data preprocessing is the process of transforming raw, unstructured data into a clean, organised form that a machine learning model can learn from. This project had four distinct preprocessing phases, each with a dedicated Python script.")]),

  h2("4.1 Phase 1 — Dataset Organisation (organise_data.py)"),
  para([
    run("The raw PlantVillage dataset came with folder names like "), bold("Tomato___Late_blight"), run(" and "), bold("Corn_(maize)___Common_rust_"), run(". These are inconsistent in formatting and difficult to use in code. The "), bold("organise_data.py"), run(" script renamed all 38 folders to clean, consistent lowercase names with underscores, such as "), bold("tomato_late_blight"), run(" and "), bold("maize_common_rust"), run(". These renamed folders were created in a new "), bold("data/processed/"), run(" directory, and images were copied (not moved) from the raw folder, preserving the original data."),
  ]),
  para([
    bold("Why this matters: "), run("Consistent folder names serve as the class labels for training. The training code reads folder names and uses them as the ground truth category for every image inside that folder."),
  ]),

  h2("4.2 Phase 2 — Data Cleaning (clean_data.py)"),
  para([
    run("Not every image in a dataset is usable. Poor-quality images can confuse the model during training, causing it to learn wrong patterns. The "), bold("clean_data.py"), run(" script checked every one of the 54,305 images for three types of problems:"),
  ]),
  numbered([bold("Corrupt images: "), run("Images that could not be opened at all. These were detected by attempting to open each file with Pillow and catching any exceptions. Result: 0 corrupt images found.")]),
  numbered([bold("Undersized images: "), run("Images smaller than 100x100 pixels. Images this small contain insufficient detail for the model to learn meaningful features. These were detected by checking the image dimensions with Pillow. Result: 0 undersized images found.")]),
  numbered([bold("Blurry images: "), run("Images that are out of focus and lack sharp edges. These were detected using OpenCV's Laplacian variance method — computing the variance of the Laplacian operator applied to the image. A threshold of 100 was used (variance below 100 = blurry). Result: 1,191 blurry images detected and removed. The highest rejection counts were in orange_citrus_greening (596 removed) and tomato_yellow_leaf_curl (413 removed).")]),
  para([
    bold("Safe removal: "), run("Rejected images were moved to a "), bold("data/rejected/"), run(" folder rather than permanently deleted. This preserves the ability to review or recover images later if the threshold needs adjusting."),
  ]),
  para([
    bold("Final clean dataset: "), run("53,114 images — a rejection rate of only 2.19%, meaning the dataset was already very high quality."),
  ]),

  h2("4.3 Phase 3 — Data Splitting (split_data.py)"),
  para([
    run("Before training, the dataset must be split into three separate, non-overlapping subsets: training, validation, and test. It is critical that the model never sees the validation or test images during training, because we need these held-out sets to measure how well the model generalises to "), bold("new, unseen data"), run("."),
  ]),
  threeColTable([
    ["Training Set", "42,474 images (80%)", "What the model learns from. The model sees these images during training and adjusts its weights based on them."],
    ["Validation Set", "5,297 images (10%)", "Used after each epoch to measure accuracy on data the model has never seen. Used to monitor for overfitting and to select the best model checkpoint."],
    ["Test Set", "5,343 images (10%)", "Used only once, after training is fully complete, to measure final real-world performance. Never used during training."],
  ], "Split", "Size", "Purpose", 2000, 2680, 4680),

  spacer(),
  para([
    bold("Random seed 42: "), run("The split was performed with a random seed of 42. A random seed is a starting point for the random number generator, ensuring that the split is reproducible — if you run the script again, you get the exact same images in each split. This is important for scientific reproducibility."),
  ]),
  para([
    bold("Stratified split: "), run("The split was performed class-by-class, ensuring each of the 38 classes is proportionally represented in all three splits. Without stratification, a random split could accidentally put all images of one rare class into the training set, leaving nothing for validation."),
  ]),

  h2("4.4 class_names.json"),
  para([
    run("After the split, a "), bold("class_names.json"), run(" file was created listing all 38 class names in the exact order they correspond to model outputs. This file is critical: when the model outputs a number (say, 31), the app must look up what class that number corresponds to (\"tomato_late_blight\"). Without this mapping file, the model output would be meaningless."),
  ]),

  pageBreak()
];

// ─── SECTION 5: DATA AUGMENTATION ────────────────────────────────────────────

const section5 = [
  h1("5. Data Augmentation"),

  para([
    bold("Data augmentation"), run(" is the practice of applying random transformations to training images to create artificially varied versions of the data. The model sees a slightly different version of each image on every epoch, which helps it learn to recognise diseases under various real-world conditions: different lighting, different angles, different positions on the leaf."),
  ]),
  para([
    run("Augmentation only applies to the "), bold("training set"), run(". The validation and test sets are never augmented — they always receive only basic resizing and normalisation. This is because augmentation is a training tool to build robustness, not a preprocessing step that should change what we are evaluating against."),
  ]),

  h2("5.1 Resize to 224x224"),
  para([
    bold("What it does: "), run("Every image, regardless of its original dimensions, is scaled to exactly 224 by 224 pixels."),
  ]),
  para([
    bold("Why: "), run("EfficientNet-B0 has a fixed input size of 224x224. All images must be exactly this size for the model to process them. Without this step, the model would receive images of different sizes and could not process them in batches."),
  ]),

  h2("5.2 Random Horizontal Flip"),
  para([
    bold("What it does: "), run("With 50% probability, the image is mirrored left-to-right. A leaf facing left becomes a leaf facing right."),
  ]),
  para([
    bold("Why: "), run("A disease does not care which side of a leaf it is on. If the model has only seen disease spots on the right side of leaves during training, it might fail to recognise spots on the left side during deployment. Horizontal flipping ensures the model learns that disease patterns are position-independent."),
  ]),

  h2("5.3 Random Rotation (up to ±15 degrees)"),
  para([
    bold("What it does: "), run("The image is rotated by a random angle between -15 and +15 degrees."),
  ]),
  para([
    bold("Why: "), run("Farmers take photos of leaves at whatever angle is convenient. A leaf photographed at a slight tilt should still be diagnosed correctly. Rotation augmentation teaches the model to be invariant to small rotational changes."),
  ]),

  h2("5.4 Color Jitter"),
  para([
    bold("What it does: "), run("Randomly adjusts the image's brightness, contrast, and saturation by up to ±20% each (factor of 0.2). For example, a bright, sunny photo and a cloudy, dim photo of the same diseased leaf should both give the same diagnosis."),
  ]),
  para([
    bold("Why: "), run("Real-world photos are taken under wildly different lighting conditions. A phone photo in afternoon sunlight looks very different from a photo taken in shade. Color jitter teaches the model that disease patterns are defined by their shape and texture, not by their absolute colour values under a specific lighting condition."),
  ]),

  h2("5.5 ToTensor"),
  para([
    bold("What it does: "), run("Converts the image from a Pillow image object (with pixel values in the range 0-255) to a PyTorch tensor with values in the range 0.0 to 1.0. Also rearranges the dimensions from height x width x channels (H, W, C) to channels x height x width (C, H, W), which is the format PyTorch expects."),
  ]),
  para([
    bold("Why: "), run("PyTorch models only accept PyTorch tensors as input, not raw image files."),
  ]),

  h2("5.6 Normalisation"),
  para([
    bold("What it does: "), run("Adjusts the pixel values of each colour channel using the formula: (pixel_value - mean) / standard_deviation. The values used are: Mean = [0.485, 0.456, 0.406] and Standard Deviation = [0.229, 0.224, 0.225] for the Red, Green, and Blue channels respectively."),
  ]),
  para([
    bold("Why: "), run("These specific mean and standard deviation values are the statistics of the ImageNet dataset — the dataset that EfficientNet-B0 was pre-trained on. By normalising with the same values, we ensure that our crop leaf images \"look\" like ImageNet images to the pre-trained layers. If we did not normalise, the pre-trained weights would not work well because the input distribution would be different from what those weights were trained on. Think of it like calibrating a measuring instrument — without calibration (normalisation), your measurements (model weights) give wrong results."),
  ]),

  pageBreak()
];

// ─── SECTION 6: MODEL ARCHITECTURE ───────────────────────────────────────────

const section6 = [
  h1("6. Model Architecture"),

  h2("6.1 What Is a Convolutional Neural Network?"),
  para([
    run("A "), bold("Convolutional Neural Network (CNN)"), run(" is a type of deep learning model designed specifically for processing grid-structured data like images. To understand it, we first need to understand why regular (fully-connected) neural networks do not work well for images."),
  ]),
  para([
    run("A 224x224 colour image has 224 × 224 × 3 = 150,528 individual pixel values. If you fed these directly into a standard neural network, the first layer alone would need millions of connections, making the network enormous, slow to train, and prone to overfitting. Worse, such a network would have no built-in understanding that pixels near each other are related (spatial structure) — it treats each pixel as completely independent."),
  ]),
  para([
    run("Convolutional Neural Networks solve this by using "), bold("convolutional filters"), run(" (also called kernels). A filter is a small grid of numbers (typically 3x3 or 5x5) that slides across the entire image. At each position, it computes the dot product between its values and the image pixels underneath it. This operation detects a specific pattern — a horizontal edge, a diagonal, a colour transition. A single convolutional layer contains dozens to hundreds of such filters, each detecting a different feature. The output of one convolutional layer becomes the input to the next, and deeper layers combine simple features into complex ones: edges → shapes → textures → complex disease patterns."),
  ]),

  h2("6.2 EfficientNet-B0 Internal Structure"),
  para([
    run("EfficientNet-B0 consists of the following major components:"),
  ]),
  numbered([bold("Stem Layer: "), run("A single convolutional layer that converts the 224x224x3 input image into a 112x112 feature map with 32 channels. Think of this as the first stage of feature detection — extracting basic edge information from the raw pixels.")]),
  numbered([bold("Mobile Inverted Bottleneck Blocks (MBConv): "), run("The core building blocks of EfficientNet. There are 7 stages of MBConv blocks (16 total layers). Each MBConv block uses a technique called Depthwise Separable Convolution, which separates the convolution operation into two cheaper steps: a depthwise convolution (applying one filter per channel) and a pointwise convolution (combining channels). This achieves similar accuracy to regular convolution using far fewer calculations.")]),
  numbered([bold("Squeeze-and-Excitation (SE) Blocks: "), run("A lightweight attention mechanism inside each MBConv block. It learns to emphasise informative feature channels and suppress less useful ones. For example, when detecting a rust disease, certain colour channels and texture features are more diagnostic than others — SE blocks help the network focus on those.")]),
  numbered([bold("Global Average Pooling Layer: "), run("After the final convolutional stage, a 7x7 spatial feature map is reduced to a single 1280-dimensional vector by averaging across all spatial positions. This converts the spatial feature map into a compact feature descriptor for the whole image.")]),
  numbered([bold("Classifier (Fully Connected Layer): "), run("The original EfficientNet-B0 has a final linear layer that maps 1280 features to 1000 outputs (ImageNet classes). In FasalGuard AI, this layer was replaced with a new linear layer mapping 1280 features to 38 outputs — one per PlantVillage disease class. This single layer replacement is the core change made for transfer learning.")]),

  h2("6.3 How the Model Makes a Prediction"),
  para([
    run("Here is the complete prediction process step by step, for a single uploaded image:"),
  ]),
  numbered("The user uploads an image file (JPEG or PNG)"),
  numbered("Flask receives the file and saves it temporarily to the app/uploads/ folder"),
  numbered("Pillow opens the file and converts it to RGB format (3 colour channels)"),
  numbered("Torchvision transforms resize the image to 224x224 pixels, convert it to a tensor, and normalise it with ImageNet statistics"),
  numbered("The image tensor has dimensions added to become shape [1, 3, 224, 224] — batch size of 1, 3 channels, 224x224 pixels"),
  numbered("The tensor is passed through EfficientNet-B0's layers in sequence (forward pass)"),
  numbered("The final layer produces 38 numbers — called logits (raw, unnormalised scores)"),
  numbered("A Softmax function converts these 38 logits into 38 probabilities that all add up to 1.0 (100%). For example: [0.001, 0.003, 0.99, 0.002, ...]"),
  numbered("The class with the highest probability becomes the predicted class"),
  numbered("The highest probability value becomes the confidence percentage"),
  numbered("The predicted class name is used to look up treatment information in the TREATMENTS dictionary"),

  h2("6.4 What Is Softmax?"),
  para([
    bold("Softmax"), run(" is a mathematical function that converts a vector of any real numbers (logits) into a probability distribution. Given 38 raw output scores from the model, Softmax exponentiates each score (making all values positive) and then divides by the sum of all exponentiated values. This guarantees that all 38 output values lie between 0.0 and 1.0 and sum to exactly 1.0 (100%)."),
  ]),
  para([
    run("For example, if the model predicts "), bold("tomato_late_blight"), run(" with a logit of 8.0, and all other classes have logits around 2.0, Softmax turns this into a probability of 0.99 (99% confidence) for late blight, with the remaining 1% split among the other 37 classes. This makes the outputs intuitive and directly usable as a confidence score. The class with the highest probability is selected as the prediction, and the probability value is displayed as the confidence percentage."),
  ]),
  pageBreak()
];

// ─── SECTION 7: MODEL TRAINING & HYPERPARAMETERS ─────────────────────────────

const section7 = [
  h1("7. Model Training & Hyperparameters"),
  para([
    run("Model training is the process where the neural network adjusts its weights based on feedback from its predictions, iteratively reducing errors. In this project, training was performed using transfer learning, fine-tuning a pre-trained EfficientNet-B0 model on the custom PlantVillage dataset.")
  ]),
  h2("7.1 Training Configuration"),
  para([
    run("The following hyperparameters and settings were used to train FasalGuard AI on the school GPU computer:")
  ]),
  threeColTable([
    ["Hyperparameter", "Value", "Explanation"],
    ["Epochs", "20", "The number of complete passes through the entire training dataset. 20 epochs were chosen to allow the model to converge without overfitting."],
    ["Batch Size", "32", "The number of images processed at once before updating the model weights. Set to 32, but can be reduced to 16 if the GPU runs out of memory (OOM)."],
    ["Learning Rate", "0.001", "Controls how much the model weights are adjusted in response to the estimated error each time. A rate of 0.001 is a standard starting point for the Adam optimizer."],
    ["Image Size", "224 x 224", "Standard input resolution required by EfficientNet-B0. All images are resized to this dimension during preprocessing."],
    ["Optimizer", "Adam", "Adaptive Moment Estimation. It dynamically adjusts the learning rate for each parameter, leading to faster and more stable training."],
    ["Loss Function", "Cross-Entropy Loss", "Standard loss function used for multi-class classification. It measures the difference between the predicted probability distribution and the true one-hot encoded label."]
  ], "Parameter", "Value", "Explanation", 2000, 2680, 4680),
  spacer(),
  h2("7.2 Training Process"),
  para([
    run("During each epoch, the model performs a "), bold("forward pass"), run(" on a batch of 32 augmented training images, calculates the loss (error) using Cross-Entropy Loss, and performs a "), bold("backward pass (backpropagation)"), run(" to compute gradients. The Adam optimizer then updates the weights of the classification layer (and fine-tunes the feature extraction layers) to reduce the loss. After each epoch, the model is evaluated on the validation set to measure accuracy and loss without updating weights. The checkpoint with the highest validation accuracy is saved as "), bold("best_model.pt"), run(".")
  ]),
  h2("7.3 Expected and Achieved Results"),
  para([
    run("The training achieves high accuracy very quickly due to transfer learning, since the model's feature extraction layers were already pre-trained on ImageNet:")
  ]),
  threeColTable([
    ["Metric", "Value / Target", "Notes"],
    ["Validation Accuracy", "93% – 97%+", "Excellent performance on the PlantVillage dataset."],
    ["Training Time", "~20 minutes", "On a school computer equipped with a standard NVIDIA GPU."],
    ["Inference Time (CPU)", "< 3 seconds", "On a standard personal laptop, enabling real-time offline diagnostics during presentation."]
  ], "Metric", "Value / Target", "Notes", 2400, 3480, 3480),
  pageBreak()
];

// ─── SECTION 8: GRAD-CAM AND EXPLAINABILITY ──────────────────────────────────

const section8 = [
  h1("8. Grad-CAM and Explainability"),
  h2("8.1 What is Explainable AI (XAI)?"),
  para([
    run("Deep learning models are often criticised as \"black boxes\" because it is difficult to see how they arrive at a decision. In agricultural applications, if a model predicts that a leaf has late blight, a farmer needs to know why. Explainable AI (XAI) refers to techniques that make machine learning models transparent and understandable to humans.")
  ]),
  h2("8.2 Grad-CAM Technical Explanation"),
  para([
    bold("Gradient-weighted Class Activation Mapping (Grad-CAM)"), run(" is an explainability technique that generates a visual heatmap showing which parts of an input image most influenced the model's prediction. It works by looking at the last convolutional layer (in this project, "), bold("model.features[-1]"), run("). The last convolutional layer contains the richest spatial and semantic information about the image (shapes, lesions, rust spots).")
  ]),
  para([
    run("Grad-CAM calculates the gradients of the score for the predicted class with respect to the feature map activations of this last layer. These gradients represent how important each feature map is to the final decision. By taking a weighted combination of the feature maps based on these gradients, Grad-CAM produces a 2D activation map. This map is then resized to the original image dimensions and overlaid as a heatmap.")
  ]),
  h2("8.3 Grad-CAM Implementation Details"),
  para([
    run("The heatmap uses a standard jet colour map (blue to red):")
  ]),
  bullet([bold("Red regions: "), run("High importance. These are the specific areas (e.g., a spot, lesion, or discoloured margin) that the model focused on to make its prediction.")]),
  bullet([bold("Blue/Green regions: "), run("Low importance. The model ignored these areas (such as the background or healthy portions of the leaf).")]),
  para([
    run("This visual output is shown side-by-side with the original image on the web app's results page, allowing farmers to verify that the AI is indeed looking at the disease symptoms and not at background noise.")
  ], { spacing: { before: 120, after: 120 } }),
  pageBreak()
];

// ─── SECTION 9: WEB APPLICATION & SYSTEM LOGIC ───────────────────────────────

const section9 = [
  h1("9. Web Application & System Logic"),
  h2("9.1 Flask Web Server"),
  para([
    run("The frontend web interface communicates with a backend written in Python using Flask. Flask acts as the orchestrator: it serves the HTML pages, handles file uploads, runs the PyTorch model on the uploaded image, generates the Grad-CAM heatmap, and sends the results back to the user.")
  ]),
  para([
    bold("Flask Backend Routes:")
  ]),
  bullet([bold("GET '/' : "), run("Serves the homepage (index.html) containing the file upload form.")]),
  bullet([bold("POST '/predict' : "), run("Receives the uploaded image, validates it (checks format and size), passes it through the preprocessing pipeline, runs inference using PyTorch, calls the Grad-CAM library to generate the heatmap, and renders the results page (result.html) with the prediction, confidence, severity, and treatments.")]),
  h2("9.2 Severity Calculation Logic"),
  para([
    run("Because the dataset does not have bounding boxes, we cannot count lesions. Instead, we use the model's confidence percentage as a proxy for disease severity. If the model is extremely confident, the symptoms are likely distinct and well-developed (high severity). If confidence is lower, the disease may be in its early stages (low severity). Healthy crops are marked as 'None'.")
  ]),
  twoColTable([
    ["Confidence Score", "Severity Level", "Action Recommendation"],
    ["Below 60%", "Low", "Early stage. Monitor closely. Apply preventive measures."],
    ["60% – 85%", "Medium", "Disease established. Action recommended soon to prevent spread."],
    ["Above 85%", "High", "Severe infection. Immediate chemical or physical intervention required."],
    ["Any 'healthy' class", "None", "Crop is healthy. No action required. Continue weekly monitoring."]
  ], "Confidence Range", "Severity & Action", 3120, 6240),
  spacer(),
  h2("9.3 Treatment Dictionary Mapping"),
  para([
    run("Once a prediction is made (e.g. 'tomato_late_blight'), the server looks up the corresponding entry in the TREATMENTS dictionary. This dictionary contains four key fields: Common Name, Action (physical/cultural steps), Chemical Treatment (specific product name and dosage), and Prevention (long-term advice). This details-rich response ensures the farmer gets actionable guidance immediately.")
  ]),
  pageBreak()
];

// ─── SECTION 10: PRESENTATION & LIVE DEMO PLAN ───────────────────────────────

const section10 = [
  h1("10. Presentation & Live Demo Plan"),
  h2("10.1 Curated Demo Test Images"),
  para([
    run("To ensure a smooth presentation, a folder named demo_images/ has been prepared with 10 test images downloaded from Google. These images represent close-ups of single leaves with plain backgrounds to match the model's training distribution:")
  ]),
  threeColTable([
    ["Image #", "Search Term", "Expected Prediction"],
    ["Image 1", "tomato late blight leaf close up", "tomato_late_blight"],
    ["Image 2", "tomato healthy green leaf", "tomato_healthy"],
    ["Image 3", "maize common rust orange pustules", "maize_common_rust"],
    ["Image 4", "potato late blight dark spots", "potato_late_blight"],
    ["Image 5", "apple scab lesions leaf", "apple_scab"],
    ["Image 6", "tomato yellow leaf curl virus", "tomato_yellow_leaf_curl"],
    ["Image 7", "pepper bacterial spot leaf", "pepper_bacterial_spot"],
    ["Image 8", "grape black rot leaf", "grape_black_rot"],
    ["Image 9", "tomato spider mite damage", "tomato_spider_mite"],
    ["Image 10", "corn northern leaf blight", "maize_northern_blight"]
  ], "Image", "Google Search Query", "Expected Output", 1500, 4860, 3000),
  spacer(),
  h2("10.2 Live Demo Script"),
  numbered([bold("Step 1: "), run("Open the web browser and navigate to http://localhost:5000. Point out the clean user interface, the green agricultural styling, and explain that the server is running locally on the laptop with no internet connection required.")]),
  numbered([bold("Step 2: "), run("Upload demo Image 2 (healthy tomato leaf). Show that the model predicts 'healthy' with high confidence. Show the green severity badge and explain that no treatment is needed.")]),
  numbered([bold("Step 3: "), run("Upload demo Image 1 (tomato late blight). Show the red severity badge, the detailed treatment recommendations, and the Grad-CAM heatmap highlighting the dark spots. Explain: 'The red area shows exactly where the AI looked to identify the late blight.'")]),
  numbered([bold("Step 4: "), run("Upload demo Image 3 (maize common rust) to demonstrate that the model works across different crop types (maize, tomato, potato, apple, etc.).")]),
  h2("10.3 Backup Plan"),
  para([
    run("In case of technical issues during the live presentation, the following backup plan is prepared:")
  ]),
  bullet([bold("Flask server fails: "), run("Press Ctrl+C in the terminal and run 'python app.py' to restart it.")]),
  bullet([bold("Wrong predictions: "), run("Explain that the model is trained on PlantVillage (plain backgrounds). If an image has complex backgrounds (e.g., weeds, soil, hands), explain that background noise can confuse the model, and building real-world robustness is a key area for future improvement (e.g., using leaf segmentation).")]),
  bullet([bold("Pre-saved screenshots: "), run("Keep 3 screenshots of successful predictions open on the desktop to show the examiners in case the server cannot run at all.")]),
  pageBreak()
];

// ─── SECTION 11: VIVA PREPARATION Q&A ────────────────────────────────────────

const section11 = [
  h1("11. Viva Preparation Q&A"),
  para([
    run("This section contains a list of critical questions that examiners are likely to ask during the Viva exam, along with their precise, technically accurate answers.")
  ]),
  vivaBox(
    "Why did you use image classification instead of object detection?",
    "We used image classification because the PlantVillage training dataset only provides images labelled with a category name (e.g., tomato_late_blight), not with bounding box coordinates. Image classification identifies the category of the entire leaf, which is exactly what our dataset supports and is highly effective for this task. Object detection would require manual bounding box labeling of over 50,000 images, which is extremely time-consuming."
  ),
  vivaBox(
    "What is transfer learning, and why did you use it?",
    "Transfer learning is a machine learning technique where a model trained on a large dataset (like ImageNet with 1.4 million images) is adapted for a new, specific task (like crop disease classification). We used it because training a deep learning model from scratch requires massive computing resources and millions of images. EfficientNet-B0 already knows how to detect basic features like edges, textures, and shapes from ImageNet. We only replace the final classification layer and fine-tune it on our 53,114 PlantVillage images, achieving over 95% accuracy in just 20 minutes of training."
  ),
  vivaBox(
    "What is the difference between the training, validation, and test sets?",
    "The training set (80%) is used by the model to learn and adjust its weights. The validation set (10%) is evaluated after each epoch to monitor performance on unseen data and detect overfitting (when a model performs well on training data but poorly on validation data). The test set (10%) is kept completely hidden and used only once, after training is fully completed, to measure the model's final real-world generalization accuracy."
  ),
  vivaBox(
    "How does Grad-CAM work, and why did you use it?",
    "Grad-CAM (Gradient-weighted Class Activation Mapping) is an explainability technique. It takes the gradients of the predicted class score with respect to the feature map activations of the last convolutional layer (model.features[-1]). It calculates a weighted average of these feature maps to create a 2D activation map, showing which regions of the image most influenced the prediction. We overlay this map on the original leaf image as a heatmap. We used it to make our model transparent, allowing farmers to verify that the AI is looking at the actual disease symptoms and not at the background."
  ),
  vivaBox(
    "Why did you choose EfficientNet-B0 over other models like ResNet or VGG?",
    "EfficientNet-B0 uses 'compound scaling' to scale depth, width, and resolution in a balanced way, making it highly accurate but extremely lightweight. It has only 5.3 million parameters, compared to ResNet-50 (25 million) or VGG-16 (138 million). This small size (17 MB file size after training) allows FasalGuard AI to perform inference on a standard CPU-only laptop in under 3 seconds, making it ideal for rural deployment without expensive GPUs."
  ),
  vivaBox(
    "Why did you normalise the images using the specific mean [0.485, 0.456, 0.406]?",
    "These are the mean and standard deviation values of the ImageNet dataset, which our EfficientNet-B0 model was pre-trained on. By normalising our input crop leaf images with these exact values, we ensure that their pixel value distribution matches the distribution the model saw during pre-training. If we did not normalise, the pre-trained weights would receive data in a different range, leading to poor feature extraction and very low accuracy."
  ),
  vivaBox(
    "Why did you apply data augmentation only to the training set and not the validation/test sets?",
    "Data augmentation (flips, rotations, colour jitter) is a training technique to expose the model to variations in lighting, angle, and position, which builds robustness and prevents overfitting. We do not augment the validation and test sets because they must represent clean, standard, real-world evaluation points. Augmenting them would introduce random variations into our evaluation metrics, making it harder to measure the model's true accuracy on standard test images."
  )
];

// ─── DOCUMENT CREATION & SAVING ─────────────────────────────────────────────

const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [
          { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT },
          { level: 1, format: LevelFormat.BULLET, text: "○", alignment: AlignmentType.LEFT },
        ]
      },
      {
        reference: "numbers",
        levels: [
          { level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT },
          { level: 1, format: LevelFormat.DECIMAL, text: "%2.", alignment: AlignmentType.LEFT },
        ]
      }
    ]
  },
  sections: [
    {
      properties: {},
      children: [
        ...titlePage,
        ...section1,
        ...section2,
        ...section3,
        ...section4,
        ...section5,
        ...section6,
        ...section7,
        ...section8,
        ...section9,
        ...section10,
        ...section11
      ]
    }
  ]
});

Packer.toBuffer(doc).then((buffer) => {
  const outputPath = 'C:\\Users\\dhhdb\\Desktop\\fasalguard\\docs\\FasalGuard_Technical_Documentation.docx';
  
  // Create docs directory if it doesn't exist
  const dir = 'C:\\Users\\dhhdb\\Desktop\\fasalguard\\docs';
  if (!fs.existsSync(dir)){
    fs.mkdirSync(dir, { recursive: true });
  }

  fs.writeFileSync(outputPath, buffer);
  console.log('Document created successfully at:', outputPath);
}).catch((err) => {
  console.error('Error generating document:', err);
});
