def evaluate_vendor(extracted_data):
    score = 100
    issues = []

    if not extracted_data.get("gstin"):
        score -= 40
        issues.append("GSTIN missing or invalid")

    if not extracted_data.get("pan"):
        score -= 20
        issues.append("PAN missing or invalid")

    if not extracted_data.get("invoice_date"):
        score -= 10
        issues.append("Invoice date missing")

    if not extracted_data.get("amount"):
        score -= 20
        issues.append("Invoice amount missing")

    if score >= 90:
        status = "Approved"
        recommendation = "Auto-approved for payment"
    elif score >= 70:
        status = "Needs Review"
        recommendation = "Manual review recommended before payment"
    else:
        status = "Rejected"
        recommendation = "Vendor resubmission required"

    return {
        "vendor_status": status,
        "confidence_score": score,
        "issues": issues,
        "ai_recommendation": recommendation
    }
