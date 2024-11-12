from anvil_reactive.main import bind, writeback, effect
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
        bind(
            self.author_dropdown,
            "items",
            globals.stores["author"],
            "dropdown_items",
        )
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
        # self.author_dropdown.items = globals.stores["author"].dropdown_items
        # self.author_dropdown.selected_value = self.item["author"]
        self.init_components(**properties)

    # @effect
    # def render_1(self):
    #     print("RENDER 1")
    #     self.author_dropdown.items = globals.stores["author"].dropdown_items
    #     print(globals.stores["author"].dropdown_items)
    #     print("RENDER 1 DONE")
        
    #     # print(self.item["author"], self.author_dropdown.selected_value)

    # @effect
    # def render_2(self):
    #     print("RENDER 2")
    #     self.author_dropdown.selected_value = self.item["author"]
    #     print(self.item["author"])
    #     print("RENDER 2 DONE")
    #     # print(self.item["author"], self.author_dropdown.selected_value)

    # @effect
    # def render_3(self):
    #     print("RENDER 3")
    #     print(self.item["author"], self.author_dropdown.selected_value)
    #     print("RENDER 3 DONE")

    # def form_show(self, **event_args):
    #     """This method is called when the form is shown on the page"""
    #     print("SHOW")
