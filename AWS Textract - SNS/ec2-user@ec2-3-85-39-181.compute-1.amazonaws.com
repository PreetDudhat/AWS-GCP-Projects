from flask import Flask, render_template, request
import requests
import webbrowser
from threading import Timer

app = Flask(__name__)
# AWS credentials
AWS_ACCESS_KEY_ID = 'ASIASAWFVLWSQCIUJQMN'
AWS_SECRET_ACCESS_KEY = 'sx+00qA66RgeSXzIu1Be+R7gYtCuSG3JGI7HmDb7'
AWS_SESSION_TOKEN = 'FwoGZXIvYXdzEPL//////////wEaDIaSqCGHJTibWoDC2iLAAQOYcCQNgg1R3jL0mlHzhI5bBJ9OcnSz/c1RPiKb6RjqAfgAQ4HLZaIUVOpbChhUSFekoD965exSRZgQsjr2uXWEe6y0ZNZQYwuIJ1/hsSNminiEy6nFyETopFRQqTz3Wm2Xik69m2cvaP80HDGU5Ja01WhtSGdxBur2SRw20WNG7Uit2PbMqGUt/yV9UhRohmE3HTptRuZM+Ke/Q3vJT847T5LGrhZMoBpP53fN/NKZ1bhJwXgJReQOZVW/ZwvWQSjj14+mBjItn1nETvOXVVCM35xgxEazst3RmsixfemDWw5SWFc6Wf3w4mvUetIFCbD927wD'
AWS_REGION = 'us-east-1'

@app.route('/')
def index():
    return render_template('subscription.html')

@app.route('/dashboard')
def dashboard():
    # The logic to get and display the headings goes here
    return render_template('dashboard.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    data = {'email': email}

    # Send the email to your API Gateway
    response = requests.post('https://50fzfcxmll.execute-api.us-east-1.amazonaws.com/gen/EmailSubscription', json=data)
    return f'Subscription request sent! <a href="/dashboard">Click here to Create your Headings</a>'

if __name__ == '__main__':
    # Open a web browser pointing at the app.
    Timer(1, lambda: webbrowser.open('http://localhost:80')).start()
    app.run(host='0.0.0.0', port=80)
