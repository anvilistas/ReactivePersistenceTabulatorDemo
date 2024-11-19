from anvil_reactive.main import writeback
from app import globals
from app.services import model

from ._anvil_designer import DetailTemplate

_model = model.Author


class Detail(DetailTemplate):
    def __init__(self, item=None, **properties):
        self.actions_panel.mode = "create" if item is None else "update"
        self.actions_panel.store = globals.stores["author"]
        self.item = _model() if item is None else item
        self.actions_panel.item = self.item
        writeback(self.name_text_box, "text", self.item, "name", events=["change"])
        self.init_components(**properties)

    def form_hide(self, **event_args):
        self.item.reset()
