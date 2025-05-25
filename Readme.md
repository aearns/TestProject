# Mini Book Search CLI Tool

A command-line interface tool that allows users to search for books using the Google Books API, view results, and save their favorite books to a local JSON file.

---

## Features

-   **Search Books:** Search for books by title or author using the Google Books API.
-   **Display Results:** Shows the top 5 relevant results including Title, Author(s), and Published Date.
-   **Save Favorites:** Select and save desired books to a local `saved_books.json` file. Saved books include Title, Author(s), Published Date, Description, and ISBN(s).
-   **View Saved Books:** List all books previously saved by the user.
-   **Pagination :** Supports viewing additional search results beyond the initial 5.
-   **Rich TUI :** Utilizes the `rich` library for an enhanced and colorful terminal UI.

---

## Setup Instructions

1.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
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