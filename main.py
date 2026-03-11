from ocr import extract_text
from validator import extract_gstin, extract_pan, extract_invoice_date, extract_amount, validate_fields

FILE_PATH = "sample_data/invoice1.pdf"  # OR invoice1.pdf

text = extract_text(FILE_PATH)

print("\n--- OCR TEXT ---\n")
print(text)

data = {
    "gstin": extract_gstin(text),
    "pan": extract_pan(text),
    "invoice_date": extract_invoice_date(text),
    "amount": extract_amount(text)
}

print("\n--- Extracted Data ---\n")
print(data)

validation_result = validate_fields(data)

print("\n--- Validation Result ---\n")
print(validation_result)
