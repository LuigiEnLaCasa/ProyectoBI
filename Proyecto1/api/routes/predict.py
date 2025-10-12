import os
from fastapi import HTTPException
from fastapi import APIRouter
from typing import List, Optional
from pydantic import BaseModel
from src.pipeline import predecir, probabilidades, listar_modelos, cargar_modelo

router = APIRouter(prefix="/predict", tags=["Predicción"])
#-------------
# Moldes 
#-------------

# Moldes de entrada y salida 
class PredictIn(BaseModel):
    textos: List[str]
    modelo_path: Optional[str] = None

class PredictOut(BaseModel):
    texto: str
    prediccion: int
    confianza: float

#-------------
# Endpoints 
#-------------

# Mostrar los modelos de la carpeta /models
@router.get("/models")
def models():
    return {"modelos": listar_modelos()}


@router.post("/", response_model=List[PredictOut])
def predict(body: PredictIn):
    modelos = listar_modelos()
    if not modelos:
        return [PredictOut(texto=t, prediccion=-1, confianza=0.0) for t in body.textos]

    # si viene vacío, usa el último
    modelo_path = body.modelo_path or modelos[-1]

    # si es solo nombre (sin separador), asume carpeta models/
    if body.modelo_path and os.path.sep not in body.modelo_path:
        modelo_path = os.path.join("models", body.modelo_path)

    if not os.path.exists(modelo_path):
        raise HTTPException(status_code=400, detail=f"Modelo no encontrado: {modelo_path}")

    obj = cargar_modelo(modelo_path)  # {'model': pipe, 'metadata': {...}}
    pipe = obj["model"]

    y = predecir(pipe, body.textos)
    p = probabilidades(pipe, body.textos)
    conf = p.max(axis=1)

    return [PredictOut(texto=t, prediccion=int(lbl), confianza=float(c))
            for t, lbl, c in zip(body.textos, y, conf)]