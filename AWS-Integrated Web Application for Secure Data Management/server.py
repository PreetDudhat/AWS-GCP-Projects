import grpc
import computeandstorage_pb2
import computeandstorage_pb2_grpc
import boto3
import botocore.exceptions
from grpc import RpcError
from concurrent import futures

class EC2OperationsServicer(computeandstorage_pb2_grpc.EC2OperationsServicer):
    def __init__(self):
        
        # Authenticate with AWS using access key, secret key, session token and region
        session = boto3.Session(
            aws_access_key_id='ASIASAWFVLWS5RCI4LHT',
            aws_secret_access_key='arlOBVwmpRUJ+45Ko/cB+mt9r70fTjPhQXOidrHe',
            region_name='us-east-1',
            aws_session_token="FwoGZXIvYXdzEH0aDCGOWlFAogNGqa8iUSLAAWabWvubi7IwT3aTgRMsoKJuOu9DU/GKPxNIfO4k3fZND5w3qGlsHIz7PETKQIHuIHgasjcSn36Xgj6y1rDuEzsQXbWMfoVaJOlKvYz0EzyU5MEQe5xbUWc+oaoOsa1mCfgkQIz1oydzSamVrCqmRQYyrDkVNMmnadrDoMdNwtgcwCt1BG7AJ9LR6riKBPj96t4GjoqltDbX90WKZYRtM2lNizH+FrS4gwTKaOwptIWvF8xVIvOrYd/rwBuiQu+YviiN9JSkBjIt4tZui6IHimjo+WsMQGMIZyqFBG8aqvQZhrRrro3DKm6szRkc+Nkg8Cr6g9Z/"
        )
        self.s3_client = session.client('s3')
        self.bucket_name = 'buck2assignment'
        self.file_name = 'buck2.txt'

        # Create S3 bucket if no bucket is present
        if not self._check_bucket_exists():
            self._create_bucket()

    def _check_bucket_exists(self):
        response = self.s3_client.list_buckets()
        buckets = response['Buckets']
        for bucket in buckets:
            if bucket['Name'] == self.bucket_name:
                print("Bucket Exists")
                return True
        return False

    def _create_bucket(self):
        self.s3_client.create_bucket(Bucket=self.bucket_name)
        print("Bucket Created")

    def StoreData(self, request, context):
        # Store the data in the S3 Bucket
        data = request.data.encode('utf-8')

        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=self.file_name,
            Body=data
        )
        # Generate the public S3 URL
        s3uri = f"https://{self.bucket_name}.s3.us-east-1.amazonaws.com/{self.file_name}"

        # Return the StoreReply message with the S3 URL.
        return computeandstorage_pb2.StoreReply(s3uri=s3uri)

    def AppendData(self, request, context):
        # Retrieve the existing file contents
        response = self.s3_client.get_object(
            Bucket=self.bucket_name,
            Key=self.file_name
        )

        existing_data = response['Body'].read().decode('utf-8')

        # Append the new data
        new_data = request.data.encode('utf-8')
        appended_data = existing_data + new_data.decode('utf-8')

        # Overwrite the existing file with the appended data
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=self.file_name,
            Body=appended_data.encode('utf-8')
        )

        # Since Append Reply message has no fields, no need to return anything.
        return computeandstorage_pb2.AppendReply()

    def DeleteFile(self, request, context):
        try:
            # Delete the file from S3
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=self.file_name
            )

        except botocore.exceptions.ClientError as e:
            error_code = e.response.get("Error", {}).get("Code")
            if error_code == "404":
                context.abort(404, "File not found")
                return computeandstorage_pb2.DeleteReply()
            
        except Exception as e:
            print(f"Error deleting file from S3: {str(e)}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return computeandstorage_pb2.DeleteReply()

        # Successful deletion, return empty message
        return computeandstorage_pb2.DeleteReply()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    computeandstorage_pb2_grpc.add_EC2OperationsServicer_to_server(EC2OperationsServicer(), server)
    server.add_insecure_port('[::]:50051')
    #server.add_insecure_port('localhost:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
