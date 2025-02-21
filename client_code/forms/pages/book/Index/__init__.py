from app.forms.templates.Index import Index as IndexTemplate
from app.globals import session
from app.services import formatters

from ..Detail import Detail


class Index(IndexTemplate):
    tabulator_columns = [
        {
            "title": "Title",
            "field": "title",
            "formatter": formatters.label,
            "formatter_params": {"attr": "title"},
        },
    ]
    store = session.stores["book"]
    detail_form = Detail
    title = "Books"