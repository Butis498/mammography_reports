# Medical Image Data Retrieval and Storage

## Overview

This Python code provides a framework for retrieving and storing medical images and associated reports from an Azure Blob Storage container and Azure Table Storage. The code is designed to work with DICOM format medical images and provides functionality for indexing images to improve retrieval performance.

## Requirements

Make sure you have the following dependencies installed:

Install them using:

```bash
pip install -r requirements.txt
```

Also make sure you have the correct credentials to access the Azure container, the following values should be stored in a `.env` file or set on the environment:

```
AZURE_STORAGE_ACCOUNT_NAME=accountName
AZURE_STORAGE_ACCOUNT_KEY=keyForAccount
AZURE_STORAGE_CONNECTION_STRING=connection string (optional depending on the other values)
AZURE_STORAGE_CONTAINER_NAME=images
AZURE_STORAGE_TABLE_NAME=report
```

## Usage

### DataGathering Class - Initialization Method

The initialization method (`__init__`) of the `DataGathering` class sets up instances with the following functionalities:

#### Default Parameter Values
- `blob_container_name='images'`: Default value for the blob container name.
- `table_name='report'`: Default value for the table name.
- `save_path='/`: Default value for the save path.

#### Attributes
- `self.proyections`: A list of strings representing projections - ['L__CC', 'L__MLO', 'R__CC', 'R__MLO'].
- `self.azure_blob_connection`: Instance of `AzureBlobConnection` initialized with the blob container name.
- `self.azure_table_connection`: Instance of `AzureTableConnection` initialized with the table name.
- `table_exists` and `blob_exists`: Checks for the existence of the Azure table and blob container, respectively.
- `self.path`: Sets the save path for storing cases.

#### Connection Check
Raises a `ConnectionError` if either the table or the blob container doesn't exist.

#### Image and Report Retrieval
- `self.image_retreival`: Initializes an instance of `ImageRetreival` with the Azure Blob resource client.
- `self.report_retreival`: Initializes an instance of `ReportRetreival` with the Azure Table resource client.

The initialization method establishes connections to Azure Blob and Table, checks their existence, and creates instances for image and report retrieval. Default values are provided for parameters related to the blob container name, table name, and save path.

### Indexing images

The code includes an image indexing mechanism to improve the performance of image retrieval. The indexing is done during the initialization of the ImageRetrieval class. To leverage this feature, make sure to call the index_images method:
This will significantly enhance the speed of retrieving DICOM images by utilizing the pre-built index.


```python
tool.image_retrieval.index_images()

```
Note: Ensure that the indexing is performed periodically or when there are changes to the storage contents to keep the index up to date.

### Get clinical case

For getting the case you will use `get_case` method which receives 3 paramters `id`,`year`and a boolean parameter to save the image `save_case` by defult is False. 

```python
case = tool.get_case(id='S0000001',year='2014')
```

The method will return a ClinicalCase object defines as:

```python
class ClinicalCase:
    id:str
    year:str
    l_cc:Image
    l_mlo:Image
    r_cc:Image
    r_mlo:Image
    report:str
```

The `ClinicalCase` class has the following attributes:

1. **id (str):** Represents a unique identifier for the clinical case.

2. **year (str):** Represents the year associated with the clinical case.

3. **l_cc, l_mlo, r_cc, r_mlo (Image):** Represent four images associated with the clinical case. The prefixes "l" and "r" suggest left and right, while "cc" and "mlo" likely stand for craniocaudal and mediolateral oblique, respectively. The type `Image` indicates these are objects representing images.

4. **report (str):** Represents a textual report or description associated with the clinical case.

In summary, the class is designed to hold information about a clinical case, including its identifier, associated year, four images (left craniocaudal, left mediolateral oblique, right craniocaudal, right mediolateral oblique), and a textual report.
## Contributors

Esteban Salazar
