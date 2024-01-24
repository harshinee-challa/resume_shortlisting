from transformers import AutoTokenizer, AutoModel
from  viewapi import output
from  modelapi import ResumeModel
from  controllerapi import ResumeController
import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
app = FastAPI()

resume_folder='H:/Resume/resumes'
@app.get('/path')
async def path(path:str):
    resume_folder = path
    return {"message":f"the resume path is {path}"}
    
@app.get('/jd')
async def main(jd:str):
    model = ResumeModel(resume_folder)
    view = output()
    controller =ResumeController(model, view)

    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    model_bert = AutoModel.from_pretrained("bert-base-uncased")

    job_description = jd
    skills = model.extract_skills_nlp_based(job_description)
    match_list = controller.shortlist(skills)
    results=controller.process_resume(match_list,resume_folder, job_description)
    return {
        "message": "Success",
        "data": results
    }

@app.get("/")
async def home():
    return {
        "message":"Hello!!!Please enter JD for further processing."
    }