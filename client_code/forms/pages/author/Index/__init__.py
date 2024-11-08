from app import globals
from app.services import formatters, model
from app import globals
from tabulator.Tabulator import Tabulator
from anvil_reactive.main import render_effect
from ..Detail import Detail
from ._anvil_designer import IndexTemplate

_model = model.Author

_tabulator_options = {
    "data_loader": False,
    "loading_indicator": False,
    "selectable": True,
    "header_visible": False,
    "mutator": _model,
    "index": _model.key,
    "pagination": False,
    "progressive_load": "scroll",
    "progressive_load_scroll_margin": 300,
}
_tabulator_columns = [
    {
        "title": "Name",
        "field": "name",
        "formatter": formatters.label,
        "formatter_params": {"attr": "name"},
    },
]
logger = globals.logger


class Index(IndexTemplate):
    def __init__(self, **properties):
        self.tabulator = None
        self.store = globals.stores["author"]
        self.init_components(**properties)

    def build_tabulator(self):
        tabulator = Tabulator()
        tabulator.options = _tabulator_options
        tabulator.columns = _tabulator_columns
        tabulator.role = "index"
        tabulator.options.update(app_table=self.store.view)
        tabulator.add_event_handler("row_click", self.tabulator_row_click)
        self.layout.slots["content"].add_component(tabulator, full_width_row=True)
        self.tabulator = tabulator
    
    @render_effect
    def loading_visibility(self):
        self.loading_panel.visible = self.store.loading
    
    @render_effect
    def refresh_tabulator(self):
        logger.debug("refreshing tabulator...")
        _ = self.store.changed

        if not self.store.view:
            logger.debug("No view. bombing out.")
            return

        if self.tabulator is None:
            logger.debug("No tabulator yet. Building it.")
            self.build_tabulator()
            return

        self.tabulator.deselect_row()
        self.tabulator.clear_app_table_cache()
        self.tabulator.set_data()

    def tabulator_row_click(self, sender, row, **event_args):
        sender.deselect_row()
        row.select()
        detail = Detail(row.getModel())
        self.layout.show_detail(detail)

    def form_show(self, **event_args):
        if self.store.view is None:
            self.store.initialise()

    def new_button_click(self, **event_args):
        detail = Detail()
        self.layout.show_detail(detail)
