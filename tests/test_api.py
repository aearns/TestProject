import pytest
from unittest.mock import MagicMock
import requests

from api import BooksAPI
from books import BookDir

@pytest.fixture
def mock_requests_get(mocker):
    """Fixture to mock requests.get for API calls."""
    return mocker.patch('requests.get')

def test_search_books_success(mock_requests_get):
    """Test successful API response with multiple books."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {
                "volumeInfo": {
                    "title": "DSA",
                    "authors": ["Kofi Braimah", "Ama Ghana"],
                    "publishedDate": "2023-01-01",
                }
            },
            {
                "volumeInfo": {
                    "title": "Data Science Basics",
                    "authors": ["Alice Brown"],
                    "publishedDate": "2022-05-15",
                }
            }
        ]
    }
    mock_requests_get.return_value = mock_response

    api = BooksAPI()
    books = api.search_books("Python")

    assert len(books) == 2
    assert books[0].title == "Python Programming"
    assert "John Doe" in books[0].authors
    assert books[0].published_date == "2023-01-01"
    assert "comprehensive" in books[0].description
    assert len(books[0].isbns) == 2
    assert books[1].title == "Data Science Basics"
    assert "Alice Brown" in books[1].authors
    assert len(books[1].isbns) == 0

def test_search_books_no_results(mock_requests_get):
    """Test API response with no items found."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": []} # No items key or empty list
    mock_requests_get.return_value = mock_response

    api = BooksAPI()
    books = api.search_books("NonExistentBook")

    assert len(books) == 0

def test_search_books_api_error(mock_requests_get):
    """Test API response for HTTP errors (e.g., 404, 500)."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    mock_requests_get.return_value = mock_response

    api = BooksAPI()
    books = api.search_books("ErrorTest")

    assert len(books) == 0


def test_search_books_network_error(mocker):
    """Test for network connection errors."""
    mocker.patch('requests.get', side_effect=requests.exceptions.ConnectionError("Connection Refused"))

    api = BooksAPI()
    books = api.search_books("NetworkFail")

    assert len(books) == 0

def test_search_books_malformed_json(mock_requests_get):
    """Test handling of malformed JSON response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("Malformed JSON") 
    mock_requests_get.return_value = mock_response

    api = BooksAPI()
    books = api.search_books("BadJson")

    assert len(books) == 0