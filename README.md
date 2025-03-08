---
title: Fire Detection App
emoji: 📈
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.42.2
app_file: app.py
pinned: false
license: apache-2.0
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# AI-Powered Fire & Smoke Detection System
## Overview

This project leverages the state-of-the-art YOLOv8 deep learning model to detect fire and smoke in images and videos. By combining powerful object detection with a user-friendly Streamlit dashboard and deployment on Hugging Face Spaces, the system provides a robust solution for early fire hazard detection.

The model was trained on a diverse dataset from [Roboflow’s FireSmoke Dataset](https://universe.roboflow.com/catargiuconstantin/firesmokedataset) which includes over 46,000 images captured in various conditions—day and night, urban and rural settings. This diversity ensures that the system can be deployed in a wide range of environments.

## Setup and Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Aarishbangash/AI-Powered-Fire-Smoke-Detection-System.git
   cd AI-Powered-Fire-Smoke-Detection-System

2. **Set Up the Environment and Install Dependencies:**

- **Create and activate a virtual environment:**
  ```bash
  python -m venv venv
  # On Linux/Mac:
  source venv/bin/activate
  # On Windows:
  venv\Scripts\activate

Install the required packages:

pip install -r requirements.txt

Run the App:

streamlit run app.py
