import anvil.server
from anvil_extras import persistence as ps
from anvil_reactive.main import reactive_class


@reactive_class
@ps.persisted_class
class Author:
    key = "name"

    def __str__(self):
        return self.name

    def delete(self, linked=None, *args, **kwargs):
        """
        linked: dict
            of the form:
            {Model Class: iterable of Model Class instances}
        """
        rows = [book._store for book in linked[Book]]
        rows.append(self._store)
        anvil.server.call("delete_rows", rows)
        self._delta.clear()


@reactive_class
@ps.persisted_class
class Book:
    key = "isbn_13"
    author = Author
