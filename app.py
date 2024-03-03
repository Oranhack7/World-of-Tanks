from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import bson

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['tanksdb']
tanks_collection = db['tanks']

def initialize_database():
    # Check if the collection is empty
    if tanks_collection.count_documents({}) == 0:
        # Placeholder for the actual German tank data
        german_tanks = [
    {"name": "Panzer I", "type": "Light Tank", "country": "Germany", "year": 1934},
    {"name": "Panzer II", "type": "Light Tank", "country": "Germany", "year": 1936},
    {"name": "Panzer III", "type": "Medium Tank", "country": "Germany", "year": 1937},
    {"name": "Panzer IV", "type": "Medium Tank", "country": "Germany", "year": 1939},
    {"name": "Panther", "type": "Medium Tank", "country": "Germany", "year": 1942},
    {"name": "Tiger I", "type": "Heavy Tank", "country": "Germany", "year": 1942},
    {"name": "Tiger II", "type": "Heavy Tank", "country": "Germany", "year": 1944},
    {"name": "Leopard 1", "type": "Main Battle Tank", "country": "Germany", "year": 1965},
    {"name": "Leopard 2", "type": "Main Battle Tank", "country": "Germany", "year": 1979},
]
        tanks_collection.insert_many(german_tanks)
        print('Database initialized with German tank data.')

@app.route('/')
def index():
    tanks = list(tanks_collection.find({}, {'_id': False}))
    return render_template('index.html', tanks=tanks)

@app.route('/add_tank', methods=['POST'])
def add_tank():
    tank_name = request.form.get('name')
    tank_type = request.form.get('type')
    tank_country = request.form.get('country')
    tank_year_str = request.form.get('year')
    
    try:
        tank_year = int(tank_year_str)
        tank_data = {
            "name": tank_name,
            "type": tank_type,
            "country": tank_country,
            "year": tank_year
        }
        tanks_collection.insert_one(tank_data)
        flash('Tank successfully added!', 'success')
    except ValueError:
        flash("Year must be an integer.", 'error')
    
    return redirect(url_for('index'))

@app.route('/delete_tank', methods=['POST'])
def delete_tank():
    tank_name = request.form.get('name')
    
    if tanks_collection.count_documents({"name": tank_name}) > 0:
        tanks_collection.delete_one({"name": tank_name})
        flash('Tank successfully deleted!', 'success')
    else:
        flash('Tank not found.', 'error')

    return redirect(url_for('index'))

@app.route('/german_tanks')
def german_tanks():
    # Fetch all tanks from Germany
    tanks = list(tanks_collection.find({"country": "Germany"}, {'_id': False}))
    return render_template('german_tanks.html', tanks=tanks)

if __name__ == '__main__':
    initialize_database()  # Initialize the database with German tank data
    app.run(debug=True)
