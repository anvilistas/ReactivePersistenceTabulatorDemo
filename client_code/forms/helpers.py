import m3.components as m3
from app.globals import session
from routing import router


class WithRoutedSidesheet:
    def init_tabulator(self):
        self.tabulator.store = self.store
        self.tabulator.columns = self.tabulator_columns
        self.tabulator.role = self.tabulator_role
        self.tabulator.logger = session.logger
        self.tabulator.add_event_handler("row_click", self.tabulator_row_click)
        self.tabulator.add_event_handler("ready", self.tabulator_ready)

    def tabulator_ready(self, **event_args):
        self.routing_context.add_event_handler("query_changed", self.on_query_change)
        self.routing_context.raise_init_events()

    def on_query_change(self, query, **event_args):
        model_key = query.get("m")
        is_new = query.get("new")
        detail = None

        if model_key is not None:
            row = self.tabulator.getRow(model_key)
            if not row:
                return
            row.select()
            model = row.getModel()
            detail = self.detail_form(model)
            title = m3.Heading(text=f"{self.store.persisted_class.__name__} Details")
        elif is_new:
            detail = self.detail_form()
            title = m3.Heading(text=f"New {self.store.persisted_class.__name__}")

        sidesheet = self.layout.sidesheet_content
        sidesheet.slots["anvil-m3-sidesheet"].clear()
        sidesheet.slots["anvil-m3-sidesheet-title"].clear()
        if detail is not None:
            sidesheet.slots["anvil-m3-sidesheet"].add_component(detail)
            sidesheet.slots["anvil-m3-sidesheet-title"].add_component(title)

    def tabulator_row_click(self, sender, row, **event_args):
        sender.deselect_row()
        row.select()
        model = row.getModel()
        model_key = getattr(model, model.key)

        def query(prev):
            prev_m = prev.get("m")
            if prev_m == model_key:
                return {**prev, "detail": not prev.get("detail")}
            return {"m": model_key, "detail": True}

        router.navigate(query=query)
