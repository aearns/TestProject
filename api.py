import requests
from books import BookDir
import json

class BooksAPI:
    """
    Fetching data from Google books API
    """
    Base_URL = "https://www.googleapis.com/books/v1/volumes"

    def __init__(self, api_key=None):
        self.api_key = api_key

    def search_book(self, query, top_results=5, start_index=0):
        """
        Search for books using title or author.

        Args:
            query (_type_): _description_
            top_results (int, optional): _description_. Defaults to 5.
            start_index (int, optional): _description_. Defaults to 0.

        Returns:
            list[BookDir]
        """
        params = {
            "q": query,
            "startIndex": start_index,
            "topResults": top_results
        }
    
        if self.api_key:
            params["key"] = self.api_key
        
        try:
            response = requests.get(self.Base_URL, params=params)
            response.raise_for_status()
            data = response.json()

            print("\n--- Raw API Response (for debugging) ---")
            print(json.dumps(data, indent=2))
            print("----------------------------------------\n")

            books = []
            if "items" in data:
                for item in data["items"]:
                    volume_info = item.get("volumenInfo", {})
                    title = volume_info.get("title", "N/A")
                    authors = volume_info.get("authors", "N/A")
                    published_date = volume_info.get("publishedDate", "N/A")

                    book = BookDir(
                        title = title,
                        authors = authors,
                        published_date = published_date
                    )

                    books.append(book)
            return books
        

        except requests.exceptions.ConnectionError as e:
            print(f"Network Error: Try connecting to internet. {e}")
            return []
        except requests.exceptions.Timeout as e:
            print(f"Timeout Error: Request to Google Books API timed out. {e}")
            return []
        except requests.exceptions.RequestException as e:
            print(f"An unexpected error occurred during the API request: {e}")
            return []
        except ValueError as e:
            print(f"Error parsing JSON response from API: {e}")
            return []