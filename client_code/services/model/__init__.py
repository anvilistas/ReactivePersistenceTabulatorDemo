from anvil.tables import app_tables
from anvil_reactive.main import reactive_class

from .helpers import LinkedClass, WithLinks, WithUniqueKey


@reactive_class
class Book(
    WithUniqueKey, app_tables.book.Row, buffered=True, attrs=True, client_writable=True
):
    table = app_tables.book
    index_title = "Books"
    key = "isbn_13"


@reactive_class
class Author(
    WithLinks,
    WithUniqueKey,
    app_tables.author.Row,
    buffered=True,
    attrs=True,
    client_writable=True,
):
    table = app_tables.author
    key = "name"
    index_title = "Authors"
    links = [LinkedClass(Book, column="author", on_delete="restrict")]

    def __str__(self):
        return self.name
