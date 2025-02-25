import boto3
import requests
import sys
import os

# Check arguments
if len(sys.argv) != 4:
    print("Usage: python3 upload_and_presign.py <file-path-or-url> <bucket-name> <expiration-time>")
    sys.exit(1)

file_input = sys.argv[1]  # This can be a local file path or a URL
bucket_name = sys.argv[2]
expiration = int(sys.argv[3])

# Determine if input is a URL or a local file
if file_input.startswith("http"):
    file_name = file_input.split("/")[-1]  # Extract filename from URL
    response = requests.get(file_input)
    
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {file_name}")
    else:
        print("Failed to download the file")
        sys.exit(1)
else:
    # Treat as local file
    if not os.path.exists(file_input):
        print(f"Error: Local file '{file_input}' not found.")
        sys.exit(1)
    file_name = os.path.basename(file_input)

# Upload to S3
s3 = boto3.client('s3')
s3.upload_file(file_input, bucket_name, file_name)

# Generate a presigned URL
presigned_url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket_name, 'Key': file_name},
    ExpiresIn=expiration
)

print(f"Presigned URL (valid for {expiration} seconds): {presigned_url}")

