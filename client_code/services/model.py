from anvil.server import server_method
from anvil.tables import app_tables
from anvil_reactive.main import reactive_class

from .exceptions import ChildExists


def restrict_on_delete(row, table, column):
    params = {column: row}
    results = table.search(**params)
    if results:
        raise ChildExists("Child row found, cannot delete parent row")


def cascade_on_delete(row, table, column):
    params = {column: row}
    table.search(**params).delete_all_rows()


@reactive_class
class Book(app_tables.book.Row, buffered=True, attrs=True, client_writable=True):
    key = "isbn_13"

    @server_method
    @classmethod
    def get_view(cls):
        return app_tables.book.client_readable()


@reactive_class
class Author(app_tables.author.Row, buffered=True, attrs=True, client_writable=True):
    key = "name"
    links = [{"class": Book, "column": "author", "on_delete": restrict_on_delete}]

    @server_method
    @classmethod
    def get_view(cls):
        return app_tables.author.client_readable()

    def __str__(self):
        return self.name

    def _do_delete(self, from_client):
        for link in self.links:
            view = link["class"].get_view()
            link["on_delete"](self, view, link["column"])
        super()._do_delete(from_client)
