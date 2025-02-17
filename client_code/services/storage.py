import anvil.server
from anvil_extras.logging import Logger
from anvil_reactive.main import computed, signal

try:
    from anvil.designer import in_designer
except ImportError:
    in_designer = False


_null_logger = Logger()
_null_logger.disabled = True


def _snakify(text):
    return "".join("_" + c.lower() if c.isupper() else c for c in text).lstrip("_")


class PersistedClassStore:
    changed = signal(0)
    loading = signal(True)

    def __init__(self, persisted_class, linked_stores=None, logger=None, cache=None):
        """
        linked_stores: dict
            of the form:
            PersistedClassStore instance: linked column name
        """
        self.linked_stores = linked_stores or {}
        self._logger = logger or _null_logger
        if in_designer:
            self._logger.disabled = True
        self.persisted_class = persisted_class
        self._class_name = _snakify(persisted_class.__name__)
        self.view = None
        self._logger.debug(
            f"PersistedClassStore: Initialised for {self.persisted_class.__name__:}"
        )

    def __len__(self):
        return len(self.view.search()) if self.view is not None else 0

    def _log_action(self, msg):
        self._logger.debug(f"{self.__class__.__name__}: {msg}")

    @computed
    @property
    def list_search(self):
        return list(self.search())

    @computed
    @property
    def dropdown_items(self):
        return [(str(item), item) for item in self.list_search]

    def get(self, key):
        row = anvil.server.call_s(f"get_{self._class_name}", key)
        return self.persisted_class(row)

    def create(self, instance):
        instance.add()
        self._log_action(f"instance {getattr(instance, instance.key)} added.")
        self.changed += 1

    def delete(self, instance):
        key = getattr(instance, instance.key)
        linked = {
            store.persisted_class: store.search(**{linked_column: instance._store})
            for store, linked_column in self.linked_stores.items()
        }
        instance.delete(linked=linked)
        for store in self.linked_stores:
            self._log_action(f"Refreshing {store.persisted_class.__name__} store")
            store.refresh()
        self._log_action(f"{self.persisted_class.__name__} instance {key} deleted.")
        self.changed += 1

    def update(self, instance):
        instance.update()
        self._log_action(f"instance {getattr(instance, instance.key)} updated.")
        self.changed += 1

    def search(self, *args, **kwargs):
        self.initialise()
        _ = self.changed
        return (self.persisted_class(row) for row in self.view.search(*args, **kwargs))

    def initialise(self):
        if self.view is None:
            self._log_action("no view found. Fetching...")
            self.refresh()

    def refresh(self, **kwargs):
        self.loading = True
        self.view = anvil.server.call_s(f"get_{self._class_name}_view", **kwargs)
        self._log_action(f"{self._class_name} view refreshed.")
        self.changed += 1
        self.loading = False
