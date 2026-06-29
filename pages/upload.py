import os
import streamlit as st

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def upload_prescription():
    st.title("📤 Upload Prescription")

    uploaded_file = st.file_uploader(
        "Choose a prescription image or PDF",
        type=["png", "jpg", "jpeg", "pdf"],
    )

    if uploaded_file is not None:
        safe_name = uploaded_file.name.replace(" ", "_")
        save_path = os.path.join(UPLOAD_FOLDER, safe_name)

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("Prescription uploaded successfully ✅")

        if save_path.lower().endswith((".png", ".jpg", ".jpeg")):
            st.image(save_path, caption="Uploaded Prescription", use_container_width=True)
        else:
            st.info("PDF uploaded. OCR will try to extract text from it.")

        return save_path

    return None
