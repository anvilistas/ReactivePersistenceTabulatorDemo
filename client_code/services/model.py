from anvil.server import portable_class, server_method
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


@portable_class
class WithView:
    table = None

    @server_method
    @classmethod
    def get_view(cls):
        return cls.table.client_readable()


@portable_class
class WithLinks:
    links = []

    def _do_delete(self, from_client):
        for link in self.links:
            link.on_delete(self)
        super()._do_delete(from_client)


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
