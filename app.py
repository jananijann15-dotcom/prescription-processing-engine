import streamlit as st

from pages.login import login
from pages.dashboard import dashboard
from pages.upload import upload_prescription
from utils.ocr import extract_text
from utils.gemini import analyze_prescription
from utils.pdf import generate_pdf
from utils.database import insert_prescription, create_table
from pages.history import show_history


# DB create
create_table()


st.set_page_config(page_title="AI Prescription System", layout="wide")


# Session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "extracted_text" not in st.session_state:
    st.session_state["extracted_text"] = ""

if "ai_result" not in st.session_state:
    st.session_state["ai_result"] = ""


# LOGIN
if not st.session_state["logged_in"]:
    login()

else:

    st.sidebar.title("Navigation")

    menu = st.sidebar.radio(
        "Go to",
        ["Dashboard", "Upload Prescription", "History"]
    )

    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()


    # DASHBOARD
    if menu == "Dashboard":
        dashboard()


    # UPLOAD + AI PIPELINE
    elif menu == "Upload Prescription":

        st.title("📤 Upload & Analyze Prescription")

        image_path = upload_prescription()

        if image_path:

            st.subheader("🔍 OCR Extracting Text...")
            text = extract_text(image_path)

            st.text_area("Extracted Text", text, height=200)

            st.subheader("🤖 AI Analysis (Gemini)")

            result = analyze_prescription(text)

            st.text_area("AI Result", result, height=300)

            # Save to DB
            st.subheader("💾 Saving to Database...")

            insert_prescription(
                patient_name="Unknown",
                doctor_name="Unknown",
                medicines="Extracted by AI",
                dosage="Auto",
                precautions="Auto",
                summary=result,
                image_path=image_path
            )

            st.success("Saved Successfully ✅")

            # PDF generate
            pdf_path = generate_pdf(result)

            st.success("PDF Generated ✅")

            with open(pdf_path, "rb") as f:
                st.download_button(
                    "⬇ Download PDF",
                    f,
                    file_name="prescription_report.pdf"
                )


    # HISTORY
    elif menu == "History":
        show_history()