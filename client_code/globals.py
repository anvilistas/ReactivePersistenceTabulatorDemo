from anvil_extras.logging import DEBUG, Logger
from app.services import model
from app.services.storage import PersistedClassStore
from routing import router

_LOG_LEVEL = DEBUG
_logger = Logger(name="Demo Client", level=_LOG_LEVEL)
_models = (model.Author, model.Book)


def _build_stores(models, logger):
    stores = (PersistedClassStore(model, logger) for model in models)
    return {store._class_name: store for store in stores}


class _Session:
    def __init__(self, logger):
        self.user = None
        self.logger = logger
        self.routing_launched = False
        self.stores = None

    def launch(self):
        self.terminate()
        self.stores = _build_stores(_models, self.logger)
        if not self.routing_launched:
            router.launch()
            self.routing_launched = True
        router.navigate("/")

    def terminate(self):
        router.clear_cache()
        self.user = None
        self.stores = None


session = _Session(logger=_logger)
