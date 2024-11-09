from anvil_extras import persistence as ps
from anvil_reactive.main import reactive_class


@reactive_class
@ps.persisted_class
class Author:
    key = "name"


@reactive_class
@ps.persisted_class
class Book:
    key = "isbn_13"
    author = Author