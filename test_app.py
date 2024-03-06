import pytest
from app import app as flask_app  # make sure this import matches the structure of your Flask app
from pymongo import MongoClient
import tempfile, os


@pytest.fixture
def app():
    db_fd, flask_app.config['DATABASE'] = tempfile.mkstemp()
    flask_app.config['TESTING'] = True

    with flask_app.test_client() as client:
        with flask_app.app_context():
            pass  # here you can initialize your test database if needed
    yield client

    os.close(db_fd)
    os.unlink(flask_app.config['DATABASE'])

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
