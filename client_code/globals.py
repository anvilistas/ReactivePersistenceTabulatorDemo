from app.services.storage import PersistedClassStore
from app.services import model
from anvil_extras.logging import Logger, DEBUG

LOG_LEVEL = DEBUG

logger = Logger(name="Demo Client", level=LOG_LEVEL)
stores = {
    "author": PersistedClassStore(model.Author, logger),
    "book": PersistedClassStore(model.Book, logger),
}
