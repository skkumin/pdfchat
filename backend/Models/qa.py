from typing import List, Optional
from pydantic import BaseModel
from odmantic import Model


#For Request
class QuestionRequest(BaseModel):
    question: str
    options: List[str]


#For MongDB
class QA(Model):
    info: dict

    class Config:
        collection = "qa"
