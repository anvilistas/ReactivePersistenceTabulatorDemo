import anvil
from routing import router

from ._anvil_designer import MainTemplate


class Main(MainTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

    def on_navigate(self, **event_args):
        context = router.get_routing_context()
        self.layout.show_sidesheet = context.query.get("detail", False)

    def form_show(self, **event_args):
        if not anvil.designer.in_designer:
            router.add_event_handler("navigate", self.on_navigate)
            self.on_navigate()

    def form_hide(self, **event_args):
        router.remove_event_handler("navigate", self.on_navigate)

    def close_button_click(self, **event_args):
        def query(prev):
            return {**prev, "detail": False}

        router.navigate(query=query)
