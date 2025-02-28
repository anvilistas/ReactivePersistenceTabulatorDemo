from app.forms.helpers import WithRoutedSidesheet
from app.globals import session
from app.services import formatters
from routing import router

from ..Detail import Detail
from ._anvil_designer import IndexTemplate


class Index(WithRoutedSidesheet, IndexTemplate):
    tabulator_columns = [
        {
            "title": "Title",
            "field": "title",
            "formatter": formatters.label,
            "formatter_params": {"attr": "title"},
        },
    ]
    tabulator_role = "index"
    store = session.stores["book"]
    detail_form = Detail

    def __init__(self, routing_context: router.RoutingContext, **properties):
        self.routing_context = routing_context
        self.init_tabulator()
        self.init_components(**properties)

    def new_button_click(self, **event_args):
        router.navigate(query={"new": True, "detail": True})
