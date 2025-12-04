import re
from datetime import datetime


def find_pattern(text: str, patterns: list):
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return m.group(1) if m.group(1) else m.group(0)
    return None


def extract_date(text: str):
    match = re.search(r"(\d{2}/\d{2}/\d{4})", text)
    return match.group(1) if match else None


def extract_amount(text: str):
    match = re.search(r"(\d+[\.,]?\d*)", text)
    if match:
        return float(match.group(1).replace(",", ""))  
    return None
