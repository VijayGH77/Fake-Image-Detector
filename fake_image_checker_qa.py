import streamlit as st
import requests
import base64
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_USER = os.getenv("API_USER")
API_SECRET = os.getenv("API_SECRET")

# App title and instructions
st.set_page_config(page_title="Fake Image Detection - Dev", layout="centered")
st.title("🧪Fake Image Detection App: DEV")
st.markdown("Upload an image to check if it may be **AI-generated or manipulated**.")

# File uploader
uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="📷 Uploaded Image", use_container_width=True)
    st.success("✅ Image uploaded successfully.")

    with st.spinner("🧠 Running fake image detection..."):
        try:
        # Save uploaded file
             with open("temp.jpg", "wb") as f:
                 f.write(uploaded_file.read())

        # Prepare request
             url = "https://api.sightengine.com/1.0/check.json"
             params = {
                 "models": "deepfake",
                 "api_user": API_USER,
                 "api_secret": API_SECRET,
             }

             files = {"media": open("temp.jpg", "rb")}
             response = requests.post(url, files=files, data=params)
             result = response.json()

             # Display raw API response
            #  if st.checkbox("Show API Raw Response (for Developers)"):
            #      st.subheader("🧾 API Raw Response")
            #      st.json(result)

             # Display detection result
             if result.get("status") == "success" and "type" in result and "deepfake" in result["type"]:
                 score = result["type"]["deepfake"]
                 st.success(f"✅ Deepfake Confidence Score: {score * 100:.0f}% (0% = Real, 100% = Fake)")
             elif result.get("status") == "success":
                 st.warning("⚠️ Detection result is incomplete or the image looks real.")
             else:
                 st.error("❌ Error: Unexpected API response.")

        except Exception as e:
             st.error(f"❌ API Error: {e}")

else:
    st.info("👆 Please upload an image file to begin.")
