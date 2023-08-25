# The code used here is from Assignment 1 just made necessary changes to fit the requirements
import boto3
import os
import time
from botocore.exceptions import NoCredentialsError

AWS_ACCESS_KEY = 'ASIAV2KIV3TPBVFVJFW7'
AWS_SECRET_KEY = '4CDSaD5B6VaKys5jjyP3UwNevh882ndBTpi4omOZ'
AWS_SESSION_TOKEN = 'FwoGZXIvYXdzEEoaDOWkuLhGUaBf3v5nIiLAAbPiREEdhLw/zMDV2AqtLB1e68oWGrAWyyGOKcMHxRKRUt7QmehYgb3tm1gnVIRutaaDYgGxAr0/4BihDL727nLeWt6/m5xbSfkuV56tngi4XSzv5C0D6uBa8oECOm1MphHmi6P8VoECTJ70lKljSi6G5/f8qUdS4x+79StWN72AAnbfKFkaINeTMKS+w8h4povoM3egv+U6E1zCdBqp18HWDy20DrPTCPSTwLMQfr1GHatgbq8oy9l0hvrp1naqgSiz4+qlBjItJDzcV48kx0YWBVF4INgb0uMBcjNTDKYFsUPXBEIjeB5UgG4DqIEQ0R1i92Sf'
REGION_NAME = 'us-east-1'

def upload_to_aws(local_file, bucket, s3_file):
    session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY,
                            aws_secret_access_key=AWS_SECRET_KEY,
                            aws_session_token=AWS_SESSION_TOKEN,
                            region_name=REGION_NAME)
    s3 = session.resource('s3')

    try:
        s3.Bucket(bucket).upload_file(local_file, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

# Define your directory path and bucket name
dir_path = r'D:/Serverless/A3 - final/PartB/tech'
bucket_name = 'sampledatab00913117'

# Iterate over all the files in the directory and upload them to the bucket
for file_name in os.listdir(dir_path):
    local_file = os.path.join(dir_path, file_name)
    s3_file_name = file_name
    upload_to_aws(local_file, bucket_name, s3_file_name)
    time.sleep(0.1)  # Add delay of 100 milliseconds
