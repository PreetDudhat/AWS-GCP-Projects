import json
import boto3
import markovify
from botocore.exceptions import NoCredentialsError

topic_name = 'EmailSubscription'
region = 'us-east-1'  # your region
aws_account_id = '138927234469'  # your AWS account id

# Construct the Topic ARN

def lambda_handler(event, context):
    # Initialize the boto3 client
    sns_client = boto3.client('sns', region_name='us-east-1') # replace with your region
    s3_client = boto3.client('s3')
    textract_client = boto3.client('textract')

    # Use Textract to extract text from the image
    bucket_name = 'mytextgen'
    file_name = event['Records'][0]['s3']['object']['key']

    try:
        response = textract_client.detect_document_text(
            Document={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': file_name
                }
            }
        )
    except NoCredentialsError:
        return {
            'statusCode': 401,
            'body': json.dumps('No AWS credentials found!')
        }
    
    # Extract the text from the Textract response
    extracted_text = ' '.join([item['Text'] for item in response['Blocks'] if item['BlockType'] == 'LINE'])

    # Use Markovify to generate a sentence
    text_model = markovify.Text(extracted_text)
    sentence = text_model.make_short_sentence(100) # generating short sentence with a maximum of 100 characters

    # Publish the sentence to the SNS topic
    # Assuming you have saved the topic ARN from the first function somewhere accessible, like a DynamoDB table or environment variable.
    topic_arn = f'arn:aws:sns:{region}:{aws_account_id}:{topic_name}'
    message = f"Extracted Text: {extracted_text}\n\n\nGenerated Sentence: {sentence}"  # compose the message with both texts
    response = sns_client.publish(
    TopicArn=topic_arn,
    Message=message,
    Subject='Generated Sentence'
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Message sent successfully!')
    }
