import anvil.server
from anvil_extras.logging import Logger
from anvil_reactive.main import reactive_class, signal, computed

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

    def __init__(self, persisted_class, logger=None, cache=None):
        self._logger = logger or _null_logger
        if in_designer:
            self._logger.disabled = True
        self.persisted_class = persisted_class
        self._class_name = _snakify(persisted_class.__name__)
        self.view = None
        self._logger.debug(
            f"PersistedClassStore: Initialised for {self.persisted_class.__name__:}"
        )

    def _log_action(self, msg):
        self._logger.debug(f"{self.__class__.__name__}: {msg}")

    # @computed
    @property
    def list_search(self):
        return list(self.search())

    # @computed
    @property
    def dropdown_items(self):
        return [(str(item), item) for item in self.list_search]

    def create(self, instance):
        instance.add()
        self._log_action(f"instance {getattr(instance, instance.key)} added.")
        self.changed += 1

    def delete(self, instance):
        key = getattr(instance, instance.key)
        instance.delete()
        self._log_action(f"instance {key} deleted.")
        self.changed += 1

    def update(self, instance):
        instance.update()
        self._log_action(f"instance {getattr(instance, instance.key)} updated.")
        self.changed += 1

    def search(self):
        self.initialise()
        _ = self.changed
        return (self.persisted_class(row) for row in self.view.search())

    def initialise(self):
        if self.view is None:
            self._log_action("no view found. Fetching...")
            self.refresh()

    def refresh(self):
        self.loading = True
        self.view = anvil.server.call_s(f"get_{self._class_name}_view")
        self._log_action("view refreshed.")
        self.changed += 1
        self.loading = False
