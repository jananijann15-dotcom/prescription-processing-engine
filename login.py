import streamlit as st


# Demo login credentials
USERNAME = "admin"
PASSWORD = "admin123"


def login():

    st.title("🔐 AI Prescription System Login")

    st.markdown("### Please login to continue")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        login_btn = st.button("Login")

    with col2:
        clear_btn = st.button("Clear")

    if clear_btn:
        st.rerun()

    if login_btn:

        if username == USERNAME and password == PASSWORD:

            st.session_state["logged_in"] = True
            st.success("Login Successful ✅")
            st.rerun()

        else:
            st.error("Invalid Username or Password ❌")