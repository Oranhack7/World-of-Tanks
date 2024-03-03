import unittest
from app import app
from pymongo import MongoClient

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        # Configure the app for testing
        app.config['TESTING'] = True
        self.app = app.test_client()

        # Connect to test database
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client['test_tanksdb']
        
        # Use a separate collection for tests to avoid affecting production data
        self.tanks_collection = self.db['test_tanks']

    def tearDown(self):
        # Drop the test database to clean up after tests
        self.client.drop_database('test_tanksdb')

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        # Adjusted to check for the presence of "Tanks Database" which appears in the title of your index page.
        self.assertIn(b'Tanks Database', response.data)

    def test_german_tanks_page(self):
        response = self.app.get('/german_tanks')
        self.assertEqual(response.status_code, 200)
        # Assuming "German Tanks" is a text you expect to find on the german_tanks page. Adjust as necessary.
        self.assertIn(b'Germany', response.data)  # Adjust based on actual content

if __name__ == '__main__':
    unittest.main()
