# 🧠 Brain Tumor Segmentation App

## Features
- Upload brain MRI scans
- Visualize and segment tumors
- Download results

## How to Run

1. Clone the repo:
   ''' git clone https://github.com/syarkK/TumorDetection-Segmentation
cd brain-tumor-segmentation-gui '''
2. Install dependencies: 
   ''' pip install -r requirements.txt ''' 
3. Launch the app:
   ''' streamlit run app.py '''


## 💡 Note on Model Files
This app uses two pre-trained models:
- Classification (Keras): downloaded from [Hugging Face](https://huggingface.co/whattheduckk/Classification)
- Segmentation (PyTorch): downloaded from [Hugging Face](https://huggingface.co/whattheduckk/Segmentation)

The models are **automatically downloaded** at runtime using the `huggingface_hub` package.


## Notes
- Make sure the model file is in `model/`.
- Supported formats: JPG, PNG.