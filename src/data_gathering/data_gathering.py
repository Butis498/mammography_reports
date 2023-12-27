from connection import AzureBlobConnection,AzureTableConnection
from report import ReportRetreival
from image import ImageRetreival
from dataclasses import dataclass
from PIL import Image
import pickle
import os

@dataclass
class ClinicalCase:
    id:str
    year:str
    l_cc:Image
    l_mlo:Image
    r_cc:Image
    r_mlo:Image
    report:str

class DataGathering:

    def __init__(self,blob_container_name='images',table_name='report',save_path='/') -> None:
        self.proyections = ['L__CC','L__MLO','R__CC','R__MLO']
        self.azure_blob_connection = AzureBlobConnection(resource_name=blob_container_name)
        self.azure_table_connection = AzureTableConnection(resource_name=table_name)
        table_exists = self.azure_table_connection.table_exists()
        blob_exists = self.azure_blob_connection.blob_exists()
        self.path = save_path

        if not (table_exists and blob_exists):
            raise ConnectionError('Couldnt Connect to Azure')
        
        self.image_retreival = ImageRetreival(self.azure_blob_connection.resource_client)
        self.report_retreival = ReportRetreival(self.azure_table_connection.resource_client)

    def save_case(self,case:ClinicalCase):
        # Create the directory if it does not exist
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        # Construct the filename
        filename = f"{case.id}_{case.year}.pkl"

        # Save the object using pickle
        with open(filename, 'wb') as f:
            pickle.dump(case, f)

    
    def get_case(self,id,year,save_case=False):

        req_case = ClinicalCase(id=id,year=year,l_cc=None,l_mlo=None,r_cc=None,r_mlo=None,report=None)
        valid = True
        for proyection in self.proyections:
            try:
                image = self.image_retreival.get_image_png(id,year,proyection)
            except FileNotFoundError:
                print(f'Image {id} {year} {proyection} not found')
                image = None
                valid = False
            if proyection == 'L__CC':
                req_case.l_cc = image
            elif proyection == 'L__MLO':
                req_case.l_mlo = image
            elif proyection == 'R__CC':
                req_case.r_cc = image
            elif proyection == 'R__MLO':
                req_case.r_mlo = image

        req_case.report = self.report_retreival.get_report(id,year)
        if req_case.report is None:
            print(f'Report {id} {year} not found')
            valid = False

        if not valid:
            return None
        
        
        if save_case:
            self.save_case(req_case)

                

        return req_case


        

