import streamlit as st
from utils.prescription_processor import process_prescription

st.set_page_config(
    page_title="Prescription Processing Engine",
    page_icon="💊"
)

st.title("💊 Prescription Processing Engine")
st.write("AI Powered Prescription Analysis System")

user_input = st.chat_input("Enter Prescription Details")

if user_input:

    with st.chat_message("user"):
        st.write(user_input)

    result = process_prescription(user_input)

    with st.chat_message("assistant"):
        st.write(result)