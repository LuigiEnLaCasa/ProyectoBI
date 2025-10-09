# ----------------------------------------------------------------------
# Librerías
# ----------------------------------------------------------------------
from fastapi import FastAPI
from typing import List, Optional, Dict
from pydantic import BaseModel
from src.pipeline import predecir, probabilidades, listar_modelos, cargar_modelo
import numpy as np

# ----------------------------------------------------------------------
# Instanciación y clases base para la entrada y salida mood json
# ----------------------------------------------------------------------

# crea la aplicación FastAPI
app = FastAPI(title="ODS Classifier API", version="1.0.0")

# Moldes de entrada y salida 
class PredictIn(BaseModel):
    textos: List[str]
    modelo_path: Optional[str] = None

class PredictOut(BaseModel):
    texto: str
    prediccion: int
    confianza: float

class RetrainIn(BaseModel):
    textos: List[str]
    labels: List[int]
    
class RetrainOut(BaseModel):
    modelo_path: str
    best_params: Optional[Dict[str, float]] = None
    best_score: Optional[float] = None

# ----------------------------------------------------------------------
# Main endpoints
# ----------------------------------------------------------------------


# ruta básica de prueba
@app.get("/health")
def health():
    return {"status": "ok"}

# Mostrar los modelos de la carpeta /models
@app.get("/models")
def models():
    return {"modelos": listar_modelos()}

# Hacer una predicción con el model elegido (path)
@app.post("/predict", response_model=List[PredictOut])
def predict(body: PredictIn):
    modelos = listar_modelos()
    if not modelos:
        # no hay .pkl guardados aún
        return [PredictOut(texto=t, prediccion=-1, confianza=0.0) for t in body.textos]

    # usa el que indiquen o el último listado
    modelo_path = body.modelo_path or modelos[-1]
    pipe = cargar_modelo(modelo_path)

    y = predecir(pipe, body.textos)
    p = probabilidades(pipe, body.textos)
    conf = p.max(axis=1)

    return [PredictOut(texto=t, prediccion=int(lbl), confianza=float(c)) for t, lbl, c in zip(body.textos, y, conf)]