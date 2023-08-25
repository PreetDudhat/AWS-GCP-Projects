from flask import Flask, render_template, request
import requests
import boto3
import os
import json

app = Flask(__name__)

AWS_REGION = 'us-east-1'
S3_BUCKET_NAME = 'mytextgen'
SECRET_NAME = "myurl"
AWS_ACCESS_KEY = 'ASIASAWFVLWSSV6ZMV63'
AWS_SECRET_KEY = 'kNjJP8XP3DDXre4vmab7nIqsVhZZogjT6pdQ0sYy'
AWS_SESSION_TOKEN = 'FwoGZXIvYXdzEEAaDGC4YD16curI18muPiLAAXZsGbJOGDe2Y3U1iSWXgjYIXVjK7G38Ub2gc08kbjNDGYLqMPaWp7SBB2ERMCZxIw1Ex3XMMg4R5BTlpJFW5GbK4URzhpKP8FVlVnCP7Wpw3F9FbG/VLlZ7YNJdo3oQTCArGyFyifl6FepJCp4adzsuja6xJNqQCeiT722JOrVZ3ZXRqJ6ZOLR7vw33uffp8JURfZW8a3/0AQ57BzcoXwjvpyDF7a/1dblakvxFwyeul/AHu76MNeeCfLC1rIDpCSiq9KCmBjItTC7eETuygIBah4ahR7+8qQbM9yfRc0fxmfmQ9Ac18r+BoR64FnR1ygYmv1s2'

def get_aws_client(service):
    return boto3.client(service,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        aws_session_token=AWS_SESSION_TOKEN,
        region_name=AWS_REGION)

def get_secret(secret_name):
    secretsmanager = get_aws_client('secretsmanager')
    response = secretsmanager.get_secret_value(SecretId=secret_name)
    return response['SecretString']

API_GATEWAY_URL = get_secret(SECRET_NAME) + '/EmailSub'

@app.route('/')
def index():
    return render_template('subscription.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    data = {'email': email}

    print(f"API_GATEWAY_URL: {API_GATEWAY_URL}")
    
    response = requests.post(API_GATEWAY_URL, json=data)
    return f'Subscription request sent! <a href="/dashboard">Click here to Create your Headings</a>'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part in the request', 400
    file = request.files['file']

    s3 = get_aws_client('s3')
    s3.upload_fileobj(file, S3_BUCKET_NAME, file.filename)

    return F'File uploaded successfully!! <a href="https://mail.google.com/mail/u/1/?ogbl#inbox"> Check your mail !!! </a>', 200

if __name__ == '__main__':
    print(f"API_GATEWAY_URL: {API_GATEWAY_URL}")  # print the API Gateway URL
    app.run(host='0.0.0.0', port=5002)
