from flask import Flask, render_template, request, redirect, session, url_for
import requests

app = Flask(__name__)

name = ''  # Initialize a global name variable

@app.route('/register', methods=['POST'])
def register():
    # Get the name, email, password and location from the registration form
    name = request.form['name']  
    email = request.form['email']
    password = request.form['password']
    location = request.form['location']

    # Send a POST request to the registration URL to add data to Firestore
    registration_url = "https://con-1-rbzikp7jzq-uc.a.run.app/register"
    payload = {
        'name': name,
        'email': email,
        'password': password,
        'location': location
    }
    response = requests.post(registration_url, json=payload)

    return 'Registration successful! <a href="/">Click here to login</a>'
"""
***************************************************************************************/
*    Title: Flask Tutorial #4 - HTTP Methods (GET/POST) & Retrieving Form Data
*    Author: Tech With Tim 
*    Date: 2020
*    Code version: 1.0
*    Availability: https://www.youtube.com/watch?v=9MHYHgh4jYc
*
***************************************************************************************/
"""
@app.route('/login', methods=['POST'])
def login():
    global name  # Use the global name variable
    # Get the email and password from the Login form
    email = request.form.get('email')
    password = request.form.get('password')

    login_url = 'https://con-2-rbzikp7jzq-uc.a.run.app/login'
    login_data = {'email': email, 'password': password}

    headers = {'Content-Type': 'application/json'}  # Set the content type to JSON

    response = requests.post(login_url, json=login_data, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'message' in data and data['message'] == 'Login successful':
            data = response.json()
            name = data.get('name', '')  # Update the global name variable
            return redirect(url_for('dashboard')) # Redirect to the dashboard page
        elif 'error' in data:
            return render_template('index.html', error=data['error']) # Render the index page with an error message
        
    return 'Login Failed!!!<a href="/">Click here to login</a>'

@app.route('/dashboard')
def dashboard():
    global name  # Use the global name variable

    online_users_url = 'https://con-3-rbzikp7jzq-uc.a.run.app/online-users'
    response = requests.get(online_users_url)
    
    if response.status_code == 200:
        data = response.json()
        online_users = data.get('onlineUsers', [])
        online_users = [user for user in online_users if user['name'] != name]
        return render_template('dashboard.html', online_users=online_users, name=name)
    return render_template('dashboard.html', online_users=[], name='')

@app.route('/logout', methods=['POST'])
def logout():
    global name  # Use the global name variable
    
    # Construct the JSON payload
    payload = {
        'name': name
    }
    headers = {'Content-Type': 'application/json'}  # Set the content type to JSON

    logout_url = "https://con-3-rbzikp7jzq-uc.a.run.app/logout"
    response = requests.post(logout_url, json=payload, headers=headers)
    return f"Logout successful for user: {name}! <a href='/'>Click here to login</a>"

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
