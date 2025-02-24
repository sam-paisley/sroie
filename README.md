# Uploading folder with contents to COS bucket

Contents of .env file

```
$ cat .env
export COS_ENDPOINT="https://s3.au-syd.cloud-object-storage.appdomain.cloud" # Current list avaiable at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
export COS_API_KEY_ID="<FILL_IN>" #IBM CLOUD API KEY
export COS_INSTANCE_CRN="<FILL_IN>"
export COS_BUCKET_NAME="<FILL_IN>"
```

```
$ source .env
```
```
$ ./upload_folder_to_cos.py
Usage: python upload_folder_to_cos.py <local_folder_path> <cos_folder>
```
```
$ python img_upload_cos.py ./folder/ test-folder
📂 Uploading 1 files from './folder/' to 'test-folder/' in IBM COS bucket 'sdu-bucket'...
✅ Uploaded: ./folder/example.jpg → 'test-folder/example.jpg' in bucket 'sdu-bucket'.



