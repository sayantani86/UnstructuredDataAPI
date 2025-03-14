import warnings
import pandas as pd
import boto3
from botocore.exceptions import NoCredentialsError

warnings.simplefilter("ignore", UserWarning)

def get_s3_client():
    """Initialize and return an S3 client."""
    try:
        return boto3.client('s3')
    except NoCredentialsError:
        print("AWS credentials not found. Please configure them.")
        return None

def format_file_size(file_size_bytes):
    """Convert bytes to human-readable KB or MB format."""
    return f"{file_size_bytes / (1024 * 1024):.2f} MB" if file_size_bytes >= 1024 * 1024 else f"{file_size_bytes / 1024:.2f} KB"

def list_objects_in_s3(s3_client, bucket_name, prefix):
    """List all objects (folders and files) under a given prefix."""
    paginator = s3_client.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    files = []
    for page in pages:
        if "Contents" in page:
            for obj in page["Contents"]:
                if not obj["Key"].endswith('/'):
                    files.append(obj["Key"])

    return sorted(files)

def extract_folder_structure(file_key, base_prefix):
    """
    Extracts parent folder, subfolders (dynamically expanding columns), and file name.
    """
    relative_path = file_key[len(base_prefix):]
    parts = relative_path.split('/')

    parent_folder = parts[0] if len(parts) > 1 else ""
    sub_folders = parts[1:-1] if len(parts) > 2 else []
    file_name = parts[-1]

    return parent_folder, sub_folders, file_name

def process_folders_in_s3(bucket_name, s3_prefix, allowed_alphabets):
    """Process all valid files and dynamically structure subfolder columns."""
    s3_client = get_s3_client()
    if not s3_client:
        return

    all_files = list_objects_in_s3(s3_client, bucket_name, s3_prefix)
    if not all_files:
        print("No files found in the specified prefix.")
        return

    # Identify first-level parent folders
    all_parent_folders = set()
    for file_key in all_files:
        relative_path = file_key[len(s3_prefix):]
        parts = relative_path.split('/')
        if len(parts) > 1:
            all_parent_folders.add(parts[0])

    # Filter parent folders by allowed alphabets
    allowed_parent_folders = [pf for pf in all_parent_folders if pf[0].upper() in allowed_alphabets]
    print(f"Total matching parent folders found: {len(allowed_parent_folders)}")

    file_data = []
    max_subfolder_depth = 0  # Track max depth for CSV column creation

    # Process all files, checking their parent folder
    for file_key in all_files:
        parent_folder, sub_folders, file_name = extract_folder_structure(file_key, s3_prefix)

        # Only process files if they belong to an allowed parent folder
        if parent_folder in allowed_parent_folders or parent_folder == "":
            response = s3_client.head_object(Bucket=bucket_name, Key=file_key)
            file_size_bytes = response["ContentLength"]
            file_size = format_file_size(file_size_bytes)
            file_extension = file_name.split('.')[-1]
            file_type = file_extension if file_extension else "unknown"

            max_subfolder_depth = max(max_subfolder_depth, len(sub_folders))

            file_data.append({
                "parent_folder": parent_folder,
                "sub_folders": sub_folders,
                "file_name": file_name,
                "file_size": file_size,
                "file_type": file_type,
                "s3_path": f"s3://{bucket_name}/{file_key}"
            })

    # Save after processing
    save_to_csv(file_data, max_subfolder_depth, allowed_alphabets)

def save_to_csv(file_data, max_subfolder_depth, allowed_alphabets):
    """Save processed data to CSV with dynamic subfolder columns."""
    if not file_data:
        print("No data to save.")
        return

    # Dynamically create subfolder column headers
    columns = ["parent_folder"] + [f"sub_folder{i+1}" for i in range(max_subfolder_depth)] + ["file_name", "file_size", "file_type", "s3_path"]
    
    # Prepare rows for the DataFrame
    rows = []
    for entry in file_data:
        row = [entry["parent_folder"]]  # Parent folder
        row += entry["sub_folders"] + [""] * (max_subfolder_depth - len(entry["sub_folders"]))  # Subfolder columns
        row += [entry["file_name"], entry["file_size"], entry["file_type"], entry["s3_path"]]  # File name, size, and path
        rows.append(row)

    # Create DataFrame and save to CSV
    df = pd.DataFrame(rows, columns=columns)
    file_name = f"filtered_folders_with_{allowed_alphabets[0]}.csv"
    df.to_csv(file_name, encoding='utf-8', index=False)
    print(f"Saved {len(file_data)} records to {file_name}")

if __name__ == "__main__":
    BUCKET_NAME = "ayata-clients"  # Change this to your S3 bucket
    S3_PREFIX = "baytex/raw_data/"  # Change this prefix as needed

    # Get user input for allowed starting alphabets (only filters first-level parent folders)
    allowed_alphabets = input("Enter the allowed starting alphabets (e.g., A,B,C): ").upper().split(',')

    print(f"Processing first-level parent folders starting with {allowed_alphabets}, including all subfolders inside...")
    process_folders_in_s3(BUCKET_NAME, S3_PREFIX, allowed_alphabets)
    print("Processing complete.")
