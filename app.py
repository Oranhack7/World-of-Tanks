from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import bson
import os
#
app = Flask(__name__)
app.secret_key = 'your_secret_key'

mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://mongo:27017/')
# Connect to MongoDB
client = MongoClient(mongodb_uri)
db = client['tanksdb']
tanks_collection = db['tanks']

def format_country_name(country):
    if country.lower() == "uk":
        return "UK"
    elif country.lower() == "usa":
        return "USA"
    else:
        return country.capitalize()

def initialize_database(): #PreBuilt DATABASE.
    # Check if the collection is empty
    if tanks_collection.count_documents({}) == 0:
        # german tanks data
        germany_tanks = [
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
        tanks_collection.insert_many(germany_tanks)
        print('Database initialized with the tank data of Germany.')

        # USA tanks data
        usa_tanks = [
            {"name": "M1917", "type": "Light Tank", "country": "USA", "year": 1917},
            {"name": "M2", "type": "Medium Tank", "country": "USA", "year": 1939},
            {"name": "M3 Stuart", "type": "Light Tank", "country": "USA", "year": 1941},
            {"name": "M4 Sherman", "type": "Medium Tank", "country": "USA", "year": 1942},
            {"name": "M26 Pershing", "type": "Heavy Tank", "country": "USA", "year": 1945},
            {"name": "M48 Patton", "type": "Main Battle Tank", "country": "USA", "year": 1952},
            {"name": "M60 Patton", "type": "Main Battle Tank", "country": "USA", "year": 1960},
            {"name": "M1 Abrams", "type": "Main Battle Tank", "country": "USA", "year": 1980},
        ]
        tanks_collection.insert_many(usa_tanks)
        print('Database initialized with the tank data of USA.')

        # UK tanks data
        uk_tanks = [
            {"name": "Mark I", "type": "Heavy Tank", "country": "UK", "year": 1916},
            {"name": "Matilda II", "type": "Infantry Tank", "country": "UK", "year": 1937},
            {"name": "Cruiser Mk IV", "type": "Cruiser Tank", "country": "UK", "year": 1939},
            {"name": "Churchill", "type": "Infantry Tank", "country": "UK", "year": 1941},
            {"name": "Cromwell", "type": "Cruiser Tank", "country": "UK", "year": 1943},
            {"name": "Comet", "type": "Cruiser Tank", "country": "UK", "year": 1944},
            {"name": "Centurion", "type": "Main Battle Tank", "country": "UK", "year": 1945},
            {"name": "Chieftain", "type": "Main Battle Tank", "country": "UK", "year": 1966},
            {"name": "Challenger 1", "type": "Main Battle Tank", "country": "UK", "year": 1983},
            {"name": "Challenger 2", "type": "Main Battle Tank", "country": "UK", "year": 1998},
        ]
        tanks_collection.insert_many(uk_tanks)
        print('Database initialized with the tank data of UK.')

        # Russian tanks data
        russia_tanks = [
            {"name": "T-18 (MS-1)", "type": "Light Tank", "country": "Russia", "year": 1928},
            {"name": "BT-2", "type": "Light Tank", "country": "Russia", "year": 1932},
            {"name": "KV-1", "type": "Heavy Tank", "country": "Russia", "year": 1939},
            {"name": "T-34", "type": "Medium Tank", "country": "Russia", "year": 1940},
            {"name": "IS-2", "type": "Heavy Tank", "country": "Russia", "year": 1944},
            {"name": "T-54", "type": "Main Battle Tank", "country": "Russia", "year": 1947},
            {"name": "T-62", "type": "Main Battle Tank", "country": "Russia", "year": 1961},
            {"name": "T-72", "type": "Main Battle Tank", "country": "Russia", "year": 1973},
            {"name": "T-80", "type": "Main Battle Tank", "country": "Russia", "year": 1976},
            {"name": "T-90", "type": "Main Battle Tank", "country": "Russia", "year": 1992},
            {"name": "T-14 Armata", "type": "Main Battle Tank", "country": "Russia", "year": 2015},
        ]
        tanks_collection.insert_many(russia_tanks)
        print('Database initialized with the tank data of Russia.')

        # Chinese tanks data
        china_tanks = [
            {"name": "Type 58", "type": "Medium Tank", "country": "China", "year": 1958},
            {"name": "Type 59", "type": "Main Battle Tank", "country": "China", "year": 1959},
            {"name": "Type 62", "type": "Light Tank", "country": "China", "year": 1963},
            {"name": "Type 63", "type": "Amphibious Light Tank", "country": "China", "year": 1963},
            {"name": "Type 69/79", "type": "Main Battle Tank", "country": "China", "year": 1974},
            {"name": "Type 80/88", "type": "Main Battle Tank", "country": "China", "year": 1980},
            {"name": "Type 85/90", "type": "Main Battle Tank", "country": "China", "year": 1985},
            {"name": "Type 96", "type": "Main Battle Tank", "country": "China", "year": 1996},
            {"name": "Type 99", "type": "Main Battle Tank", "country": "China", "year": 2001},
            {"name": "Type 15", "type": "Light Tank", "country": "China", "year": 2018},
        ]
        tanks_collection.insert_many(china_tanks)
        print('Database initialized with the tank data of China.')

        # Japanese tanks data
        japan_tanks = [
            {"name": "Type 89 I-Go", "type": "Medium Tank", "country": "Japan", "year": 1928},
            {"name": "Type 95 Ha-Go", "type": "Light Tank", "country": "Japan", "year": 1935},
            {"name": "Type 97 Chi-Ha", "type": "Medium Tank", "country": "Japan", "year": 1937},
            {"name": "Type 2 Ka-Mi", "type": "Amphibious Light Tank", "country": "Japan", "year": 1942},
            {"name": "Type 3 Chi-Nu", "type": "Medium Tank", "country": "Japan", "year": 1943},
            {"name": "Type 4 Chi-To", "type": "Medium Tank", "country": "Japan", "year": 1944},
            {"name": "Type 61", "type": "Main Battle Tank", "country": "Japan", "year": 1961},
            {"name": "Type 90", "type": "Main Battle Tank", "country": "Japan", "year": 1990},
            {"name": "Type 10", "type": "Main Battle Tank", "country": "Japan", "year": 2010},
        ]
        tanks_collection.insert_many(japan_tanks)
        print('Database initialized with the tank data of Japan.')

        # French tanks data
        france_tanks = [
            {"name": "Renault FT", "type": "Light Tank", "country": "France", "year": 1917},
            {"name": "Char B1", "type": "Heavy Tank", "country": "France", "year": 1935},
            {"name": "SOMUA S35", "type": "Medium Tank", "country": "France", "year": 1936},
            {"name": "AMX-13", "type": "Light Tank", "country": "France", "year": 1953},
            {"name": "AMX-30", "type": "Main Battle Tank", "country": "France", "year": 1966},
            {"name": "AMX-40", "type": "Main Battle Tank", "country": "France", "year": 1980},
            {"name": "Leclerc", "type": "Main Battle Tank", "country": "France", "year": 1992},
        ]
        tanks_collection.insert_many(france_tanks)
        print('Database initialized with the tank data of France.')

@app.route('/')
def index():
    tanks = list(tanks_collection.find({}, {'_id': False}).sort("year", 1)) # Sort tanks by year in ascending order
    return render_template('index.html', tanks=tanks)

@app.route('/add_tank', methods=['POST'])
def add_tank():
    tank_name = request.form.get('name')
    tank_type = request.form.get('type')
    raw_tank_country = request.form.get('country')
    print(f"Raw country input: {raw_tank_country}")  # Debug print

    tank_country = format_country_name(raw_tank_country.lower())
    print(f"Formatted country: {tank_country}")  # Debug print

    tank_year_str = request.form.get('year')
    
    try:
        tank_year = int(tank_year_str)
        tank_data = {
            "name": tank_name,
            "type": tank_type,
            "country": tank_country,  # Use the formatted country name
            "year": tank_year
        }
        print(f"Tank data being inserted: {tank_data}")  # Debug print
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

@app.route('/remove_all_tanks', methods=['POST'])
def remove_all_tanks():
    tanks_collection.delete_many({})
    flash('All tanks have been successfully removed!', 'success')
    return redirect(url_for('index'))

@app.route('/germany_tanks')
def germany_tanks():
    tanks = list(tanks_collection.find({"country": "Germany"}, {'_id': False}).sort("year", 1))
    # Format country names before sending to the template
    for tank in tanks:
        tank['country'] = format_country_name(tank['country'])
    return render_template('germany_tanks.html', tanks=tanks)

@app.route('/usa_tanks')
def usa_tanks():
    tanks = list(tanks_collection.find({"country": "USA"}, {'_id': False}).sort("year", 1))
    # Format country names before sending to the template
    for tank in tanks:
        tank['country'] = format_country_name(tank['country'])
    return render_template('usa_tanks.html', tanks=tanks)

@app.route('/uk_tanks')
def uk_tanks():
    tanks = list(tanks_collection.find({"country": "UK"}, {'_id': False}).sort("year", 1))
    # Format country names before sending to the template
    for tank in tanks:
        tank['country'] = format_country_name(tank['country'])
    return render_template('uk_tanks.html', tanks=tanks)

@app.route('/russia_tanks')
def russia_tanks():
    tanks = list(tanks_collection.find({"country": "Russia"}, {'_id': False}).sort("year", 1))
    # Format country names before sending to the template
    for tank in tanks:
        tank['country'] = format_country_name(tank['country'])
    return render_template('russia_tanks.html', tanks=tanks)

@app.route('/china_tanks')
def china_tanks():
    tanks = list(tanks_collection.find({"country": "China"}, {'_id': False}).sort("year", 1))
    # Format country names before sending to the template
    for tank in tanks:
        tank['country'] = format_country_name(tank['country'])
    return render_template('china_tanks.html', tanks=tanks)

@app.route('/japan_tanks')
def japan_tanks():
    tanks = list(tanks_collection.find({"country": "Japan"}, {'_id': False}).sort("year", 1))
    # Format country names before sending to the template
    for tank in tanks:
        tank['country'] = format_country_name(tank['country'])
    return render_template('japan_tanks.html', tanks=tanks)

@app.route('/france_tanks')
def france_tanks():
    tanks = list(tanks_collection.find({"country": "France"}, {'_id': False}).sort("year", 1))
    # Format country names before sending to the template
    for tank in tanks:
        tank['country'] = format_country_name(tank['country'])
    return render_template('france_tanks.html', tanks=tanks)

if __name__ == '__main__':
    initialize_database()  # Initialize the database with tanks data
    app.run(host="0.0.0.0", port=5000, debug=True)