import os
from dotenv import load_dotenv

load_dotenv()

try:
    import google.generativeai as genai
except ImportError:
    genai = None

if genai is not None:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    model = None


def analyze_prescription(text):
    if model is None:
        return "Gemini SDK is not available. Please install the required package and set GEMINI_API_KEY."

    prompt = f"""
You are an AI Medical Assistant.

Analyze the following prescription and return a structured report with:
1. Patient Name
2. Doctor Name
3. Medicines
4. Dosage
5. Frequency
6. Duration
7. Doctor Instructions
8. Drug Interaction Warnings
9. Summary

Prescription:
{text}
"""

    response = model.generate_content(prompt)
    return response.text
