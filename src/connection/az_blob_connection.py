import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from .connection import AzureConnection
class AzureBlobConnection(AzureConnection):

    def __init__(self, account_name=None, account_key=None, connection_string=None, resource_name=None):
        super().__init__(account_name, account_key, connection_string, resource_name)
        self._initialize_blob_service_client()
        self._initialize_container_client()
    
    def _initialize_blob_service_client(self):
        if self.connection_string:
            self.resource_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        else:
            connection_string = f"DefaultEndpointsProtocol=https;AccountName={self.account_name};AccountKey={self.account_key};EndpointSuffix=core.windows.net"
            self.resource_service_client = BlobServiceClient.from_connection_string(connection_string)

    def _initialize_container_client(self):
        try:
            self.resource_client = self.resource_service_client.get_container_client(self.resource_name)
        except Exception as e:
            print('Not possible to get client: ',str(e))

    def blob_exists(self):
        try:
            
            return self.resource_client.exists()
        except Exception as e:
            print(str(e))
            return False