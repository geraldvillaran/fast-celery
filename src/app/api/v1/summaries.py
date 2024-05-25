from fastapi import APIRouter
from fastapi.responses import JSONResponse
from worker import summarize_task

from databases.database import database

router = APIRouter()

@router.post("/summarize-task", status_code=201, tags=["Summarization Tasks"],
          description="""
          Submit a single document for summarization from a text file:
          
          - document-1-357-1697.txt (357 Tokens): Will and Estate
          
          The operation returns task IDs for the summarization task.
          """)
def summarize_task_endpoint():
    model = "gpt-3.5-turbo-0613"
    document_1 = read_text_file("documents/document-1-357-1697.txt")
    task_1 = summarize_task.delay(model, document_1)
    return JSONResponse({"task_ids": {"document_1": task_1.id}})

def read_text_file(file_path: str) -> str:
    """Utility function to read text from a given file path."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()