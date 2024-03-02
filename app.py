# db.py
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['tanksdb']
tanks_collection = db['tanks']

@app.route('/')
def index():
    # Fetch tank data from MongoDB
    tanks = tanks_collection.find()
    return render_template('index.html', tanks=tanks)

@app.route('/add_tank', methods=['POST'])
def add_tank():
    if request.method == 'POST':
        name = request.form['name']
        tank_type = request.form['type']
        country = request.form['country']
        year = request.form['year']
        
        # Insert tank into MongoDB
        tanks_collection.insert_one({'name': name, 'type': tank_type, 'country': country, 'year': year})
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
