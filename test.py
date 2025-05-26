# test_app.py

import pytest
import os
import re # Import regex for more flexible string matching

# Import the Flask app instance from your main application file
# Assuming your Flask app is in a file named 'app.py'
from app import app, VERSION

@pytest.fixture
def client():
    """
    A pytest fixture that provides a test client for the Flask application.
    This allows us to make requests to the app without running a live server.
    """
    # Set Flask to testing mode
    app.config['TESTING'] = True
    # Use a test client to make requests
    with app.test_client() as client:
        yield client # This yields the client to the test functions

def test_hello_route(client):
    """
    Tests the '/' (hello) route of the Flask application.
    """
    # Simulate an OS environment variable for HOSTNAME for consistent testing
    # In a real container, this would be dynamically set.
    # We'll temporarily set it for the test.
    original_hostname = os.environ.get('HOSTNAME')
    os.environ['HOSTNAME'] = 'test-instance-123'

    try:
        response = client.get('/')
        # Check if the status code is 200 OK
        assert response.status_code == 200
        # Decode the response data to a string
        response_text = response.data.decode('utf-8')

        # Check if the response contains the correct version
        assert f"HelloWorld version: {VERSION}" in response_text

        # Check if the response contains the instance hostname
        # Use regex to be flexible about whitespace around "instance"
        assert re.search(r'instance\s*test-instance-123', response_text) is not None

        print(f"\nTest / passed. Response: {response_text.strip()}")

    finally:
        # Clean up: restore original HOSTNAME environment variable
        if original_hostname is not None:
            os.environ['HOSTNAME'] = original_hostname
        else:
            del os.environ['HOSTNAME'] # Remove if it wasn't set before

def test_health_route(client):
    """
    Tests the '/health' route of the Flask application.
    """
    response = client.get('/health')
    # Check if the status code is 200 OK
    assert response.status_code == 200
    # Check if the response text is exactly 'Helloworld is healthy'
    assert response.data.decode('utf-8') == 'Helloworld is healthy'

    print(f"\nTest /health passed. Response: {response.data.decode('utf-8').strip()}")
