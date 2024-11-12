from anvil_reactive.main import bind, writeback
from app import globals
from app.services import model

from ._anvil_designer import DetailTemplate

_model = model.Book


class Detail(DetailTemplate):
    def __init__(self, item=None, **properties):
        self.actions_panel.mode = "create" if item is None else "update"
        self.actions_panel.store = globals.stores["book"]
        self.item = _model() if item is None else item
        self.actions_panel.item = self.item
        bind(self.author_dropdown, "items", lambda: globals.dropdown_items["authors"])
        writeback(self.isbn_text_box, "text", self.item, "isbn_13", events=["change"])
        writeback(self.title_text_box, "text", self.item, "title", events=["change"])
        writeback(
            self.edition_text_box, "text", self.item, "edition", events=["change"]
        )
        writeback(
            self.published_on_date_picker,
            "date",
            self.item,
            "published_on",
            events=["change"],
        )
        writeback(
            self.author_dropdown,
            "selected_value",
            self.item,
            "author",
            events=["change"],
        )
        self.init_components(**properties)
