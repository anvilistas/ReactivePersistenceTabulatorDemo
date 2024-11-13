from app import globals
from app.services import formatters
from routing import router

from ..Detail import Detail
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
    def __init__(self, routing_context: router.RoutingContext, **properties):
        self.routing_context = routing_context
        self.tabulator.store = globals.stores["author"]
        self.tabulator.columns = _tabulator_columns
        self.tabulator.role = "index"
        self.tabulator.logger = globals.logger
        self.tabulator.add_event_handler("row_click", self.tabulator_row_click)
        self.tabulator.add_event_handler("ready", self.tabulator_ready)
        self.init_components(**properties)

    def tabulator_ready(self, **event_args):
        self.routing_context.add_event_handler("query_changed", self.on_query_change)
        self.routing_context.raise_init_events()

    def on_query_change(self, query, **event_args):
        model_key = query.get("m")
        is_new = query.get("new")
        model = None

        if model_key is not None:
            row = self.tabulator.getRow(model_key)
            row.select()
            model = row.getModel()
            detail = Detail(model)
            self.layout.add_detail(detail)

        elif is_new:
            detail = Detail(model)
            self.layout.add_detail(detail)

    def tabulator_row_click(self, sender, row, **event_args):
        row.select()
        model = row.getModel()
        model_key = getattr(model, model.key)

        def query(prev):
            prev_m = prev.get("m")
            if prev_m == model_key:
                return {**prev, "detail": not prev.get("detail")}
            return {"m": model_key, "detail": True}

        router.navigate(query=query)

    def new_button_click(self, **event_args):
        router.navigate(query={"new": True, "detail": True})
