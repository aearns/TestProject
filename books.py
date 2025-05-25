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

    def __repr__(self):
        return f"Book(title={self.title}, authors={self.authors}, published_date={self.published_date})"

    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return (self.title == other.title and
                self.authors == other.authors and 
                self.published_date == other.published_date)
        

