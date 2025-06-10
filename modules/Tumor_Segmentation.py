import streamlit as st
from PIL import Image
from utils.image_processing import preprocess, segment, overlay_mask
from streamlit_lottie import st_lottie
import requests

# ===== Color Palette =====
COLOR_PURPLE = "#610f86"
COLOR_TEXT = "#f5f5f5"

# ===== Load Lottie Animation from URL =====
def load_lottie_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

lottie_loading = load_lottie_url("https://lottie.host/5d3568ea-24c0-4843-8a9e-9cc7f5db3233/wYGSF5fWAk.json")
lottie_headline = load_lottie_url("https://lottie.host/8fdfa294-378a-4dc8-ab5f-75017b687791/Fqz0j0fwtp.json")

def show_detection_page():
    # ===== Animated Title =====
    st_lottie(lottie_headline, height=250, key="tumornet_headline")
    st.markdown("<h5 style='text-align: center; color: gray;'>Help doctors segment tumor area of Brain MRI images</h5>", unsafe_allow_html=True)

    # ===== Upload Box =====
    uploaded_file = st.file_uploader("Upload an MRI image", type=["jpg", "jpeg", "png"])
    col1, col2 = st.columns([1, 1])

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")

        with col1:
            st.image(image, caption="Uploaded Image", use_container_width=True)

        with col2:
            if st.button("Segment", use_container_width=True):
                # Show animation placeholder
                placeholder = st.empty()
                with placeholder.container():
                    center = st.columns([1, 2, 1])[1]
                    with center:
                        st_lottie(lottie_loading, height=200, key="segmentation")

                # Perform segmentation
                tensor_img = preprocess(image)
                mask = segment(tensor_img)
                overlay = overlay_mask(image, mask)

                # Clear animation
                placeholder.empty()

                st.session_state['segmented_image'] = overlay
                st.image(overlay, caption="Segmented Tumor", use_container_width=True)

    st.markdown("---")

    # ===== Download and Refresh Buttons =====
    if 'segmented_image' in st.session_state:
        colA, colB = st.columns([1, 1])

        with colA:
            st.download_button(
                label="Download",
                data=st.session_state['segmented_image'].tobytes(),
                file_name="segmented_tumor.png",
                mime="image/png"
            )

        with colB:
            if st.button("Refresh (Start Again)"):
                for key in ['segmented_image']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
