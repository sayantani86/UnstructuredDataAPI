import os
import boto3
import zipfile
import io
from botocore.exceptions import BotoCoreError, ClientError

# Initialize S3 client
s3 = boto3.client('s3')

# Configuration
BUCKET_NAME = 'ayata-clients'
SOURCE_FOLDER = 'mdtadco/Time_H & P_501_MUNSON RANCH 13H_160278.zip'  # folder where zip files are located
DEST_FOLDER = 'Baytex_new/ayata_processed_data/mdtadco/'  # folder where extracted files will be stored

def list_zip_files(bucket, prefix):
    """
    List all ZIP files in the specified S3 folder.
    """
    try:
        zip_files = []
        paginator = s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            for obj in page.get('Contents', []):
                if obj['Key'].endswith('.zip'):
                    zip_files.append(obj['Key'])
        return zip_files
    except (BotoCoreError, ClientError) as e:
        print(f"Error listing files: {e}")
        return []

def folder_exists(bucket, folder_prefix):
    """
    Check if a folder (prefix) exists in the bucket.
    Returns True if at least one object exists in the folder.
    """
    try:
        response = s3.list_objects_v2(Bucket=bucket, Prefix=folder_prefix, MaxKeys=1)
        return 'Contents' in response  # True if any file is present
    except (BotoCoreError, ClientError) as e:
        print(f"Error checking folder {folder_prefix}: {e}")
        return False

def process_zip_file_in_memory(bucket, key):
    """
    Stream a zip file from S3, extract in-memory, and upload files to S3.
    No local disk storage is used.
    """
    try:
        # Get the zip file as a binary stream
        response = s3.get_object(Bucket=bucket, Key=key)
        zip_file_stream = io.BytesIO(response['Body'].read())

        # Folder name derived from zip file name (no extension)
        zip_base_name = os.path.splitext(os.path.basename(key))[0]

        # Open zip file from stream
        with zipfile.ZipFile(zip_file_stream) as zip_ref:
            for file_name in zip_ref.namelist():
                with zip_ref.open(file_name) as extracted_file:
                    # Prepare S3 key for extracted file
                    s3_key = f"{DEST_FOLDER}{zip_base_name}/{file_name}"

                    # Upload directly to S3
                    print(f"Uploading {file_name} to s3://{bucket}/{s3_key}")

                    s3.upload_fileobj(extracted_file, bucket, s3_key)

            print(f"Processed {key} into folder '{zip_base_name}' successfully.")

    except (BotoCoreError, ClientError, zipfile.BadZipFile) as e:
        print(f"Failed to process {key}: {e}")

def main():
    zip_files = list_zip_files(BUCKET_NAME, SOURCE_FOLDER)

    if not zip_files:
        print("No zip files found.")
        return

    print(f"Found {len(zip_files)} zip files to process.")

    for zip_file_key in zip_files:
        zip_base_name = os.path.splitext(os.path.basename(zip_file_key))[0]
        processed_folder_prefix = f"{DEST_FOLDER}{zip_base_name}/"

        if folder_exists(BUCKET_NAME, processed_folder_prefix):
            print(f"Skipping {zip_file_key} - Already processed.")
            continue

        print(f"Processing {zip_file_key} ...")
        process_zip_file_in_memory(BUCKET_NAME, zip_file_key)

if __name__ == "__main__":
    main()
