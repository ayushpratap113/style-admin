import os
import streamlit as st
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import FAISS
import boto3

bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0", client=bedrock_client)

s3_client = boto3.client("s3", region_name="us-east-1")

def create_vector_store(bucket_name, style_key, documents):
    """
    Create and store a FAISS index for the given style_key (e.g., 'mail', 'normal', 'report', 'feedback').
    The index files will be saved with style_key suffix in /tmp and then uploaded to S3.
    """
    vectorstore_faiss = FAISS.from_documents(documents, bedrock_embeddings)
    folder_path = "/tmp/"
    
    # Decide on file names based on style_key
    faiss_index_name = f"my_faiss_{style_key}"
    faiss_index_file = faiss_index_name + ".faiss"
    faiss_pkl_file = faiss_index_name + ".pkl"
    
    # Save locally
    vectorstore_faiss.save_local(index_name=faiss_index_name, folder_path=folder_path)

    # Upload to S3
    try:
        s3_client.upload_file(
            Filename=os.path.join(folder_path, faiss_index_file), 
            Bucket=bucket_name,
            Key=faiss_index_file
        )
        s3_client.upload_file(
            Filename=os.path.join(folder_path, faiss_pkl_file), 
            Bucket=bucket_name,
            Key=faiss_pkl_file
        )
        return True
    except Exception as e:
        st.error(f"Error uploading to S3: {str(e)}")
        return False