import requests
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Book:
    title: str
    authors: List[str]
    published_date: str
    description: Optional[str]
    isbn: Optional[str]

class GoogleBooksAPI:
    BASE_URL = "https://www.googleapis.com/books/v1/volumes"
    
    def __init__(self):
        self.session = requests.Session()
    
    def search_books(self, query: str, max_results: int = 5) -> List[Book]:
        """
        Search for books using the Google Books API
        
        Args:
            query (str): Search query (title or author)
            max_results (int): Maximum number of results to return
            
        Returns:
            List[Book]: List of Book objects containing search results
        """
        try:
            params = {
                'q': query,
                'maxResults': max_results
            }
            
            response = self.session.get(self.BASE_URL, params=params)
            response.raise_for_status()
            
            data = response.json()
            books = []
            
            for item in data.get('items', []):
                volume_info = item.get('volumeInfo', {})
                
                # Extract ISBN if available
                isbn = None
                if 'industryIdentifiers' in volume_info:
                    for identifier in volume_info['industryIdentifiers']:
                        if identifier.get('type') == 'ISBN_13':
                            isbn = identifier.get('identifier')
                            break
                
                book = Book(
                    title=volume_info.get('title', 'Unknown Title'),
                    authors=volume_info.get('authors', ['Unknown Author']),
                    published_date=volume_info.get('publishedDate', 'Unknown Date'),
                    description=volume_info.get('description'),
                    isbn=isbn
                )
                books.append(book)
            
            return books
            
        except requests.RequestException as e:
            print(f"Error searching books: {str(e)}")
            return [] 