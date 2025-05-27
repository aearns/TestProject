import pytest
import os
import json


from manager import SaveLoad
from books import BookDir

@pytest.fixture
def temp_json_file(tmp_path):
    """Fixture to create a temporary JSON file for testing."""
    file_path = tmp_path / "test_saved_books.json"
    yield str(file_path)
    

@pytest.fixture
def sample_books():
    """Fixture providing sample Book objects."""
    book1 = BookDir(
        title="Sample Book 1",
        authors=["Author A"],
        published_date="2020-01-01",
        description="Description for book 1.",
        isbns=[{"type": "ISBN_10", "identifier": "1234567890"}]
    )
    book2 = BookDir(
        title="Sample Book 2",
        authors=["Author B", "Author C"],
        published_date="2021-02-02",
        description="Description for book 2 with more details.",
        isbns=[]
    )
    return [book1, book2]

def test_load_books_empty_file(temp_json_file):
    """Test loading books from a non-existent or empty file."""
    manager = SaveLoad(temp_json_file)
    books = manager.load_books()
    assert len(books) == 0
    assert os.path.exists(temp_json_file) # Should create an empty file if it doesn't exist upon load attempt

def test_save_single_book(temp_json_file, sample_books):
    """Test saving a single book."""
    manager = SaveLoad(temp_json_file)
    book1 = sample_books[0]
    manager.save_book(book1)

    loaded_data = []
    with open(temp_json_file, 'r', encoding='utf-8') as f:
        loaded_data = json.load(f)

    assert len(loaded_data) == 1
    assert loaded_data[0]["title"] == book1.title
    assert loaded_data[0]["authors"] == book1.authors

def test_save_multiple_books_and_load(temp_json_file, sample_books):
    """Test saving multiple books sequentially and then loading them."""
    manager = SaveLoad(temp_json_file)
    book1, book2 = sample_books

    manager.save_book(book1)
    manager.save_book(book2)

    loaded_books = manager.load_books()

    assert len(loaded_books) == 2
    assert loaded_books[0] == book1
    assert loaded_books[1] == book2

def test_load_books_malformed_json(temp_json_file):
    """Test handling of malformed JSON in the saved file."""
    with open(temp_json_file, 'w', encoding='utf-8') as f:
        f.write("this is not valid json {")

    manager = SaveLoad(temp_json_file)
    books = manager.load_books()
    assert len(books) == 0

def test_save_duplicate_book(temp_json_file, sample_books, capsys):
    """Test that duplicate books are not saved."""
    manager = SaveLoad(temp_json_file)
    book1 = sample_books[0]

    manager.save_book(book1)
    manager.save_book(book1) # Try to save again

    loaded_books = manager.load_books()
    assert len(loaded_books) == 1 # Should only have one instance of the book

    captured = capsys.readouterr()
    assert f"'{book1.title}' by {', '.join(book1.authors)} is already saved." in captured.out

def test_book_equality(sample_books):
    """Test the __eq__ method of the Book class."""
    book1 = sample_books[0]
    book1_copy = BookDir(
        title="Sample Book 1",
        authors=["Author A"],
        published_date="2020-01-01",
        description="Description for book 1.",
        isbns=[{"type": "ISBN_10", "identifier": "1234567890"}]
    )
    book_different = sample_books[1]

    assert book1 == book1_copy
    assert book1 != book_different
    assert book1 != "not a book"