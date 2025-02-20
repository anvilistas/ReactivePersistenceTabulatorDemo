from anvil_reactive.main import bind
from routing import router

from ._anvil_designer import DetailActionsTemplate


class DetailActions(DetailActionsTemplate):
    def __init__(self, **properties):
        self._store = None
        self._item = None
        self._mode = None
        self.init_components(**properties)

    @property
    def store(self):
        return self._store

    @store.setter
    def store(self, value):
        self._store = value

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, value):
        self._item = value
        bind(self.save_button, "enabled", self._item, "buffered_changes")

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = value

    def delete_button_click(self, **event_args):
        router.navigate(query={})
        self.store.delete(self.item)

    def save_button_click(self, **event_args):
        self.store.save(self.item)
        router.navigate(query={})
