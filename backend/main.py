import uvicorn
import openai
import os
import asyncio
from typing import List
from fastapi import FastAPI
from llama_index.response.schema import Response

# from pydantic import BaseModel

# Functions
from Functions.Subquery import (
    get_vectorstoreindex,
    get_retrievers,
    make_synthesizer,
    make_engine,
    make_subqueryengine,
    final_engine
)
from Functions.Jsonparser import (
    make_dict_sub,
    make_dict_single
)

# Models
from Models.qa import QuestionRequest, QA
from Models import mongodb


app = FastAPI()

@app.get("/")
async def root():
    return None


@app.post("/question")
async def process_question(request: QuestionRequest):
    question = request.question
    options = request.options
    print(question)
    if len(options) == 0:
        return "No options. Please select pdf file"
    
    print("response 시작")
    response = await final_engine(options).aquery(question)
    if len(options) == 1:
        info = await make_dict_single(question, response)
    else:
        info = await make_dict_sub(question, response)
    db_json = QA(info=info)
    print(await mongodb.engine.save(db_json))
    print(question)

    return info


@app.on_event("startup")
def on_app_start():
    mongodb.connect()


@app.on_event("shutdown")
def on_app_shutdown():
    mongodb.close()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)  # reload=True

