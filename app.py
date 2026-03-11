import streamlit as st
import os
from bulk_processor import process_bulk  # your bulk processing logic

st.set_page_config(page_title="Vendor Invoice Evaluation", layout="wide")

st.title("AI + Rule-Based Vendor Invoice Validation System")

st.markdown("""
Upload one or multiple invoices (PDF or image), and the system will:
- Extract GSTIN, PAN, invoice date, and amount  
- Run rule-based evaluation 
- Run  AI semantic checks (Azure OpenAI)  
- Suggest the best vendor based on price and score
""")

uploaded_files = st.file_uploader("Upload Invoices", type=['pdf','png','jpg','jpeg'], accept_multiple_files=True)

if uploaded_files:
    st.info(f"Processing {len(uploaded_files)} files...")
    
    # Save files temporarily
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    file_paths = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        file_paths.append(file_path)

    # Override bulk_processor process function to accept specific files
    from bulk_processor import process_bulk
    
    # Save original list of files inside bulk_processor or modify process_bulk to take a list
    # For demo, let's assume process_bulk can take a list of files
    results = process_bulk(files=file_paths)

    st.success("Processing complete!")

    for res in results:
        st.markdown(f"### File: {res['file_name']}")
        st.json(res)
