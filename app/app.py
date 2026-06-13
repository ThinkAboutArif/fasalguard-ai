# app.py — FasalGuard AI Flask Web Server
# This file runs the web application on your laptop.
# It handles image uploads and displays prediction results.

# ============================================================
# STEP 1: IMPORTS
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, flash
import os
import uuid
import json
import torch
from torch import nn
from torchvision import transforms
import torchvision.models as models
from PIL import Image
import torch.nn.functional as F
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image
import numpy as np


# ============================================================
# STEP 2: FLASK APP SETUP
# ============================================================

app = Flask(__name__)
app.secret_key = 'fasalguard-secret-key-2026'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')

try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
except FileExistsError:
    pass

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ============================================================
# STEP 3: MODEL LOADING (runs ONCE when Flask starts)
# ============================================================

CHECKPOINT_PATH = os.path.join(BASE_DIR, 'model', 'best_model.pt')
CLASS_NAMES_PATH = os.path.join(BASE_DIR, 'model', 'class_names.json')

with open(CLASS_NAMES_PATH, 'r') as f:
    class_names = json.load(f)

NUM_CLASSES = len(class_names)

print(f"Loaded {NUM_CLASSES} class names from {CLASS_NAMES_PATH}")
print(f"First 5 classes: {class_names[:5]}")

print("[MODEL] Building EfficientNet-B0 architecture...")
model = models.efficientnet_b0(weights=None)
model.classifier[1] = nn.Linear(model.classifier[1].in_features, NUM_CLASSES)

print(f"[MODEL] Loading checkpoint from {CHECKPOINT_PATH}...")
checkpoint = torch.load(CHECKPOINT_PATH, map_location='cpu')
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

print(f"[MODEL] Model loaded successfully!")
print(f"[MODEL] Best validation accuracy from training: {checkpoint.get('val_acc', 'N/A')}%")
print(f"[MODEL] Model is ready for inference on CPU.")

device = torch.device('cpu')
model = model.to(device)

print("[MODEL] Finding target layer for Grad-CAM...")
target_layer_name = None
target_layer_module = None
for name, module in model.named_modules():
    if isinstance(module, nn.Conv2d):
        target_layer_name = name
        target_layer_module = module

if target_layer_module:
    print(f"[MODEL] Grad-CAM target layer: {target_layer_name}")
else:
    print("[MODEL] WARNING: No Conv2d layer found for Grad-CAM!")

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


# ============================================================
# STEP 4: GRAD-CAM HEATMAP FUNCTION
# ============================================================

def generate_heatmap(image_path, predicted_idx, output_path):
    try:
        pil_image = Image.open(image_path).convert('RGB').resize((224, 224))
        rgb_img = np.array(pil_image) / 255.0
        input_tensor = transform(pil_image).unsqueeze(0).to(device)

        if target_layer_module is None:
            print("WARNING: No target layer available for Grad-CAM")
            return False

        cam = GradCAM(model=model, target_layers=[target_layer_module])
        targets = [ClassifierOutputTarget(predicted_idx)]
        grayscale_cam = cam(input_tensor=input_tensor, targets=targets)
        grayscale_cam = grayscale_cam[0, :]
        visualization = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True)
        heatmap_pil = Image.fromarray((visualization * 255).astype(np.uint8))
        heatmap_pil.save(output_path)
        return True

    except Exception as e:
        print(f"Grad-CAM generation failed: {e}")
        return False


# ============================================================
# STEP 5: TREATMENT DICTIONARY
# ============================================================

