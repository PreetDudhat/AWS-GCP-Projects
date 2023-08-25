import boto3
import json
import re

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Get the source bucket and key from the event
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    source_key = event['Records'][0]['s3']['object']['key']
    
    # Get the filename without the extension
    file_name = source_key.split('.')[0]
    
    # Read the file content from S3
    file_content = get_file_content(source_bucket, source_key)
    
    # Extract named entities
    named_entities = extract_named_entities(file_content)
    
    # Create a JSON array of named entities
    json_array = {f"{file_name}ne": named_entities}
    
    # Save the JSON array as a file in the target bucket
    target_bucket = 'tagsb00913117'
    target_key = f"{file_name}ne.txt"
    save_json_file(json_array, target_bucket, target_key)
    
    return {
        'statusCode': 200,
        'body': 'Named entities extracted and saved successfully.'
    }

def get_file_content(bucket, key):
    response = s3_client.get_object(Bucket=bucket, Key=key)
    file_content = response['Body'].read().decode('utf-8')
    return file_content

def extract_named_entities(file_content):
    # Regular expression pattern to match named entities
    pattern = r'\b[A-Z][a-zA-Z]*\b'
    named_entities = {}
    
    # Find all named entities in the file content
    matches = re.findall(pattern, file_content)
    
    # Count the occurrences of each named entity
    for entity in matches:
        if entity not in named_entities:
            named_entities[entity] = 1
        else:
            named_entities[entity] += 1
    
    return named_entities

def save_json_file(data, bucket, key):
    json_content = json.dumps(data)
    s3_client.put_object(Body=json_content, Bucket=bucket, Key=key)