from azure.data.tables import TableServiceClient, TableClient
from .connection import AzureConnection
from azure.core.exceptions import ResourceNotFoundError

class AzureTableConnection(AzureConnection):

    def __init__(self, account_name=None, account_key=None, connection_string=None, resource_name=None):
        super().__init__(account_name, account_key, connection_string, resource_name)
        self._initialize_table_service_client()
        self._initialize_table_client()


    def _initialize_table_service_client(self):
        if self.connection_string:
            self.resource_service_client = TableServiceClient.from_connection_string(self.connection_string)
        else:
            connection_string = f"DefaultEndpointsProtocol=https;AccountName={self.account_name};AccountKey={self.account_key};TableEndpoint=https://{self.account_name}.table.core.windows.net/;"
            self.resource_service_client = TableServiceClient.from_connection_string(connection_string)

    def _initialize_table_client(self):
        try:
            self.resource_client = self.resource_service_client.get_table_client(self.resource_name)
        except ResourceNotFoundError:
            print(f"The table '{self.resource_name}' does not exist.")

    def get_container_client(self):
        return self.resource_service_client.get_container_client(self.container_name)


    def table_exists(self):
        table_service_client = self.resource_service_client
        try:
            # Try to get the table client
            table_client = table_service_client.get_table_client(self.resource_name)
            return True
        except ResourceNotFoundError:
            # If the table doesn't exist, an error will be raised
            return False
        except Exception as e:
            # If an error occurs (other than the table not existing), print the error message
            return False
