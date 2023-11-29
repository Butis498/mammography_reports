import os
from dotenv import load_dotenv


class AzureConnection:
    def __init__(self, account_name=None, account_key=None, connection_string=None, resource_name=None):
        self.account_name = account_name
        self.account_key = account_key
        self.connection_string = connection_string
        self.resource_name = resource_name
        self.resource_service_client = None
        self.resource_client = None
        self._load_env_variables()

        if not any([self.account_name, self.connection_string]):
            raise ValueError("Either 'account_name' or 'connection_string' must be provided.")

        if not self.resource_name:
            raise ValueError("Please provide the 'table_name'.")


    def _load_env_variables(self):
        # Load environment variables from .env file
        load_dotenv()

        # Get values from the environment or use the provided values
        self.account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME", self.account_name)
        self.account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY", self.account_key)
        self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING", self.connection_string)


