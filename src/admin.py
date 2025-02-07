import streamlit as st
import os
from dotenv import load_dotenv
from s3_utils import ensure_bucket_exists, list_pdfs_in_s3, download_and_process_pdf
from text_processing import split_text
from vector_store import create_vector_store

# Load environment variables from .env file
load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME")
if not BUCKET_NAME:
    raise ValueError("BUCKET_NAME environment variable is not set")

def main():
    st.title("Admin - Process PDFs into FAISS Index by Style")
    st.write("Process PDFs from specific S3 subfolders to create style-specific embeddings.")
    
    # Add bucket creation check at the start
    if not ensure_bucket_exists(BUCKET_NAME):
        st.error("Failed to ensure S3 bucket exists. Please check your AWS credentials and permissions.")
        return

    # Let user choose which style to process
    style_choice = st.radio(
        "Select which style you want to process:",
        ("Email Style", "Normal Style", "Report Style", "Feedback Style")
    )
    
    # Map the style_choice to the S3 prefix
    prefix_map = {
        "Email Style": "mail/",
        "Normal Style": "normal/",
        "Report Style": "report/",
        "Feedback Style": "feedback/"
    }
    
    # Also map the style_choice to a unique key used for saving FAISS indexes
    style_key_map = {
        "Email Style": "mail",
        "Normal Style": "normal",
        "Report Style": "report",
        "Feedback Style": "feedback"
    }
    
    selected_prefix = prefix_map[style_choice]
    style_key = style_key_map[style_choice]

    st.write(f"You selected: {style_choice} (S3 prefix: {selected_prefix})")
    pdf_files = list_pdfs_in_s3(BUCKET_NAME, selected_prefix)
    
    if not pdf_files:
        st.warning(f"No PDF files found in S3 bucket under prefix: {selected_prefix}")
        return

    st.write(f"Found {len(pdf_files)} PDF files in S3 for this style.")
    
    if st.button(f"Process PDFs for {style_choice}"):
        all_pages = []
        
        # Process each PDF
        for pdf_file in pdf_files:
            st.write(f"Processing {pdf_file}...")
            pages = download_and_process_pdf(BUCKET_NAME, pdf_file)
            if pages:
                all_pages.extend(pages)
                st.write(f"Added {len(pages)} pages from {pdf_file}")

        if all_pages:
            # Split Text
            splitted_docs = split_text(all_pages, chunk_size=1000, chunk_overlap=200)
            st.write(f"Total chunks created: {len(splitted_docs)}")

            # Show sample chunks
            if len(splitted_docs) > 0:
                with st.expander("View sample chunks"):
                    st.write(splitted_docs[0])
                    if len(splitted_docs) > 1:
                        st.write(splitted_docs[1])

            # Create the Vector Store
            st.write(f"Creating the Vector Store for {style_choice}...")
            result = create_vector_store(BUCKET_NAME, style_key, splitted_docs)

            if result:
                st.success(f"PDFs processed and FAISS index created successfully for {style_choice}!")
            else:
                st.error("Error creating vector store. Please check logs.")

if __name__ == "__main__":
    main()