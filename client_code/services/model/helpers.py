from anvil.server import portable_class, server_method
from app.services.exceptions import ChildExists, KeyExists


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
        if len(results) > 0:
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
class WithUniqueKey(WithView):
    key = None

    @classmethod
    def _do_create(cls, values, from_client):
        key_value = values[cls.key]
        search_params = {cls.key: key_value}
        existing = cls.get_view().search(**search_params)
        if len(existing) > 0:
            raise KeyExists(f"An instance with {cls.key}: {key_value} already exists")
        return super()._do_create(values, from_client)


@portable_class
class WithLinks:
    links = []

    def _do_delete(self, from_client):
        for link in self.links:
            link.on_delete(self)
        super()._do_delete(from_client)
