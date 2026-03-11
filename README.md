# 🧾 Vendor evaluation - Bulk Processing and Finalization-SSH_018

## 📌 Problem Statement

Organizations process large volumes of vendor invoices daily. Manual validation of invoices is:

* Time-consuming
* Error-prone
* Costly
* Vulnerable to fraud and compliance issues

Finance teams spend significant effort verifying GSTIN, PAN, invoice dates, and amounts before approving payments.

---

## 💡 Solution Overview

This solution automates **end-to-end vendor invoice validation** using a **hybrid approach** that combines:

* **Rule-based validation** for compliance and accuracy
* **AI-based semantic validation** for contextual understanding
* **Automated vendor scoring and ranking** for decision-making

The system converts unstructured invoices (PDF/Image) into **trusted, AI-driven payment decisions**.

---

## 🏗️ System Architecture (High Level)

```
Invoice (PDF / Image)
        ↓
OCR Extraction
        ↓
Field Extraction (GSTIN, PAN, Date, Amount)
        ↓
Rule-Based Validation
        ↓
AI Semantic Validation (LLM)
        ↓
Score Aggregation
        ↓
Vendor Ranking & Recommendation
        ↓
Final Decision (Approve / Review / Reject)
```

---
## Tech Stack
- Python 3.10
- Streamlit (UI)
- OCR (Tesseract / PaddleOCR)
- Rule Engine (Custom Python validators)
- Azure OpenAI (Semantic Invoice Validation)

## How to Run
```bash
pip install -r requirements.txt
streamlit run bulk_processor.py
--------------

## ⚙️ Key Components

### 1. OCR Module

* Extracts raw text from invoice PDFs or images
* Handles noisy and scanned documents

### 2. Field Extraction Engine

* Identifies and extracts:

  * GSTIN
  * PAN
  * Invoice Date
  * Invoice Amount
* Designed to work across different invoice formats

### 3. Rule-Based Validator

* Validates:

  * GSTIN format
  * PAN format
  * Date presence
  * Amount validity
* Produces a **confidence score** and issue list

### 4. AI Semantic Validator

* Uses LLM (e.g., Azure OpenAI) to:

  * Understand invoice context
  * Cross-verify extracted fields
  * Detect inconsistencies or missing data
* Outputs AI confidence and insights

### 5. Vendor Evaluation Engine

* Combines:

  * Rule-based score
  * AI confidence score
* Determines:

  * Vendor status (Approved / Needs Review / Rejected)
  * Payment recommendation

### 6. Price Ranking & Best Vendor Selection

* Ranks vendors based on invoice amount
* Suggests **best vendor** using:

  * Highest confidence score
  * Lowest cost

---

## 🖥️ User Interface

* Built using **Streamlit**
* Supports:

  * Single invoice upload
  * Bulk invoice processing
* Displays:

  * Extracted fields
  * Validation results
  * AI insights
  * Final vendor recommendation

---

## 📈 Business Impact

### 💰 Cost Savings

* Reduces manual invoice processing effort
* Minimizes payment errors and rework

### 🛡️ Risk Reduction

* Prevents incorrect or fraudulent payments
* Improves compliance and audit readiness

### ⚡ Faster Processing

* Invoice decisions in minutes instead of days
* Faster vendor payments improve relationships

### 📊 Scalability

* Processes hundreds or thousands of invoices
* Easily integrates with ERP and finance systems

---

## 🚀 Key Benefits

* Hybrid AI + rule-based validation (enterprise-ready)
* Automated decision-making
* Vendor cost optimization
* Modular and scalable architecture
* Real-world business applicability

---

## 🧪 Working Prototype

* Fully functional Streamlit application
* Demonstrates:

  * OCR extraction
  * Validation logic
  * AI insights
  * Vendor ranking and recommendations

---

## 🔮 Future Enhancements

* Fraud pattern detection
* Duplicate invoice detection
* ERP integration (SAP, Oracle)
* Dashboard analytics
* Multi-language invoice support

---

## 🏁 Conclusion

This system bridges the gap between **manual finance operations and intelligent automation**, delivering faster, safer, and smarter invoice processing at scale.

> **From unstructured invoices to confident payment decisions — powered by AI.**


