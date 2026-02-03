import streamlit as st
from stegano import lsb
from PIL import Image
import tempfile
import os

st.set_page_config(page_title="Hide Secret Message", layout="centered")

st.title("🫥 Hide Secret Message in Image")
st.write("Upload an image and hide your secret message inside it.")

# Upload image
uploaded_file = st.file_uploader(
    "Choose an image (PNG recommended)", 
    type=["png", "jpg", "jpeg"]
)

# Secret message input
secret_message = st.text_area("Enter the secret message to hide")

if uploaded_file and secret_message:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_container_width=True)

    if st.button("🔐 Hide Message"):
        try:
            # Save uploaded image temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_input:
                image.save(tmp_input.name)
                input_path = tmp_input.name

            # Output temp file
            output_path = input_path.replace(".png", "_secret.png")

            # Hide message
            secret_img = lsb.hide(input_path, secret_message)
            secret_img.save(output_path)

            st.success("✅ Secret message hidden successfully!")

            # Download button
            with open(output_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download Image with Hidden Message",
                    data=f,
                    file_name="secret_image.png",
                    mime="image/png"
                )

        except Exception as e:
            st.error("❌ Failed to hide message. Use PNG images for best results.")
