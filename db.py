# db.py
from flask import Flask, render_template
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

if __name__ == '__main__':
    app.run(debug=True)