import boto3
import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader


s3_client = boto3.client("s3", region_name="us-east-1")

def ensure_bucket_exists(bucket_name):
    try:
        # Check if bucket exists
        s3_client.head_bucket(Bucket=bucket_name)
    except s3_client.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            # Bucket doesn't exist, create it
            try:
                s3_client.create_bucket(Bucket=bucket_name)
                st.success(f"Created new S3 bucket: {bucket_name}")
            except Exception as create_error:
                st.error(f"Failed to create S3 bucket: {str(create_error)}")
                return False
        else:
            st.error(f"Error checking S3 bucket: {str(e)}")
            return False
    return True

def list_pdfs_in_s3(bucket_name, prefix):
    """
    List all PDF files in the specified prefix (subfolder) in S3.
    """
    try:
        response = s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix
        )
        pdf_files = [obj['Key'] for obj in response.get('Contents', []) 
                    if obj['Key'].lower().endswith('.pdf')]
        return pdf_files
    except Exception as e:
        st.error(f"Error listing PDFs from S3 for prefix '{prefix}': {str(e)}")
        return []

def download_and_process_pdf(bucket_name, s3_key):
    """
    Download PDF from S3 and process it using PyPDFLoader.
    """
    try:
        local_file = f"/tmp/{os.path.basename(s3_key)}"
        s3_client.download_file(bucket_name, s3_key, local_file)
        
        loader = PyPDFLoader(local_file)
        pages = loader.load_and_split()
        return pages
    except Exception as e:
        st.error(f"Error processing {s3_key}: {str(e)}")
        return None