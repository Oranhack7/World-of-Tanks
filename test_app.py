from app import app
from pymongo import MongoClient
import pytest

@pytest.fixture(scope="module")
def client():
    # Configure the app for testing
    app.config['TESTING'] = True
    with app.test_client() as testing_client:
        yield testing_client

@pytest.fixture(scope="module")
def mongodb():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['test_tanksdb']
    tanks_collection = db['test_tanks']
    yield tanks_collection
    client.drop_database('test_tanksdb')

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    # Adjusted to check for the presence of "Tanks Database" which appears in the title of your index page.
    assert b'Tanks Database' in response.data

def test_german_tanks_page(client):
    response = client.get('/german_tanks')
    assert response.status_code == 200
    # Assuming "German Tanks" is a text you expect to find on the german_tanks page. Adjust as necessary.
    assert b'Germany' in response.data  # Adjust based on actual content
