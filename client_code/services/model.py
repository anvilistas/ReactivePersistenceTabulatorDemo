from anvil.server import server_method
from anvil.tables import app_tables
from anvil_reactive.main import reactive_class


@reactive_class
class Author(app_tables.author.Row, buffered=True, attrs=True, client_writable=True):
    key = "name"

    @server_method
    @classmethod
    def get_view(cls):
        return app_tables.author.client_readable()

    def __str__(self):
        return self.name
    

@reactive_class
class Book(app_tables.book.Row, buffered=True, attrs=True, client_writable=True):
    key = "isbn_13"

    @server_method
    @classmethod
    def get_view(cls):
        return app_tables.book.client_readable()
