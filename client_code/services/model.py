from anvil.server import server_method
from anvil.tables import app_tables
from anvil_reactive.main import reactive_class

from .exceptions import ChildExists


class LinkedClass:
    def __init__(self, klass, column, on_delete):
        self.klass = klass
        self.column = column
        delete_actions = {
            "restrict": self.restrict_on_delete,
            "cascade": self.cascade_on_delete,
        }
        self.on_delete = delete_actions[on_delete]

    def restrict_on_delete(self, row):
        params = {self.column: row}
        results = self.klass.get_view().search(**params)
        if results:
            raise ChildExists("Child row found, cannot delete parent row")

    def cascade_on_delete(self, row):
        params = {self.column: row}
        self.klass.get_view().search(**params).delete_all_rows()


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
    links = [LinkedClass(Book, column="author", on_delete="restrict")]

    @server_method
    @classmethod
    def get_view(cls):
        return app_tables.author.client_readable()

    def __str__(self):
        return self.name

    def _do_delete(self, from_client):
        for link in self.links:
            link.on_delete(self)
        super()._do_delete(from_client)
