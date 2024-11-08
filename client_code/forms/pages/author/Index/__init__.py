from app import globals
from ..Detail import Detail
from app.services import formatters
from ._anvil_designer import IndexTemplate

_tabulator_columns = [
    {
        "title": "Name",
        "field": "name",
        "formatter": formatters.label,
        "formatter_params": {"attr": "name"},
    },
]


class Index(IndexTemplate):
    def __init__(self, **properties):
        self.tabulator.store = globals.stores["author"]
        self.tabulator.columns = _tabulator_columns
        self.tabulator.role = "index"
        self.tabulator.logger = globals.logger
        self.tabulator.add_event_handler("row_click", self.tabulator_row_click)
        self.init_components(**properties)

    def tabulator_row_click(self, sender, row, **event_args):
        row.select()
        detail = Detail(row.getModel())
        self.layout.show_detail(detail)

    def new_button_click(self, **event_args):
        detail = Detail()
        self.layout.show_detail(detail)