TREATMENTS = {

    # ── APPLE ──────────────────────────────────────────────────────────────────

    "apple_scab": {
        "common_name": "Apple Scab",
        "pathogen": "Fungal disease caused by Venturia inaequalis. One of the most economically damaging apple diseases worldwide.",
        "symptoms": "Olive-green to brown velvety lesions on leaves, often with a faint yellow border. On fruit, lesions turn dark, corky, and cracked. Severely infected leaves curl and drop early.",
        "spread": "Spreads rapidly via spores released during rain. A single infected leaf can release millions of spores. Most dangerous during cool, wet spring weather (10–21°C).",
        "action": "Immediately rake and destroy all fallen leaves — they harbour spores that survive winter. Remove and bag infected fruit. Do not compost. Prune to open the canopy so leaves dry faster after rain.",
        "chemical": "Apply Captan 50WP at 2g per litre of water. Begin spraying at green tip stage in spring, repeat every 7–10 days during wet weather. Switch to Myclobutanil 20EW at 1ml per litre if infection is already visible.",
        "prevention": "Plant scab-resistant varieties (e.g. Liberty, Redfree, Enterprise). Apply a dormant copper spray before buds open each spring. Maintain wide spacing between trees for airflow.",
        "urgency": "Act within 48 hours of first spotting symptoms. Scab spreads fastest during wet periods."
    },

    "apple_black_rot": {
        "common_name": "Apple Black Rot",
        "pathogen": "Fungal disease caused by Botryosphaeria obtusa. Infects fruit, leaves, and bark — all three at once in severe cases.",
        "symptoms": "On leaves: purple spots with brown centres (frog-eye leaf spot). On fruit: brown rot starting at the blossom end, turning black and shrivelling into a hard mummy. On bark: reddish-brown cankers that kill branches.",
        "spread": "Spreads through rain splash and wind. Dead wood and mummified fruit left on the tree are the main source of new infections. Warm, wet conditions (24–29°C) accelerate spread dramatically.",
        "action": "Prune all dead, cankered, and diseased wood immediately. Remove mummified fruit from both the tree and the ground. Sterilise pruning shears with 70% alcohol between cuts. Burn or bag all removed material.",
        "chemical": "Apply Thiophanate-methyl 70WP at 1.5g per litre. Begin at pink bud stage, repeat every 10–14 days through petal fall. For active cankers, paint wounds with Copper oxychloride paste after pruning.",
        "prevention": "Eliminate all sources of dead wood — this is the single most effective prevention step. Avoid pruning wounds in wet weather. Ensure trees are well-fertilised so they resist infection.",
        "urgency": "High. Cankers spread to healthy wood over winter if not removed this season."
    },

    "apple_cedar_rust": {
        "common_name": "Apple Cedar Rust",
        "pathogen": "Fungal disease caused by Gymnosporangium juniperi-virginianae. Unusual because it requires two host plants to complete its life cycle — apple and cedar/juniper.",
        "symptoms": "Bright orange-yellow spots on the upper leaf surface, roughly 1–2cm diameter. On the underside of the same spots, orange tube-like structures develop. Infected fruit develop similar orange lesions and may be deformed.",
        "spread": "Spores produced on cedar/juniper trees in spring are carried by wind to apple trees. Cannot spread apple-to-apple — it must cycle through cedar. Warm, wet spring weather (16–24°C) triggers heavy spore release.",
        "action": "In late winter (before buds open), inspect nearby cedar and juniper trees for orange jelly-like galls. Remove and destroy every gall you find before they release spores. On infected apple leaves, no spray will reverse damage — focus on prevention.",
        "chemical": "Apply Myclobutanil 20EW at 1ml per litre starting at pink bud stage. Repeat every 7–10 days through the first 4–5 weeks of leaf development. Propiconazole 25EC at 1ml per litre is an effective alternative.",
        "prevention": "Remove all cedar and juniper trees within 300 metres of the orchard if possible. Plant rust-resistant apple varieties (e.g. Redfree, Williams Pride). Apply protective fungicide spray before rain events in spring.",
        "urgency": "Moderate. Act before bloom — sprays applied after infection are far less effective."
    },

    "apple_healthy": {
        "common_name": "Healthy Apple",
        "pathogen": "No disease detected.",
        "symptoms": "Leaves are uniformly green with no spots, lesions, or discolouration. Fruit surface is clean and unblemished.",
        "spread": "N/A",
        "action": "No action needed. Your apple crop appears healthy.",
        "chemical": "No chemical treatment required.",
        "prevention": "Continue weekly scouting from bud break through harvest. Maintain good orchard sanitation — remove fallen leaves and fruit promptly. Ensure balanced fertilisation; excessive nitrogen makes trees more susceptible to scab and fire blight.",
        "urgency": "None."
    },

    # ── BLUEBERRY ──────────────────────────────────────────────────────────────

    "blueberry_healthy": {
        "common_name": "Healthy Blueberry",
        "pathogen": "No disease detected.",
        "symptoms": "Leaves are deep green, firm, and free of spots or discolouration.",
        "spread": "N/A",
        "action": "No action needed. Crop is healthy.",
        "chemical": "No chemical treatment required.",
        "prevention": "Test and maintain soil pH between 4.5 and 5.5 — blueberries are extremely pH-sensitive and will decline rapidly in alkaline soils. Mulch heavily with pine bark or wood chips. Monitor for mummy berry disease and spotted wing drosophila during fruiting.",
        "urgency": "None."
    },

    # ── CHERRY ────────────────────────────────────────────────────────────────

    "cherry_healthy": {
        "common_name": "Healthy Cherry",
        "pathogen": "No disease detected.",
        "symptoms": "Leaves are glossy green with no lesions, holes, or yellowing.",
        "spread": "N/A",
        "action": "No action needed.",
        "chemical": "No chemical treatment required.",
        "prevention": "Scout weekly for cherry leaf spot and brown rot — both can appear quickly after wet weather. Prune for an open canopy shape to maximise light penetration and reduce humidity inside the tree.",
        "urgency": "None."
    },

    "cherry_powdery_mildew": {
        "common_name": "Cherry Powdery Mildew",
        "pathogen": "Fungal disease caused by Podosphaera clandestina. Unlike most fungi, it thrives in dry conditions with high humidity — rain actually washes spores away.",
        "symptoms": "White to grey powdery coating on young leaves, shoots, and buds. Infected leaves curl upward and may turn purple-red before dropping. Young fruit may be russeted or fail to develop normally.",
        "spread": "Spread entirely by wind-borne spores. Infects only young, actively growing tissue. Cool nights (15–18°C) combined with warm dry days (26–28°C) are ideal conditions. New flushes of growth in spring and early summer are highest risk.",
        "action": "Remove and bag all visibly infected shoots — cut 10cm below the last visible symptom. Do not compost. Increase spacing between branches through selective pruning to reduce the humid microclimate that favours the fungus.",
        "chemical": "Apply Sulphur 80WP at 2g per litre as a protective spray when new growth begins. For active infection, switch to Hexaconazole 5EC at 1ml per litre or Myclobutanil 20EW at 1ml per litre. Spray every 14 days, covering upper and lower leaf surfaces.",
        "prevention": "Avoid excessive nitrogen fertiliser — it promotes the soft new growth that mildew prefers. Choose mildew-resistant cherry varieties if replanting. Apply first protective spray at bud break every year regardless of visible symptoms.",
        "urgency": "Moderate. Control during early leaf development to protect the current season's crop."
    },

    # ── MAIZE / CORN ──────────────────────────────────────────────────────────

    "maize_cercospora": {
        "common_name": "Maize Gray Leaf Spot (Cercospora)",
        "pathogen": "Fungal disease caused by Cercospora zeae-maydis. One of the most yield-limiting maize diseases in humid regions.",
        "symptoms": "Rectangular, tan to grey lesions with parallel edges, running between leaf veins. Lesions are typically 2–5cm long. Under humid conditions, a grey powdery growth appears on lesions. Starts on lower leaves and progresses upward.",
        "spread": "Spores survive in crop debris and are splashed or windborne to new plants. Warm temperatures (25–30°C) combined with persistent leaf wetness (over 11 hours per day) are optimal for infection. Dense planting increases risk significantly.",
        "action": "Apply fungicide immediately at first sign of lesions on the lower 3 leaves. Remove and destroy heavily infected leaves if the stand is small. Avoid working in the field when leaves are wet as this spreads spores on clothing and equipment.",
        "chemical": "Apply Azoxystrobin 250SC at 1ml per litre. Spray at tasselling stage (VT) when lesions are first detected, then repeat 14 days later. Propiconazole 25EC at 1ml per litre is an effective alternative. Use a spreader-sticker adjuvant for better coverage on waxy maize leaves.",
        "prevention": "Plant resistant hybrids — this is the single most cost-effective control measure. Rotate crops with soybean or wheat to break the disease cycle. Avoid minimum tillage in areas with a history of the disease, as spores survive in surface residue.",
        "urgency": "High if lesions reach the ear leaf before tasselling — yield loss can exceed 50% in severe cases."
    },

    "maize_common_rust": {
        "common_name": "Maize Common Rust",
        "pathogen": "Fungal disease caused by Puccinia sorghi. Airborne spores can travel hundreds of kilometres on wind currents.",
        "symptoms": "Circular to elongated, brick-red to brown powdery pustules on both upper and lower leaf surfaces. Pustules rupture the leaf epidermis and release orange-red spores that rub off on fingers. Severe infections cause leaves to yellow and die prematurely.",
        "spread": "Wind-dispersed spores — source can be thousands of kilometres away. Cool temperatures (16–23°C) and high humidity or dew periods of 6+ hours are ideal. Can go from first lesion to epidemic across a field in under 2 weeks.",
        "action": "Apply fungicide at first detection — do not wait. Scout from V6 (6-leaf stage) onwards. If more than 5% of the leaf area on lower leaves is covered with pustules before tasselling, immediate treatment is warranted.",
        "chemical": "Apply Propiconazole 25EC at 1ml per litre. Spray at 14-day intervals. Tebuconazole 250EW at 1ml per litre or Azoxystrobin + Propiconazole mixture provides broader spectrum control and is recommended for severe outbreaks.",
        "prevention": "Plant rust-resistant hybrid varieties — effective resistance exists and is the best long-term solution. Avoid late planting into the cool season when rust pressure is highest. Monitor crop from V6 stage onwards weekly.",
        "urgency": "High. Early fungicide application (before tasselling) gives far better results than late application."
    },

    "maize_healthy": {
        "common_name": "Healthy Maize",
        "pathogen": "No disease detected.",
        "symptoms": "Leaves are broad, flat, and medium to dark green. No lesions, pustules, or streaking visible.",
        "spread": "N/A",
        "action": "No action needed.",
        "chemical": "No chemical treatment required.",
        "prevention": "Scout weekly from emergence to silking — the period from V6 to tasselling is the most critical window for disease entry. Ensure adequate potassium nutrition, as potassium deficiency increases susceptibility to rust and blight diseases.",
        "urgency": "None."
    },

    "maize_northern_blight": {
        "common_name": "Maize Northern Leaf Blight (Turcicum Blight)",
        "pathogen": "Fungal disease caused by Exserohilum turcicum (formerly Helminthosporium turcicum). A major constraint to maize production in cooler highland areas.",
        "symptoms": "Long, cigar-shaped lesions, 5–15cm in length, with tan or grey centres and dark brown borders. Lesions have a distinctive 'water-soaked' appearance when young. In humid weather, a dark olive-green sporulation forms on lesion surfaces. Starts on lower leaves.",
        "spread": "Spreads via wind and rain splash. Debris from previous seasons is the primary inoculum source. Cool (18–27°C), humid conditions with regular dew or rain are ideal. Spreads from lower to upper canopy over 2–4 weeks.",
        "action": "Apply fungicide when lesions are first detected on lower leaves, before the disease reaches the ear leaf. Remove heavily infected leaves from small plantings. Avoid overhead irrigation — shift to drip or furrow irrigation if possible.",
        "chemical": "Apply Mancozeb 75WP at 2.5g per litre. Spray every 14 days. For faster-acting control, use Propiconazole 25EC at 1ml per litre or Azoxystrobin 250SC at 1ml per litre as a curative spray.",
        "prevention": "Use resistant hybrids — the most cost-effective solution for recurring problems. Practice crop rotation: avoid maize-after-maize in the same field. Incorporate crop residue by deep tillage to reduce surface debris carrying spores.",
        "urgency": "High if lesions are present before tasselling. Protect the ear leaf at all costs — it supplies most of the carbohydrate for grain fill."
    },

    # ── GRAPE ─────────────────────────────────────────────────────────────────

    "grape_black_rot": {
        "common_name": "Grape Black Rot",
        "pathogen": "Fungal disease caused by Guignardia bidwellii. Can destroy 80–100% of a grape crop in a single season if uncontrolled.",
        "symptoms": "On leaves: small, circular, tan-brown spots with a dark border and tiny black dots (pycnidia) in the centre. On berries: begins as a white spot that rapidly spreads, turning the entire berry brown, then black, then shrivelling into a hard black mummy. Mummies remain attached to the cluster.",
        "spread": "Overwintered mummies on the vine or ground release spores during spring rain. Infection requires 8–10 hours of wet weather. All green tissue is susceptible — berries are most vulnerable from fruit set through 4 weeks after, then become resistant as they ripen.",
        "action": "Remove every mummified berry from the vine and the ground immediately — this is the single most important action. Rake and destroy all debris under vines. Prune infected shoots back to healthy wood. Apply fungicide before the next rain event.",
        "chemical": "Apply Mancozeb 75WP at 2g per litre. Begin at early shoot growth (5–10cm), spray every 10–14 days through 4 weeks after bloom. Myclobutanil 20EW at 1ml per litre is highly effective as a curative spray if applied within 72 hours of infection.",
        "prevention": "Eliminate mummies — they are the sole source of primary inoculum. Train vines to allow maximum airflow through the canopy. Apply dormant lime-sulphur spray before bud break each spring.",
        "urgency": "Critical during bloom and the 4 weeks after. Miss this window and the crop can be lost entirely."
    },

    "grape_esca": {
        "common_name": "Grape Esca (Black Measles)",
        "pathogen": "Complex fungal disease involving multiple pathogens (Phaeomoniella chlamydospora, Phaeoacremonium minimum, and Fomitiporia mediterranea). Infects the woody tissue of the vine, not just leaves.",
        "symptoms": "Tiger-stripe pattern on leaves — interveinal yellowing (red in red varieties) with a green border along the veins. Berries develop small dark purple spots ('measles'). In chronic form, vines decline slowly over years. In apoplectic form, entire vine wilts and dies within days during hot weather.",
        "spread": "Enters through pruning wounds. Spores are released during wet weather and colonise fresh cuts within hours. There is no evidence of direct vine-to-vine spread — every infection enters through a wound. Old, poorly maintained vineyards are most affected.",
        "action": "There is no curative chemical treatment. Remove apoplectic (suddenly wilted) vines immediately. For chronic infections, severely infected cordons or arms can be removed and the vine retrained from healthy wood — this can extend vine productive life by many years.",
        "chemical": "Protect every pruning wound with fungicidal wound paste (containing Trichoderma harzianum or thiophanate-methyl) applied within 30 minutes of cutting. This is the only effective chemical intervention.",
        "prevention": "Prune only during dry weather — never during rain. Disinfect all pruning tools between vines with 70% alcohol or 10% bleach solution. Double pruning (leaving a long cane, then cutting to final position 2–3 weeks later) reduces wound size and healing time.",
        "urgency": "Chronic form: moderate — plan for the next pruning season. Apoplectic collapse: remove that vine immediately before summer."
    },

    "grape_healthy": {
        "common_name": "Healthy Grape",
        "pathogen": "No disease detected.",
        "symptoms": "Leaves are medium to dark green, broadly lobed, with no discolouration or lesions.",
        "spread": "N/A",
        "action": "No action needed.",
        "chemical": "No chemical treatment required.",
        "prevention": "Scout weekly during the growing season. The critical disease windows for grapes are: bloom (downy mildew, black rot), post-bloom (powdery mildew), and veraison (botrytis). Maintain a spray diary to track what was applied and when.",
        "urgency": "None."
    },

    "grape_leaf_blight": {
        "common_name": "Grape Leaf Blight (Isariopsis Leaf Spot)",
        "pathogen": "Fungal disease caused by Pseudocercospora vitis. More common in hot, humid climates. Primarily a cosmetic issue but heavy infection causes premature defoliation.",
        "symptoms": "Irregular, angular, dark brown to black spots on upper leaf surface, often with a yellow halo. Lower leaf surface shows a grey-brown mouldy growth. Leaves turn yellow around infected areas and drop early, weakening the vine going into dormancy.",
        "spread": "Spreads via rain splash and wind from infected debris. Hot, humid weather (28–35°C with frequent rain) promotes rapid spread. Late-season infection is most common after veraison.",
        "action": "Remove and destroy infected leaves. Improve airflow through canopy by leaf removal around the fruit zone. Avoid overhead irrigation — switch to drip if using overhead sprinklers.",
        "chemical": "Apply Copper oxychloride 50WP at 3g per litre. Spray every 14 days from mid-season when conditions are humid. Mancozeb 75WP at 2g per litre is an effective alternative for protective sprays.",
        "prevention": "Ensure good canopy management — remove lateral shoots in the fruit zone to promote air circulation. Avoid excessive nitrogen fertilisation which produces dense, shaded canopies. Apply end-of-season clean-up spray after harvest.",
        "urgency": "Low to moderate. Primarily affects vine vigour for next season rather than current fruit."
    },

    # ── ORANGE ────────────────────────────────────────────────────────────────

    "orange_citrus_greening": {
        "common_name": "Citrus Greening (Huanglongbing / HLB)",
        "pathogen": "Caused by the bacterium Candidatus Liberibacter asiaticus, transmitted by the Asian citrus psyllid insect. Currently the most destructive citrus disease in the world — there is no cure.",
        "symptoms": "Blotchy, asymmetrical yellowing of leaves (unlike nutrient deficiencies which are symmetrical). Fruit remains partially green even when ripe, is lopsided, has a bitter taste, and contains aborted seeds. Infected trees decline over 5–10 years and eventually die.",
        "spread": "Spread exclusively by the Asian citrus psyllid (Diaphorina citri). A single psyllid can transmit the bacterium after feeding on an infected tree for just minutes. There is no tree-to-tree spread without the insect vector. New plantings near infected trees are at extreme risk.",
        "action": "There is no cure and no recovery. Infected trees must be removed and destroyed immediately to prevent the psyllid from spreading the disease to healthy trees. Do not leave stumps — grind or burn them. Report confirmed HLB to your local agricultural authority.",
        "chemical": "Psyllid control is the only management option: apply Imidacloprid 200SL as a soil drench at 1ml per litre of water around the tree base twice per year. Alternatively, foliar spray with Thiamethoxam 25WG at 0.5g per litre when new flushes of growth appear (this is when psyllids feed).",
        "prevention": "Source planting material only from certified disease-free nurseries. Install fine mesh windbreaks or netting around young trees in high-risk areas. Monitor weekly for psyllid adults and nymphs — they are small (3–4mm) and found on new growth flushes.",
        "urgency": "Critical. Every day an infected tree remains in the orchard is a day the psyllid is being reinfected and spreading HLB to your healthy trees."
    },

    # ── PEACH ─────────────────────────────────────────────────────────────────

    "peach_bacterial_spot": {
        "common_name": "Peach Bacterial Spot",
        "pathogen": "Bacterial disease caused by Xanthomonas arboricola pv. pruni. Affects peach, nectarine, plum, and apricot. One of the most difficult stone fruit diseases to manage because bacteria cannot be killed by fungicides.",
        "symptoms": "On leaves: small, water-soaked spots (2–5mm) that turn purple-brown with a yellow halo. Centre of spots often falls out creating a 'shot-hole' appearance. On fruit: small dark pits or craters on the surface, sometimes with cracking. Heavily infected fruit becomes unsaleable.",
        "spread": "Bacteria overwinter in buds and infected twigs. Released by rain and spread by water splash, wind-driven rain, and insects. Cool, wet spring weather (16–28°C) with frequent rain is ideal for epidemic spread. Wounds from insects, hail, or pruning tools accelerate infection.",
        "action": "Remove and bag all infected fruit and leaves — do not compost. Prune out any dead or cankered wood. Avoid working in the orchard during or after rain. Disinfect all pruning tools between trees. Apply copper spray before the next rain event.",
        "chemical": "Apply Copper hydroxide 77WP at 3g per litre. Spray every 7–10 days from green tip through petal fall during wet weather. Avoid copper during bloom (phytotoxic to flowers). Oxytetracycline (agricultural antibiotic) at label rates can be used during bloom as an alternative.",
        "prevention": "Plant resistant or tolerant varieties — susceptibility varies widely between cultivars. Establish windbreaks to reduce wind-driven rain impact. Avoid overhead irrigation. Prune to open tree structure, reducing the humid microclimate inside the canopy.",
        "urgency": "High during spring rain events. Apply copper protectively before rain — bacterial sprays are far less effective if applied after infection occurs."
    },

    "peach_healthy": {
        "common_name": "Healthy Peach",
        "pathogen": "No disease detected.",
        "symptoms": "Leaves are lance-shaped, medium green, and free from spots, holes, or gumming.",
        "spread": "N/A",
        "action": "No action needed.",
        "chemical": "No chemical treatment required.",
        "prevention": "Apply a copper-based dormant spray every year before bud swell to suppress bacterial spot and brown rot inoculum. Thin fruit to one per cluster 4–6 weeks after bloom to improve airflow and reduce disease risk.",
        "urgency": "None."
    },

    # ── PEPPER ────────────────────────────────────────────────────────────────

    "pepper_bacterial_spot": {
        "common_name": "Pepper Bacterial Spot",
        "pathogen": "Bacterial disease caused by Xanthomonas euvesicatoria. Affects pepper and tomato. Seed-borne — infected seed is the primary way the disease enters new fields.",
        "symptoms": "Small, water-soaked spots on leaves that enlarge and turn brown with a yellow halo. Centres dry out and may fall out, giving a ragged appearance. On fruit: raised, blister-like spots that become dark, sunken, and cracked — severely reducing marketability.",
        "spread": "Bacteria survive in infected seed, plant debris, and volunteer plants. Spread by rain splash, overhead irrigation, and wind-driven water. Hot (24–30°C), wet conditions with frequent overhead water contact cause explosive spread. Moves between plants rapidly when workers walk through wet foliage.",
        "action": "Remove and destroy severely infected plants immediately — do not compost. Reduce overhead irrigation to the minimum necessary. Stop all operations in the field when foliage is wet. Apply copper bactericide protectively before the next rain.",
        "chemical": "Apply Copper oxychloride 50WP at 2.5g per litre. Spray every 5–7 days during wet weather. For best results, mix copper with Mancozeb 75WP at 1.5g per litre — this combination provides broader protection. Strictly rotate products to delay copper resistance.",
        "prevention": "Use certified hot-water treated or disease-free seed. Transplant seedlings from clean, disease-free nurseries only. Avoid overhead irrigation — use drip irrigation. Rotate crops: do not plant pepper or tomato in the same field for at least 2 years.",
        "urgency": "High during warm, wet conditions. Apply copper spray before rain events for best protection."
    },

    "pepper_healthy": {
        "common_name": "Healthy Bell Pepper",
        "pathogen": "No disease detected.",
        "symptoms": "Leaves are glossy, dark green, and free from spots, wilting, or discolouration.",
        "spread": "N/A",
        "action": "No action needed.",
        "chemical": "No chemical treatment required.",
        "prevention": "Water at the base of plants only — overhead water on foliage is the primary driver of bacterial spot spread. Scout weekly, especially after rain or high humidity periods. Calcium sprays during fruit development can help prevent blossom-end rot.",
        "urgency": "None."
    },

    # ── POTATO ────────────────────────────────────────────────────────────────

    "potato_early_blight": {
        "common_name": "Potato Early Blight",
        "pathogen": "Fungal disease caused by Alternaria solani. Despite the name, it typically appears mid-season when plants begin to stress, not early in the season.",
        "symptoms": "Dark brown to black lesions with distinctive concentric rings forming a 'bull's-eye' or 'target' pattern. Surrounded by a yellow halo. Usually starts on lower, older leaves and progresses upward. Lesions may merge on severely infected leaves, causing complete leaf death.",
        "spread": "Spores survive in infected debris and infected seed tubers. Spread by wind, rain splash, and irrigation water. Warm (24–29°C), alternating wet and dry conditions favour rapid spread. Stressed plants (from drought, nutrient deficiency, heavy crop load) are far more susceptible.",
        "action": "Remove and destroy infected lower leaves immediately — do not compost. Ensure adequate nitrogen, phosphorus, and potassium nutrition to reduce plant stress. Apply fungicide at first symptom appearance. Begin irrigation management to avoid extreme wet-dry cycles.",
        "chemical": "Apply Mancozeb 75WP at 2.5g per litre. Spray every 7 days during humid conditions. For faster-acting curative control, use Difenoconazole 250EC at 0.5ml per litre or Azoxystrobin 250SC at 1ml per litre — rotate between chemical classes to prevent resistance.",
        "prevention": "Plant certified disease-free seed potatoes. Maintain adequate soil fertility — especially potassium, which strengthens cell walls against fungal penetration. Avoid overhead irrigation in the afternoon. Harvest promptly when mature — do not leave tubers in the ground.",
        "urgency": "Moderate. Primarily affects foliage and reduces yield through early defoliation rather than destroying tubers directly."
    },

    "potato_healthy": {
        "common_name": "Healthy Potato",
        "pathogen": "No disease detected.",
        "symptoms": "Leaves are dark green, compound, and free from spots, lesions, or wilting.",
        "spread": "N/A",
        "action": "No action needed.",
        "chemical": "No chemical treatment required.",
        "prevention": "Scout every 5–7 days from emergence. The critical monitoring periods are: early blight from tuber initiation onwards, late blight from canopy closure onwards. Hill soil up around stems to protect developing tubers from greening and blight infection.",
        "urgency": "None."
    },

    "potato_late_blight": {
        "common_name": "Potato Late Blight",
        "pathogen": "Caused by Phytophthora infestans — technically a water mould, not a true fungus. This pathogen caused the Irish Potato Famine of 1845–49. Still the most destructive potato disease in the world.",
        "symptoms": "Water-soaked, pale green to brown lesions on leaf edges and tips that expand rapidly. White fluffy sporulation visible on the underside of lesions in humid conditions. Infected stems turn brown and collapse. Tubers develop a reddish-brown dry rot internally that may not be visible externally.",
        "spread": "Spreads with terrifying speed in cool (10–20°C), wet or foggy conditions. A single infected plant can release 100,000+ spores per hour. An entire field can be destroyed in 7–10 days under ideal conditions. Wind carries spores over 10km.",
        "action": "This is an emergency. Remove and destroy every visibly infected plant immediately — do not leave infected haulm in the field. Bag and remove — do not compost. If infection is widespread, apply fungicide immediately and begin emergency harvest planning. Inspect tubers at harvest — discard any showing internal discolouration.",
        "chemical": "Apply Metalaxyl + Mancozeb (Ridomil Gold MZ) at 2g per litre immediately. Spray every 5–7 days. If resistance to Metalaxyl is suspected (which is increasingly common), switch to Cymoxanil + Mancozeb at 2.5g per litre. Mandipropamid (Revus) at 0.6ml per litre is highly effective against resistant strains.",
        "prevention": "Use certified blight-free seed tubers every season — do not save seed from infected crops. Plant resistant varieties where available. Begin preventive fungicide sprays when the canopy closes, before any symptoms appear. Avoid overhead irrigation — switch to drip. Eliminate volunteer plants from previous seasons.",
        "urgency": "CRITICAL — treat as an emergency. Every hour of delay in wet conditions allows exponential spread. Begin action immediately."
    },

    # ── RASPBERRY ─────────────────────────────────────────────────────────────

    "raspberry_healthy": {
        "common_name": "Healthy Raspberry",
        "pathogen": "No disease detected.",
        "symptoms": "Canes are firm and green (or red/purple depending on variety), leaves are bright green with no spots or distortion.",
        "spread": "N/A",
        "action": "No action needed.",
        "chemical": "No chemical treatment required.",
        "prevention": "Remove all old (fruited) canes immediately after harvest — cut to ground level. This eliminates the primary overwintering site for cane blight, spur blight, and grey mould. Tie in new canes with adequate spacing for air movement.",
        "urgency": "None."
    },

    # ── SOYBEAN ───────────────────────────────────────────────────────────────

    "soybean_healthy": {
        "common_name": "Healthy Soybean",
        "pathogen": "No disease detected.",
        "symptoms": "Trifoliate leaves are medium to dark green, flat, and free from spots, yellowing, or puckering.",
        "spread": "N/A",
        "action": "No action needed.",
        "chemical": "No chemical treatment required.",
        "prevention": "Scout from V3 growth stage weekly. Key disease windows: sudden death syndrome from early vegetative stages, soybean rust from R1 (flowering) onwards, white mould from R2 through R6. Ensure adequate potassium and boron nutrition for strong stem and pod development.",
        "urgency": "None."
    },

    # ── SQUASH ────────────────────────────────────────────────────────────────

    "squash_powdery_mildew": {
        "common_name": "Squash Powdery Mildew",
        "pathogen": "Fungal disease caused by Podosphaera xanthii (formerly Sphaerotheca fuliginea). Affects all cucurbit crops — squash, cucumber, melon, courgette, pumpkin.",
        "symptoms": "Characteristic white to grey powdery coating on leaf surfaces, starting as discrete circular patches that expand to cover the entire leaf. Unlike most fungal diseases, it thrives in dry conditions — rain does not spread it, it washes spores away. Infected leaves yellow, then brown, and die prematurely. Fruit may be small and poorly flavoured.",
        "spread": "Wind-dispersed spores only — no need for water on leaves. Warm days (20–27°C) with cool nights and high humidity (without rain) are ideal. Spreads extremely rapidly — can go from first spots to complete canopy infection in under 2 weeks.",
        "action": "Remove and destroy heavily infected leaves — do not compost. Increase plant spacing to improve airflow. Spray immediately at first sign of the white powder — do not wait.",
        "chemical": "Apply Sulphur 80WP at 2g per litre as a first-line treatment — highly effective and inexpensive. For established infection, use Myclobutanil 20EW at 1ml per litre or Trifloxystrobin 500SC at 0.3ml per litre. Potassium bicarbonate at 5g per litre is an organic option. Spray every 7 days. Do not use sulphur when temperatures exceed 32°C — it causes leaf burn.",
        "prevention": "Plant resistant varieties — significant differences in susceptibility exist between cultivars. Space plants at least 60–90cm apart. Avoid late-afternoon irrigation that creates humid overnight conditions. Remove all crop debris immediately after harvest.",
        "urgency": "High. Powdery mildew can reduce photosynthesis by 50% and severely limit fruit quality and shelf life."
    },

    # ── STRAWBERRY ────────────────────────────────────────────────────────────

    "strawberry_healthy": {
        "common_name": "Healthy Strawberry",
        "pathogen": "No disease detected.",
        "symptoms": "Leaves are trifoliate, dark green, firm, and free from spots, reddening, or marginal scorch.",
        "spread": "N/A",
        "action": "No action needed.",
        "chemical": "No chemical treatment required.",
        "prevention": "Scout weekly for angular leaf spot, grey mould (botrytis), and powdery mildew. Remove old and dead leaves regularly from the plant crown area to improve airflow and reduce fungal inoculum. Replace strawberry beds every 3–4 years as disease pressure accumulates over time.",
        "urgency": "None."
    },

    "strawberry_leaf_scorch": {
        "common_name": "Strawberry Leaf Scorch",
        "pathogen": "Fungal disease caused by Diplocarpon earlianum. Often confused with drought stress but the pattern is distinctly different.",
        "symptoms": "Small, irregular, dark purple to red spots on the upper leaf surface, often with no yellow halo (unlike leaf spot). Spots merge to give the leaf an overall scorched, dried appearance. Leaf edges and tips darken. Severely infected leaves dry and die but often remain attached to the plant.",
        "spread": "Conidia (spores) spread by rain splash and irrigation water. Infected debris in and around the plant crown is the main inoculum source. Cool to mild (15–25°C), wet weather promotes infection. Older leaves are more susceptible than young leaves.",
        "action": "Remove and destroy all infected and dead leaves. Clear all debris from around the plant crown. Avoid overhead irrigation — switch to drip. Apply fungicide after removal of infected material.",
        "chemical": "Apply Myclobutanil 20EW at 1ml per litre. Spray every 14 days during the growing season. Captan 50WP at 2g per litre is an effective alternative for protective applications.",
        "prevention": "Renovate beds after harvest — mow foliage, thin plants, and apply a protective fungicide spray. Use drip irrigation only. Avoid planting strawberries in the same site as a previous strawberry crop for at least 2 years.",
        "urgency": "Moderate. Reduces plant vigour and can significantly impact yield in the following season if left uncontrolled."
    },

    # ── TOMATO ────────────────────────────────────────────────────────────────

    "tomato_bacterial_spot": {
        "common_name": "Tomato Bacterial Spot",
        "pathogen": "Caused by Xanthomonas perforans (and related species). Seed-borne. One of the most common and damaging bacterial diseases of tomato worldwide.",
        "symptoms": "Small, circular, water-soaked spots on leaves (2–4mm) with yellow halos that later turn dark brown to black. Centre of spots may fall out creating shot holes. On green fruit: small, raised, blister-like spots with white halos that turn brown and sunken as fruit ripens — severely affecting marketability.",
        "spread": "Bacteria survive in infected seed, plant debris, and weeds. Spread explosively by rain splash, overhead irrigation, and wind-driven water. Workers moving through wet foliage spread bacteria on hands, clothing, and tools. Hot (27–30°C) wet weather is ideal. Can spread from one infected plant to the entire field within a week.",
        "action": "Remove and destroy infected plants or heavily infected plant parts. Stop all field operations when foliage is wet. Apply copper bactericide immediately. Switch to drip irrigation if using overhead sprinklers.",
        "chemical": "Apply Copper hydroxide 77WP at 3g per litre every 7 days. Mix with Mancozeb 75WP at 1.5g per litre for better coverage. Rotate copper products with Kasugamycin (where available) every 3–4 sprays to slow resistance development — copper resistance is increasingly common.",
        "prevention": "Source certified pathogen-free seed or treat seed with hot water (50°C for 25 minutes) before planting. Never save seed from infected crops. Use drip irrigation exclusively. Rotate tomatoes with non-solanaceous crops for 2+ years.",
        "urgency": "High during warm, wet conditions. Apply copper spray protectively before forecast rain."
    },

    "tomato_early_blight": {
        "common_name": "Tomato Early Blight",
        "pathogen": "Fungal disease caused by Alternaria solani. Extremely common wherever tomatoes are grown. Most damaging during warm, humid conditions after fruit set.",
        "symptoms": "Dark brown to black, circular lesions with a distinctive concentric ring 'bull's-eye' pattern and yellow halo. Typically 1–2cm diameter. Starts on the oldest, lowest leaves and moves steadily upward. In severe cases, entire lower canopy is killed, dramatically reducing photosynthetic capacity and yield.",
        "spread": "Conidia spread by wind, rain splash, and water. Survives in plant debris and infected seed. Alternating wet and dry conditions with moderate temperatures (24–29°C) are ideal. Plant stress (drought, heavy crop load, nitrogen deficiency) dramatically increases susceptibility.",
        "action": "Remove and destroy all infected lower leaves immediately — bag and remove from the field. Stake or trellis plants to keep foliage off the ground. Apply fungicide at first symptom. Ensure adequate nitrogen fertilisation — stressed plants are far more vulnerable.",
        "chemical": "Apply Mancozeb 75WP at 2.5g per litre every 7 days. For active infection, rotate with Difenoconazole 250EC at 0.5ml per litre or Azoxystrobin 250SC at 1ml per litre every second spray to prevent resistance. Always use a wetting agent for better coverage on tomato foliage.",
        "prevention": "Mulch soil under plants to prevent rain splash carrying spores from soil to lower leaves — this alone can significantly delay disease onset. Avoid overhead irrigation. Space plants 60–90cm apart for good airflow. Use disease-free seed.",
        "urgency": "Moderate to high once visible on lower canopy. Act before it reaches the upper leaves and fruit."
    },

    "tomato_healthy": {
        "common_name": "Healthy Tomato",
        "pathogen": "No disease detected.",
        "symptoms": "Leaves are pinnately compound, deep green, slightly sticky (from glandular hairs), and free from spots, lesions, or yellowing.",
        "spread": "N/A",
        "action": "No action needed. Crop is healthy.",
        "chemical": "No chemical treatment required.",
        "prevention": "Scout every 5–7 days. Watch for early blight symptoms on lower leaves from fruit set onwards. Ensure consistent watering — irregular moisture causes blossom-end rot and physiological leaf roll, which can be confused with disease. Stake or cage all plants.",
        "urgency": "None."
    },

    "tomato_late_blight": {
        "common_name": "Tomato Late Blight",
        "pathogen": "Caused by Phytophthora infestans — the same pathogen that causes potato late blight and caused the Irish Famine. Extremely destructive and fast-moving.",
        "symptoms": "Pale green to brown, water-soaked, irregular lesions on leaves that expand rapidly, with a white fluffy mould visible on the underside of lesions in humid conditions. Infected stems turn brown to black and collapse. Fruit develops firm brown rot from the stem end inward.",
        "spread": "Spreads with exceptional speed in cool (10–20°C), wet or misty conditions. A single infected plant under ideal conditions can produce over 100,000 spores per hour. Wind carries spores to new fields kilometres away. An entire unprotected tomato crop can be destroyed in under 2 weeks.",
        "action": "EMERGENCY ACTION REQUIRED. Remove every infected plant part from the field immediately. Do not compost — burn or bury deeply. If more than 10% of the crop shows symptoms, begin emergency harvest of any mature green fruit before they are infected. Apply fungicide immediately and every 5 days.",
        "chemical": "Apply Metalaxyl + Mancozeb (Ridomil Gold MZ) at 2g per litre immediately. Repeat every 5–7 days. Cymoxanil + Famoxadone (Equation Pro) at 0.4g per litre is effective against Metalaxyl-resistant strains. Mandipropamid (Revus) at 0.6ml per litre provides excellent curative and protective activity.",
        "prevention": "Apply preventive fungicide sprays from canopy closure — before any symptoms appear. Never plant tomatoes near or downwind from potatoes. Use certified disease-free transplants. Avoid overhead irrigation. Plant resistant varieties wherever available.",
        "urgency": "CRITICAL. This is one of the fastest-spreading plant diseases known. Begin emergency action now — every 24 hours without action in wet weather can double the infected area."
    },

    "tomato_leaf_mold": {
        "common_name": "Tomato Leaf Mold",
        "pathogen": "Fungal disease caused by Passalora fulva (formerly Fulvia fulva). Almost exclusively a disease of greenhouse and tunnel-grown tomatoes where humidity can be controlled less easily.",
        "symptoms": "Upper leaf surface: pale green to yellow, irregular, diffuse patches without sharp borders. Lower leaf surface (directly below the yellow patches): dense, olive-green to greyish-brown velvety mould — this is the diagnostic feature. Infected leaves curl upward, yellow, then die. Severe infection causes rapid defoliation.",
        "spread": "Spreads by airborne conidia under high humidity (over 85% RH). Spores can survive in dry conditions for months on plant debris and greenhouse structures. Optimal temperature is 22–24°C. In greenhouses, the disease can spread from a single plant to the entire crop within 2 weeks.",
        "action": "Immediately increase ventilation — open all side vents and roof vents. Run heating at night to reduce relative humidity below 80%. Remove and bag all infected leaves. Sanitise greenhouse surfaces (benches, clips, strings) with a suitable disinfectant at end of season.",
        "chemical": "Apply Chlorothalonil 75WP at 2g per litre. Spray every 10–14 days, covering the undersides of leaves thoroughly where the fungus grows. Fenhexamid or Iprodione can be used as alternatives. Ensure good penetration into the canopy with a fine mist sprayer.",
        "prevention": "Maintain humidity below 85% at all times through active ventilation and heating. Ensure wide in-row spacing (at least 40cm). Use resistant varieties where available — significant resistance has been bred into modern commercial varieties. Disinfect the entire greenhouse structure between crops.",
        "urgency": "High in humid greenhouse or tunnel conditions. Control humidity immediately — it is more effective than fungicide alone."
    },

    "tomato_septoria": {
        "common_name": "Tomato Septoria Leaf Spot",
        "pathogen": "Fungal disease caused by Septoria lycopersici. Very common in temperate humid regions. Does not infect fruit but can completely defoliate a plant.",
        "symptoms": "Numerous small, circular spots (3–6mm), with dark brown borders and a pale tan to grey centre. Tiny black dots (pycnidia — the fungal fruiting bodies) are visible in the centre of spots under a hand lens — this is the diagnostic feature distinguishing it from early blight. Starts on lowest leaves, progresses upward rapidly.",
        "spread": "Spreads primarily by rain splash from infected debris on the soil surface. Also spread by contact — hands, tools, clothing. Warm (20–25°C), wet weather with frequent rain or overhead irrigation. Spores are released from pycnidia during rain and can infect new leaves immediately.",
        "action": "Remove and destroy infected lower leaves at first sign. Mulch soil surface to prevent rain splash from soil-borne spores. Apply fungicide immediately and continue on a 7-day schedule during wet weather. Avoid working in the field when plants are wet.",
        "chemical": "Apply Mancozeb 75WP at 2g per litre every 7 days. Rotate every 2–3 sprays with Chlorothalonil 75WP at 2g per litre or Azoxystrobin 250SC at 1ml per litre to prevent resistance development. Ensure thorough coverage of lower canopy where disease is most active.",
        "prevention": "Mulch around plants with straw or plastic to prevent soil-to-leaf spore splash — this is one of the most effective low-cost prevention measures. Rotate crops — do not plant tomato or potato in the same field for 2 years. Remove all crop debris immediately after harvest.",
        "urgency": "Moderate to high. Can cause complete defoliation leaving fruit exposed to sunscald and reducing yield by 50%+."
    },

    "tomato_spider_mite": {
        "common_name": "Tomato Spider Mite (Two-Spotted)",
        "pathogen": "Not a disease but an infestation by the two-spotted spider mite (Tetranychus urticae). One of the most damaging arthropod pests of vegetables worldwide. Extremely difficult to control once established.",
        "symptoms": "First sign: pale yellow stippling (tiny dots) on upper leaf surface caused by mites piercing cells and extracting contents. Lower leaf surface has fine webbing with tiny moving specks (mites, eggs). As infestation worsens, leaves bronzen, turn completely yellow, dry out, and fall. Fruit may be scarred. Entire plants can be killed in 2–3 weeks under hot, dry conditions.",
        "spread": "Spreads by walking between plants, on clothing and tools, and by wind. Hot (27–38°C), dry, dusty conditions cause rapid population explosions — populations can double every 3–5 days. Water stress dramatically increases susceptibility. Broad-spectrum insecticide use kills natural predators (especially predatory mites) and triggers massive mite outbreaks.",
        "action": "Spray leaf undersides forcefully with water first — this physically removes mites and webbing and is surprisingly effective at reducing populations. Remove heavily infested lower leaves. Apply acaricide immediately, targeting leaf undersides where mites live. If possible, introduce predatory mites (Phytoseiulus persimilis) as a biological control.",
        "chemical": "Apply Abamectin 1.8EC at 1ml per litre. Spray in the early evening — do not spray in midday heat above 32°C as the product breaks down and mites become heat-stressed (making the spray seem effective when it was not). Spiromesifen 240SC at 0.75ml per litre is effective against eggs and nymphs. Always rotate acaricides — mites develop resistance extremely rapidly.",
        "prevention": "Maintain adequate soil moisture — water-stressed plants are far more attractive to mites. Avoid broad-spectrum pyrethroid sprays that kill beneficial predatory insects. Remove dusty conditions (mites thrive in dust). Monitor leaf undersides weekly from fruit set — early detection is critical.",
        "urgency": "High. Mite populations can increase 10-fold within a week under hot, dry conditions. Act at first sign of stippling."
    },

    "tomato_target_spot": {
        "common_name": "Tomato Target Spot",
        "pathogen": "Fungal disease caused by Corynespora cassiicola. Increasingly important in tropical and subtropical regions. Can infect leaves, stems, and fruit.",
        "symptoms": "Brown, circular lesions with concentric rings (similar to early blight but more pronounced rings and less yellow halo). Lesions on stems are elongated and sunken. On fruit: dark, sunken, circular lesions with concentric rings — these cause fruit rot and can make entire batches unsaleable. Lesions can appear on all plant parts.",
        "spread": "Airborne conidia spread by wind and rain splash. Survives in infected debris. Warm (24–32°C), humid conditions with extended leaf wetness (8+ hours) are ideal. More prevalent in greenhouses and tunnel growing, especially at high temperatures.",
        "action": "Remove infected leaves and fruit immediately. Do not compost. Improve air circulation through pruning lateral shoots. Apply fungicide immediately at first sign of lesions on leaves — do not wait until fruit is affected.",
        "chemical": "Apply Azoxystrobin 250SC at 1ml per litre every 14 days. Chlorothalonil 75WP at 2g per litre is effective as a protective spray. Tebuconazole 250EW at 1ml per litre provides curative activity. Rotate chemical classes every 2 sprays.",
        "prevention": "Crop rotation with non-solanaceous crops for 2 years. Avoid overhead irrigation — use drip. Increase plant spacing. Remove all crop debris after harvest and consider soil fumigation in severely affected fields.",
        "urgency": "Moderate to high when fruit is infected — fruit losses can be severe and rapid."
    },

    "tomato_mosaic_virus": {
        "common_name": "Tomato Mosaic Virus (ToMV)",
        "pathogen": "Caused by Tomato mosaic virus (ToMV) and/or Tobacco mosaic virus (TMV). These are among the most stable plant viruses known — TMV can survive on dry surfaces and in soil for decades.",
        "symptoms": "Mosaic (alternating light green, yellow, and dark green areas) on leaves — the pattern looks marbled. Young leaves may be distorted, narrow, and fern-like ('fern leaf'). Fruit may show yellow blotches, brown internal discolouration ('internal browning'), and reduced size. Plants are stunted and unproductive.",
        "spread": "Spread primarily by physical contact — on hands, tools, clothing, cigarettes (tobacco products contain TMV and must never be handled near tomato plants). There is no insect vector for TMV/ToMV. Spreads plant-to-plant when workers touch infected then healthy plants. Seed transmission occurs at low rates.",
        "action": "There is no cure for virus-infected plants. Remove and destroy infected plants immediately if they are early-stage — if most of the crop is infected, leave plants in place as removing them may spread the virus further via contact. Immediately disinfect all tools, ties, stakes, and hands with milk (casein in milk denatures the virus — highly effective and cheap) or 10% bleach solution.",
        "chemical": "No effective chemical treatment exists against plant viruses. Focus entirely on sanitation and prevention. Imidacloprid 200SL at 0.5ml per litre can control aphid vectors of other viruses if aphids are present.",
        "prevention": "Wash hands thoroughly before handling plants and between rows. Never smoke near tomato plants. Source certified virus-tested seed. Use TMV/ToMV-resistant varieties — broad resistance is available in commercial cultivars. Disinfect all greenhouse equipment between crops with 10% trisodium phosphate solution.",
        "urgency": "High if detected early — remove infected plants before the virus spreads through the crop via contact. If widespread, focus on sanitation to protect remaining healthy plants."
    },

    "tomato_yellow_leaf_curl": {
        "common_name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "pathogen": "Caused by Tomato yellow leaf curl virus (TYLCV), transmitted exclusively by the silverleaf whitefly (Bemisia tabaci). One of the most economically important tomato viruses globally.",
        "symptoms": "Upward curling and cupping of leaves, giving a spoon-like appearance. Leaves are smaller than normal and show yellowing of leaf margins and interveinal areas. Infected plants are severely stunted — sometimes half the normal size. Flowers may drop and fruit set is dramatically reduced or absent on plants infected at a young stage. Fruit on infected plants is small and of poor quality.",
        "spread": "Spread only by the silverleaf whitefly (Bemisia tabaci). A single whitefly can acquire the virus in 15–30 minutes of feeding and transmit it immediately to the next plant. Whitefly populations can explode rapidly in hot, dry conditions. The virus can also persist in whitefly for its entire life (persistent transmission).",
        "action": "Remove and destroy infected plants immediately — especially if caught in the first few weeks. Visually inspect plants daily and remove any showing early symptoms before whiteflies have time to acquire and transmit the virus from them. Apply whitefly control spray immediately to kill the vector — this will not cure infected plants but will protect healthy ones.",
        "chemical": "Apply Imidacloprid 200SL at 0.5ml per litre as a soil drench to transplants 2 days before field planting — this gives 3–4 weeks of systemic whitefly control during the most critical establishment period. For foliar application, use Thiamethoxam 25WG at 0.5g per litre or Spirotetramat 150OD at 0.8ml per litre. Rotate insecticide classes every 2 sprays — whitefly resistance to neonicotinoids is increasingly common.",
        "prevention": "Install fine UV-blocking mesh (50-mesh) over nursery beds and tunnels — this physically excludes whiteflies without chemicals. Use TYLCV-resistant varieties where available. Plant away from older infected crops and weed hosts. Hang yellow sticky traps (1 per 25m²) to monitor whitefly populations — act when you catch more than 5 per trap per week.",
        "urgency": "Critical. Plants infected before the 5-leaf stage produce almost no yield. Protecting transplants during the first 4 weeks in the field is the highest priority intervention."
    },
}


