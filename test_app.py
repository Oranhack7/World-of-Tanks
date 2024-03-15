import pytest
from app import app, db
from pymongo import MongoClient
import os

# Setup MongoDB test client and test database
@pytest.fixture(scope='module')
def mongodb():
    test_mongodb_uri = os.getenv('TEST_MONGODB_URI', 'mongodb://mongo-mongodb:27017/test_tanksdb')
    client = MongoClient(test_mongodb_uri, serverSelectionTimeoutMS=5000)
    test_db = client["test_tanksdb"]
    yield test_db
    client.drop_database("test_tanksdb")

# Configure Flask test client and use the test database for the duration of the tests
@pytest.fixture
def client(mongodb):
    app.config['TESTING'] = True
    app.config['MONGODB_URI'] = 'mongodb://mongo-mongodb:27017/test_tanksdb'
    db = mongodb
    tanks_collection = db['tanks']
    
    with app.test_client() as client:
        with app.app_context():
            # Initialize anything if needed
            pass
        yield client

def test_china_tanks(client):
    response = client.get('/china_tanks')
    assert response.status_code == 200
    assert b'China' in response.data  # Update based on your actual china_tanks.html content

def test_france_tanks(client):
    response = client.get('/france_tanks')
    assert response.status_code == 200
    assert b'France' in response.data  # Update based on your actual france_tanks.html content

def test_germany_tanks(client):
    response = client.get('/germany_tanks')
    assert response.status_code == 200
    assert b'Germany' in response.data  # Update based on your actual germany_tanks.html content

def test_japan_tanks(client):
    response = client.get('/japan_tanks')
    assert response.status_code == 200
    assert b'Japan' in response.data  # Update based on your actual japan_tanks.html content

def test_russia_tanks(client):
    response = client.get('/russia_tanks')
    assert response.status_code == 200
    assert b'Russia' in response.data  # Update based on your actual russia_tanks.html content

def test_uk_tanks(client):
    response = client.get('/uk_tanks')
    assert response.status_code == 200
    assert b'UK' in response.data  # Update based on your actual uk_tanks.html content

def test_usa_tanks(client):
    response = client.get('/usa_tanks')
    assert response.status_code == 200
    assert b'USA' in response.data  # Update based on your actual usa_tanks.html content

def test_add_tank(client):
    response = client.post('/add_tank', data=dict(
        name='Test Tank',
        type='Medium',
        country='Testland',
        year='2021'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Tank successfully added!' in response.data

def test_delete_tank(client):
    client.post('/add_tank', data=dict(
        name='Test Tank Delete',
        type='Medium',
        country='Testland',
        year='2021'
    ), follow_redirects=True)
    response = client.post('/delete_tank', data=dict(
        name='Test Tank Delete'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Tank successfully deleted!' in response.data

def test_remove_all_tanks(client):
    response = client.post('/remove_all_tanks', follow_redirects=True)
    assert response.status_code == 200
    assert b'All tanks have been successfully removed!' in response.data
