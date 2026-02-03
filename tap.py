import streamlit as st
from stegano import lsb
from PIL import Image
from PIL.ExifTags import TAGS
import tempfile

# App Configuration
st.set_page_config(page_title="Image Data Reveal", layout="centered")

st.title("🕵️‍♂️ Image Hidden Data Reveal")
st.write("Upload an image to check for hidden steganographic data or metadata.")

uploaded_file = st.file_uploader(
    "Choose an image file...", 
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    col1, col2 = st.columns(2)

    # -------- LSB EXTRACTION --------
    with col1:
        if st.button("🔍 Extract Hidden Text (LSB)"):
            with st.spinner("Analyzing pixels..."):
                try:
                    # Save image temporarily (IMPORTANT FIX)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                        image.save(tmp.name)
                        hidden_message = lsb.reveal(tmp.name)

                    if hidden_message:
                        st.success("Hidden Message Found:")
                        st.code(hidden_message)
                    else:
                        st.warning("No hidden text detected using LSB.")

                except Exception as e:
                    st.error("LSB extraction failed. Use PNG images only.")

    # -------- METADATA EXTRACTION --------
    with col2:
        if st.button("📋 View Image Metadata"):
            exif_data = image.getexif()
            if exif_data:
                metadata = {}
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    metadata[tag] = value
                st.json(metadata)
            else:
                st.warning("No EXIF metadata found.")

# Sidebar Instructions
st.divider()
st.sidebar.header("How to Use")
st.sidebar.markdown("""
1. Upload a **PNG image** (best for LSB).
2. Click **Extract Hidden Text** to reveal secret messages.
3. Click **View Metadata** to analyze EXIF data.
4. JPEG images may not contain LSB data due to compression.
""")
