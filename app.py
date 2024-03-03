from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import bson

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ensure this is a strong, secret value in production

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['tanksdb']
tanks_collection = db['tanks']

@app.route('/')
def index():
    # Fetch tanks from the MongoDB collection and convert them to a list of dictionaries
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
    
    # Check if the tank exists before attempting to delete
    if tanks_collection.count_documents({"name": tank_name}) > 0:
        tanks_collection.delete_one({"name": tank_name})
        flash('Tank successfully deleted!', 'success')
    else:
        flash('Tank not found.', 'error')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
