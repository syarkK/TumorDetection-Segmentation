# pages/welcome.py
import streamlit as st
from streamlit_lottie import st_lottie
import json
import requests

def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def show_welcome():
    # Load your custom headline animation
    headline_lottie_url = "https://lottie.host/8fdfa294-378a-4dc8-ab5f-75017b687791/Fqz0j0fwtp.json"
    headline_lottie_json = load_lottie_url(headline_lottie_url)

    # Display the animation centered at the top as the "TumorNet" logo/title
    st_lottie(headline_lottie_json, height=250, key="tumornet_headline")

    # Optional subheadline
    st.markdown("<h4 style='text-align: center; color: gray;'>Helping doctors detect and segment brain MRI tumors</h4>", unsafe_allow_html=True)

    # Load brain animation
    lottie_url = "https://lottie.host/2841b819-67cd-4299-abd6-aec5c09a4ec3/3xguLRcNIM.json"
    lottie_json = load_lottie_url(lottie_url)

    st_lottie(lottie_json, height=350, key="brain_animation")

    # Create two columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div style="background-color:#7f27a8; padding:20px; border-radius:10px; color:white;">
                <h3>🧠 Features</h3>
                <ul>
                    <li><b>Classification:</b> Detect if the uploaded MRI image is tumorous.</li>
                    <li><b>Segmentation:</b> If tumorous, we'll highlight the affected brain region.</li>
                </ul>
                <p>👉 Navigate to <b>Tumor Detection</b> to get started!</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div style="background-color:#ffd200; padding:20px; border-radius:10px; color:black">
                <h3>👥 Group Members</h3>
                <ul>
                    <li><b>Anastasia Prameswari Dwi Putri</b></li>
                    <li><b>Aliyah Fathimah Assagaf</b></li>
                    <li><b>Talitha Galuh Nur Syifa</b></li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
