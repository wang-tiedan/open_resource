import unittest
from open_resource_service import app 

class FlaskTestCase(unittest.TestCase):

  # Run once before all tests
  @classmethod
  def setUpClass(cls):
      # Set up test client
      cls.client = app.test_client()
      # Set the Flask application in test mode
      app.config['TESTING'] = True

  # Test homepage
  def test_index(self):
      # Send HTTP GET request to application
      response = self.client.get('/')
      # Make sure the request is successful
      self.assertEqual(response.status_code, 200)
      # More assertions can be added to check the returned HTML content

  # Test specific function pages
  def test_show_feature(self):
      # Assume there is a Feature_ID of 1
      feature_id = '1'
      # Send HTTP GET request to application
      response = self.client.get(f'/show/{feature_id}')
      # Make sure the request is successful
      self.assertEqual(response.status_code, 200)
     # You can add more assertions to check whether the returned HTML content contains relevant data with Feature_ID 1

if __name__ == '__main__':
  unittest.main()
