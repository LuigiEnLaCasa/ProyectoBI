from fastapi import APIRouter, Form, HTTPException
from pydantic import BaseModel
from src.train_utils import train_from_file

router = APIRouter(prefix="/train", tags=["Re-Entrenamiento"])


#-------------
# Moldes 
#-------------

class RetrainIn(BaseModel):
    modelo_path: Optional[str] = None
    # Textos y labels deben tener la misma longitud
    textos: List[str]
    labels: List[int]
    
class RetrainOut(BaseModel):
    modelo_path: str
    best_params: Optional[Dict[str, float]] = None
    best_score: Optional[float] = None


#-------------
# Endpoints 
#-------------