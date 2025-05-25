import requests

from books

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
            list[Book]
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

            books = []
            if "items" in data:
                for item in data["items"]:
                    title_info = item.get("volume")
                    title = volume_info.get("title", "N/A")