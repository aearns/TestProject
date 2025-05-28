import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import MagicMock
import requests

from api import BooksAPI
from books import BookDir

def test_search_books_success(mocker):
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
                    "authors": ["Kofi Kankam"],
                    "publishedDate": "2022-05-15",
                }
            }
        ]
    }
    mock_response.raise_for_status = MagicMock()
    mock_requests_get = mocker.patch('requests.get', return_value=mock_response)

    api = BooksAPI()
    books = api.search_book("Python")

    assert len(books) == 2
    assert books[0].title == "DSA"
    assert "Kofi Braimah" in books[0].authors
    assert books[0].published_date == "2023-01-01"
    assert books[1].title == "Data Science Basics"
    assert "Kofi Kankam" in books[1].authors
    assert books[1].published_date == "2022-05-15"


def test_search_books_no_results(mocker):
    """Test API response with no items found."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": []}
    mock_response.raise_for_status = MagicMock()
    mock_requests_get = mocker.patch('requests.get', return_value=mock_response)

    api = BooksAPI()
    books = api.search_book("NonExistentBook")

    assert len(books) == 0


def test_search_books_api_error(mocker):
    """Test API response for HTTP errors (e.g., 404, 500)."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    mock_requests_get = mocker.patch('requests.get', return_value=mock_response)

    api = BooksAPI()
    books = api.search_book("ErrorTest")

    assert len(books) == 0


def test_search_books_network_error(mocker):
    """Test for network connection errors."""
    mocker.patch('requests.get', side_effect=requests.exceptions.ConnectionError("Connection Refused"))

    api = BooksAPI()
    books = api.search_book("NetworkFail")

    assert len(books) == 0


def test_search_books_malformed_json(mocker):
    """Test handling of malformed JSON response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("Malformed JSON")
    mock_response.raise_for_status = MagicMock()
    mock_requests_get = mocker.patch('requests.get', return_value=mock_response)

    api = BooksAPI()
    books = api.search_book("BadJson")

    assert len(books) == 0