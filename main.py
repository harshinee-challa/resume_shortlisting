from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from  view import output
from  controller import ResumeController
from getfiles import  Database
from fastapi import FastAPI,Body
from fastapi.responses import HTMLResponse
from jd import ChatBotModel
import os

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("API_KEY")
app = FastAPI()

account_name="resumeshortlisting"
account_key="VYXMvje5wOT2M9VjPjNhIxm/HOUssW5CEfl7AniXtnOjb4NISZBuGPuGRXklxhrfFV+Ui7woOYPj+ASt5G7kTQ=="
container_name="resumes"
connect_str = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
blob_service_client= BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(container_name)
database=Database(account_name, account_key, container_name, connect_str, container_client)
view = output()
controller =ResumeController(view,database)
jd_enhance=ChatBotModel(api_key)
@app.get("/shortlist")   
def shortlist(item: dict = Body(...)):
    jd = item['jd']
    jd_new = jd_enhance.prompt(jd)
    skills = controller.extract_skills_nlp_based(jd_new)
    match_list = controller.shortlist(skills)
    resume_scores=controller.process_resume(match_list) 
    ans=view.display_final_list(resume_scores)
    return {"message":ans}


@app.get("/upload_file")
def upload(item: dict = Body(...)):
        path = item['path']
        name=item['name']
        msg= database.upload_to_blob_storage(path,name) 
        return {"message": msg}

@app.get("/delete_file")
def delete(item: dict = Body(...)):
    name=item["name"]
    msg=database.delete_blob_from_storage(name)  
    return {"message": msg}
       
    
@app.get("/")
def display():
    return {"message": "Hello, user!"}
