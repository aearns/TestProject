# Test Project for a Mini Book Search CLI Tool

A command-line interface tool that allows users to search for books using the Google Books API, view results, and save their favorite books to a local JSON file.

---

## Features

-   **Search Books:** Search for books by title or author using the Google Books API.
-   **Display Results:** Shows the top 5 relevant results including Title, Author(s), and Published Date.
-   **Save Favorites:** Select and save desired books to a local `saved_books.json` file. Saved books include Title, Author(s), and Published Date.
-   **View Saved Books:** List all books previously saved by the user.
-   **Pagination:** Supports viewing additional search results beyond the initial 5.
-   **Rich TUI:** Utilizes the `rich` library for an enhanced and colorful terminal UI.

---

## Setup Instructions

1.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## How to Run the Tool

Once the setup is complete, run the main application:

```bash
python main.py
```

---

## Usage

When you run the tool, you will be presented with a main menu:

1.  **Search for books:** Allows you to enter a query (book title or author) to search the Google Books API.
2.  **View saved books:** Displays the list of books you have previously saved.
3.  **Exit:** Quits the application.

### Searching for Books:

- Enter your search query when prompted.
- The tool will display the top 5 results.
- You can then:
    - Enter the number corresponding to a book to save it.
    - Type `n` to view the next page of results.
    - Type `b` to go back to the main menu.

---

## Running Tests

The project includes unit tests using `pytest`. To run the tests:

1.  Ensure your virtual environment is activated.
2.  Navigate to the project's root directory in your terminal.
3.  Run the following command:
    ```bash
    pytest
    ```

You can also use the following options:
-   `pytest -v`: For more verbose output, showing details for each test.
-   `pytest -s`: To show print statements during test execution (useful for debugging test logic).
