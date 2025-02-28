from anvil_extras.logging import Logger
from anvil_reactive.main import render_effect
from tabulator.Tabulator import Tabulator

from ._anvil_designer import ReactiveTabulatorTemplate

try:
    from anvil.designer import in_designer
except ImportError:
    in_designer = False

_null_logger = Logger()
_null_logger.disabled = True
_default_options = {
    "data_loader": False,
    "header_visible": False,
    "loading_indicator": False,
    "selectable": True,
    "pagination": False,
    "progressive_load": "scroll",
    "progressive_load_scroll_margin": 300,
}


class ReactiveTabulator(ReactiveTabulatorTemplate):
    def __init__(self, **properties):
        self._logger = _null_logger
        if in_designer:
            self.add_component(Tabulator(), full_width_row=True)
        self._store = None
        self._options = _default_options
        self._columns = []
        self._role = None
        self.tabulator = None
        self.init_components(**properties)

    def __getattr__(self, attr):
        if attr == "tabulator":
            raise AttributeError(attr)
        return getattr(self.tabulator, attr)

    @property
    def store(self):
        return self._store

    @store.setter
    def store(self, value):
        self._store = value
        self._options["index"] = self._store.persisted_class.key

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value):
        self._columns = value

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, value):
        self._options = self._options | value

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        self._role = value

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        if not in_designer:
            self._logger = value

    def build_tabulator(self):
        self.logger.debug(
            "ReactivePersistentTabulator.build_tabulator: Building tabulator"
        )
        tabulator = Tabulator()
        tabulator.options = self.options
        tabulator.columns = self.columns
        tabulator.role = self.role
        tabulator.options.update(app_table=self.store.view)
        tabulator.add_event_handler("row_click", self.row_click)
        tabulator.add_event_handler("table_built", self.tabulator_built)
        self.add_component(tabulator, full_width_row=True)
        self.tabulator = tabulator

    def tabulator_built(self, **event_args):
        self.raise_event("ready")

    @render_effect
    def refresh_tabulator(self):
        try:
            _ = self.store.changed
        except AttributeError:
            return

        self.logger.debug(
            "ReactivePersistenceTabulator.refresh_tabulator: Refreshing tabulator"
        )
        if not self.store.view:
            self.logger.debug(
                "ReactivePersistenceTabulator.refresh_tabulator: Store is empty. Bailing out."
            )
            return
        if self.tabulator is None:
            self.logger.debug(
                "ReactivePersistenceTabulator.refresh_tabulator: No tabulator exists yet. Building it..."
            )
            self.build_tabulator()
            return

        rows = self.tabulator.getSelectedRows()
        self.tabulator.clear_app_table_cache()
        self.tabulator.set_data()
        self.tabulator.selectRow([row.getIndex() for row in rows])

    def row_click(self, sender, **event_args):
        self.raise_event("row_click", **event_args)

    def form_show(self, **event_args):
        self.logger.debug(
            "ReactivePersistenceTabulator.form_show: Form shown event raised"
        )
        try:
            self.store.initialise()
        except AttributeError:
            return
