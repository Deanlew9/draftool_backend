# ------------------------------------------------------------------- External-imports -----------------------------------------------
from pymongo import MongoClient as PyMongoClient
from urllib.parse import quote_plus

# ------------------------------------------------------------------- Local-imports --------------------------------------------------
from application_service.config.Config import settings
from application_service.aws.constants import SecretKeys, SecretNames


# ------------------------------------------------------------------- Constants ------------------------------------------------------

# ------------------------------------------------------------------- Classes --------------------------------------------------------

class MongoClient:
    MONGO_SECRET_NAME = None
    MONGO_USER = None
    CLIENT_ADDRESS = None

    def __init__(self, secrets_manager):
        self._set_mongo_client_constants()
        self.client = self._init_client(secrets_manager)
        self.db_names = self.client.list_database_names()

    def _set_mongo_client_constants(self):
        env_settings = settings.from_env("dev")
        self.MONGO_SECRET_NAME = SecretNames.MONGO_DEV
        self.MONGO_USER = env_settings.MONGO_USER
        self.CLIENT_ADDRESS = env_settings.MONGO_ADDRESS

    def _init_client(self, secrets_manager):
        secret = secrets_manager.get_secret(self.MONGO_SECRET_NAME)
        pwd = secret.get(SecretKeys.PASSWORD)
        uri = f"mongodb+srv://{self.MONGO_USER}:{quote_plus(pwd)}@{self.CLIENT_ADDRESS}/?retryWrites=true&w=majority"
        client = PyMongoClient(uri)
        client.server_info()
        return client

# ----------------------------------------------- Functions ---------------------------------------------------
