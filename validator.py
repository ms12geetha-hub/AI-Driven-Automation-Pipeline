import re

# ---------- GSTIN ----------



def extract_gstin(text):
    if not text:
        return None

    text = text.upper()

    # Find 15-character alphanumeric candidates
    candidates = re.findall(r"\b[A-Z0-9]{15}\b", text)

    for gst in candidates:
        gst_list = list(gst)

        # FIX ONLY POSITION 14 (index 13)
        if gst_list[13] == "2":   # OCR mistake
            gst_list[13] = "Z"

        fixed = "".join(gst_list)

        # Strict GSTIN validation
        pattern = r"\d{2}[A-Z]{5}\d{4}[A-Z]\dZ[A-Z0-9]"
        if re.fullmatch(pattern, fixed):
            return fixed

    return None




# ---------- PAN ----------
def normalize_pan_candidate(raw):
    raw = raw.upper()
    mapping = {"L":"E","I":"1","O":"0"}
    return "".join([mapping.get(c,c) for c in raw])

def extract_pan(text):
    text_norm = text.upper()
    text_norm = normalize_pan_candidate(text_norm)

    # Candidates after PAN label
    candidates = re.findall(r"PAN[:\s]*([A-Z0-9]{9,11})", text_norm)
    if not candidates:
        candidates = re.findall(r"\b[A-Z0-9]{10}\b", text_norm)

    for cand in candidates:
        pattern = r"[A-Z]{5}\d{4}[A-Z]"
        if re.fullmatch(pattern, cand):
            return cand

    return None

# ---------- DATE ----------
def extract_invoice_date(text):
    match = re.search(r"\b\d{2}[/-]\d{2}[/-]\d{4}\b", text)
    return match.group() if match else None

# ---------- AMOUNT ----------
def extract_amount(text):
    pattern = r"(?:₹|RS\.?)?\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})"
    match = re.findall(pattern, text.upper())
    if match:
        return match[-1].strip()
    return None

# ---------- VALIDATION ----------
def validate_fields(data):
    errors = []
    if not data.get("gstin"):
        errors.append("GSTIN not found")
    if not data.get("pan"):
        errors.append("PAN not found")
    if not data.get("invoice_date"):
        errors.append("Invoice date missing")
    if not data.get("amount"):
        errors.append("Invoice amount missing")
    return {"is_valid": len(errors)==0, "errors": errors}
