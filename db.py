# db.py
from flask import Flask, render_template
from pymongo import MongoClient
import os 

app = Flask(__name__)

# Connect to MongoDB
mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://mongo-mongodb:27017/')
client = MongoClient(mongodb_uri)
db = client['tanksdb']
tanks_collection = db['tanks']

@app.route('/')
def index():
    # Fetch tank data from MongoDB
    tanks = tanks_collection.find()
    return render_template('index.html', tanks=tanks)

if __name__ == '__main__':
    app.run(debug=True)

# Close the connection to the MongoDB server
client.close()