# ----------------------------------------------------------------------
# Librerías
# ----------------------------------------------------------------------
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os

router = APIRouter(prefix="/files", tags=["Archivos"])

DATA_DIRECTORY = "data"
ALLOWED_EXT = {".csv", ".xlsx", ".xls"}

def ensure_data_dir():
    os.makedirs(DATA_DIRECTORY, exist_ok=True)

def is_allowed(filename: str) -> bool:
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXT

# ----------------------------------------------------------------------
# Endpoints
# ----------------------------------------------------------------------

# Listar archivos en la carpeta /data
@router.get("/list")
def list_files() :
    ensure_data_dir()
    files = []
    for fname in os.listdir(DATA_DIRECTORY):
        path = os.path.join(DATA_DIRECTORY, fname)
        if os.path.isfile(path) and is_allowed(fname):
            files.append(path)  # ej: "data/mi_dataset.xlsx"
    return {"archivos": files}

#Subir archivos a la carpeta /data
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)) :
    ensure_data_dir()

    if not is_allowed(file.filename):
        raise HTTPException(status_code=400,detail="Formato no soportado. Usa .csv, .xlsx o .xls")

    save_path = os.path.join(DATA_DIRECTORY, file.filename)

    if os.path.exists(save_path):
         raise HTTPException(400, detail="Ya existe un archivo con ese nombre.")
    content = await file.read()
    with open(save_path, "wb") as f:
        f.write(content)
    return {"message": "Archivo subido con éxito", "path": save_path, "size_bytes": len(content)}