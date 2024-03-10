import pytest
from app import app as flask_app  # Ensures correct import from your Flask app structure
from pymongo import MongoClient
import os

# Setup MongoDB test client and test database
@pytest.fixture(scope='module')
def mongodb():
    # Use an environment variable or fallback to a default test URI
    test_mongodb_uri = os.getenv('TEST_MONGODB_URI', 'mongodb://localhost:27017/test_tanksdb')
    client = MongoClient(test_mongodb_uri, serverSelectionTimeoutMS=5000)
    test_db = client["test_tanksdb"]
    yield test_db
    # Clean up the test database
    client.drop_database("test_tanksdb")

@pytest.fixture
def app(mongodb):
    flask_app.config['TESTING'] = True
    # Point the Flask app to the test MongoDB instance
    flask_app.config['MONGODB_URI'] = 'mongodb://localhost:27017/test_tanksdb'

    # Use the MongoDB setup for the test database
    db = mongodb
    tanks_collection = db['tanks']  # Assuming 'tanks' is the collection used in your app

    # Initialize database if necessary, e.g., with any required test data setup

    with flask_app.test_client() as client:
        with flask_app.app_context():
            pass  # Additional app context setup if necessary
    yield client

def test_china_tanks(app):
    response = app.get('/china_tanks')
    assert response.status_code == 200
    assert b'China' in response.data  # Update based on your actual china_tanks.html content

def test_france_tanks(app):
    response = app.get('/france_tanks')
    assert response.status_code == 200
    assert b'France' in response.data  # Update based on your actual france_tanks.html content

def test_germany_tanks(app):
    response = app.get('/germany_tanks')
    assert response.status_code == 200
    assert b'Germany' in response.data  # Update based on your actual germany_tanks.html content

def test_japan_tanks(app):
    response = app.get('/japan_tanks')
    assert response.status_code == 200
    assert b'Japan' in response.data  # Update based on your actual japan_tanks.html content

def test_russia_tanks(app):
    response = app.get('/russia_tanks')
    assert response.status_code == 200
    assert b'Russia' in response.data  # Update based on your actual russia_tanks.html content

def test_uk_tanks(app):
    response = app.get('/uk_tanks')
    assert response.status_code == 200
    assert b'UK' in response.data  # Update based on your actual uk_tanks.html content

def test_usa_tanks(app):
    response = app.get('/usa_tanks')
    assert response.status_code == 200
    assert b'USA' in response.data  # Update based on your actual usa_tanks.html content

def test_add_tank(app):
    response = app.post('/add_tank', data=dict(
        name='Test Tank',
        type='Medium',
        country='Testland',
        year='2021'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Tank successfully added!' in response.data

def test_delete_tank(app):
    app.post('/add_tank', data=dict(
        name='Test Tank Delete',
        type='Medium',
        country='Testland',
        year='2021'
    ), follow_redirects=True)
    response = app.post('/delete_tank', data=dict(
        name='Test Tank Delete'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Tank successfully deleted!' in response.data

def test_remove_all_tanks(app):
    response = app.post('/remove_all_tanks', follow_redirects=True)
    assert response.status_code == 200
    assert b'All tanks have been successfully removed!' in response.data
