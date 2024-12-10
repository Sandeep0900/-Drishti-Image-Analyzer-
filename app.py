import os
import streamlit as st
import PIL.Image
import google.generativeai as genai
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

# Configure Gemini API Key
genai.configure(api_key=st.secrets["google"]["api_key"])  # Replace with your actual Gemini API key

# Set Streamlit page configuration
st.set_page_config(page_title="Drishti ज्ञान Image Analyzer", layout="centered", page_icon="📷")

# Title and Description
st.title("📷 Drishti ज्ञान (Image Analyzer)")
st.write("Upload or click a photo to get insights powered by ज्ञान AI.")

# Sidebar for language selection
st.sidebar.title("Language Settings")
language = st.sidebar.radio("Choose Response Language:", ["English", "Hindi", "Marathi"])

# Webcam functionality to capture live photo
st.write("### Capture a photo using your webcam:")
webrtc_ctx = webrtc_streamer(key="example", video_transformer_factory=VideoTransformerBase)

if webrtc_ctx.video_frame is not None:
    # Capture image when a frame is available from webcam
    frame = webrtc_ctx.video_frame
    image = PIL.Image.fromarray(frame.to_ndarray(format="bgr24"))
    st.image(image, caption="Captured Image", use_column_width=True)

    # Analyze the captured image using Gemini API
    st.write("### Analyzing the Image...")
    prompt = f"Describe the content of this image in {language.lower()}."

    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        response = model.generate_content([prompt, image])

        if response and hasattr(response, "text"):
            st.write(f"### Gemini AI Response in {language}:")
            st.success(response.text)
        else:
            st.error("Failed to generate a response. Please try again.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Footer
st.write("Made by **Sandeep Sharma**")
