from anvil.tables import app_tables
from functools import partial
import anvil.server
from anvil_extras.logging import Logger, DEBUG
from app.services import routes  # noqa unused_import

logger = Logger(name="Demo Server", level=DEBUG)

_templated_models = {
    "author": {
        "table_name": "author",
        "ops": ["create", "update", "delete", "get_view"],
    },
    "book": {
        "table_name": "book",
        "ops": ["create", "update", "delete", "get_view"],
    },
}


def _create(model, table_name, attrs):
    table = getattr(app_tables, table_name)
    return table.add_row(**attrs)


def _update(model, row, attrs):
    logger.debug(f"update_{model} called")
    row.update(**attrs)


def _delete(model, row):
    logger.debug(f"delete_{model} called")
    row.delete()


def _get_view(model, table_name, *args, **kwargs):
    logger.debug(f"get_{model}_view called")
    table = getattr(app_tables, table_name)
    return table.client_readable(*args, **kwargs)


def _actions(model, table_name):
    return {
        "create": {
            "callable": partial(_create, model, table_name),
            "name": f"add_{model}",
        },
        "update": {
            "callable": partial(_update, model),
            "name": f"update_{model}",
        },
        "delete": {
            "callable": partial(_delete, model),
            "name": f"delete_{model}"
        },
        "get_view": {
            "callable": partial(_get_view, model, table_name),
            "name": f"get_{model}_view",
        },
    }


def register_callables():
    for model, spec in _templated_models.items():
        actions = _actions(model, spec["table_name"])
        for op in spec["ops"]:
            logger.debug(f"Registering {op} function for {model}")
            anvil.server.callable(actions[op]["name"])(actions[op]["callable"])


register_callables()
