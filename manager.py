import json
import os
from books import BookDir

class SaveLoad:
    """
    Save and load books from file
    """

    def __ini__(self, file_path='saved_books.json'):
        self.file_path = file_path

    def view_book(self):
        """
        View books saved
        """
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, 'r', encoding='utf+8') as file:
                data = json.load(file)
                return [BookDir.from_dict(item) for item in data]
        except json.JSONDecodeError:
            print (f"Warning: File failed to load")
            return []
        except IOError as e:
            print(f"Error reading file {self.file_path}: {e}")
            return []

    def save_book(self, book):
        """
        Saves a single BookDir object to the local file.
        Add new book to existing ones.

        Args:
            book (BookDir): The Book object to save.
        """
        saved_books = self.view_books()     #confirm if book exists
      
        if any(b.title == book.title and b.authors == book.authors for b in saved_books):
            print(f"'{book.title}' by {', '.join(book.authors)} is already saved.")
            return

        saved_books.append(book)
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([b.to_dict() for b in saved_books], f, indent=4, ensure_ascii=False)
            print(f"'{book.title}' by {', '.join(book.authors)} saved successfully!")
        except IOError as e:
            print(f"Error writing to file {self.file_path}: {e}")