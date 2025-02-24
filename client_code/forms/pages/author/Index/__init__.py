from app.forms.templates.Index import Index as IndexTemplate
from app.globals import session
from app.services import formatters

from ..Detail import Detail


class Index(IndexTemplate):
    tabulator_columns = [
        {
            "title": "Name",
            "field": "name",
            "formatter": formatters.label,
            "formatter_params": {"attr": "name"},
        },
    ]
    store = session.stores["author"]
    detail_form = Detail
    title = "Authors"
