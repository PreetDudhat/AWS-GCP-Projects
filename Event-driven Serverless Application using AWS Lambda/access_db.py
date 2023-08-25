import boto3
import json
import logging

dynamodb_client = boto3.client('dynamodb')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Get the bucket name and key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Read the named entities JSON file from S3
    try:
        named_entities = read_named_entities(bucket, key)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON file: {e}")
        return {
            'statusCode': 500,
            'body': 'Error decoding JSON file.'
        }
    
    # Update the DynamoDB table
    update_dynamodb(named_entities)
    
    return {
        'statusCode': 200,
        'body': 'DynamoDB table updated successfully.'
    }

def read_named_entities(bucket, key):
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket, Key=key)
    named_entities_content = response['Body'].read().decode('utf-8')
    
    try:
        named_entities = json.loads(named_entities_content)
        return named_entities
    except json.JSONDecodeError as e:
        raise e

def update_dynamodb(named_entities):
    table_name = 'fileDb'
    
    for key, value in named_entities.items():
        for sub_key, sub_value in value.items():
            dynamodb_client.put_item(
                TableName=table_name,
                Item={
                    'key': {'S': sub_key},
                    'value': {'S': str(sub_value)}
                }
            )
