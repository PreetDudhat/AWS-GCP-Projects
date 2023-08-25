# The code used here is from Assignment 1 just made necessary changes to fit the requirements

import boto3
from botocore.exceptions import NoCredentialsError, ClientError

AWS_ACCESS_KEY = 'ASIAV2KIV3TPBVFVJFW7'
AWS_SECRET_KEY = '4CDSaD5B6VaKys5jjyP3UwNevh882ndBTpi4omOZ'
AWS_SESSION_TOKEN = 'FwoGZXIvYXdzEEoaDOWkuLhGUaBf3v5nIiLAAbPiREEdhLw/zMDV2AqtLB1e68oWGrAWyyGOKcMHxRKRUt7QmehYgb3tm1gnVIRutaaDYgGxAr0/4BihDL727nLeWt6/m5xbSfkuV56tngi4XSzv5C0D6uBa8oECOm1MphHmi6P8VoECTJ70lKljSi6G5/f8qUdS4x+79StWN72AAnbfKFkaINeTMKS+w8h4povoM3egv+U6E1zCdBqp18HWDy20DrPTCPSTwLMQfr1GHatgbq8oy9l0hvrp1naqgSiz4+qlBjItJDzcV48kx0YWBVF4INgb0uMBcjNTDKYFsUPXBEIjeB5UgG4DqIEQ0R1i92Sf'
REGION_NAME = 'us-east-1'

def create_bucket(bucket_name, region=REGION_NAME):
    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY,
                            aws_secret_access_key=AWS_SECRET_KEY, region_name=REGION_NAME, aws_session_token=AWS_SESSION_TOKEN)
    try:
        if region == 'us-east-1':
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    except ClientError as e:
        print(e)
        return False
    print(f'Bucket {bucket_name} created.')
    return True

# Bucket names
bucket_name1 = 'sampledatab00913117'
bucket_name2 = 'tagsb00913117'

create_bucket(bucket_name1)
create_bucket(bucket_name2)
