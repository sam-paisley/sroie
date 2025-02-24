import os
import sys
import ibm_boto3
from ibm_botocore.client import Config, ClientError


# Load IBM COS credentials from environment variables
COS_ENDPOINT = os.getenv("COS_ENDPOINT")  # Example: "https://s3.au-syd.cloud-object-storage.appdomain.cloud"
COS_API_KEY_ID = os.getenv("COS_API_KEY_ID")  # Example: "your-api-key"
COS_INSTANCE_CRN = os.getenv("COS_INSTANCE_CRN")  # Example: "your-instance-crn"
COS_BUCKET_NAME = os.getenv("COS_BUCKET_NAME")  # Example: "your-bucket-name"

# Check if all required environment variables are set
if not all([COS_ENDPOINT, COS_API_KEY_ID, COS_INSTANCE_CRN, COS_BUCKET_NAME]):
    raise ValueError("❌ Missing one or more required environment variables.")

# Create resource
cos_resource = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

# Function to list available files in the bucket
def list_files_in_bucket():
    try:
        # List all objects (files) in the specified bucket
        bucket = cos_client.Bucket(COS_BUCKET_NAME)
        
        # If there are objects, print their names
        if bucket.objects.all():
            print("Files in the bucket:")
            for obj in bucket.objects.all():
                print(f" - {obj.key}")  # The object key is the filename in the bucket
        else:
            print("The bucket is empty.")
    
    except ClientError as e:
        print(f"Error occurred: {e}")

# Function to upload a file to a specified folder in the bucket
def upload_file_to_folder(file_path, cos_folder):
    """Uploads a single file to a specified folder in IBM COS bucket."""
    file_name = os.path.basename(file_path)  # Extract filename from path
    object_name = f"{cos_folder}/{file_name}"  # Store file inside the given COS folder
    
    try:
        # Open file as binary and use `put_object()`
        with open(file_path, "rb") as file_data:
            cos_resource.Bucket(COS_BUCKET_NAME).put_object(Key=object_name, Body=file_data)
        
        print(f"✅ Uploaded: {file_path} → '{object_name}' in bucket '{COS_BUCKET_NAME}'.")
    except ClientError as e:
        print(f"❌ Error uploading {file_path}: {e}")

# Function to upload all files from a folder
def upload_folder(local_folder, cos_folder):
    """Uploads all files from a given local folder to a specific folder in IBM COS bucket."""
    if not os.path.isdir(local_folder):
        print(f"❌ Error: The provided path '{local_folder}' is not a valid directory.")
        sys.exit(1)

    files = [f for f in os.listdir(local_folder) if os.path.isfile(os.path.join(local_folder, f))]
    
    if not files:
        print(f"⚠️ No files found in '{local_folder}'. Nothing to upload.")
        return

    print(f"📂 Uploading {len(files)} files from '{local_folder}' to '{cos_folder}/' in IBM COS bucket '{COS_BUCKET_NAME}'...")
    
    for file_name in files:
        file_path = os.path.join(local_folder, file_name)
        upload_file_to_folder(file_path, cos_folder)

# Check for command-line arguments
if len(sys.argv) < 3:
    print("❌ Usage: python upload_folder_to_cos.py <local_folder_path> <cos_folder>")
    sys.exit(1)

local_folder_path = sys.argv[1]  # Get local folder path from CLI argument
cos_folder_name = sys.argv[2]  # Get COS folder name from CLI argument
upload_folder(local_folder_path, cos_folder_name)
