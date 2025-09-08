import sqlite3
import sys
import os
from flask import Flask, jsonify, request, send_from_directory

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.db_setup import setup_database

app = Flask(__name__, static_folder='../frontend')

DATABASE = 'database/properties.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    # send_from_directory will look for the file in the static_folder
    return send_from_directory(app.static_folder, path)

@app.route('/search', methods=['GET'])
def search():
    area = request.args.get('area')
    property_type = request.args.get('property_type')

    # Mock data - in a real app, this would come from an external API
    mock_properties = [
        {
            "address": "123 Main St", "city": "San Francisco", "region": "Bay Area",
            "property_type": "Apartment", "price": 3000, "bedrooms": 2, "bathrooms": 1
        },
        {
            "address": "456 Oak Ave", "city": "San Francisco", "region": "Bay Area",
            "property_type": "House", "price": 1500000, "bedrooms": 4, "bathrooms": 3
        },
        {
            "address": "789 Pine Ln", "city": "Palo Alto", "region": "Bay Area",
            "property_type": "House", "price": 2500000, "bedrooms": 5, "bathrooms": 4
        }
    ]

    db = get_db()
    cursor = db.cursor()

    # For this example, we clear and re-populate the DB on each search.
    # In a real app, you'd have a more sophisticated data pipeline.
    cursor.execute("DELETE FROM properties")
    for prop in mock_properties:
        cursor.execute("""
            INSERT INTO properties (address, city, region, property_type, price, bedrooms, bathrooms)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (prop['address'], prop['city'], prop['region'], prop['property_type'], prop['price'], prop['bedrooms'], prop['bathrooms']))
    db.commit()

    # Query the database
    query = "SELECT * FROM properties WHERE (city LIKE ? OR region LIKE ?) AND property_type LIKE ?"
    cursor.execute(query, (f'%{area}%', f'%{area}%', f'%{property_type}%'))

    properties = cursor.fetchall()
    db.close()

    # Convert rows to list of dictionaries
    results = [dict(row) for row in properties]

    response = {
        "filters": {
            "area": area,
            "property_type": property_type
        },
        "results": results
    }

    return jsonify(response)

if __name__ == '__main__':
    # Setup the database/table if it doesn't exist
    setup_database()
    app.run(debug=True)
