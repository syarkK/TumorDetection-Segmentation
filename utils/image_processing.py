# utils/image_processing.py
import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import segmentation_models_pytorch as smp
import cv2
import torchvision.transforms as transforms
import streamlit as st
from huggingface_hub import hf_hub_download

model_path = hf_hub_download(repo_id="whattheduckk/Classification", filename="classification.keras")
classification_model = load_model(model_path)


# Device setup
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Constants
image_width = 255
image_height = 255

# Load classification model
def load_classification_model():
    model_path = hf_hub_download(repo_id="whattheduckk/Classification", filename="classification.keras")
    return load_model(model_path)

def convert_to_rgb(image_path_or_pil):
    if isinstance(image_path_or_pil, str):
        img = Image.open(image_path_or_pil)
    else:
        img = image_path_or_pil
    
    return img.convert("RGB")

# Classify image
def classify_image(image: Image.Image, model):
    image = image.resize((image_width, image_height))
    img_array = img_to_array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)[0][0]
    return prediction

# Load segmentation model
@st.cache_resource
def load_model_segmentation():
    model_path = hf_hub_download(repo_id="whattheduckk/Segmentation", filename="segmentation.pth")
    model = torch.load(model_path, map_location=device, weights_only=False)
    model.to(device)
    model.eval()
    return model


# Preprocess image for segmentation
def normalize_image(img):
    img = img.astype(np.float32)
    return (img - np.min(img)) / (np.max(img) - np.min(img) + 1e-5)

def enhance_contrast_clahe_color(img):
    if len(img.shape) == 2:  # Grayscale
        img = np.uint8(255 * normalize_image(img))
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        return clahe.apply(img)
    else:  # Color image
        img = np.uint8(255 * normalize_image(img))
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l_clahe = clahe.apply(l)
        lab_clahe = cv2.merge((l_clahe, a, b))
        return cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)

def preprocess(image: Image.Image):
    # Convert PIL to NumPy
    img_np = np.array(image)

    # Apply CLAHE
    img_clahe = enhance_contrast_clahe_color(img_np)

    # Convert NumPy back to PIL for TorchVision transform
    image_clahe = Image.fromarray(img_clahe)

    # Resize & convert to tensor
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
    ])
    return transform(image_clahe).unsqueeze(0)

# Run segmentation
def segment(tensor_image):
    model = st.session_state['segmentation_model']
    with torch.no_grad():
        output = model(tensor_image.to(device))[0]
        mask = output.squeeze().cpu().numpy()
        return (mask > 0.5).astype(np.uint8)

# Overlay mask
def overlay_mask(image: Image.Image, mask: np.ndarray):
    mask_img = Image.fromarray((mask * 255).astype(np.uint8)).resize(image.size)
    red_mask = Image.new("RGBA", image.size, color=(255, 0, 0, 100))
    mask_img = mask_img.convert("L")
    return Image.composite(red_mask, image.convert("RGBA"), mask_img)
