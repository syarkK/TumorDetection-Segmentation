import streamlit as st
from PIL import Image
from streamlit_lottie import st_lottie
import requests
from utils.image_processing import classify_image, preprocess, segment, overlay_mask, convert_to_rgb

# ===== Color Palette =====
COLOR_RED = "#610f86"
COLOR_GREEN = "#ffb404"
COLOR_BG_TUMOR = "#7f27a8"
COLOR_BG_NON = "#ffd400"
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
    st.markdown("<h5 style='text-align: center; color: gray;'>help doctors segment tumor area of Brain MRI images</h5>", unsafe_allow_html=True)

    # ===== Upload Box =====
    uploaded_file = st.file_uploader("Upload an MRI image", type=["jpg", "jpeg", "png"])
    col1, col2 = st.columns([2, 1])

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")

        with col1:
            st.image(image, caption="Uploaded Image", use_container_width=True)

        with col2:
            if st.button("Classify", use_container_width=True):
                # Show Lottie animation in placeholder
                placeholder = st.empty()
                with placeholder.container():
                    center = st.columns([1, 2, 1])[1]
                    with center:
                        st_lottie(lottie_loading, height=200, key="classify_animation")

                # Perform classification
                model = st.session_state['classification_model']
                rgb_image = convert_to_rgb(image)
                prediction = classify_image(rgb_image, model)

                # Clear animation
                placeholder.empty()

                # Save results
                st.session_state['classification_result'] = prediction
                st.session_state['show_segment_button'] = prediction > 0.5
                st.session_state['uploaded_image'] = image

            if 'classification_result' in st.session_state:
                prob = st.session_state['classification_result']
                is_tumorous = prob > 0.5
                percentage = prob * 100 if is_tumorous else (1 - prob) * 100

                st.markdown(
                    f"""
                    <div style='
                        background-color: {COLOR_BG_TUMOR if is_tumorous else COLOR_BG_NON};
                        padding: 20px;
                        border-radius: 10px;
                        border-left: 10px solid {COLOR_RED if is_tumorous else COLOR_GREEN};
                        text-align: center;
                        margin-top: 20px;
                    '>
                        <h1 style='color: {COLOR_TEXT}; font-size: 48px; margin: 0;'>{percentage:.2f}%</h1>
                        <div style='
                            width: 100%;
                            background-color: rgba(255,255,255,0.2);
                            border-radius: 10px;
                            height: 15px;
                            margin: 10px 0;
                        '>
                            <div style='
                                width: {percentage}% ;
                                background-color: {COLOR_RED if is_tumorous else COLOR_GREEN};
                                height: 100%;
                                border-radius: 10px;
                            '></div>
                        </div>
                        <h2 style='font-size: 20px; margin-top: 2px; color: {COLOR_TEXT};'>
                            {"Tumorous" if is_tumorous else "Non-Tumorous"}
                        </h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown("---")

    # ===== Segmentation =====
    if st.session_state.get('show_segment_button', False):
        if st.button("Segment Tumor", use_container_width=True):
            # Show Lottie animation in placeholder
            placeholder = st.empty()
            with placeholder.container():
                center = st.columns([1, 2, 1])[1]
                with center:
                    st_lottie(lottie_loading, height=200, key="segment_animation")

            # Perform segmentation
            image = st.session_state.get('uploaded_image')
            tensor_img = preprocess(image)
            mask = segment(tensor_img)
            overlay = overlay_mask(image, mask)

            # Clear animation
            placeholder.empty()

            st.session_state['segmented_image'] = overlay
            st.image(overlay, caption="Segmented Tumor", use_container_width=True)

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
                for key in ['classification_result', 'show_segment_button', 'uploaded_image', 'segmented_image']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
