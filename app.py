import streamlit as st
from PIL import Image
import pillow_heif
import zipfile
import io

# Pillow-HEIFの設定
pillow_heif.register_heif_opener()

def convert_heif_to_jpeg(file):
    # HEIF/HEICファイルを読み込む
    image = Image.open(file)
    return image

st.title("HEIF/HEIC to JPEG Converter")

# 複数のHEIF/HEICファイルをアップロード
uploaded_files = st.file_uploader("Drop HEIF/HEIC files", type=["heif", "heic"], accept_multiple_files=True)
st.write("ドラッグ&ドロップで複数ファイルをアップロードできます")

if uploaded_files:
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for uploaded_file in uploaded_files:
            image = convert_heif_to_jpeg(uploaded_file)
            
            # JPEGファイルに変換
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format="JPEG", quality=95)
            img_byte_arr.seek(0)
            
            # ファイル名を変更してZIPに追加
            zip_file.writestr(f"{uploaded_file.name.split('.')[0]}.jpeg", img_byte_arr.read())

    zip_buffer.seek(0)
    
    # ZIPファイルをダウンロード
    st.download_button(
        label="Download ZIP",
        data=zip_buffer,
        file_name="converted_images.zip",
        mime="application/zip",
    )

# カスタムCSSとHTMLを追加してフッターを作成
footer = """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        right: 0;
        width: 100%;
        text-align: right;
        padding: 10px;
        font-size: 12px;
        color: #555;
    }
    </style>
    <div class="footer">
    <p>© 2024 ICT Lab.</p>
    </div>
    """

st.markdown(footer, unsafe_allow_html=True)