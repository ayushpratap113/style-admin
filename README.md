# forte-admin

This project is a Streamlit-based web application designed to process PDF documents stored in an S3 bucket, split the text into chunks, and create FAISS indexes for different document styles.

## Project Structure

```
forte-admin/
├── .env
├── Dockerfile
├── README.md
├── requirements.txt
└── src/
    ├── __init__.py
    ├── admin.py
    ├── s3_utils.py
    ├── text_processing.py
    └── vector_store.py
```

### Files and Directories

- **`.env`**: Contains environment variables for the project.
- **`Dockerfile`**: Defines the Docker image for the application.
- **`README.md`**: This file, which explains the project functionality and usage.
- **`requirements.txt`**: Lists the Python dependencies required for the project.
- **`src/`**: Contains the source code for the project.
  - **`__init__.py`**: Marks the directory as a Python package.
  - **`admin.py`**: Main script for the Streamlit application.
  - **`s3_utils.py`**: Contains S3-related utility functions.
  - **`text_processing.py`**: Contains text processing functions.
  - **`vector_store.py`**: Contains functions for creating and storing FAISS indexes.

## Functionality

The application allows users to:

1. **Select a Document Style**: Choose from Email Style, Normal Style, Report Style, or Feedback Style.
2. **List PDF Files**: List all PDF files in the specified S3 prefix (subfolder).
3. **Process PDFs**: Download and process the selected PDFs, split the text into chunks, and create a FAISS index.
4. **View Results**: Display the results and any errors encountered during processing.

## Usage

### Prerequisites

- Docker installed on your machine.
- AWS credentials with access to the specified S3 bucket.

### Setup

1. **Create and Configure `.env` File**: Add the necessary environment variables to the `.env` file.

```env
BUCKET_NAME=your-s3-bucket-name
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
AWS_REGION=your-aws-region
```

2. **Build and Run the Docker Container**: Use the following commands to build and run the Docker container.

```sh
docker build -t forte-admin .
docker run -p 8083:8083 --env-file .env forte-admin
```

3. **Access the Application**: Open a web browser and navigate to `http://localhost:8083`. You should see the Streamlit application running.

### Example Workflow

1. **Select a Document Style**: Choose the style of documents you want to process.
2. **List PDF Files**: The application will list all PDF files in the specified S3 prefix.
3. **Process PDFs**: Click the button to process the PDFs. The application will download, split, and create a FAISS index for the documents.
4. **View Results**: The results and any errors will be displayed in the application.

## Additional Information

- **`s3_utils.py`**: Contains functions to ensure the S3 bucket exists, list PDF files in S3, and download and process PDFs.
- **`text_processing.py`**: Contains functions to split text into chunks.
- **`vector_store.py`**: Contains functions to create and store FAISS indexes.

By following these steps, you should be able to run the project and access the Streamlit application.