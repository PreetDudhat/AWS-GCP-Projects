# Import necessary libraries
import random
import boto3

# Define lists of car types, accessories, and client addresses
CAR_TYPES = ["Buggati Bolide", "Bugatti La Voiture Noire", "Batmobile", "SSC Tuatara", "Aston Martin Valkyrie", "Koenigsegg Jesko Absolut"]
ACCESSORIES = ["Voice-Activated Car Display", "Disco Ball Gear Shift Knob", "Bubble Machine Roof", "LED Underglow with Music Sync", "DASH CAMS & RADAR DETECTORS", "All accessories"]
CLIENT_ADDRESSES = ["Area 51, Nevada", "Wayne Manor, Gotham City", "White House, 1600 Pennsylvania Avenue NW, Washington, D.C., United States", "Suzuka Circuit, Japan", "Sepang International Circuit, Malaysia", "Circuit Gilles Villeneuve, Canada"]

def lambda_handler(event, context):
    # Randomly select car type, car accessory, and delivery address
    car_type = random.choice(CAR_TYPES)
    accessory = random.choice(ACCESSORIES)
    address = random.choice(CLIENT_ADDRESSES)

    # Publish the generated order details to the three SQS queues
    sqs_client = boto3.client('sqs')

    # Construct the order message with car type, accessory, and delivery address
    order_message = f"Car Type: {car_type}, Accessory: {accessory}, Delivery Address: {address}"

    # Send order details to the CarTypeQueue
    car_type_queue_url = 'https://sqs.us-east-1.amazonaws.com/400121257182/Car_Type'
    sqs_client.send_message(QueueUrl=car_type_queue_url, MessageBody=order_message)

    # Send order details to the AccessoryQueue
    accessory_queue_url = 'https://sqs.us-east-1.amazonaws.com/400121257182/Car_Accessories'
    sqs_client.send_message(QueueUrl=accessory_queue_url, MessageBody=order_message)

    # Send order details to the AddressQueue
    address_queue_url = 'https://sqs.us-east-1.amazonaws.com/400121257182/Client_address'
    sqs_client.send_message(QueueUrl=address_queue_url, MessageBody=order_message)

    # Publish the generated order details to the SNS topic (optional)
    sns_client = boto3.client('sns')
    sns_topic_arn = 'arn:aws:sns:us-east-1:400121257182:Car_Order'
    sns_client.publish(TopicArn=sns_topic_arn, Message=order_message)

    return {
        'statusCode': 200,
        'body': 'Order generated and sent to SQS queues.'
    }
