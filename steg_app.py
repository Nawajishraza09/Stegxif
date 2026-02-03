import streamlit as st
from stegano import lsb
from PIL import Image
from PIL.ExifTags import TAGS
import tempfile
import hashlib
import base64
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Steganography Toolkit", layout="centered")
st.title("🕵️‍♂️ Steganography Toolkit")
st.caption("Hide & Extract secret messages securely")

# ---------------- CRYPTO HELPERS ----------------
def derive_key(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()

def encrypt(message: str, password: str) -> str:
    key = derive_key(password)
    data = message.encode()
    encrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])
    return base64.b64encode(encrypted).decode()

def decrypt(encoded: str, password: str) -> str:
    key = derive_key(password)
    encrypted = base64.b64decode(encoded)
    decrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(encrypted)])
    return decrypted.decode(errors="ignore")

# ---------------- EXIF HELPERS ----------------
def extract_exif(image: Image.Image):
    exif = image.getexif()
    if not exif:
        return None

    data = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        data[str(tag)] = str(value)

    return data

# ---------------- UI TABS ----------------
tab1, tab2, tab3 = st.tabs(["🔐 Hide Message", "🔍 Extract Message", "📋 EXIF Data"])

# ======================================================
# 🔐 HIDE MESSAGE
# ======================================================
with tab1:
    st.subheader("Hide a Secret Message")

    uploaded = st.file_uploader("Upload image (PNG recommended)", type=["png", "jpg", "jpeg"])
    secret = st.text_area("Secret Message")
    password = st.text_input("Password", type="password")

    if uploaded and secret and password:
        image = Image.open(uploaded)
        st.image(image, caption="Original Image", width="stretch")

        if st.button("🔐 Hide Message"):
            try:
                encrypted_text = encrypt(secret, password)

                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                    image.save(tmp.name)
                    temp_input = tmp.name

                stego_img = lsb.hide(temp_input, encrypted_text)

                output_path = os.path.join(os.getcwd(), "secret_image.png")
                stego_img.save(output_path)

                with open(output_path, "rb") as f:
                    data = f.read()

                st.success("✅ Message hidden successfully!")
                st.info(f"Saved locally as: {output_path}")

                st.download_button(
                    "⬇️ Download Image",
                    data=data,
                    file_name="secret_image.png",
                    mime="image/png"
                )

                os.remove(temp_input)

            except Exception as e:
                st.error("❌ Failed to hide message. Use PNG images.")

# ======================================================
# 🔍 EXTRACT MESSAGE
# ======================================================
with tab2:
    st.subheader("Extract a Secret Message")

    uploaded = st.file_uploader("Upload image with hidden data", type=["png", "jpg", "jpeg"])
    password = st.text_input("Password", type="password", key="extract")

    if uploaded and password:
        image = Image.open(uploaded)
        st.image(image, caption="Uploaded Image", width="stretch")

        if st.button("🔍 Extract Message"):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                    image.save(tmp.name)
                    temp_path = tmp.name

                hidden = lsb.reveal(temp_path)

                if hidden:
                    message = decrypt(hidden, password)
                    st.success("✅ Hidden Message Found:")
                    st.code(message)
                else:
                    st.warning("⚠️ No hidden data found.")

                os.remove(temp_path)

            except Exception:
                st.error("❌ Wrong password or corrupted image.")

# ======================================================
# 📋 EXIF DATA TAB
# ======================================================
with tab3:
    st.subheader("Image EXIF Metadata Analysis")

    uploaded = st.file_uploader(
        "Upload an image to analyze EXIF metadata",
        type=["jpg", "jpeg", "png"],
        key="exif_upload"
    )

    if uploaded:
        image = Image.open(uploaded)
        st.image(image, caption="Uploaded Image", width="stretch")

        if st.button("📋 Show EXIF Data"):
            exif_data = extract_exif(image)

            if exif_data:
                st.success("✅ EXIF Metadata Found")
                st.json(exif_data)
            else:
                st.warning("⚠️ No EXIF metadata found in this image.")

# Sidebar Instructions
st.divider()
st.sidebar.header("How to Use")
st.sidebar.markdown("""
1. Select the different tabs to perform action.
2. Upload a **PNG image** (best for LSB) by Clicking on **Browse File** button.
3. Type the content which you want to hide.
4. Provide basic **Password** (e.g 1234, boby, etc...)
5. Click **Hide Message** to hide the message.
6. Same for extractimg the message.
7. Upload the image, type the **Password**.
8. Click **Extract Message** to reveal secret messages.
9. In **EXIF Data** upload the file.
10. Click **Show EXIF Data** to analyze EXIF data.
11. JPEG images may not contain LSB data due to compression.
""")
