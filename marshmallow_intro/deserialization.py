"""
DESERIALIZATION

-- Undefined Columns in Schema --

The schema has to know the incoming data.
If that is not the case, i.e. there is a column or there are columns there were not defined in the schema,
then marshmallow will throw an error.

To avoid this,
1. It is possible to define those columns in BookSchema class.
2. It is possible to set unknown = INCLUDE: It will ignore this problem.
3. It is possible to set unknown = EXCLUDE: It will NOT except the columns that are undefined in the schema.

-- Data Validation --

Marshmallow makes it possible to validate data.
Data validation is a check for the input schema.
To implement validation, we can set required=True while defining fields in the BookSchema.

"""

from marshmallow import Schema, fields, INCLUDE, EXCLUDE


class BookSchema(Schema):
    """
    The schema for Book class.
    """
    title = fields.Str()
    author = fields.Str()
    description = fields.Str()


class Book:
    """
    Book class.
    """

    def __init__(self, title, author):
        self.title = title
        self.author = author


incoming_book_data = {
    "title": "Clean Code",
    "author": "Bob Martin",
    # "description": "A book about writing cleaner code."
}

book_schema = BookSchema()
book = book_schema.load(incoming_book_data)
book_obj = Book(**book)

print(book_obj.title)
