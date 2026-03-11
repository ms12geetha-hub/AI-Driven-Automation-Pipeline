import streamlit as st
from Extractions import extract_and_validate

st.title("Invoice Processing App")

# File uploader
uploaded_file = st.file_uploader("Upload an Invoice (Image or PDF)", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file is not None:
    # Process the uploaded file
    with st.spinner("Processing..."):
        result = extract_and_validate(uploaded_file)

    # Display the raw OCR text for debugging
    if "text" in result:
        st.subheader("Raw OCR Text")
        st.text(result["text"])

    # Display the results
    if "error" in result:
        st.error(result["error"])
    else:
        st.subheader("Extracted Data")
        st.json(result.get("extracted_data", {}))

        st.subheader("Validation Result")
        st.json(result.get("validation_result", {}))