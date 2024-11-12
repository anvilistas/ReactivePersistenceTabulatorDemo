from anvil_extras import persistence as ps
from anvil_reactive.main import reactive_class


@reactive_class
@ps.persisted_class
class Author:
    key = "name"

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if not isinstance(other, Author):
            return NotImplemented
        return self._store is not None and self._store == other._store


@reactive_class
@ps.persisted_class
class Book:
    key = "isbn_13"
    author = Author
