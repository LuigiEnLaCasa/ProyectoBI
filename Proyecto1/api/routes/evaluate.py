from fastapi import APIRouter, Form, HTTPException
from pydantic import BaseModel
from typing import Dict
from src.evaluate import evaluate_model_on_file 

router = APIRouter(prefix = "/evaluate" , tags = ["Evaluación"])

class EvalOut(BaseModel):
    n_samples: int
    accuracy: float
    precision_macro: float
    recall_macro: float
    f1_macro: float
    f1_micro: float
    f1_weighted: float


class EvalIn(BaseModel):
    model_name: str
    file_name: str
    text_col: str
    label_col: str


# Endpoint para evaluar un modelo con un archivo
@router.post("/from-file")
def evaluate_from_file(body: EvalIn):
    try:
        res: Dict = evaluate_model_on_file(
            body.model_name, body.file_name, body.text_col, body.label_col
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))