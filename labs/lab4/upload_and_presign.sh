#!/bin/bash

# Check if correct arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <file-name> <bucket-name> <expiration-time-in-seconds>"
    exit 1
fi

FILE_NAME=$1
BUCKET_NAME=$2
EXPIRATION=$3

# Upload file to S3 (private by default)
aws s3 cp "$FILE_NAME" s3://"$BUCKET_NAME"/

# Generate presigned URL
PRESIGNED_URL=$(aws s3 presign --expires-in "$EXPIRATION" s3://"$BUCKET_NAME"/"$FILE_NAME")

# Print the presigned URL
echo "Presigned URL (valid for $EXPIRATION seconds):"
echo "$PRESIGNED_URL"

