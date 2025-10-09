from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict
from pydantic import BaseModel
from src.train_utils import retrain_with_samples

router = APIRouter(prefix="/retrain", tags=["Re-Entrenamiento"])


#-------------
# Moldes 
#-------------

class RetrainIn(BaseModel):
    base_file_path: str          # dataset base en /data
    text_col: str
    label_col: str
    textos: List[str]            # nuevos textos
    labels: List[int]            # nuevas etiquetas

class RetrainOut(BaseModel):
    model_path: str
    metadata: Dict

#-------------
# Endpoints 
#-------------

@router.post("/json", response_model=RetrainOut)
def retrain_with_json(body: RetrainIn):
    """
    Reentrena un modelo sumando nuevos textos/labels a un dataset base.
    Devuelve la ruta del nuevo modelo y metadatos de entrenamiento.
    """
    try:
        ruta, meta = retrain_with_samples(
            base_file_path=body.base_file_path,
            text_col=body.text_col,
            label_col=body.label_col,
            nuevos_textos=body.textos,
            nuevos_labels=body.labels,
        )
        return {"model_path": ruta, "metadata": meta}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))