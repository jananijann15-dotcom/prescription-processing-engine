import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_prescription(text):

    prompt = f"""
You are an AI Medical Assistant.

Analyze the following prescription.

Provide:

1. Patient Name
2. Doctor Name
3. Medicines
4. Dosage
5. Precautions
6. Summary

Prescription:

{text}
"""

    response = model.generate_content(prompt)

    return response.text