#run file using uvicorn main:app --reload

# python -m spacy download en_core_web_sm
from azure.storage.blob import BlobServiceClient
from  view import output
from  controller import ResumeController
from getfiles import  Database
from fastapi import FastAPI

app = FastAPI()

account_name="resumeshortlisting"
account_key="VYXMvje5wOT2M9VjPjNhIxm/HOUssW5CEfl7AniXtnOjb4NISZBuGPuGRXklxhrfFV+Ui7woOYPj+ASt5G7kTQ=="
container_name="resumes"
connect_str = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
blob_service_client= BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(container_name)

view = output()
database=Database(account_name,account_key,container_name,connect_str,container_client)
controller =ResumeController(view,database)

@app.get("/shortlist")   
def shortlist(jd:str) :
    skills = controller.extract_skills_nlp_based(jd)
    match_list = controller.shortlist(skills)
    resume_scores=controller.process_resume(match_list) 
    ans=view.display_final_list(resume_scores)
    return {"message":ans}

@app.get("/upload_file")
def upload(path:str ,name:str):
        msg= database.upload_to_blob_storage(path,name) 
        return {"message": msg}

@app.get("/delete_file")
def delete(name:str):
    msg=database.delete_blob_from_storage(name)  
    return {"message": msg}
       
    
@app.get("/")
def display():
    return {"message": "Hello, user!"}
