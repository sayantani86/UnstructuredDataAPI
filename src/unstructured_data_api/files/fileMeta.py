import boto3
import pandas as pd
import os
import math
import re

# AWS S3 Configuration
BUCKET_NAME = "ayata-clients"
S3_FOLDER_PATH = "Baytex_new/ayata_processed_data/mdtadco/"

# S3 Client
s3 = boto3.client('s3')
SHEET_LIMIT = 10
SKIP_FILES = 340
START_FILE_INDEX = 35


def list_all_csv_files(bucket, prefix):
    csv_files = []
    paginator = s3.get_paginator('list_objects_v2')
    operation_parameters = {'Bucket': bucket, 'Prefix': prefix}

    for page in paginator.paginate(**operation_parameters):
        if 'Contents' in page:
            for obj in page['Contents']:
                if obj['Key'].lower().endswith('.csv'):
                    csv_files.append(obj['Key'])

    return csv_files


def detect_entropy(series):
    series_str = series.astype(str)
    all_text = ''.join(series_str)

    byte_arr = bytearray(all_text, 'utf-8')
    n = len(byte_arr)
    if n <= 1:
        return 0.0

    frequencies = {}
    for byte in byte_arr:
        frequencies[byte] = frequencies.get(byte, 0) + 1

    entropy = sum(-p * math.log2(p) for p in (freq / n for freq in frequencies.values()))

    return entropy


def detect_data_type(series):
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"

    if pd.api.types.is_integer_dtype(series):
        return "int"

    if pd.api.types.is_float_dtype(series):
        return "float"

    if pd.api.types.is_bool_dtype(series):
        return "boolean"

    if pd.api.types.is_string_dtype(series) or series.dtype == "object":
        non_null_values = series.dropna()

        date_patterns = [
            r"^\d{4}-\d{2}-\d{2}$",
            r"^\d{2}/\d{2}/\d{4}$",
            r"^\d{4}/\d{2}/\d{2}$",
            r"^\d{2}-\d{2}-\d{4}$",
            r"^\d{4}\d{2}\d{2}$",
        ]

        date_match_count = sum(
            any(re.match(pattern, str(val)) for pattern in date_patterns)
            for val in non_null_values
        )
        datetime_ratio = date_match_count / len(non_null_values) if len(non_null_values) > 0 else 0

        if datetime_ratio > 0.8:
            return "datetime"

        entropy = detect_entropy(series)
        return "encrypted" if entropy > 7.5 else "varchar"

    return "unknown"


def process_csv_from_s3(file_key):
    file_name, _ = os.path.splitext(os.path.basename(file_key))
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)

    try:
        csv_chunk = pd.read_csv(
            obj["Body"], on_bad_lines="skip", encoding="utf-8", low_memory=False, chunksize=10000
        )

        row_count = 0
        column_count = 0
        variable_types = {}

        for chunk in csv_chunk:
            row_count += chunk.shape[0]
            column_count = max(column_count, chunk.shape[1])

            for col in chunk.columns:
                detected_type = detect_data_type(chunk[col])
                variable_types[col] = detected_type

        sheet_name = file_name.split('_')[-2] + '_' + file_name.split('_')[-1]
        sheet_name = re.sub(r'[\\/*?:"<>|]', '', sheet_name[-31:])  # Clean sheet name

        return {
            "tablename": file_name,
            "row_count": row_count,
            "column_count": column_count,
            "sheet_name": sheet_name,
            "columns": [{"Col_Name": col, "D_type": dtype} for col, dtype in variable_types.items()]
        }
    except Exception as e:
        print(f"❌ Error processing {file_name}.csv: {e}")
        return None


def write_metadata_to_excel(metadata_list, file_index):
    output_path = f"mdtadco/mdtadco_Meta_{file_index}.xlsx"
    print(f"✅ Saving metadata to {output_path}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    writer = pd.ExcelWriter(output_path, engine="xlsxwriter")
    workbook = writer.book

    # Formatting
    bold_center = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1})
    bold_left = workbook.add_format({'bold': True, 'align': 'left', 'border': 1})
    text_format = workbook.add_format({'align': 'left', 'border': 1})
    merge_format = workbook.add_format({'bold': True, 'align': 'center', 'border': 1})

    for metadata in metadata_list:
        sheet_name = metadata['sheet_name']
        worksheet = workbook.add_worksheet(sheet_name)

        # Write table-level metadata
        worksheet.write(0, 0, "tablename", bold_center)
        worksheet.write(0, 1, "row_count", bold_center)
        worksheet.write(0, 2, "column_count", bold_center)

        worksheet.write(1, 0, metadata['tablename'], text_format)
        worksheet.write(1, 1, metadata['row_count'], text_format)
        worksheet.write(1, 2, metadata['column_count'], text_format)

        # Write Variable Name as Section Header
        worksheet.merge_range(0, 3, 0, 4, "Variable Name", merge_format)
        worksheet.write(1, 3, "Col_Name", bold_left)
        worksheet.write(1, 4, "D_type", bold_left)

        # Write columns under Variable Name
        for idx, col in enumerate(metadata['columns'], start=2):
            worksheet.write(idx, 3, col['Col_Name'], text_format)
            worksheet.write(idx, 4, col['D_type'], text_format)

    writer.close()
    print(f"✅ Metadata saved successfully: {output_path}")


def main():
    csv_files = list_all_csv_files(BUCKET_NAME, S3_FOLDER_PATH)
    print(f"🔍 Found {len(csv_files)} CSV files under {S3_FOLDER_PATH}")

    file_index = START_FILE_INDEX
    metadata_list = []
    counter = 0

    for idx, file_key in enumerate(csv_files):
        # ✅ Skip the first 130 files
        # counter += 1
        if idx <= SKIP_FILES:
            print(f"⏩ Skipping file {idx + 1}: {file_key}")
            continue

        
        print(f"📊 Processing {idx} - file: {file_key}")
        metadata = process_csv_from_s3(file_key)

        if metadata:
            metadata_list.append(metadata)

        # ✅ Save after processing 10 files
        if len(metadata_list) >= SHEET_LIMIT:
            write_metadata_to_excel(metadata_list, file_index)
            metadata_list = []  # Reset the list
            file_index += 1

    # ✅ Save remaining files
    if metadata_list:
        write_metadata_to_excel(metadata_list, file_index)


if __name__ == "__main__":
    main()
