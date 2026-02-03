# 🕵️‍♂️ Steganography Toolkit (Streamlit)
A Python-based Steganography & Image Forensics Web App built with Streamlit.
This tool allows users to hide secret messages inside images, extract hidden messages,
and analyze EXIF metadata, all from a single, user-friendly interface.

# 🚀 Features
1. 🔐 Hide Message
- Hide secret text inside images using LSB steganography
- Password-protected message encryption
- Supports PNG (recommended), JPG, JPEG
- Output image saved locally and downloadable

2. 🔍 Extract Message
- Extract hidden messages from steganographic images
- Password-based decryption
- Detects absence of hidden data gracefully

3. 📋 EXIF Metadata Analysis
- View EXIF metadata of images
- Detects:
    Camera make & model
    Date & time
    GPS coordinates (if present)
    Editing software
- Helps identify privacy leaks

4. 🧹 Secure Handling
- Temporary files are auto-deleted
- No hard-coded file paths
- Browser-safe file handling

# 🛠️ Software/Libraries
1. Python 3.8+
2. Streamlit – Web framework
3. Stegano – LSB steganography
4. Pillow (PIL) – Image processing
5. Hashlib + Base64 – Password-based encryption

# 📦 Installation
1️⃣ Clone the repository
- git clone https://github.com/Nawajishraza09/Stegxif.git
- cd Stegxif

2️⃣ Install dependencies
- pip install -r requirements.txt

▶️ Run the Application
- streamlit run steg_app.py -> after that it will automatically open on browser "http://localhost:8501"
- There is two different files also available for two different task for "Hiding" & "Extracting" separately.

# 🔐 How Encryption Works
1. Password is converted into a SHA-256 key
2. Secret message is encrypted using XOR encryption
3. Encrypted data is encoded using Base64
4. Stored safely using LSB steganography
5. Same password is required for extraction
6. Note - ⚠️ This encryption is for educational use, for production use, AES/Fernet is recommended.

# 📷 Supported Image Formats
| Format | Steganography | EXIF Metadata |
| ------ | ------------- | ------------- |
| PNG    | ✅ Best        | ❌ Usually No  |
| JPG    | ⚠️ Limited    | ✅ Yes         |
| JPEG   | ⚠️ Limited    | ✅ Yes         |

# 🎓 Academic Relevance

1. This project demonstrates:
- Information hiding techniques
- Image forensics & metadata analysis
- Secure file handling
- Python web application development

2. Suitable for:
- Final-year projects
- Cybersecurity demos
- Digital forensics coursework
