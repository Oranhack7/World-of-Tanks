from flask import Flask, render_template
from pymongo import MongoClient
from db import start_mongodb

app = Flask(__name__)

# Start MongoDB before running Flask app
start_mongodb()

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['tank_database']
collection = db['tanks']

@app.route('/')
def index():
    # Retrieve tank data from MongoDB
    tanks = list(collection.find())
    return render_template('index.html', tanks=tanks)

if __name__ == '__main__':
    app.run(debug=True)
