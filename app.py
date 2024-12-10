import os
import streamlit as st
import PIL.Image
import google.generativeai as genai

# Configure Gemini API Key
genai.configure(api_key=st.secrets["google"]["api_key"])  # Replace with your actual Gemini API key

# Set Streamlit page configuration
st.set_page_config(page_title="Drishti ज्ञान Image Analyzer", layout="centered", page_icon="📷")

# Title and Description
st.title("📷 Drishti ज्ञान (Image Analyzer)")
st.write("Upload an image to get insights powered by ज्ञान AI.")

# Sidebar for language selection
st.sidebar.title("Language Settings")
language = st.sidebar.radio("Choose Response Language:", ["English", "Hindi", "Marathi"])

# Upload Image Section
st.write("### Upload an image to analyze:")
uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save and display the uploaded image
    with open("uploaded_image.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    image = PIL.Image.open("uploaded_image.jpg")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Analyze the image using Gemini API
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
