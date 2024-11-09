from ._anvil_designer import DetailTemplate
from app.services import model
from app import globals
from anvil_reactive.main import writeback

_model = model.Book


class Detail(DetailTemplate):
    def __init__(self, item=None, **properties):
        self.actions_panel.mode = "create" if item is None else "update"
        self.actions_panel.store = globals.stores["book"]
        self.item = _model() if item is None else item
        self.actions_panel.item = self.item
        writeback(self.isbn_text_box, "text", self.item, "isbn_13", events=["change"])
        writeback(self.title_text_box, "text", self.item, "title", events=["change"])
        self.init_components(**properties)
