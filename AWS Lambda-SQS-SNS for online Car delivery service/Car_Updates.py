import boto3

def lambda_handler(event, context):
    # Initialize SQS client
    sqs_client = boto3.client('sqs')

    # Initialize SNS client
    sns_client = boto3.client('sns')

    # SQS queue URLs
    car_type_queue_url = 'https://sqs.us-east-1.amazonaws.com/400121257182/Car_Type'
    accessory_queue_url = 'https://sqs.us-east-1.amazonaws.com/400121257182/Car_Accessories'
    address_queue_url = 'https://sqs.us-east-1.amazonaws.com/400121257182/Client_address'

    # Process car types
    process_sqs_messages(sqs_client, sns_client, car_type_queue_url, "Car Type")

    # Process accessories
    process_sqs_messages(sqs_client, sns_client, accessory_queue_url, "Accessory")

    # Process delivery addresses
    process_sqs_messages(sqs_client, sns_client, address_queue_url, "Delivery Address")

    return {
        'statusCode': 200,
        'body': 'SQS queues processed successfully.'
    }

def process_sqs_messages(sqs_client, sns_client, queue_url, message_type):
    while True:
        response = sqs_client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10)

        if 'Messages' in response:
            for message in response['Messages']:
                body = message['Body']
                print(f"Received {message_type}: {body}")

                # Send a notification to the delivery person via SNS
                sns_topic_arn = 'arn:aws:sns:us-east-1:400121257182:Order_Status_Notification'
                notification_message = f"New order received! {message_type}: {body}"
                sns_client.publish(TopicArn=sns_topic_arn, Message=notification_message)

                # Delete the processed message from the queue
                sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])
        else:
            break
