import streamlit as st
import cv2
import numpy as np
import tempfile
import os
from ultralytics import YOLO
import moviepy.editor as mpy

# Load YOLO model
MODEL_PATH = "Best.pt"
model = YOLO(MODEL_PATH, task="detect")
# If you have a GPU, you might speed things up by uncommenting the next line:
# model.to('cuda')

def process_video(input_video):
    """Process the video frame-by-frame, run detection, and reassemble video using MoviePy."""
    cap = cv2.VideoCapture(input_video)
    
    # Get video FPS with a fallback value
    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps == 0:
        fps = 30
    fps = int(fps)
    
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    
    if not frames:
        return None
    
    processed_frames = []
    progress_bar = st.progress(0)
    total_frames = len(frames)
    
    # Process frames one by one (with progress feedback)
    for i, frame in enumerate(frames):
        result = model(frame)
        processed_frame = result[0].plot()
        processed_frames.append(processed_frame)
        progress_bar.progress((i + 1) / total_frames)
    
    # Convert frames from BGR (OpenCV) to RGB (MoviePy expects RGB)
    processed_frames_rgb = [cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) for frame in processed_frames]
    
    # Use MoviePy to assemble the video file using H.264 encoding
    output_video_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
    clip = mpy.ImageSequenceClip(processed_frames_rgb, fps=fps)
    clip.write_videofile(output_video_path, codec='libx264', audio=False, verbose=False, logger=None)
    
    return output_video_path

def detect_fire_image(image):
    """Detect fire in an image and return the annotated image."""
    result = model(image)
    return result[0].plot()

def process_cctv(cctv_url):
    st.warning("CCTV stream processing is not implemented yet.")

# Streamlit UI
st.title("🔥 Fire and Smoke Detection System")
st.sidebar.header("Upload Video, Image, or Enter CCTV Link")
option = st.sidebar.radio("Choose an Input", ("Image", "Video", "CCTV"))

if option == "Image":
    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        detected_image = detect_fire_image(image)
        st.image(detected_image, channels="BGR", caption="Processed Image")

elif option == "Video":
    uploaded_video = st.file_uploader("Upload a Video", type=["mp4", "avi"])
    if uploaded_video:
        # Save the uploaded video to a temporary file
        temp_input_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        with open(temp_input_video, "wb") as f:
            f.write(uploaded_video.read())
        
        st.info("🚀 Processing video... Please wait ⏳")
        processed_video_path = process_video(temp_input_video)
        
        if processed_video_path:
            st.success("✅ Video processing complete!")
            # Read the video as bytes and display it in the Streamlit video player
            with open(processed_video_path, 'rb') as f:
                video_bytes = f.read()
            st.video(video_bytes)
        else:
            st.error("❌ Error in video processing. Please try again.")

elif option == "CCTV":
    cctv_url = st.text_input("Enter CCTV Stream URL")
    if st.button("Start CCTV Stream") and cctv_url:
        process_cctv(cctv_url)
