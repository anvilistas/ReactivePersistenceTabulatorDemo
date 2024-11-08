from anvil_extras import persistence as ps


@ps.persisted_class
class Author:
    key = "name"


@ps.persisted_class
class Book:
    key = "isbn_13"
    author = Author