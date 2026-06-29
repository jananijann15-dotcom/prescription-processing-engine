# AI Prescription Processing System

A Streamlit-based application for uploading prescription images/PDFs, extracting text with OCR, analyzing prescriptions with Gemini AI, and generating downloadable PDF reports.

## Features
- Login page
- Dashboard
- Upload prescription (image/PDF)
- OCR text extraction
- Gemini AI analysis
- Medicine summary and instructions
- History storage in SQLite
- PDF report generation

## Setup
1. Install dependencies:
   pip install -r requirements.txt
2. Add your Gemini API key to the .env file:
   GEMINI_API_KEY=your_key_here
3. Run the app:
   streamlit run app.py