# ============================================================
# STEP 6: ROUTES
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

        image = Image.open(filepath).convert('RGB')
        input_tensor = transform(image).unsqueeze(0).to(device)

        with torch.no_grad():
            output = model(input_tensor)

        temperature = 2.1
        scaled_output = output[0] / temperature
        probabilities = F.softmax(scaled_output, dim=0)
        predicted_idx = torch.argmax(probabilities).item()
        confidence = probabilities[predicted_idx].item() * 100

        predicted_class = class_names[predicted_idx]

        heatmap_filename = 'heatmap_' + unique_filename
        heatmap_path = os.path.join(app.config['UPLOAD_FOLDER'], heatmap_filename)
        heatmap_success = generate_heatmap(filepath, predicted_idx, heatmap_path)

        if not heatmap_success:
            heatmap_path = None

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

        treatment = TREATMENTS.get(predicted_class, {
            "common_name": predicted_class.replace('_', ' ').title(),
            "pathogen": "No pathogen information available.",
            "symptoms": "No symptom information available.",
            "spread": "No spread information available.",
            "action": "No specific treatment information available.",
            "chemical": "Consult a local agricultural expert.",
            "prevention": "Monitor regularly and maintain good crop hygiene.",
            "urgency": "Unknown."
        })

        result = {
            'filename': unique_filename,
            'original_image': filepath,
            'predicted_class': predicted_class,
            'common_name': treatment['common_name'],
            'confidence': int(confidence) if confidence == int(confidence) else round(confidence, 1),
            'severity': severity,
            'severity_color': severity_color,
            'pathogen': treatment.get('pathogen', ''),
            'symptoms': treatment.get('symptoms', ''),
            'spread': treatment.get('spread', ''),
            'action': treatment['action'],
            'chemical': treatment['chemical'],
            'prevention': treatment['prevention'],
            'urgency': treatment.get('urgency', ''),
            'heatmap_path': heatmap_filename if heatmap_success else None
        }

        return render_template('result.html', result=result)

    flash('Invalid file type. Please upload PNG, JPG, or JPEG.')
    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)