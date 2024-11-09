from ._anvil_designer import MainTemplate


class Main(MainTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

    def show_detail(self, content):
        self.slots["sidesheet"].clear()
        self.slots["sidesheet"].add_component(content)
        self.layout.show_sidesheet = True

    def close_sidesheet_button_click(self, **event_args):
        self.layout.show_sidesheet = False
