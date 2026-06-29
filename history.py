import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "database/prescription.db"


def show_history():

    st.title("📜 Prescription History")

    conn = sqlite3.connect(DB_PATH)

    try:
        df = pd.read_sql_query(
            "SELECT * FROM prescriptions ORDER BY id DESC",
            conn
        )

        if df.empty:
            st.info("No prescriptions found.")
        else:
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")

    finally:
        conn.close()