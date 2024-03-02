from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import re

# Function to validate tank data
def validate_tank_data(tank_data):
    """Validate tank data before adding to the database."""
    # Check if all fields are provided and not empty
    for field in ['name', 'type', 'country', 'year']:
        if not tank_data.get(field):
            return False, f'Missing {field} field.'

    # You can add more validation rules as per your requirements

    return True, ''

# Initialize Flask app
app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['tanksdb']
tanks_collection = db['tanks']

# Route to display main page with tanks
@app.route('/')
def index():
    # Fetch tanks from the MongoDB collection
    tanks = list(tanks_collection.find())
    return render_template('index.html', tanks=tanks)

# Route to add a new tank
@app.route('/add_tank', methods=['POST'])
def add_tank():
    # Get tank data from the form submitted via POST request
    tank_data = {
        "name": request.form['name'],
        "type": request.form['type'],
        "country": request.form['country'],
        "year": request.form['year']
    }

    # Validate tank data
    is_valid, error_message = validate_tank_data(tank_data)
    if not is_valid:
        # Redirect to the main page with an error message
        return redirect(url_for('index', error_message=error_message))

    # Insert the tank data into the MongoDB collection
    tanks_collection.insert_one(tank_data)

    # Redirect to the main page after adding the tank
    return redirect(url_for('index'))

# Route to delete a tank
@app.route('/delete_tank', methods=['POST'])
def delete_tank():
    # Get the tank name from the form
    tank_name = request.form.get('name')

    # Delete the tank from the database
    if tank_name:
        tanks_collection.delete_one({"name": tank_name})

    # Redirect to the main page after deletion
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
