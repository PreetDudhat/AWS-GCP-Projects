import boto3
from flask import Flask, request, jsonify
import pymysql
import json
import pymysql.cursors

app = Flask(__name__)

# AWS authentication
aws_access_key_id = "ASIASAWFVLWS7RU4SGV6"
aws_secret_access_key = "0aKx/YsTet0358nLmPVF6XuXmJHyd1EBiHFUFsec"
region_name = "us-east-1"
aws_session_token_id = "FwoGZXIvYXdzEAEaDGBDjddpwXXZE7pO1yLAAeUXpqUMdEAEY4WUorihOn30rxTEzZsDwpJpMWnDY/LGMfl1CXbL6KeRVp/BglLSq+eLP035YzACNoex5tZ/YFtMQgdnHHgK0ddVV1za9rM+oNQN4ExF2AwoW+fmz/3CBGCiPgfNNFhKbYVlxaZQSv1YmU3+XPpekk+Ut9OkiJGEzZOYFb2hfD6DniAU/D6ywiBXmHvhqjlSMtzqG9UC+U5Bq7xpeFvz36E77Y2kR8oUtn/ryxnAFdIhMe3x+PbhAyjMvKKlBjItDA5e4UpJwuOV/Jb6ApXERz6rqpUOpdZUlcEGeUK4cuhNvWhPKXZhKng7LK/U"

# Database configuration
db_host = "database-1-instance-1.csumk5xlgu06.us-east-1.rds.amazonaws.com"
db_name = "netdb"
db_user = "admin"
db_password = "UnknownVPC"

# Authenticate with AWS
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name,
    aws_session_token=aws_session_token_id
)

# Check if the 'products' table exists in the database, if not, create it
def create_products():
    try:
        conn = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            db=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()

        cursor.execute("SHOW TABLES LIKE 'products'")
        table_exists = cursor.fetchone()

        if not table_exists:
            cursor.execute("""
                CREATE TABLE products (
                    name VARCHAR(255),
                    price VARCHAR(255),
                    availability BOOLEAN
                )
            """)

        cursor.close()
        conn.close()

    except Exception as e:
        print("Error creating 'products' table:", str(e))

# List products from the database
@app.route('/list-products', methods=['GET'])
def list_products():
    try:
        create_products()  # Check if the table exists, if not, create it

        # Connect to the RDS database
        conn = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            db=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()

        # Fetch products from the database
        cursor.execute("SELECT name, price, availability FROM products")
        rows = cursor.fetchall()

        # Build the products list
        products = []
        for row in rows:
            product = {
                'name': row['name'],
                'price': row['price'],
                'availability': row['availability']
            }
            products.append(product)

        cursor.close()
        conn.close()

        return jsonify({'products': products}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Store products in the database
@app.route('/store-products', methods=['POST'])
def store_products():
    try:
        data = request.get_json()
        products = data.get('products', [])

        create_products()  # Check if the table exists, if not, create it

        # Connect to the RDS database
        conn = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            db=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()

        # Insert products into the database
        for product in products:
            name = product.get('name')
            price = product.get('price')
            availability = product.get('availability')

            cursor.execute(
                "INSERT INTO products (name, price, availability) VALUES (%s, %s, %s)",
                (name, price, availability)
            )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Success.'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
