from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

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
    tank_name = request.form['name']
    tank_type = request.form['type']
    tank_country = request.form['country']
    tank_year_str = request.form['year']  # Get year as string

    # Validate if tank_year is an integer
    try:
        tank_year = int(tank_year_str)
    except ValueError:
        # If tank_year is not an integer, redirect back to the main page with an error message
        error_message = "Year must be an integer."
        tanks = list(tanks_collection.find())
        return render_template('index.html', tanks=tanks, error=error_message)

    # Insert the tank data into the MongoDB collection
    tank_data = {
        "name": tank_name,
        "type": tank_type,
        "country": tank_country,
        "year": tank_year
    }
    tanks_collection.insert_one(tank_data)

    # Redirect to the main page after adding the tank
    return redirect(url_for('index'))

# Route to delete a tank
@app.route('/delete_tank', methods=['POST'])
def delete_tank():
    # Get the tank name from the form
    tank_name = request.form.get('name')

    # Delete the tank from the database
    tanks_collection.delete_one({"name": tank_name})

    # Redirect to the main page after deletion
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
