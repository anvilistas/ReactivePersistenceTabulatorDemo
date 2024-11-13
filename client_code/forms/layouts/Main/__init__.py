import anvil
from routing import router

from ._anvil_designer import MainTemplate


class Main(MainTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

    def add_detail(self, content):
        self.slots["sidesheet"].clear()
        self.slots["sidesheet"].add_component(content)

    def close_sidesheet_button_click(self, **event_args):
        def query(prev):
            return {**prev, "detail": False}

        router.navigate(query=query)

    def on_navigate(self, **event_args):
        context = router.get_routing_context()
        self.layout.show_sidesheet = context.query.get("detail", False)

    def form_show(self, **event_args):
        if not anvil.designer.in_designer:
            router.add_event_handler("navigate", self.on_navigate)
            self.on_navigate()

    def form_hide(self, **event_args):
        router.add_event_handler("navigate", self.on_navigate)
