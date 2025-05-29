from dotenv import load_dotenv
import os

load_dotenv()  # This loads the .env file

API_USER = os.getenv("523065712")
API_SECRET = os.getenv("ZXRd7UaQhkqAcstYTyU4PRA4sTDgXzxZ")

import streamlit as st
import requests

# App title
st.title("🕵️‍♂️ Fake Image Detection App")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "HEIC"])

# Check if image is uploaded
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    st.success("Image uploaded successfully!")

    # Save uploaded file temporarily
    with open("temp.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.markdown("🔍 *Running fake image detection...*")

    # 🔐 Your Sightengine credentials
    api_user = "523065712"      # Replace this
    api_secret = "ZXRd7UaQhkqAcstYTyU4PRA4sTDgXzxZ"  # Replace this

    # Send image to Sightengine
    url = "https://api.sightengine.com/1.0/check.json"
    files = {'media': open("temp.jpg", 'rb')}
    params = {
        'models': 'deepfake',
        'api_user': "523065712",
        'api_secret': "ZXRd7UaQhkqAcstYTyU4PRA4sTDgXzxZ"
    }

    response = requests.post(url, files=files, data=params)
    result = response.json()
    st.json(result)


    # 🧾 Display results
    st.markdown("🔍 *Running fake image detection...*")

    # Optional: show raw JSON for debugging
    # st.json(result)

    if result.get("status") == "success" and "type" in result and "deepfake" in result["type"]:
        score = result["type"]["deepfake"]
        st.success(f"✅ Deepfake detection score: {score:.2f}")

        st.progress(score)

        if score > 0.7:
            st.error("⚠️ This image is likely AI-generated or fake!")
        else:
            st.success("🎉 This image appears to be authentic.")
    else:
        st.error("❌ Unable to process image or API returned an error.")

