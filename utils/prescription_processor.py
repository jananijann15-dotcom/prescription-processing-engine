import json
import os
import re
import urllib.request
import urllib.error

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency
    load_dotenv = None


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


def _call_gemini_api(text, api_key, model_name):
    if not api_key:
        return None

    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "Analyze this prescription and return: Medicine, Dosage, Frequency, Duration, "
                            "Condition, and Precautions. Prescription: "
                            f"{text}"
                        )
                    }
                ]
            }
        ]
    }

    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            body = response.read().decode("utf-8")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
        return None

    try:
        data = json.loads(body)
    except Exception:
        return None

    candidates = data.get("candidates") or []
    if not candidates:
        return None

    content_parts = candidates[0].get("content", {}).get("parts", [])
    if not content_parts:
        return None

    texts = []
    for part in content_parts:
        if isinstance(part, dict):
            text_value = part.get("text")
            if text_value:
                texts.append(text_value)

    return "\n".join(texts).strip() or None


def process_prescription(text):
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    content = _call_gemini_api(text, api_key, model_name)
    if content:
        return content

    return _extract_local_analysis(text)