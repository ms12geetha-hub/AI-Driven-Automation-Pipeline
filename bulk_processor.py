import os
import glob
import json
import streamlit as st
from ocr import extract_text
from extraction import extract_gstin, extract_pan, extract_invoice_date, extract_amount
from validator import validate_fields
from evaluation import evaluate_vendor
from ai_validator import ai_validate_invoice

# Folder containing invoices
INVOICE_DIR = "sample_data"

st.title("Vendor evaluation - Bulk Processing and Finalization-SSH_018")
st.write("Upload invoices (PDF/PNG/JPG) or use sample_data folder for bulk processing.")

uploaded_files = st.file_uploader(
    "Upload invoice PDFs/images",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# Save uploaded files to temp folder
file_paths = []
if uploaded_files:
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    for f in uploaded_files:
        path = os.path.join(temp_dir, f.name)
        with open(path, "wb") as out:
            out.write(f.read())
        file_paths.append(path)
else:
    file_paths = glob.glob(os.path.join(INVOICE_DIR, "*.pdf")) + \
                 glob.glob(os.path.join(INVOICE_DIR, "*.png")) + \
                 glob.glob(os.path.join(INVOICE_DIR, "*.jpg")) + \
                 glob.glob(os.path.join(INVOICE_DIR, "*.jpeg"))

def process_bulk(files):
    results = []

    for file in files:
        st.info(f"Processing: {os.path.basename(file)}")

        # Step 1: OCR extraction
        text = extract_text(file)

        # Step 2: Field extraction
        extracted_data = {
            "gstin": extract_gstin(text),
            "pan": extract_pan(text),
            "invoice_date": extract_invoice_date(text),
            "amount": extract_amount(text),
            "vendor_name": ""  # optional, leave blank if not present
        }

        # Step 3: Rule-based evaluation
        evaluation = evaluate_vendor(extracted_data)

        # Step 4: AI semantic check
        corrected_text = f"""
        Vendor Name: {extracted_data.get('vendor_name', '')}
        GSTIN: {extracted_data.get('gstin', '')}
        PAN: {extracted_data.get('pan', '')}
        Invoice Date: {extracted_data.get('invoice_date', '')}
        Amount: {extracted_data.get('amount', '')}
        """
        ai_result = ai_validate_invoice(extracted_data, corrected_text)

        # Step 5: Combine scores
        ai_conf = ai_result.get("ai_confidence", 50)
        rule_conf = evaluation.get("confidence_score", 100)
        final_score = int(0.6 * rule_conf + 0.4 * ai_conf)

        # Step 6: Determine final vendor status
        if final_score >= 90:
            final_status = "Approved"
            final_recommendation = "Auto-approved for payment"
        elif final_score >= 70:
            final_status = "Needs Review"
            final_recommendation = "Manual review recommended before payment"
        else:
            final_status = "Rejected"
            final_recommendation = "Vendor resubmission required"

        # Numeric amount
        numeric_amount = None
        if extracted_data.get("amount"):
            amt_str = str(extracted_data["amount"]).replace(",", "").replace("₹", "").strip()
            try:
                numeric_amount = float(amt_str)
            except:
                numeric_amount = 0.0

        results.append({
            "file_name": os.path.basename(file),
            "extracted_data": extracted_data,
            "evaluation": {
                "confidence_score": final_score,
                "vendor_status": final_status,
                "ai_recommendation": final_recommendation,
                "issues": evaluation.get("issues", [])
            },
            "ai_insights": ai_result,
            "numeric_amount": numeric_amount,
            "final_vendor_score": final_score,
            "price_score": None,
            "price_rank": None
        })

    # Step 7: Price ranking
    sorted_by_price = sorted([r for r in results if r["numeric_amount"] is not None],
                             key=lambda x: x["numeric_amount"])
    for idx, r in enumerate(sorted_by_price, 1):
        r["price_rank"] = idx
        r["price_score"] = int(100 - ((idx - 1) / len(sorted_by_price) * 50))  # scale 100-50

    # Step 8: Best vendor suggestion
    if results:
        best_vendor = max(results, key=lambda x: (x["final_vendor_score"], -x.get("numeric_amount", 0)))
        for r in results:
            r["best_vendor_suggestion"] = (r["file_name"] == best_vendor["file_name"])
            if r["best_vendor_suggestion"]:
                r["best_vendor_reason"] = f"Highest combined score ({r['final_vendor_score']}) and lowest invoice amount ({r.get('numeric_amount')})"

    return results

if file_paths:
    output = process_bulk(file_paths)
    st.subheader("Bulk Processing Results")
    st.json(output)
else:
    st.warning("No files found in sample_data folder or uploaded.")
