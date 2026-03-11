import re
from validator import normalize_pan_candidate, extract_gstin, extract_pan, extract_invoice_date, extract_amount, validate_fields



def extract_pan(text):
    """
    Extract PAN from the text
    """
    text = text.upper()
    candidates = re.findall(r"PAN[:\s]*([A-Z0-9]{9,11})", text)

    # Debugging: Print the candidates
    print(f"PAN candidates: {candidates}")

    for cand in candidates:
        fixed = normalize_pan_candidate(cand)

        # Debugging: Print the normalized PAN candidate
        print(f"Normalized PAN candidate: {fixed}")

        match = re.search(r"\b[A-Z]{5}\d{4}[A-Z]\b", fixed)
        if match:
            return match.group()

    return None


def extract_invoice_date(text):
    pattern = r"\b\d{2}[/-]\d{2}[/-]\d{4}\b"
    match = re.search(pattern, text)
    return match.group() if match else None


def extract_amount(text):
    """
    Handles:
    ₹45,230.00
    45,230.00
    Rs. 45230
    """
    pattern = r"(₹|Rs\.?)?\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})"
    matches = re.findall(pattern, text.replace("₹", "₹ "))
    amounts = re.findall(r"\d{1,3}(?:,\d{3})*(?:\.\d{2})", text)

    if amounts:
        return amounts[-1]  # take LAST amount (usually total)
    return None