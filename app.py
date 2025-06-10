# app.py
import streamlit as st
from utils.image_processing import load_classification_model, load_model_segmentation

# Set Streamlit page config
st.set_page_config(page_title="Brain Tumor Segmentation", layout="centered")

# Sidebar navigation
with st.sidebar:
    st.markdown("### Navigation")
    page = st.radio("Go to", ["Welcome", "Tumor Detection and Segmentation","Tumor Segmentation"])


# Load models only once
st.session_state.setdefault('classification_model', load_classification_model())
st.session_state.setdefault('segmentation_model', load_model_segmentation())

# Route to appropriate page
if page == "Welcome":
    from modules.welcome import show_welcome
    show_welcome()
elif page == "Tumor Detection and Segmentation":
    from modules.Tumor_Detection import show_detection_page
    show_detection_page()
elif page == "Tumor Segmentation":
    from modules.Tumor_Segmentation import show_detection_page
    show_detection_page()
