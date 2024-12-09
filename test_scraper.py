"""
Unit tests for the web scraper module.
"""

from unittest.mock import Mock
from scraper import fetch_page

def test_fetch_page():
    """
    Tests the fetch_page function to ensure it correctly fetches page content.
    """
    # Mock inputs
    mock_url = "https://example.com"
    mock_session = Mock()

    # Mock the response from session.get
    mock_response = Mock()
    mock_response.history = []  # No redirects
    mock_response.status_code = 200
    mock_response.text = "<html><body>Example</body></html>"
    mock_session.get.return_value = mock_response

    # Call the function
    result = fetch_page(mock_url, mock_session)

    # Validate the result
    assert result == "<html><body>Example</body></html>", (
    "fetch_page should return the HTML content"
    )
