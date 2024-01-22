import pydicom as dicom
from io import BytesIO
import numpy as np
from PIL import Image
import re



class ImageRetreival:

    def __init__(self,client) -> None:
        self.client = client
        self.index = {}
        self.indexed = False
        

    def get_all_image_names(self):

        return self.client.list_blobs()
    
    def get_image_png(self, id, year, proyection) -> Image:
        dcm = self.get_image_dcm(id, year, proyection)
        if dcm == None:
            raise FileExistsError('Image not found')
            
        dcm.NumberOfFrames = int(dcm.NumberOfFrames)
        if dcm.file_meta.TransferSyntaxUID.is_compressed:
            dcm.decompress('pylibjpeg')

        arr = dcm.pixel_array
        # Normalize to 0-255
        arr = arr - np.min(arr)
        arr = arr / np.max(arr)
        arr = (arr * 255).astype(np.uint8)

        # Convert to PIL Image
        final_image = Image.fromarray(arr)
        
        return final_image


    def index_images(self):
        blobs = self.get_all_image_names()
        print('Indexing images...')
        
        for blob in blobs:
            # Updated regex to match a four-digit number with surrounding non-digit characters
            regex1 = r'\D(\d{4})\D'
            
            regex2 = r'(S\d+)'

            regex3 = r'(L|R)__(CC|MLO)'

            # Use re.search to find matches
            year_match = re.search(regex1, blob.name)
            id_match = re.search(regex2, blob.name)
            proyection_match = re.search(regex3, blob.name)

            if year_match and id_match and proyection_match:
                year_value = year_match.group(1)  # Extract the matched four-digit number
                id_value = id_match.group(1)
                proyection_value = proyection_match.group(0)

                if year_value not in self.index:
                    self.index[year_value] = {}

                if id_value not in self.index[year_value]:
                    self.index[year_value][id_value] = {}

                self.index[year_value][id_value][proyection_value] = blob.name
        self.indexed = True
        
        print('Done indexing images')


    
    def get_image_dcm(self,id,year,proyection):

        if year in self.index and id in self.index[year] and proyection in self.index[year][id]:
            
            requested_blob = self.index[year][id][proyection]

        else:
            blobs = self.get_all_image_names()
            requested_blob:str=None
            for blob in blobs:
    
                if str(id) in blob.name and str(year) in blob.name and str(proyection) in blob.name:
                    requested_blob = blob.name
                    break
        
        if requested_blob is None:
            raise FileNotFoundError('Image not found')
        
        return self.get_dcm(requested_blob)

    def get_dcm(self, image_blob):

        blob_client = self.client.get_blob_client(blob=image_blob)
        download_stream = blob_client.download_blob()
        data = download_stream.readall()  # Read the data from the stream
        dicom_stream = BytesIO(data)  # Pass the data to BytesIO
        ds = dicom.dcmread(dicom_stream)  # Corrected module name

        return ds
