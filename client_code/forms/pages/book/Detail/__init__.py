from ._anvil_designer import DetailTemplate
from app.services import model
from app import globals

_model = model.Book


class Detail(DetailTemplate):
    def __init__(self, item=None, **properties):
        self.actions_panel.mode = "create" if item is None else "update"
        self.actions_panel.store = globals.stores["book"]
        self.item = _model() if item is None else item
        self.actions_panel.item = self.item
        self.init_components(**properties)
