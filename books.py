import json

class Book:

    def __init__(self, title, authors=None, published_date=None):
        self.title = title
        self.authors = authors if authors is not None else []
        self.published_date = published_date

    def to_dict(self):
        return {
            "title": self.title,
            "authors": self.authors,
            "published_date": self.published_date
        }  

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data.get("title"),
            authors=data.get("authors", []),
            published_date=data.get("published_date")
        )

    def __str__(self):
        return f"Book(title={self.title}, authors={self.authors}, published_date={self.published_date})"
        
        

