"""
SERIALIZATION
"""

from marshmallow import Schema, fields


class BookSchema(Schema):
    """
    BookSchema class.
    """
    title = fields.Str()
    author = fields.Str()


class Book:
    """
    Book class.
    """

    def __init__(self, title, author, description):
        self.title = title
        self.author = author
        self.description = description


book = Book("Clean code", "Bob Martin", "A book about writing cleaner code.")

book_schema = BookSchema()
book_dict = book_schema.dump(book)

print(book_dict)
