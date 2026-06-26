import os
import re

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency
    load_dotenv = None

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover - optional dependency
    genai = None


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
    api_key = os.getenv("GEMINI_API_KEY")
    if genai is not None and api_key:
        try:
            # configure the official Google Generative AI client
            try:
                genai.configure(api_key=api_key)
            except Exception:
                # some client versions use client.configure
                try:
                    from google.generativeai import client as genai_client

                    genai_client.configure(api_key=api_key)
                except Exception:
                    pass

            response = genai.chat.completions.create(
                model=os.getenv("GEMINI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": "You analyze prescription text and return a concise medical summary."},
                    {
                        "role": "user",
                        "content": f"Analyze this prescription and return: Medicine, Dosage, Frequency, Duration, Condition, and Precautions. Prescription: {text}",
                    },
                ],
                temperature=0.2,
            )

            # Response shapes vary between client versions; try a few safe access patterns.
            content = None
            # 1) Common dict-style: response['candidates'][0]['content']
            try:
                if isinstance(response, dict):
                    candidates = response.get("candidates") or []
                    if candidates:
                        first = candidates[0]
                        if isinstance(first, dict):
                            content = first.get("content") or first.get("message", {}).get("content")
                        else:
                            content = str(first)
            except Exception:
                content = None

            # 2) Object-style used by some wrappers: response.choices[0].message.content
            if not content:
                try:
                    content = response.choices[0].message.content
                except Exception:
                    pass

            # 3) Some clients return top-level 'content' or string conversion
            if not content:
                content = getattr(response, "content", None) or (str(response) if response is not None else None)

            if content:
                return content.strip()
        except Exception:
            pass

    return _extract_local_analysis(text)