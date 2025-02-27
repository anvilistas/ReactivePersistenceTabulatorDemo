from anvil_extras.logging import Logger
from anvil_reactive.main import computed, signal
from anvil.server import no_loading_indicator
import datetime as dt

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
    loading_since = dt.datetime.now()

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

    def save(self, instance):
        instance.save()
        self._log_action(f"{instance.__class__.__name__} instance {instance.key} saved.")
        self.changed += 1

    def delete(self, instance):
        key = getattr(instance, instance.key)
        instance.delete()
        self._log_action(f"{self.persisted_class.__name__} instance {key} deleted.")
        self.changed += 1

    def update(self, instance):
        instance.update()
        self._log_action(f"instance {getattr(instance, instance.key)} updated.")
        self.changed += 1

    def search(self, *args, **kwargs):
        self.initialise()
        _ = self.changed
        return self.view.search(*args, **kwargs)

    def initialise(self):
        if self.view is None:
            self._log_action("no view found. Fetching...")
            self.refresh()

    def refresh(self, **kwargs):
        self.loading_since = dt.datetime.now()
        self.loading = True
        with no_loading_indicator:
            self.view = self.persisted_class.get_view()
        self._log_action(f"{self._class_name} view refreshed.")
        self.changed += 1
        self.loading = False
        self.loading_since = None
