import pytesseract
from PIL import Image
import os
import pdfplumber
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Normalize OCR text globally for image OCR
def normalize_ocr_text(text: str) -> str:
    text = text.upper()
    replacements = {
        "L": "1",
        "I": "1",
        "O": "0",
        "Z": "2",
        "S": "5",
        "TOTA1": "TOTAL",
        "OTAL": "TOTAL"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def extract_text_from_image(img_path):
    img = Image.open(img_path).convert("L")
    raw_text = pytesseract.image_to_string(img, config="--psm 6")
    return normalize_ocr_text(raw_text)

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text  # PDFs usually clean; no global normalization

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".png", ".jpg", ".jpeg"]:
        return extract_text_from_image(file_path)
    else:
        raise ValueError("Unsupported file type")
