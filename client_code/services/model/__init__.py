from anvil.tables import app_tables
from anvil_reactive.main import reactive_class

from .helpers import LinkedClass, WithLinks, WithView


@reactive_class
class Book(
    WithView, app_tables.book.Row, buffered=True, attrs=True, client_writable=True
):
    table = app_tables.book
    key = "isbn_13"


@reactive_class
class Author(
    WithLinks,
    WithView,
    app_tables.author.Row,
    buffered=True,
    attrs=True,
    client_writable=True,
):
    table = app_tables.author
    key = "name"
    links = [LinkedClass(Book, column="author", on_delete="restrict")]

    def __str__(self):
        return self.name
