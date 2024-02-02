import PyPDF2
import io
from azure.storage.blob import BlobServiceClient, BlobClient, generate_blob_sas,BlobSasPermissions
from azure.storage.blob._shared.shared_access_signature import QueryStringConstants
from datetime import datetime, timedelta
from urllib.parse import quote
import urllib.parse
import webbrowser

class Database:
    def __init__(self, account_name, account_key, container_name, connect_str, container_client):
        self.account_name = account_name
        self.account_key = account_key
        self.container_name = container_name
        self.connect_str=connect_str
        self.container_client = container_client
        self.blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    def upload_to_blob_storage(self,file_path,file_name):
        blob_client =self.blob_service_client.get_blob_client(container=self.container_name, blob=file_name)        
        try:
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            msg= f"Uploaded and overwritten {file_name} file."
        except FileNotFoundError:
            msg= f"{file_name} not found. Check the file path."
        except Exception as e:
            msg= f"Error uploading {file_name} file."
        return msg
        
    
    def delete_blob_from_storage(self, file_name):
        blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=file_name)

        try:
            blob_client.delete_blob()
            msg=f"Deleted {file_name} file"
        except FileNotFoundError:
            msg=f"{file_name} not found. It may have already been deleted."
        except Exception as e:
            msg=f"Error deleting {file_name} file."
        return msg
        
        
    
    def get_filenames_from_azure(self):
        return [blob.name for blob in self.container_client.list_blobs()]
    


    def get_url(self, blob_name):
        connection_string = f"DefaultEndpointsProtocol=https;AccountName={self.account_name};AccountKey={self.account_key};EndpointSuffix=core.windows.net"
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=self.container_name, blob=blob_name)

        sas_token = generate_blob_sas(
            account_name=self.account_name,
            account_key=self.account_key,
            container_name=self.container_name,
            blob_name=blob_name,
            permission=BlobSasPermissions(read=True,write=False),
            expiry=datetime.utcnow() + timedelta(hours=1)  # Adjust the expiration time as needed
        )

        blob_url = f"{blob_client.url}?{sas_token}"
        quote_name= urllib.parse.quote(blob_name)
        disposition=f"inline; filename*=utf-8''{quote_name};"
        blob_url+=f"&content-disposition={disposition}"
        return blob_url
    
    
    def get_pdf_text(self):
        pdf_text = []

        for blob in self.container_client.list_blobs() :
                blob_client = BlobClient(
                    account_url=f"https://{self.account_name}.blob.core.windows.net",
                    container_name=self.container_name,
                    blob_name=blob.name,
                    credential=self.account_key
                )
                stream = blob_client.download_blob()
                bytes_data = stream.readall()

                pdf_reader = PyPDF2.PdfReader(io.BytesIO(bytes_data))

                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()

                pdf_text.append(text)
        return pdf_text
    
    
    
    def download_blob(self, file_path):

        # Extract container name and blob name from the file path
        container_name, blob_name = file_path.split('/', 1)

        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        # Download the blob content
        blob_content = blob_client.download_blob().readall()
        return blob_content

    


