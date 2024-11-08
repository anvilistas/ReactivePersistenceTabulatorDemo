import anvil


def label(cell, attr, **params):
    model = cell.getModel()
    return anvil.Label(text=getattr(model, attr))


def label_with_description(cell, attr, **params):
    model = cell.getModel()
    flow_panel = anvil.FlowPanel(align="left")
    panel = anvil.ColumnPanel(spacing_above=None, spacing_below=None)
    flow_panel.add_component(panel)
    panel.add_component(
        anvil.Label(text=getattr(model, attr), spacing_above=None, spacing_below=None)
    )
    panel.add_component(
        anvil.Label(
            text=model.description, spacing_above=None, spacing_below=None, font_size=12
        )
    )
    return flow_panel
