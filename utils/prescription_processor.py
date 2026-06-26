import os
import re

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency
    load_dotenv = None

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - optional dependency
    OpenAI = None


if load_dotenv is not None:
    load_dotenv()


def _extract_local_analysis(text):
    cleaned_text = (text or "").strip()
    if not cleaned_text:
        return "No prescription details were provided."

    medicine = "Unknown"
    dosage = "Not specified"
    frequency = "Not specified"
    duration = "Not specified"
    condition = "Not specified"

    words = cleaned_text.split()
    if words:
        medicine = words[0]

    dosage_match = re.search(r"(\d+(?:\.\d+)?)\s*(mg|mcg|g|ml|tablet|tablets|capsule|capsules)", cleaned_text, re.IGNORECASE)
    if dosage_match:
        dosage = dosage_match.group(0)

    frequency_match = re.search(r"(once|twice|thrice|daily|every\s+day|every\s+\d+\s*hours|morning|evening|night)", cleaned_text, re.IGNORECASE)
    if frequency_match:
        frequency = frequency_match.group(0)

    duration_match = re.search(r"for\s+(\d+\s*(day|days|week|weeks|month|months))", cleaned_text, re.IGNORECASE)
    if duration_match:
        duration = duration_match.group(1)

    condition_match = re.search(r"for\s+([a-zA-Z\s]+)$", cleaned_text, re.IGNORECASE)
    if condition_match:
        condition = condition_match.group(1).strip()

    return f"""Prescription Analysis Report

Prescription: {cleaned_text}

Medicine: {medicine}
Dosage: {dosage}
Frequency: {frequency}
Duration: {duration}
Condition: {condition}

Precautions:
- Follow doctor's instructions
- Take medicines on time
- Complete the full course
"""


def process_prescription(text):
    api_key = os.getenv("OPENAI_API_KEY")
    if OpenAI is not None and api_key:
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {
                        "role": "system",
                        "content": "You analyze prescription text and return a concise medical summary.",
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this prescription and return: Medicine, Dosage, Frequency, Duration, Condition, and Precautions. Prescription: {text}",
                    },
                ],
                temperature=0.2,
            )
            content = response.choices[0].message.content.strip()
            if content:
                return content
        except Exception:
            pass

    return _extract_local_analysis(text)