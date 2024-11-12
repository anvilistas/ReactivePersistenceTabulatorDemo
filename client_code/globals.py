from anvil_extras.logging import DEBUG, Logger
from app.services import model
from app.services.storage import PersistedClassStore

LOG_LEVEL = DEBUG

logger = Logger(name="Demo Client", level=LOG_LEVEL)
stores = {
    "author": PersistedClassStore(model.Author, logger),
    "book": PersistedClassStore(model.Book, logger),
}

dropdown_items = {
    "authors": [(str(a), a) for a in stores["author"].list_search],
}