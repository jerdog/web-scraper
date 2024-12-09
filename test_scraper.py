import pytest
from scraper import fetch_page

def test_fetch_page():
    url = "https://example.com"
    response = fetch_page(url, None)  # Pass a mock session if needed
    assert response is not None, "Failed to fetch example.com"
