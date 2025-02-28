from anvil_reactive.main import bind
from routing import router

from ._anvil_designer import IndexHeaderTemplate


class IndexHeader(IndexHeaderTemplate):
    def __init__(self, **properties):
        self._store = None
        bind(self.loading_indicator, "visible", self, "loading")
        self.init_components(**properties)

    @property
    def store(self):
        return self._store

    @store.setter
    def store(self, value):
        self.heading.text = value.persisted_class.index_title
        self._store = value

    @property
    def loading(self):
        try:
            _loading = self.store.loading
            return _loading
        except AttributeError:
            return True

    def new_button_click(self, **event_args):
        router.navigate(query={"new": True, "detail": True})
