from celery.result import AsyncResult
from fastapi import Body, FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
import os

from worker import create_task, summarize_task
from services.summary_services import summarize
from utils.v1.openai import heartbeat

from api.v1 import summaries
from api.v1.summaries import read_text_file

app = FastAPI(title="Knowledge Research Inc. API", description="FastAPI + Celery + Redis")
origins = [
    "*",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

api_key=os.environ.get("OPENAI_API_KEY")

app.include_router(summaries.router, prefix="/api/v1/summaries")

@app.post("/tasks", status_code=201, tags=["General Tasks"], description="Run a generic task.")
def run_task(payload = Body(...)):
    task_type = payload["type"]
    task = create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})


@app.get("/tasks/{task_id}", tags=["General Tasks"], description="Get the status of a task by its ID.")
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)



@app.post("/batch-summarize-task", status_code=201, tags=["Summarization Tasks"],
          description="""
          Submit multiple documents for summarization. Each document content should be passed as a plain text input.
          
          This endpoint is designed to submit 10 summarization tasks from text files:
          
          - document-1-357-1697.txt (357 Tokens): Will and Estate
          - document-2-2035-10856.txt (2,035 Tokens): Environmental Policy
          - document-3-388-1786.txt (388 Tokens): Will and Estate
          - document-4-733-3229.txt (733 Tokens): Will and Estate
          - document-5-649-2820.txt (649 Tokens): Will and Estate
          - document-6-1401-7828.txt (1,201 Tokens): Marketing Services Agreement
          - document-7-1008-5201.txt (1,008 Tokens): Website Development Agreement
          - document-8-1047-5303.txt (1,047 Tokens): Website Development Agreement
          - document-9-825-4318.txt (825 Tokens): Non-Disclosure Agrement
          - document-10-1173-5362.txt (1,173 Tokens): Loan Agreement
          
          Returns a dictionary of task IDs for each summarization task.
          """)
def batch_summarize_task_endpoint():
    
    model = "gpt-3.5-turbo-0613"
    document_1 = read_text_file("documents/document-1-357-1697.txt")
    document_2 = read_text_file("documents/document-2-2035-10856.txt")
    document_3 = read_text_file("documents/document-3-388-1786.txt")
    document_4 = read_text_file("documents/document-4-733-3229.txt")
    document_5 = read_text_file("documents/document-5-649-2820.txt")
    document_6 = read_text_file("documents/document-6-1401-7828.txt")
    document_7 = read_text_file("documents/document-7-1008-5201.txt")
    document_8 = read_text_file("documents/document-8-1047-5303.txt")
    document_9 = read_text_file("documents/document-9-825-4318.txt")
    document_10 = read_text_file("documents/document-10-1173-5362.txt")
    task_1 = summarize_task.delay(model, document_1)
    task_2 = summarize_task.delay(model, document_2)
    task_3 = summarize_task.delay(model, document_3)
    task_4 = summarize_task.delay(model, document_4)
    task_5 = summarize_task.delay(model, document_5)
    task_6 = summarize_task.delay(model, document_6)
    task_7 = summarize_task.delay(model, document_7)
    task_8 = summarize_task.delay(model, document_8)
    task_9 = summarize_task.delay(model, document_9)
    task_10 = summarize_task.delay(model, document_10)
    return JSONResponse({
        "task_ids": {
            "document_1": task_1.id,
            "document_2": task_2.id,
            "document_3": task_3.id,
            "document_4": task_4.id,
            "document_5": task_5.id,
            "document_6": task_6.id,
            "document_7": task_7.id,
            "document_8": task_8.id,
            "document_9": task_9.id,
            "document_10": task_10.id
        }
    })

@app.get("/heartbeat", tags=["Utilities"])
async def heartbeat_endpoint():
    result = await heartbeat(api_key)
    return(result)


